"""
Vector 2 Generator: Multi-Topology AI Money Mule Network Layering
Generates synthetic transaction graph networks with NetworkX simulating 4 distinct money laundering topologies:
1. Linear Chain Layering (Origin -> Mule 1 -> Mule 2 -> Mule 3 -> Exfil)
2. Fan-Out Dispersal (1 Source -> Multiple Mules in parallel)
3. Smurfing / Structuring (1 Source -> Many micro-deposits < $250 to evade thresholds)
4. Round-Trip Wash Cycle (Circular loop A -> B -> C -> A)

Computes enterprise topological graph features:
- amount, pass_through_delay_sec
- sender_in_degree, sender_out_degree
- receiver_in_degree, receiver_out_degree
- receiver_mule_funnel_score
"""

import numpy as np
import pandas as pd
import networkx as nx
from typing import Dict, Any, Tuple

GRAPH_FEATURE_COLS = [
    "amount",
    "pass_through_delay_sec",
    "sender_in_degree",
    "sender_out_degree",
    "receiver_in_degree",
    "receiver_out_degree",
    "receiver_mule_funnel_score"
]


def generate_money_mule_graph(
    num_users: int = 1000,
    num_mule_rings: int = 100,
    ring_depth: int = 4,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generates synthetic payment transfer network with embedded multi-topology money mule rings
    and hard-negative fast legitimate business/P2P transfers.
    """
    np.random.seed(random_seed)
    
    G = nx.DiGraph()
    users = [f"ACC_{i:05d}" for i in range(num_users)]
    for u in users:
        G.add_node(u)
        
    records = []
    tx_id_counter = 0
    
    # ── 1. Generate Organic Legitimate Customer Transfers ──
    num_normal_tx = num_users * 5
    for _ in range(num_normal_tx):
        src, dst = np.random.choice(users, size=2, replace=False)
        amount = np.round(np.random.lognormal(mean=4.2, sigma=0.9), 2)
        timestamp = np.random.uniform(0, 86400 * 5)
        
        G.add_edge(src, dst, amount=amount, timestamp=timestamp)
        records.append({
            "transaction_id": f"TX_GRAPH_{tx_id_counter:06d}",
            "sender_account": src,
            "receiver_account": dst,
            "amount": amount,
            "timestamp_sec": timestamp,
            "pass_through_delay_sec": np.random.uniform(3600, 86400 * 3),  # Hours/days hold
            "is_fraud": 0,
            "attack_vector": "legitimate_transfer",
            "mule_topology": "organic_commerce"
        })
        tx_id_counter += 1
        
    # ── 2. Inject Multi-Topology Synthetic Money Mule Networks ──
    # Allocate rings across 4 topologies:
    # 1. Linear Chain (35%)
    # 2. Fan-Out Dispersal (25%)
    # 3. Smurfing / Structuring (25%)
    # 4. Round-Trip Wash Cycle (15%)
    
    n_linear = int(num_mule_rings * 0.35)
    n_fanout = int(num_mule_rings * 0.25)
    n_smurf = int(num_mule_rings * 0.25)
    n_roundtrip = num_mule_rings - (n_linear + n_fanout + n_smurf)
    
    # Topology 1: Linear Chain Layering (Origin -> Mule 1 -> ... -> Exfil)
    for ring_idx in range(n_linear):
        ring_users = np.random.choice(users, size=ring_depth + 2, replace=False)
        origin = ring_users[0]
        exfil = ring_users[-1]
        mules = ring_users[1:-1]
        
        base_time = np.random.uniform(0, 86400 * 4)
        stolen_amount = np.round(np.random.uniform(8000, 45000), 2)
        
        current_src = origin
        current_time = base_time
        
        for hop_idx, current_dst in enumerate(list(mules) + [exfil]):
            pass_through_delay = np.random.uniform(2.0, 25.0)  # Rapid < 30s pass-through
            current_time += pass_through_delay
            hop_amount = np.round(stolen_amount * (0.975 ** (hop_idx + 1)), 2)
            
            G.add_edge(current_src, current_dst, amount=hop_amount, timestamp=current_time)
            records.append({
                "transaction_id": f"TX_MULE_LIN_{ring_idx}_{tx_id_counter:06d}",
                "sender_account": current_src,
                "receiver_account": current_dst,
                "amount": hop_amount,
                "timestamp_sec": current_time,
                "pass_through_delay_sec": pass_through_delay,
                "is_fraud": 1,
                "attack_vector": "multi_hop_ai_mule_network",
                "mule_topology": "linear_chain"
            })
            tx_id_counter += 1
            current_src = current_dst

    # Topology 2: Fan-Out Dispersal (1 Source -> Multiple Mules in parallel)
    for ring_idx in range(n_fanout):
        fanout_size = np.random.randint(4, 9)
        ring_users = np.random.choice(users, size=fanout_size + 1, replace=False)
        origin = ring_users[0]
        mule_recipients = ring_users[1:]
        
        base_time = np.random.uniform(0, 86400 * 4)
        total_stolen = np.round(np.random.uniform(15000, 60000), 2)
        split_amount = np.round(total_stolen / fanout_size, 2)
        
        for mule_idx, mule in enumerate(mule_recipients):
            jitter = np.random.uniform(1.0, 30.0)
            tx_time = base_time + jitter
            pass_through_delay = np.random.uniform(5.0, 35.0)
            
            G.add_edge(origin, mule, amount=split_amount, timestamp=tx_time)
            records.append({
                "transaction_id": f"TX_MULE_FAN_{ring_idx}_{tx_id_counter:06d}",
                "sender_account": origin,
                "receiver_account": mule,
                "amount": split_amount,
                "timestamp_sec": tx_time,
                "pass_through_delay_sec": pass_through_delay,
                "is_fraud": 1,
                "attack_vector": "multi_hop_ai_mule_network",
                "mule_topology": "fan_out"
            })
            tx_id_counter += 1

    # Topology 3: Smurfing / Structuring (1 Source -> Many micro-deposits < $250)
    for ring_idx in range(n_smurf):
        smurf_count = np.random.randint(8, 16)
        ring_users = np.random.choice(users, size=smurf_count + 1, replace=False)
        origin = ring_users[0]
        smurf_recipients = ring_users[1:]
        
        base_time = np.random.uniform(0, 86400 * 4)
        for s_idx, smurf_acc in enumerate(smurf_recipients):
            micro_amt = np.round(np.random.uniform(75.0, 245.0), 2)  # Sub-threshold micro-amounts
            jitter = np.random.uniform(5.0, 180.0)
            tx_time = base_time + jitter
            delay = np.random.uniform(8.0, 45.0)
            
            G.add_edge(origin, smurf_acc, amount=micro_amt, timestamp=tx_time)
            records.append({
                "transaction_id": f"TX_MULE_SMURF_{ring_idx}_{tx_id_counter:06d}",
                "sender_account": origin,
                "receiver_account": smurf_acc,
                "amount": micro_amt,
                "timestamp_sec": tx_time,
                "pass_through_delay_sec": delay,
                "is_fraud": 1,
                "attack_vector": "multi_hop_ai_mule_network",
                "mule_topology": "smurfing_structuring"
            })
            tx_id_counter += 1

    # Topology 4: Round-Trip Wash Cycle (Circular Loop A -> B -> C -> D -> A)
    for ring_idx in range(n_roundtrip):
        cycle_len = np.random.randint(3, 6)
        cycle_nodes = list(np.random.choice(users, size=cycle_len, replace=False))
        cycle_nodes.append(cycle_nodes[0])  # Complete the circle
        
        base_time = np.random.uniform(0, 86400 * 4)
        wash_amount = np.round(np.random.uniform(6000, 32000), 2)
        current_time = base_time
        
        for c_idx in range(len(cycle_nodes) - 1):
            src_node = cycle_nodes[c_idx]
            dst_node = cycle_nodes[c_idx + 1]
            delay = np.random.uniform(15.0, 80.0)
            current_time += delay
            
            G.add_edge(src_node, dst_node, amount=wash_amount, timestamp=current_time)
            records.append({
                "transaction_id": f"TX_MULE_CYCLE_{ring_idx}_{tx_id_counter:06d}",
                "sender_account": src_node,
                "receiver_account": dst_node,
                "amount": wash_amount,
                "timestamp_sec": current_time,
                "pass_through_delay_sec": delay,
                "is_fraud": 1,
                "attack_vector": "multi_hop_ai_mule_network",
                "mule_topology": "round_trip_wash"
            })
            tx_id_counter += 1
            
    df_tx = pd.DataFrame(records)
    
    # ── 3. Inject Hard-Negative Fast Legitimate Transactions ──
    hard_neg_records = []
    num_hard_negatives = num_mule_rings * ring_depth * 4  # Scaled fast legitimate corporate & P2P
    for hn_idx in range(num_hard_negatives):
        src, dst = np.random.choice(users, size=2, replace=False)
        hn_type = np.random.choice(["instant_p2p", "payroll_batch", "merchant_settlement", "corporate_wire"])
        
        if hn_type == "instant_p2p":
            amount = np.round(np.random.uniform(5.0, 500.0), 2)
            delay = np.random.uniform(10.0, 90.0)
        elif hn_type == "payroll_batch":
            amount = np.round(np.random.uniform(1500.0, 8000.0), 2)
            delay = np.random.uniform(30.0, 120.0)
        elif hn_type == "corporate_wire":
            amount = np.round(np.random.uniform(5000.0, 30000.0), 2)
            delay = np.random.uniform(5.0, 45.0)
        else:  # merchant_settlement
            amount = np.round(np.random.uniform(200.0, 5000.0), 2)
            delay = np.random.uniform(15.0, 60.0)
            
        timestamp = np.random.uniform(0, 86400 * 5)
        G.add_edge(src, dst, amount=amount, timestamp=timestamp)
        hard_neg_records.append({
            "transaction_id": f"TX_HARDNEG_{tx_id_counter:06d}",
            "sender_account": src,
            "receiver_account": dst,
            "amount": amount,
            "timestamp_sec": timestamp,
            "pass_through_delay_sec": delay,
            "is_fraud": 0,
            "attack_vector": f"legitimate_{hn_type}",
            "mule_topology": "legitimate_hard_negative"
        })
        tx_id_counter += 1
    
    df_hard_neg = pd.DataFrame(hard_neg_records)
    df_tx = pd.concat([df_tx, df_hard_neg], ignore_index=True)
    
    # ── 4. Compute Graph Topological Features ──
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    
    df_tx["sender_in_degree"] = df_tx["sender_account"].map(in_degrees).fillna(0).astype(int)
    df_tx["sender_out_degree"] = df_tx["sender_account"].map(out_degrees).fillna(0).astype(int)
    df_tx["receiver_in_degree"] = df_tx["receiver_account"].map(in_degrees).fillna(0).astype(int)
    df_tx["receiver_out_degree"] = df_tx["receiver_account"].map(out_degrees).fillna(0).astype(int)
    
    # Compute high-risk funnel score feature (high in-degree AND out-degree balance)
    df_tx["receiver_mule_funnel_score"] = np.minimum(
        df_tx["receiver_in_degree"], df_tx["receiver_out_degree"]
    )
    
    df_tx = df_tx.sort_values("timestamp_sec").reset_index(drop=True)
    return df_tx


if __name__ == "__main__":
    df_mules = generate_money_mule_graph(num_users=1000, num_mule_rings=100, ring_depth=4)
    print(f"Generated {len(df_mules)} graph transactions.")
    print(f"Fraud count: {(df_mules['is_fraud'] == 1).sum()} / {len(df_mules)}")
    print("Mule topology breakdown:")
    print(df_mules["mule_topology"].value_counts())
    print(df_mules.head())
