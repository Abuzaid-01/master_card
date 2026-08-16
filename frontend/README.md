# GenAI Fraud Shield — Interactive Web Dashboard

Frontend interface for the **GenAI Fraud Shield** red–blue team adversarial defense engine.

## Overview

- **Stack:** React 19, TanStack Start & Router, TailwindCSS, Motion, TanStack Query
- **Architecture:** SSR & Client-side hybrid with real-time API connection to FastAPI backend
- **Sections:**
  1. **Overview / Hero:** Live metrics summary & Mastercard Innovation Challenge showcase
  2. **Identify:** 8 FinCEN GenAI attack vectors catalog
  3. **Generate:** AI Red Team synthetic attack engine benchmarks
  4. **Defend:** AI Blue Team ONNX & Semantic detection results
  5. **Closed Loop:** Adversarial active learning loop metrics & 0% catastrophic forgetting
  6. **Live Demo:** Interactive playground with single-transaction inference + full 6-step live pipeline wizard
  7. **Stack & Team:** Technical architecture and project links

## Running Locally

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend runs on `http://localhost:8080` and proxies `/api` calls to the FastAPI backend on port 8000.
