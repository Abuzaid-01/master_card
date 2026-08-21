export type Severity = "Critical" | "High" | "Medium";

export const heroStats = [
  { value: 3, suffix: "", label: "Correlated Risk Signals", icon: "shield" as const },
  {
    value: 96.3,
    suffix: "%",
    decimals: 1,
    label: "Adversarial Catch Rate",
    icon: "target" as const,
  },
  {
    value: 0.008,
    suffix: "ms",
    decimals: 3,
    label: "Decision Latency",
    icon: "zap" as const,
  },
  {
    value: 3061,
    prefix: "$",
    label: "Loss Avoided per Batch",
    icon: "dollar" as const,
  },
];

export const attackVectors: {
  n: number;
  name: string;
  desc: string;
  severity: Severity;
  multiplier: string;
  icon: string;
}[] = [
  {
    n: 1,
    name: "Indirect Prompt Injection",
    desc: "Jailbreaking bank AI chatbots to bypass transfer limits",
    severity: "Critical",
    multiplier: "LLMs generate infinite paraphrased jailbreaks across 13 threat categories.",
    icon: "terminal",
  },
  {
    n: 2,
    name: "Deepfake KYC Bypass",
    desc: "AI-generated identity documents fooling liveness checks",
    severity: "Critical",
    multiplier:
      "Diffusion models forge photoreal IDs and live faces in seconds, at near-zero marginal cost.",
    icon: "scan-face",
  },
  {
    n: 3,
    name: "AI Voice Clone Scams",
    desc: "Cloned CEO voices authorizing million-dollar wire transfers",
    severity: "Critical",
    multiplier:
      "Three seconds of public audio is enough to clone an executive voice with emotional prosody.",
    icon: "mic",
  },
  {
    n: 4,
    name: "Synthetic Identity Fraud",
    desc: "AI-generated synthetic identities opening funnel accounts",
    severity: "High",
    multiplier:
      "Generative models fabricate coherent credit histories that survive bureau plausibility checks.",
    icon: "user-round-search",
  },
  {
    n: 5,
    name: "Evasive Card Testing",
    desc: "Multi-pattern bots testing stolen cards (burst, ATO, bot siphon, CNP, slow drip)",
    severity: "High",
    multiplier:
      "Agentic bots adapt amount, velocity, geo-displacement and merchant channels in real time.",
    icon: "credit-card",
  },
  {
    n: 6,
    name: "Multi-Hop Money Mule Networks",
    desc: "Layered fund transfers across 4 graph topologies (chains, fan-out, smurfing, cycles)",
    severity: "High",
    multiplier:
      "Path-planning agents route funds across sub-threshold hops to evade automated SAR triggers.",
    icon: "share-2",
  },
  {
    n: 7,
    name: "GenAI Merchant Fraud",
    desc: "AI-generated fake e-commerce storefronts for chargeback scams",
    severity: "Medium",
    multiplier:
      "Full storefronts, catalogs, reviews and policies are spun up in minutes and burned after payout.",
    icon: "store",
  },
  {
    n: 8,
    name: "Adversarial Transaction Evasion",
    desc: "Mathematical perturbations to dodge detection boundaries",
    severity: "High",
    multiplier:
      "Gradient-guided perturbations find detector blind spots while preserving attacker economics.",
    icon: "git-branch",
  },
];

export const datasets = [
  {
    title: "Tabular Card Fraud",
    count: 50000,
    unit: "transactions",
    lines: [
      "5 Sub-Types: Burst, ATO, Bot Siphon, CNP, Slow Drip",
      "10 Enterprise Features · 100% Domain Rule Pass",
    ],
    icon: "table-2",
    accent: "cyan" as const,
  },
  {
    title: "Prompt Injection Text",
    count: 1500,
    unit: "prompts",
    lines: [
      "13 Threat Categories: Voice Pretext, Compliance, Tool Hijack, etc.",
      "SentenceTransformer all-MiniLM-L6-v2 Semantic Embeddings",
    ],
    icon: "message-square-code",
    accent: "violet" as const,
  },
  {
    title: "Money Mule Graph Network",
    count: 7297,
    unit: "transfers",
    lines: [
      "4 Topologies: Linear, Fan-Out, Smurfing, Round-Trip",
      "NetworkX Multi-Hop Directed Graph · 100 Mule Rings",
    ],
    icon: "network",
    accent: "orange" as const,
  },
  {
    title: "Adversarial Evasion",
    count: 50000,
    unit: "perturbed transactions",
    lines: [
      "Multi-Dimensional Decision-Boundary Perturbations",
      "Active Learning Adversarial Holdout Preservation",
    ],
    icon: "crosshair",
    accent: "red" as const,
  },
];

export const terminalLines = [
  "$ python -m generate.run_pipeline --all-vectors",
  "",
  "[1/4] Generating Vector 5: Multi-Pattern Card Fraud (5 sub-types)...",
  "      → Generated 50,000 rows (Burst, ATO, Bot Siphon, CNP, Slow Drip). Pass Rate: 100.0%",
  "[2/4] Generating Vector 1: Prompt Injection Payloads (13 categories)...",
  "      → Generated 1,500 prompts across 13 categories. Pass Rate: 100.0%",
  "[3/4] Generating Vector 2: Multi-Topology Mule Graph (4 topologies)...",
  "      → Generated 7,297 transfers across 100 rings. Pass Rate: 100.0%",
  "[4/4] Generating Vector 8: Adversarial Evasion Set...",
  "      → Generated 50,000 perturbed rows. Pass Rate: 100.0%",
  "",
  "✓ Domain constraints satisfied across 4/4 vectors.",
  "✓ TSTR fidelity verified against 20,000 real IEEE-CIS records.",
];

export const shapFeatures = [
  { name: "geo_distance_km", value: 45.2 },
  { name: "device_risk_score", value: 23.6 },
  { name: "velocity", value: 16.2 },
  { name: "mcc_risk_weight", value: 6.9 },
  { name: "failed_attempts_24h", value: 4.0 },
  { name: "amount", value: 2.8 },
];

export const loopRows = [
  {
    metric: "Tabular Adversarial Catch Rate",
    r1: "69.1%",
    r2: "96.3%",
    delta: "+27.2% (+204 caught)",
    good: true,
  },
  {
    metric: "Text Paraphrased Catch Rate",
    r1: "0.0%",
    r2: "100.0%",
    delta: "+100.0% (+38 caught)",
    good: true,
  },
  {
    metric: "Graph Topology Catch Rate",
    r1: "28.6%",
    r2: "82.9%",
    delta: "+54.3% (+38 caught)",
    good: true,
  },
  {
    metric: "AUC-PR (Adversarial Holdout)",
    r1: "0.985",
    r2: "1.000",
    delta: "+0.015",
    good: true,
  },
  {
    metric: "Baseline False Positive Rate",
    r1: "0.00%",
    r2: "0.00%",
    delta: "0.00% (No Degradation)",
    good: true,
  },
  {
    metric: "Catastrophic Forgetting",
    r1: "n/a",
    r2: "None (0.0% Drift)",
    delta: "Verified Safe",
    good: true,
  },
];

export const techGroups = [
  {
    group: "ML / AI",
    items: ["Python", "XGBoost", "ONNX Runtime", "Sentence Transformers", "SHAP", "scikit-learn"],
    accent: "cyan" as const,
  },
  {
    group: "Data",
    items: ["Pandas", "NumPy", "NetworkX", "IEEE-CIS Benchmark"],
    accent: "violet" as const,
  },
  {
    group: "LLM Red Team",
    items: [
      "Groq Cloud (GPT OSS 120B & Llama 3.3 70B)",
      "Google Gemini (3.5 & 3.1 Flash Lite)",
      "Hugging Face (all-MiniLM-L6-v2)",
    ],
    accent: "orange" as const,
  },
  {
    group: "Infrastructure",
    items: ["ONNX Runtime (C++ compiled inference)", "PCI-DSS Compliant"],
    accent: "red" as const,
  },
  {
    group: "Frontend",
    items: ["React", "Framer Motion", "TailwindCSS"],
    accent: "cyan" as const,
  },
];

export const navSections = [
  { id: "hero", label: "Overview" },
  { id: "identify", label: "Threats" },
  { id: "generate", label: "Red team" },
  { id: "defend", label: "Defense" },
  { id: "loop", label: "Learning loop" },
  { id: "demo", label: "Live lab" },
  { id: "team", label: "About" },
];
