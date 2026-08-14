"""
Step 2 End-to-End Orchestrator Pipeline
Executes all 4 synthetic attack generators, runs domain logic validation, calculates fidelity metrics,
and exports synthetic datasets & JSON reports to data/synthetic/.
"""

import os
import json
import pandas as pd
from generate.generator_tabular import generate_tabular_card_testing
from generate.generator_text import generate_text_prompt_injections
from generate.generator_graph import generate_money_mule_graph
from generate.generator_evasion import apply_adversarial_evasion_perturbations
from generate.domain_validator import validate_domain_constraints
from generate.fidelity_eval import generate_fidelity_report

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "synthetic")

def run_step2_generation_pipeline(
    num_samples_per_vector: int = 500,
    export_data: bool = True
) -> dict:
    """Runs the complete Step 2 Generation Pipeline end-to-end."""
    print("=" * 60)
    print(" Mastercard Innovation Challenge 2026 — Step 2 Generation Pipeline")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Vector 5: Evasive Card Testing (Tabular)
    print("[1/4] Generating Vector 5: Evasive Card Testing (Micro-Bursts)...")
    df_tabular = generate_tabular_card_testing(num_samples=num_samples_per_vector)
    val_tabular = validate_domain_constraints(df_tabular)
    print(f"      -> Generated {len(df_tabular)} rows. Domain Pass Rate: {val_tabular['pass_rate_pct']}%")
    
    # 2. Vector 1: Indirect Prompt Injection (Text)
    print("[2/4] Generating Vector 1: Indirect Prompt Injection Payloads...")
    df_text = generate_text_prompt_injections(num_samples=num_samples_per_vector // 5)
    val_text = validate_domain_constraints(df_text)
    print(f"      -> Generated {len(df_text)} prompt logs. Domain Pass Rate: {val_text['pass_rate_pct']}%")
    
    # 3. Vector 2: AI Money Mule Networks (Graph)
    print("[3/4] Generating Vector 2: Multi-Hop Money Mule Graph Network...")
    df_graph = generate_money_mule_graph(num_users=num_samples_per_vector // 5, num_mule_rings=10)
    val_graph = validate_domain_constraints(df_graph)
    print(f"      -> Generated {len(df_graph)} graph transfers. Domain Pass Rate: {val_graph['pass_rate_pct']}%")
    
    # 4. Vector 8: Adversarial Transaction Pattern Evasion
    print("[4/4] Applying Vector 8: Adversarial Boundary Perturbations...")
    df_evasion = apply_adversarial_evasion_perturbations(df_tabular, evasion_ratio=0.3)
    val_evasion = validate_domain_constraints(df_evasion)
    print(f"      -> Generated perturbed dataset. Domain Pass Rate: {val_evasion['pass_rate_pct']}%")
    
    # 5. Compute Fidelity Benchmark Report
    print("\n[Fidelity Suite] Computing Wasserstein Distances & TSTR Score...")
    df_real_baseline = generate_tabular_card_testing(num_samples=num_samples_per_vector, random_seed=999)
    fidelity_report = generate_fidelity_report(
        df_real_baseline,
        df_tabular,
        feature_cols=["amount", "device_risk_score", "is_decline"]
    )
    
    summary = {
        "tabular_pass_rate_pct": val_tabular["pass_rate_pct"],
        "text_pass_rate_pct": val_text["pass_rate_pct"],
        "graph_pass_rate_pct": val_graph["pass_rate_pct"],
        "evasion_pass_rate_pct": val_evasion["pass_rate_pct"],
        "tstr_auc_pr": fidelity_report["tstr_utility"]["tstr_auc_pr"],
        "fidelity_details": fidelity_report
    }
    
    # Export datasets
    if export_data:
        df_tabular.to_csv(os.path.join(OUTPUT_DIR, "synthetic_tabular_card_testing.csv"), index=False)
        df_text.to_csv(os.path.join(OUTPUT_DIR, "synthetic_prompt_injections.csv"), index=False)
        df_graph.to_csv(os.path.join(OUTPUT_DIR, "synthetic_mule_graph.csv"), index=False)
        df_evasion.to_csv(os.path.join(OUTPUT_DIR, "synthetic_evasion_patterns.csv"), index=False)
        
        with open(os.path.join(OUTPUT_DIR, "fidelity_report.json"), "w") as f:
            json.dump(summary, f, indent=2)
            
        print(f"\n[Success] All datasets & fidelity reports exported to: {OUTPUT_DIR}")
        
    return summary

if __name__ == "__main__":
    run_step2_generation_pipeline()
