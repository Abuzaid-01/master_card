import { ArrowUpRight, MessagesSquare, Network, ShieldCheck } from "lucide-react";
import { Reveal, SectionTitle } from "@/components/shared/Section";
import { Counter } from "@/components/shared/Counter";
import { GaugeRing } from "@/components/shared/GaugeRing";
import { NodeGraph } from "@/components/shared/NodeGraph";
import { shapFeatures } from "@/data/content";

function Bar({
  label,
  percent,
  value,
  accent,
}: {
  label: string;
  percent: number;
  value: string;
  accent: "cyan" | "muted" | "orange";
}) {
  const fill = {
    cyan: "bg-cyan",
    muted: "bg-muted-foreground/50",
    orange: "bg-mc-orange",
  }[accent];

  return (
    <div>
      <div className="flex items-baseline justify-between text-xs">
        <span className="text-muted-foreground">{label}</span>
        <span className="font-mono text-foreground">{value}</span>
      </div>
      <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-secondary">
        <div
          className={`h-full rounded-full ${fill}`}
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}

export function Defend() {
  return (
    <section
      id="defend"
      className="snap-section relative flex min-h-screen w-full flex-col justify-center overflow-hidden px-5 py-24 sm:px-8 lg:px-16"
    >
      <div className="grid-backdrop absolute inset-0 opacity-40" />
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(50% 45% at 25% 90%, color-mix(in oklab, var(--neon-cyan) 12%, transparent), transparent 70%)",
        }}
      />

      <div className="relative z-10 mx-auto w-full max-w-7xl">
        <SectionTitle
          eyebrow="03 · Defense"
          title="One decision layer across every risk signal."
          description="Specialized detectors explain what they see, while a shared risk layer keeps customer friction and financial loss in view."
          accent="cyan"
        />

        <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
          <Reveal>
            <div className="glass-panel tilt-card h-full rounded-2xl p-6">
              <ShieldCheck className="h-6 w-6 text-cyan" strokeWidth={1.6} />
              <h3 className="mt-4 text-base font-semibold">Tabular Card Testing Detector</h3>
              <p className="mt-1 font-mono text-[11px] text-muted-foreground">
                XGBoost + Isolation Forest → ONNX Runtime
              </p>

              <div className="mt-6">
                <div className="font-mono text-4xl font-semibold text-glow-cyan">
                  <Counter value={100.0} decimals={1} suffix="%" />
                </div>
                <div className="font-mono text-[10px] tracking-[0.2em] text-muted-foreground uppercase">
                  AUC-PR
                </div>
              </div>

              <div className="mt-6 space-y-4">
                <GaugeRing percent={100.0} value="100.0%" label="F1-Score" />
                <GaugeRing
                  percent={0.01}
                  value="0.00%"
                  label="False Positive Rate"
                  accent="orange"
                />
              </div>

              <div className="mt-6 border-t border-glass-border pt-4">
                <div className="font-mono text-2xl font-semibold text-glow-cyan">
                  <Counter value={0.008} decimals={3} suffix="ms" />
                </div>
                <div className="mt-1 text-xs text-muted-foreground">
                  ONNX latency — 6,000× faster than the 50ms SLA
                </div>
                <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-secondary">
                  <div
                    className="h-full rounded-full bg-cyan"
                    style={{ width: "3%" }}
                  />
                </div>
              </div>
            </div>
          </Reveal>

          <Reveal delay={0.12}>
            <div className="glass-panel tilt-card h-full rounded-2xl p-6">
              <MessagesSquare className="h-6 w-6 text-ai-violet" strokeWidth={1.6} />
              <h3 className="mt-4 text-base font-semibold">Text Prompt Injection Detector</h3>
              <p className="mt-1 font-mono text-[11px] text-muted-foreground">
                Sentence Transformers (all-MiniLM-L6-v2) vs TF-IDF baseline
              </p>

              <div className="mt-8 space-y-5">
                <Bar label="TF-IDF on paraphrased" percent={89.6} value="89.6%" accent="muted" />
                <Bar label="Semantic on paraphrased" percent={98.8} value="98.8%" accent="cyan" />
              </div>

              <div
                className="glow-cyan mt-8 inline-flex items-center gap-2 rounded-full bg-cyan/10 px-3 py-1.5"
              >
                <span>
                  <ArrowUpRight className="h-4 w-4 text-cyan" />
                </span>
                <span className="font-mono text-sm font-semibold text-cyan">+10.17% lift</span>
              </div>
              <p className="mt-4 text-xs text-muted-foreground">
                Semantic embeddings hold up when attackers paraphrase, where lexical baselines
                collapse.
              </p>
            </div>
          </Reveal>

          <Reveal delay={0.24}>
            <div className="glass-panel tilt-card h-full rounded-2xl p-6">
              <Network className="h-6 w-6 text-mc-orange" strokeWidth={1.6} />
              <h3 className="mt-4 text-base font-semibold">Graph Money Mule Detector</h3>
              <p className="mt-1 font-mono text-[11px] text-muted-foreground">
                GBDT on topological features — in-degree, out-degree, funnel score
              </p>

              <div className="mt-6">
                <div className="font-mono text-4xl font-semibold text-glow-cyan">
                  <Counter value={94.5} decimals={1} suffix="%" />
                </div>
                <div className="font-mono text-[10px] tracking-[0.2em] text-muted-foreground uppercase">
                  AUC-PR
                </div>
              </div>

              <div className="mt-6">
                <GaugeRing percent={87.3} value="87.3%" label="F1-Score" />
              </div>

              <div className="mt-6 border-t border-glass-border pt-4">
                <NodeGraph />
                <p className="mt-1 text-center font-mono text-[10px] text-muted-foreground">
                  funnel account detected at ring terminus
                </p>
              </div>
            </div>
          </Reveal>
        </div>

        <Reveal delay={0.15} className="mt-6">
          <div className="glass-panel rounded-2xl p-6">
            <h3 className="font-mono text-xs tracking-[0.24em] text-mc-orange uppercase">
              Financial Impact
            </h3>
            <div className="mt-5 grid grid-cols-1 gap-8 lg:grid-cols-2">
              <div className="space-y-5">
                <div>
                  <div className="text-sm font-semibold">Cost Optimizer</div>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Optimal threshold <span className="font-mono text-foreground">τ* = 0.21</span>{" "}
                    saves{" "}
                    <span className="font-mono font-semibold text-glow-orange">
                      <Counter value={3060.79} decimals={2} prefix="$" />
                    </span>{" "}
                    per batch.
                  </p>
                </div>
                <div>
                  <div className="text-sm font-semibold">Explainability</div>
                  <p className="mt-1 text-sm text-muted-foreground">
                    PCI-DSS compliant SHAP waterfall — top feature:{" "}
                    <span className="font-mono text-cyan">geo_distance_km (45.2%)</span>
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                {shapFeatures.map((f) => (
                  <div key={f.name}>
                    <div className="flex items-baseline justify-between font-mono text-[11px]">
                      <span className="text-muted-foreground">{f.name}</span>
                      <span>{f.value}%</span>
                    </div>
                    <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-secondary">
                      <div
                        className="h-full rounded-full"
                        style={{
                          background: "linear-gradient(90deg, var(--ai-violet), var(--neon-cyan))",
                          width: `${f.value}%`,
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
