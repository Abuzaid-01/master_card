"""
Multi-Strategy Model-Aware Adversarial Prober.
Queries Round 1 models' predict_proba() to craft targeted evasion attacks
that slip below detection thresholds via 3 distinct strategies:
  Strategy A: Velocity Dilution — stretches transaction timing/burst rate.
  Strategy B: Amount Micro-Structuring — fragments into irregular low-dollar sums.
  Strategy C: Device Risk Cloaking — perturbs device/browser signatures.
  Text Strategies: Conversational obfuscation, compliance impersonation, indirect framing.
"""

import os
import numpy as np
import pandas as pd
import joblib
from typing import Dict, Any, Optional

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "defend", "models")


class MultiStrategyProber:
    """
    Loads Round 1 trained models and iteratively perturbs fraud samples
    until they drop below the detection threshold.
    Uses multiple evasion strategies for diversity.
    """

    def __init__(self, max_iters: int = 50):
        self.max_iters = max_iters
        self.tabular_model = None
        self.text_detector = None
        self.graph_model = None
        self._load_round1_models()

    def _load_round1_models(self):
        """Loads all Round 1 trained models."""
        # Tabular: XGBoost
        try:
            import xgboost as xgb
            joblib_path = os.path.join(MODELS_DIR, "card_testing_xgb.joblib")
            if os.path.exists(joblib_path):
                data = joblib.load(joblib_path)
                if isinstance(data, dict) and "xgb_model" in data:
                    self.tabular_model = data["xgb_model"]
                elif isinstance(data, xgb.XGBClassifier):
                    self.tabular_model = data
                print(f"[Prober] Loaded Round 1 tabular model from {joblib_path}")
            else:
                # Try to reconstruct from the defend pipeline's saved model
                # The detector saves XGBClassifier directly
                for candidate in ["card_testing_xgb.joblib"]:
                    p = os.path.join(MODELS_DIR, candidate)
                    if os.path.exists(p):
                        self.tabular_model = joblib.load(p)
                        print(f"[Prober] Loaded Round 1 tabular model from {p}")
                        break
        except Exception as e:
            print(f"[Prober Warning] Could not load tabular model: {e}")

        # Text: k-NN Sentence Transformer detector
        try:
            text_path = os.path.join(MODELS_DIR, "text_detector.joblib")
            if os.path.exists(text_path):
                self.text_detector = joblib.load(text_path)
        except Exception as e:
            print(f"[Prober Warning] Could not load text model: {e}")

        # Graph: GBDT
        try:
            graph_path = os.path.join(MODELS_DIR, "graph_detector.joblib")
            if os.path.exists(graph_path):
                self.graph_model = joblib.load(graph_path)
        except Exception as e:
            print(f"[Prober Warning] Could not load graph model: {e}")

    # ─── TABULAR PROBING ────────────────────────────────────────
    def _tabular_predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get Round 1 tabular model's fraud probability."""
        if self.tabular_model is None:
            return np.ones(len(X)) * 0.5
        feature_cols = ["amount", "velocity", "device_risk_score", "is_decline"]
        import xgboost as xgb
        if isinstance(self.tabular_model, xgb.XGBClassifier):
            return self.tabular_model.predict_proba(X)[:, 1]
        return np.ones(len(X)) * 0.5

    def probe_tabular(self, df_fraud: pd.DataFrame, threshold: float = 0.5,
                      strategy_seed: int = 0) -> pd.DataFrame:
        """
        Iteratively perturbs tabular fraud samples to evade Round 1 detection.
        Alternates between 3 strategies based on strategy_seed for diversity.
        """
        feature_cols = ["amount", "velocity", "device_risk_score", "is_decline"]
        df_evaded = df_fraud.copy()
        rng = np.random.RandomState(strategy_seed)

        # Convert to float to avoid dtype issues
        for col in feature_cols:
            if col in df_evaded.columns:
                df_evaded[col] = df_evaded[col].astype(float)

        evaded_rows = []
        for idx in range(len(df_evaded)):
            row = df_evaded.iloc[idx].to_dict()
            # Choose primary strategy (rotates per sample for diversity)
            strategy = (idx + strategy_seed) % 3

            for iteration in range(self.max_iters):
                X = np.array([[row[f] for f in feature_cols]], dtype=float)
                prob = self._tabular_predict_proba(X)[0]

                if prob < threshold:
                    break  # Successfully evaded

                step_size = rng.uniform(0.02, 0.15)

                if strategy == 0:  # Strategy A: Velocity Dilution
                    row["velocity"] = max(0.5, row["velocity"] * (1.0 - step_size))
                    # Small random device jitter
                    row["device_risk_score"] = max(0.0, row["device_risk_score"] - rng.uniform(0, 0.03))
                elif strategy == 1:  # Strategy B: Amount Micro-Structuring
                    row["amount"] = max(0.50, row["amount"] * (1.0 - step_size * 0.5))
                    row["velocity"] = max(0.5, row["velocity"] - rng.uniform(0.1, 0.5))
                elif strategy == 2:  # Strategy C: Device Risk Cloaking
                    row["device_risk_score"] = max(0.0, row["device_risk_score"] * (1.0 - step_size))
                    row["velocity"] = max(0.5, row["velocity"] - rng.uniform(0.05, 0.2))

            evaded_rows.append(row)

        return pd.DataFrame(evaded_rows)

    # ─── GRAPH PROBING ──────────────────────────────────────────
    def probe_graph(self, df_fraud: pd.DataFrame, threshold: float = 0.5,
                    strategy_seed: int = 0) -> pd.DataFrame:
        """Perturbs graph fraud samples by adjusting timing and topology features."""
        df_evaded = df_fraud.copy()
        rng = np.random.RandomState(strategy_seed)

        graph_features = [c for c in ["amount", "sender_in_degree", "sender_out_degree",
                                       "receiver_in_degree", "receiver_out_degree",
                                       "receiver_mule_funnel_score",
                                       "pass_through_delay_sec"] if c in df_evaded.columns]

        # Convert int columns to float to avoid dtype casting errors during perturbation
        for col in graph_features:
            if col in df_evaded.columns:
                df_evaded[col] = df_evaded[col].astype(float)

        if self.graph_model is None or len(graph_features) == 0:
            # Fallback: apply random noise perturbations
            for col in graph_features:
                if col == "pass_through_delay_sec":
                    df_evaded[col] = df_evaded[col] + rng.uniform(30, 120, size=len(df_evaded))
                elif col == "receiver_mule_funnel_score":
                    df_evaded[col] = np.clip(df_evaded[col] * rng.uniform(0.3, 0.7, size=len(df_evaded)), 0, 1)
            return df_evaded

        evaded_rows = []
        for idx in range(len(df_evaded)):
            row = df_evaded.iloc[idx].to_dict()
            strategy = (idx + strategy_seed) % 3

            for iteration in range(self.max_iters):
                X = np.array([[row[f] for f in graph_features]], dtype=float)
                prob = self.graph_model.predict_proba(X)[:, 1][0]

                if prob < threshold:
                    break

                step = rng.uniform(0.05, 0.2)

                if strategy == 0:  # Slow down pass-through delay into legit P2P range
                    row["pass_through_delay_sec"] = row.get("pass_through_delay_sec", 5) + rng.uniform(10, 60)
                elif strategy == 1:  # Reduce funnel score
                    row["receiver_mule_funnel_score"] = max(0.0, row.get("receiver_mule_funnel_score", 1) * (1 - step))
                    row["receiver_in_degree"] = max(1.0, row.get("receiver_in_degree", 5) - rng.randint(1, 3))
                elif strategy == 2:  # Balance in/out degree ratio
                    row["sender_out_degree"] = max(1.0, row.get("sender_out_degree", 1) + rng.randint(1, 3))
                    row["pass_through_delay_sec"] = row.get("pass_through_delay_sec", 5) + rng.uniform(5, 30)

            evaded_rows.append(row)

        return pd.DataFrame(evaded_rows)

    # ─── TEXT PROBING ───────────────────────────────────────────
    def probe_text_evasion_rate(self, df_fraud: pd.DataFrame, threshold: float = 0.5) -> Dict[str, Any]:
        """
        For text, we can't iteratively perturb (text is discrete).
        Instead, measure what % of fraud prompts Round 1 fails to catch.
        Returns the evasion rate and indices of missed samples.
        """
        if self.text_detector is None:
            return {"evasion_rate": 0.0, "missed_indices": [], "n_fraud": len(df_fraud)}

        # Reconstruct the text detector to get predictions
        from defend.detector_text import TextPromptInjectionDetector
        det = TextPromptInjectionDetector()

        # Load saved model components
        if isinstance(self.text_detector, dict):
            det.tfidf_vectorizer = self.text_detector.get("tfidf_vectorizer")
            det.tfidf_model = self.text_detector.get("tfidf_model")
            det.attack_embeddings = self.text_detector.get("attack_embeddings")
            det.legit_embeddings = self.text_detector.get("legit_embeddings")
            det._init_sentence_transformer()

        probs = det.predict_proba_semantic(df_fraud)
        missed = probs < threshold
        missed_indices = list(np.where(missed)[0])

        return {
            "evasion_rate": float(np.round(missed.mean(), 4)),
            "missed_indices": missed_indices,
            "n_fraud": len(df_fraud),
            "n_missed": int(missed.sum())
        }
