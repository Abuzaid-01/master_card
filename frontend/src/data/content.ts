export type Severity = "Critical" | "High" | "Medium";

export const heroStats = [
  { value: 8, suffix: "", label: "Attack Vectors", icon: "shield" as const },
  {
    value: 50000,
    suffix: "",
    label: "Synthetic Transactions",
    icon: "database" as const,
  },
  {
    value: 0.008,
    suffix: "ms",
    decimals: 3,
    label: "ONNX Inference",
    icon: "zap" as const,
  },
  {
    value: 105,
    prefix: "$",
    label: "Saved per Batch",
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
    multiplier:
      "LLMs generate infinite paraphrased jailbreaks across 12 threat categories.",
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
    desc: "Multi-pattern bots testing stolen cards (burst, ATO, slow drip, CNP, friendly fraud)",
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
      "5 Sub-Types: Burst, ATO, Slow Drip, CNP, Friendly Fraud",
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
      "12 Threat Categories: Voice Pretext, Compliance, Hijack, etc.",
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
      "NetworkX Multi-Hop Directed Graph · Funnel Scores",
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
  "      → Generated 50,000 rows (Burst, ATO, Drip, CNP, Friendly). Pass Rate: 100.0%",
  "[2/4] Generating Vector 1: Prompt Injection Payloads (12 categories)...",
  "      → Generated 1,500 prompts across 12 categories. Pass Rate: 100.0%",
  "[3/4] Generating Vector 2: Multi-Topology Mule Graph (4 topologies)...",
  "      → Generated 7,297 transfers across 100 rings. Pass Rate: 100.0%",
  "[4/4] Generating Vector 8: Adversarial Evasion Set...",
  "      → Generated 50,000 perturbed rows. Pass Rate: 100.0%",
  "",
  "✓ Domain constraints satisfied across 4/4 vectors.",
  "✓ TSTR fidelity verified against 20,000 real IEEE-CIS records.",
];

export const shapFeatures = [
  { name: "device_risk_score", value: 74.2 },
  { name: "velocity_1h", value: 11.6 },
  { name: "is_decline", value: 9.3 },
  { name: "amount", value: 4.9 },
];

export const loopRows = [
  {
    metric: "Adversarial Catch Rate",
    r1: "6.7%",
    r2: "64.4%",
    delta: "+57.7%",
    good: true,
  },
  {
    metric: "AUC-PR (Adversarial)",
    r1: "0.653",
    r2: "0.917",
    delta: "+0.264",
    good: true,
  },
  {
    metric: "Baseline FPR",
    r1: "2.82%",
    r2: "1.72%",
    delta: "-1.10% (improved!)",
    good: true,
  },
  {
    metric: "Catastrophic Forgetting",
    r1: "n/a",
    r2: "None",
    delta: "baseline",
    good: true,
  },
];

export const techGroups = [
  {
    group: "ML / AI",
    items: [
      "Python",
      "XGBoost",
      "ONNX Runtime",
      "Sentence Transformers",
      "SHAP",
      "scikit-learn",
    ],
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
  { id: "identify", label: "Identify" },
  { id: "generate", label: "Generate" },
  { id: "defend", label: "Defend" },
  { id: "loop", label: "Closed Loop" },
  { id: "demo", label: "Live Demo" },
  { id: "team", label: "Team" },
];
