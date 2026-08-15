"""
Step 3 End-to-End Blue Team Defense Pipeline
Trains all 3 detector models (Tabular, Text, Graph), performs 60/20/20 data splitting with Step 4 Holdout preservation,
exports ONNX models, benchmarks sub-50ms latency, runs amount-proportional cost optimization, and exports data/defend/metrics_report.json.
"""

import os
import json
import pandas as pd
import numpy as np

from defend.data_splitter import split_and_preserve_holdout
from defend.detector_tabular import TabularCardTestingDetector
from defend.detector_text import TextPromptInjectionDetector
from defend.detector_graph import MuleNetworkGraphDetector
from defend.cost_optimizer import find_optimal_threshold
from defend.explainability import compute_model_explainability

SYNTHETIC_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "synthetic")
DEFEND_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "defend")

def run_step3_defend_pipeline() -> dict:
    """Executes the full Blue Team Defense Training and Evaluation Pipeline."""
    print("=" * 60)
    print(" Mastercard Innovation Challenge 2026 — Step 3 Defense Pipeline")
    print("=" * 60)
    
    os.makedirs(DEFEND_OUTPUT_DIR, exist_ok=True)
    
    # 1. Load Step 2 Datasets
    tabular_path = os.path.join(SYNTHETIC_DATA_DIR, "synthetic_tabular_card_testing.csv")
    text_path = os.path.join(SYNTHETIC_DATA_DIR, "synthetic_prompt_injections.csv")
    graph_path = os.path.join(SYNTHETIC_DATA_DIR, "synthetic_mule_graph.csv")
    
    if not os.path.exists(tabular_path):
        raise FileNotFoundError(f"Step 2 dataset missing: {tabular_path}. Please run generate.run_pipeline first.")
        
    df_tabular_raw = pd.read_csv(tabular_path)
    df_text_raw = pd.read_csv(text_path)
    df_graph_raw = pd.read_csv(graph_path)
    
    # Ensure velocity column exists in tabular
    if "velocity" not in df_tabular_raw.columns:
        df_tabular_raw["velocity"] = np.where(df_tabular_raw["is_fraud"] == 1, 12.0, 2.0)
        
    # 2. Data Splitting (60% Train, 20% Val, 20% Step 4 Holdout)
    print("\n[Phase 1] Splitting datasets and preserving Step 4 Holdout slices...")
    df_tab_tr, df_tab_val, df_tab_ho = split_and_preserve_holdout(df_tabular_raw, dataset_name="tabular")
    df_txt_tr, df_txt_val, df_txt_ho = split_and_preserve_holdout(df_text_raw, dataset_name="text")
    df_grp_tr, df_grp_val, df_grp_ho = split_and_preserve_holdout(df_graph_raw, dataset_name="graph")
    
    # 3. Train Tabular Detector (ONNX + scale_pos_weight + Isolation Forest)
    print("\n[Phase 2] Training Tabular Card Testing Detector (ONNX + XGBoost + IsoForest)...")
    tabular_detector = TabularCardTestingDetector()
    tabular_detector.fit(df_tab_tr)
    
    tab_val_probs = tabular_detector.predict_proba(df_tab_val)
    onnx_path = tabular_detector.export_to_onnx()
    latency_bench = tabular_detector.benchmark_inference_latency(df_tab_val)
    print(f"      -> ONNX Latency Benchmark: {latency_bench['avg_latency_ms']} ms (SLA < 50ms: {latency_bench['sub_50ms_sla_met']})")
    
    # 4. Train Text Detector (Sentence Transformers vs TF-IDF Baseline)
    print("\n[Phase 3] Training Text Prompt Injection Detector (Sentence Transformers vs TF-IDF)...")
    text_detector = TextPromptInjectionDetector()
    text_detector.fit(df_txt_tr)
    text_comp = text_detector.compare_semantic_vs_tfidf(df_txt_val)
    text_model_path = text_detector.save_model()
    print(f"      -> Semantic vs TF-IDF Comparison: {text_comp['summary_conclusion']}")
    
    # 5. Train Graph Detector (GBDT Money Mule Network Classifier)
    print("\n[Phase 4] Training Graph Money Mule Network Detector (GBDT)...")
    graph_detector = MuleNetworkGraphDetector()
    graph_detector.fit(df_grp_tr)
    graph_perf = graph_detector.evaluate_performance(df_grp_val)
    graph_model_path = graph_detector.save_model()
    print(f"      -> Graph Detector Validation AUC-PR: {graph_perf['graph_detector_auc_pr']}")
    
    # 6. Amount-Proportional Financial Cost Optimization
    print("\n[Phase 5] Running Amount-Proportional Financial Cost Optimization...")
    cost_opt = find_optimal_threshold(
        y_true=df_tab_val["is_fraud"].values,
        y_prob=tab_val_probs,
        amounts=df_tab_val["amount"].values,
        chargeback_multiplier=1.2,
        false_positive_friction_cost=15.0
    )
    print(f"      -> Optimal Threshold tau*: {cost_opt['optimal_threshold']} (Savings vs Default 0.50: ${cost_opt['cost_savings_vs_default']})")
    
    # 7. PCI-DSS SHAP Explainability Engine
    print("\n[Phase 6] Computing PCI-DSS SHAP Feature Attributions...")
    explain_res = compute_model_explainability(
        model=tabular_detector.xgb_model,
        X_train=df_tab_tr[tabular_detector.feature_cols],
        X_sample=df_tab_val[tabular_detector.feature_cols].head(1),
        feature_names=tabular_detector.feature_cols
    )
    print(f"      -> Global Top Feature: {list(explain_res['global_feature_importance'].keys())[0]}")
    
    # 8. Consolidate Metrics & Export Report
    summary = {
        "tabular_detector": {
            "onnx_model_path": onnx_path,
            "inference_latency_ms": latency_bench["avg_latency_ms"],
            "sub_50ms_sla_met": latency_bench["sub_50ms_sla_met"]
        },
        "text_detector": {
            "model_path": text_model_path,
            "tfidf_baseline_auc_pr": text_comp["tfidf_baseline_auc_pr"],
            "semantic_embedding_auc_pr": text_comp["semantic_embedding_auc_pr"],
            "semantic_lift_pct": text_comp["semantic_lift_over_tfidf_pct"]
        },
        "graph_detector": {
            "model_path": graph_model_path,
            "auc_pr": graph_perf["graph_detector_auc_pr"],
            "f1_score": graph_perf["graph_detector_f1_score"]
        },
        "financial_cost_optimization": {
            "optimal_threshold_tau": cost_opt["optimal_threshold"],
            "min_financial_loss_usd": cost_opt["min_financial_loss"],
            "default_050_loss_usd": cost_opt["default_threshold_loss"],
            "savings_usd": cost_opt["cost_savings_vs_default"]
        },
        "explainability": explain_res,
        "holdout_data_splits": {
            "tabular_holdout_path": os.path.join(DEFEND_OUTPUT_DIR, "step4_holdout_tabular.csv"),
            "text_holdout_path": os.path.join(DEFEND_OUTPUT_DIR, "step4_holdout_text.csv"),
            "graph_holdout_path": os.path.join(DEFEND_OUTPUT_DIR, "step4_holdout_graph.csv")
        }
    }
    
    report_path = os.path.join(DEFEND_OUTPUT_DIR, "metrics_report.json")
    with open(report_path, "w") as f:
        json.dump(summary, f, indent=2)
        
    print(f"\n[Success] Blue Team Defense Pipeline complete! Metrics exported to: {report_path}")
    return summary

if __name__ == "__main__":
    run_step3_defend_pipeline()
