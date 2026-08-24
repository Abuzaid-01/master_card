"""
Vector 8 Generator: Adversarial Transaction Pattern Evasion Engine
Applies adversarial decision-boundary perturbations to fraud transaction records across multi-dimensional feature space:
- Amount Structuring (e.g. $1.99 micro-pricing, $99.50 threshold skirting)
- Velocity Dilution (slowing down bot request intervals)
- Device Score & Geo-Spoofing (manipulating client telemetry & proxy headers)
- Failed Attempt Masking
- Model Poisoning Injection (backdoor-triggered training data corruption)
- Adaptive RL Bot Probing (iterative decision boundary exploration at 0.49-0.51 range)
- Black-Box Surrogate Probing (surrogate model approximation for boundary clustering)
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
    Includes 7 evasion strategies: amount structuring, velocity dilution, device/geo spoofing,
    failed attempt masking, model poisoning, adaptive RL probing, and surrogate boundary probing.
    """
    np.random.seed(random_seed)
    df_perturbed = df.copy()
    
    fraud_indices = df_perturbed[df_perturbed["is_fraud"] == 1].index
    if len(fraud_indices) == 0:
        return df_perturbed
        
    num_to_perturb = int(len(fraud_indices) * evasion_ratio)
    selected_indices = np.random.choice(fraud_indices, size=num_to_perturb, replace=False)
    
    # Split perturbation budget across 7 strategies
    strategy_splits = np.array_split(selected_indices, 7)
    
    # ── Strategy 1: Amount Structuring ──
    for idx in strategy_splits[0]:
        orig_amount = df_perturbed.loc[idx, "amount"]
        if orig_amount > 100.0:
            df_perturbed.loc[idx, "amount"] = float(np.floor(orig_amount * 0.92))
        elif orig_amount <= 3.00:
            df_perturbed.loc[idx, "amount"] = 1.99
        df_perturbed.loc[idx, "attack_vector"] = "adversarial_amount_structuring"
    
    # ── Strategy 2: Timestamp Micro-Jittering ──
    for idx in strategy_splits[1]:
        if "timestamp_sec" in df_perturbed.columns:
            df_perturbed.loc[idx, "timestamp_sec"] += float(np.random.uniform(0.1, 2.5))
        df_perturbed.loc[idx, "attack_vector"] = "adversarial_timestamp_jitter"
            
    # ── Strategy 3: Device Risk Score Spoofing ──
    for idx in strategy_splits[2]:
        if "device_risk_score" in df_perturbed.columns:
            orig_risk = df_perturbed.loc[idx, "device_risk_score"]
            df_perturbed.loc[idx, "device_risk_score"] = float(np.round(max(0.12, orig_risk * 0.45), 4))
        df_perturbed.loc[idx, "attack_vector"] = "adversarial_device_spoofing"
            
    # ── Strategy 4: Velocity Dilution + Geo-Spoofing + Failed Attempt Masking ──
    for idx in strategy_splits[3]:
        if "velocity" in df_perturbed.columns:
            orig_vel = df_perturbed.loc[idx, "velocity"]
            df_perturbed.loc[idx, "velocity"] = float(np.round(max(1.5, orig_vel * 0.35), 2))
        if "geo_distance_km" in df_perturbed.columns:
            df_perturbed.loc[idx, "geo_distance_km"] = float(np.round(np.random.uniform(2.0, 28.0), 2))
        if "failed_attempts_24h" in df_perturbed.columns:
            df_perturbed.loc[idx, "failed_attempts_24h"] = 0
        df_perturbed.loc[idx, "attack_vector"] = "adversarial_velocity_dilution"

    # ── Strategy 5: Model Poisoning Injection ──
    # Injects backdoor-triggered records: flip labels on specific trigger pattern
    # (amount ending in .77 + clean device) — simulates training data corruption
    for idx in strategy_splits[4]:
        df_perturbed.loc[idx, "amount"] = float(np.round(np.random.uniform(50, 500), 0)) + 0.77
        if "device_risk_score" in df_perturbed.columns:
            df_perturbed.loc[idx, "device_risk_score"] = float(np.round(np.random.uniform(0.02, 0.10), 4))
        if "velocity" in df_perturbed.columns:
            df_perturbed.loc[idx, "velocity"] = float(np.round(np.random.uniform(0.5, 2.0), 2))
        if "failed_attempts_24h" in df_perturbed.columns:
            df_perturbed.loc[idx, "failed_attempts_24h"] = 0
        df_perturbed.loc[idx, "attack_vector"] = "adversarial_model_poisoning"

    # ── Strategy 6: Adaptive RL Bot Probing ──
    # Iteratively shifts features toward the model's decision boundary (score ~0.49-0.51)
    for idx in strategy_splits[5]:
        df_perturbed.loc[idx, "amount"] = float(np.round(np.random.uniform(80, 350), 2))
        if "velocity" in df_perturbed.columns:
            df_perturbed.loc[idx, "velocity"] = float(np.round(np.random.uniform(2.0, 5.0), 2))
        if "device_risk_score" in df_perturbed.columns:
            df_perturbed.loc[idx, "device_risk_score"] = float(np.round(np.random.uniform(0.20, 0.40), 4))
        if "geo_distance_km" in df_perturbed.columns:
            df_perturbed.loc[idx, "geo_distance_km"] = float(np.round(np.random.uniform(15.0, 80.0), 2))
        if "failed_attempts_24h" in df_perturbed.columns:
            df_perturbed.loc[idx, "failed_attempts_24h"] = int(np.random.choice([0, 1], p=[0.7, 0.3]))
        df_perturbed.loc[idx, "attack_vector"] = "adversarial_rl_adaptive_bot"

    # ── Strategy 7: Black-Box Surrogate Decision Boundary Probing ──
    # Clusters fraud features at the exact decision boundary of a surrogate model
    for idx in strategy_splits[6]:
        df_perturbed.loc[idx, "amount"] = float(np.round(np.random.uniform(120, 280), 2))
        if "velocity" in df_perturbed.columns:
            df_perturbed.loc[idx, "velocity"] = float(np.round(np.random.uniform(2.5, 4.5), 2))
        if "device_risk_score" in df_perturbed.columns:
            df_perturbed.loc[idx, "device_risk_score"] = float(np.round(np.random.uniform(0.25, 0.35), 4))
        if "geo_distance_km" in df_perturbed.columns:
            df_perturbed.loc[idx, "geo_distance_km"] = float(np.round(np.random.uniform(25.0, 60.0), 2))
        if "failed_attempts_24h" in df_perturbed.columns:
            df_perturbed.loc[idx, "failed_attempts_24h"] = 0
        if "provisioning_channel" in df_perturbed.columns:
            df_perturbed.loc[idx, "provisioning_channel"] = int(np.random.choice([0, 1]))
        if "nfc_tap_latency_ms" in df_perturbed.columns:
            df_perturbed.loc[idx, "nfc_tap_latency_ms"] = 0.0
        if "raas_dispute_score" in df_perturbed.columns:
            df_perturbed.loc[idx, "raas_dispute_score"] = float(np.round(np.random.uniform(0.05, 0.15), 4))
        df_perturbed.loc[idx, "attack_vector"] = "adversarial_surrogate_probing"
        
    return df_perturbed


if __name__ == "__main__":
    from generate.generator_tabular import generate_tabular_card_testing
    df_sample = generate_tabular_card_testing(num_samples=100)
    df_evaded = apply_adversarial_evasion_perturbations(df_sample, evasion_ratio=0.5)
    print("Perturbed samples count:", len(df_evaded[df_evaded["attack_vector"].str.startswith("adversarial")]))
    print("Strategy breakdown:")
    print(df_evaded[df_evaded["attack_vector"].str.startswith("adversarial")]["attack_vector"].value_counts())
