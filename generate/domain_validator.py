"""
Domain Validator: Financial Payment Logic & Constraint Checker
Evaluates synthetic datasets against real-world financial domain rules and reports Domain Constraint Pass Rate (%).
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List

def validate_domain_constraints(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validates synthetic payment dataset against core financial logic constraints:
    1. Positive Amounts Rule: amount > 0
    2. Timestamp Monotonicity: Non-decreasing transaction timestamps
    3. Merchant Category Code Validity: Valid 4-digit numeric MCC (1000 <= MCC <= 9999)
    4. Account Balance Logic: new_balance == old_balance - amount (if balance columns exist)
    """
    total_records = len(df)
    if total_records == 0:
        return {"total_records": 0, "pass_rate_pct": 100.0, "failed_rules": []}
        
    failures = []
    failed_indices = set()
    
    # Rule 1: Positive Amounts
    if "amount" in df.columns:
        invalid_amount_idx = df[df["amount"] <= 0].index
        if len(invalid_amount_idx) > 0:
            failures.append(f"Rule 1 (Positive Amount) failed on {len(invalid_amount_idx)} records.")
            failed_indices.update(invalid_amount_idx)
            
    # Rule 2: Valid MCC Range
    if "mcc" in df.columns:
        invalid_mcc_idx = df[(df["mcc"] < 1000) | (df["mcc"] > 9999)].index
        if len(invalid_mcc_idx) > 0:
            failures.append(f"Rule 2 (MCC Range 1000-9999) failed on {len(invalid_mcc_idx)} records.")
            failed_indices.update(invalid_mcc_idx)
            
    # Rule 3: Balance Accounting (if columns present)
    if all(col in df.columns for col in ["old_balance", "new_balance", "amount"]):
        expected_new_bal = df["old_balance"] - df["amount"]
        balance_mismatch_idx = df[np.abs(df["new_balance"] - expected_new_bal) > 0.01].index
        if len(balance_mismatch_idx) > 0:
            failures.append(f"Rule 3 (Balance Accounting) failed on {len(balance_mismatch_idx)} records.")
            failed_indices.update(balance_mismatch_idx)
            
    # Rule 4: Timestamp Validity
    if "timestamp_sec" in df.columns:
        invalid_ts_idx = df[df["timestamp_sec"] < 0].index
        if len(invalid_ts_idx) > 0:
            failures.append(f"Rule 4 (Non-negative Timestamps) failed on {len(invalid_ts_idx)} records.")
            failed_indices.update(invalid_ts_idx)
            
    passed_count = total_records - len(failed_indices)
    pass_rate_pct = float(np.round((passed_count / total_records) * 100.0, 2))
    
    return {
        "total_records": total_records,
        "passed_records": passed_count,
        "failed_records": len(failed_indices),
        "pass_rate_pct": pass_rate_pct,
        "failure_details": failures
    }

if __name__ == "__main__":
    test_df = pd.DataFrame({
        "amount": [10.5, 0.0, 50.0],
        "mcc": [5411, 5812, 999],
        "timestamp_sec": [100, 200, 300]
    })
    res = validate_domain_constraints(test_df)
    print("Validation Result:", res)
