import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Zap,
  ShieldCheck,
  ShieldAlert,
  Crosshair,
  RefreshCw,
  Loader2,
  Check,
  ChevronRight,
  BarChart3,
  Database,
} from "lucide-react";
import { Reveal } from "@/components/shared/Section";
import { Counter } from "@/components/shared/Counter";
import {
  usePipelineGenerate,
  usePipelineTrain,
  usePipelineAttack,
  usePipelineRetrain,
  usePipelineEvaluate,
  usePipelineReset,
  type PipelineGenerateInput,
} from "@/hooks/useBackendMetrics";

type StepId = "setup" | "generate" | "train" | "attack" | "retrain" | "evaluate";

interface PipelineResults {
  generate?: {
    total_rows: number;
    fraud_count: number;
    legit_count: number;
    train_size?: number;
  };
  train?: { auc_pr: number; f1_score: number; fpr: number };
  attack?: { evasion_rate: number; r1_missed: number; total_adversarial: number };
  retrain?: {
    r2_auc_pr: number;
    evaded_samples_added: number;
    augmented_train_size: number;
  };
  evaluate?: {
    r1_caught: number;
    r2_caught: number;
    total_adversarial_eval: number;
    delta_caught: number;
    r1_catch_rate: number;
    r2_catch_rate: number;
    r1_baseline_auc: number;
    r2_baseline_auc: number;
    r1_baseline_fpr: number;
    baseline_stable: boolean;
  };
}

const STEPS: { id: StepId; label: string; icon: typeof Zap }[] = [
  { id: "setup", label: "Setup", icon: Database },
  { id: "generate", label: "Generate", icon: Zap },
  { id: "train", label: "Train R1", icon: ShieldCheck },
  { id: "attack", label: "Attack", icon: Crosshair },
  { id: "retrain", label: "Retrain R2", icon: RefreshCw },
  { id: "evaluate", label: "Compare", icon: BarChart3 },
];

/* ── Progress Bar ── */
function ProgressBar({ current }: { current: number }) {
  return (
    <div className="mb-8 flex items-center gap-1">
      {STEPS.map((step, i) => {
        const Icon = step.icon;
        const done = i < current;
        const active = i === current;
        return (
          <div key={step.id} className="flex items-center">
            <div
              className={`flex items-center gap-1.5 rounded-full px-3 py-1.5 font-mono text-[10px] uppercase tracking-wider transition-all ${
                done
                  ? "bg-cyan/15 text-cyan"
                  : active
                    ? "bg-ai-violet/15 text-ai-violet glow-violet"
                    : "text-muted-foreground/40"
              }`}
            >
              {done ? <Check className="h-3 w-3" /> : <Icon className="h-3 w-3" />}
              <span className="hidden sm:inline">{step.label}</span>
            </div>
            {i < STEPS.length - 1 && (
              <ChevronRight
                className={`mx-0.5 h-3 w-3 ${done ? "text-cyan/50" : "text-muted-foreground/20"}`}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}

/* ── Step Action Button ── */
function StepButton({
  label,
  onClick,
  loading,
  icon: Icon,
  accent = "cyan",
}: {
  label: string;
  onClick: () => void;
  loading: boolean;
  icon: typeof Zap;
  accent?: "cyan" | "violet" | "red" | "orange";
}) {
  const colors = {
    cyan: "bg-cyan/15 text-cyan hover:bg-cyan/25",
    violet: "bg-ai-violet/15 text-ai-violet hover:bg-ai-violet/25",
    red: "bg-mc-red/15 text-mc-red hover:bg-mc-red/25",
    orange: "bg-mc-orange/15 text-mc-orange hover:bg-mc-orange/25",
  };
  return (
    <button
      onClick={onClick}
      disabled={loading}
      className={`flex w-full items-center justify-center gap-2 rounded-xl px-4 py-3 font-mono text-sm transition-all disabled:opacity-50 ${colors[accent]}`}
    >
      {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Icon className="h-4 w-4" />}
      {loading ? "Processing..." : label}
    </button>
  );
}

/* ── Metric Badge ── */
function MetricBadge({
  label,
  value,
  accent = "cyan",
}: {
  label: string;
  value: string;
  accent?: "cyan" | "orange" | "red" | "violet";
}) {
  const cls = {
    cyan: "text-glow-cyan",
    orange: "text-glow-orange",
    red: "text-glow-red",
    violet: "text-ai-violet",
  };
  return (
    <div className="text-center">
      <div className={`font-mono text-2xl font-bold ${cls[accent]}`}>{value}</div>
      <div className="mt-1 text-[10px] uppercase tracking-wider text-muted-foreground">{label}</div>
    </div>
  );
}

/* ── Main LivePipeline Component ── */
export function LivePipeline() {
  const [currentStep, setCurrentStep] = useState(0);
  const [vector, setVector] = useState<"tabular" | "text" | "cross_vector">("tabular");
  const [selectedLLM, setSelectedLLM] = useState("openai/gpt-oss-120b");
  const [nSamples, setNSamples] = useState(30000);
  const [fraudPct, setFraudPct] = useState(0.15);

  const [results, setResults] = useState<PipelineResults>({});

  const generate = usePipelineGenerate();
  const train = usePipelineTrain();
  const attack = usePipelineAttack();
  const retrain = usePipelineRetrain();
  const evaluate = usePipelineEvaluate();
  const reset = usePipelineReset();

  const handleGenerate = () => {
    const input: PipelineGenerateInput = {
      vector,
      n_samples: nSamples,
      fraud_pct: fraudPct,
      ...(vector === "text" ? { llm_model: selectedLLM } : {}),
    };
    generate.mutate(input, {
      onSuccess: (data) => {
        setResults((r) => ({ ...r, generate: data }));
        setCurrentStep(2);
      },
    });
  };

  const handleTrain = () => {
    train.mutate(undefined, {
      onSuccess: (data) => {
        setResults((r) => ({ ...r, train: data }));
        setCurrentStep(3);
      },
    });
  };

  const handleAttack = () => {
    attack.mutate(undefined, {
      onSuccess: (data) => {
        setResults((r) => ({ ...r, attack: data }));
        setCurrentStep(4);
      },
    });
  };

  const handleRetrain = () => {
    retrain.mutate(undefined, {
      onSuccess: (data) => {
        setResults((r) => ({ ...r, retrain: data }));
        setCurrentStep(5);
      },
    });
  };

  const handleEvaluate = () => {
    evaluate.mutate(undefined, {
      onSuccess: (data) => {
        setResults((r) => ({ ...r, evaluate: data }));
        setCurrentStep(6);
      },
    });
  };

  const handleReset = () => {
    reset.mutate(undefined, {
      onSuccess: () => {
        setCurrentStep(0);
        setResults({});
        generate.reset();
        train.reset();
        attack.reset();
        retrain.reset();
        evaluate.reset();
      },
    });
  };

  const isLoading =
    generate.isPending ||
    train.isPending ||
    attack.isPending ||
    retrain.isPending ||
    evaluate.isPending;

  return (
    <div>
      <ProgressBar current={currentStep} />

      <AnimatePresence mode="wait">
        {/* STEP A: SETUP */}
        {currentStep === 0 && (
          <motion.div
            key="setup"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <div className="glass-panel rounded-2xl p-6">
              <h4 className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-muted-foreground">
                <Database className="h-4 w-4" /> Pipeline Configuration
              </h4>
              <div className="mt-5 space-y-5">
                {/* Attack Vector Selector */}
                <div>
                  <label className="text-xs text-muted-foreground block mb-2">
                    Select Target Threat Vector
                  </label>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                    <button
                      onClick={() => {
                        setVector("tabular");
                        setNSamples(30000);
                      }}
                      className={`flex flex-col rounded-xl p-3 text-left transition-all border ${
                        vector === "tabular"
                          ? "bg-cyan/15 border-cyan text-cyan shadow-sm shadow-cyan/20"
                          : "bg-secondary/40 border-transparent text-muted-foreground hover:bg-secondary"
                      }`}
                    >
                      <span className="font-mono text-xs font-semibold">
                        💳 Evasive Card Testing
                      </span>
                      <span className="text-[10px] opacity-70 mt-0.5">
                        9 domain features · ONNX XGBoost
                      </span>
                    </button>

                    <button
                      onClick={() => {
                        setVector("text");
                        setNSamples(150);
                      }}
                      className={`flex flex-col rounded-xl p-3 text-left transition-all border ${
                        vector === "text"
                          ? "bg-ai-violet/20 border-ai-violet text-ai-violet shadow-sm shadow-ai-violet/20"
                          : "bg-secondary/40 border-transparent text-muted-foreground hover:bg-secondary"
                      }`}
                    >
                      <span className="font-mono text-xs font-semibold">
                        💬 Prompt Injection (LLM)
                      </span>
                      <span className="text-[10px] opacity-70 mt-0.5">
                        Calibrated MiniLM · LLM Red Team
                      </span>
                    </button>

                    <button
                      onClick={() => {
                        setVector("cross_vector");
                        setNSamples(30000);
                      }}
                      className={`flex flex-col rounded-xl p-3 text-left transition-all border ${
                        vector === "cross_vector"
                          ? "bg-mc-orange/20 border-mc-orange text-mc-orange shadow-sm shadow-mc-orange/20"
                          : "bg-secondary/40 border-transparent text-muted-foreground hover:bg-secondary"
                      }`}
                    >
                      <span className="font-mono text-xs font-semibold">
                        ⚡ Cross-Vector Compound
                      </span>
                      <span className="text-[10px] opacity-70 mt-0.5">
                        Injection + Burst + Mule Network
                      </span>
                    </button>
                  </div>
                </div>

                {/* LLM Selector if Text Vector */}
                {vector === "text" && (
                  <div className="rounded-xl border border-ai-violet/30 bg-ai-violet/5 p-3.5">
                    <label className="text-[11px] font-mono text-foreground flex items-center justify-between mb-2">
                      <span>Red Team LLM Generator:</span>
                      <span className="text-[10px] text-cyan">
                        {selectedLLM.includes("gemini") ? "🌟 Google Gemini" : "⚡ Groq Cloud"}
                      </span>
                    </label>
                    <div className="grid grid-cols-2 gap-1.5 sm:grid-cols-4">
                      {[
                        { id: "openai/gpt-oss-120b", name: "GPT OSS 120B", provider: "groq" },
                        {
                          id: "gemini-3.5-flash-lite",
                          name: "Gemini 3.5 Flash Lite",
                          provider: "gemini",
                        },
                        {
                          id: "gemini-3.1-flash-lite",
                          name: "Gemini 3.1 Flash Lite",
                          provider: "gemini",
                        },
                        { id: "llama-3.3-70b-versatile", name: "Llama 3.3 70B", provider: "groq" },
                      ].map((m) => (
                        <button
                          key={m.id}
                          onClick={() => setSelectedLLM(m.id)}
                          className={`rounded-lg px-2.5 py-1.5 text-left text-xs font-mono transition-all ${
                            selectedLLM === m.id
                              ? m.provider === "gemini"
                                ? "bg-cyan/20 border border-cyan text-cyan"
                                : "bg-mc-orange/20 border border-mc-orange text-mc-orange"
                              : "bg-secondary/60 text-muted-foreground hover:bg-secondary hover:text-foreground"
                          }`}
                        >
                          <div className="text-[9px] uppercase tracking-wider opacity-60">
                            {m.provider === "gemini" ? "Google" : "Groq"}
                          </div>
                          <div className="font-semibold truncate">{m.name}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                <div>
                  <div className="flex items-baseline justify-between">
                    <label className="text-xs text-muted-foreground">Number of Samples</label>
                    <span className="font-mono text-sm text-cyan">{nSamples.toLocaleString()}</span>
                  </div>
                  <input
                    type="range"
                    min={vector === "text" ? 20 : 5000}
                    max={vector === "text" ? 350 : 60000}
                    step={vector === "text" ? 10 : 1000}
                    value={nSamples}
                    onChange={(e) => setNSamples(parseInt(e.target.value))}
                    className="mt-2 w-full accent-cyan"
                  />
                </div>
                <div>
                  <div className="flex items-baseline justify-between">
                    <label className="text-xs text-muted-foreground">Fraud Ratio</label>
                    <span className="font-mono text-sm text-cyan">
                      {(fraudPct * 100).toFixed(0)}%
                    </span>
                  </div>
                  <input
                    type="range"
                    min={0.05}
                    max={0.4}
                    step={0.01}
                    value={fraudPct}
                    onChange={(e) => setFraudPct(parseFloat(e.target.value))}
                    className="mt-2 w-full accent-cyan"
                  />
                </div>
                <div className="rounded-lg bg-secondary/50 p-3 text-xs text-muted-foreground">
                  <p>
                    <strong className="text-foreground">Pipeline Split:</strong> 60% train · 20%
                    validation · 10% mining · 10% untouched final holdout
                  </p>
                </div>
              </div>
              <div className="mt-6">
                <StepButton
                  label="⚡ Generate Attacks"
                  onClick={() => setCurrentStep(1)}
                  loading={false}
                  icon={Zap}
                />
              </div>
            </div>
          </motion.div>
        )}

        {/* STEP B: GENERATE */}
        {currentStep === 1 && (
          <motion.div
            key="generate"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <div className="glass-panel rounded-2xl p-6">
              <h4 className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-muted-foreground">
                <Zap className="h-4 w-4" /> Generating Synthetic Attacks
              </h4>
              <p className="mt-2 text-sm text-muted-foreground">
                Creating {nSamples.toLocaleString()}{" "}
                {vector === "text"
                  ? "prompt injection logs with " + selectedLLM
                  : "card testing transactions"}{" "}
                with {(fraudPct * 100).toFixed(0)}% fraud ratio...
              </p>
              <div className="mt-4">
                <StepButton
                  label="Generate Now"
                  onClick={handleGenerate}
                  loading={generate.isPending}
                  icon={Zap}
                />
              </div>
            </div>
          </motion.div>
        )}

        {/* STEP C: TRAIN R1 */}
        {currentStep === 2 && (
          <motion.div
            key="train"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              <div className="glass-panel rounded-2xl p-6">
                <h4 className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-cyan">
                  <Check className="h-4 w-4" /> Data Generated
                </h4>
                {results.generate && (
                  <div className="mt-4 grid grid-cols-3 gap-4">
                    <MetricBadge
                      label="Total Rows"
                      value={results.generate.total_rows.toLocaleString()}
                    />
                    <MetricBadge
                      label="Fraud"
                      value={results.generate.fraud_count.toString()}
                      accent="red"
                    />
                    <MetricBadge
                      label="Legit"
                      value={results.generate.legit_count.toString()}
                      accent="cyan"
                    />
                  </div>
                )}
              </div>
              <div className="glass-panel rounded-2xl p-6">
                <h4 className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-muted-foreground">
                  <ShieldCheck className="h-4 w-4" /> Train Round 1 Defender
                </h4>
                <p className="mt-2 text-sm text-muted-foreground">
                  {vector === "text"
                    ? "Sentence Transformers (all-MiniLM-L6-v2) + TF-IDF on "
                    : "XGBoost + Isolation Forest on "}
                  {results.generate?.train_size ?? "?"} training samples
                </p>
                <div className="mt-4">
                  <StepButton
                    label="🛡️ Train Round 1"
                    onClick={handleTrain}
                    loading={train.isPending}
                    icon={ShieldCheck}
                    accent="cyan"
                  />
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* STEP D: ATTACK */}
        {currentStep === 3 && (
          <motion.div
            key="attack"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              <div className="glass-panel rounded-2xl p-6">
                <h4 className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-cyan">
                  <Check className="h-4 w-4" /> Round 1 Trained
                </h4>
                {results.train && (
                  <div className="mt-4 grid grid-cols-3 gap-4">
                    <MetricBadge
                      label="AUC-PR"
                      value={`${(results.train.auc_pr * 100).toFixed(1)}%`}
                    />
                    <MetricBadge
                      label="F1-Score"
                      value={`${(results.train.f1_score * 100).toFixed(1)}%`}
                      accent="cyan"
                    />
                    <MetricBadge
                      label="FPR"
                      value={`${(results.train.fpr * 100).toFixed(1)}%`}
                      accent="orange"
                    />
                  </div>
                )}
              </div>
              <div className="glass-panel rounded-2xl p-6">
                <h4 className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-muted-foreground">
                  <Crosshair className="h-4 w-4" /> Adversarial Probing
                </h4>
                <p className="mt-2 text-sm text-muted-foreground">
                  {vector === "text"
                    ? "3 NLP evasion strategies: Conversational Framing, Admin Roleplay, Obfuscation"
                    : "3 tabular strategies: Velocity Dilution, Amount Structuring, Device Cloaking"}
                </p>
                <div className="mt-4">
                  <StepButton
                    label="🔴 Attack Round 1"
                    onClick={handleAttack}
                    loading={attack.isPending}
                    icon={Crosshair}
                    accent="red"
                  />
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* STEP E: RETRAIN */}
        {currentStep === 4 && (
          <motion.div
            key="retrain"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              <div className="glass-panel rounded-2xl border-mc-red/30 p-6">
                <h4 className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-mc-red">
                  <ShieldAlert className="h-4 w-4" /> Round 1 Blind Spots Found
                </h4>
                {results.attack && (
                  <div className="mt-4">
                    <div className="text-center">
                      <div className="font-mono text-3xl font-bold text-glow-red">
                        <Counter value={results.attack.evasion_rate} decimals={1} suffix="%" />
                      </div>
                      <div className="mt-1 text-xs text-muted-foreground">
                        Evasion Rate — R1 missed {results.attack.r1_missed}/
                        {results.attack.total_adversarial}
                      </div>
                    </div>
                  </div>
                )}
              </div>
              <div className="glass-panel rounded-2xl p-6">
                <h4 className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-muted-foreground">
                  <RefreshCw className="h-4 w-4" /> Retrain with Adversarial Data
                </h4>
                <p className="mt-2 text-sm text-muted-foreground">
                  Augmenting training data with {results.attack?.r1_missed ?? 0} evaded samples
                </p>
                <div className="mt-4">
                  <StepButton
                    label="🔄 Retrain Round 2"
                    onClick={handleRetrain}
                    loading={retrain.isPending}
                    icon={RefreshCw}
                    accent="violet"
                  />
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* STEP F: EVALUATE */}
        {currentStep === 5 && (
          <motion.div
            key="evaluate"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              <div className="glass-panel rounded-2xl p-6">
                <h4 className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-cyan">
                  <Check className="h-4 w-4" /> Round 2 Trained
                </h4>
                {results.retrain && (
                  <div className="mt-4 grid grid-cols-3 gap-4">
                    <MetricBadge
                      label="R2 AUC-PR"
                      value={`${(results.retrain.r2_auc_pr * 100).toFixed(1)}%`}
                    />
                    <MetricBadge
                      label="Samples Added"
                      value={`+${results.retrain.evaded_samples_added}`}
                      accent="violet"
                    />
                    <MetricBadge
                      label="Augmented Size"
                      value={results.retrain.augmented_train_size.toString()}
                      accent="cyan"
                    />
                  </div>
                )}
              </div>
              <div className="glass-panel rounded-2xl p-6">
                <h4 className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-muted-foreground">
                  <BarChart3 className="h-4 w-4" /> Final Evaluation
                </h4>
                <p className="mt-2 text-sm text-muted-foreground">
                  Testing R1 vs R2 on unseen adversarial holdout
                </p>
                <div className="mt-4">
                  <StepButton
                    label="📊 Run Final Comparison"
                    onClick={handleEvaluate}
                    loading={evaluate.isPending}
                    icon={BarChart3}
                    accent="orange"
                  />
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* RESULTS: THE MONEY SLIDE */}
        {currentStep === 6 && results.evaluate && (
          <motion.div
            key="results"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
          >
            {/* Headline */}
            <div className="mb-6 text-center">
              <div className="font-mono text-2xl font-bold leading-tight sm:text-4xl">
                <span className="text-glow-red">R1: {results.evaluate.r1_caught}</span>
                <span className="text-muted-foreground">
                  /{results.evaluate.total_adversarial_eval} caught
                </span>
                <span className="mx-3 text-muted-foreground">→</span>
                <span className="text-glow-cyan">R2: {results.evaluate.r2_caught}</span>
                <span className="text-muted-foreground">
                  /{results.evaluate.total_adversarial_eval} caught
                </span>
              </div>
              <p className="mt-2 font-mono text-lg text-glow-orange sm:text-xl">
                +{results.evaluate.delta_caught} more adversarial attacks caught
              </p>
            </div>

            {/* R1 vs R2 side-by-side */}
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div className="glass-panel rounded-2xl border-mc-red/30 p-6">
                <h4 className="font-mono text-xs uppercase tracking-wider text-mc-red">
                  Round 1 Defender
                </h4>
                <dl className="mt-4 space-y-3">
                  <div className="flex justify-between border-b border-glass-border pb-2 text-sm">
                    <dt className="text-muted-foreground">Catch Rate</dt>
                    <dd className="font-mono">{results.evaluate.r1_catch_rate}%</dd>
                  </div>
                  <div className="flex justify-between border-b border-glass-border pb-2 text-sm">
                    <dt className="text-muted-foreground">Baseline AUC</dt>
                    <dd className="font-mono">{results.evaluate.r1_baseline_auc}</dd>
                  </div>
                  <div className="flex justify-between text-sm">
                    <dt className="text-muted-foreground">Baseline FPR</dt>
                    <dd className="font-mono">
                      {(results.evaluate.r1_baseline_fpr * 100).toFixed(2)}%
                    </dd>
                  </div>
                </dl>
              </div>

              <div className="glass-panel glow-cyan rounded-2xl p-6">
                <h4 className="font-mono text-xs uppercase tracking-wider text-cyan">
                  Round 2 Defender
                </h4>
                <dl className="mt-4 space-y-3">
                  <div className="flex justify-between border-b border-glass-border pb-2 text-sm">
                    <dt className="text-muted-foreground">Catch Rate</dt>
                    <dd className="flex items-baseline gap-2 font-mono">
                      <span className="text-cyan">{results.evaluate.r2_catch_rate}%</span>
                      <span className="text-[11px] text-mc-orange">
                        +
                        {(results.evaluate.r2_catch_rate - results.evaluate.r1_catch_rate).toFixed(
                          1,
                        )}
                        %
                      </span>
                    </dd>
                  </div>
                  <div className="flex justify-between border-b border-glass-border pb-2 text-sm">
                    <dt className="text-muted-foreground">Baseline AUC</dt>
                    <dd className="font-mono text-cyan">{results.evaluate.r2_baseline_auc}</dd>
                  </div>
                  <div className="flex justify-between text-sm">
                    <dt className="text-muted-foreground">Forgetting</dt>
                    <dd className="font-mono text-cyan">
                      {results.evaluate.baseline_stable ? "None ✅" : "Detected ⚠️"}
                    </dd>
                  </div>
                </dl>
              </div>
            </div>

            {/* Reset Button */}
            <Reveal delay={0.3} className="mt-6 text-center">
              <button
                onClick={handleReset}
                disabled={isLoading}
                className="inline-flex items-center gap-2 rounded-full bg-secondary px-5 py-2 font-mono text-xs text-muted-foreground transition-all hover:text-foreground"
              >
                <RefreshCw className="h-3 w-3" />
                Run Again with Different Settings
              </button>
            </Reveal>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
