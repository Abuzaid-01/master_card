"""
Vector 2 Detector: Multi-Hop Money Mule Network Graph Classifier
Trains GBDT with class_weight='balanced' on NetworkX graph features to detect fast pass-through money mule sweeps.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score, f1_score

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

class MuleNetworkGraphDetector:
    """
    Multi-Hop Money Mule Network Detector.
    Evaluates topological graph features (in/out degree balance, pass-through delay <30s, funnel score).
    """
    def __init__(self, feature_cols: list = None):
        self.feature_cols = feature_cols or [
            "amount",
            "pass_through_delay_sec",
            "sender_in_degree",
            "sender_out_degree",
            "receiver_in_degree",
            "receiver_out_degree",
            "receiver_mule_funnel_score"
        ]
        self.model = None

    def fit(self, df_train: pd.DataFrame, target_col: str = "is_fraud"):
        X_train = df_train[self.feature_cols].fillna(0)
        y_train = df_train[target_col].values
        
        print("[Graph Detector] Training HistGradientBoostingClassifier (class_weight='balanced')...")
        self.model = HistGradientBoostingClassifier(
            class_weight="balanced",
            max_iter=100,
            learning_rate=0.08,
            random_state=42
        )
        self.model.fit(X_train, y_train)

    def predict_proba(self, df_test: pd.DataFrame) -> np.ndarray:
        X_test = df_test[self.feature_cols].fillna(0)
        return self.model.predict_proba(X_test)[:, 1]

    def evaluate_performance(self, df_test: pd.DataFrame, target_col: str = "is_fraud") -> Dict[str, float]:
        y_test = df_test[target_col].values
        y_prob = self.predict_proba(df_test)
        
        auc_pr = float(np.round(average_precision_score(y_test, y_prob), 4))
        y_pred = (y_prob >= 0.50).astype(int)
        f1 = float(np.round(f1_score(y_test, y_pred, zero_division=0), 4))
        
        return {
            "graph_detector_auc_pr": auc_pr,
            "graph_detector_f1_score": f1,
            "test_samples_count": len(df_test)
        }

    def save_model(self, path: str = None) -> str:
        os.makedirs(MODELS_DIR, exist_ok=True)
        out_path = path or os.path.join(MODELS_DIR, "graph_detector.joblib")
        joblib.dump(self.model, out_path)
        return out_path

if __name__ == "__main__":
    df_sample = pd.DataFrame({
        "amount": [100.0, 5000.0, 50.0, 4900.0],
        "pass_through_delay_sec": [86400.0, 5.0, 43200.0, 12.0],
        "sender_in_degree": [1, 5, 2, 8],
        "sender_out_degree": [1, 5, 1, 8],
        "receiver_in_degree": [2, 6, 1, 9],
        "receiver_out_degree": [1, 6, 2, 9],
        "receiver_mule_funnel_score": [1, 6, 1, 9],
        "is_fraud": [0, 1, 0, 1]
    })
    det = MuleNetworkGraphDetector()
    det.fit(df_sample)
    perf = det.evaluate_performance(df_sample)
    print("Graph Detector Performance:", perf)
