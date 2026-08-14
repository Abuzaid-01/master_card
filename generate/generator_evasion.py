"""
Vector 8 Generator: Adversarial Transaction Pattern Evasion Engine
Applies adversarial decision-boundary perturbations to fraud transaction records.
Simulates an attacker probing classifier thresholds with amount rounding ($9,990 vs $10,000) and feature jittering.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any

def apply_adversarial_evasion_perturbations(
    df: pd.DataFrame,
    evasion_ratio: float = 0.20,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Applies adversarial feature perturbations to fraudulent records in the input dataframe.
    
    Perturbations include:
    - Amount Structuring: Rounding transaction amounts to just under threshold limits (e.g. $9,990 instead of $10,000).
    - Timestamp Jitter: Micro-perturbations in execution timestamp to blur frequency detection.
    - Device Score Spoofing: Manipulating secondary telemetry attributes to lower composite risk score.
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
            df_perturbed.loc[idx, "amount"] = float(np.floor(orig_amount * 0.95))
        elif orig_amount <= 2.50:
            df_perturbed.loc[idx, "amount"] = 1.99  # Standard legitimate-looking price point
            
        # Timestamp micro-jittering
        if "timestamp_sec" in df_perturbed.columns:
            df_perturbed.loc[idx, "timestamp_sec"] += float(np.random.uniform(0.1, 2.5))
            
        # Device risk score perturbation (spoofing secondary telemetry)
        if "device_risk_score" in df_perturbed.columns:
            orig_risk = df_perturbed.loc[idx, "device_risk_score"]
            df_perturbed.loc[idx, "device_risk_score"] = float(np.round(max(0.1, orig_risk * 0.5), 4))
            
        # Mark attack vector as evasive perturbation
        df_perturbed.loc[idx, "attack_vector"] = "adversarial_pattern_evasion"
        
    return df_perturbed

if __name__ == "__main__":
    from generate.generator_tabular import generate_tabular_card_testing
    df_sample = generate_tabular_card_testing(num_samples=50)
    df_evaded = apply_adversarial_evasion_perturbations(df_sample, evasion_ratio=0.5)
    print("Perturbed samples count:", len(df_evaded[df_evaded["attack_vector"] == "adversarial_pattern_evasion"]))
    print(df_evaded[df_evaded["attack_vector"] == "adversarial_pattern_evasion"].head())
