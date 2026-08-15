"""
Data Splitter & Step 4 Holdout Manager
Splits synthetic datasets into Train (60%), Validation (20%), and Step 4 Holdout (20%) sets.
Saves the 20% Holdout set to data/defend/step4_holdout.csv for Step 4 evaluation.
"""

import os
import pandas as pd
from typing import Tuple, Dict, Any
from sklearn.model_selection import train_test_split

DEFEND_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "defend")

def split_and_preserve_holdout(
    df: pd.DataFrame,
    target_col: str = "is_fraud",
    dataset_name: str = "tabular",
    random_seed: int = 42,
    verbose: bool = True
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Splits dataframe into Train (60%), Validation (20%), and Step 4 Holdout (20%).
    Preserves class balance via stratify on target_col.
    """
    os.makedirs(DEFEND_DATA_DIR, exist_ok=True)
    
    # First split: 80% Train+Val, 20% Holdout
    df_train_val, df_holdout = train_test_split(
        df,
        test_size=0.20,
        random_state=random_seed,
        stratify=df[target_col] if target_col in df.columns else None
    )
    
    # Second split: 60% Train, 20% Val (0.25 of 80% is 20% total)
    df_train, df_val = train_test_split(
        df_train_val,
        test_size=0.25,
        random_state=random_seed,
        stratify=df_train_val[target_col] if target_col in df_train_val.columns else None
    )
    
    # Save Step 4 Holdout to disk
    holdout_path = os.path.join(DEFEND_DATA_DIR, f"step4_holdout_{dataset_name}.csv")
    df_holdout.to_csv(holdout_path, index=False)
    
    if verbose:
        print(f"[Data Splitter] {dataset_name.upper()} Dataset split: Train={len(df_train)}, Val={len(df_val)}, Step4 Holdout={len(df_holdout)} (Saved to: {holdout_path})")
    
    return df_train, df_val, df_holdout

if __name__ == "__main__":
    df_test = pd.DataFrame({
        "feature_1": range(100),
        "is_fraud": [0]*85 + [1]*15
    })
    tr, val, ho = split_and_preserve_holdout(df_test, dataset_name="test")
    print(f"Train fraud count: {tr['is_fraud'].sum()}, Val fraud count: {val['is_fraud'].sum()}, Holdout fraud count: {ho['is_fraud'].sum()}")
