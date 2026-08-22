# Identify: GenAI-enabled payment-fraud landscape

This document defines the research scope behind SENTRIX AI. It separates the broader threat taxonomy from the vectors implemented in the prototype.

## Taxonomy

| Vector | Payment surface | GenAI or automation advantage | Observable signals | Prototype status |
| --- | --- | --- | --- | --- |
| Indirect prompt injection | Banking assistants and agentic support tools | Rephrases or hides instructions intended to alter tool behavior | override language, role impersonation, encoded instructions, anomalous tool intent | Generated and detected |
| Automated money-mule routing | Account-to-account and interbank transfers | Coordinates routing, timing, splitting, and account reuse | short pass-through delay, fan-out, cycles, degree and funnel anomalies | Generated and detected |
| Synthetic KYC bypass | Digital onboarding | Produces identity media and adapts to liveness challenges | virtual-camera telemetry, identity inconsistencies, device/location mismatch | Researched only |
| Voice-clone APP fraud | UPI, wire, and other push-payment flows | Scales convincing impersonation and interactive scripts | new beneficiary, unusual amount, call-to-transfer timing, device anomaly | Researched only |
| Evasive card testing | Merchant authorization endpoints | Varies cadence, merchant, device, and amount to avoid rules | micro-authorizations, decline clusters, velocity, device novelty, MCC risk | Generated and detected |
| Synthetic storefront fraud | Merchant acquiring and card-not-present commerce | Produces stores, catalogs, reviews, and support content cheaply | young merchant, sudden volume, fulfillment and chargeback anomalies | Researched only |
| GenAI-assisted BEC and invoice fraud | Corporate payables and wires | Reproduces vendor tone and documents, and supports live impersonation | beneficiary change, new routing details, anomalous communications | Researched only |
| Model-guided transaction evasion | Fraud-scoring boundaries | Uses feedback to search for lower-risk variants | repeated near-threshold attempts and coordinated feature changes | Simulated in the closed loop |

## Implemented scope

The executable system concentrates on four related vectors:

1. Prompt injection and conversational social engineering.
2. Card testing, account takeover, bot siphoning, card-not-present fraud, and slow-drip transaction patterns.
3. Mule-network chains, fan-out, smurfing, and circular routing.
4. Adversarial changes designed to expose detector blind spots.

The cross-vector demonstration combines the first three into a single synthetic campaign. The remaining taxonomy entries provide breadth for the Identify pillar but are not represented by trained media, identity, merchant, or voice models.

## Mapping from threat to data

| Signal lane | Generated fields | Defender |
| --- | --- | --- |
| Text | `prompt_text`, `attack_type`, `severity`, `is_fraud` | calibrated semantic or TF-IDF text classifier |
| Transaction | amount, velocity, device risk, decline flag, time encoding, MCC risk, geographic distance, card age, failed attempts | XGBoost classifier and ONNX export |
| Graph | amount, pass-through delay, sender/receiver degrees, receiver funnel score | histogram gradient-boosting classifier |

## Research basis

The taxonomy is informed by public material including:

- FinCEN Alert FIN-2024-Alert004 on fraud involving deepfake media.
- U.S. Treasury material on AI-specific financial-services risk.
- OWASP guidance on prompt injection and adversarial ML.
- FBI/IC3 and interagency guidance on impersonation, BEC, and synthetic media.
- Public payment-fraud descriptions covering card testing, authorized push-payment fraud, and money-mule networks.

These sources motivate the scenarios; they do not validate the synthetic distributions or make SENTRIX a regulatory-compliance system.

## Scope boundaries

- No real customer data or credentials are used.
- No payment instruction is sent to a financial institution.
- Deepfake, KYC, storefront, BEC, and voice vectors are research entries, not implemented detector claims.
- The generated text represents suspicious inputs to an assistant; the prototype does not run a banking tool and observe whether the text causes an unauthorized tool call.
- Mitigation outputs are recommendations for a hypothetical control plane.
