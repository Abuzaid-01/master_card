# SENTRIX AI web experience

The frontend is a React 19 and TanStack Start demonstration interface for the SENTRIX Identify → Generate → Defend → Learn story. It is designed as a lightweight cinematic product narrative rather than a conventional dashboard landing page.

## Landing-page narrative

The opening scene uses GSAP ScrollTrigger to turn a physical card authorization into connected fraud evidence:

1. The user scrolls while the card moves into the payment terminal.
2. The terminal approves the apparently ordinary authorization and captures a risk signal.
3. The physical scene recedes and the campaign-level view is revealed.
4. Five connected attempts animate from a ₹199 probe to a ₹94,000 cash-out request in seventeen seconds.
5. The interface explains the 472× value escalation and marks the sequence risk as critical.

The rest of the page continues the story through notification correlation, payment velocity, beneficiary-network analysis, intervention, and closed-loop learning. Motion is scoped to its scene and cleaned up when the component unmounts so it does not interfere with normal document scrolling.

## What the UI shows

- The fraud taxonomy and implemented signal lanes.
- Checked-in generation, defense, fidelity, and closed-loop metrics served by FastAPI.
- Transaction inference with feature contributions.
- Text prompt-injection inference with the backend's active semantic or TF-IDF mode.
- Curated three-phase cross-vector scenario scoring.
- A stateful generate/train/probe/retrain/evaluate wizard for text and transaction lanes.

The interface does not execute actions against a payment network. Freeze, hold, block, and step-up labels are simulated recommendations.

## Run locally

Start the FastAPI service from the repository root on port 8000:

```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Then, from `frontend/`:

```bash
npm install
npm run dev
```

Open `http://localhost:8080`. The Vite development configuration proxies `/api` to `http://localhost:8000`.

## Production API selection

Production builds use `VITE_API_URL` when provided. The checked-in `.env.production` points to the hosted Render backend. Update that value for a different deployment before building:

```text
VITE_API_URL=https://your-api.example.com
```

The frontend query layer falls back to the configured hosted API outside local development.

## Commands

```bash
npm run dev
npm run build
npm run preview
npm run lint
npm run format
```

`npm run build` currently succeeds. The repository still has a CRLF/Prettier line-ending mismatch that causes the lint command to report formatting failures on Windows-originated files; this is a formatting issue, not a production build failure.

## Architecture

- `src/routes/index.tsx` assembles the landing page.
- `src/components/sections/` contains the story and live-demo sections.
- `src/hooks/useBackendMetrics.ts` owns API reads and mutations.
- `src/styles.css` contains page-level design and motion styling.
- `src/routes/__root.tsx` is the TanStack Start application shell.

## Theme behavior

Light mode uses a warm ivory surface while dark mode keeps the high-contrast cinematic palette. The card and payment terminal intentionally remain high contrast in both themes. The preference is controlled from the sticky navigation and persisted in the browser.

Theme-specific landing-page styles live alongside the core scene styles in `src/styles.css`; avoid adding hard-coded page backgrounds outside those theme blocks.

The pipeline session is held in the backend process. Refreshing the UI keeps backend state only while that process remains alive; restarting or replacing the server clears it.

## Accessibility and motion

Visual motion should remain supportive rather than carrying required information. New animation work should honor `prefers-reduced-motion`, preserve readable contrast, and keep all controls usable by keyboard.
