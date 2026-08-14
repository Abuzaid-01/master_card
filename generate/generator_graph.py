"""
Vector 2 Generator: Multi-Hop AI Money Mule Network Layering
Generates synthetic transaction graph networks with NetworkX simulating multi-hop mule account chains.
Computes topological features (in-degree, out-degree, pass-through velocity, cycle detection).
"""

import numpy as np
import pandas as pd
import networkx as nx
from typing import Dict, Any, Tuple

def generate_money_mule_graph(
    num_users: int = 200,
    num_mule_rings: int = 5,
    ring_depth: int = 3,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generates synthetic payment transfer network with embedded multi-hop money mule rings.
    
    Legitimate transfers connect random customer pairs with realistic hold times.
    Money mule rings feature:
    - Layered topology: Origin -> Mule 1 -> Mule 2 -> Mule 3 -> Crypto/Offshore Exfiltration
    - Ultra-fast pass-through velocity (< 30 seconds between hops)
    - High in-degree and out-degree balance on funnel accounts (near-zero net balance retention)
    """
    np.random.seed(random_seed)
    
    G = nx.DiGraph()
    users = [f"ACC_{i:05d}" for i in range(num_users)]
    for u in users:
        G.add_node(u)
        
    records = []
    tx_id_counter = 0
    
    # 1. Generate Normal Payment Graph Edges
    num_normal_tx = num_users * 3
    for _ in range(num_normal_tx):
        src, dst = np.random.choice(users, size=2, replace=False)
        amount = np.round(np.random.lognormal(mean=4.0, sigma=0.8), 2)
        timestamp = np.random.uniform(0, 86400)
        
        G.add_edge(src, dst, amount=amount, timestamp=timestamp)
        records.append({
            "transaction_id": f"TX_GRAPH_{tx_id_counter:06d}",
            "sender_account": src,
            "receiver_account": dst,
            "amount": amount,
            "timestamp_sec": timestamp,
            "pass_through_delay_sec": np.random.uniform(3600, 86400 * 3),  # Hours/days hold
            "is_fraud": 0,
            "attack_vector": "legitimate_transfer"
        })
        tx_id_counter += 1
        
    # 2. Inject Synthetic Multi-Hop Mule Chains (Funnel Networks)
    for ring_idx in range(num_mule_rings):
        ring_users = np.random.choice(users, size=ring_depth + 2, replace=False)
        origin = ring_users[0]
        exfil = ring_users[-1]
        mules = ring_users[1:-1]
        
        base_time = np.random.uniform(0, 86400)
        stolen_amount = np.round(np.random.uniform(5000, 25000), 2)
        
        current_src = origin
        current_time = base_time
        
        for hop_idx, current_dst in enumerate(list(mules) + [exfil]):
            pass_through_delay = np.random.uniform(2.0, 25.0)  # Ultra-fast <30s sweep
            current_time += pass_through_delay
            
            # Micro-split or transfer 98% of funds (leaving 2% fee)
            hop_amount = np.round(stolen_amount * (0.98 ** (hop_idx + 1)), 2)
            
            G.add_edge(current_src, current_dst, amount=hop_amount, timestamp=current_time)
            records.append({
                "transaction_id": f"TX_MULE_RING{ring_idx}_{tx_id_counter:06d}",
                "sender_account": current_src,
                "receiver_account": current_dst,
                "amount": hop_amount,
                "timestamp_sec": current_time,
                "pass_through_delay_sec": pass_through_delay,
                "is_fraud": 1,
                "attack_vector": "multi_hop_ai_mule_network"
            })
            tx_id_counter += 1
            current_src = current_dst
            
    df_tx = pd.DataFrame(records)
    
    # 3. Compute Graph Topological Features
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    
    df_tx["sender_in_degree"] = df_tx["sender_account"].map(in_degrees)
    df_tx["sender_out_degree"] = df_tx["sender_account"].map(out_degrees)
    df_tx["receiver_in_degree"] = df_tx["receiver_account"].map(in_degrees)
    df_tx["receiver_out_degree"] = df_tx["receiver_account"].map(out_degrees)
    
    # Compute high-risk funnel score feature (high in-degree AND out-degree balance)
    df_tx["receiver_mule_funnel_score"] = np.minimum(
        df_tx["receiver_in_degree"], df_tx["receiver_out_degree"]
    )
    
    return df_tx

if __name__ == "__main__":
    df_mules = generate_money_mule_graph(num_users=50, num_mule_rings=2)
    print(f"Generated {len(df_mules)} graph transactions.")
    print(df_mules.tail())
