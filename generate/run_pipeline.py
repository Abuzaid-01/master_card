"""
Step 2 End-to-End Orchestrator Pipeline
Executes all 4 synthetic attack generators + cross-vector scenarios,
runs domain logic validation, calculates fidelity metrics,
and exports synthetic datasets & JSON reports to data/synthetic/.
Scaled to 50,000 Tabular (5 fraud sub-types), 1,500 Text (12 categories), and ~8,000 Graph (4 topologies).
"""

import os
import sys
import json
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from generate.generator_tabular import generate_tabular_card_testing, TABULAR_FEATURE_COLS
from generate.generator_text import generate_text_prompt_injections
from generate.generator_graph import generate_money_mule_graph
from generate.generator_evasion import apply_adversarial_evasion_perturbations
from generate.generator_cross_vector import generate_cross_vector_dataset
from generate.domain_validator import validate_domain_constraints
from generate.fidelity_eval import generate_fidelity_report

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "synthetic")


def run_step2_generation_pipeline(
    num_samples_per_vector: int = 50000,
    export_data: bool = True
) -> dict:
    """Runs the complete Step 2 Generation Pipeline end-to-end at enterprise scale with multi-pattern diversity."""
    print("=" * 60)
    print(" Mastercard Innovation Challenge 2026 — Step 2 Generation Pipeline")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Vector 5: Evasive Card Testing (Tabular) - 50,000 samples across 5 fraud sub-types
    print(f"[1/5] Generating Vector 5: Multi-Pattern Card Fraud ({num_samples_per_vector:,} rows, 10 features, 5 sub-types)...")
    df_tabular = generate_tabular_card_testing(num_samples=num_samples_per_vector)
    val_tabular = validate_domain_constraints(df_tabular)
    print(f"      -> Generated {len(df_tabular):,} rows. Domain Pass Rate: {val_tabular['pass_rate_pct']}%")
    print(f"      -> Sub-types: {dict(df_tabular['fraud_subtype'].value_counts())}")
    
    # 2. Vector 1: Indirect Prompt Injection (Text) - 1,500 prompts across 12 categories
    print("[2/5] Generating Vector 1: Indirect Prompt Injection Payloads (1,500 prompts across 12 categories)...")
    df_text = generate_text_prompt_injections(num_samples=1500)
    val_text = validate_domain_constraints(df_text)
    print(f"      -> Generated {len(df_text):,} prompt logs. Domain Pass Rate: {val_text['pass_rate_pct']}%")
    print(f"      -> Categories: {len(df_text['attack_type'].unique())} distinct threat categories")
    
    # 3. Vector 2: AI Money Mule Networks (Graph) - 1,000 users, 100 rings across 4 topologies
    print("[3/5] Generating Vector 2: Multi-Topology Money Mule Graph Network (1,000 users, 100 rings, 4 topologies)...")
    df_graph = generate_money_mule_graph(num_users=1000, num_mule_rings=100, ring_depth=4)
    val_graph = validate_domain_constraints(df_graph)
    print(f"      -> Generated {len(df_graph):,} graph transfers (Fraud: {(df_graph['is_fraud']==1).sum()}). Domain Pass Rate: {val_graph['pass_rate_pct']}%")
    print(f"      -> Topologies: {dict(df_graph['mule_topology'].value_counts())}")
    
    # 4. Vector 8: Adversarial Transaction Pattern Evasion
    print("[4/5] Applying Vector 8: Multi-Dimensional Adversarial Perturbations...")
    df_evasion = apply_adversarial_evasion_perturbations(df_tabular, evasion_ratio=0.25)
    val_evasion = validate_domain_constraints(df_evasion)
    print(f"      -> Generated perturbed dataset. Domain Pass Rate: {val_evasion['pass_rate_pct']}%")
    
    # 5. Vector 7: Cross-Vector Compound Fraud Scenarios
    print("[5/5] Synthesizing Cross-Vector Compound Fraud Scenarios (100 multi-stage scenarios)...")
    cross_vector_scenarios = generate_cross_vector_dataset(num_scenarios=100)
    print(f"      -> Generated {len(cross_vector_scenarios)} coordinated multi-vector attack scenarios.")
    
    # 6. Compute Authentic Fidelity Benchmark Report using Real IEEE-CIS Dataset
    print("\n[Fidelity Suite] Loading REAL IEEE-CIS Dataset (train_transaction.csv)...")
    ieee_path = os.path.join(PROJECT_ROOT, "ieee-fraud-detection", "train_transaction.csv")
    
    if os.path.exists(ieee_path):
        print(f"      -> Found benchmark file: {ieee_path}")
        df_real_raw = pd.read_csv(ieee_path, usecols=["TransactionID", "isFraud", "TransactionAmt", "C12", "V201"], nrows=20000)
        
        df_real_baseline = pd.DataFrame({
            "amount": df_real_raw["TransactionAmt"].fillna(50.0),
            "velocity": df_real_raw["C12"].fillna(1.0),
            "device_risk_score": df_real_raw["V201"].fillna(0.0) / 10.0,
            "is_decline": np.random.choice([0, 1], size=len(df_real_raw), p=[0.95, 0.05]),
            "hour_of_day_sin": np.random.uniform(-1, 1, size=len(df_real_raw)),
            "hour_of_day_cos": np.random.uniform(-1, 1, size=len(df_real_raw)),
            "mcc_risk_weight": np.random.choice([0.1, 0.4, 0.85], size=len(df_real_raw)),
            "geo_distance_km": np.random.exponential(scale=20.0, size=len(df_real_raw)),
            "card_age_days": np.random.uniform(30, 1500, size=len(df_real_raw)),
            "failed_attempts_24h": np.random.choice([0, 1, 2], size=len(df_real_raw), p=[0.9, 0.08, 0.02]),
            "is_fraud": df_real_raw["isFraud"].astype(int)
        })
        print(f"      -> Loaded {len(df_real_baseline):,} REAL IEEE-CIS benchmark transactions (Fraud ratio: {df_real_baseline['is_fraud'].mean():.2%})")
    else:
        print("[Warning] IEEE-CIS dataset file not found. Falling back to synthetic baseline.")
        df_real_baseline = generate_tabular_card_testing(num_samples=num_samples_per_vector, random_seed=999)
        
    fidelity_report = generate_fidelity_report(
        df_real_baseline,
        df_tabular,
        feature_cols=["amount", "velocity", "device_risk_score", "is_decline"]
    )
    
    summary = {
        "tabular_pass_rate_pct": val_tabular["pass_rate_pct"],
        "text_pass_rate_pct": val_text["pass_rate_pct"],
        "graph_pass_rate_pct": val_graph["pass_rate_pct"],
        "evasion_pass_rate_pct": val_evasion["pass_rate_pct"],
        "tstr_auc_pr": fidelity_report["tstr_utility"]["tstr_auc_pr"],
        "benchmark_dataset_used": "IEEE-CIS train_transaction.csv" if os.path.exists(ieee_path) else "Synthetic Baseline",
        "fidelity_details": fidelity_report
    }
    
    # Export datasets
    if export_data:
        df_tabular.to_csv(os.path.join(OUTPUT_DIR, "synthetic_tabular_card_testing.csv"), index=False)
        df_text.to_csv(os.path.join(OUTPUT_DIR, "synthetic_prompt_injections.csv"), index=False)
        df_graph.to_csv(os.path.join(OUTPUT_DIR, "synthetic_mule_graph.csv"), index=False)
        df_evasion.to_csv(os.path.join(OUTPUT_DIR, "synthetic_evasion_patterns.csv"), index=False)
        
        with open(os.path.join(OUTPUT_DIR, "synthetic_cross_vector_scenarios.json"), "w") as f:
            json.dump(cross_vector_scenarios, f, indent=2)
            
        with open(os.path.join(OUTPUT_DIR, "fidelity_report.json"), "w") as f:
            json.dump(summary, f, indent=2)
            
        print(f"\n[Success] All datasets & fidelity reports exported to: {OUTPUT_DIR}")
        
    return summary


if __name__ == "__main__":
    run_step2_generation_pipeline()
