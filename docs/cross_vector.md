# Cross-vector campaign simulation and fusion

SENTRIX demonstrates why weak signals from separate payment systems can become important when they occur in one coordinated campaign.

## Demonstrated campaign

```text
Phase 1: suspicious instruction sent to a banking assistant
   ↓ same synthetic target account and short scenario timeline
Phase 2: card-testing micro-burst followed by a larger drain
   ↓ synthetic recipient links
Phase 3: rapid multi-hop or fan-out mule routing
```

[`generator_cross_vector.py`](../generate/generator_cross_vector.py) contains four curated templates. A generated scenario includes prompt text, transaction records, mule hops, a target account, and timing fields. Repeated generation adds seeded numeric variation but does not invent new campaign structures.

## Scoring

[`cross_vector_fusion.py`](../defend/cross_vector_fusion.py) scores each phase with the corresponding saved model:

- Text: semantic detector when explicitly enabled, otherwise the TF-IDF deployment fallback.
- Transaction: maximum fraud probability among the scenario's transaction records.
- Graph: a representative graph-feature vector derived from hop count and pass-through timing.

The current fused score is:

```text
joint = 1 - (1 - text_risk) × (1 - transaction_risk) × (1 - graph_risk)
fused = min(0.9999, joint + synergy)
```

`synergy` is a fixed `0.05` when both text and transaction risks are at least `0.5`.

This is a transparent heuristic. The component probabilities are not proven independent, and the fusion equation has not been calibrated against real linked payment campaigns.

## Policy output

| Fused score | Returned recommendation |
| ---: | --- |
| `>= 0.80` | `INSTANT_KILL_SWITCH_AND_FREEZE` |
| `>= 0.50` and `< 0.80` | `STEP_UP_2FA_AND_HOLD` |
| `< 0.50` | `ALLOW_AND_MONITOR` |

These strings are simulated policy recommendations. No token, card, account, transfer, or wire is modified by this repository. The returned `interception_timeline_ms` is a demonstration value, not an end-to-end measured settlement intervention.

## API usage

Generate and score one curated scenario:

```http
GET /api/simulate/cross_vector?scenario_id=0
```

Score a caller-provided scenario with the same schema:

```http
POST /api/simulate/cross_vector_evaluate
Content-Type: application/json
```

The browser's cross-vector sandbox uses these endpoints. The separate interactive learning wizard does not yet retrain all three detector heads as one campaign model: its `cross_vector` selection currently follows the transaction lane, while the offline closed-loop script retrains text, transaction, and graph detectors independently.

## Next architectural steps

1. Introduce a canonical event envelope with campaign, customer, account, device, merchant, beneficiary, and event-time identifiers.
2. Generate linked stage events from a broader campaign policy instead of four fixed templates.
3. Compute graph features from the full scenario graph rather than a representative aggregate row.
4. Calibrate fusion and thresholds using linked campaign and legitimate multi-channel sessions.
5. Retrain and evaluate all three heads plus fusion inside one leakage-resistant campaign split.
6. Replace action strings with a sandboxed policy adapter and auditable human-approval workflow.
