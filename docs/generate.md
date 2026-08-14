# Mastercard Innovation Challenge 2026 — Pillar 2: Synthetic Attack Simulation

**Project Phase:** Pillar 2 — Generate  
**Focus:** High-fidelity simulation of GenAI-powered payment fraud across 4 selected vectors  
**Primary Goal:** Build scalable, realistic synthetic data generators and evaluate dataset fidelity using domain constraints, Wasserstein Distance, and TSTR (Train on Synthetic, Test on Real) metrics.

---

## 1. Overview of Generator Engine (`/generate/`)

The synthetic simulation engine generates datasets across 4 distinct attack modalities:

| Generator Script | Target Attack Vector | Technology / Strategy | Output Artifact |
|---|---|---|---|
| [`generator_tabular.py`](file:///Users/abuzaid/Desktop/final/master/generate/generator_tabular.py) | **Vector 5: Evasive Card Testing** | Log-normal spending baseline + CTGAN/micro-burst sampler | `synthetic_tabular_card_testing.csv` |
| [`generator_text.py`](file:///Users/abuzaid/Desktop/final/master/generate/generator_text.py) | **Vector 1: Indirect Prompt Injection** | Groq API (`llama-3.1-8b-instant`) / Template Fallback | `synthetic_prompt_injections.csv` |
| [`generator_graph.py`](file:///Users/abuzaid/Desktop/final/master/generate/generator_graph.py) | **Vector 2: AI Money Mule Networks** | `NetworkX` Graph Topology + Fast Pass-Through Sweeps | `synthetic_mule_graph.csv` |
| [`generator_evasion.py`](file:///Users/abuzaid/Desktop/final/master/generate/generator_evasion.py) | **Vector 8: Pattern Evasion** | Decision-boundary feature perturbers & amount structuring | `synthetic_evasion_patterns.csv` |

---

## 2. Domain Validation & Quality Assurance

All synthetic data passes through [`domain_validator.py`](file:///Users/abuzaid/Desktop/final/master/generate/domain_validator.py) to guarantee payment logic compliance:

1. **Positive Amounts Rule:** `amount > 0` across all transaction records.
2. **Merchant Category Code Validity:** Valid 4-digit numeric MCC (`1000 <= MCC <= 9999`).
3. **Timestamp Monotonicity:** Non-decreasing chronological timestamps per user.
4. **Balance Accounting:** `new_balance == old_balance - amount` (when balance fields are present).

---

## 3. Statistical & Utility Fidelity Suite

Dataset fidelity is benchmarked via [`fidelity_eval.py`](file:///Users/abuzaid/Desktop/final/master/generate/fidelity_eval.py) across three dimensions:

* **Wasserstein Distance:** Measures continuous distribution distance between real baseline data and synthetic samples.
* **Kolmogorov-Smirnov (KS) Test:** Evaluates marginal probability distribution alignment.
* **TSTR (Train on Synthetic, Test on Real) Score:** A Random Forest classifier is trained exclusively on synthetic data and evaluated on held-out real data. High AUC-PR proves that the synthetic dataset retains genuine predictive fraud utility.

---

## 4. Execution Command

To run the full Step 2 generation pipeline and export all datasets & fidelity reports:

```bash
python -m generate.run_pipeline
```
