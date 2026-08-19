"""
Test script to refine tabular generator distributions and verify realistic classification boundaries.
Tests independent signal activations:
- Legitimate large purchase ($2,110) at normal human velocity (1.0 tx/min) -> SAFE
- Automated script attack ($2,110) at bot velocity (19.5 tx/min) -> FRAUD
- Account takeover ($2,110) from unrecognized device (92%) -> FRAUD
- Card testing burst ($1.50 micro-swipes) -> FRAUD
"""

import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.ensemble import IsolationForest

MCC_RISK_MAP = {
    5999: 0.85, 7399: 0.90, 5816: 0.88, 5968: 0.80, 5969: 0.82,
    5311: 0.40, 4121: 0.35, 7523: 0.30,
    5411: 0.10, 5812: 0.15, 5912: 0.12, 5541: 0.18,
}

TABULAR_FEATURE_COLS = [
    "amount", "velocity", "device_risk_score", "is_decline",
    "hour_of_day_sin", "hour_of_day_cos", "mcc_risk_weight",
    "geo_distance_km", "card_age_days", "failed_attempts_24h"
]

def build_realistic_dataset(num_samples=50000, fraud_ratio=0.15, random_seed=42):
    np.random.seed(random_seed)
    num_fraud = int(num_samples * fraud_ratio)
    num_legit = num_samples - num_fraud
    
    num_std_legit = int(num_legit * 0.75)
    
    # Tier 1: Everyday micro/daily (35% of std legit)
    n_everyday = int(num_std_legit * 0.35)
    amt_everyday = np.round(np.random.uniform(2.50, 65.0, size=n_everyday), 2)
    mcc_everyday = np.random.choice([5411, 5812, 5912, 4121, 5541, 7523], size=n_everyday)
    risk_everyday = np.round(np.random.beta(1.2, 8.0, size=n_everyday), 4)
    vel_everyday = np.round(np.random.uniform(1.0, 3.0, size=n_everyday), 2)
    geo_everyday = np.round(np.random.uniform(0.5, 35.0, size=n_everyday), 2)
    
    # Tier 2: Standard retail & dining (35% of std legit)
    n_retail = int(num_std_legit * 0.35)
    amt_retail = np.round(np.random.uniform(65.0, 450.0, size=n_retail), 2)
    mcc_retail = np.random.choice([5311, 5812, 5999, 5541, 4121], size=n_retail)
    risk_retail = np.round(np.random.beta(1.2, 8.0, size=n_retail), 4)
    vel_retail = np.round(np.random.uniform(1.0, 3.0, size=n_retail), 2)
    geo_retail = np.round(np.random.uniform(1.0, 65.0, size=n_retail), 2)
    
    # Tier 3: Major high-value legitimate purchases (30% of std legit) e.g. Electronics, Laptops, Flights, Rent: $450 - $4,200
    n_highval = num_std_legit - n_everyday - n_retail
    amt_highval = np.round(np.random.uniform(450.0, 4200.0, size=n_highval), 2)
    mcc_highval = np.random.choice([5311, 5999, 5816, 5812, 4121], size=n_highval)
    risk_highval = np.round(np.random.beta(1.0, 10.0, size=n_highval), 4) # Very clean device 0.01 - 0.15
    vel_highval = np.round(np.random.uniform(0.5, 2.0, size=n_highval), 2) # Low normal velocity
    geo_highval = np.round(np.random.uniform(1.0, 40.0, size=n_highval), 2) # Known domestic location
    
    amt_legit = np.concatenate([amt_everyday, amt_retail, amt_highval])
    mcc_legit = np.concatenate([mcc_everyday, mcc_retail, mcc_highval])
    risk_legit = np.concatenate([risk_everyday, risk_retail, risk_highval])
    vel_legit = np.concatenate([vel_everyday, vel_retail, vel_highval])
    geo_legit = np.concatenate([geo_everyday, geo_retail, geo_highval])
    
    ts_legit = np.sort(np.random.uniform(0, 86400 * 7, size=num_std_legit))
    hours_legit = (ts_legit % 86400) / 3600.0
    
    df_legit = pd.DataFrame({
        "amount": amt_legit,
        "velocity": vel_legit,
        "device_risk_score": risk_legit,
        "is_decline": np.random.choice([0, 1], size=num_std_legit, p=[0.98, 0.02]),
        "hour_of_day_sin": np.round(np.sin(2 * np.pi * hours_legit / 24.0), 4),
        "hour_of_day_cos": np.round(np.cos(2 * np.pi * hours_legit / 24.0), 4),
        "mcc_risk_weight": np.array([MCC_RISK_MAP.get(m, 0.20) for m in mcc_legit]),
        "geo_distance_km": geo_legit,
        "card_age_days": np.round(np.random.uniform(60, 1800, size=num_std_legit), 0),
        "failed_attempts_24h": np.random.choice([0, 1], size=num_std_legit, p=[0.97, 0.03]),
        "is_fraud": 0
    })
    
    # Hard negatives (25% of legit)
    num_hard_neg = num_legit - num_std_legit
    num_coffee = num_hard_neg // 3
    num_vpn = num_hard_neg // 3
    num_power = num_hard_neg - num_coffee - num_vpn
    
    # Coffee ($0.50 - $3.50, low velocity)
    c_amt = np.round(np.random.uniform(0.50, 3.50, size=num_coffee), 2)
    c_vel = np.round(np.random.uniform(1.0, 3.0, size=num_coffee), 2)
    c_risk = np.round(np.random.beta(1.5, 6.0, size=num_coffee), 4)
    c_geo = np.round(np.random.uniform(0.5, 20.0, size=num_coffee), 2)
    c_mcc = np.array([0.15] * num_coffee)
    
    # VPN ($20 - $2500, geo 400-2500km, risk 0.55-0.85, vel 1.0-2.5)
    v_amt = np.round(np.random.uniform(20.0, 2500.0, size=num_vpn), 2)
    v_vel = np.round(np.random.uniform(1.0, 2.5, size=num_vpn), 2)
    v_risk = np.round(np.random.uniform(0.55, 0.85, size=num_vpn), 4)
    v_geo = np.round(np.random.uniform(400.0, 2500.0, size=num_vpn), 2)
    v_mcc = np.array([0.30] * num_vpn)
    
    # Power shoppers (vel 8-20, clean device 0.1-0.25, amount 20-500)
    p_amt = np.round(np.random.uniform(20.0, 500.0, size=num_power), 2)
    p_vel = np.round(np.random.uniform(8.0, 20.0, size=num_power), 2)
    p_risk = np.round(np.random.beta(1.2, 7.0, size=num_power), 4)
    p_geo = np.round(np.random.uniform(1.0, 45.0, size=num_power), 2)
    p_mcc = np.array([0.40] * num_power)
    
    df_hn = pd.DataFrame({
        "amount": np.concatenate([c_amt, v_amt, p_amt]),
        "velocity": np.concatenate([c_vel, v_vel, p_vel]),
        "device_risk_score": np.concatenate([c_risk, v_risk, p_risk]),
        "is_decline": np.random.choice([0, 1], size=num_hard_neg, p=[0.94, 0.06]),
        "hour_of_day_sin": 0.0,
        "hour_of_day_cos": 1.0,
        "mcc_risk_weight": np.concatenate([c_mcc, v_mcc, p_mcc]),
        "geo_distance_km": np.concatenate([c_geo, v_geo, p_geo]),
        "card_age_days": np.round(np.random.uniform(60, 1500, size=num_hard_neg), 0),
        "failed_attempts_24h": np.random.choice([0, 1], size=num_hard_neg, p=[0.95, 0.05]),
        "is_fraud": 0
    })
    
    # Fraud Sub-Types
    n_p1 = num_fraud // 5  # Burst
    n_p2 = num_fraud // 5  # ATO
    n_p3 = num_fraud // 5  # Slow Drip
    n_p4 = num_fraud // 5  # CNP
    n_p5 = num_fraud - (n_p1 + n_p2 + n_p3 + n_p4) # Friendly Fraud
    
    # 1. Burst ($0.50-$3.00 micro test + $1500-$4000 drain, HIGH velocity 8-30, HIGH device risk 0.75-0.95)
    f1_amt = np.concatenate([np.random.uniform(0.50, 3.00, size=int(n_p1*0.6)), np.random.uniform(1500.0, 4000.0, size=n_p1 - int(n_p1*0.6))])
    f1_vel = np.round(np.random.uniform(8.0, 32.0, size=n_p1), 2)
    f1_risk = np.round(np.random.beta(6.0, 1.5, size=n_p1), 4)
    f1_dec = np.random.choice([0, 1], size=n_p1, p=[0.30, 0.70])
    f1_fail = np.random.choice([2, 3, 4, 5, 7], size=n_p1)
    df_f1 = pd.DataFrame({
        "amount": np.round(f1_amt, 2), "velocity": f1_vel, "device_risk_score": f1_risk,
        "is_decline": f1_dec, "hour_of_day_sin": 0.0, "hour_of_day_cos": 1.0,
        "mcc_risk_weight": 0.85, "geo_distance_km": np.round(np.random.uniform(10.0, 4000.0, size=n_p1), 2),
        "card_age_days": np.round(np.random.uniform(5, 500, size=n_p1), 0),
        "failed_attempts_24h": f1_fail, "is_fraud": 1
    })
    
    # 2. ATO (High amount $500 - $3500 + EXTREME DEVICE RISK 0.78-0.98 + FOREIGN GEO 3000-6500km)
    f2_amt = np.round(np.random.uniform(500.0, 3500.0, size=n_p2), 2)
    f2_vel = np.round(np.random.uniform(1.0, 3.0, size=n_p2), 2)
    f2_risk = np.round(np.random.uniform(0.78, 0.98, size=n_p2), 4) # High device risk
    f2_geo = np.round(np.random.uniform(3000.0, 6800.0, size=n_p2), 2) # Foreign geo displacement
    df_f2 = pd.DataFrame({
        "amount": f2_amt, "velocity": f2_vel, "device_risk_score": f2_risk,
        "is_decline": np.random.choice([0, 1], size=n_p2, p=[0.85, 0.15]),
        "hour_of_day_sin": 0.0, "hour_of_day_cos": 1.0, "mcc_risk_weight": 0.40,
        "geo_distance_km": f2_geo, "card_age_days": np.round(np.random.uniform(180, 1500, size=n_p2), 0),
        "failed_attempts_24h": np.random.choice([0, 1, 2], size=n_p2, p=[0.7, 0.2, 0.1]), "is_fraud": 1
    })
    
    # 3. Slow Drip ($20-$85 recurring, proxy/device risk 0.50-0.75, high mcc weight 0.80-0.90)
    f3_amt = np.round(np.random.uniform(18.0, 85.0, size=n_p3), 2)
    f3_vel = np.round(np.random.uniform(0.5, 2.0, size=n_p3), 2)
    f3_risk = np.round(np.random.uniform(0.50, 0.75, size=n_p3), 4)
    df_f3 = pd.DataFrame({
        "amount": f3_amt, "velocity": f3_vel, "device_risk_score": f3_risk,
        "is_decline": np.random.choice([0, 1], size=n_p3, p=[0.95, 0.05]),
        "hour_of_day_sin": 0.0, "hour_of_day_cos": 1.0, "mcc_risk_weight": 0.88,
        "geo_distance_km": np.round(np.random.uniform(5.0, 120.0, size=n_p3), 2),
        "card_age_days": np.round(np.random.uniform(60, 1200, size=n_p3), 0),
        "failed_attempts_24h": 0, "is_fraud": 1
    })
    
    # 4. CNP ($150-$3000, risky MCC 0.88, elevated device risk 0.65-0.85, vel 2-5)
    f4_amt = np.round(np.random.uniform(150.0, 3000.0, size=n_p4), 2)
    f4_vel = np.round(np.random.uniform(2.0, 5.0, size=n_p4), 2)
    f4_risk = np.round(np.random.uniform(0.65, 0.88, size=n_p4), 4)
    df_f4 = pd.DataFrame({
        "amount": f4_amt, "velocity": f4_vel, "device_risk_score": f4_risk,
        "is_decline": np.random.choice([0, 1], size=n_p4, p=[0.70, 0.30]),
        "hour_of_day_sin": 0.0, "hour_of_day_cos": 1.0, "mcc_risk_weight": 0.88,
        "geo_distance_km": np.round(np.random.uniform(100.0, 2500.0, size=n_p4), 2),
        "card_age_days": np.round(np.random.uniform(10, 800, size=n_p4), 0),
        "failed_attempts_24h": np.random.choice([1, 2, 3], size=n_p4), "is_fraud": 1
    })
    
    # 5. Friendly Fraud ($500-$3200 luxury/specialty, late night off-hours 02:00-04:00, moderate device risk 0.30-0.55)
    f5_amt = np.round(np.random.uniform(500.0, 3200.0, size=n_p5), 2)
    f5_vel = np.round(np.random.uniform(1.0, 2.5, size=n_p5), 2)
    f5_risk = np.round(np.random.uniform(0.30, 0.55, size=n_p5), 4)
    f5_hours = np.random.choice([1.0, 2.0, 3.0, 4.0], size=n_p5)
    df_f5 = pd.DataFrame({
        "amount": f5_amt, "velocity": f5_vel, "device_risk_score": f5_risk,
        "is_decline": 0,
        "hour_of_day_sin": np.round(np.sin(2 * np.pi * f5_hours / 24.0), 4),
        "hour_of_day_cos": np.round(np.cos(2 * np.pi * f5_hours / 24.0), 4),
        "mcc_risk_weight": 0.40,
        "geo_distance_km": np.round(np.random.uniform(1.0, 40.0, size=n_p5), 2),
        "card_age_days": np.round(np.random.uniform(150, 1600, size=n_p5), 0),
        "failed_attempts_24h": 0, "is_fraud": 1
    })
    
    df = pd.concat([df_legit, df_hn, df_f1, df_f2, df_f3, df_f4, df_f5], ignore_index=True)
    return df

if __name__ == "__main__":
    df = build_realistic_dataset()
    print("Dataset shape:", df.shape)
    
    X = df[TABULAR_FEATURE_COLS].values
    y = df["is_fraud"].values
    
    # Fit XGBoost
    num_neg = (y == 0).sum()
    num_pos = (y == 1).sum()
    scale_pos_weight = float(num_neg / max(1, num_pos))
    
    clf = XGBClassifier(
        n_estimators=250, max_depth=6, learning_rate=0.05,
        subsample=0.85, colsample_bytree=0.85,
        scale_pos_weight=scale_pos_weight, random_state=42, eval_metric="logloss"
    )
    clf.fit(X, y)
    
    print("\n--- TEST CASES ---")
    test_cases = [
        ("Legit Single Purchase $2,110 (Clean Device 5%, Vel 1.0, Domestic 25km, Daytime)",
         {"amount": 2110.0, "velocity": 1.0, "device_risk_score": 0.05, "is_decline": 0, "hour_of_day_sin": 0.0, "hour_of_day_cos": 1.0, "mcc_risk_weight": 0.35, "geo_distance_km": 25.0, "card_age_days": 365.0, "failed_attempts_24h": 0}),
        
        ("Legit Everyday Grocery $45.00 (Clean Device 5%, Vel 1.0)",
         {"amount": 45.0, "velocity": 1.0, "device_risk_score": 0.05, "is_decline": 0, "hour_of_day_sin": 0.0, "hour_of_day_cos": 1.0, "mcc_risk_weight": 0.10, "geo_distance_km": 5.0, "card_age_days": 365.0, "failed_attempts_24h": 0}),

        ("ATO Fraud $2,110 (Attacker Device 92%, Foreign Geo 4500km, Vel 1.0)",
         {"amount": 2110.0, "velocity": 1.0, "device_risk_score": 0.92, "is_decline": 0, "hour_of_day_sin": 0.0, "hour_of_day_cos": 1.0, "mcc_risk_weight": 0.40, "geo_distance_km": 4500.0, "card_age_days": 365.0, "failed_attempts_24h": 0}),

        ("Card Testing Burst ($1.50 swipe, Velocity 16.0, Device Risk 85%, Failed 3)",
         {"amount": 1.50, "velocity": 16.0, "device_risk_score": 0.85, "is_decline": 1, "hour_of_day_sin": 0.0, "hour_of_day_cos": 1.0, "mcc_risk_weight": 0.85, "geo_distance_km": 150.0, "card_age_days": 45.0, "failed_attempts_24h": 3}),

        ("Card Testing Drain ($2,110 after burst, Velocity 22.0, Device Risk 90%)",
         {"amount": 2110.0, "velocity": 22.0, "device_risk_score": 0.90, "is_decline": 0, "hour_of_day_sin": 0.0, "hour_of_day_cos": 1.0, "mcc_risk_weight": 0.85, "geo_distance_km": 150.0, "card_age_days": 45.0, "failed_attempts_24h": 4}),
    ]
    
    for name, d in test_cases:
        x_row = np.array([[d[f] for f in TABULAR_FEATURE_COLS]], dtype=np.float32)
        prob = clf.predict_proba(x_row)[0][1]
        print(f"[{'SAFE' if prob < 0.5 else 'FRAUD'}] ({prob*100:.1f}%) -> {name}")
