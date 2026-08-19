# Cross-Vector Compound Fraud Defense: Architecture & Mathematical Formulation

## 1. Executive Summary & Threat Model
Traditional financial fraud systems treat security vectors in silos:
* The conversational AI / chatbot team monitors customer service transcripts.
* The payment gateway team monitors transaction authorization velocity.
* The anti-money laundering (AML) team monitors interbank wire transfers.

Modern cybercrime syndicates exploit these operational silos by executing **Cross-Vector Compound Attacks** across three sequential phases:

```
┌───────────────────────────────────────────────┐
│  Phase 1: Chatbot Infiltration                │
│  Target: Bank Virtual Assistant               │
│  Threat Vector: Indirect Prompt Injection     │
│  Goal: Suppress alerts / Exfiltrate 2FA token │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  Phase 2: Payment Gateway Testing & Drain     │
│  Target: Card Authorization Gateway           │
│  Threat Vector: Micro-Burst Card Testing      │
│  Goal: Validate CVV / Drain Card Limit ($)    │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  Phase 3: Interbank Exfiltration Layering     │
│  Target: Wire Transfer & Settlement Network   │
│  Threat Vector: Multi-Hop Money Mule Ring     │
│  Goal: Disperse funds to Crypto Off-Ramp      │
└───────────────────────────────────────────────┘
```

---

## 2. Multi-Model Defense Architecture

The **GenAI Fraud Shield** deploys three specialized machine learning models running in parallel across the transaction event stream:

| Attack Phase | Model Architecture | Primary Features | Inference SLA |
|---|---|---|---|
| **Phase 1 (Text)** | `SentenceTransformers (all-MiniLM-L6-v2)` + Calibrated Logistic Head (Platt Scaling) | 384-dimensional dense semantic vectors + TF-IDF n-grams | $<15\,\text{ms}$ |
| **Phase 2 (Tabular)** | Quantized 9-Feature XGBoost (`card_testing_xgb.onnx`) | `amount`, `velocity`, `device_risk_score`, `is_decline`, `hour_sin`, `hour_cos`, `mcc_risk_weight`, `geo_distance_km`, `card_age_days`, `failed_attempts_24h` | **$0.0056\,\text{ms}$** |
| **Phase 3 (Graph)** | `HistGradientBoostingClassifier` (Network Topology) | `pass_through_delay_sec`, `sender_in_degree`, `sender_out_degree`, `receiver_in_degree`, `receiver_out_degree`, `mule_funnel_score` | $<2\,\text{ms}$ |

---

## 3. Mathematical Risk Fusion Formulation

To compute the **Correlated Compound Risk Score** ($R_{\text{fused}}$), the system uses an independent failure probability fusion model augmented with temporal co-occurrence synergy:

### 3.1 Joint Probability Equation:
$$R_{\text{joint}} = 1 - \prod_{i \in \{\text{text}, \text{tabular}, \text{graph}\}} \big(1 - R_i\big)$$

Where:
* $R_{\text{text}} \in [0, 1]$ is the calibrated semantic probability of prompt injection.
* $R_{\text{tabular}} \in [0, 1]$ is the maximum transaction fraud probability across the burst window.
* $R_{\text{graph}} \in [0, 1]$ is the topological mule network probability.

### 3.2 Temporal Correlation & Synergy Boost:
If $R_{\text{text}} \ge \tau_{\text{text}}^*$ and $R_{\text{tabular}} \ge \tau_{\text{tabular}}^*$ within a co-occurrence window $\Delta t \le 300\,\text{seconds}$:
$$R_{\text{fused}} = \min\Big(0.9999, \; R_{\text{joint}} + \Delta_{\text{synergy}}\Big) \quad \text{where } \Delta_{\text{synergy}} = 0.05$$

---

## 4. Autonomous Mastercard Enforcement Decision Matrix

Based on the computed $R_{\text{fused}}$, the autonomous decision head executes policy rules in sub-second time:

| Fused Risk $R_{\text{fused}}$ | Severity | Automated Action | Business Impact |
|---|---|---|---|
| **$R_{\text{fused}} \ge 0.80$** | **CRITICAL** | **`INSTANT_KILL_SWITCH_AND_FREEZE`** | Immediate card token revocation, pending wire hold, and customer security alert. |
| **$0.50 \le R_{\text{fused}} < 0.80$** | **HIGH** | **`STEP_UP_2FA_AND_HOLD`** | Out-of-band biometric challenge required before transaction approval. |
| **$R_{\text{fused}} < 0.50$** | **LOW** | **`ALLOW_AND_MONITOR`** | Transaction approved with background telemetry auditing. |
