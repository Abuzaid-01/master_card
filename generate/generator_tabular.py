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

v3.0 — Realistic Feature Overlap & Label Noise Edition
- Fraud features intentionally overlap with legitimate distributions (mirroring real-world
  sophisticated attackers who use residential proxies, clean devices, normal MCCs).
- 3.5% fraud ratio (real-world enterprise baseline).
- ~3% label noise to simulate undetected fraud and reversed chargebacks.
- Temporal concept drift: test-window fraud patterns shift subtly from training data.
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
    fraud_ratio: float = 0.08,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generates realistic synthetic card transaction records with authentic payment network noise.

    v3.0 design philosophy:
    - Fraud features DELIBERATELY overlap with legitimate distributions.
    - No single feature should separate classes (target: single-feature ROC-AUC < 0.72).
    - Combined model target: ROC-AUC 0.94-0.97 (matching IEEE-CIS Kaggle benchmark).
    - Label noise simulates real-world annotation uncertainty.
    """
    np.random.seed(random_seed)

    num_fraud = int(num_samples * fraud_ratio)
    num_legit = num_samples - num_fraud

    # ══════════════════════════════════════════════════════════════════════════
    # 1. LEGITIMATE TRANSACTIONS
    # ══════════════════════════════════════════════════════════════════════════

    # ── 1a. Standard Legitimate Transactions (60% of legit) ──
    num_standard_legit = int(num_legit * 0.60)

    # Tier 1: Everyday micro/daily ($2.50 to $65.00)
    n_everyday = int(num_standard_legit * 0.40)
    amt_everyday = np.round(np.random.lognormal(mean=2.8, sigma=0.7, size=n_everyday), 2)
    amt_everyday = np.clip(amt_everyday, 1.50, 150.0)
    mcc_everyday = np.random.choice([5411, 5812, 5912, 4121, 5541, 7523], size=n_everyday,
                                     p=[0.30, 0.25, 0.15, 0.12, 0.10, 0.08])
    risk_everyday = np.round(np.random.beta(1.8, 12.0, size=n_everyday), 4)
    vel_everyday = np.round(np.random.lognormal(mean=0.3, sigma=0.35, size=n_everyday), 2)
    vel_everyday = np.clip(vel_everyday, 0.3, 6.0)
    geo_everyday = np.round(np.abs(np.random.normal(15.0, 18.0, size=n_everyday)), 2)
    geo_everyday = np.clip(geo_everyday, 0.2, 120.0)

    # Tier 2: Standard retail & dining ($50.00 to $500.00)
    n_retail = int(num_standard_legit * 0.35)
    amt_retail = np.round(np.random.lognormal(mean=4.8, sigma=0.6, size=n_retail), 2)
    amt_retail = np.clip(amt_retail, 30.0, 1200.0)
    mcc_retail = np.random.choice([5311, 5812, 5999, 5541, 4121, 5912], size=n_retail,
                                   p=[0.25, 0.20, 0.15, 0.15, 0.15, 0.10])
    risk_retail = np.round(np.random.beta(1.5, 10.0, size=n_retail), 4)
    vel_retail = np.round(np.random.lognormal(mean=0.2, sigma=0.3, size=n_retail), 2)
    vel_retail = np.clip(vel_retail, 0.3, 5.0)
    geo_retail = np.round(np.abs(np.random.normal(20.0, 30.0, size=n_retail)), 2)
    geo_retail = np.clip(geo_retail, 0.5, 250.0)

    # Tier 3: High-value major commerce ($300.00 to $5,000.00)
    n_highval = num_standard_legit - n_everyday - n_retail
    amt_highval = np.round(np.random.lognormal(mean=6.2, sigma=0.55, size=n_highval), 2)
    amt_highval = np.clip(amt_highval, 200.0, 8000.0)
    mcc_highval = np.random.choice([5311, 5999, 5816, 5812, 4121, 7399], size=n_highval,
                                    p=[0.30, 0.20, 0.15, 0.15, 0.10, 0.10])
    risk_highval = np.round(np.random.beta(1.3, 9.0, size=n_highval), 4)
    vel_highval = np.round(np.random.lognormal(mean=0.1, sigma=0.25, size=n_highval), 2)
    vel_highval = np.clip(vel_highval, 0.3, 4.0)
    geo_highval = np.round(np.abs(np.random.normal(25.0, 40.0, size=n_highval)), 2)
    geo_highval = np.clip(geo_highval, 0.5, 350.0)

    amt_std = np.concatenate([amt_everyday, amt_retail, amt_highval])
    mcc_std = np.concatenate([mcc_everyday, mcc_retail, mcc_highval])
    risk_std = np.concatenate([risk_everyday, risk_retail, risk_highval])
    vel_std = np.concatenate([vel_everyday, vel_retail, vel_highval])
    geo_std = np.concatenate([geo_everyday, geo_retail, geo_highval])

    ts_std = np.sort(np.random.uniform(0, 86400 * 14, size=num_standard_legit))
    hours_std = (ts_std % 86400) / 3600.0

    df_legit_std = pd.DataFrame({
        "transaction_id": [f"TX_LEG_STD_{i:06d}" for i in range(num_standard_legit)],
        "timestamp_sec": ts_std,
        "amount": amt_std,
        "mcc": mcc_std,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.20) for m in mcc_std]),
        "is_decline": np.random.choice([0, 1], size=num_standard_legit, p=[0.96, 0.04]),
        "hour_of_day_sin": np.round(np.sin(2 * np.pi * hours_std / 24.0), 4),
        "hour_of_day_cos": np.round(np.cos(2 * np.pi * hours_std / 24.0), 4),
        "card_type": np.random.choice(["visa", "mastercard", "amex"], size=num_standard_legit, p=[0.5, 0.4, 0.1]),
        "device_risk_score": risk_std,
        "velocity": vel_std,
        "geo_distance_km": geo_std,
        "card_age_days": np.round(np.random.lognormal(mean=6.0, sigma=0.9, size=num_standard_legit), 0),
        "failed_attempts_24h": np.random.choice([0, 1, 2], size=num_standard_legit, p=[0.90, 0.08, 0.02]),
        "user_agent_category": "standard_browser",
        "is_fraud": 0,
        "attack_vector": "legitimate",
        "fraud_subtype": "legitimate_standard"
    })
    # Clip card_age_days to realistic range
    df_legit_std["card_age_days"] = df_legit_std["card_age_days"].clip(15, 3650)

    # ── 1b. Hard-Negative Legitimate Edge Cases (40% of legit) ──
    num_hard_neg = num_legit - num_standard_legit
    n_travelers = int(num_hard_neg * 0.20)
    n_transit_rush = int(num_hard_neg * 0.20)
    n_gaming_digital = int(num_hard_neg * 0.20)
    n_cvv_typos = int(num_hard_neg * 0.15)
    n_new_card_legit = int(num_hard_neg * 0.15)
    n_high_risk_merchant_legit = num_hard_neg - n_travelers - n_transit_rush - n_gaming_digital - n_cvv_typos - n_new_card_legit

    # Edge Case A: International Business/Vacation Travelers
    t_amt = np.round(np.random.lognormal(mean=5.0, sigma=0.7, size=n_travelers), 2)
    t_amt = np.clip(t_amt, 20.0, 4000.0)
    t_vel = np.round(np.random.lognormal(mean=0.2, sigma=0.3, size=n_travelers), 2)
    t_vel = np.clip(t_vel, 0.3, 4.0)
    t_risk = np.round(np.random.beta(2.5, 6.0, size=n_travelers), 4)
    t_geo = np.round(np.random.uniform(800.0, 9000.0, size=n_travelers), 2)
    t_mcc = np.random.choice([5311, 4121, 5812, 5999, 5411, 5541], size=n_travelers,
                              p=[0.25, 0.20, 0.20, 0.15, 0.10, 0.10])
    t_declines = np.random.choice([0, 1], size=n_travelers, p=[0.88, 0.12])

    # Edge Case B: Transit Rush / Subway / Food Festival
    r_amt = np.round(np.random.uniform(1.50, 30.0, size=n_transit_rush), 2)
    r_vel = np.round(np.random.uniform(4.0, 12.0, size=n_transit_rush), 2)
    r_risk = np.round(np.random.beta(1.5, 10.0, size=n_transit_rush), 4)
    r_geo = np.round(np.abs(np.random.normal(5.0, 8.0, size=n_transit_rush)), 2)
    r_geo = np.clip(r_geo, 0.2, 40.0)
    r_mcc = np.random.choice([4121, 5411, 5812, 7523], size=n_transit_rush,
                              p=[0.35, 0.25, 0.25, 0.15])
    r_declines = np.random.choice([0, 1], size=n_transit_rush, p=[0.95, 0.05])

    # Edge Case C: Legitimate Digital Goods & Gaming
    g_amt = np.round(np.random.lognormal(mean=3.5, sigma=0.8, size=n_gaming_digital), 2)
    g_amt = np.clip(g_amt, 5.0, 500.0)
    g_vel = np.round(np.random.lognormal(mean=0.5, sigma=0.4, size=n_gaming_digital), 2)
    g_vel = np.clip(g_vel, 0.5, 6.0)
    g_risk = np.round(np.random.beta(2.0, 5.0, size=n_gaming_digital), 4)
    g_geo = np.round(np.abs(np.random.normal(12.0, 15.0, size=n_gaming_digital)), 2)
    g_geo = np.clip(g_geo, 0.5, 80.0)
    g_mcc = np.random.choice([5816, 7399, 5968, 5969], size=n_gaming_digital,
                              p=[0.40, 0.30, 0.20, 0.10])
    g_declines = np.random.choice([0, 1], size=n_gaming_digital, p=[0.92, 0.08])

    # Edge Case D: CVV Typo / Multi-Attempt Retries
    c_amt = np.round(np.random.lognormal(mean=4.2, sigma=0.6, size=n_cvv_typos), 2)
    c_amt = np.clip(c_amt, 15.0, 800.0)
    c_vel = np.round(np.random.lognormal(mean=0.5, sigma=0.3, size=n_cvv_typos), 2)
    c_vel = np.clip(c_vel, 0.5, 5.0)
    c_risk = np.round(np.random.beta(1.5, 7.0, size=n_cvv_typos), 4)
    c_geo = np.round(np.abs(np.random.normal(18.0, 20.0, size=n_cvv_typos)), 2)
    c_geo = np.clip(c_geo, 0.5, 120.0)
    c_mcc = np.random.choice([5411, 5311, 5812, 5912, 5999], size=n_cvv_typos,
                              p=[0.30, 0.25, 0.20, 0.15, 0.10])
    c_declines = np.random.choice([0, 1], size=n_cvv_typos, p=[0.30, 0.70])
    c_failed = np.random.choice([2, 3, 4], size=n_cvv_typos, p=[0.50, 0.35, 0.15])

    # Edge Case E: Newly Issued Cards
    nc_amt = np.round(np.random.lognormal(mean=3.8, sigma=0.7, size=n_new_card_legit), 2)
    nc_amt = np.clip(nc_amt, 5.0, 600.0)
    nc_vel = np.round(np.random.lognormal(mean=0.6, sigma=0.4, size=n_new_card_legit), 2)
    nc_vel = np.clip(nc_vel, 0.5, 6.0)
    nc_risk = np.round(np.random.beta(2.0, 8.0, size=n_new_card_legit), 4)
    nc_geo = np.round(np.abs(np.random.normal(10.0, 12.0, size=n_new_card_legit)), 2)
    nc_geo = np.clip(nc_geo, 0.2, 60.0)
    nc_mcc = np.random.choice([5411, 5311, 5812, 5912, 5541], size=n_new_card_legit,
                               p=[0.30, 0.25, 0.20, 0.15, 0.10])
    nc_declines = np.random.choice([0, 1], size=n_new_card_legit, p=[0.85, 0.15])
    nc_age = np.random.choice(range(1, 30), size=n_new_card_legit)

    # Edge Case F: High-Risk Merchant Legit Purchases
    hr_amt = np.round(np.random.lognormal(mean=4.5, sigma=0.7, size=n_high_risk_merchant_legit), 2)
    hr_amt = np.clip(hr_amt, 10.0, 1500.0)
    hr_vel = np.round(np.random.lognormal(mean=0.3, sigma=0.3, size=n_high_risk_merchant_legit), 2)
    hr_vel = np.clip(hr_vel, 0.3, 4.0)
    hr_risk = np.round(np.random.beta(1.8, 9.0, size=n_high_risk_merchant_legit), 4)
    hr_geo = np.round(np.abs(np.random.normal(15.0, 20.0, size=n_high_risk_merchant_legit)), 2)
    hr_geo = np.clip(hr_geo, 0.5, 120.0)
    hr_mcc = np.random.choice([5999, 7399, 5816, 5968, 5969], size=n_high_risk_merchant_legit,
                               p=[0.30, 0.25, 0.20, 0.15, 0.10])
    hr_declines = np.random.choice([0, 1], size=n_high_risk_merchant_legit, p=[0.93, 0.07])

    hn_amt = np.concatenate([t_amt, r_amt, g_amt, c_amt, nc_amt, hr_amt])
    hn_vel = np.concatenate([t_vel, r_vel, g_vel, c_vel, nc_vel, hr_vel])
    hn_risk = np.concatenate([t_risk, r_risk, g_risk, c_risk, nc_risk, hr_risk])
    hn_geo = np.concatenate([t_geo, r_geo, g_geo, c_geo, nc_geo, hr_geo])
    hn_mcc = np.concatenate([t_mcc, r_mcc, g_mcc, c_mcc, nc_mcc, hr_mcc])
    hn_dec = np.concatenate([t_declines, r_declines, g_declines, c_declines, nc_declines, hr_declines])
    hn_fail = np.concatenate([
        np.random.choice([0, 1], size=n_travelers, p=[0.88, 0.12]),
        np.random.choice([0, 1], size=n_transit_rush, p=[0.94, 0.06]),
        np.random.choice([0, 1, 2], size=n_gaming_digital, p=[0.85, 0.10, 0.05]),
        c_failed,
        np.random.choice([0, 1, 2], size=n_new_card_legit, p=[0.80, 0.15, 0.05]),
        np.random.choice([0, 1], size=n_high_risk_merchant_legit, p=[0.90, 0.10]),
    ])
    hn_card_age = np.concatenate([
        np.round(np.random.lognormal(mean=5.8, sigma=0.9, size=n_travelers), 0),
        np.round(np.random.lognormal(mean=6.0, sigma=0.8, size=n_transit_rush), 0),
        np.round(np.random.lognormal(mean=5.5, sigma=1.0, size=n_gaming_digital), 0),
        np.round(np.random.lognormal(mean=5.8, sigma=0.9, size=n_cvv_typos), 0),
        nc_age.astype(float),
        np.round(np.random.lognormal(mean=5.8, sigma=0.9, size=n_high_risk_merchant_legit), 0),
    ])
    hn_card_age = np.clip(hn_card_age, 1, 3650)

    hn_ts = np.sort(np.random.uniform(0, 86400 * 14, size=num_hard_neg))
    hn_hours = (hn_ts % 86400) / 3600.0

    df_hard_neg = pd.DataFrame({
        "transaction_id": [f"TX_LEG_HN_{i:06d}" for i in range(num_hard_neg)],
        "timestamp_sec": hn_ts,
        "amount": hn_amt,
        "mcc": hn_mcc,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.30) for m in hn_mcc]),
        "is_decline": hn_dec,
        "hour_of_day_sin": np.round(np.sin(2 * np.pi * hn_hours / 24.0), 4),
        "hour_of_day_cos": np.round(np.cos(2 * np.pi * hn_hours / 24.0), 4),
        "card_type": np.random.choice(["visa", "mastercard", "amex"], size=num_hard_neg, p=[0.5, 0.4, 0.1]),
        "device_risk_score": hn_risk,
        "velocity": hn_vel,
        "geo_distance_km": hn_geo,
        "card_age_days": hn_card_age,
        "failed_attempts_24h": hn_fail,
        "user_agent_category": "standard_browser",
        "is_fraud": 0,
        "attack_vector": "legitimate_hard_negative",
        "fraud_subtype": "legitimate_hard_negative"
    })

    # ══════════════════════════════════════════════════════════════════════════
    # 2. FRAUD TRANSACTIONS — Realistic Overlapping Distributions
    # ══════════════════════════════════════════════════════════════════════════
    # Key design principle: Each fraud subtype has 1-2 "signal" features that
    # are SLIGHTLY elevated above legit, but NO feature alone is a giveaway.
    # The model must learn COMBINATIONS of weak signals.

    n_p1 = int(num_fraud * 0.22)  # Card Testing Burst
    n_p2 = int(num_fraud * 0.22)  # Account Takeover (ATO)
    n_p3 = int(num_fraud * 0.18)  # High-Velocity Bot Swarm
    n_p4 = int(num_fraud * 0.18)  # Card-Not-Present (CNP)
    n_p5 = num_fraud - (n_p1 + n_p2 + n_p3 + n_p4)  # Slow Drip & Stealth

    fraud_frames = []

    # ── Sub-Type 1: Card Testing Burst ──
    # Signal: Slightly elevated velocity (3-8, overlaps transit rush) + more declines + young card
    # Camouflage: Uses MIX of normal and risky MCCs, device risk overlaps with legit gamers
    p1_micro = int(n_p1 * 0.55)
    p1_drain = n_p1 - p1_micro
    p1_amounts = np.concatenate([
        np.round(np.random.lognormal(mean=1.5, sigma=0.6, size=p1_micro), 2),  # $2-$15 probes
        np.round(np.random.lognormal(mean=6.5, sigma=0.5, size=p1_drain), 2),   # Drain attempts
    ])
    p1_amounts = np.clip(p1_amounts, 0.50, 5000.0)
    np.random.shuffle(p1_amounts)
    # 50% normal MCCs to blend in
    p1_mccs = np.random.choice([5999, 7399, 5816, 5411, 5812, 5541, 7523], size=n_p1,
                                p=[0.15, 0.10, 0.10, 0.20, 0.20, 0.15, 0.10])
    p1_declines = np.random.choice([0, 1], size=n_p1, p=[0.35, 0.65])
    # Device risk: 0.20-0.65 — overlaps with legit travelers/gamers but slightly elevated
    p1_risk = np.round(np.random.beta(3.5, 4.0, size=n_p1), 4)
    p1_risk = np.clip(p1_risk, 0.08, 0.70)
    # Velocity: 4-14 — overlaps with transit rush (4-12) but slightly higher
    p1_velocity = np.round(np.random.lognormal(mean=1.8, sigma=0.4, size=n_p1), 2)
    p1_velocity = np.clip(p1_velocity, 3.0, 20.0)
    # Geo: LOCAL — residential proxy is near victim's home moderate distance
    p1_geo = np.round(np.abs(np.random.normal(40.0, 60.0, size=n_p1)), 2)
    p1_geo = np.clip(p1_geo, 0.5, 500.0)
    p1_age = np.round(np.random.lognormal(mean=3.8, sigma=1.0, size=n_p1), 0)
    p1_age = np.clip(p1_age, 3, 1200)
    p1_failed = np.random.choice([0, 1, 2, 3, 4, 5], size=n_p1, p=[0.10, 0.20, 0.25, 0.25, 0.15, 0.05])
    p1_ts = np.sort(np.random.uniform(0, 86400 * 14, size=n_p1))
    p1_hours = (p1_ts % 86400) / 3600.0

    df_p1 = pd.DataFrame({
        "transaction_id": [f"TX_FRD_BURST_{i:06d}" for i in range(n_p1)],
        "timestamp_sec": p1_ts,
        "amount": p1_amounts,
        "mcc": p1_mccs,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.30) for m in p1_mccs]),
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

    # ── Sub-Type 2: Account Takeover (ATO) ──
    # Signal: Moderate geo shift (100-2000km) + slightly elevated device risk + unusual hour
    # Camouflage: Normal velocity, normal amounts, normal MCCs
    p2_amounts = np.round(np.random.lognormal(mean=5.2, sigma=0.7, size=n_p2), 2)
    p2_amounts = np.clip(p2_amounts, 30.0, 4000.0)
    p2_mccs = np.random.choice([5311, 5812, 5411, 5999, 5816, 4121], size=n_p2,
                                p=[0.25, 0.20, 0.15, 0.15, 0.15, 0.10])
    p2_declines = np.random.choice([0, 1], size=n_p2, p=[0.82, 0.18])
    p2_risk = np.round(np.random.beta(3.0, 4.5, size=n_p2), 4)
    p2_risk = np.clip(p2_risk, 0.12, 0.65)
    p2_velocity = np.round(np.random.lognormal(mean=0.4, sigma=0.35, size=n_p2), 2)
    p2_velocity = np.clip(p2_velocity, 0.5, 5.0)
    # Geo: 150-4000km — significant but overlaps with legitimate travelers
    p2_geo = np.round(np.random.lognormal(mean=6.2, sigma=0.7, size=n_p2), 2)
    p2_geo = np.clip(p2_geo, 80.0, 6000.0)
    p2_age = np.round(np.random.lognormal(mean=5.8, sigma=0.9, size=n_p2), 0)
    p2_age = np.clip(p2_age, 30, 2500)
    p2_failed = np.random.choice([0, 1, 2], size=n_p2, p=[0.60, 0.25, 0.15])
    p2_ts = np.sort(np.random.uniform(0, 86400 * 14, size=n_p2))
    p2_hours = (p2_ts % 86400) / 3600.0

    df_p2 = pd.DataFrame({
        "transaction_id": [f"TX_FRD_ATO_{i:06d}" for i in range(n_p2)],
        "timestamp_sec": p2_ts,
        "amount": p2_amounts,
        "mcc": p2_mccs,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.30) for m in p2_mccs]),
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

    # ── Sub-Type 3: High-Velocity Bot Swarm ──
    # Signal: Elevated velocity (5-18, overlaps transit) + moderate amounts + structured timing
    # Camouflage: Clean device (residential proxy), local geo, normal MCCs
    p3_amounts = np.round(np.random.lognormal(mean=4.8, sigma=0.6, size=n_p3), 2)
    p3_amounts = np.clip(p3_amounts, 20.0, 3000.0)
    p3_mccs = np.random.choice([5311, 5812, 5411, 5999, 5541, 4121], size=n_p3,
                                p=[0.25, 0.20, 0.15, 0.15, 0.15, 0.10])
    p3_declines = np.random.choice([0, 1], size=n_p3, p=[0.78, 0.22])
    p3_risk = np.round(np.random.beta(1.8, 8.0, size=n_p3), 4)
    p3_risk = np.clip(p3_risk, 0.03, 0.35)
    # Velocity: NORMAL — sophisticated ATOs don't rush (4-12) but slightly higher
    p3_velocity = np.round(np.random.lognormal(mean=2.0, sigma=0.4, size=n_p3), 2)
    p3_velocity = np.clip(p3_velocity, 4.0, 28.0)
    p3_geo = np.round(np.abs(np.random.normal(20.0, 25.0, size=n_p3)), 2)
    p3_geo = np.clip(p3_geo, 0.5, 150.0)
    p3_age = np.round(np.random.lognormal(mean=5.5, sigma=0.9, size=n_p3), 0)
    p3_age = np.clip(p3_age, 15, 2000)
    p3_failed = np.random.choice([0, 1, 2], size=n_p3, p=[0.55, 0.30, 0.15])
    p3_ts = np.sort(np.random.uniform(0, 86400 * 14, size=n_p3))
    p3_hours = (p3_ts % 86400) / 3600.0

    df_p3 = pd.DataFrame({
        "transaction_id": [f"TX_FRD_BOT_{i:06d}" for i in range(n_p3)],
        "timestamp_sec": p3_ts,
        "amount": p3_amounts,
        "mcc": p3_mccs,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.25) for m in p3_mccs]),
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

    # ── Sub-Type 4: Card-Not-Present (CNP) ──
    # Signal: Slightly elevated device risk + high-risk MCC + moderate geo
    # Camouflage: Normal velocity, amounts within legit high-value range
    p4_amounts = np.round(np.random.lognormal(mean=5.3, sigma=0.65, size=n_p4), 2)
    p4_amounts = np.clip(p4_amounts, 40.0, 3500.0)
    p4_mccs = np.random.choice([5816, 7399, 5999, 5311, 5812, 5969], size=n_p4,
                                p=[0.20, 0.15, 0.15, 0.20, 0.15, 0.15])
    p4_declines = np.random.choice([0, 1], size=n_p4, p=[0.65, 0.35])
    p4_risk = np.round(np.random.beta(3.2, 4.0, size=n_p4), 4)
    p4_risk = np.clip(p4_risk, 0.15, 0.70)
    p4_velocity = np.round(np.random.lognormal(mean=0.5, sigma=0.4, size=n_p4), 2)
    p4_velocity = np.clip(p4_velocity, 0.5, 6.0)
    p4_geo = np.round(np.random.lognormal(mean=4.5, sigma=1.0, size=n_p4), 2)
    p4_geo = np.clip(p4_geo, 5.0, 2000.0)
    p4_age = np.round(np.random.lognormal(mean=4.5, sigma=1.0, size=n_p4), 0)
    p4_age = np.clip(p4_age, 5, 1500)
    p4_failed = np.random.choice([0, 1, 2, 3], size=n_p4, p=[0.35, 0.30, 0.25, 0.10])
    p4_ts = np.sort(np.random.uniform(0, 86400 * 14, size=n_p4))
    p4_hours = (p4_ts % 86400) / 3600.0

    df_p4 = pd.DataFrame({
        "transaction_id": [f"TX_FRD_CNP_{i:06d}" for i in range(n_p4)],
        "timestamp_sec": p4_ts,
        "amount": p4_amounts,
        "mcc": p4_mccs,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.40) for m in p4_mccs]),
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

    # ── Sub-Type 5: Slow Drip Siphon & Stealth Fraud ──
    # Signal: Nearly invisible — small recurring charges, completely clean profile
    n_drip_std = int(n_p5 * 0.45)
    n_stealth_loc = int(n_p5 * 0.30)
    n_friendly = n_p5 - n_drip_std - n_stealth_loc

    # Standard Slow Drip
    d_amt = np.round(np.random.lognormal(mean=3.0, sigma=0.5, size=n_drip_std), 2)
    d_amt = np.clip(d_amt, 8.0, 120.0)
    d_mccs = np.random.choice([5968, 5816, 7399, 5969, 5812], size=n_drip_std,
                               p=[0.25, 0.20, 0.15, 0.15, 0.25])
    d_risk = np.round(np.random.beta(1.5, 10.0, size=n_drip_std), 4)
    d_vel = np.round(np.random.lognormal(mean=0.1, sigma=0.25, size=n_drip_std), 2)
    d_vel = np.clip(d_vel, 0.3, 3.0)
    d_geo = np.round(np.abs(np.random.normal(10.0, 12.0, size=n_drip_std)), 2)
    d_geo = np.clip(d_geo, 0.5, 60.0)

    # Stealth Local Residential Proxy ATO
    s_amt = np.round(np.random.lognormal(mean=4.5, sigma=0.5, size=n_stealth_loc), 2)
    s_amt = np.clip(s_amt, 40.0, 500.0)
    s_mccs = np.random.choice([5311, 5812, 5411, 5912, 5541], size=n_stealth_loc,
                               p=[0.25, 0.25, 0.20, 0.15, 0.15])
    s_risk = np.round(np.random.beta(1.3, 10.0, size=n_stealth_loc), 4)
    s_vel = np.round(np.random.lognormal(mean=0.2, sigma=0.25, size=n_stealth_loc), 2)
    s_vel = np.clip(s_vel, 0.3, 3.0)
    s_geo = np.round(np.abs(np.random.normal(8.0, 10.0, size=n_stealth_loc)), 2)
    s_geo = np.clip(s_geo, 0.2, 40.0)

    # Friendly Fraud
    f_amt = np.round(np.random.lognormal(mean=5.8, sigma=0.5, size=n_friendly), 2)
    f_amt = np.clip(f_amt, 150.0, 2500.0)
    f_mccs = np.random.choice([5311, 5999, 5816, 5812], size=n_friendly,
                               p=[0.35, 0.25, 0.20, 0.20])
    f_risk = np.round(np.random.beta(1.2, 12.0, size=n_friendly), 4)
    f_vel = np.round(np.random.lognormal(mean=0.0, sigma=0.2, size=n_friendly), 2)
    f_vel = np.clip(f_vel, 0.3, 2.5)
    f_geo = np.round(np.abs(np.random.normal(5.0, 6.0, size=n_friendly)), 2)
    f_geo = np.clip(f_geo, 0.2, 25.0)

    p5_amounts = np.concatenate([d_amt, s_amt, f_amt])
    p5_mccs = np.concatenate([d_mccs, s_mccs, f_mccs])
    p5_risk = np.concatenate([d_risk, s_risk, f_risk])
    p5_vel = np.concatenate([d_vel, s_vel, f_vel])
    p5_geo = np.concatenate([d_geo, s_geo, f_geo])

    p5_ts = np.sort(np.random.uniform(0, 86400 * 14, size=n_p5))
    p5_hours = (p5_ts % 86400) / 3600.0

    df_p5 = pd.DataFrame({
        "transaction_id": [f"TX_FRD_DRIP_{i:06d}" for i in range(n_p5)],
        "timestamp_sec": p5_ts,
        "amount": p5_amounts,
        "mcc": p5_mccs,
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.30) for m in p5_mccs]),
        "is_decline": np.random.choice([0, 1], size=n_p5, p=[0.92, 0.08]),
        "hour_of_day_sin": np.round(np.sin(2 * np.pi * p5_hours / 24.0), 4),
        "hour_of_day_cos": np.round(np.cos(2 * np.pi * p5_hours / 24.0), 4),
        "card_type": np.random.choice(["visa", "mastercard"], size=n_p5, p=[0.55, 0.45]),
        "device_risk_score": p5_risk,
        "velocity": p5_vel,
        "geo_distance_km": p5_geo,
        "card_age_days": np.round(np.random.lognormal(mean=5.5, sigma=1.0, size=n_p5), 0).clip(10, 2500),
        "failed_attempts_24h": np.random.choice([0, 1], size=n_p5, p=[0.88, 0.12]),
        "user_agent_category": "residential_proxy_bot",
        "is_fraud": 1,
        "attack_vector": "slow_drip",
        "fraud_subtype": "slow_drip_stealth"
    })
    fraud_frames.append(df_p5)

    df_fraud_all = pd.concat(fraud_frames, ignore_index=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 3. COMBINE, APPLY NOISE, AND ADD LABEL UNCERTAINTY
    # ══════════════════════════════════════════════════════════════════════════
    df = pd.concat([df_legit_std, df_hard_neg, df_fraud_all], ignore_index=True)

    # ── 3a. Realistic telemetry sensor jitter ──
    jitter_geo = np.random.normal(0, 8.0, size=len(df))
    jitter_risk = np.random.normal(0, 0.03, size=len(df))
    jitter_vel = np.random.normal(0, 0.2, size=len(df))
    jitter_amt = np.random.normal(0, 0.05, size=len(df)) * df["amount"].values

    df["geo_distance_km"] = np.round(np.clip(df["geo_distance_km"] + jitter_geo, 0.1, 10000.0), 2)
    df["device_risk_score"] = np.round(np.clip(df["device_risk_score"] + jitter_risk, 0.01, 0.99), 4)
    df["velocity"] = np.round(np.clip(df["velocity"] + jitter_vel, 0.1, 40.0), 2)
    df["amount"] = np.round(np.clip(df["amount"] + jitter_amt, 0.01, 15000.0), 2)

    # ── 3b. Label noise — simulates real-world annotation uncertainty ──
    # Flip ~2.0% of legit labels to fraud (undetected fraud in training data)
    legit_mask = df["is_fraud"] == 0
    n_flip_to_fraud = int(legit_mask.sum() * 0.020)
    flip_idx = np.random.choice(df.index[legit_mask], size=n_flip_to_fraud, replace=False)
    df.loc[flip_idx, "is_fraud"] = 1
    df.loc[flip_idx, "fraud_subtype"] = "label_noise_undetected"

    # Flip ~1.5% of fraud labels to legit (reversed chargebacks / dispute resolution)
    fraud_mask = df["is_fraud"] == 1
    n_flip_to_legit = int(fraud_mask.sum() * 0.015)
    if n_flip_to_legit > 0:
        flip_idx_2 = np.random.choice(df.index[fraud_mask], size=n_flip_to_legit, replace=False)
        df.loc[flip_idx_2, "is_fraud"] = 0
        df.loc[flip_idx_2, "fraud_subtype"] = "label_noise_reversed"

    df = df.sort_values("timestamp_sec").reset_index(drop=True)
    return df


if __name__ == "__main__":
    df_test = generate_tabular_card_testing(num_samples=1000)
    print(f"Generated {len(df_test)} transactions with {len(TABULAR_FEATURE_COLS)} features.")
    print(f"Fraud ratio: {df_test['is_fraud'].mean()*100:.1f}%")
    print("Fraud sub-type distribution:")
    print(df_test["fraud_subtype"].value_counts())
    print(df_test[TABULAR_FEATURE_COLS + ['is_fraud', 'fraud_subtype']].head())
