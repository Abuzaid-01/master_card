# Defend and learn: detector suite

The defense layer trains one model per signal lane and evaluates an offline adversarial retraining loop. The system detects synthetic telemetry and emits recommended controls; it does not execute a card block, account freeze, authentication challenge, or wire intercept.

## Detector heads

| Module | Model | Inputs | Saved artifact |
| --- | --- | --- | --- |
| [`detector_tabular.py`](../defend/detector_tabular.py) | XGBoost classifier with an Isolation Forest component and ONNX export | 10 transaction features | `card_testing_xgb.joblib`, `card_testing_xgb.onnx` |
| [`detector_text.py`](../defend/detector_text.py) | Sentence Transformer embeddings with a calibrated classifier; TF-IDF fallback/baseline | prompt text | `text_detector.joblib` |
| [`detector_graph.py`](../defend/detector_graph.py) | `HistGradientBoostingClassifier` | transfer and local graph-topology features | `graph_detector.joblib` |

The hosted API intentionally defaults to TF-IDF text inference to fit its memory budget. Semantic inference can be enabled with `SENTRIX_ENABLE_SEMANTIC_MODEL=true` on an appropriately sized runtime.

## Offline training

After generating data, run:

```bash
python -m defend.run_defend_pipeline
```

The pipeline:

1. Loads the generated text, transaction, and graph datasets.
2. Creates 60% training, 20% validation, and 20% Step-4 holdout slices.
3. Trains and saves all three detectors.
4. Exports and benchmarks the transaction ONNX model.
5. Compares semantic and TF-IDF text performance, including 15 hand-written paraphrase probes.
6. Tunes an amount-sensitive transaction threshold.
7. records XGBoost feature attribution.
8. Writes `data/defend/metrics_report.json`.

## Checked-in baseline metrics

| Lane | AUC-PR | F1 | Additional result |
| --- | ---: | ---: | --- |
| Transaction | 1.0000 | 1.0000 | FPR 0.0000; recorded ONNX latency 0.008 ms |
| Text semantic | 0.9996 | — | paraphrase AUC-PR 0.9877 versus TF-IDF 0.8965 |
| Graph | 0.9455 | 0.8727 | topology-feature classifier |

These metrics come from the checked-in experiment and are dominated by generated data. They should be presented with the fidelity report and sample counts, not as production accuracy or an SLA guarantee.

## Cost and explanation outputs

[`cost_optimizer.py`](../defend/cost_optimizer.py) sweeps decision thresholds using false-negative transaction value and a configurable false-positive friction cost. The checked-in run selected `0.21` and reported `$3,060.79` lower modeled batch loss than threshold `0.50`. This is a scenario-specific simulated cost, not expected bank savings.

[`explainability.py`](../defend/explainability.py) records global feature importance and a local contribution example. The API uses native XGBoost contribution values for transaction explanations. These outputs support model inspection; they do not by themselves establish PCI-DSS, FCRA, or other regulatory compliance.

## Offline closed loop

Run:

```bash
python -m loop.run_closed_loop
```

The loop divides the Step-4 holdout into blind-spot-mining and final-evaluation portions, perturbs mining fraud against Round 1, adds successful evasions to the original training data, trains Round 2, and compares both rounds on independently perturbed evaluation fraud.

Checked-in catch-rate changes:

| Lane | Round 1 | Round 2 | Fraud samples in evaluation |
| --- | ---: | ---: | ---: |
| Transaction | 69.07% | 96.27% | 750 |
| Graph | 28.57% | 82.86% | 70 |
| Text | 0.00% | 100.00% | 38 |

See [`closed_loop_report.json`](../data/loop/closed_loop_report.json) for thresholds, AUC-PR changes, added sample counts, and baseline stability checks. The text result is especially sensitive to its small evaluation set and the chosen wrapping attack.

## Interactive pipeline evaluation

The web wizard uses [`api/pipeline_runner.py`](../api/pipeline_runner.py) and a separate 60/20/10/10 split. Fraud generator families are isolated across partitions; legitimate records are time-ordered where possible. Mining data selects retraining samples, while the evaluation partition remains untouched until the Round-1/Round-2 comparison.

The interactive learning loop currently supports text and transaction detectors. Graph retraining is part of the offline loop.

## Limitations

- Checked-in serialized models require compatible dependency versions; mismatches can produce scikit-learn warnings or unreliable loading.
- Perfect synthetic transaction metrics indicate separable generator rules and should not be generalized to real traffic.
- Thresholds are tuned on prototype validation data.
- Current adversarial strategies are heuristic, not gradient-based attacks.
- No persistence, approval workflow, audit store, access control, or payment-rail integration is implemented.
