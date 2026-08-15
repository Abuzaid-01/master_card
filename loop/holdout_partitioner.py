"""
Holdout Partitioner: Splits Step 4 holdout slices into Mining and Final Eval partitions.
Ensures strict data isolation to prevent leakage between retraining and evaluation.
"""

import os
import pandas as pd
from typing import Tuple

DEFEND_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "defend")

def partition_holdout(
    holdout_path: str,
    mining_ratio: float = 0.5,
    random_seed: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits a Step 4 holdout CSV into Mining and Final Eval partitions.
    Uses stratified sampling to preserve fraud ratio in both halves.
    
    Returns:
        (df_mine, df_eval) — two strictly isolated DataFrames.
    """
    df = pd.read_csv(holdout_path)
    
    # Determine target column
    target_col = "is_fraud"
    if target_col not in df.columns:
        raise ValueError(f"Expected column '{target_col}' in holdout file: {holdout_path}")
    
    # Stratified split: separately shuffle fraud and legit, take first half of each
    df_fraud = df[df[target_col] == 1].sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    df_legit = df[df[target_col] == 0].sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    
    n_fraud_mine = int(len(df_fraud) * mining_ratio)
    n_legit_mine = int(len(df_legit) * mining_ratio)
    
    df_mine = pd.concat([
        df_fraud.iloc[:n_fraud_mine],
        df_legit.iloc[:n_legit_mine]
    ], ignore_index=True).sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    
    df_eval = pd.concat([
        df_fraud.iloc[n_fraud_mine:],
        df_legit.iloc[n_legit_mine:]
    ], ignore_index=True).sample(frac=1.0, random_state=random_seed + 1).reset_index(drop=True)
    
    return df_mine, df_eval


def partition_all_holdouts() -> dict:
    """Partitions all three Step 4 holdout files (tabular, text, graph)."""
    results = {}
    
    for name in ["tabular", "text", "graph"]:
        path = os.path.join(DEFEND_DATA_DIR, f"step4_holdout_{name}.csv")
        if not os.path.exists(path):
            print(f"[Warning] Holdout file not found: {path}")
            continue
            
        df_mine, df_eval = partition_holdout(path)
        
        fraud_mine = (df_mine["is_fraud"] == 1).sum()
        fraud_eval = (df_eval["is_fraud"] == 1).sum()
        
        results[name] = {
            "df_mine": df_mine,
            "df_eval": df_eval,
            "mine_total": len(df_mine),
            "mine_fraud": int(fraud_mine),
            "eval_total": len(df_eval),
            "eval_fraud": int(fraud_eval),
        }
        
        print(f"[Holdout Partitioner] {name.upper()}: "
              f"Mining={len(df_mine)} ({fraud_mine} fraud) | "
              f"Final Eval={len(df_eval)} ({fraud_eval} fraud)")
    
    return results
