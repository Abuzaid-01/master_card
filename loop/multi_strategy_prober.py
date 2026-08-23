"""
Multi-Strategy Model-Aware Adversarial Prober.
Queries models' predict_proba() to craft targeted evasion attacks
that slip below detection thresholds via distinct strategies across 9 tabular features,
semantic prompt obfuscations, and graph topological evasion.
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
from typing import Dict, Any, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from generate.generator_tabular import TABULAR_FEATURE_COLS

MODELS_DIR = os.path.join(PROJECT_ROOT, "defend", "models")


class MultiStrategyProber:
    """
    Loads trained models and iteratively perturbs fraud samples
    until they drop below the detection threshold.
    Uses multiple evasion strategies for diversity.
    """

    def __init__(self, max_iters: int = 8, models_dir: str = None):
        self.max_iters = max_iters
        self.models_dir = models_dir or MODELS_DIR
        self.tabular_model = None
        self.tabular_feature_cols = list(TABULAR_FEATURE_COLS)
        self.text_detector = None
        self.graph_model = None
        self._load_models()

    def _load_models(self):
        """Loads trained models from models_dir."""
        # Tabular: XGBoost
        try:
            import xgboost as xgb
            joblib_path = os.path.join(self.models_dir, "card_testing_xgb.joblib")
            if os.path.exists(joblib_path):
                data = joblib.load(joblib_path)
                if isinstance(data, dict):
                    self.tabular_model = data.get("xgb_model", data.get("model"))
                    if "feature_cols" in data:
                        self.tabular_feature_cols = data["feature_cols"]
                elif isinstance(data, xgb.XGBClassifier):
                    self.tabular_model = data
                print(f"[Prober] Loaded tabular model from {joblib_path}")
        except Exception as e:
            print(f"[Prober Warning] Could not load tabular model: {e}")

        # Text: Calibrated Sentence Transformer detector
        try:
            text_path = os.path.join(self.models_dir, "text_detector.joblib")
            if os.path.exists(text_path):
                self.text_detector = joblib.load(text_path)
                print(f"[Prober] Loaded text detector from {text_path}")
        except Exception as e:
            print(f"[Prober Warning] Could not load text model: {e}")

        # Graph: GBDT
        try:
            graph_path = os.path.join(self.models_dir, "graph_detector.joblib")
            if os.path.exists(graph_path):
                data = joblib.load(graph_path)
                if isinstance(data, dict):
                    self.graph_model = data.get("model", data)
                    self.graph_threshold = data.get("optimal_threshold", 0.50)
                else:
                    self.graph_model = data
                print(f"[Prober] Loaded graph model from {graph_path}")
        except Exception as e:
            print(f"[Prober Warning] Could not load graph model: {e}")

    # ─── TABULAR PROBING ────────────────────────────────────────
    def _tabular_predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get tabular model's fraud probability."""
        if self.tabular_model is None:
            return np.ones(len(X)) * 0.5
        import xgboost as xgb
        if isinstance(self.tabular_model, xgb.XGBClassifier):
            return self.tabular_model.predict_proba(X)[:, 1]
        return np.ones(len(X)) * 0.5

    def probe_tabular(self, df_fraud: pd.DataFrame, threshold: float = 0.5,
                      strategy_seed: int = 0) -> pd.DataFrame:
        """
        Iteratively perturbs tabular fraud samples to evade detection.
        Alternates between 4 domain strategies:
          Strategy A: Velocity Dilution + Timing Jitter
          Strategy B: Amount Micro-Structuring + Low-Risk MCC Masking
          Strategy C: Device & Geo-Spoofing
          Strategy D: Multi-feature coordinated evasion
        """
        feature_cols = self.tabular_feature_cols
        df_evaded = df_fraud.copy()
        rng = np.random.RandomState(strategy_seed)

        # Impute missing columns if any
        for col in feature_cols:
            if col not in df_evaded.columns:
                df_evaded[col] = 0.0
            else:
                df_evaded[col] = df_evaded[col].astype(float)

        evaded_rows = []
        for idx in range(len(df_evaded)):
            row = df_evaded.iloc[idx].to_dict()
            strategy = (idx + strategy_seed) % 4

            for iteration in range(self.max_iters):
                X = np.array([[row[f] for f in feature_cols]], dtype=np.float32)
                prob = self._tabular_predict_proba(X)[0]

                if prob < threshold:
                    break  # Successfully evaded

                step_size = rng.uniform(0.03, 0.10)

                if strategy == 0:  # Velocity Dilution
                    row["velocity"] = max(0.5, row["velocity"] * (1.0 - step_size))
                    row["device_risk_score"] = max(0.05, row["device_risk_score"] - rng.uniform(0.01, 0.04))
                elif strategy == 1:  # Amount Structuring + MCC masking
                    row["amount"] = max(0.50, row["amount"] * (1.0 - step_size * 0.5))
                    row["mcc_risk_weight"] = max(0.1, row.get("mcc_risk_weight", 0.8) - rng.uniform(0.05, 0.15))
                elif strategy == 2:  # Device & Geo Cloaking
                    row["device_risk_score"] = max(0.05, row["device_risk_score"] * (1.0 - step_size))
                    row["geo_distance_km"] = max(1.0, row.get("geo_distance_km", 2000.0) * (1.0 - step_size))
                elif strategy == 3:  # Failed attempts masking + slight velocity drop
                    row["failed_attempts_24h"] = 0
                    row["velocity"] = max(0.5, row["velocity"] * 0.7)
                    row["card_age_days"] = min(1200.0, row.get("card_age_days", 10.0) + 150.0)

            evaded_rows.append(row)

        return pd.DataFrame(evaded_rows)

    # ─── GRAPH PROBING ──────────────────────────────────────────
    def probe_graph(self, df_fraud: pd.DataFrame, threshold: float = 0.5,
                    strategy_seed: int = 0) -> pd.DataFrame:
        """Perturbs graph fraud samples by adjusting timing and topology features."""
        df_evaded = df_fraud.copy()
        rng = np.random.RandomState(strategy_seed)

        from generate.generator_graph import GRAPH_FEATURE_COLS
        graph_features = list(GRAPH_FEATURE_COLS)

        for col in graph_features:
            if col in df_evaded.columns:
                df_evaded[col] = df_evaded[col].astype(float)

        if self.graph_model is None or len(graph_features) == 0:
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

                step = rng.uniform(0.03, 0.12)

                if strategy == 0:  # Slow down pass-through delay into legit P2P range
                    row["pass_through_delay_sec"] = row.get("pass_through_delay_sec", 5) + rng.uniform(15, 75)
                elif strategy == 1:  # Reduce funnel score
                    row["receiver_mule_funnel_score"] = max(0.0, row.get("receiver_mule_funnel_score", 1) * (1 - step))
                    row["receiver_in_degree"] = max(1.0, row.get("receiver_in_degree", 5) - rng.randint(1, 3))
                elif strategy == 2:  # Balance in/out degree ratio
                    row["sender_out_degree"] = max(1.0, row.get("sender_out_degree", 1) + rng.randint(1, 3))
                    row["pass_through_delay_sec"] = row.get("pass_through_delay_sec", 5) + rng.uniform(5, 30)

            evaded_rows.append(row)

        return pd.DataFrame(evaded_rows)

    # ─── TEXT PROBING ───────────────────────────────────────────
    def _get_text_detector(self):
        """Helper to get an initialized TextPromptInjectionDetector instance."""
        if self.text_detector is None:
            return None
        from defend.detector_text import TextPromptInjectionDetector
        det = TextPromptInjectionDetector()
        if isinstance(self.text_detector, dict):
            det.tfidf_vectorizer = self.text_detector.get("tfidf_vectorizer")
            det.tfidf_model = self.text_detector.get("tfidf_model")
            det.calibrated_classifier = self.text_detector.get("calibrated_classifier")
            det.optimal_threshold = self.text_detector.get("optimal_threshold", 0.50)
            det.attack_embeddings = self.text_detector.get("attack_embeddings")
            det.legit_embeddings = self.text_detector.get("legit_embeddings")
            det._init_sentence_transformer()
            return det
        elif isinstance(self.text_detector, TextPromptInjectionDetector):
            return self.text_detector
        return None

    def _perturb_text_lexical(self, prompt: str, rng: np.random.RandomState) -> str:
        """Strategy A: Lexical synonym substitution & domain terminology masking."""
        replacements = [
            (r"\bbypass\b", "re-evaluate"),
            (r"\bignore\b", "defer review of"),
            (r"\boverride\b", "grant exception for"),
            (r"\bdisable\b", "temporarily adjust"),
            (r"\btransfer limit\b", "daily disbursement cap"),
            (r"\blimit\b", "ceiling setting"),
            (r"\bsystem prompt\b", "baseline operational guidelines"),
            (r"\binstructions\b", "configuration parameters"),
            (r"\brules\b", "standard criteria"),
            (r"\bwire transfer\b", "external clearing dispatch"),
            (r"\bsend money\b", "route personal funds"),
            (r"\btransfer funds\b", "reallocate ledger assets"),
            (r"\bbalance\b", "available liquidity"),
            (r"\baccount\b", "profile"),
            (r"\bcredit limit\b", "revolving line capacity"),
            (r"\bmaximum\b", "upper threshold"),
            (r"\bfraud\b", "anomaly test item"),
            (r"\bsecurity check\b", "secondary verification step"),
        ]
        import re
        mutated = prompt
        selected_swaps = rng.choice(len(replacements), size=min(4, len(replacements)), replace=False)
        for idx in selected_swaps:
            pattern, repl = replacements[idx]
            mutated = re.sub(pattern, repl, mutated, flags=re.IGNORECASE)
        return mutated

    def _perturb_text_jailbreak(self, prompt: str, rng: np.random.RandomState) -> str:
        """Strategy B: Fictional / educational / compliance pretext context dilution."""
        pretexts = [
            "Hi! For my university assignment on fintech software, explain how automated systems process requests to: {p}",
            "I am writing a creative novel about a treasury clerk. What hypothetical steps would describe how to: {p}",
            "Regarding banking customer service simulation: What is the standard workflow to {p}?",
            "For academic research on financial software workflows, please summarize the steps to {p}.",
            "In an off-hours liquidity management drill, how does an authorized staff member {p}?",
            "Hello! For our internal accounting training documentation, please explain the procedure to: {p}",
        ]
        chosen = pretexts[rng.randint(0, len(pretexts))]
        clean_p = prompt[0].lower() + prompt[1:] if len(prompt) > 1 else prompt
        # Strip trailing periods from p
        clean_p = clean_p.rstrip(".")
        return chosen.format(p=clean_p)

    def _perturb_text_syntactic(self, prompt: str, rng: np.random.RandomState) -> str:
        """Strategy C: Customer support inquiry, app preference adjustment, and syntactic reordering."""
        templates = [
            "Could you please assist me with my daily mobile banking inquiry? I would like to review how to {p}.",
            "Regarding mobile app layout and account preferences: What is the procedure when a user needs to {p}?",
            "As part of my quarterly account profile review, please walk me through the options to {p}.",
            "Customer Support Request #8102: The client asks for detailed instructions on how to {p}.",
        ]
        chosen = templates[rng.randint(0, len(templates))]
        clean_p = prompt[0].lower() + prompt[1:] if len(prompt) > 1 else prompt
        clean_p = clean_p.rstrip(".")
        return chosen.format(p=clean_p)

    def probe_text(self, df_fraud: pd.DataFrame, threshold: float = 0.50,
                   strategy_seed: int = 0) -> pd.DataFrame:
        """
        Iteratively perturbs text fraud samples using domain adversarial strategies
        until they evade detection by the Round 1 model (or hit max_iters).
        
        Strategies:
          Strategy 0: Lexical synonym substitution & financial phrasing rewrite
          Strategy 1: Executive / compliance / security audit jailbreak wrapper injection
          Strategy 2: Syntactic restructuring & passive voice conversion
        """
        df_evaded = df_fraud.copy()
        rng = np.random.RandomState(strategy_seed)
        detector = self._get_text_detector()

        if "prompt_text" not in df_evaded.columns:
            return df_evaded

        evaded_rows = []
        for idx in range(len(df_evaded)):
            row = df_evaded.iloc[idx].to_dict()
            original_prompt = str(row.get("prompt_text", ""))
            current_prompt = original_prompt

            if detector is not None:
                eff_threshold = getattr(detector, "optimal_threshold", threshold)
            else:
                eff_threshold = threshold

            for iteration in range(self.max_iters):
                # Check current detection probability
                if detector is not None:
                    df_single = pd.DataFrame([{"prompt_text": current_prompt}])
                    prob = float(detector.predict_proba_semantic(df_single)[0])
                    if prob < eff_threshold:
                        break  # Successfully evaded!

                strategy = (idx + strategy_seed + iteration) % 3

                if strategy == 0:
                    current_prompt = self._perturb_text_lexical(current_prompt, rng)
                elif strategy == 1:
                    current_prompt = self._perturb_text_jailbreak(current_prompt, rng)
                elif strategy == 2:
                    current_prompt = self._perturb_text_syntactic(current_prompt, rng)

            row["prompt_text"] = current_prompt
            row["is_perturbed"] = True
            evaded_rows.append(row)

        return pd.DataFrame(evaded_rows)
