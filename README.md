# 🛡️ SENTRIX AI — Autonomous Tri-Vector Compound Fraud Defense Platform

> **They Attack, We Defend: An AI Security Engine That Simulates Next-Gen Scams and Trains Itself to Stop Them.**
> 
> *A self-healing, multi-modal artificial intelligence defense system designed to intercept compound GenAI-enabled financial fraud across Chatbot, Payment Gateway, and Interbank Mule Settlement layers.*

---

## 📑 Table of Contents
1. [Executive Summary & The Big Picture](#-executive-summary--the-big-picture)
2. [The Core Problem: Compound GenAI Fraud](#-the-core-problem-compound-genai-fraud)
3. [End-to-End System Architecture](#-end-to-end-system-architecture)
4. [Pillar 1: Threat Landscape & Taxonomy (Identify)](#-pillar-1-threat-landscape--taxonomy-identify)
5. [Pillar 2: AI Red Team Attack Simulation (Generate)](#-pillar-2-ai-red-team-attack-simulation-generate)
6. [Pillar 3: AI Blue Team Multi-Modal Defense Heads (Defend)](#-pillar-3-ai-blue-team-multi-modal-defense-heads-defend)
7. [Cross-Vector Neural Fusion & Autonomous Kill Switch](#-cross-vector-neural-fusion--autonomous-kill-switch)
8. [Pillar 4: Self-Healing Adversarial Active Learning (Closed Loop)](#-pillar-4-self-healing-adversarial-active-learning-closed-loop)
9. [Interactive Fullstack Web Dashboard](#-interactive-fullstack-web-dashboard)
10. [Repository Structure](#-repository-structure)
11. [Quick Start & Reproduction Guide](#-quick-start--reproduction-guide)
12. [Creator & Attribution](#-creator--attribution)

---

## 🌟 Executive Summary & The Big Picture

### What is SENTRIX AI?
**SENTRIX AI** is an enterprise-grade autonomous fraud defense platform that stops modern, coordinated cyber-attacks before money leaves the bank.

In traditional banking, fraud detection systems operate in **isolated silos**:
- The **Chatbot team** only checks for offensive text.
- The **Credit Card gateway** only checks single transaction amounts.
- The **Anti-Money Laundering (AML) team** only looks at account transfers days later.

**Hackers exploit these silos.** An attacker uses GenAI to trick the bank's support chatbot into disabling security alerts, uses an automated script to drain a stolen card through micro-bursts, and immediately launders the stolen funds across a complex web of money mule accounts.

**SENTRIX AI unifies these 3 layers into a single intelligent defense head:**
1. **Chatbot Infiltration Defense** (NLP Deep Learning / Sentence Transformers)
2. **Card Authorization Defense** (Quantized ONNX XGBoost + Isolation Forest Anomaly Engine)
3. **Money Mule Exfiltration Defense** (Graph Machine Learning & Network Topology Analysis)

```
┌────────────────────────────────────────────────────────────────────────┐
│                              SENTRIX AI                                │
│                     ATTACK → DEFEND → EVOLVE                           │
├───────────────────┬───────────────────────────┬────────────────────────┤
│   1. RED TEAM     │      2. BLUE TEAM         │    3. CLOSED LOOP      │
│  We simulate the  │  We intercept fraud in    │  The AI learns from    │
│  wildest attacks  │  real-time (<15ms SLA)    │  missed attacks 24/7   │
└───────────────────┴───────────────────────────┴────────────────────────┘
```

---

## 💥 The Core Problem: Compound GenAI Fraud

Modern financial fraud is no longer a single stolen card swipe. It is a **3-stage compound kill chain**:

```
[ Phase 1: Infiltration ]          [ Phase 2: Authorization ]          [ Phase 3: Exfiltration ]
 ┌──────────────────────┐           ┌──────────────────────┐           ┌──────────────────────┐
 │ AI Chatbot Phishing  │           │ Automated Bot Drain  │           │ Multi-Hop Mule Graph │
 │  & Prompt Injection  │ ────────> │ & Evasive Card Siphon│ ────────> │ & Smurfing Network   │
 │                      │           │                      │           │                      │
 │ "Bypass 2FA alerts"  │           │ 20 tx/min bot swipe  │           │ 4-hop wash cycles    │
 └──────────────────────┘           └──────────────────────┘           └──────────────────────┘
            │                                  │                                  │
            ▼                                  ▼                                  ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────┐
 │                               SENTRIX CROSS-VECTOR FUSION HEAD                             │
 │    Correlates individual low-risk signals into a 99.9% Critical Threat in 12.4 milliseconds│
 └────────────────────────────────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
                              🚨 INSTANT KILL SWITCH TRIGGERED:
                      Token Revoked · Card Blocked · Wire Intercepted
```

### Why Traditional Rule Engines Fail:
1. **Keyword Blocklists fail against LLM Paraphrasing**: Attackers use roleplay and subtle linguistic reframing that evade static keywords.
2. **Static Thresholds fail against Multi-Signal Evasion**: A bot making a $2,110 charge from a domestic IP looks safe on amount alone, but is lethal when combined with a velocity spike of 19.5 tx/min.
3. **Single-Account Watchlists fail against Mule Graphs**: Smurfing (splitting funds into $1,900 hops across 10 accounts) stays beneath traditional $10,000 regulatory reporting triggers.

---

## 🏗️ End-to-End System Architecture

```
                                  ┌──────────────────────────┐
                                  │   Incoming Event Stream  │
                                  └─────────────┬────────────┘
                                                │
                 ┌──────────────────────────────┼──────────────────────────────┐
                 │                              │                              │
                 ▼                              ▼                              ▼
     [ Text / Chatbot Stream ]     [ Tabular Transaction Stream ]   [ Interbank Transfer Graph ]
                 │                              │                              │
                 ▼                              ▼                              ▼
     ┌───────────────────────┐      ┌───────────────────────┐      ┌───────────────────────┐
     │  Phase 1 Text Head    │      │ Phase 2 Tabular Head  │      │  Phase 3 Graph Head   │
     │ SentenceTransformers  │      │ ONNX Quantized XGBoost│      │ HistGradientBoosting  │
     │  (all-MiniLM-L6-v2)   │      │   + Isolation Forest  │      │   Graph Topology ML   │
     │ Latency: <15 ms       │      │ Latency: 0.008 ms     │      │ Latency: <2 ms        │
     └───────────┬───────────┘      └───────────┬───────────┘      └───────────┬───────────┘
                 │ Risk: R_text                 │ Risk: R_tabular              │ Risk: R_graph
                 └──────────────────────┬───────┴──────────────────────────────┘
                                        │
                                        ▼
                 ┌─────────────────────────────────────────────┐
                 │        Cross-Vector Fusion Engine           │
                 │   R_joint = 1 - ∏(1 - R_i) + Synergy_Boost  │
                 └──────────────────────┬──────────────────────┘
                                        │
                                        ▼
                 ┌─────────────────────────────────────────────┐
                 │        Autonomous Decision Engine           │
                 │      Interception SLA: 12.4 ms (<50ms)      │
                 ├─────────────────────────────────────────────┤
                 │ • Risk ≥ 85%  → INSTANT KILL SWITCH & FREEZE│
                 │ • Risk ≥ 65%  → STEP-UP BIOMETRIC CHALLENGE │
                 │ • Risk ≥ 40%  → FLAG & THROTTLE VELOCITY    │
                 │ • Risk < 40%  → ALLOW & AUDIT TELEMETRY     │
                 └──────────────────────┬──────────────────────┘
                                        │
                         [ Evasion / Probing Telemetry ]
                                        │
                                        ▼
                 ┌─────────────────────────────────────────────┐
                 │    Step 4: Closed-Loop Active Learning      │
                 │  • Adversarial Multi-Strategy Prober        │
                 │  • Automated Dataset Augmentation           │
                 │  • Zero Catastrophic Forgetting Validation  │
                 └─────────────────────────────────────────────┘
```

---

## 🔍 Pillar 1: Threat Landscape & Taxonomy (Identify)

SENTRIX AI catalogs and defends against the **8 Core FinCEN & GenAI Attack Vectors**:

| # | Attack Vector | Mechanism | Real-World Impact | Severity |
|---|---|---|---|---|
| **V1** | **Indirect Prompt Injection** | Linguistic adversarial jailbreaks feeding malicious context into bank support LLMs | Unauthorized limit increases, suppressed 2FA alerts | **Critical** |
| **V2** | **Deepfake KYC Bypass** | Diffusion-generated synthetic identity documents and video stream spoofing | Opening unverified bank accounts at scale | **Critical** |
| **V3** | **AI Voice Clone Scams** | 3-second audio sample voice cloning of corporate executives | Authorizing high-value wire transfers | **Critical** |
| **V4** | **Synthetic Identity Fraud** | Generative creation of synthetic personas that survive bureau credit checks | Long-con credit line bust-outs | **High** |
| **V5** | **Evasive Card Testing** | Bot swarms executing micro-swipes ($1.25) before high-value account drains | Depleting compromised card balances | **High** |
| **V6** | **Multi-Hop Mule Networks** | Layered fund routing through smurfing, fan-out, and round-trip wash cycles | Exfiltrating stolen funds to offshore mixers | **High** |
| **V7** | **GenAI Merchant Fraud** | Automatically generated e-commerce storefronts created for chargeback bust-outs | Merchant acquiring chargeback losses | **Medium** |
| **V8** | **Adversarial Evasion** | Mathematical gradient perturbations masking fraud features beneath risk thresholds | Dodging machine learning decision boundaries | **High** |

---

## ⚡ Pillar 2: AI Red Team Attack Simulation (Generate)

To train robust defenders, SENTRIX AI generates **large-scale, authentic, mathematically verified synthetic datasets**:

### 1. Tabular Card Fraud Dataset (`50,000` rows)
Models realistic 3-tier consumer spending and 5 distinct fraud patterns:
* **Legitimate Spectrum**:
  - *Everyday Micro*: $2.50 – $65.00 (grocery, transit, dining)
  - *Standard Retail*: $65.00 – $450.00 (shopping, utilities)
  - *Major High-Value Commerce*: $450.00 – $4,200.00 (electronics, Apple Store, flights) on clean devices.
* **5 Fraud Patterns**:
  1. *Card Testing Burst*: Rapid micro-swipes ($0.50–$3.00) + high-value drain, elevated velocity (8–32 tx/min), device risk >75%.
  2. *Account Takeover (ATO)*: High dollar amounts ($500–$3,500), unrecognized new device (risk >78%), foreign proxy geolocation jump (3,000–6,800 km).
  3. *High-Velocity Bot Siphon*: Script velocity (8–35 tx/min) on spoofed residential proxy IPs.
  4. *Card-Not-Present (CNP)*: High-risk digital goods MCCs (5816, 7399) with elevated device risk.
  5. *Slow Drip Siphon*: Sub-radar recurring charges ($18–$85) spread across multiple days.

### 2. Text Prompt Injection Dataset (`1,500` prompts)
Covers **13 Threat Categories** generated via LLM prompt synthesis:
* *Deepfake Voice Pretexting*, *Compliance Officer Impersonation*, *Tool-Use Hijacking*, *Multi-Turn Context Poisoning*, *Social Engineering Urgency*, *Multilingual Evasion*, *Encoding Obfuscation (Base64/ROT13)*, and *Jailbreak Roleplay*.

### 3. Money Mule Graph Network (`7,297` transfers)
Generated using NetworkX across **1,000 accounts and 100 mule rings** spanning **4 AML topologies**:
1. *Linear Chains*: $A \to B \to C \to D \to \text{Offshore}$
2. *Fan-Out Dispersal*: 1 compromise account dispersing to 8 mule nodes simultaneously.
3. *Smurfing / Structuring*: Splitting large balances into sub-$2,000 chunks to evade AML alerts.
4. *Round-Trip Wash Cycles*: Circular fund routing to wash transaction provenance.

### 4. Mathematical Fidelity Verification (TSTR)
* **100% Domain Rule Pass Rate** across all physical and financial constraints (e.g. non-negative amounts, valid timestamps, probability bounds).
* **Train on Synthetic, Test on Real (TSTR)**: Validated against **20,000 real-world credit card transactions from the IEEE-CIS benchmark** dataset (`train_transaction.csv`).
* **Wasserstein & Kolmogorov-Smirnov Tests**: Verified statistical distribution alignment.

---

## 🛡️ Pillar 3: AI Blue Team Multi-Modal Defense Heads (Defend)

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                 DEFENSE BENCHMARK SUMMARY                                │
├─────────────────────────┬───────────────────────────┬──────────────┬─────────────────────┤
│ Model Head              │ Architecture              │ Metric       │ Performance         │
├─────────────────────────┼───────────────────────────┼──────────────┼─────────────────────┤
│ 💳 Phase 2: Card Fraud  │ Quantized ONNX XGBoost    │ AUC-PR / F1  │ 100.0% / 100.0%     │
│                         │ + Isolation Forest        │ Latency      │ 0.008 ms (8 µs)     │
├─────────────────────────┼───────────────────────────┼──────────────┼─────────────────────┤
│ 💬 Phase 1: Text Prompt │ SentenceTransformers      │ AUC-PR       │ 99.96%              │
│                         │ (all-MiniLM-L6-v2)        │ Paraphr. Lift│ +10.17% over TF-IDF │
├─────────────────────────┼───────────────────────────┼──────────────┼─────────────────────┤
│ 🕸️ Phase 3: Mule Graph  │ HistGradientBoosting GBDT │ AUC-PR / F1  │ 94.55% / 87.27%     │
├─────────────────────────┼───────────────────────────┼──────────────┼─────────────────────┤
│ 💰 Financial Optimizer  │ Cost-Sensitive Threshold  │ Cost Savings │ $3,060.79 per batch │
└─────────────────────────┴───────────────────────────┴──────────────┴─────────────────────┘
```

### 1. Sub-10 Microsecond ONNX Inference
The tabular XGBoost model is compiled down to **ONNX Runtime (C++ compiled inference)**:
* **Inference Speed**: **`0.008 ms`** (8 microseconds).
* **Compliance**: Over **6,000× faster** than the strict 50ms payment authorization SLA.

### 2. Semantic Embedding Lift vs. TF-IDF
Traditional keyword matchers fail when attackers rephrase prompts. SENTRIX AI benchmarks `all-MiniLM-L6-v2` dense 384-dimensional embeddings against TF-IDF n-gram baselines:
* **Paraphrased Attacks**: TF-IDF achieves `89.65%` AUC-PR $\to$ Semantic Embeddings achieve **`98.77%`** AUC-PR (**`+10.17% lift`**).

### 3. Financial Cost-Sensitive Optimization
Instead of assuming all errors have equal cost (treating a $5 error the same as a $5,000 error), SENTRIX AI minimizes the **Amount-Proportional Financial Loss Function**:
$$\mathcal{L}(\tau) = \sum_{i \in \text{FN}} \text{Amount}_i + \alpha \sum_{j \in \text{FP}} \text{Amount}_j$$
* **Optimal Threshold**: $\tau^* = 0.21$, reducing financial loss by **`$3,060.79`** per transaction batch compared to a naive $0.50$ threshold.

### 4. PCI-DSS Compliant SHAP Explainability
Every authorization prediction provides an exact local SHAP feature attribution breakdown:
* **Global Top Features**: `geo_distance_km` ($45.2\%$), `device_risk_score` ($23.6\%$), `velocity` ($16.2\%$), `mcc_risk_weight` ($6.9\%$).

---

## 🔀 Cross-Vector Neural Fusion & Autonomous Kill Switch

When an attack spans multiple channels, single-vector detectors might only see moderate risk. The **SENTRIX Cross-Vector Fusion Head** computes the joint probabilistic risk:

$$R_{\text{correlated}} = 1 - (1 - R_{\text{text}}) \times (1 - R_{\text{tabular}}) \times (1 - R_{\text{graph}}) + \text{Synergy Boost}$$

```
                                    CROSS-VECTOR DECISION MATRIX
┌──────────────────────┬──────────────────────┬──────────────────────┬──────────────────┬─────────────────────────────────┐
│ Phase 1: Text Prompt │ Phase 2: Card Swipes │ Phase 3: Mule Graph  │ Correlated Risk  │ Autonomous Enforcement Action   │
├──────────────────────┼──────────────────────┼──────────────────────┼──────────────────┼─────────────────────────────────┤
│ 🔴 Jailbreak (93.8%) │ 🔴 19.5 tx/min (99%) │ 🟢 Normal (0.02%)    │ 🚨 100.0% Risk   │ INSTANT_KILL_SWITCH_AND_FREEZE  │
│ 🟢 Safe Chat (16.6%) │ 🟢 $2,110 Clean (0%) │ 🟢 Normal (0.02%)    │ 🟢 16.6% Risk    │ ALLOW_AND_MONITOR               │
│ 🟢 Safe Chat (10.0%) │ 🔴 ATO Device (100%) │ 🟢 Normal (0.02%)    │ 🚨 100.0% Risk   │ INSTANT_KILL_SWITCH_AND_FREEZE  │
│ 🟢 Safe Chat (10.0%) │ 🟢 Legit $85 (0.1%)  │ 🔴 Smurfing (98.2%)  │ 🚨 98.4% Risk    │ FREEZE_INTERBANK_WIRE_SETTLEMENT│
└──────────────────────┴──────────────────────┴──────────────────────┴──────────────────┴─────────────────────────────────┘
```

**Autonomous Enforcement SLA**: Interception timeline executes in **`12.4 ms`**, freezing funds before ACH or interbank wire settlement completes.

---

## 🔄 Pillar 4: Self-Healing Adversarial Active Learning (Closed Loop)

In Step 4, SENTRIX AI acts as its own Red Team by unleashing an **Adversarial Multi-Strategy Prober** against its own models:
1. **Velocity Dilution**: Attackers slow down transaction speed to stay under radar.
2. **Amount Structuring**: Attackers split amounts into small increments ($1.25–$2.50).
3. **Device Spoofing**: Attackers cycle user agents and residential proxy IPs.

```
                              STEP 4 ACTIVE LEARNING RETRAINING RESULTS
┌──────────────────────────────────────┬─────────────┬─────────────┬─────────────────────────────────┐
│ Evaluation Dimension                 │ Round 1     │ Round 2     │ Improvement / Lift              │
├──────────────────────────────────────┼─────────────┼─────────────┼─────────────────────────────────┤
│ 💳 Tabular Evasion Catch Rate        │ 518 / 750   │ 722 / 750   │ +204 caught (+27.2% lift)       │
│ 💳 Tabular Adversarial AUC-PR        │ 0.9845      │ 0.9997      │ +0.0152                         │
├──────────────────────────────────────┼─────────────┼─────────────┼─────────────────────────────────┤
│ 💬 Text Paraphrased Catch Rate       │ 0 / 38      │ 38 / 38     │ +38 caught (+100.0% lift)       │
│ 💬 Text Adversarial AUC-PR           │ 0.2517      │ 1.0000      │ +0.7483                         │
├──────────────────────────────────────┼─────────────┼─────────────┼─────────────────────────────────┤
│ 🕸️ Graph Mule Topology Catch Rate   │ 20 / 70     │ 58 / 70     │ +38 caught (+54.3% lift)        │
│ 🕸️ Graph Adversarial AUC-PR          │ 0.6107      │ 0.9208      │ +0.3101                         │
├──────────────────────────────────────┼─────────────┼─────────────┼─────────────────────────────────┤
│ 🛡️ Catastrophic Forgetting Drift     │ 0.00% FPR   │ 0.00% FPR   │ ZERO FORGETTING (0.00% Drift)   │
└──────────────────────────────────────┴─────────────┴─────────────┴─────────────────────────────────┘
```

---

## 💻 Interactive Fullstack Web Dashboard

The web platform is built with **React 19, TanStack Start & Router, TailwindCSS, Motion, and FastAPI**:

* **Overview & Hero**: Dynamic glitch animations, live counters, and high-impact security telemetry.
* **Identify**: Interactive cards cataloging all 8 attack vectors.
* **Generate**: Live Red Team pipeline terminal window and Wasserstein distance fidelity metrics.
* **Defend**: Interactive gauges for ONNX latency (0.008 ms), semantic lift (+10.17%), and cost optimization ($3,060.79).
* **Closed Loop**: Interactive Round 1 vs Round 2 active learning comparison matrix.
* **Live Demo & Sandbox**:
  - *Custom Cross-Vector Evaluator*: Real-time sliders for amount ($0.50–$5,000), velocity (0–30 tx/min), device risk, and custom prompt inputs.
  - *Live 6-Step Pipeline Wizard*: Trigger and monitor dataset generation, detector training, and closed-loop retraining in real time.

---

## 📁 Repository Structure

```
master/
├── api/
│   ├── main.py                    # FastAPI backend with dynamic timestamp-aware model loaders
│   └── pipeline_runner.py         # Subprocess runner for live web pipeline execution
├── data/
│   ├── synthetic/                 # 50k Tabular, 1.5k Text, 7.3k Graph synthetic datasets
│   ├── defend/                    # metrics_report.json & Step 4 holdout data slices
│   └── loop/                      # closed_loop_report.json (Round 1 vs Round 2 benchmark)
├── defend/
│   ├── models/                    # Exported card_testing_xgb.onnx, joblib model binaries
│   ├── cross_vector_fusion.py     # Cross-vector neural correlation & kill switch logic
│   ├── detector_tabular.py        # XGBoost + Isolation Forest ONNX exporter
│   ├── detector_text.py           # SentenceTransformers semantic prompt detector
│   ├── detector_graph.py          # HistGradientBoosting AML mule network detector
│   ├── cost_optimizer.py          # Amount-proportional financial threshold optimization
│   ├── explainability.py          # TreeSHAP feature attribution module
│   └── run_defend_pipeline.py     # Blue Team defense training pipeline
├── generate/
│   ├── generator_tabular.py       # 50,000 row multi-pattern tabular card generator
│   ├── generator_text.py          # 1,500 prompt 13-category injection generator
│   ├── generator_graph.py         # 7,297 transfer 4-topology mule graph generator
│   ├── generator_cross_vector.py  # 100 multi-stage compound attack scenarios
│   ├── domain_validator.py        # Financial rule checker (100% pass rate)
│   ├── fidelity_eval.py           # Wasserstein, KS-test, and TSTR benchmarks
│   └── run_pipeline.py            # Red Team synthetic attack pipeline
├── loop/
│   ├── multi_strategy_prober.py   # Adversarial evasion generator
│   ├── loop_retrainer.py          # Calibrated Round 2 retraining engine
│   ├── loop_evaluator.py          # R1 vs R2 holdout evaluator & forgetting checker
│   └── run_closed_loop.py         # Step 4 active learning pipeline
├── frontend/                      # React 19 / TanStack Start web application
│   ├── public/                    # Favicons, SVGs, and sentrix_logo.png
│   ├── src/
│   │   ├── components/sections/   # Hero, Identify, Generate, Defend, ClosedLoop, CrossVectorPanel
│   │   ├── components/shared/     # SentrixMark, Counter, GaugeRing, StickyNav
│   │   ├── hooks/                 # React Query hooks for real-time backend API integration
│   │   └── data/content.ts        # Dynamic content and metric definitions
│   └── package.json
└── README.md                      # Complete project documentation
```

---

## 🚀 Quick Start & Reproduction Guide

### Prerequisites
* Python 3.11+
* Node.js 20+ & npm

### 1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/Abuzaid-01/master_card.git
cd master_card

# Create and activate Python virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Run the End-to-End AI Pipelines
```bash
# Step 2: Generate 50,000 synthetic multi-pattern attacks & verify TSTR fidelity
./venv/bin/python generate/run_pipeline.py

# Step 3: Train Blue Team detectors, export ONNX, and optimize financial thresholds
./venv/bin/python defend/run_defend_pipeline.py

# Step 4: Run closed-loop active learning against adversarial evasion holdouts
./venv/bin/python loop/run_closed_loop.py
```

### 3. Start the FastAPI Backend Server
```bash
./venv/bin/uvicorn api.main:app --port 8000 --host 0.0.0.0 --reload
```
* API Documentation / Swagger UI: `http://localhost:8000/docs`

### 4. Start the Frontend Dashboard
```bash
# In a new terminal window:
cd frontend
npm install
npm run dev
```
* Open your browser and navigate to: **`http://localhost:8080`**

---

## 👨‍💻 Creator & Attribution

**SENTRIX AI** was designed and developed by **Abuzaid**:

* **GitHub**: [https://github.com/Abuzaid-01/master_card](https://github.com/Abuzaid-01/master_card)
* **LinkedIn**: [https://www.linkedin.com/in/abuzaid01](https://www.linkedin.com/in/abuzaid01)

```
Made with ❤️ by Abuzaid
SENTRIX AI · Next-Generation Autonomous Fraud Intelligence Head
```
