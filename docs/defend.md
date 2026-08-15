# Mastercard Innovation Challenge 2026 — Pillar 3: Blue Team Defense Engine

**Project Phase:** Pillar 3 — Defend  
**Focus:** Multi-modal machine learning detection suite, ONNX sub-50ms inline authorization, Sentence Transformer semantic embeddings, PCI-DSS SHAP interpretability, and amount-proportional cost optimization.  
**Primary Goal:** Train high-performance Blue Team classifiers on Step 2 synthetic attack datasets, evaluate metrics (AUC-PR, F1, latency), and preserve clean holdout datasets for Step 4 (Closing the Loop).

---

## 1. Blue Team Architecture Overview (`/defend/`)

The Blue Team Defense Engine ingests exported synthetic attack datasets from `data/synthetic/*.csv` and trains specialized classifiers across all 4 attack modalities:

| Detector Module | Target Attack Modality | Architecture / Algorithm | Key Feature | Output Artifact |
|---|---|---|---|---|
| [`detector_tabular.py`](file:///Users/abuzaid/Desktop/final/master/defend/detector_tabular.py) | **Vector 5 & 8: Card Testing & Pattern Evasion** | **ONNX-Quantized XGBoost** (`scale_pos_weight`) + Isolation Forest | Sub-50ms inline transaction authorization latency | `card_testing_xgb.onnx` |
| [`detector_text.py`](file:///Users/abuzaid/Desktop/final/master/defend/detector_text.py) | **Vector 1: Indirect Prompt Injection** | **Sentence Transformers** (`all-MiniLM-L6-v2`) vs TF-IDF Baseline | Catches paraphrased prompt injections | `text_semantic_detector.joblib` |
| [`detector_graph.py`](file:///Users/abuzaid/Desktop/final/master/defend/detector_graph.py) | **Vector 2: Money Mule Networks** | **GBDT** (`class_weight='balanced'`) on NetworkX Topology | Identifies $<30\text{s}$ pass-through money sweeps | `graph_detector.joblib` |
| [`explainability.py`](file:///Users/abuzaid/Desktop/final/master/defend/explainability.py) | **PCI-DSS Compliance** | **TreeSHAP / Feature Attribution** | Feature importance & waterfall attributions | Included in `metrics_report.json` |
| [`cost_optimizer.py`](file:///Users/abuzaid/Desktop/final/master/defend/cost_optimizer.py) | **Financial Risk Management** | **Amount-Proportional Loss Matrix** | Finds optimal threshold $\tau^*$ minimizing dollar loss | Included in `metrics_report.json` |
| [`data_splitter.py`](file:///Users/abuzaid/Desktop/final/master/defend/data_splitter.py) | **Step 4 Holdout Manager** | **60% Train / 20% Val / 20% Holdout Split** | Preserves clean holdout data for Step 4 | `step4_holdout_*.csv` |

---

## 2. Technical Defense Upgrades

### A. Sub-50ms Inline Authorization Latency (ONNX Runtime)
Real-time card network authorization requires sub-50ms decision latency. The tabular card testing classifier is exported to **ONNX runtime format** (`card_testing_xgb.onnx`) and benchmarked for single-record inference latency.

### B. Semantic Sentence Embeddings vs. TF-IDF Baseline
Attackers paraphrase prompt injections to dodge word-frequency filters. Our text detector extracts 384-dimensional dense semantic embeddings using `sentence-transformers/all-MiniLM-L6-v2` and calculates cosine similarity to known attack clusters, benchmarking performance against a traditional TF-IDF baseline.

### C. Amount-Proportional Financial Cost Optimization
Rather than assuming flat fraud penalties, decision thresholds $\tau \in [0.01, 0.99]$ are tuned against an amount-proportional loss function:
$$\text{Total Cost}(\tau) = \sum_{i \in \text{FN}(\tau)} \left( \text{Amount}_i \times 1.2 \right) + \sum_{j \in \text{FP}(\tau)} \$15.00$$

### D. Class Imbalance Handling
To prevent classifiers from biasing toward majority legitimate transactions, `scale_pos_weight` is set dynamically in XGBoost and `class_weight='balanced'` is enforced across all models.

---

## 3. Data Splitting & Step 4 Holdout Strategy

All synthetic datasets are split via [`data_splitter.py`](file:///Users/abuzaid/Desktop/final/master/defend/data_splitter.py):
- **60% Training Set:** Used for model fitting.
- **20% Validation Set:** Used for threshold tuning, ONNX latency benchmarking, and SHAP calculations.
- **20% Step 4 Holdout Set:** Saved to `data/defend/step4_holdout_*.csv` and kept completely un-contaminated to evaluate round-over-round detector gains in Step 4.

---

## 4. Execution Command

To train all Blue Team classifiers, run cost optimization, compute SHAP attributions, and export `data/defend/metrics_report.json`:

```bash
./venv/bin/python3 -m defend.run_defend_pipeline
```
