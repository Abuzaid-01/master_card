"""
Vector 5 Generator: AI-Automated Evasive Card Testing & Fraud Transactions
Generates synthetic tabular card authorization records simulating evasive card testing and realistic fraud spending.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional

def generate_tabular_card_testing(
    num_samples: int = 1000,
    fraud_ratio: float = 0.15,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generates synthetic card transaction records.
    
    Legitimate transactions follow standard spending patterns.
    Fraudulent transactions feature:
    - Mix of low-and-slow micro-amounts ($0.50 - $2.50) and high-value fraud ($50 - $850)
    - High frequency velocity across disparate Merchant Category Codes (MCCs)
    - Elevated device risk scores & proxy IP rotation
    - Elevated decline rates (invalid CVV / expired date)
    """
    np.random.seed(random_seed)
    
    num_fraud = int(num_samples * fraud_ratio)
    num_legit = num_samples - num_fraud
    
    # 1. Legitimate Transactions
    legit_amounts = np.random.lognormal(mean=4.2, sigma=1.1, size=num_legit)  # Mean ~$75-$120
    legit_amounts = np.round(np.clip(legit_amounts, 5.0, 2500.0), 2)
    
    legit_mccs = np.random.choice([5411, 5812, 5912, 5311, 4121, 5541], size=num_legit)
    legit_declines = np.random.choice([0, 1], size=num_legit, p=[0.97, 0.03])
    legit_timestamps = np.sort(np.random.uniform(0, 86400 * 7, size=num_legit))
    legit_risk_scores = np.round(np.random.beta(a=1.5, b=8.0, size=num_legit), 4)  # Low risk (mean ~0.15)
    legit_velocity = np.round(np.random.exponential(scale=1.5, size=num_legit) + 1.0, 2)  # Low velocity (1-3)
    
    df_legit = pd.DataFrame({
        "transaction_id": [f"TX_LEG_{i:06d}" for i in range(num_legit)],
        "timestamp_sec": legit_timestamps,
        "amount": legit_amounts,
        "mcc": legit_mccs,
        "is_decline": legit_declines,
        "card_type": np.random.choice(["visa", "mastercard", "amex"], size=num_legit, p=[0.5, 0.4, 0.1]),
        "device_risk_score": legit_risk_scores,
        "velocity": legit_velocity,
        "user_agent_category": "standard_browser",
        "is_fraud": 0,
        "attack_vector": "legitimate"
    })
    
    # 2. Synthetic Fraud Transactions (Micro-bursts + High-value Fraud)
    num_micro = int(num_fraud * 0.5)
    num_high_val = num_fraud - num_micro
    
    micro_amounts = np.random.uniform(0.50, 3.00, size=num_micro)
    high_val_amounts = np.random.lognormal(mean=5.2, sigma=1.0, size=num_high_val)
    fraud_amounts = np.round(np.clip(np.concatenate([micro_amounts, high_val_amounts]), 0.50, 4500.0), 2)
    np.random.shuffle(fraud_amounts)
    
    fraud_mccs = np.random.choice([5999, 7399, 5816, 5968, 5969], size=num_fraud)
    fraud_declines = np.random.choice([0, 1], size=num_fraud, p=[0.40, 0.60])
    
    base_time = np.random.uniform(0, 86400 * 7)
    time_jitters = np.cumsum(np.random.exponential(scale=15.0, size=num_fraud))
    fraud_timestamps = base_time + time_jitters
    fraud_risk_scores = np.round(np.random.beta(a=6.0, b=2.0, size=num_fraud), 4)  # High risk (mean ~0.75)
    fraud_velocity = np.round(np.random.exponential(scale=8.0, size=num_fraud) + 4.0, 2)  # High velocity (4-25)
    
    df_fraud = pd.DataFrame({
        "transaction_id": [f"TX_FRD_{i:06d}" for i in range(num_fraud)],
        "timestamp_sec": fraud_timestamps,
        "amount": fraud_amounts,
        "mcc": fraud_mccs,
        "is_decline": fraud_declines,
        "card_type": np.random.choice(["visa", "mastercard"], size=num_fraud, p=[0.6, 0.4]),
        "device_risk_score": fraud_risk_scores,
        "velocity": fraud_velocity,
        "user_agent_category": "headless_chrome_bot",
        "is_fraud": 1,
        "attack_vector": "evasive_card_testing"
    })
    
    # 3. Hard-Negative Legitimate Transactions (overlap with fraud feature ranges)
    # These force the classifier to learn a real decision boundary, not just trivial separation.
    num_hard_neg = int(num_legit * 0.25)  # ~25% of legit are confusing cases
    
    # Coffee/parking buyers: $0.50-$3.00 amounts (overlaps with micro-burst fraud amounts)
    num_coffee = num_hard_neg // 3
    coffee_amounts = np.round(np.random.uniform(0.50, 3.50, size=num_coffee), 2)
    coffee_risk = np.round(np.random.beta(a=2.0, b=5.0, size=num_coffee), 4)  # Slightly elevated risk
    coffee_velocity = np.round(np.random.uniform(2.0, 6.0, size=num_coffee), 2)  # Morning coffee + newspaper
    coffee_declines = np.random.choice([0, 1], size=num_coffee, p=[0.85, 0.15])  # Occasional NFC fails
    
    # VPN/privacy users: high device_risk_score (0.55-0.95) but normal behavior
    num_vpn = num_hard_neg // 3
    vpn_amounts = np.round(np.random.lognormal(mean=4.2, sigma=1.1, size=num_vpn), 2)
    vpn_amounts = np.clip(vpn_amounts, 5.0, 2500.0)
    vpn_risk = np.round(np.random.uniform(0.55, 0.95, size=num_vpn), 4)  # Heavy overlap with fraud risk
    vpn_velocity = np.round(np.random.exponential(scale=2.0, size=num_vpn) + 1.0, 2)
    vpn_declines = np.random.choice([0, 1], size=num_vpn, p=[0.90, 0.10])
    
    # Power shoppers: high velocity (6-20 tx/hour) during flash sales
    num_power = num_hard_neg - num_coffee - num_vpn
    power_amounts = np.round(np.random.lognormal(mean=3.5, sigma=0.8, size=num_power), 2)
    power_amounts = np.clip(power_amounts, 5.0, 500.0)
    power_risk = np.round(np.random.beta(a=3.0, b=4.0, size=num_power), 4)  # Moderate risk
    power_velocity = np.round(np.random.uniform(6.0, 20.0, size=num_power), 2)  # Heavy overlap with fraud velocity
    power_declines = np.random.choice([0, 1], size=num_power, p=[0.80, 0.20])  # Some declines from rapid auth
    
    hn_amounts = np.concatenate([coffee_amounts, vpn_amounts, power_amounts])
    hn_risk = np.concatenate([coffee_risk, vpn_risk, power_risk])
    hn_velocity = np.concatenate([coffee_velocity, vpn_velocity, power_velocity])
    hn_declines = np.concatenate([coffee_declines, vpn_declines, power_declines])
    
    df_hard_neg = pd.DataFrame({
        "transaction_id": [f"TX_HN_{i:06d}" for i in range(num_hard_neg)],
        "timestamp_sec": np.sort(np.random.uniform(0, 86400 * 7, size=num_hard_neg)),
        "amount": hn_amounts,
        "mcc": np.random.choice([5411, 5812, 5912, 5311, 4121, 5541, 7523], size=num_hard_neg),
        "is_decline": hn_declines,
        "card_type": np.random.choice(["visa", "mastercard", "amex"], size=num_hard_neg, p=[0.5, 0.4, 0.1]),
        "device_risk_score": hn_risk,
        "velocity": hn_velocity,
        "user_agent_category": "standard_browser",
        "is_fraud": 0,
        "attack_vector": "legitimate_hard_negative"
    })
    
    # Combine and sort by timestamp
    df = pd.concat([df_legit, df_fraud, df_hard_neg], ignore_index=True)
    df = df.sort_values("timestamp_sec").reset_index(drop=True)
    return df

if __name__ == "__main__":
    df_test = generate_tabular_card_testing(num_samples=100)
    print(f"Generated {len(df_test)} transactions.")
    print(df_test.head())
