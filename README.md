# SENTRIX AI

SENTRIX AI is a research prototype for the Mastercard Innovation Challenge 2026. It implements the challenge's **Identify → Generate → Defend → Learn** cycle for GenAI-enabled payment fraud.

The project simulates fraud telemetry in a controlled environment. It does not connect to a bank, card network, customer account, or settlement rail, and the actions shown by the UI are policy recommendations rather than executed payment controls.

## Product experience

The web experience presents fraud as a connected story rather than a collection of isolated alerts. Its opening payment sequence follows five authorizations over seventeen seconds: a ₹199 probe grows through progressively larger attempts into a ₹94,000 cash-out request. Sentrix correlates the shared card, device, behavioral, and beneficiary-path evidence before presenting the campaign-level decision.

The landing page includes:

- A GSAP-driven card-to-terminal sequence tied to deliberate scroll progress.
- A five-step transaction escalation trail showing the 472× value increase.
- Connected conversational, authorization, and settlement-network threat scenes.
- Interactive transaction and text analysis backed by FastAPI.
- Persistent light and dark themes, responsive layouts, and reduced-motion support.

The animation is narrative support only: amounts, risk states, and explanatory copy remain available as structured page content.

## What is implemented

| Challenge stage | Implementation | Main outputs |
| --- | --- | --- |
| Identify | An eight-vector payment-fraud taxonomy grounded in payment workflows and public threat guidance | [`docs/identify.md`](docs/identify.md) |
| Generate | Seeded generators for transaction, prompt-injection, mule-graph, adversarial-evasion, and compound-campaign data | `data/synthetic/` |
| Defend | XGBoost transaction detector, semantic/TF-IDF text detector, graph-feature classifier, threshold optimization, and feature attribution | `defend/models/`, `data/defend/metrics_report.json` |
| Learn | Offline three-lane adversarial probing and Round-2 retraining, plus an interactive text/tabular demo loop | `data/loop/closed_loop_report.json` |
| Demonstrate | React/TanStack frontend backed by FastAPI endpoints | `frontend/`, `api/` |

## Threat model

The implemented prototype focuses on three observable signal types:

1. **Conversational signals** — prompt injection, role impersonation, notification suppression, and tool-hijacking language.
2. **Authorization signals** — transaction amount, velocity, device risk, declines, merchant risk, geographic distance, card age, and failed attempts.
3. **Settlement-network signals** — rapid pass-through transfers, fan-out, chains, cycles, degree anomalies, and mule-funnel behavior.

Compound scenarios link those signals into a demonstration sequence:

```text
social-engineering prompt → card-testing burst and drain → mule-routing hops
           ↓                         ↓                         ↓
      text detector          transaction detector          graph detector
           └──────────────────── risk fusion ────────────────────┘
                                  ↓
                         recommended policy action
```

The compound generator currently uses four curated scenario templates with seeded numeric variation. It is a campaign demonstration, not a learned event-correlation model.

## Repository structure

```text
api/                    FastAPI service and interactive pipeline runner
defend/                 detector training, fusion, cost, and explanation code
docs/                   technical documentation for each challenge pillar
frontend/               React 19 + TanStack Start web prototype
generate/               synthetic data generators and fidelity evaluation
loop/                   offline adversarial probing and Round-2 retraining
data/synthetic/         generated datasets and fidelity report
data/defend/            baseline evaluation reports and held-out data
data/loop/              closed-loop report and Round-2 model artifacts
```

Detailed documentation:

- [Identify](docs/identify.md)
- [Generate](docs/generate.md)
- [Defend and evaluate](docs/defend.md)
- [Cross-vector fusion](docs/cross_vector.md)
- [Frontend](frontend/README.md)

## Two execution paths

### 1. Reproducible offline experiment

This is the complete research path. It generates all data modalities, trains all three detector heads, probes each model, retrains on discovered misses, and writes reports to disk.

```text
generate/run_pipeline.py
        ↓
defend/run_defend_pipeline.py
        ↓
loop/run_closed_loop.py
```

### 2. Interactive web pipeline

The browser exposes a shorter stateful pipeline through `api/pipeline_runner.py`:

```text
generate → train Round 1 → probe → retrain Round 2 → evaluate
```

It currently supports the full live learning sequence for **text** and **tabular** data. The `cross_vector` selection currently runs the tabular learning lane; the separate cross-vector sandbox scores a three-phase curated scenario with all three saved detector heads. Graph Round-2 learning is therefore demonstrated by the offline pipeline, not the interactive wizard.

The live pipeline uses a leakage-resistant four-way split:

- 60% training
- 20% validation
- 10% blind-spot mining
- 10% final evaluation

Fraud families are isolated between partitions, legitimate transaction data is time-ordered where timestamps are available, and the final evaluation partition is not used for retraining.

## Reported results

These values are the checked-in outputs of the current experiment. They are results on generated or mapped benchmark data, not production guarantees.

### Baseline defense

| Detector | Checked-in result |
| --- | --- |
| Transaction | AUC-PR `1.0000`, F1 `1.0000`, FPR `0.0000` on the synthetic validation split |
| Text | semantic AUC-PR `0.9996`; paraphrase subset `0.9877` versus TF-IDF `0.8965` |
| Graph | AUC-PR `0.9455`, F1 `0.8727` |
| ONNX transaction benchmark | `0.008 ms` average in the recorded local benchmark |

### Closed-loop evaluation

| Lane | Round 1 catch rate | Round 2 catch rate | Evaluation fraud samples |
| --- | ---: | ---: | ---: |
| Transaction | 69.07% | 96.27% | 750 |
| Text | 0.00% | 100.00% | 38 |
| Graph | 28.57% | 82.86% | 70 |

The small text evaluation set and synthetic separability make these results illustrative. See [`data/loop/closed_loop_report.json`](data/loop/closed_loop_report.json) for sample counts, thresholds, AUC changes, and stability checks.

### Fidelity

All generated records passed the implemented domain rules in the checked-in run. That is not the same as proving real-world fidelity. When mapped to a 20,000-row IEEE-CIS benchmark sample, the recorded transaction TSTR AUC-PR is `0.1472`, and several marginal KS tests show substantial distribution mismatch. Improving cross-domain fidelity is active work; the repository does not claim that the generated distribution is production-equivalent.

See [`data/synthetic/fidelity_report.json`](data/synthetic/fidelity_report.json).

## Local setup

### Prerequisites

- Python 3.11
- Node.js 20 or newer
- npm
- Optional: the IEEE-CIS `train_transaction.csv` dataset for the external fidelity comparison

### Install the backend

From the repository root:

```bash
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

```bash
source .venv/bin/activate
```

Then install dependencies:

```bash
python -m pip install -r requirements.txt
```

For the lower-memory API-only deployment dependency set, use `api/requirements.txt` instead.

### Reproduce the offline reports

Run from the repository root so module imports and output paths resolve correctly:

```bash
python -m generate.run_pipeline
python -m defend.run_defend_pipeline
python -m loop.run_closed_loop
```

If `ieee-fraud-detection/train_transaction.csv` is unavailable, generation falls back to a synthetic comparison baseline and labels the report accordingly.

### Run the API

```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

- Health: `http://localhost:8000/api/health`
- OpenAPI: `http://localhost:8000/docs`

### Run the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:8080`. Development requests under `/api` are proxied to `http://localhost:8000`.

### Production frontend

The frontend is built as a Cloudflare-compatible TanStack Start application and published through OpenAI Sites. Production builds read the backend origin from `frontend/.env.production`; the current checked-in value targets `https://master-card.onrender.com`.

Before publishing against another API deployment, update `VITE_API_URL` and rebuild the frontend.

## API summary

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | model/report availability and text inference mode |
| GET | `/api/metrics` | checked-in baseline defense report |
| GET | `/api/fidelity` | checked-in synthetic fidelity report |
| GET | `/api/closed-loop` | checked-in offline Round-1/Round-2 report |
| POST | `/api/demo/tabular` | transaction inference with native XGBoost contributions |
| POST | `/api/demo/text` | text inference and active inference mode |
| GET | `/api/simulate/cross_vector` | generate and score a curated compound scenario |
| POST | `/api/simulate/cross_vector_evaluate` | score a caller-provided compound scenario |
| GET/POST | `/api/llm/*` | discover configured providers and generate text samples |
| POST | `/api/pipeline/*` | run the interactive generate/train/attack/retrain/evaluate sequence |

The hosted API defaults to the deployment-safe TF-IDF text model. Set `SENTRIX_ENABLE_SEMANTIC_MODEL=true` only on a runtime with enough memory to load Sentence Transformers and PyTorch.

## Optional text-generation providers

The text generator works without external credentials by using curated and programmatic samples. Optional provider-backed generation can be enabled with:

```text
GROQ_API_KEY=...
GEMINI_API_KEY=...
```

Never commit a local `.env` file or API keys.

## Verification

```bash
python -m pytest -q
cd frontend
npm run build
```

At the time of this documentation update, the backend suite passes 8 tests and the production frontend build succeeds. Loading checked-in scikit-learn artifacts with a different scikit-learn version may emit compatibility warnings; install the pinned repository dependencies before relying on serialized models.

## Known limitations

- Cross-vector fusion assumes independent component probabilities and adds a fixed `0.05` text-plus-transaction synergy boost; it is not calibrated on real linked campaigns.
- Cross-vector templates share identifiers within each scenario, but the prototype does not ingest a real event stream or learn entity resolution.
- Recommended actions such as hold, step-up authentication, or freeze are simulated policy outputs only.
- Some current transaction probing strategies modify risk-derived fields. A production red-team simulator should restrict attacker controls to observable, operationally plausible inputs.
- Interactive pipeline state is process-local and is lost when the API restarts.
- Generated-data metrics can be optimistic because the simulator encodes strong class signatures.
- The web prototype is a demonstration interface, not an authenticated or production-hardened payment application.

## Submission scope

This repository is the code artifact for the challenge. A valid competition submission also requires a separate `.docx` solution walkthrough, a working hosted web prototype, and a submitted Kaggle Writeup before the deadline. A draft Writeup is not a completed submission.

## Team and attribution

SENTRIX AI is a challenge project maintained through the contributors shown in this repository's Git history. Third-party datasets, libraries, and public threat sources remain subject to their respective licenses and terms.
