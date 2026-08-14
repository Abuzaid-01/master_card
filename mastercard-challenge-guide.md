
# Mastercard Innovation Challenge 2026 — Full Project Guide

**Event:** Global Fintech Fest, Mumbai
**Registration deadline:** Aug 20
**Submission deadline:** Aug 31, 11:59 PM IST
**Results:** Sep 5 | **Live showcase:** Sep 8–11, Mumbai
**Prizes:** 1st ₹2,56,000 · 2nd ₹1,28,000 · 3rd ₹64,000

---

## 1. What This Challenge Actually Is

You're not building a fraud detector. You're building the **attacker AND the defender** as one closed-loop system that feeds itself:

```
Attack Ideas → Simulated Attacks → Detector → Detector's Blind Spots → Better Attacks → repeat
```

Judges specifically reward this loop existing — a static "10 attacks + 1 classifier" submission scores lower than one showing 2-3 rounds of the detector actually improving because it kept failing against new attacks you generated.

## 2. The 3 Pillars

| Pillar             | What it means                                                                                                               |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| **Identify** | Research and list*novel* GenAI-powered payment fraud vectors — real-world grounded, not generic                          |
| **Generate** | Build agents/algorithms that simulate these attacks at scale with high fidelity (realistic, not random noise)               |
| **Defend**   | Build a real ML/AI classifier that detects the attacks you generated — optimize precision/recall, keep false positives low |

## 3. What You Must Submit (non-negotiable)

1. **Code repo** — full working code, all 3 pillars, documented, reproducible
2. **Solution walkthrough** — deck/doc: attacks found, generation approach, detection results, real-world feasibility
3. **Working web prototype** — live UI demonstrating the closed loop, not just a static demo

**Judged on:** diversity of attacks · fidelity of simulation · detection efficacy · novelty · real-world feasibility

---

## 4. Full Step-by-Step Procedure

### Step 0 — Setup (Day 1)

- Register on Kaggle competition page, lock team (solo or up to 5)
- Create GitHub repo with skeleton folders: `/identify`, `/generate`, `/defend`, `/loop`, `/prototype`, `/docs`
- Set up dev environment: VS Code locally for code, Kaggle/Colab notebooks for GPU-heavy training
- Keep a running tracking doc — every decision you make becomes deck content later

### Step 1 — IDENTIFY (Days 1–3, no coding)

Create `/docs/identify.md`. For **8-12 fraud attack vectors**, write:

```
### [Attack Name]
- How it works today: ...
- How GenAI changes it: ...
- Data signature it leaves: ... (what pattern your model will actually learn)
- Source: [link]
```

**Categories to research (search these):**

- Deepfake identity/KYC bypass fraud → search `FinCEN deepfake fraud alert`
- AI-automated social engineering / scam calls → search `AI scam call voice clone bank`
- Prompt injection against bank AI agents (strong novelty pick) → search `prompt injection banking AI agent`
- Adversarial transaction pattern evasion → search `adversarial transaction pattern fraud detection evasion`
- Automated/AI-driven card testing → search `AI bot card testing fraud automated`
- Fake AI-generated merchant/e-commerce fraud → search `AI generated fake online store chargeback scam`
- AI-driven money mule network recruitment → search `AI money mule recruitment fraud`
- AI-generated check/document forgery → search `AI generated check fraud forgery`

**Ground every vector in a real source** — FinCEN.gov, Mastercard.com/news-and-trends, OWASP LLM Top 10, FBI IC3 (ic3.gov). Judges score "real-world feasibility" — ungrounded/sci-fi attacks lose points.

**Upgrade — add these 2 vectors if not already in your list:**

- **Prompt Injection on Bank AI Agents** (already covered above)
- **Multi-hop AI Mule Networks** — GenAI-assisted layering of funds through chains of mule accounts to obscure the money trail. Novel, graph-shaped attack — strong diversity/novelty score.

### Step 2 — GENERATE (Days 4–8, coding starts)

1. **Pick 4-5 attacks** out of your 8-12 to actually simulate (rest stay as "future work" in the doc — still counts for diversity scoring)
2. **Split by type:**
   - Number-based attacks (transaction fraud, card testing, mules) → need **structured/tabular data**
   - Text-based attacks (phishing scripts, scam transcripts, chatbot manipulation) → need **text data**
3. **Get a real base dataset** (don't invent fraud data from nothing):
   - **IEEE-CIS Fraud Detection** dataset (Kaggle) — real anonymized transactions
   - **PaySim** dataset (Kaggle) — synthetic mobile-money data built to mimic real fraud statistically
4. **Build the generator:**
   - Tabular: CTGAN/TVAE or careful statistical sampling, conditioned on legit vs fraud labels
   - Text: LLM agent (LangGraph) role-playing a "fraudster persona" to generate scam scripts at scale
   - **Upgrade — Adversarial Evasion Perturbers:** don't just generate once — perturb generated samples specifically to dodge your *current* detector's decision boundary. This is what actually powers your closed loop in Step 4, not a separate feature — build it here so it's ready to reuse.
   - **Upgrade — Domain Rule Checker:** validate every generated sample against basic domain constraints (amount > 0, valid merchant category codes, timestamps make sense, etc.). Report **% of samples that pass** — cheap to build, strong credibility signal that your data isn't just numeric noise.
5. **Check fidelity** — compare generated data vs real data distribution:
   - KS-test + histogram overlap (baseline)
   - **Upgrade — Wasserstein Distance:** one more standard distribution-distance metric, cheap to add alongside KS-test
   - **Upgrade — Domain Constraint Pass Rate:** % of samples passing the rule checker above
   - **Upgrade — TSTR Score (Train on Synthetic, Test on Real):** train your detector *only* on synthetic data, test it *only* on real held-out data. If it still performs well, that's your strongest proof of realistic fraud generation — highest-impact metric to add, cheap to implement (just swap train/test sets). Put this front and center in your deck.

### Step 3 — DEFEND (Days 9–13)

Build two detector types:

- **Tabular fraud** → XGBoost/LightGBM + an anomaly-detection layer (isolation forest/autoencoder) to catch novel patterns without labeled examples
- **Text-based social engineering** → semantic/embedding-based classifier (not keyword rules — attackers paraphrase past keyword filters)
- **Mule network detection** → keep this simple: represent mule chains as a graph, use basic graph features (degree, path length, cycle detection) rather than training a full GNN — you get the novelty credit without burning days on GNN debugging. Only go for a trained GNN if you have spare time near the end.

**Upgrade — Tiered Defense architecture (real-world feasibility booster):**
Mirrors how production fraud systems actually work — fast simple model inline, slower complex model async.

- **Inline (sub-50ms):** export your XGBoost model to **ONNX** (quick one-line export) for fast scoring in the critical transaction path
- **Out-of-band (async):** run the text/GNN model separately, not blocking the transaction
- You don't need a real message queue — just architect it this way and show the latency numbers in your deck. This single addition strongly signals production-readiness to judges.

**Key theory to get right (signals real ML maturity to judges):**

- Fraud is rare → use class weighting/focal loss, evaluate with **AUC-PR** not just AUC-ROC
- False positives cost real money in payments → tune decision threshold against a cost function
- Add **SHAP explainability** — judges reward interpretability in a regulated industry

### Step 4 — CLOSE THE LOOP (Days 14–15) — your strongest differentiator

1. Run your detector against the attacks you generated
2. Find what it **misses**
3. Feed those failure patterns back to the Generate agent → produce a harder batch targeting the gaps
4. Retrain/re-evaluate the detector
5. Show detection metrics improving **round over round** (even just 2 rounds) — this is your best "novelty" and "closed-loop" evidence

### Step 5 — PROTOTYPE (Days 16–17)

Web UI that shows the **loop live**, not a static fraud/not-fraud box:

- Pick attack category → generate a synthetic attack → detector scores it → dashboard showing detection performance across rounds (before vs after retraining)
- FastAPI backend (same pattern you've used before), deployed on Render/Vercel so judges get a live link

### Step 6 — DECK + POLISH (Day 18)

- Finalize solution walkthrough deck
- Clean README, requirements.txt, test full pipeline runs end-to-end from a fresh clone
- Submit early on Aug 31 — not at 11:58 PM

---

## 5. Tech Stack Mapping

| Part               | Tool                                                                                      | Where                                           |
| ------------------ | ----------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Identify           | Just research + markdown doc                                                              | Local repo                                      |
| Generate (tabular) | CTGAN / statistical sampling                                                              | Kaggle/Colab notebook (needs compute)           |
| Generate (text)    | LangGraph agent + HF/Groq-hosted model                                                    | Local                                           |
| Defend             | XGBoost/LightGBM, embedding classifier, SHAP                                              | Colab/Kaggle for training, load weights locally |
| Loop orchestration | LangGraph state graph (Attack → Generate → Detect → Evaluate → conditional loop back) | Local                                           |
| Prototype          | FastAPI backend + simple frontend                                                         | Local → deploy Render/Vercel                   |

---

## 6. What Makes This "Genuinely Good" vs "Just a Hackathon Project"

1. **Cite real sources** in your Identify doc — actual fraud reports, advisories, real incidents
2. **Show a metric, not a claim** — every pillar needs a number (KS-test score, AUC-PR, confusion matrix)
3. **Show the loop actually closing** — round 1 vs round 2 metrics side by side
4. **Address false positives explicitly** — a threshold-tuning tradeoff slide signals real domain thinking
5. **Address regulatory reality** — one slide on PCI-DSS, latency requirements, explainability for compliance
6. **Clean, reproducible repo** — stranger should be able to clone and run it end to end

---

## 7. Submission Checklist

- [ ] Code repo — all 3 pillars, documented, runs end-to-end
- [ ] Solution walkthrough deck/doc
- [ ] Working web prototype (live link)
- [ ] Registered on Kaggle before Aug 20
- [ ] Submitted before Aug 31, 11:59 PM IST
