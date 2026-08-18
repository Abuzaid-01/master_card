"""
Vector 5 Generator: AI-Automated Evasive Card Testing & Fraud Transactions
Generates synthetic tabular card authorization records with 9 enterprise-grade domain features:
- amount, velocity, device_risk_score, is_decline
- hour_of_day_sin, hour_of_day_cos (cyclical diurnal temporal encoding)
- mcc_risk_weight (merchant category risk profiling)
- geo_distance_km (geographical displacement from home location)
- card_age_days (account/token longevity)
- failed_attempts_24h (prior authorization failures)
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional

MCC_RISK_MAP = {
    # High-Risk / Card Testing Target MCCs
    5999: 0.85,  # Miscellaneous Specialty Retail
    7399: 0.90,  # Business Services / Digital Services
    5816: 0.88,  # Digital Goods / Gaming / Tokens
    5968: 0.80,  # Direct Marketing - Continuity / Subscription
    5969: 0.82,  # Direct Marketing - Other
    # Moderate-Risk MCCs
    5311: 0.40,  # Department Stores
    4121: 0.35,  # Taxicabs & Rideshares
    7523: 0.30,  # Automobile Parking Lots / Meters
    # Low-Risk MCCs
    5411: 0.10,  # Grocery Stores / Supermarkets
    5812: 0.15,  # Eating Places / Restaurants
    5912: 0.12,  # Drug Stores & Pharmacies
    5541: 0.18,  # Service Stations (Fuel)
}

TABULAR_FEATURE_COLS = [
    "amount",
    "velocity",
    "device_risk_score",
    "is_decline",
    "hour_of_day_sin",
    "hour_of_day_cos",
    "mcc_risk_weight",
    "geo_distance_km",
    "card_age_days",
    "failed_attempts_24h"
]


def generate_tabular_card_testing(
    num_samples: int = 15000,
    fraud_ratio: float = 0.15,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generates realistic synthetic card transaction records with realistic feature distributions.
    Avoids artificial single-feature dominance so models learn multi-factor risk boundaries.
    """
    np.random.seed(random_seed)
    
    num_fraud = int(num_samples * fraud_ratio)
    num_legit = num_samples - num_fraud
    
    # ── 1. Legitimate Transactions ──
    legit_amounts = np.random.lognormal(mean=4.2, sigma=1.1, size=num_legit)  # Mean ~$75-$120
    legit_amounts = np.round(np.clip(legit_amounts, 5.0, 2500.0), 2)
    
    legit_mccs = np.random.choice([5411, 5812, 5912, 5311, 4121, 5541, 5999, 7523], size=num_legit, p=[0.25, 0.20, 0.15, 0.15, 0.10, 0.08, 0.04, 0.03])
    legit_mcc_weights = np.array([MCC_RISK_MAP.get(m, 0.2) for m in legit_mccs])
    legit_declines = np.random.choice([0, 1], size=num_legit, p=[0.97, 0.03])
    legit_timestamps = np.sort(np.random.uniform(0, 86400 * 7, size=num_legit))
    
    # Diurnal temporal distribution (normal daytime curve)
    legit_hours = (legit_timestamps % 86400) / 3600.0
    legit_hour_sin = np.round(np.sin(2 * np.pi * legit_hours / 24.0), 4)
    legit_hour_cos = np.round(np.cos(2 * np.pi * legit_hours / 24.0), 4)
    
    legit_risk_scores = np.round(np.random.beta(a=1.5, b=8.0, size=num_legit), 4)  # Low risk (mean ~0.15)
    legit_velocity = np.round(np.random.exponential(scale=1.5, size=num_legit) + 1.0, 2)  # Low velocity (1-3)
    legit_geo_dist = np.round(np.clip(np.random.exponential(scale=12.0, size=num_legit) + 0.5, 0.5, 350.0), 2)
    legit_card_age = np.round(np.random.uniform(30, 1800, size=num_legit), 0)  # 30 - 1800 days
    legit_failed_attempts = np.random.choice([0, 1], size=num_legit, p=[0.96, 0.04])
    
    df_legit = pd.DataFrame({
        "transaction_id": [f"TX_LEG_{i:06d}" for i in range(num_legit)],
        "timestamp_sec": legit_timestamps,
        "amount": legit_amounts,
        "mcc": legit_mccs,
        "mcc_risk_weight": legit_mcc_weights,
        "is_decline": legit_declines,
        "hour_of_day_sin": legit_hour_sin,
        "hour_of_day_cos": legit_hour_cos,
        "card_type": np.random.choice(["visa", "mastercard", "amex"], size=num_legit, p=[0.5, 0.4, 0.1]),
        "device_risk_score": legit_risk_scores,
        "velocity": legit_velocity,
        "geo_distance_km": legit_geo_dist,
        "card_age_days": legit_card_age,
        "failed_attempts_24h": legit_failed_attempts,
        "user_agent_category": "standard_browser",
        "is_fraud": 0,
        "attack_vector": "legitimate"
    })
    
    # ── 2. Synthetic Fraud Transactions ──
    # Combines: Micro-burst Card Testing (50%) + Compromised High-Value Card Fraud (50%)
    num_micro = int(num_fraud * 0.5)
    num_high_val = num_fraud - num_micro
    
    micro_amounts = np.random.uniform(0.50, 3.00, size=num_micro)
    high_val_amounts = np.random.lognormal(mean=5.5, sigma=1.0, size=num_high_val)
    fraud_amounts = np.round(np.clip(np.concatenate([micro_amounts, high_val_amounts]), 0.50, 4500.0), 2)
    np.random.shuffle(fraud_amounts)
    
    fraud_mccs = np.random.choice([5999, 7399, 5816, 5968, 5969, 5311, 5411], size=num_fraud, p=[0.35, 0.25, 0.20, 0.08, 0.06, 0.04, 0.02])
    fraud_mcc_weights = np.array([MCC_RISK_MAP.get(m, 0.85) for m in fraud_mccs])
    fraud_declines = np.random.choice([0, 1], size=num_fraud, p=[0.35, 0.65])
    
    base_time = np.random.uniform(0, 86400 * 7)
    time_jitters = np.cumsum(np.random.exponential(scale=12.0, size=num_fraud))
    fraud_timestamps = base_time + time_jitters
    
    fraud_hours = (fraud_timestamps % 86400) / 3600.0
    fraud_hour_sin = np.round(np.sin(2 * np.pi * fraud_hours / 24.0), 4)
    fraud_hour_cos = np.round(np.cos(2 * np.pi * fraud_hours / 24.0), 4)
    
    # Core Fraud Signals: High device risk, elevated velocity, failed attempts
    fraud_risk_scores = np.round(np.random.beta(a=6.0, b=2.0, size=num_fraud), 4)  # High risk (mean ~0.75)
    fraud_velocity = np.round(np.random.exponential(scale=8.0, size=num_fraud) + 5.0, 2)  # High velocity (5-30)
    
    # Realistic mixed geo-distance: 35% domestic proxy (5-80 km), 65% remote (200-5000 km)
    num_local_fraud = int(num_fraud * 0.35)
    num_remote_fraud = num_fraud - num_local_fraud
    local_geo = np.random.uniform(2.0, 75.0, size=num_local_fraud)
    remote_geo = np.random.uniform(200.0, 5000.0, size=num_remote_fraud)
    fraud_geo_dist = np.round(np.concatenate([local_geo, remote_geo]), 2)
    np.random.shuffle(fraud_geo_dist)
    
    # Realistic mixed card age: 40% fresh stolen tokens (1-45 days), 60% compromised aged cards (60-1500 days)
    num_fresh_cards = int(num_fraud * 0.40)
    num_aged_cards = num_fraud - num_fresh_cards
    fresh_card_age = np.random.uniform(1.0, 45.0, size=num_fresh_cards)
    aged_card_age = np.random.uniform(60.0, 1500.0, size=num_aged_cards)
    fraud_card_age = np.round(np.concatenate([fresh_card_age, aged_card_age]), 0)
    np.random.shuffle(fraud_card_age)
    
    fraud_failed_attempts = np.random.choice([1, 2, 3, 4, 5, 7], size=num_fraud, p=[0.15, 0.25, 0.30, 0.15, 0.10, 0.05])
    
    df_fraud = pd.DataFrame({
        "transaction_id": [f"TX_FRD_{i:06d}" for i in range(num_fraud)],
        "timestamp_sec": fraud_timestamps,
        "amount": fraud_amounts,
        "mcc": fraud_mccs,
        "mcc_risk_weight": fraud_mcc_weights,
        "is_decline": fraud_declines,
        "hour_of_day_sin": fraud_hour_sin,
        "hour_of_day_cos": fraud_hour_cos,
        "card_type": np.random.choice(["visa", "mastercard"], size=num_fraud, p=[0.6, 0.4]),
        "device_risk_score": fraud_risk_scores,
        "velocity": fraud_velocity,
        "geo_distance_km": fraud_geo_dist,
        "card_age_days": fraud_card_age,
        "failed_attempts_24h": fraud_failed_attempts,
        "user_agent_category": "headless_chrome_bot",
        "is_fraud": 1,
        "attack_vector": "evasive_card_testing"
    })
    
    # ── 3. Hard-Negative Legitimate Transactions (Edge Cases) ──
    num_hard_neg = int(num_legit * 0.25)
    
    # Coffee/parking buyers ($0.50-$3.50 amounts overlap with micro-bursts, but low velocity)
    num_coffee = num_hard_neg // 3
    coffee_amounts = np.round(np.random.uniform(0.50, 3.50, size=num_coffee), 2)
    coffee_risk = np.round(np.random.beta(a=2.0, b=5.0, size=num_coffee), 4)
    coffee_velocity = np.round(np.random.uniform(1.0, 4.0, size=num_coffee), 2)
    coffee_declines = np.random.choice([0, 1], size=num_coffee, p=[0.88, 0.12])
    coffee_geo = np.round(np.random.uniform(0.5, 20.0, size=num_coffee), 2)
    coffee_mccs = np.random.choice([5411, 5812, 7523], size=num_coffee)
    coffee_card_age = np.round(np.random.uniform(30, 1500, size=num_coffee), 0)
    coffee_failed = np.random.choice([0, 1], size=num_coffee, p=[0.92, 0.08])
    
    # VPN / Travelers: high geo-distance (500-2500 km) and higher device risk (0.6-0.9), but low velocity and 0 declines
    num_vpn = num_hard_neg // 3
    vpn_amounts = np.round(np.clip(np.random.lognormal(mean=4.2, sigma=1.1, size=num_vpn), 5.0, 2500.0), 2)
    vpn_risk = np.round(np.random.uniform(0.55, 0.88, size=num_vpn), 4)
    vpn_velocity = np.round(np.random.exponential(scale=1.5, size=num_vpn) + 1.0, 2)  # Low velocity
    vpn_declines = np.random.choice([0, 1], size=num_vpn, p=[0.95, 0.05])
    vpn_geo = np.round(np.random.uniform(300.0, 2500.0, size=num_vpn), 2)
    vpn_mccs = np.random.choice([5311, 4121, 5812], size=num_vpn)
    vpn_card_age = np.round(np.random.uniform(60, 1500, size=num_vpn), 0)
    vpn_failed = np.random.choice([0, 1], size=num_vpn, p=[0.94, 0.06])
    
    # Power shoppers / Flash sale buyers: high velocity (8-18 tx/hr), but clean device (0.1-0.3)
    num_power = num_hard_neg - num_coffee - num_vpn
    power_amounts = np.round(np.clip(np.random.lognormal(mean=3.5, sigma=0.8, size=num_power), 5.0, 500.0), 2)
    power_risk = np.round(np.random.beta(a=1.5, b=6.0, size=num_power), 4)  # Low/clean device risk
    power_velocity = np.round(np.random.uniform(8.0, 22.0, size=num_power), 2)
    power_declines = np.random.choice([0, 1], size=num_power, p=[0.85, 0.15])
    power_geo = np.round(np.random.uniform(1.0, 45.0, size=num_power), 2)
    power_mccs = np.random.choice([5311, 5999, 5816], size=num_power)
    power_card_age = np.round(np.random.uniform(60, 1200, size=num_power), 0)
    power_failed = np.random.choice([0, 1], size=num_power, p=[0.90, 0.10])
    
    hn_amounts = np.concatenate([coffee_amounts, vpn_amounts, power_amounts])
    hn_risk = np.concatenate([coffee_risk, vpn_risk, power_risk])
    hn_velocity = np.concatenate([coffee_velocity, vpn_velocity, power_velocity])
    hn_declines = np.concatenate([coffee_declines, vpn_declines, power_declines])
    hn_geo = np.concatenate([coffee_geo, vpn_geo, power_geo])
    hn_mccs = np.concatenate([coffee_mccs, vpn_mccs, power_mccs])
    hn_mcc_weights = np.array([MCC_RISK_MAP.get(m, 0.3) for m in hn_mccs])
    hn_card_age = np.concatenate([coffee_card_age, vpn_card_age, power_card_age])
    hn_failed = np.concatenate([coffee_failed, vpn_failed, power_failed])
    
    hn_timestamps = np.sort(np.random.uniform(0, 86400 * 7, size=num_hard_neg))
    hn_hours = (hn_timestamps % 86400) / 3600.0
    hn_hour_sin = np.round(np.sin(2 * np.pi * hn_hours / 24.0), 4)
    hn_hour_cos = np.round(np.cos(2 * np.pi * hn_hours / 24.0), 4)
    
    df_hard_neg = pd.DataFrame({
        "transaction_id": [f"TX_HN_{i:06d}" for i in range(num_hard_neg)],
        "timestamp_sec": hn_timestamps,
        "amount": hn_amounts,
        "mcc": hn_mccs,
        "mcc_risk_weight": hn_mcc_weights,
        "is_decline": hn_declines,
        "hour_of_day_sin": hn_hour_sin,
        "hour_of_day_cos": hn_hour_cos,
        "card_type": np.random.choice(["visa", "mastercard", "amex"], size=num_hard_neg, p=[0.5, 0.4, 0.1]),
        "device_risk_score": hn_risk,
        "velocity": hn_velocity,
        "geo_distance_km": hn_geo,
        "card_age_days": hn_card_age,
        "failed_attempts_24h": hn_failed,
        "user_agent_category": "standard_browser",
        "is_fraud": 0,
        "attack_vector": "legitimate_hard_negative"
    })
    
    # Combine and sort by timestamp
    df = pd.concat([df_legit, df_fraud, df_hard_neg], ignore_index=True)
    df = df.sort_values("timestamp_sec").reset_index(drop=True)
    return df


if __name__ == "__main__":
    df_test = generate_tabular_card_testing(num_samples=1000)
    print(f"Generated {len(df_test)} transactions with {len(TABULAR_FEATURE_COLS)} features.")
    print(df_test[TABULAR_FEATURE_COLS + ['is_fraud']].head())
