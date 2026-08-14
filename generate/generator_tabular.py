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
    
    # Combine and sort by timestamp
    df = pd.concat([df_legit, df_fraud], ignore_index=True)
    df = df.sort_values("timestamp_sec").reset_index(drop=True)
    return df

if __name__ == "__main__":
    df_test = generate_tabular_card_testing(num_samples=100)
    print(f"Generated {len(df_test)} transactions.")
    print(df_test.head())
