"""
Loop Evaluator: Compares Round 1 vs Round 2 (and multi-round) performance on:
  1. Unseen adversarial final test set (evasion robustness gain)
  2. Original Step 3 baseline validation set (catastrophic forgetting check)
Reports raw sample counts alongside percentages.
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import Dict, Any
from sklearn.metrics import average_precision_score, f1_score

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from generate.generator_tabular import TABULAR_FEATURE_COLS


def evaluate_round_comparison(
    round2_models: dict,
    partitions: dict,
    baseline_val_data: dict,
    eval_strategy_seed: int = 99
) -> Dict[str, Any]:
    """
    Evaluates Round 1 vs Round 2 on:
    1. df_eval adversarial (independently perturbed unseen fraud)
    2. Baseline validation (catastrophic forgetting check)
    """
    from loop.multi_strategy_prober import MultiStrategyProber
    prober = MultiStrategyProber()
    report = {}

    # ── TABULAR ──
    if "tabular" in round2_models and "tabular" in partitions:
        print("\n[Loop Evaluator] TABULAR: Round 1 vs Round 2 Comparison...")
        feature_cols = list(TABULAR_FEATURE_COLS)
        df_eval = partitions["tabular"]["df_eval"].copy()
        for col in feature_cols:
            if col not in df_eval.columns:
                df_eval[col] = 0.0

        df_eval_fraud = df_eval[df_eval["is_fraud"] == 1].copy()
        df_eval_legit = df_eval[df_eval["is_fraud"] == 0].copy()

        # Independently perturb eval fraud with alternate strategy weighting
        df_eval_fraud_adv = prober.probe_tabular(
            df_eval_fraud, threshold=0.5, strategy_seed=eval_strategy_seed
        )
        
        # Reconstruct full eval set with adversarial fraud + original legit
        df_eval_adv = pd.concat([df_eval_fraud_adv, df_eval_legit], ignore_index=True)
        y_true = df_eval_adv["is_fraud"].values
        X_eval = df_eval_adv[feature_cols].values.astype(np.float32)

        # Round 1 predictions
        r1_probs = prober._tabular_predict_proba(X_eval)
        r1_auc = float(np.round(average_precision_score(y_true, r1_probs), 4))
        r1_caught = int((r1_probs[y_true == 1] >= 0.5).sum())
        r1_total_fraud = int((y_true == 1).sum())

        # Round 2 predictions
        r2_model = round2_models["tabular"]["model"]
        r2_probs = r2_model.predict_proba(X_eval)[:, 1]
        r2_auc = float(np.round(average_precision_score(y_true, r2_probs), 4))
        r2_caught = int((r2_probs[y_true == 1] >= 0.5).sum())

        # Catastrophic forgetting check on baseline
        tab_baseline = {}
        if "tabular" in baseline_val_data:
            df_base = baseline_val_data["tabular"].copy()
            for col in feature_cols:
                if col not in df_base.columns:
                    df_base[col] = 0.0
            y_base = df_base["is_fraud"].values
            X_base = df_base[feature_cols].values.astype(np.float32)
            r1_base_probs = prober._tabular_predict_proba(X_base)
            r2_base_probs = r2_model.predict_proba(X_base)[:, 1]
            
            r1_base_fpr = float(np.round((r1_base_probs[y_base == 0] >= 0.5).mean(), 4))
            r2_base_fpr = float(np.round((r2_base_probs[y_base == 0] >= 0.5).mean(), 4))
            r1_base_auc = float(np.round(average_precision_score(y_base, r1_base_probs), 4))
            r2_base_auc = float(np.round(average_precision_score(y_base, r2_base_probs), 4))
            
            tab_baseline = {
                "baseline_r1_auc_pr": r1_base_auc,
                "baseline_r2_auc_pr": r2_base_auc,
                "baseline_auc_delta": float(np.round(r2_base_auc - r1_base_auc, 4)),
                "baseline_r1_fpr": r1_base_fpr,
                "baseline_r2_fpr": r2_base_fpr,
                "baseline_fpr_delta": float(np.round(r2_base_fpr - r1_base_fpr, 4)),
                "catastrophic_forgetting": bool(r2_base_auc < r1_base_auc - 0.05),
            }

        report["tabular"] = {
            "adversarial_eval": {
                "n_fraud_total": r1_total_fraud,
                "n_legit_total": int((y_true == 0).sum()),
                "r1_caught": r1_caught, "r1_catch_rate": float(np.round(r1_caught / max(1, r1_total_fraud), 4)),
                "r2_caught": r2_caught, "r2_catch_rate": float(np.round(r2_caught / max(1, r1_total_fraud), 4)),
                "net_caught_delta": r2_caught - r1_caught,
                "r1_auc_pr": r1_auc, "r2_auc_pr": r2_auc,
                "auc_delta": float(np.round(r2_auc - r1_auc, 4)),
            },
            "catastrophic_forgetting_check": tab_baseline,
        }
        print(f"      -> Adversarial: R1 caught {r1_caught}/{r1_total_fraud} | R2 caught {r2_caught}/{r1_total_fraud} | Δ={r2_caught-r1_caught}")
        print(f"      -> AUC-PR: R1={r1_auc} → R2={r2_auc} (Δ={r2_auc-r1_auc:+.4f})")
        if tab_baseline:
            print(f"      -> Baseline FPR: R1={tab_baseline['baseline_r1_fpr']} → R2={tab_baseline['baseline_r2_fpr']} "
                  f"(Δ={tab_baseline['baseline_fpr_delta']:+.4f}) | Forgetting={tab_baseline['catastrophic_forgetting']}")

    # ── GRAPH ──
    if "graph" in round2_models and "graph" in partitions:
        print("\n[Loop Evaluator] GRAPH: Round 1 vs Round 2 Comparison...")
        df_eval = partitions["graph"]["df_eval"]
        df_eval_fraud = df_eval[df_eval["is_fraud"] == 1].copy()
        df_eval_legit = df_eval[df_eval["is_fraud"] == 0].copy()

        df_eval_fraud_adv = prober.probe_graph(
            df_eval_fraud, threshold=0.5, strategy_seed=eval_strategy_seed
        )
        df_eval_adv = pd.concat([df_eval_fraud_adv, df_eval_legit], ignore_index=True)
        y_true = df_eval_adv["is_fraud"].values
        
        graph_features = [c for c in ["amount", "sender_in_degree", "sender_out_degree",
                                       "receiver_in_degree", "receiver_out_degree",
                                       "receiver_mule_funnel_score",
                                       "pass_through_delay_sec"] if c in df_eval_adv.columns]
        X_eval = df_eval_adv[graph_features].values.astype(float)

        r1_probs = prober.graph_model.predict_proba(X_eval)[:, 1] if prober.graph_model else np.zeros(len(X_eval))
        r1_auc = float(np.round(average_precision_score(y_true, r1_probs), 4))
        r1_caught = int((r1_probs[y_true == 1] >= 0.5).sum())
        r1_total_fraud = int((y_true == 1).sum())

        r2_model = round2_models["graph"]["model"]
        r2_probs = r2_model.predict_proba(X_eval)[:, 1]
        r2_auc = float(np.round(average_precision_score(y_true, r2_probs), 4))
        r2_caught = int((r2_probs[y_true == 1] >= 0.5).sum())

        # Catastrophic forgetting
        graph_baseline = {}
        if "graph" in baseline_val_data:
            df_base = baseline_val_data["graph"]
            y_base = df_base["is_fraud"].values
            X_base = df_base[graph_features].values.astype(float)
            r1_base_probs = prober.graph_model.predict_proba(X_base)[:, 1] if prober.graph_model else np.zeros(len(X_base))
            r2_base_probs = r2_model.predict_proba(X_base)[:, 1]
            r1_base_auc = float(np.round(average_precision_score(y_base, r1_base_probs), 4))
            r2_base_auc = float(np.round(average_precision_score(y_base, r2_base_probs), 4))
            graph_baseline = {
                "baseline_r1_auc_pr": r1_base_auc, "baseline_r2_auc_pr": r2_base_auc,
                "baseline_auc_delta": float(np.round(r2_base_auc - r1_base_auc, 4)),
                "catastrophic_forgetting": bool(r2_base_auc < r1_base_auc - 0.05),
            }

        report["graph"] = {
            "adversarial_eval": {
                "n_fraud_total": r1_total_fraud,
                "n_legit_total": int((y_true == 0).sum()),
                "r1_caught": r1_caught, "r1_catch_rate": float(np.round(r1_caught / max(1, r1_total_fraud), 4)),
                "r2_caught": r2_caught, "r2_catch_rate": float(np.round(r2_caught / max(1, r1_total_fraud), 4)),
                "net_caught_delta": r2_caught - r1_caught,
                "r1_auc_pr": r1_auc, "r2_auc_pr": r2_auc,
                "auc_delta": float(np.round(r2_auc - r1_auc, 4)),
            },
            "catastrophic_forgetting_check": graph_baseline,
        }
        print(f"      -> Adversarial: R1 caught {r1_caught}/{r1_total_fraud} | R2 caught {r2_caught}/{r1_total_fraud} | Δ={r2_caught-r1_caught}")
        print(f"      -> AUC-PR: R1={r1_auc} → R2={r2_auc} (Δ={r2_auc-r1_auc:+.4f})")

    # ── TEXT ──
    if "text" in round2_models and "text" in partitions:
        print("\n[Loop Evaluator] TEXT: Round 1 vs Round 2 Comparison...")
        df_eval = partitions["text"]["df_eval"]
        y_true = df_eval["is_fraud"].values

        # Round 1: use prober's saved text detector
        r1_result = prober.probe_text_evasion_rate(df_eval[df_eval["is_fraud"] == 1], threshold=0.5)
        r1_total_fraud = r1_result["n_fraud"]
        r1_caught = r1_total_fraud - r1_result["n_missed"]

        # Round 2: use retrained detector
        r2_det = round2_models["text"]["detector"]
        r2_probs = r2_det.predict_proba_semantic(df_eval)
        r2_caught = int((r2_probs[y_true == 1] >= r2_det.optimal_threshold).sum())
        
        r2_auc = float(np.round(average_precision_score(y_true, r2_probs), 4))
        
        # Round 1 AUC on same set
        from defend.detector_text import TextPromptInjectionDetector
        r1_det = TextPromptInjectionDetector()
        r1_data = prober.text_detector
        if isinstance(r1_data, dict):
            r1_det.tfidf_vectorizer = r1_data.get("tfidf_vectorizer")
            r1_det.tfidf_model = r1_data.get("tfidf_model")
            r1_det.calibrated_classifier = r1_data.get("calibrated_classifier")
            r1_det.optimal_threshold = r1_data.get("optimal_threshold", 0.5)
            r1_det.attack_embeddings = r1_data.get("attack_embeddings")
            r1_det.legit_embeddings = r1_data.get("legit_embeddings")
            r1_det._init_sentence_transformer()
        r1_probs = r1_det.predict_proba_semantic(df_eval)
        r1_auc = float(np.round(average_precision_score(y_true, r1_probs), 4))

        report["text"] = {
            "adversarial_eval": {
                "n_fraud_total": r1_total_fraud,
                "r1_caught": r1_caught, "r1_catch_rate": float(np.round(r1_caught / max(1, r1_total_fraud), 4)),
                "r2_caught": r2_caught, "r2_catch_rate": float(np.round(r2_caught / max(1, r1_total_fraud), 4)),
                "net_caught_delta": r2_caught - r1_caught,
                "r1_auc_pr": r1_auc, "r2_auc_pr": r2_auc,
                "auc_delta": float(np.round(r2_auc - r1_auc, 4)),
            },
        }
        print(f"      -> R1 caught {r1_caught}/{r1_total_fraud} | R2 caught {r2_caught}/{r1_total_fraud} | Δ={r2_caught-r1_caught}")
        print(f"      -> AUC-PR: R1={r1_auc} → R2={r2_auc} (Δ={r2_auc-r1_auc:+.4f})")

    return report
