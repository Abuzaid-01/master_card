"""
Amount-Proportional Financial Cost Curve Optimizer
Finds the optimal decision threshold tau* minimizing total financial loss:
Total Cost = Sum_{FN}(Amount * 1.2) + Sum_{FP}(Customer Friction Cost $15.00)
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple

def calculate_amount_proportional_cost(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    amounts: np.ndarray,
    threshold: float,
    chargeback_multiplier: float = 1.2,
    false_positive_friction_cost: float = 15.0
) -> Dict[str, float]:
    """
    Calculates total financial loss at a given decision threshold tau:
    - False Negative Cost = Sum of (Amount * 1.2) for missed fraud transactions
    - False Positive Cost = Sum of ($15.00 customer friction fee) for falsely flagged legit transactions
    """
    y_pred = (y_prob >= threshold).astype(int)
    
    # Identify False Negatives (actual fraud = 1, predicted = 0)
    fn_mask = (y_true == 1) & (y_pred == 0)
    # Identify False Positives (actual legit = 0, predicted = 1)
    fp_mask = (y_true == 0) & (y_pred == 1)
    # Identify True Positives (actual fraud = 1, predicted = 1)
    tp_mask = (y_true == 1) & (y_pred == 1)
    # Identify True Negatives (actual legit = 0, predicted = 0)
    tn_mask = (y_true == 0) & (y_pred == 0)
    
    fn_count = int(np.sum(fn_mask))
    fp_count = int(np.sum(fp_mask))
    tp_count = int(np.sum(tp_mask))
    tn_count = int(np.sum(tn_mask))
    
    fn_cost = float(np.sum(amounts[fn_mask] * chargeback_multiplier)) if fn_count > 0 else 0.0
    fp_cost = float(fp_count * false_positive_friction_cost)
    total_cost = fn_cost + fp_cost
    
    saved_fraud_amount = float(np.sum(amounts[tp_mask])) if tp_count > 0 else 0.0
    
    return {
        "threshold": float(np.round(threshold, 4)),
        "total_financial_loss": float(np.round(total_cost, 2)),
        "fn_fraud_loss": float(np.round(fn_cost, 2)),
        "fp_friction_loss": float(np.round(fp_cost, 2)),
        "saved_fraud_amount": float(np.round(saved_fraud_amount, 2)),
        "false_negatives_count": fn_count,
        "false_positives_count": fp_count,
        "true_positives_count": tp_count,
        "true_negatives_count": tn_count
    }

def find_optimal_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    amounts: np.ndarray,
    chargeback_multiplier: float = 1.2,
    false_positive_friction_cost: float = 15.0
) -> Dict[str, Any]:
    """Sweeps thresholds tau in [0.01, 0.99] to find optimal tau* minimizing total financial loss."""
    thresholds = np.linspace(0.01, 0.99, 99)
    cost_curve = []
    
    best_cost = float("inf")
    best_result = None
    
    for tau in thresholds:
        res = calculate_amount_proportional_cost(
            y_true, y_prob, amounts, tau,
            chargeback_multiplier, false_positive_friction_cost
        )
        cost_curve.append(res)
        if res["total_financial_loss"] < best_cost:
            best_cost = res["total_financial_loss"]
            best_result = res
            
    # Default threshold (0.50) cost for comparison
    default_res = calculate_amount_proportional_cost(
        y_true, y_prob, amounts, 0.50,
        chargeback_multiplier, false_positive_friction_cost
    )
    
    savings = default_res["total_financial_loss"] - best_result["total_financial_loss"]
    
    return {
        "optimal_threshold": best_result["threshold"],
        "min_financial_loss": best_result["total_financial_loss"],
        "default_threshold_loss": default_res["total_financial_loss"],
        "cost_savings_vs_default": float(np.round(savings, 2)),
        "optimal_details": best_result,
        "cost_curve_sample": cost_curve[::10]  # Every 10th point for summary reporting
    }

if __name__ == "__main__":
    y_true = np.array([0]*90 + [1]*10)
    y_prob = np.random.uniform(0, 1, 100)
    amounts = np.random.uniform(10, 500, 100)
    opt = find_optimal_threshold(y_true, y_prob, amounts)
    print("Optimal Threshold Result:", opt["optimal_threshold"], "Min Loss:", opt["min_financial_loss"])
