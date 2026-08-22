# Generate: synthetic attack simulation

The `generate/` package creates controlled datasets for detector training and red-team experiments. Generators are seeded where supported so experiments can be reproduced.

## Generators

| Module | Output | Current method |
| --- | --- | --- |
| [`generator_tabular.py`](../generate/generator_tabular.py) | `synthetic_tabular_card_testing.csv` | statistical legitimate-spending baseline plus five parameterized fraud families |
| [`generator_text.py`](../generate/generator_text.py) | `synthetic_prompt_injections.csv` | curated/programmatic samples with optional Groq or Gemini generation |
| [`generator_graph.py`](../generate/generator_graph.py) | `synthetic_mule_graph.csv` | NetworkX-derived transfer features for chains, fan-out, smurfing, and cycles |
| [`generator_evasion.py`](../generate/generator_evasion.py) | `synthetic_evasion_patterns.csv` | feature perturbations applied to transaction fraud samples |
| [`generator_cross_vector.py`](../generate/generator_cross_vector.py) | `synthetic_cross_vector_scenarios.json` | four curated three-phase campaign templates with seeded transaction variation |

The code does not currently use CTGAN, PaySim, or LangGraph.

## Default full run

`generate.run_pipeline` produces:

- 50,000 transaction rows spanning legitimate activity and five fraud subtypes.
- 1,500 text rows spanning legitimate prompts and multiple injection/social-engineering categories.
- A graph dataset built from 1,000 users and 100 synthetic mule rings.
- An adversarial transaction derivative.
- 100 compound scenario instances drawn from four base templates.

Run from the repository root:

```bash
python -m generate.run_pipeline
```

Outputs are written to `data/synthetic/`.

## Domain validation

[`domain_validator.py`](../generate/domain_validator.py) checks applicable schema and range constraints, including positive amounts, valid labels/probability-like fields, timestamp behavior, and graph/transaction consistency rules when the required fields exist.

A 100% domain pass rate means records satisfied these implemented rules. It does not establish resemblance to a real payment population.

## Fidelity evaluation

[`fidelity_eval.py`](../generate/fidelity_eval.py) reports:

- Wasserstein distance for selected continuous features.
- Kolmogorov-Smirnov statistics for marginal distributions.
- Train-on-synthetic, test-on-real (TSTR) AUC-PR when a mapped benchmark is available.

For the checked-in run, `ieee-fraud-detection/train_transaction.csv` was mapped into the prototype schema using selected IEEE-CIS columns plus derived fields. The resulting report records TSTR AUC-PR `0.1472`, with large mismatches on several selected features. This is evidence of a current fidelity gap, not a high-fidelity result.

If the local IEEE-CIS file is absent, the pipeline uses a second seeded synthetic dataset as its comparison baseline and records `Synthetic Baseline` in the report. That fallback must not be described as real-data validation.

## Optional LLM generation

The text generator does not require network access or credentials. Optional provider generation uses environment variables:

```text
GROQ_API_KEY=...
GEMINI_API_KEY=...
```

Provider output is parsed and combined with locally generated data. Credentials belong in an untracked `.env` file.

## Limitations

- Fixed simulator rules create recognizable generator fingerprints and can make synthetic validation easier than deployment data.
- The four compound templates do not provide broad campaign diversity.
- Cross-vector stages are linked by template identifiers, not by a learned temporal/entity model.
- The IEEE-CIS mapping cannot recreate unavailable operational features and includes derived proxy fields.
- Current perturbation code can change defender-derived risk features; a production simulator should mutate attacker-controllable source events and let the feature pipeline recalculate risk fields.
