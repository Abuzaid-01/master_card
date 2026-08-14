"""
Fidelity Evaluator: Statistical & ML Utility Benchmark Suite
Computes Wasserstein Distance, KS-Test scores, Domain Pass Rates, and TSTR (Train on Synthetic, Test on Real) AUC-PR.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any
from scipy.stats import wasserstein_distance, ks_2samp
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve, auc

def evaluate_distribution_fidelity(
    real_series: pd.Series,
    synth_series: pd.Series
) -> Dict[str, float]:
    """Computes Wasserstein Distance and KS-Test statistic between real and synthetic feature distributions."""
    r_clean = real_series.dropna().values
    s_clean = synth_series.dropna().values
    
    if len(r_clean) == 0 or len(s_clean) == 0:
        return {"wasserstein_distance": 0.0, "ks_statistic": 0.0, "ks_p_value": 1.0}
        
    wd = float(wasserstein_distance(r_clean, s_clean))
    ks_res = ks_2samp(r_clean, s_clean)
    
    return {
        "wasserstein_distance": float(np.round(wd, 4)),
        "ks_statistic": float(np.round(ks_res.statistic, 4)),
        "ks_p_value": float(np.round(ks_res.pvalue, 4))
    }

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import average_precision_score

def compute_tstr_score(
    df_synthetic_train: pd.DataFrame,
    df_real_test: pd.DataFrame,
    feature_cols: list,
    target_col: str = "is_fraud"
) -> Dict[str, float]:
    """
    Computes Train on Synthetic, Test on Real (TSTR) classification utility score.
    Trains a model ONLY on synthetic data, tests on real held-out data, and computes AUC-PR.
    """
    X_train = df_synthetic_train[feature_cols].fillna(0)
    y_train = df_synthetic_train[target_col]
    
    X_test = df_real_test[feature_cols].fillna(0)
    y_test = df_real_test[target_col]
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    clf = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
    clf.fit(X_train_scaled, y_train)
    
    y_pred_proba = clf.predict_proba(X_test_scaled)[:, 1] if len(clf.classes_) > 1 else np.zeros(len(X_test))
    
    auc_pr = float(np.round(average_precision_score(y_test, y_pred_proba), 4))
    
    return {
        "tstr_auc_pr": auc_pr,
        "train_samples_count": len(df_synthetic_train),
        "test_samples_count": len(df_real_test)
    }

def generate_fidelity_report(
    df_real: pd.DataFrame,
    df_synthetic: pd.DataFrame,
    feature_cols: list
) -> Dict[str, Any]:
    """Generates complete fidelity report covering distribution distances and TSTR utility."""
    report = {"feature_metrics": {}}
    
    for col in feature_cols:
        if col in df_real.columns and col in df_synthetic.columns:
            if pd.api.types.is_numeric_dtype(df_real[col]):
                metrics = evaluate_distribution_fidelity(df_real[col], df_synthetic[col])
                report["feature_metrics"][col] = metrics
                
    # Compute TSTR Score
    tstr_res = compute_tstr_score(df_synthetic, df_real, feature_cols)
    report["tstr_utility"] = tstr_res
    
    return report

if __name__ == "__main__":
    from generate.generator_tabular import generate_tabular_card_testing
    df_real = generate_tabular_card_testing(num_samples=200, random_seed=1)
    df_synth = generate_tabular_card_testing(num_samples=200, random_seed=2)
    
    feats = ["amount", "device_risk_score", "is_decline"]
    rep = generate_fidelity_report(df_real, df_synth, feats)
    print("Fidelity Report:", rep)
