"""
Vector 5 Generator: AI-Automated Evasive Card Testing (Micro-Bursts)
Generates synthetic tabular card authorization records simulating low-and-slow micro-burst card testing.
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
    Fraudulent micro-burst transactions feature:
    - Micro-amounts ($0.50 - $2.50)
    - High frequency across disparate Merchant Category Codes (MCCs)
    - Simulated human circadian latency & proxy IP rotation
    - Elevated decline rates (invalid CVV / expired date)
    """
    np.random.seed(random_seed)
    
    num_fraud = int(num_samples * fraud_ratio)
    num_legit = num_samples - num_fraud
    
    # 1. Legitimate Transactions
    legit_amounts = np.random.lognormal(mean=3.5, sigma=1.0, size=num_legit)  # ~$30-$100
    legit_amounts = np.round(np.clip(legit_amounts, 5.0, 2500.0), 2)
    
    legit_mccs = np.random.choice([5411, 5812, 5912, 5311, 4121, 5541], size=num_legit)  # Groceries, Dining, etc.
    legit_declines = np.random.choice([0, 1], size=num_legit, p=[0.97, 0.03])
    legit_timestamps = np.sort(np.random.uniform(0, 86400 * 7, size=num_legit))
    legit_risk_scores = np.round(np.random.beta(a=1.5, b=8.0, size=num_legit), 4)
    
    df_legit = pd.DataFrame({
        "transaction_id": [f"TX_LEG_{i:06d}" for i in range(num_legit)],
        "timestamp_sec": legit_timestamps,
        "amount": legit_amounts,
        "mcc": legit_mccs,
        "is_decline": legit_declines,
        "card_type": np.random.choice(["visa", "mastercard", "amex"], size=num_legit, p=[0.5, 0.4, 0.1]),
        "device_risk_score": legit_risk_scores,
        "user_agent_category": "standard_browser",
        "is_fraud": 0,
        "attack_vector": "legitimate"
    })
    
    # 2. Synthetic Micro-Burst Card Testing Fraud
    fraud_amounts = np.round(np.random.uniform(0.50, 2.50, size=num_fraud), 2)
    fraud_mccs = np.random.choice([5999, 7399, 5816, 5968, 5969], size=num_fraud)  # Digital goods, misc direct marketing
    fraud_declines = np.random.choice([0, 1], size=num_fraud, p=[0.40, 0.60])  # Elevated decline rate (invalid CVV/expiry)
    
    # Low-and-slow micro-burst timing jitter
    base_time = np.random.uniform(0, 86400 * 7)
    time_jitters = np.cumsum(np.random.exponential(scale=15.0, size=num_fraud))  # Every 15 seconds on average
    fraud_timestamps = base_time + time_jitters
    fraud_risk_scores = np.round(np.random.beta(a=4.0, b=3.0, size=num_fraud), 4)  # Hovering near decision boundary
    
    df_fraud = pd.DataFrame({
        "transaction_id": [f"TX_FRD_MICRO_{i:06d}" for i in range(num_fraud)],
        "timestamp_sec": fraud_timestamps,
        "amount": fraud_amounts,
        "mcc": fraud_mccs,
        "is_decline": fraud_declines,
        "card_type": np.random.choice(["visa", "mastercard"], size=num_fraud, p=[0.6, 0.4]),
        "device_risk_score": fraud_risk_scores,
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
