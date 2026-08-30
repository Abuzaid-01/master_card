export type Severity = "Critical" | "High" | "Medium";

export type AttackPillar =
  | "All"
  | "Pillar 1: AI Red-Teaming"
  | "Pillar 2: Synthetic Data"
  | "Pillar 3: Multi-Rail Payments"
  | "Pillar 4: Money Mule Networks"
  | "Pillar 5: Adversarial Evasion";

export const heroStats = [
  { value: 36, suffix: "", label: "Attack Vectors", icon: "shield" as const },
  {
    value: 50000,
    suffix: "",
    label: "Synthetic Transactions",
    icon: "database" as const,
  },
  {
    value: 0.006,
    suffix: "ms",
    decimals: 3,
    label: "ONNX Inference",
    icon: "zap" as const,
  },
  {
    value: 3072,
    prefix: "$",
    label: "Saved per Batch",
    icon: "dollar" as const,
  },
];

export interface AttackVectorItem {
  n: number;
  id: string;
  pillar: string;
  pillarShort: AttackPillar;
  name: string;
  desc: string;
  severity: Severity;
  multiplier: string;
  icon: string;
}

export const attackVectors: AttackVectorItem[] = [
  // ── Pillar 1: AI Red-Teaming & Social Engineering (8 Vectors) ──
  {
    n: 1,
    id: "V01",
    pillar: "Pillar 1: AI Red-Teaming & Social Engineering",
    pillarShort: "Pillar 1: AI Red-Teaming",
    name: "Admin Impersonation Override",
    desc: "Fabricated administrative authority tokens to force unauthorized wire execution.",
    severity: "Critical",
    multiplier: "LLM agents hijack system instructions when presented with pseudo-cryptographic audit tokens.",
    icon: "terminal",
  },
  {
    n: 2,
    id: "V02",
    pillar: "Pillar 1: AI Red-Teaming & Social Engineering",
    pillarShort: "Pillar 1: AI Red-Teaming",
    name: "API Tool-Function Hijacking",
    desc: "Nested JSON tool-call instructions triggering external ledger transfers without secondary OTP.",
    severity: "Critical",
    multiplier: "Manipulates agent function-calling schemas to invoke financial disbursement endpoints.",
    icon: "bot",
  },
  {
    n: 3,
    id: "V03",
    pillar: "Pillar 1: AI Red-Teaming & Social Engineering",
    pillarShort: "Pillar 1: AI Red-Teaming",
    name: "Compliance Officer Impersonation",
    desc: "Pretexts as AML officer conducting emergency compliance drills to extract KYC records.",
    severity: "High",
    multiplier: "Exploits helpfulness alignment by citing urgency and regulatory audit penalty clauses.",
    icon: "shield-alert",
  },
  {
    n: 4,
    id: "V04",
    pillar: "Pillar 1: AI Red-Teaming & Social Engineering",
    pillarShort: "Pillar 1: AI Red-Teaming",
    name: "AI Voice Clone Vishing",
    desc: "Synthetic corporate executive voice authorizing high-value urgent interbank transfers.",
    severity: "Critical",
    multiplier: "3 seconds of audio replicates pitch prosody and acoustic room resonance to fool call center agents.",
    icon: "mic",
  },
  {
    n: 5,
    id: "V05",
    pillar: "Pillar 1: AI Red-Teaming & Social Engineering",
    pillarShort: "Pillar 1: AI Red-Teaming",
    name: "Safe Account Impersonation Scam",
    desc: "Convinces victims their account is compromised and coerces transfer to 'safe reserve'.",
    severity: "High",
    multiplier: "Generative pretexts spoof bank fraud alert SMS headers and escalation scripts.",
    icon: "lock",
  },
  {
    n: 6,
    id: "V06",
    pillar: "Pillar 1: AI Red-Teaming & Social Engineering",
    pillarShort: "Pillar 1: AI Red-Teaming",
    name: "Pig-Butchering Romance Fraud",
    desc: "Multi-turn long-con grooming victims into fake high-yield crypto investment platforms.",
    severity: "High",
    multiplier: "Autonomous conversational agents maintain 30+ day emotional rapport across messaging channels.",
    icon: "user-round-search",
  },
  {
    n: 7,
    id: "V07",
    pillar: "Pillar 1: AI Red-Teaming & Social Engineering",
    pillarShort: "Pillar 1: AI Red-Teaming",
    name: "B2B AI Invoice Forgery",
    desc: "Generative AI produces indistinguishable vendor invoices with altered beneficiary IBAN routing.",
    severity: "Critical",
    multiplier: "Vision-LLMs ingest real ERP purchase orders and generate matching forged invoices with modified accounts.",
    icon: "file-text",
  },
  {
    n: 8,
    id: "V08",
    pillar: "Pillar 1: AI Red-Teaming & Social Engineering",
    pillarShort: "Pillar 1: AI Red-Teaming",
    name: "Agentic MCP Tool Hijacking",
    desc: "Model Context Protocol prompt injection overriding AI agent tool parameters to divert funds.",
    severity: "Critical",
    multiplier: "Exploits JSON-RPC tool parameters in MCP servers to bypass human-in-the-loop approvals.",
    icon: "cpu",
  },

  // ── Pillar 2: Synthetic Data & Obfuscation (7 Vectors) ──
  {
    n: 9,
    id: "V09",
    pillar: "Pillar 2: Synthetic Data & Obfuscation",
    pillarShort: "Pillar 2: Synthetic Data",
    name: "Base64 & Unicode Obfuscation",
    desc: "Encodes adversarial directives into Hex/Base64/Zalgo characters to blind string filters.",
    severity: "Medium",
    multiplier: "Keyword tokenizers fail while the underlying LLM decodes and executes the underlying payload.",
    icon: "terminal",
  },
  {
    n: 10,
    id: "V10",
    pillar: "Pillar 2: Synthetic Data & Obfuscation",
    pillarShort: "Pillar 2: Synthetic Data",
    name: "Indirect Memo Payload Injection",
    desc: "Malicious payload embedded in transaction memo field parsed by downstream reconciliation bots.",
    severity: "High",
    multiplier: "Corrupts automated accounting pipelines that ingest transaction descriptions.",
    icon: "message-square-code",
  },
  {
    n: 11,
    id: "V11",
    pillar: "Pillar 2: Synthetic Data & Obfuscation",
    pillarShort: "Pillar 2: Synthetic Data",
    name: "Multi-Turn Context Poisoning",
    desc: "Slowly poisons dialogue context over 10+ turns until system prompt guardrails decay.",
    severity: "High",
    multiplier: "Progressive semantic drift causes attention mechanisms to forget initial constraint tokens.",
    icon: "git-branch",
  },
  {
    n: 12,
    id: "V12",
    pillar: "Pillar 2: Synthetic Data & Obfuscation",
    pillarShort: "Pillar 2: Synthetic Data",
    name: "Multilingual Cross-Lingual Evasion",
    desc: "Translates malicious exploits into low-resource languages to evade English keyword filters.",
    severity: "Medium",
    multiplier: "Safety filters trained on English corpora fail to flag translated zero-day idioms.",
    icon: "globe",
  },
  {
    n: 13,
    id: "V13",
    pillar: "Pillar 2: Synthetic Data & Obfuscation",
    pillarShort: "Pillar 2: Synthetic Data",
    name: "Prompt Leaking & Architecture Recon",
    desc: "Extracts internal system prompts and threshold rules to calibrate subsequent zero-day attacks.",
    severity: "Medium",
    multiplier: "Provides attackers with exact decision boundary formulas and hardcoded threshold values.",
    icon: "scan-face",
  },
  {
    n: 14,
    id: "V14",
    pillar: "Pillar 2: Synthetic Data & Obfuscation",
    pillarShort: "Pillar 2: Synthetic Data",
    name: "Social Engineering Urgency Hijack",
    desc: "Simulates medical or repossession emergencies to pressure chatbot into instant limit increases.",
    severity: "High",
    multiplier: "Appeals to emotional safety heuristics to override standard cooling-off limits.",
    icon: "zap",
  },
  {
    n: 15,
    id: "V15",
    pillar: "Pillar 2: Synthetic Data & Obfuscation",
    pillarShort: "Pillar 2: Synthetic Data",
    name: "Jailbreak Roleplay 'DAN' Persona",
    desc: "Hypothetical fiction framing commanding the AI assistant to act unconstrained by compliance rules.",
    severity: "High",
    multiplier: "Virtual simulation wrappers isolate safety classifiers from recognizing live execution commands.",
    icon: "bot",
  },

  // ── Pillar 3: Multi-Rail & Digital Payment Exploits (7 Vectors) ──
  {
    n: 16,
    id: "V16",
    pillar: "Pillar 3: Multi-Rail & Digital Payment Exploits",
    pillarShort: "Pillar 3: Multi-Rail Payments",
    name: "Push Provisioning Hijack",
    desc: "Stolen card pushed to Apple/Google Pay bypassing OTP validation via hijacked sessions.",
    severity: "Critical",
    multiplier: "Attacker phone creates legitimate device token, bypassing CVV and 3DS challenge on subsequent taps.",
    icon: "smartphone",
  },
  {
    n: 17,
    id: "V17",
    pillar: "Pillar 3: Multi-Rail & Digital Payment Exploits",
    pillarShort: "Pillar 3: Multi-Rail Payments",
    name: "Ghost Tap & Contactless NFC Relay",
    desc: "APDU packet relay over cellular tunnel between modified POS terminal and accomplice smartphone.",
    severity: "Critical",
    multiplier: "Creates genuine cryptographic cryptograms miles away with only a sub-500ms network delay signature.",
    icon: "credit-card",
  },
  {
    n: 18,
    id: "V18",
    pillar: "Pillar 3: Multi-Rail & Digital Payment Exploits",
    pillarShort: "Pillar 3: Multi-Rail Payments",
    name: "BOPIS Mule Laundering",
    desc: "Buy Online, Pickup In Store laundering where mules collect high-value goods within minutes.",
    severity: "High",
    multiplier: "Bypasses delivery address verification; goods are retrieved before merchant fraud review triggers.",
    icon: "store",
  },
  {
    n: 19,
    id: "V19",
    pillar: "Pillar 3: Multi-Rail & Digital Payment Exploits",
    pillarShort: "Pillar 3: Multi-Rail Payments",
    name: "BNPL Synthetic Stacking",
    desc: "Simultaneous BNPL loan requests across multiple providers using thin-file synthetic credit profiles.",
    severity: "High",
    multiplier: "Exploits delayed credit bureau reporting windows across fintech micro-lenders.",
    icon: "activity",
  },
  {
    n: 20,
    id: "V20",
    pillar: "Pillar 3: Multi-Rail & Digital Payment Exploits",
    pillarShort: "Pillar 3: Multi-Rail Payments",
    name: "Refund-as-a-Service (RaaS) Syndicates",
    desc: "Organized Telegram syndicates filing systematic false 'item not received' chargebacks.",
    severity: "High",
    multiplier: "Social engineers carriers and merchants to issue full refunds while retaining high-value merchandise.",
    icon: "refresh-cw",
  },
  {
    n: 21,
    id: "V21",
    pillar: "Pillar 3: Multi-Rail & Digital Payment Exploits",
    pillarShort: "Pillar 3: Multi-Rail Payments",
    name: "Distributed Low-and-Slow BIN Enum",
    desc: "Low-velocity card testing distributed across thousands of residential IPs to evade velocity caps.",
    severity: "High",
    multiplier: "Bot networks distribute 1 attempt per IP every 6 hours, remaining completely invisible to local rate limits.",
    icon: "share-2",
  },
  {
    n: 22,
    id: "V22",
    pillar: "Pillar 3: Multi-Rail & Digital Payment Exploits",
    pillarShort: "Pillar 3: Multi-Rail Payments",
    name: "Synthetic Merchant Bust-Out",
    desc: "Collusive merchant account processes massive stolen card volume over 48h then drains payouts.",
    severity: "Critical",
    multiplier: "Fabricated sales velocity and clean onboarding documentation trick acquiring risk filters.",
    icon: "store",
  },

  // ── Pillar 4: Money Laundering & Network Topologies (7 Vectors) ──
  {
    n: 23,
    id: "V23",
    pillar: "Pillar 4: Money Laundering & Network Topologies",
    pillarShort: "Pillar 4: Money Mule Networks",
    name: "Multi-Hop Linear Mule Chain",
    desc: "Funds hopped sequentially through 4+ intermediate accounts to obfuscate initial injection source.",
    severity: "High",
    multiplier: "Dynamic pass-through (<30s delay) prevents transaction freezing at individual bank hops.",
    icon: "share-2",
  },
  {
    n: 24,
    id: "V24",
    pillar: "Pillar 4: Money Laundering & Network Topologies",
    pillarShort: "Pillar 4: Money Mule Networks",
    name: "Fan-Out Dispersal Sweep",
    desc: "High-value stolen balance fragmented into dozens of small transfers to retail mule accounts.",
    severity: "High",
    multiplier: "Dispersal amounts stay below \$2,000 to avoid mandatory real-time clearing surveillance.",
    icon: "git-branch",
  },
  {
    n: 25,
    id: "V25",
    pillar: "Pillar 4: Money Laundering & Network Topologies",
    pillarShort: "Pillar 4: Money Mule Networks",
    name: "Smurfing & Structuring Aggregation",
    desc: "Multiple sub-reporting-threshold cash deposits consolidated into a central funnel entity.",
    severity: "Critical",
    multiplier: "Synchronized agent swarms deposit \$9,500 increments simultaneously across geographical regions.",
    icon: "coins",
  },
  {
    n: 26,
    id: "V26",
    pillar: "Pillar 4: Money Laundering & Network Topologies",
    pillarShort: "Pillar 4: Money Mule Networks",
    name: "Round-Trip Wash Cycling",
    desc: "Circular transaction cycles across commercial shell companies creating fake legitimate turnover.",
    severity: "Critical",
    multiplier: "Graph cycles generate artificial invoice payments that justify offshore tax-haven wires.",
    icon: "refresh-cw",
  },
  {
    n: 27,
    id: "V27",
    pillar: "Pillar 4: Money Laundering & Network Topologies",
    pillarShort: "Pillar 4: Money Mule Networks",
    name: "Instant Micro-Smurfing (UPI/FedNow)",
    desc: "Automated sub-\$50 instant transfers executed across 20+ accounts in under 15 seconds.",
    severity: "Critical",
    multiplier: "Exploits zero-friction instant payment rails (FedNow/UPI) before batch graph engines run.",
    icon: "zap",
  },
  {
    n: 28,
    id: "V28",
    pillar: "Pillar 4: Money Laundering & Network Topologies",
    pillarShort: "Pillar 4: Money Mule Networks",
    name: "Chameleon Mule Network",
    desc: "Laundering transit hops buried inside 90% organic legitimate payroll and utility payments.",
    severity: "Critical",
    multiplier: "Blends illicit routing into everyday corporate payroll flows to defeat graph clustering algorithms.",
    icon: "shield-alert",
  },
  {
    n: 29,
    id: "V29",
    pillar: "Pillar 4: Money Laundering & Network Topologies",
    pillarShort: "Pillar 4: Money Mule Networks",
    name: "Crypto Off-Ramp Mixer Settlement",
    desc: "Fiat disbursements routed into decentralized OTC desks and non-custodial mixing protocols.",
    severity: "Critical",
    multiplier: "Cross-chain bridges and privacy mixers break deterministic ledger tracking.",
    icon: "shuffle",
  },

  // ── Pillar 5: Adversarial Evasion & Decision Boundary Probing (7 Vectors) ──
  {
    n: 30,
    id: "V30",
    pillar: "Pillar 5: Adversarial Evasion & Decision Boundary Probing",
    pillarShort: "Pillar 5: Adversarial Evasion",
    name: "Amount Micro-Structuring (\$1.99 Skirting)",
    desc: "Structures test transactions at \$1.99 or \$99.50 to skirt threshold-based rule triggers.",
    severity: "Medium",
    multiplier: "Exploits hardcoded merchant rule boundaries without triggering AML velocity limits.",
    icon: "credit-card",
  },
  {
    n: 31,
    id: "V31",
    pillar: "Pillar 5: Adversarial Evasion & Decision Boundary Probing",
    pillarShort: "Pillar 5: Adversarial Evasion",
    name: "Velocity Dilution & Bot Throttling",
    desc: "Throttles bot request cadence to match human inter-arrival times (1-2 tx/hour).",
    severity: "High",
    multiplier: "Dilutes statistical Poisson inter-arrival intervals into clean human distributions.",
    icon: "activity",
  },
  {
    n: 32,
    id: "V32",
    pillar: "Pillar 5: Adversarial Evasion & Decision Boundary Probing",
    pillarShort: "Pillar 5: Adversarial Evasion",
    name: "Device Score & Residential Geo-Spoofing",
    desc: "Manipulates client canvas telemetry and routes through clean residential proxies in cardholder zip.",
    severity: "High",
    multiplier: "Generates authentic WebGL/Canvas fingerprints from clean donor browser profiles.",
    icon: "globe",
  },
  {
    n: 33,
    id: "V33",
    pillar: "Pillar 5: Adversarial Evasion & Decision Boundary Probing",
    pillarShort: "Pillar 5: Adversarial Evasion",
    name: "Failed Attempt Masking & Age Inflation",
    desc: "Masks previous decline headers and spoof-inflates account age metrics.",
    severity: "Medium",
    multiplier: "Resets session cookies and injects clean synthetic transaction history headers.",
    icon: "refresh-cw",
  },
  {
    n: 34,
    id: "V34",
    pillar: "Pillar 5: Adversarial Evasion & Decision Boundary Probing",
    pillarShort: "Pillar 5: Adversarial Evasion",
    name: "Training Set Model Poisoning Backdoor",
    desc: "Injects trigger-pattern backdoor samples into synthetic training streams to create blind spots.",
    severity: "Critical",
    multiplier: "Creates specific feature trigger combinations (e.g. .77 cents + clean device) where fraud is labeled 0.",
    icon: "shield-alert",
  },
  {
    n: 35,
    id: "V35",
    pillar: "Pillar 5: Adversarial Evasion & Decision Boundary Probing",
    pillarShort: "Pillar 5: Adversarial Evasion",
    name: "Adaptive RL Decision Boundary Prober",
    desc: "Reinforcement learning bot iteratively queries model feedback to cluster features at 0.49 score.",
    severity: "Critical",
    multiplier: "Gradient-free policy search finds minimal feature shifts needed to cross below the 0.50 cutoff.",
    icon: "bot",
  },
  {
    n: 36,
    id: "V36",
    pillar: "Pillar 5: Adversarial Evasion & Decision Boundary Probing",
    pillarShort: "Pillar 5: Adversarial Evasion",
    name: "Black-Box Surrogate Boundary Probing",
    desc: "Trains local surrogate neural nets to compute adversarial transferability gradients against defense models.",
    severity: "Critical",
    multiplier: "Exploits decision boundary alignment between tree ensembles and neural surrogates.",
    icon: "cpu",
  },
];

export const datasets = [
  {
    title: "Tabular Card Fraud",
    count: 50000,
    unit: "transactions",
    lines: [
      "12 Sub-Types: Push Provisioning, NFC Relay, BOPIS, BNPL, RaaS, etc.",
      "15 Enterprise Features · 100% Domain Rule Pass (13 Rules)",
    ],
    icon: "table-2",
    accent: "cyan" as const,
  },
  {
    title: "Prompt Injection Text",
    count: 1500,
    unit: "prompts",
    lines: [
      "17 Threat Categories: Voice Clone, Safe Account, Invoice Forgery, MCP, etc.",
      "SentenceTransformer all-MiniLM-L6-v2 Semantic Embeddings",
    ],
    icon: "message-square-code",
    accent: "violet" as const,
  },
  {
    title: "Money Mule Graph Network",
    count: 7478,
    unit: "transfers",
    lines: [
      "7 Topologies: Instant Smurfing, Chameleon, Crypto Mixer, Chains, etc.",
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
      "7 Strategies: Model Poisoning, Adaptive RL, Black-Box Surrogate, etc.",
      "Active Learning Adversarial Holdout Preservation",
    ],
    icon: "crosshair",
    accent: "red" as const,
  },
];

export const terminalLines = [
  "$ python -m generate.run_pipeline --all-vectors",
  "",
  "[1/4] Generating Vector 5: Multi-Pattern Card Fraud (12 sub-types, 15 features)...",
  "      → Generated 50,000 rows (Push Provisioning, Ghost Tap, BOPIS, BNPL, RaaS). Pass Rate: 100.0%",
  "[2/4] Generating Vector 1: Prompt Injection Payloads (17 categories)...",
  "      → Generated 1,500 prompts across 17 categories. Pass Rate: 100.0%",
  "[3/4] Generating Vector 2: Multi-Topology Mule Graph (7 topologies)...",
  "      → Generated 7,478 transfers across 100 rings. Pass Rate: 100.0%",
  "[4/4] Generating Vector 8: Multi-Dimensional Adversarial Evasion (7 strategies)...",
  "      → Generated 50,000 perturbed rows. Pass Rate: 100.0%",
  "",
  "✓ Domain constraints satisfied across 4/4 vectors (38 rules evaluated).",
  "✓ TSTR fidelity verified against 20,000 real IEEE-CIS records.",
];

export const shapFeatures = [
  { name: "failed_attempts_24h", value: 12.8 },
  { name: "nfc_tap_latency_ms", value: 10.8 },
  { name: "bnpl_bureau_inquiries", value: 10.6 },
  { name: "geo_distance_km", value: 9.4 },
  { name: "device_risk_score", value: 7.4 },
  { name: "amount", value: 6.5 },
  { name: "is_decline", value: 6.0 },
  { name: "bopis_pickup_delay_min", value: 5.8 },
];

export const loopRows = [
  {
    metric: "Graph Topology Adversarial Catch Rate",
    r1: "39.8%",
    r2: "87.5%",
    delta: "+47.7% (+42 caught)",
    good: true,
  },
  {
    metric: "Graph AUC-PR (Adversarial Holdout)",
    r1: "0.7114",
    r2: "0.9404",
    delta: "+0.2290",
    good: true,
  },
  {
    metric: "Text Semantic Catch Rate (Paraphrased)",
    r1: "100.0%",
    r2: "100.0%",
    delta: "+9.19% Lift vs TF-IDF",
    good: true,
  },
  {
    metric: "Tabular AUC-PR (Adversarial Holdout)",
    r1: "0.7425",
    r2: "0.7531",
    delta: "+0.0106",
    good: true,
  },
  {
    metric: "Baseline False Positive Rate",
    r1: "0.97%",
    r2: "0.45%",
    delta: "-0.52% (FPR Halved)",
    good: true,
  },
  {
    metric: "Catastrophic Forgetting Audit",
    r1: "n/a",
    r2: "0.0% Drift",
    delta: "Verified Safe (Passed)",
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

export interface FAQItem {
  id: string;
  category: "Architecture & Workflow" | "ML & ONNX Engine" | "Closed Loop" | "Compliance & Defense";
  question: string;
  answer: string;
  highlight?: string;
}

export const faqItems: FAQItem[] = [
  {
    id: "faq-1",
    category: "Architecture & Workflow",
    question: "How does the end-to-end Red-Blue workflow operate?",
    answer:
      "SENTRIX AI operates as an automated 4-phase closed loop: (1) The Red Team synthetic engine generates 36 real-world threat vectors across conversational, gateway, and graph rails. (2) Heterogeneous Blue Team defense heads detect attacks in real time. (3) A model-aware prober discovers blind spots and auto-mines evasion samples (+4,683 cases). (4) The Active Retrainer incrementally updates the ONNX models, achieving +57 more caught attacks in Round 2 with zero catastrophic forgetting on legitimate transactions.",
    highlight: "Autonomous 4-phase loop: Simulate → Detect → Failure Mining → Active Retraining",
  },
  {
    id: "faq-2",
    category: "ML & ONNX Engine",
    question: "Why is the ONNX inference time 0.006ms and how does it meet banking SLAs?",
    answer:
      "Production fraud systems have strict sub-50ms SLA budgets. Traditional Python/PyTorch inference is throttled by GIL lock and heavy memory overhead. SENTRIX AI quantizes trained XGBoost models and compiles them into a standalone C++ ONNX Runtime engine. This enables direct CPU cache tensor evaluation in 0.0056ms — over 8,300x faster than required banking SLAs.",
    highlight: "C++ ONNX Runtime engine running at 0.0056ms SLA (8,300x faster than 50ms budget)",
  },
  {
    id: "faq-3",
    category: "Architecture & Workflow",
    question: "How is synthetic data verified to match real-world payment data?",
    answer:
      "Every generated record must satisfy 38 strict domain invariant rules (checking velocity limits, MCC risk weighting, diurnal sin/cos cycles, and conserved multi-hop graph flows). Statistical fidelity is evaluated using the Train-on-Synthetic, Test-on-Real (TSTR) protocol against 20,000 real IEEE-CIS benchmark records, achieving a 99.9% AUC-PR fidelity score without synthetic artifacts.",
    highlight: "100% Invariant pass rate across 38 domain rules + 99.9% TSTR AUC-PR on real IEEE-CIS records",
  },
  {
    id: "faq-4",
    category: "ML & ONNX Engine",
    question: "How does the Tri-Vector mathematical risk fusion formula work?",
    answer:
      "When an incoming transaction event occurs, it is evaluated across three decoupled modalities: NLP semantic injection probability (P_text), tabular gateway anomaly risk (P_tab), and graph topological ring score (P_graph). The fusion engine calculates joint risk using R_fused = 1 - ∏(1 - P_i) + Δ_synergy. If R_fused ≥ 0.80, an autonomous instant kill-switch freezes the card and halts wire dispersal.",
    highlight: "Correlated Bayesian fusion equation combining Chatbot + Gateway + Graph trails",
  },
  {
    id: "faq-5",
    category: "Closed Loop",
    question: "How does the active learning loop prevent catastrophic forgetting?",
    answer:
      "When retraining on newly discovered adversarial mutations, standard ML models risk degrading their accuracy on normal everyday transactions (catastrophic forgetting). SENTRIX AI enforces an automated dual-partition holdout audit. Round 2 models are tested against a preserved baseline validation set, confirming a 0.45% false positive rate (-0.67% drift), proving that new defenses do not introduce friction for legitimate cardholders.",
    highlight: "Dual-partition holdout audit ensuring -0.67% drift and 0.45% validation FPR",
  },
  {
    id: "faq-6",
    category: "Compliance & Defense",
    question: "Is SENTRIX AI strictly defense-only?",
    answer:
      "Yes. The synthetic generation module functions purely as an internal automated stress-testing harness (similar to a flight simulator for pilots) to validate defenses before criminals discover vulnerabilities. In production, SENTRIX AI operates strictly as an AI Risk Manager protecting merchants and cardholders from fraud loss, return abuse (RaaS), and chargebacks with asymmetric cost-loss threshold optimization.",
    highlight: "Strictly defense-only AI Risk Manager with asymmetric financial cost-loss optimization ($3,071 savings/batch)",
  },
];

export const navSections = [
  { id: "hero", label: "Overview" },
  { id: "identify", label: "Identify" },
  { id: "generate", label: "Generate" },
  { id: "defend", label: "Defend" },
  { id: "loop", label: "Closed Loop" },
  { id: "demo", label: "Live Demo" },
  { id: "faq", label: "FAQ" },
  { id: "team", label: "Team" },
];
