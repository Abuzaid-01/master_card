"""
Vector 5 Generator: Multi-Pattern Evasive Card Testing & Credit Card Fraud
Generates synthetic tabular card authorization records across 5 distinct fraud patterns:
1. Card Testing Burst (micro-amounts, high velocity, high device risk)
2. Account Takeover (ATO) (normal amounts, new device, extreme geo distance, low velocity)
3. High-Velocity Automated Bot Siphon (script velocity 8-35 tx/min, spoofed device telemetry)
4. Card-Not-Present (CNP) (high-value online digital goods, elevated device risk)
5. Slow Drip Siphon (sub-radar recurring charges across days)

Legitimate transactions model enterprise consumer spending across 3 tiers:
- Everyday micro/daily ($2.50 - $65.00, velocity 0.5 - 2.5 tx/min)
- Standard retail & dining ($65.00 - $450.00, velocity 0.5 - 2.5 tx/min)
- High-value major commerce ($450.00 - $4,200.00, velocity 0.5 - 2.0 tx/min) on clean devices

Includes 10 enterprise-grade domain features:
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
    num_samples: int = 50000,
    fraud_ratio: float = 0.15,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generates realistic synthetic card transaction records with multi-factor risk boundaries.
    Properly balances velocity, device risk, amount, and geography so each signal acts independently.
    """
    np.random.seed(random_seed)
    
    num_fraud = int(num_samples * fraud_ratio)
    num_legit = num_samples - num_fraud
    
    # ── 1. Legitimate Standard Transactions (75% of legit) ──
    num_standard_legit = int(num_legit * 0.75)
    
    # Tier 1: Everyday micro/daily (35% of std legit) -> $2.50 to $65.00, normal velocity 0.5 - 2.5 tx/min
    n_everyday = int(num_standard_legit * 0.35)
    amt_everyday = np.round(np.random.uniform(2.50, 65.0, size=n_everyday), 2)
    mcc_everyday = np.random.choice([5411, 5812, 5912, 4121, 5541, 7523], size=n_everyday)
    risk_everyday = np.round(np.random.beta(1.2, 8.0, size=n_everyday), 4)
    vel_everyday = np.round(np.random.uniform(0.5, 2.5, size=n_everyday), 2)
    geo_everyday = np.round(np.random.uniform(0.5, 35.0, size=n_everyday), 2)
    
    # Tier 2: Standard retail, utilities & dining (35% of std legit) -> $65.00 to $450.00
    n_retail = int(num_standard_legit * 0.35)
    amt_retail = np.round(np.random.uniform(65.0, 450.0, size=n_retail), 2)
    mcc_retail = np.random.choice([5311, 5812, 5999, 5541, 4121], size=n_retail)
    risk_retail = np.round(np.random.beta(1.2, 8.0, size=n_retail), 4)
    vel_retail = np.round(np.random.uniform(0.5, 2.5, size=n_retail), 2)
    geo_retail = np.round(np.random.uniform(1.0, 65.0, size=n_retail), 2)
    
    # Tier 3: Major high-value legitimate purchases (30% of std legit) -> $450.00 to $4,200.00
    # (e.g. Laptops, Apple Store, flights, rent, furniture, appliances on clean devices at normal velocity)
    n_highval = num_standard_legit - n_everyday - n_retail
    amt_highval = np.round(np.random.uniform(450.0, 4200.0, size=n_highval), 2)
    mcc_highval = np.random.choice([5311, 5999, 5816, 5812, 4121], size=n_highval)
    risk_highval = np.round(np.random.beta(1.0, 10.0, size=n_highval), 4)  # Clean device 0.01 - 0.15
    vel_highval = np.round(np.random.uniform(0.5, 2.0, size=n_highval), 2)  # Normal velocity
    geo_highval = np.round(np.random.uniform(1.0, 40.0, size=n_highval), 2)  # Domestic home location
    
    amt_legit = np.concatenate([amt_everyday, amt_retail, amt_highval])
    mcc_legit = np.concatenate([mcc_everyday, mcc_retail, mcc_highval])
    risk_legit = np.concatenate([risk_everyday, risk_retail, risk_highval])
    vel_legit = np.concatenate([vel_everyday, vel_retail, vel_highval])
    geo_legit = np.concatenate([geo_everyday, geo_retail, geo_highval])
    
    ts_legit = np.sort(np.random.uniform(0, 86400 * 7, size=num_standard_legit))
    hours_legit = (ts_legit % 86400) / 3600.0
    hour_sin_legit = np.round(np.sin(2 * np.pi * hours_legit / 24.0), 4)
    hour_cos_legit = np.round(np.cos(2 * np.pi * hours_legit / 24.0), 4)
    
    df_legit = pd.DataFrame({
        "transaction_id": [f"TX_LEG_{i:06d}" for i in range(num_standard_legit)],
        "timestamp_sec": ts_legit,
        "amount": amt_legit,
        "mcc": mcc_legit,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.20) for m in mcc_legit]),
        "is_decline": np.random.choice([0, 1], size=num_standard_legit, p=[0.98, 0.02]),
        "hour_of_day_sin": hour_sin_legit,
        "hour_of_day_cos": hour_cos_legit,
        "card_type": np.random.choice(["visa", "mastercard", "amex"], size=num_standard_legit, p=[0.5, 0.4, 0.1]),
        "device_risk_score": risk_legit,
        "velocity": vel_legit,
        "geo_distance_km": geo_legit,
        "card_age_days": np.round(np.random.uniform(60, 1800, size=num_standard_legit), 0),
        "failed_attempts_24h": np.random.choice([0, 1], size=num_standard_legit, p=[0.97, 0.03]),
        "user_agent_category": "standard_browser",
        "is_fraud": 0,
        "attack_vector": "legitimate",
        "fraud_subtype": "legitimate"
    })
    
    # ── 2. Hard-Negative Legitimate Transactions (25% of legit) ──
    num_hard_neg = num_legit - num_standard_legit
    num_coffee = num_hard_neg // 3
    num_vpn = num_hard_neg // 3
    num_power = num_hard_neg - num_coffee - num_vpn
    
    # Coffee/parking buyers ($0.50-$3.50 amounts, low velocity 0.5 - 2.0)
    c_amt = np.round(np.random.uniform(0.50, 3.50, size=num_coffee), 2)
    c_vel = np.round(np.random.uniform(0.5, 2.0, size=num_coffee), 2)
    c_risk = np.round(np.random.beta(1.5, 6.0, size=num_coffee), 4)
    c_geo = np.round(np.random.uniform(0.5, 20.0, size=num_coffee), 2)
    c_mcc = np.random.choice([5411, 5812, 7523], size=num_coffee)
    
    # VPN / Travelers: high geo-distance (400-2500 km) and higher device risk (0.55-0.85), but human velocity (0.5 - 2.5)
    v_amt = np.round(np.random.uniform(20.0, 2500.0, size=num_vpn), 2)
    v_vel = np.round(np.random.uniform(0.5, 2.5, size=num_vpn), 2)
    v_risk = np.round(np.random.uniform(0.55, 0.85, size=num_vpn), 4)
    v_geo = np.round(np.random.uniform(400.0, 2500.0, size=num_vpn), 2)
    v_mcc = np.random.choice([5311, 4121, 5812], size=num_vpn)
    
    # Power shoppers / Flash sale buyers: human upper limit velocity (2.0 - 4.5 tx/min), clean device (0.05-0.20)
    p_amt = np.round(np.random.uniform(20.0, 500.0, size=num_power), 2)
    p_vel = np.round(np.random.uniform(2.0, 4.5, size=num_power), 2)
    p_risk = np.round(np.random.beta(1.0, 8.0, size=num_power), 4)
    p_geo = np.round(np.random.uniform(1.0, 45.0, size=num_power), 2)
    p_mcc = np.random.choice([5311, 5999, 5816], size=num_power)
    
    hn_amt = np.concatenate([c_amt, v_amt, p_amt])
    hn_vel = np.concatenate([c_vel, v_vel, p_vel])
    hn_risk = np.concatenate([c_risk, v_risk, p_risk])
    hn_geo = np.concatenate([c_geo, v_geo, p_geo])
    hn_mcc = np.concatenate([c_mcc, v_mcc, p_mcc])
    
    hn_ts = np.sort(np.random.uniform(0, 86400 * 7, size=num_hard_neg))
    hn_hours = (hn_ts % 86400) / 3600.0
    
    df_hard_neg = pd.DataFrame({
        "transaction_id": [f"TX_HN_{i:06d}" for i in range(num_hard_neg)],
        "timestamp_sec": hn_ts,
        "amount": hn_amt,
        "mcc": hn_mcc,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.30) for m in hn_mcc]),
        "is_decline": np.random.choice([0, 1], size=num_hard_neg, p=[0.94, 0.06]),
        "hour_of_day_sin": np.round(np.sin(2 * np.pi * hn_hours / 24.0), 4),
        "hour_of_day_cos": np.round(np.cos(2 * np.pi * hn_hours / 24.0), 4),
        "card_type": np.random.choice(["visa", "mastercard", "amex"], size=num_hard_neg, p=[0.5, 0.4, 0.1]),
        "device_risk_score": hn_risk,
        "velocity": hn_vel,
        "geo_distance_km": hn_geo,
        "card_age_days": np.round(np.random.uniform(60, 1500, size=num_hard_neg), 0),
        "failed_attempts_24h": np.random.choice([0, 1], size=num_hard_neg, p=[0.95, 0.05]),
        "user_agent_category": "standard_browser",
        "is_fraud": 0,
        "attack_vector": "legitimate_hard_negative",
        "fraud_subtype": "legitimate_hard_negative"
    })
    
    # ── 3. Multi-Pattern Synthetic Fraud Transactions (5 Sub-Types) ──
    n_p1 = num_fraud // 5  # Card Testing Burst
    n_p2 = num_fraud // 5  # Account Takeover (ATO)
    n_p3 = num_fraud // 5  # High-Velocity Bot Siphon (spoofed clean device)
    n_p4 = num_fraud // 5  # Card-Not-Present (CNP)
    n_p5 = num_fraud - (n_p1 + n_p2 + n_p3 + n_p4)  # Slow Drip Siphon
    
    fraud_frames = []
    
    # Sub-Type 1: Card Testing Burst (micro amounts + drain, HIGH velocity 8-32, HIGH device risk 0.75-0.95, declines)
    p1_micro = int(n_p1 * 0.6)
    p1_drain = n_p1 - p1_micro
    p1_amounts = np.concatenate([
        np.random.uniform(0.50, 3.00, size=p1_micro),
        np.random.uniform(1500.0, 4000.0, size=p1_drain)
    ])
    np.random.shuffle(p1_amounts)
    p1_mccs = np.random.choice([5999, 7399, 5816, 5968, 5541, 5812, 7523], size=n_p1, p=[0.30, 0.20, 0.20, 0.10, 0.10, 0.05, 0.05])
    p1_declines = np.random.choice([0, 1], size=n_p1, p=[0.30, 0.70])
    p1_risk = np.round(np.random.beta(6.0, 1.5, size=n_p1), 4)  # High risk ~0.80
    p1_velocity = np.round(np.random.uniform(8.0, 32.0, size=n_p1), 2)  # High burst velocity
    p1_geo = np.round(np.random.uniform(10.0, 4000.0, size=n_p1), 2)
    p1_age = np.round(np.random.uniform(5.0, 500.0, size=n_p1), 0)
    p1_failed = np.random.choice([2, 3, 4, 5, 7], size=n_p1)
    p1_ts = np.sort(np.random.uniform(0, 86400 * 7, size=n_p1))
    p1_hours = (p1_ts % 86400) / 3600.0
    
    df_p1 = pd.DataFrame({
        "transaction_id": [f"TX_FRD_BURST_{i:06d}" for i in range(n_p1)],
        "timestamp_sec": p1_ts,
        "amount": np.round(p1_amounts, 2),
        "mcc": p1_mccs,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.85) for m in p1_mccs]),
        "is_decline": p1_declines,
        "hour_of_day_sin": np.round(np.sin(2 * np.pi * p1_hours / 24.0), 4),
        "hour_of_day_cos": np.round(np.cos(2 * np.pi * p1_hours / 24.0), 4),
        "card_type": np.random.choice(["visa", "mastercard"], size=n_p1, p=[0.6, 0.4]),
        "device_risk_score": p1_risk,
        "velocity": p1_velocity,
        "geo_distance_km": p1_geo,
        "card_age_days": p1_age,
        "failed_attempts_24h": p1_failed,
        "user_agent_category": "headless_chrome_bot",
        "is_fraud": 1,
        "attack_vector": "card_testing_burst",
        "fraud_subtype": "card_testing_burst"
    })
    fraud_frames.append(df_p1)
    
    # Sub-Type 2: Account Takeover (ATO) (High amount $500-$3500 + EXTREME DEVICE RISK 0.78-0.98 + FOREIGN GEO 3000-6800 km)
    p2_amounts = np.round(np.random.uniform(500.0, 3500.0, size=n_p2), 2)
    p2_mccs = np.random.choice([5311, 5999, 5816, 5812, 7399, 5411], size=n_p2, p=[0.30, 0.25, 0.20, 0.15, 0.05, 0.05])
    p2_declines = np.random.choice([0, 1], size=n_p2, p=[0.85, 0.15])
    p2_risk = np.round(np.random.uniform(0.78, 0.98, size=n_p2), 4)  # High device risk (unrecognized device)
    p2_velocity = np.round(np.random.uniform(1.0, 3.0, size=n_p2), 2)  # Low velocity
    p2_geo = np.round(np.random.uniform(3000.0, 6800.0, size=n_p2), 2)  # Foreign country jump / proxy
    p2_age = np.round(np.random.uniform(180.0, 1500.0, size=n_p2), 0)
    p2_failed = np.random.choice([0, 1, 2], size=n_p2, p=[0.70, 0.20, 0.10])
    p2_ts = np.sort(np.random.uniform(0, 86400 * 7, size=n_p2))
    p2_hours = (p2_ts % 86400) / 3600.0
    
    df_p2 = pd.DataFrame({
        "transaction_id": [f"TX_FRD_ATO_{i:06d}" for i in range(n_p2)],
        "timestamp_sec": p2_ts,
        "amount": p2_amounts,
        "mcc": p2_mccs,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.40) for m in p2_mccs]),
        "is_decline": p2_declines,
        "hour_of_day_sin": np.round(np.sin(2 * np.pi * p2_hours / 24.0), 4),
        "hour_of_day_cos": np.round(np.cos(2 * np.pi * p2_hours / 24.0), 4),
        "card_type": np.random.choice(["visa", "mastercard", "amex"], size=n_p2, p=[0.5, 0.4, 0.1]),
        "device_risk_score": p2_risk,
        "velocity": p2_velocity,
        "geo_distance_km": p2_geo,
        "card_age_days": p2_age,
        "failed_attempts_24h": p2_failed,
        "user_agent_category": "spoofed_mobile_browser",
        "is_fraud": 1,
        "attack_vector": "account_takeover",
        "fraud_subtype": "account_takeover"
    })
    fraud_frames.append(df_p2)
    
    # Sub-Type 3: High-Velocity Bot Swarm (Script Velocity 8-35 tx/min on spoofed residential clean device)
    p3_amounts = np.round(np.random.uniform(150.0, 3500.0, size=n_p3), 2)
    p3_mccs = np.random.choice([5311, 5999, 5816, 5812, 5541, 4121], size=n_p3, p=[0.30, 0.25, 0.20, 0.15, 0.05, 0.05])
    p3_declines = np.random.choice([0, 1], size=n_p3, p=[0.85, 0.15])
    p3_risk = np.round(np.random.uniform(0.05, 0.40, size=n_p3), 4)  # Spoofed low/moderate device risk
    p3_velocity = np.round(np.random.uniform(8.0, 35.0, size=n_p3), 2)  # HIGH script velocity anomaly
    p3_geo = np.round(np.random.uniform(5.0, 250.0, size=n_p3), 2)
    p3_age = np.round(np.random.uniform(60.0, 1200.0, size=n_p3), 0)
    p3_failed = np.random.choice([0, 1, 2], size=n_p3, p=[0.7, 0.2, 0.1])
    p3_ts = np.sort(np.random.uniform(0, 86400 * 7, size=n_p3))
    p3_hours = (p3_ts % 86400) / 3600.0
    
    df_p3 = pd.DataFrame({
        "transaction_id": [f"TX_FRD_BOT_{i:06d}" for i in range(n_p3)],
        "timestamp_sec": p3_ts,
        "amount": p3_amounts,
        "mcc": p3_mccs,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.35) for m in p3_mccs]),
        "is_decline": p3_declines,
        "hour_of_day_sin": np.round(np.sin(2 * np.pi * p3_hours / 24.0), 4),
        "hour_of_day_cos": np.round(np.cos(2 * np.pi * p3_hours / 24.0), 4),
        "card_type": np.random.choice(["visa", "mastercard"], size=n_p3, p=[0.55, 0.45]),
        "device_risk_score": p3_risk,
        "velocity": p3_velocity,
        "geo_distance_km": p3_geo,
        "card_age_days": p3_age,
        "failed_attempts_24h": p3_failed,
        "user_agent_category": "residential_proxy_bot",
        "is_fraud": 1,
        "attack_vector": "high_velocity_bot",
        "fraud_subtype": "high_velocity_bot"
    })
    fraud_frames.append(df_p3)
    
    # Sub-Type 4: Card-Not-Present (CNP) ($150-$3000 online digital goods, elevated device risk 0.65-0.88, vel 2-5)
    p4_amounts = np.round(np.random.uniform(150.0, 3000.0, size=n_p4), 2)
    p4_mccs = np.random.choice([5816, 7399, 5999, 5969, 5311], size=n_p4, p=[0.40, 0.25, 0.20, 0.10, 0.05])
    p4_declines = np.random.choice([0, 1], size=n_p4, p=[0.70, 0.30])
    p4_risk = np.round(np.random.uniform(0.65, 0.88, size=n_p4), 4)
    p4_velocity = np.round(np.random.uniform(2.0, 5.0, size=n_p4), 2)
    p4_geo = np.round(np.random.uniform(100.0, 2500.0, size=n_p4), 2)
    p4_age = np.round(np.random.uniform(10.0, 800.0, size=n_p4), 0)
    p4_failed = np.random.choice([1, 2, 3], size=n_p4)
    p4_ts = np.sort(np.random.uniform(0, 86400 * 7, size=n_p4))
    p4_hours = (p4_ts % 86400) / 3600.0
    
    df_p4 = pd.DataFrame({
        "transaction_id": [f"TX_FRD_CNP_{i:06d}" for i in range(n_p4)],
        "timestamp_sec": p4_ts,
        "amount": p4_amounts,
        "mcc": p4_mccs,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.88) for m in p4_mccs]),
        "is_decline": p4_declines,
        "hour_of_day_sin": np.round(np.sin(2 * np.pi * p4_hours / 24.0), 4),
        "hour_of_day_cos": np.round(np.cos(2 * np.pi * p4_hours / 24.0), 4),
        "card_type": np.random.choice(["visa", "mastercard"], size=n_p4, p=[0.5, 0.5]),
        "device_risk_score": p4_risk,
        "velocity": p4_velocity,
        "geo_distance_km": p4_geo,
        "card_age_days": p4_age,
        "failed_attempts_24h": p4_failed,
        "user_agent_category": "automated_script",
        "is_fraud": 1,
        "attack_vector": "cnp_fraud",
        "fraud_subtype": "cnp_fraud"
    })
    fraud_frames.append(df_p4)
    
    # Sub-Type 5: Slow Drip Siphon ($18-$85 recurring, elevated proxy 0.50-0.75, high mcc weight 0.88)
    p5_amounts = np.round(np.random.uniform(18.0, 85.0, size=n_p5), 2)
    p5_mccs = np.random.choice([5968, 5816, 7399, 5969], size=n_p5, p=[0.40, 0.30, 0.20, 0.10])
    p5_declines = np.random.choice([0, 1], size=n_p5, p=[0.95, 0.05])
    p5_risk = np.round(np.random.uniform(0.50, 0.75, size=n_p5), 4)
    p5_velocity = np.round(np.random.uniform(0.5, 2.0, size=n_p5), 2)
    p5_geo = np.round(np.random.uniform(5.0, 120.0, size=n_p5), 2)
    p5_age = np.round(np.random.uniform(60.0, 1200.0, size=n_p5), 0)
    p5_ts = np.sort(np.random.uniform(0, 86400 * 7, size=n_p5))
    p5_hours = (p5_ts % 86400) / 3600.0
    
    df_p5 = pd.DataFrame({
        "transaction_id": [f"TX_FRD_DRIP_{i:06d}" for i in range(n_p5)],
        "timestamp_sec": p5_ts,
        "amount": p5_amounts,
        "mcc": p5_mccs,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.88) for m in p5_mccs]),
        "is_decline": p5_declines,
        "hour_of_day_sin": np.round(np.sin(2 * np.pi * p5_hours / 24.0), 4),
        "hour_of_day_cos": np.round(np.cos(2 * np.pi * p5_hours / 24.0), 4),
        "card_type": np.random.choice(["visa", "mastercard"], size=n_p5, p=[0.55, 0.45]),
        "device_risk_score": p5_risk,
        "velocity": p5_velocity,
        "geo_distance_km": p5_geo,
        "card_age_days": p5_age,
        "failed_attempts_24h": 0,
        "user_agent_category": "residential_proxy_bot",
        "is_fraud": 1,
        "attack_vector": "slow_drip",
        "fraud_subtype": "slow_drip"
    })
    fraud_frames.append(df_p5)
    
    df_fraud_all = pd.concat(fraud_frames, ignore_index=True)
    
    # ── 4. Combine and Sort by Timestamp ──
    df = pd.concat([df_legit, df_hard_neg, df_fraud_all], ignore_index=True)
    df = df.sort_values("timestamp_sec").reset_index(drop=True)
    return df


if __name__ == "__main__":
    df_test = generate_tabular_card_testing(num_samples=1000)
    print(f"Generated {len(df_test)} transactions with {len(TABULAR_FEATURE_COLS)} features.")
    print("Fraud sub-type distribution:")
    print(df_test["fraud_subtype"].value_counts())
    print(df_test[TABULAR_FEATURE_COLS + ['is_fraud', 'fraud_subtype']].head())
