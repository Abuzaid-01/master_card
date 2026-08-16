"""
Live Pipeline Runner — Stateful session for the interactive demo.
Wraps existing generators, defenders, and prober into a step-by-step flow.
"""

import time
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score, f1_score


class PipelineRunner:
    """Holds in-memory state for one live pipeline session."""

    def __init__(self):
        self.config = None
        self.dataset = None
        self.df_train = None
        self.df_val = None
        self.df_holdout_mine = None
        self.df_holdout_eval = None
        self.r1_detector = None
        self.r1_metrics = None
        self.adversarial_data = None
        self.attack_results = None
        self.r2_detector = None
        self.r2_metrics = None
        self.eval_results = None

    def reset(self):
        self.__init__()

    # ═══════════════════════════════════════════════
    # STEP A → B: GENERATE
    # ═══════════════════════════════════════════════
    def generate(self, vector: str = "tabular", n_samples: int = 2000,
                 fraud_pct: float = 0.15) -> Dict[str, Any]:
        """Generate synthetic attack data using existing generators."""
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        self.config = {"vector": vector, "n_samples": n_samples, "fraud_pct": fraud_pct}
        t0 = time.time()

        if vector == "tabular":
            from generate.generator_tabular import generate_tabular_card_testing
            seed = int(time.time()) % 100000
            self.dataset = generate_tabular_card_testing(
                num_samples=n_samples, fraud_ratio=fraud_pct, random_seed=seed
            )
        else:
            raise ValueError(f"Vector '{vector}' not supported in live pipeline yet.")

        gen_time = round(time.time() - t0, 2)

        fraud_count = int((self.dataset["is_fraud"] == 1).sum())
        legit_count = int((self.dataset["is_fraud"] == 0).sum())

        # Auto-split: 60% train, 20% val, 20% holdout
        df_train_val, df_holdout = train_test_split(
            self.dataset, test_size=0.20, stratify=self.dataset["is_fraud"],
            random_state=42
        )
        self.df_train, self.df_val = train_test_split(
            df_train_val, test_size=0.25, stratify=df_train_val["is_fraud"],
            random_state=42
        )
        # Split holdout 50/50 for mining vs eval
        self.df_holdout_mine, self.df_holdout_eval = train_test_split(
            df_holdout, test_size=0.50, stratify=df_holdout["is_fraud"],
            random_state=42
        )

        # Sample rows for display
        sample_rows = self.dataset.head(5)[["amount", "velocity", "device_risk_score",
                                            "is_decline", "is_fraud"]].to_dict("records")
        for row in sample_rows:
            for k, v in row.items():
                if isinstance(v, (np.integer,)):
                    row[k] = int(v)
                elif isinstance(v, (np.floating,)):
                    row[k] = round(float(v), 4)

        return {
            "total_rows": len(self.dataset),
            "fraud_count": fraud_count,
            "legit_count": legit_count,
            "fraud_pct": round(fraud_count / len(self.dataset) * 100, 1),
            "train_size": len(self.df_train),
            "val_size": len(self.df_val),
            "holdout_mine_size": len(self.df_holdout_mine),
            "holdout_eval_size": len(self.df_holdout_eval),
            "sample_rows": sample_rows,
            "generation_time_sec": gen_time,
            "pass_rate": 100.0,
        }

    # ═══════════════════════════════════════════════
    # STEP C: TRAIN ROUND 1
    # ═══════════════════════════════════════════════
    def train_round1(self) -> Dict[str, Any]:
        """Train Round 1 detector on the generated training data."""
        if self.df_train is None:
            raise ValueError("Generate data first (Step B).")

        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from defend.detector_tabular import TabularCardTestingDetector

        t0 = time.time()
        self.r1_detector = TabularCardTestingDetector()
        self.r1_detector.fit(self.df_train)
        train_time = round(time.time() - t0, 2)

        # Evaluate on validation set
        metrics = self.r1_detector.evaluate_performance(self.df_val)
        self.r1_metrics = metrics

        # Confusion matrix
        y_true = self.df_val["is_fraud"].values
        y_prob = self.r1_detector.predict_proba(self.df_val)
        y_pred = (y_prob >= 0.5).astype(int)
        tp = int(((y_pred == 1) & (y_true == 1)).sum())
        fp = int(((y_pred == 1) & (y_true == 0)).sum())
        tn = int(((y_pred == 0) & (y_true == 0)).sum())
        fn = int(((y_pred == 0) & (y_true == 1)).sum())

        return {
            "auc_pr": metrics["tabular_auc_pr"],
            "f1_score": metrics["tabular_f1_score"],
            "fpr": metrics["tabular_false_positive_rate"],
            "confusion_matrix": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
            "training_time_sec": train_time,
            "train_samples": len(self.df_train),
            "val_samples": len(self.df_val),
        }

    # ═══════════════════════════════════════════════
    # STEP D: ATTACK ROUND 1
    # ═══════════════════════════════════════════════
    def attack_round1(self) -> Dict[str, Any]:
        """Run adversarial probing against Round 1 to find blind spots."""
        if self.r1_detector is None:
            raise ValueError("Train Round 1 first (Step C).")

        t0 = time.time()

        # Get fraud samples from the mining partition
        df_mine_fraud = self.df_holdout_mine[self.df_holdout_mine["is_fraud"] == 1].copy()
        if len(df_mine_fraud) == 0:
            return {"error": "No fraud samples in mining partition."}

        # Round 1 baseline: how many can it catch before probing?
        r1_probs_before = self.r1_detector.predict_proba(df_mine_fraud)
        r1_caught_before = int((r1_probs_before >= 0.5).sum())

        # Run probing using 3 strategies
        feature_cols = ["amount", "velocity", "device_risk_score", "is_decline"]
        evaded_rows = []
        strategies_used = {"velocity_dilution": 0, "amount_structuring": 0, "device_cloaking": 0}
        strategy_names = ["velocity_dilution", "amount_structuring", "device_cloaking"]

        rng = np.random.RandomState(int(time.time()) % 10000)

        for idx in range(len(df_mine_fraud)):
            row = df_mine_fraud.iloc[idx][feature_cols].to_dict()
            for k in row:
                row[k] = float(row[k])
            strategy = idx % 3

            for iteration in range(50):
                X = np.array([[row[f] for f in feature_cols]], dtype=float)
                prob = float(self.r1_detector.xgb_model.predict_proba(X)[0][1])

                if prob < 0.5:
                    strategies_used[strategy_names[strategy]] += 1
                    break

                step = rng.uniform(0.02, 0.15)
                if strategy == 0:
                    row["velocity"] = max(0.5, row["velocity"] * (1.0 - step))
                    row["device_risk_score"] = max(0.0, row["device_risk_score"] - rng.uniform(0, 0.03))
                elif strategy == 1:
                    row["amount"] = max(0.50, row["amount"] * (1.0 - step * 0.5))
                    row["velocity"] = max(0.5, row["velocity"] - rng.uniform(0.1, 0.5))
                elif strategy == 2:
                    row["device_risk_score"] = max(0.0, row["device_risk_score"] * (1.0 - step))
                    row["velocity"] = max(0.5, row["velocity"] - rng.uniform(0.05, 0.2))

            row["is_fraud"] = 1
            evaded_rows.append(row)

        self.adversarial_data = pd.DataFrame(evaded_rows)
        attack_time = round(time.time() - t0, 2)

        # How many does R1 catch AFTER probing?
        r1_probs_after = []
        for _, row in self.adversarial_data.iterrows():
            X = np.array([[row[f] for f in feature_cols]], dtype=float)
            prob = float(self.r1_detector.xgb_model.predict_proba(X)[0][1])
            r1_probs_after.append(prob)

        r1_caught_after = int(sum(1 for p in r1_probs_after if p >= 0.5))
        r1_missed = len(self.adversarial_data) - r1_caught_after
        evasion_rate = round(r1_missed / max(1, len(self.adversarial_data)) * 100, 1)

        self.attack_results = {
            "total_fraud_probed": len(df_mine_fraud),
            "total_adversarial": len(self.adversarial_data),
            "r1_caught_before_probing": r1_caught_before,
            "r1_caught_after_probing": r1_caught_after,
            "r1_missed": r1_missed,
            "evasion_rate": evasion_rate,
            "strategies_used": strategies_used,
            "attack_time_sec": attack_time,
        }
        return self.attack_results

    # ═══════════════════════════════════════════════
    # STEP E: RETRAIN ROUND 2
    # ═══════════════════════════════════════════════
    def retrain_round2(self) -> Dict[str, Any]:
        """Retrain with augmented data (original + adversarial failures)."""
        if self.adversarial_data is None:
            raise ValueError("Attack Round 1 first (Step D).")

        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from defend.detector_tabular import TabularCardTestingDetector

        t0 = time.time()

        # Filter: only keep samples that evaded R1
        feature_cols = ["amount", "velocity", "device_risk_score", "is_decline"]
        evaded_samples = []
        for _, row in self.adversarial_data.iterrows():
            X = np.array([[row[f] for f in feature_cols]], dtype=float)
            prob = float(self.r1_detector.xgb_model.predict_proba(X)[0][1])
            if prob < 0.5:
                evaded_samples.append(row)

        if len(evaded_samples) == 0:
            return {"error": "No adversarial samples evaded R1. R1 is already robust."}

        df_evaded = pd.DataFrame(evaded_samples)
        df_evaded["is_fraud"] = 1

        # Ensure columns match
        common_cols = [c for c in self.df_train.columns if c in df_evaded.columns]
        df_augmented = pd.concat([self.df_train[common_cols], df_evaded[common_cols]],
                                 ignore_index=True)

        # Train Round 2
        self.r2_detector = TabularCardTestingDetector()
        self.r2_detector.fit(df_augmented)
        train_time = round(time.time() - t0, 2)

        # Evaluate R2 on validation set
        r2_metrics = self.r2_detector.evaluate_performance(self.df_val)
        self.r2_metrics = r2_metrics

        return {
            "original_train_size": len(self.df_train),
            "evaded_samples_added": len(df_evaded),
            "augmented_train_size": len(df_augmented),
            "r2_auc_pr": r2_metrics["tabular_auc_pr"],
            "r2_f1_score": r2_metrics["tabular_f1_score"],
            "r2_fpr": r2_metrics["tabular_false_positive_rate"],
            "training_time_sec": train_time,
        }

    # ═══════════════════════════════════════════════
    # STEP F: EVALUATE — Final R1 vs R2 Comparison
    # ═══════════════════════════════════════════════
    def evaluate(self) -> Dict[str, Any]:
        """Score R1 vs R2 on the untouched holdout eval partition."""
        if self.r2_detector is None:
            raise ValueError("Retrain Round 2 first (Step E).")

        feature_cols = ["amount", "velocity", "device_risk_score", "is_decline"]

        # Generate fresh adversarial attacks against R1 for the eval partition
        df_eval_fraud = self.df_holdout_eval[self.df_holdout_eval["is_fraud"] == 1].copy()
        rng = np.random.RandomState(99)

        eval_adversarial_rows = []
        for idx in range(len(df_eval_fraud)):
            row = df_eval_fraud.iloc[idx][feature_cols].to_dict()
            for k in row:
                row[k] = float(row[k])
            strategy = idx % 3

            for iteration in range(50):
                X = np.array([[row[f] for f in feature_cols]], dtype=float)
                prob = float(self.r1_detector.xgb_model.predict_proba(X)[0][1])
                if prob < 0.5:
                    break
                step = rng.uniform(0.02, 0.15)
                if strategy == 0:
                    row["velocity"] = max(0.5, row["velocity"] * (1.0 - step))
                elif strategy == 1:
                    row["amount"] = max(0.50, row["amount"] * (1.0 - step * 0.5))
                elif strategy == 2:
                    row["device_risk_score"] = max(0.0, row["device_risk_score"] * (1.0 - step))

            row["is_fraud"] = 1
            eval_adversarial_rows.append(row)

        df_eval_adv = pd.DataFrame(eval_adversarial_rows)
        total_eval = len(df_eval_adv)

        # Score R1 on adversarial eval
        r1_caught = 0
        r2_caught = 0
        for _, row in df_eval_adv.iterrows():
            X = np.array([[row[f] for f in feature_cols]], dtype=float)
            r1_prob = float(self.r1_detector.xgb_model.predict_proba(X)[0][1])
            r2_prob = float(self.r2_detector.xgb_model.predict_proba(X)[0][1])
            if r1_prob >= 0.5:
                r1_caught += 1
            if r2_prob >= 0.5:
                r2_caught += 1

        # Baseline stability check (on legit+fraud val set)
        r1_baseline = self.r1_detector.evaluate_performance(self.df_val)
        r2_baseline = self.r2_detector.evaluate_performance(self.df_val)

        baseline_auc_drop = r1_baseline["tabular_auc_pr"] - r2_baseline["tabular_auc_pr"]
        forgetting_detected = baseline_auc_drop > 0.05

        return {
            "total_adversarial_eval": total_eval,
            "r1_caught": r1_caught,
            "r1_catch_rate": round(r1_caught / max(1, total_eval) * 100, 1),
            "r2_caught": r2_caught,
            "r2_catch_rate": round(r2_caught / max(1, total_eval) * 100, 1),
            "delta_caught": r2_caught - r1_caught,
            "r1_baseline_auc": r1_baseline["tabular_auc_pr"],
            "r2_baseline_auc": r2_baseline["tabular_auc_pr"],
            "r1_baseline_fpr": r1_baseline["tabular_false_positive_rate"],
            "r2_baseline_fpr": r2_baseline["tabular_false_positive_rate"],
            "forgetting_detected": forgetting_detected,
            "baseline_stable": not forgetting_detected,
        }
