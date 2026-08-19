"""
Loop Evaluator: Compares Round 1 vs Round 2 (and multi-round) performance on:
  1. Unseen adversarial final test set (evasion robustness gain with calibrated threshold)
  2. Original Step 3 baseline validation set (catastrophic forgetting check)
Reports raw sample counts alongside percentages and calibrated decision thresholds.
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.metrics import average_precision_score, f1_score

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from generate.generator_tabular import TABULAR_FEATURE_COLS


def _find_optimal_threshold(y_true: np.ndarray, y_prob: np.ndarray, default_th: float = 0.50) -> float:
    """Finds optimal decision threshold maximizing balanced F1 + Youden's J statistic."""
    if len(np.unique(y_true)) < 2:
        return default_th
    thresholds = np.linspace(0.05, 0.95, 91)
    best_score = -999.0
    best_th = default_th
    for th in thresholds:
        y_pred = (y_prob >= th).astype(int)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fn = np.sum((y_pred == 0) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        tn = np.sum((y_pred == 0) & (y_true == 0))
        tpr = tp / max(1, tp + fn)
        fpr = fp / max(1, fp + tn)
        score = 0.7 * f1 + 0.3 * (tpr - fpr)
        if score > best_score:
            best_score = score
            best_th = float(th)
    return round(best_th, 4)


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
    Uses calibrated operational thresholds for each round.
    """
    from loop.multi_strategy_prober import MultiStrategyProber
    prober = MultiStrategyProber()
    report = {}

    # ══════════════════════════════════════════
    # 1. TABULAR EVALUATION
    # ══════════════════════════════════════════
    if "tabular" in round2_models and "tabular" in partitions:
        print("\n[Loop Evaluator] TABULAR: Round 1 vs Round 2 Comparison...")
        feature_cols = list(TABULAR_FEATURE_COLS)
        df_eval = partitions["tabular"]["df_eval"].copy()
        for col in feature_cols:
            if col not in df_eval.columns:
                df_eval[col] = 0.0

        df_eval_fraud = df_eval[df_eval["is_fraud"] == 1].copy()
        df_eval_legit = df_eval[df_eval["is_fraud"] == 0].copy()

        # Baseline calibration
        r1_th = 0.50
        r2_th = 0.50
        tab_baseline = {}
        r2_model = round2_models["tabular"]["model"]

        if "tabular" in baseline_val_data:
            df_base = baseline_val_data["tabular"].copy()
            for col in feature_cols:
                if col not in df_base.columns:
                    df_base[col] = 0.0
            y_base = df_base["is_fraud"].values
            X_base = df_base[feature_cols].values.astype(np.float32)
            r1_base_probs = prober._tabular_predict_proba(X_base)
            r2_base_probs = r2_model.predict_proba(X_base)[:, 1]
            
            r1_th = _find_optimal_threshold(y_base, r1_base_probs, default_th=0.50)
            r2_th = _find_optimal_threshold(y_base, r2_base_probs, default_th=0.50)
            
            r1_base_fpr = float(np.round((r1_base_probs[y_base == 0] >= r1_th).mean(), 4))
            r2_base_fpr = float(np.round((r2_base_probs[y_base == 0] >= r2_th).mean(), 4))
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

        # Independently perturb eval fraud with alternate strategy weighting against R1 threshold
        df_eval_fraud_adv = prober.probe_tabular(
            df_eval_fraud, threshold=r1_th, strategy_seed=eval_strategy_seed
        )
        
        # Reconstruct full eval set with adversarial fraud + original legit
        df_eval_adv = pd.concat([df_eval_fraud_adv, df_eval_legit], ignore_index=True)
        y_true = df_eval_adv["is_fraud"].values
        X_eval = df_eval_adv[feature_cols].values.astype(np.float32)

        # Round 1 vs Round 2 on adversarial test set
        r1_probs = prober._tabular_predict_proba(X_eval)
        r2_probs = r2_model.predict_proba(X_eval)[:, 1]

        r1_auc = float(np.round(average_precision_score(y_true, r1_probs), 4))
        r2_auc = float(np.round(average_precision_score(y_true, r2_probs), 4))

        r1_caught = int((r1_probs[y_true == 1] >= r1_th).sum())
        r2_caught = int((r2_probs[y_true == 1] >= r2_th).sum())
        r1_total_fraud = int((y_true == 1).sum())

        report["tabular"] = {
            "adversarial_eval": {
                "n_fraud_total": r1_total_fraud,
                "n_legit_total": int((y_true == 0).sum()),
                "r1_caught": r1_caught, "r1_catch_rate": float(np.round(r1_caught / max(1, r1_total_fraud), 4)),
                "r2_caught": r2_caught, "r2_catch_rate": float(np.round(r2_caught / max(1, r1_total_fraud), 4)),
                "net_caught_delta": r2_caught - r1_caught,
                "r1_auc_pr": r1_auc, "r2_auc_pr": r2_auc,
                "auc_delta": float(np.round(r2_auc - r1_auc, 4)),
                "r1_threshold": r1_th, "r2_threshold": r2_th,
            },
            "catastrophic_forgetting_check": tab_baseline,
        }
        print(f"      -> Adversarial: R1 caught {r1_caught}/{r1_total_fraud} | R2 caught {r2_caught}/{r1_total_fraud} | Δ={r2_caught-r1_caught:+d}")
        print(f"      -> AUC-PR: R1={r1_auc} → R2={r2_auc} (Δ={r2_auc-r1_auc:+.4f})")
        if tab_baseline:
            print(f"      -> Baseline FPR: R1={tab_baseline['baseline_r1_fpr']} → R2={tab_baseline['baseline_r2_fpr']} "
                  f"(Δ={tab_baseline['baseline_fpr_delta']:+.4f}) | Forgetting={tab_baseline['catastrophic_forgetting']}")

    # ══════════════════════════════════════════
    # 2. GRAPH EVALUATION
    # ══════════════════════════════════════════
    if "graph" in round2_models and "graph" in partitions:
        print("\n[Loop Evaluator] GRAPH: Round 1 vs Round 2 Comparison...")
        df_eval = partitions["graph"]["df_eval"]
        df_eval_fraud = df_eval[df_eval["is_fraud"] == 1].copy()
        df_eval_legit = df_eval[df_eval["is_fraud"] == 0].copy()

        from generate.generator_graph import GRAPH_FEATURE_COLS
        graph_features = list(GRAPH_FEATURE_COLS)

        r2_model = round2_models["graph"]["model"]

        # Baseline calibration
        r1_th = 0.50
        r2_th = 0.50
        graph_baseline = {}

        if "graph" in baseline_val_data:
            df_base = baseline_val_data["graph"]
            y_base = df_base["is_fraud"].values
            X_base = df_base[graph_features].values.astype(float)
            r1_base_probs = prober.graph_model.predict_proba(X_base)[:, 1] if prober.graph_model else np.zeros(len(X_base))
            r2_base_probs = r2_model.predict_proba(X_base)[:, 1]
            
            r1_th = _find_optimal_threshold(y_base, r1_base_probs, default_th=0.50)
            r2_th = _find_optimal_threshold(y_base, r2_base_probs, default_th=0.50)
            
            r1_base_auc = float(np.round(average_precision_score(y_base, r1_base_probs), 4))
            r2_base_auc = float(np.round(average_precision_score(y_base, r2_base_probs), 4))
            graph_baseline = {
                "baseline_r1_auc_pr": r1_base_auc, "baseline_r2_auc_pr": r2_base_auc,
                "baseline_auc_delta": float(np.round(r2_base_auc - r1_base_auc, 4)),
                "catastrophic_forgetting": bool(r2_base_auc < r1_base_auc - 0.05),
            }

        df_eval_fraud_adv = prober.probe_graph(
            df_eval_fraud, threshold=r1_th, strategy_seed=eval_strategy_seed
        )
        df_eval_adv = pd.concat([df_eval_fraud_adv, df_eval_legit], ignore_index=True)
        y_true = df_eval_adv["is_fraud"].values
        X_eval = df_eval_adv[graph_features].values.astype(float)

        r1_probs = prober.graph_model.predict_proba(X_eval)[:, 1] if prober.graph_model else np.zeros(len(X_eval))
        r2_probs = r2_model.predict_proba(X_eval)[:, 1]

        r1_auc = float(np.round(average_precision_score(y_true, r1_probs), 4))
        r2_auc = float(np.round(average_precision_score(y_true, r2_probs), 4))

        # Evaluate at calibrated operational thresholds
        r1_caught = int((r1_probs[y_true == 1] >= r1_th).sum())
        r2_caught = int((r2_probs[y_true == 1] >= r2_th).sum())
        r1_total_fraud = int((y_true == 1).sum())

        report["graph"] = {
            "adversarial_eval": {
                "n_fraud_total": r1_total_fraud,
                "n_legit_total": int((y_true == 0).sum()),
                "r1_caught": r1_caught, "r1_catch_rate": float(np.round(r1_caught / max(1, r1_total_fraud), 4)),
                "r2_caught": r2_caught, "r2_catch_rate": float(np.round(r2_caught / max(1, r1_total_fraud), 4)),
                "net_caught_delta": r2_caught - r1_caught,
                "r1_auc_pr": r1_auc, "r2_auc_pr": r2_auc,
                "auc_delta": float(np.round(r2_auc - r1_auc, 4)),
                "r1_threshold": r1_th, "r2_threshold": r2_th,
            },
            "catastrophic_forgetting_check": graph_baseline,
        }
        print(f"      -> Adversarial: R1 caught {r1_caught}/{r1_total_fraud} (th={r1_th}) | R2 caught {r2_caught}/{r1_total_fraud} (th={r2_th}) | Δ={r2_caught-r1_caught:+d}")
        print(f"      -> AUC-PR: R1={r1_auc} → R2={r2_auc} (Δ={r2_auc-r1_auc:+.4f})")

    # ══════════════════════════════════════════
    # 3. TEXT EVALUATION
    # ══════════════════════════════════════════
    if "text" in round2_models and "text" in partitions:
        print("\n[Loop Evaluator] TEXT: Round 1 vs Round 2 Comparison...")
        df_eval = partitions["text"]["df_eval"]
        y_true = df_eval["is_fraud"].values

        r1_detector = prober.text_detector
        r2_detector = round2_models["text"]["detector"]

        r1_th = getattr(r1_detector, "optimal_threshold", 0.54) if r1_detector else 0.54
        r2_th = getattr(r2_detector, "optimal_threshold", 0.54) if r2_detector else 0.54

        if r1_detector and hasattr(r1_detector, "predict_proba_semantic"):
            r1_probs = r1_detector.predict_proba_semantic(df_eval)
        else:
            r1_probs = np.zeros(len(df_eval))

        if r2_detector and hasattr(r2_detector, "predict_proba_semantic"):
            r2_probs = r2_detector.predict_proba_semantic(df_eval)
        else:
            r2_probs = np.zeros(len(df_eval))

        r1_auc = float(np.round(average_precision_score(y_true, r1_probs), 4)) if len(np.unique(y_true)) > 1 else 1.0
        r2_auc = float(np.round(average_precision_score(y_true, r2_probs), 4)) if len(np.unique(y_true)) > 1 else 1.0

        r1_caught = int((r1_probs[y_true == 1] >= r1_th).sum())
        r2_caught = int((r2_probs[y_true == 1] >= r2_th).sum())
        r1_total_fraud = int((y_true == 1).sum())

        report["text"] = {
            "adversarial_eval": {
                "n_fraud_total": r1_total_fraud,
                "r1_caught": r1_caught, "r1_catch_rate": float(np.round(r1_caught / max(1, r1_total_fraud), 4)),
                "r2_caught": r2_caught, "r2_catch_rate": float(np.round(r2_caught / max(1, r1_total_fraud), 4)),
                "net_caught_delta": r2_caught - r1_caught,
                "r1_auc_pr": r1_auc, "r2_auc_pr": r2_auc,
                "auc_delta": float(np.round(r2_auc - r1_auc, 4)),
                "r1_threshold": r1_th, "r2_threshold": r2_th,
            }
        }
        print(f"      -> R1 caught {r1_caught}/{r1_total_fraud} (th={r1_th}) | R2 caught {r2_caught}/{r1_total_fraud} (th={r2_th}) | Δ={r2_caught-r1_caught:+d}")
        print(f"      -> AUC-PR: R1={r1_auc} → R2={r2_auc} (Δ={r2_auc-r1_auc:+.4f})")

    return report
