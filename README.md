# Mastercard Innovation Challenge 2026 — GenAI Payment Fraud Defense

A closed-loop, AI-powered attack simulation and defense system for detecting GenAI-enabled payment fraud vectors on Mastercard's network.

## Project Structure

```
master/
├── docs/                          # Research & documentation
│   ├── identify.md                # Pillar 1: Threat landscape & attack vector taxonomy
│   ├── generate.md                # Pillar 2: Synthetic attack engine documentation
│   └── defend.md                  # Pillar 3: Blue Team defense engine documentation
├── generate/                      # Step 2: Red Team Synthetic Attack Engine
│   ├── generator_text.py          # Vector 1: Prompt injection payloads (Groq Llama 3.3 70B)
│   ├── generator_tabular.py       # Vector 5: Evasive card testing micro-bursts
│   ├── generator_graph.py         # Vector 2: Multi-hop money mule networks (NetworkX)
│   ├── generator_evasion.py       # Vector 8: Adversarial decision-boundary perturbations
│   ├── domain_validator.py        # Financial domain constraint checker
│   ├── fidelity_eval.py           # Wasserstein, KS-test, TSTR (IEEE-CIS benchmark)
│   └── run_pipeline.py            # End-to-end generation pipeline
├── defend/                        # Step 3: Blue Team Defense Engine
│   ├── detector_tabular.py        # XGBoost + Isolation Forest (ONNX export, sub-50ms)
│   ├── detector_text.py           # Sentence Transformers vs TF-IDF baseline
│   ├── detector_graph.py          # GBDT money mule network classifier
│   ├── explainability.py          # PCI-DSS SHAP feature attributions
│   ├── cost_optimizer.py          # Amount-proportional financial loss threshold tuning
│   ├── data_splitter.py           # 60/20/20 train/val/Step 4 holdout manager
│   └── run_defend_pipeline.py     # End-to-end defense pipeline
├── data/
│   ├── synthetic/                 # Generated attack datasets & fidelity reports
│   └── defend/                    # Trained model metrics & Step 4 holdout sets
└── mastercard-challenge-guide.md  # Competition guide & roadmap
```

## Quick Start

### 1. Setup Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 3. Run Step 2: Generate Synthetic Attacks

```bash
python -m generate.run_pipeline
```

Outputs synthetic attack datasets to `data/synthetic/` and computes TSTR fidelity benchmark against IEEE-CIS real transaction data.

### 4. Run Step 3: Train Blue Team Defenders

```bash
python -m defend.run_defend_pipeline
```

Trains all 3 detector models, exports ONNX for sub-50ms authorization, benchmarks Sentence Transformers vs TF-IDF on paraphrased attacks, and exports `data/defend/metrics_report.json`.

## Key Technical Highlights

- **Authentic TSTR Benchmark:** Train on Synthetic, Test on Real using 20,000 IEEE-CIS credit card transactions (not synthetic-vs-synthetic).
- **Sub-50ms ONNX Inference:** XGBoost card testing model exported to ONNX Runtime, benchmarked at <1ms per transaction authorization.
- **Semantic Embedding Detection:** `all-MiniLM-L6-v2` Sentence Transformers catch paraphrased prompt injections that TF-IDF misses.
- **Amount-Proportional Cost Optimization:** Decision thresholds tuned against real transaction dollar amounts, not flat penalties.
- **PCI-DSS SHAP Explainability:** TreeSHAP feature attributions for regulatory interpretability compliance.
- **Class Imbalance Handling:** `scale_pos_weight` (XGBoost) and `class_weight='balanced'` (GBDT/LogReg) across all classifiers.

## License

This project was developed for the Mastercard Innovation Challenge 2026.
