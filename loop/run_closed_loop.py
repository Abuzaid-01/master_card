"""
Step 4: CLOSE THE LOOP — End-to-End Adversarial Active Learning Pipeline
Orchestrates the full closed-loop workflow:
  1. Partition Step 4 holdouts into Mining & Final Eval
  2. Multi-strategy model-aware probing against Round 1
  3. Blind spot extraction & failure mining
  4. Adversarial retraining (Round 2)
  5. Comparative evaluation (Round 1 vs Round 2) + Catastrophic Forgetting Audit
  6. Export consolidated report
"""

import os
import sys
import json
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

DEFEND_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "defend")
LOOP_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "loop")
SYNTHETIC_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "synthetic")


def load_original_training_data() -> dict:
    """Loads the original Step 3 training data for Round 2 augmentation."""
    from defend.data_splitter import split_and_preserve_holdout
    
    training_data = {}
    
    # Tabular
    tab_path = os.path.join(SYNTHETIC_DATA_DIR, "synthetic_tabular_card_testing.csv")
    if os.path.exists(tab_path):
        df = pd.read_csv(tab_path)
        if "velocity" not in df.columns:
            import numpy as np
            df["velocity"] = np.where(df["is_fraud"] == 1, 12.0, 2.0)
        df_tr, _, _ = split_and_preserve_holdout(df, dataset_name="tabular", verbose=False)
        training_data["tabular"] = df_tr
    
    # Text
    txt_path = os.path.join(SYNTHETIC_DATA_DIR, "synthetic_prompt_injections.csv")
    if os.path.exists(txt_path):
        df = pd.read_csv(txt_path)
        df_tr, _, _ = split_and_preserve_holdout(df, dataset_name="text", verbose=False)
        training_data["text"] = df_tr
    
    # Graph
    grp_path = os.path.join(SYNTHETIC_DATA_DIR, "synthetic_mule_graph.csv")
    if os.path.exists(grp_path):
        df = pd.read_csv(grp_path)
        df_tr, _, _ = split_and_preserve_holdout(df, dataset_name="graph", verbose=False)
        training_data["graph"] = df_tr
    
    return training_data


def load_baseline_validation_data() -> dict:
    """Loads the original Step 3 validation data for catastrophic forgetting checks."""
    from defend.data_splitter import split_and_preserve_holdout
    
    val_data = {}
    
    tab_path = os.path.join(SYNTHETIC_DATA_DIR, "synthetic_tabular_card_testing.csv")
    if os.path.exists(tab_path):
        df = pd.read_csv(tab_path)
        if "velocity" not in df.columns:
            import numpy as np
            df["velocity"] = np.where(df["is_fraud"] == 1, 12.0, 2.0)
        _, df_val, _ = split_and_preserve_holdout(df, dataset_name="tabular", verbose=False)
        val_data["tabular"] = df_val
    
    grp_path = os.path.join(SYNTHETIC_DATA_DIR, "synthetic_mule_graph.csv")
    if os.path.exists(grp_path):
        df = pd.read_csv(grp_path)
        _, df_val, _ = split_and_preserve_holdout(df, dataset_name="graph", verbose=False)
        val_data["graph"] = df_val
    
    return val_data


def run_closed_loop():
    """Runs the complete Step 4 closed-loop adversarial active learning pipeline."""
    print("=" * 60)
    print(" Mastercard Innovation Challenge 2026 — Step 4 Closed Loop")
    print("=" * 60)
    
    os.makedirs(LOOP_OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(LOOP_OUTPUT_DIR, "models"), exist_ok=True)
    
    # ── Phase 1: Partition Holdouts ──
    print("\n[Phase 1] Partitioning Step 4 holdouts into Mining & Final Eval sets...")
    from loop.holdout_partitioner import partition_all_holdouts
    partitions = partition_all_holdouts()
    
    # ── Phase 2: Mine Blind Spots ──
    print("\n[Phase 2] Mining Round 1 blind spots via multi-strategy model-aware probing...")
    from loop.blind_spot_extractor import extract_blind_spots
    blind_spot_results = extract_blind_spots(partitions, mining_strategy_seed=42)
    
    # ── Phase 3: Retrain Round 2 ──
    print("\n[Phase 3] Active adversarial retraining (Round 2)...")
    original_training = load_original_training_data()
    from loop.adversarial_retrainer import retrain_round2
    round2_models = retrain_round2(blind_spot_results, original_training)
    
    # ── Phase 4: Evaluate Round 1 vs Round 2 ──
    print("\n[Phase 4] Evaluating Round 1 vs Round 2 on unseen adversarial test set...")
    baseline_val = load_baseline_validation_data()
    from loop.loop_evaluator import evaluate_round_comparison
    evaluation = evaluate_round_comparison(round2_models, partitions, baseline_val, eval_strategy_seed=99)
    
    # ── Phase 5: Export Report ──
    print("\n[Phase 5] Exporting closed-loop report...")
    
    report = {
        "step4_closed_loop": {
            "holdout_partition_sizes": {},
            "blind_spot_mining": {},
            "round2_retraining": {},
            "round1_vs_round2": evaluation,
        }
    }
    
    # Populate partition sizes
    for name, part in partitions.items():
        report["step4_closed_loop"]["holdout_partition_sizes"][name] = {
            "mine_total": part["mine_total"],
            "mine_fraud": part["mine_fraud"],
            "eval_total": part["eval_total"],
            "eval_fraud": part["eval_fraud"],
        }
    
    # Populate blind spot mining stats
    for name, bs in blind_spot_results.items():
        report["step4_closed_loop"]["blind_spot_mining"][name] = {
            "n_fraud_probed": bs["n_fraud_probed"],
            "n_evaded": bs["n_evaded"],
            "evasion_rate": bs["evasion_rate"],
        }
    
    # Populate retraining stats
    for name, r2 in round2_models.items():
        report["step4_closed_loop"]["round2_retraining"][name] = {
            "original_train_size": r2.get("original_train_size", 0),
            "augmented_train_size": r2.get("augmented_train_size", 0),
            "adversarial_samples_added": r2.get("adversarial_samples_added", 0) or r2.get("missed_prompts_added", 0),
        }
    
    report_path = os.path.join(LOOP_OUTPUT_DIR, "closed_loop_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n[Success] Step 4 Closed Loop complete! Report: {report_path}")
    return report


if __name__ == "__main__":
    run_closed_loop()
