# GenAI Fraud Shield — Showcase Site

A single-page, dark cyber-fintech showcase for the Mastercard Innovation Challenge 2026, built exactly to the spec: 7 full-viewport sections, glassmorphism, neon glows, animated counters, parallax and scroll-reveal motion.

## Design system

- Near-black canvas `#0A0A0F` with a faint circuit/dot grid overlay.
- Accents as tokens: electric cyan `#00E5FF` (good/metrics), Mastercard orange `#FF5F00` (warnings/callouts), Mastercard red `#EB001B` (attacks), violet `#7C3AED` (AI).
- Space Grotesk for headings/body, JetBrains Mono for every number and terminal line, loaded via a font `<link>` in the root layout.
- Glass surfaces: blurred translucent panels with gradient hairline borders, plus reusable neon-glow and 3D hover-tilt treatments.

## Sections

1. **Hero** — glitch/typewriter headline, subtitle and event line, animated Mastercard dual-circle pulse, neural-network particle canvas, 4 staggered glass stat cards (8 attack vectors, 3,637 transactions, 0.006ms ONNX, $722 saved), animated scroll chevron.
2. **Identify** — 8 attack-vector cards in a responsive grid, each with icon, one-line description, severity badge, and a hover reveal for the "GenAI Force Multiplier" detail; staggered entrance over a slower-moving grid layer.
3. **Generate (Red Team)** — split layout: typing terminal on the left streaming the generation log, 4 dataset cards with counters on the right, and a Fidelity Benchmark panel (TSTR, 100% constraint pass rate, Wasserstein distances).
4. **Defend (Blue Team)** — 3 detector cards (tabular, prompt injection, graph mule) with odometer metrics, gauge rings, the TF-IDF vs semantic comparison bars with +12.34% lift, and an animated node graph; below, a Financial Impact banner with the τ*=0.37 / $722.31 optimizer and a SHAP importance bar chart.
5. **Closed Loop** — animated circular flow diagram with particles travelling the path, the massive 3/45 → 29/45 headline, sequential counter reveal (Round 1, then Round 2 after a beat), the four-row Round 1 vs Round 2 comparison, and the orange-bordered callout quote.
6. **Architecture & Stack** — animated pipeline diagram with the continuous-improvement return arrow, plus grouped technology pills with hover glow.
7. **Footer / Team** — project, competition, event dates, glowing GitHub button, "Built with love for Mastercard" tagline.

## Interaction & motion

- Scroll-snap between sections; each section at least 100vh.
- Framer Motion (Motion for React) for reveals, stagger, parallax layers (background ~0.3x), and hover micro-interactions.
- A shared counter hook that animates numbers only when their section enters the viewport, and a sticky floating nav whose section indicators highlight on scroll.
- Reduced-motion fallback so animations degrade gracefully.

## Technical notes

- TanStack Start + React 19 with Tailwind v4; all content lives at `/` (replacing the placeholder index route), split into per-section components under `src/components/sections/` with static data in a single `src/data/` module.
- Motion library added as a dependency; Lucide for icons; particle background and node graph drawn on a lightweight canvas, mounted client-side only to keep SSR safe.
- All colors defined as tokens in `src/styles.css`; no hardcoded color utilities in components.
- No backend — every stat is hardcoded exactly as specified.
- Route head metadata: project-specific title, description, OG and Twitter tags.
