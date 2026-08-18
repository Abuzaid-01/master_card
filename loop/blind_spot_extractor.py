"""
Blind Spot Extractor: Identifies what Round 1 misses on the Mining partition.
Runs Round 1 models against adversarially perturbed mining data and isolates failures.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List
from loop.multi_strategy_prober import MultiStrategyProber


def extract_blind_spots(
    partitions: dict,
    threshold_tabular: float = 0.5,
    threshold_graph: float = 0.5,
    threshold_text: float = 0.5,
    mining_strategy_seed: int = 42
) -> Dict[str, Any]:
    """
    For each vector's mining partition, runs model-aware probing against Round 1
    and extracts the adversarial samples that successfully evaded detection.
    
    Returns dict with evaded samples and statistics.
    """
    prober = MultiStrategyProber()
    results = {}

    # ── TABULAR ──
    if "tabular" in partitions:
        df_mine = partitions["tabular"]["df_mine"]
        df_mine_fraud = df_mine[df_mine["is_fraud"] == 1].copy()
        
        print(f"[Blind Spot Extractor] TABULAR: Probing {len(df_mine_fraud)} fraud samples from mining set...")
        df_evaded = prober.probe_tabular(df_mine_fraud, threshold=threshold_tabular,
                                          strategy_seed=mining_strategy_seed)
        
        # Check which evaded samples actually fooled Round 1
        feature_cols = prober.tabular_feature_cols
        for col in feature_cols:
            if col not in df_evaded.columns:
                df_evaded[col] = 0.0

        if prober.tabular_model is not None:
            probs_after = prober._tabular_predict_proba(
                df_evaded[feature_cols].values.astype(np.float32)
            )
            evaded_mask = probs_after < threshold_tabular
            n_evaded = int(evaded_mask.sum())
        else:
            n_evaded = len(df_evaded)
            evaded_mask = np.ones(len(df_evaded), dtype=bool)
        
        # Combine: evaded fraud + all mining legit for retraining pool
        df_mine_legit = df_mine[df_mine["is_fraud"] == 0].copy()
        df_failures = pd.concat([df_evaded[evaded_mask], df_mine_legit], ignore_index=True)
        
        results["tabular"] = {
            "df_failures": df_failures,
            "df_evaded_fraud": df_evaded,
            "n_fraud_probed": len(df_mine_fraud),
            "n_evaded": n_evaded,
            "evasion_rate": float(np.round(n_evaded / max(1, len(df_mine_fraud)), 4)),
        }
        print(f"      -> {n_evaded}/{len(df_mine_fraud)} fraud samples evaded Round 1 "
              f"({results['tabular']['evasion_rate']*100:.1f}% evasion rate)")

    # ── GRAPH ──
    if "graph" in partitions:
        df_mine = partitions["graph"]["df_mine"]
        df_mine_fraud = df_mine[df_mine["is_fraud"] == 1].copy()
        
        print(f"[Blind Spot Extractor] GRAPH: Probing {len(df_mine_fraud)} fraud samples from mining set...")
        df_evaded = prober.probe_graph(df_mine_fraud, threshold=threshold_graph,
                                        strategy_seed=mining_strategy_seed)
        
        graph_features = [c for c in ["amount", "sender_in_degree", "sender_out_degree",
                                       "receiver_in_degree", "receiver_out_degree",
                                       "receiver_mule_funnel_score",
                                       "pass_through_delay_sec"] if c in df_evaded.columns]
        
        if prober.graph_model is not None and len(graph_features) > 0:
            probs_after = prober.graph_model.predict_proba(
                df_evaded[graph_features].values.astype(float)
            )[:, 1]
            evaded_mask = probs_after < threshold_graph
            n_evaded = int(evaded_mask.sum())
        else:
            n_evaded = len(df_evaded)
            evaded_mask = np.ones(len(df_evaded), dtype=bool)
        
        df_mine_legit = df_mine[df_mine["is_fraud"] == 0].copy()
        df_failures = pd.concat([df_evaded[evaded_mask], df_mine_legit], ignore_index=True)
        
        results["graph"] = {
            "df_failures": df_failures,
            "df_evaded_fraud": df_evaded,
            "n_fraud_probed": len(df_mine_fraud),
            "n_evaded": n_evaded,
            "evasion_rate": float(np.round(n_evaded / max(1, len(df_mine_fraud)), 4)),
        }
        print(f"      -> {n_evaded}/{len(df_mine_fraud)} fraud samples evaded Round 1 "
              f"({results['graph']['evasion_rate']*100:.1f}% evasion rate)")

    # ── TEXT ──
    if "text" in partitions:
        df_mine = partitions["text"]["df_mine"]
        df_mine_fraud = df_mine[df_mine["is_fraud"] == 1].copy()
        
        print(f"[Blind Spot Extractor] TEXT: Evaluating {len(df_mine_fraud)} fraud prompts against Round 1...")
        text_result = prober.probe_text_evasion_rate(df_mine_fraud, threshold=threshold_text)
        
        results["text"] = {
            "df_mine_fraud": df_mine_fraud,
            "missed_indices": text_result["missed_indices"],
            "n_fraud_probed": text_result["n_fraud"],
            "n_evaded": text_result["n_missed"],
            "evasion_rate": text_result["evasion_rate"],
        }
        print(f"      -> {text_result['n_missed']}/{text_result['n_fraud']} prompts evaded Round 1 "
              f"({text_result['evasion_rate']*100:.1f}% evasion rate)")

    return results
