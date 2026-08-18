"""
Vector 8 Generator: Adversarial Transaction Pattern Evasion Engine
Applies adversarial decision-boundary perturbations to fraud transaction records across multi-dimensional feature space:
- Amount Structuring (e.g. $1.99 micro-pricing, $99.50 threshold skirting)
- Velocity Dilution (slowing down bot request intervals)
- Device Score & Geo-Spoofing (manipulating client telemetry & proxy headers)
- Failed Attempt Masking
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


def apply_adversarial_evasion_perturbations(
    df: pd.DataFrame,
    evasion_ratio: float = 0.25,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Applies adversarial feature perturbations to fraudulent records in the input dataframe.
    """
    np.random.seed(random_seed)
    df_perturbed = df.copy()
    
    fraud_indices = df_perturbed[df_perturbed["is_fraud"] == 1].index
    if len(fraud_indices) == 0:
        return df_perturbed
        
    num_to_perturb = int(len(fraud_indices) * evasion_ratio)
    selected_indices = np.random.choice(fraud_indices, size=num_to_perturb, replace=False)
    
    for idx in selected_indices:
        # Amount structuring perturbation
        orig_amount = df_perturbed.loc[idx, "amount"]
        if orig_amount > 100.0:
            df_perturbed.loc[idx, "amount"] = float(np.floor(orig_amount * 0.92))
        elif orig_amount <= 3.00:
            df_perturbed.loc[idx, "amount"] = 1.99  # Standard legitimate-looking price point
            
        # Timestamp micro-jittering
        if "timestamp_sec" in df_perturbed.columns:
            df_perturbed.loc[idx, "timestamp_sec"] += float(np.random.uniform(0.1, 2.5))
            
        # Device risk score perturbation (spoofing secondary telemetry)
        if "device_risk_score" in df_perturbed.columns:
            orig_risk = df_perturbed.loc[idx, "device_risk_score"]
            df_perturbed.loc[idx, "device_risk_score"] = float(np.round(max(0.12, orig_risk * 0.45), 4))
            
        # Velocity dilution (stretching burst rate)
        if "velocity" in df_perturbed.columns:
            orig_vel = df_perturbed.loc[idx, "velocity"]
            df_perturbed.loc[idx, "velocity"] = float(np.round(max(1.5, orig_vel * 0.35), 2))
            
        # Geo-spoofing (spoofed residential proxy)
        if "geo_distance_km" in df_perturbed.columns:
            df_perturbed.loc[idx, "geo_distance_km"] = float(np.round(np.random.uniform(2.0, 28.0), 2))
            
        # Failed attempt masking
        if "failed_attempts_24h" in df_perturbed.columns:
            df_perturbed.loc[idx, "failed_attempts_24h"] = 0
            
        # Mark attack vector as evasive perturbation
        df_perturbed.loc[idx, "attack_vector"] = "adversarial_pattern_evasion"
        
    return df_perturbed


if __name__ == "__main__":
    from generate.generator_tabular import generate_tabular_card_testing
    df_sample = generate_tabular_card_testing(num_samples=100)
    df_evaded = apply_adversarial_evasion_perturbations(df_sample, evasion_ratio=0.5)
    print("Perturbed samples count:", len(df_evaded[df_evaded["attack_vector"] == "adversarial_pattern_evasion"]))
    print(df_evaded[df_evaded["attack_vector"] == "adversarial_pattern_evasion"].head())
