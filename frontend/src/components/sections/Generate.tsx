import { useEffect, useRef, useState } from "react";
import { motion, useInView, useReducedMotion } from "motion/react";
import {
  CheckCircle2,
  Crosshair,
  MessageSquareCode,
  Network,
  ShieldCheck,
  Table2,
} from "lucide-react";
import { Reveal, SectionTitle } from "@/components/shared/Section";
import { Counter } from "@/components/shared/Counter";
import { datasets, terminalLines } from "@/data/content";

const icons: Record<string, typeof Table2> = {
  "table-2": Table2,
  "message-square-code": MessageSquareCode,
  network: Network,
  crosshair: Crosshair,
};

const accentText = {
  cyan: "text-cyan",
  violet: "text-ai-violet",
  orange: "text-mc-orange",
  red: "text-mc-red",
};

function TerminalWindow() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-10% 0px" });
  const reduce = useReducedMotion();
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (!inView) return;
    if (reduce) {
      setCount(terminalLines.length);
      return;
    }
    let i = 0;
    const id = window.setInterval(() => {
      i += 1;
      setCount(i);
      if (i >= terminalLines.length) window.clearInterval(id);
    }, 420);
    return () => window.clearInterval(id);
  }, [inView, reduce]);

  return (
    <div ref={ref} className="glass-panel flex h-full flex-col overflow-hidden rounded-2xl">
      <div className="flex items-center gap-2 border-b border-glass-border px-4 py-3">
        <span className="h-2.5 w-2.5 rounded-full bg-mc-red/80" />
        <span className="h-2.5 w-2.5 rounded-full bg-mc-orange/80" />
        <span className="h-2.5 w-2.5 rounded-full bg-cyan/80" />
        <span className="ml-2 font-mono text-[11px] text-muted-foreground">
          redteam@fraud-shield — generate.py
        </span>
      </div>
      <div className="min-h-[320px] flex-1 p-4 font-mono text-[11px] leading-relaxed sm:text-xs">
        {terminalLines.slice(0, count).map((line, i) => (
          <div
            key={i}
            className={
              line.trimStart().startsWith("→")
                ? "text-cyan"
                : line.startsWith("✓")
                  ? "text-mc-orange"
                  : line.startsWith("$")
                    ? "text-foreground"
                    : "text-foreground/70"
            }
          >
            {line || "\u00A0"}
          </div>
        ))}
        {count < terminalLines.length && (
          <span className="inline-block h-3 w-2 bg-cyan align-middle motion-safe:animate-pulse" />
        )}
      </div>
      <div className="grid gap-3 border-t border-glass-border bg-white/45 p-4 sm:grid-cols-2">
        <div className="flex items-start gap-3 rounded-xl border border-border/70 bg-white/70 p-3">
          <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-mc-red" />
          <div>
            <p className="text-sm font-semibold">4 of 4 vectors validated</p>
            <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">
              Domain rules passed across every generated dataset.
            </p>
          </div>
        </div>
        <div className="flex items-start gap-3 rounded-xl border border-border/70 bg-white/70 p-3">
          <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-mc-orange" />
          <div>
            <p className="text-sm font-semibold">Production fidelity checked</p>
            <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">
              Compared against 20,000 real IEEE-CIS transactions.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export function Generate() {
  return (
    <section
      id="generate"
      className="snap-section relative flex min-h-screen w-full flex-col justify-center overflow-hidden px-5 py-24 sm:px-8 lg:px-16"
    >
      <div className="grid-backdrop absolute inset-0 opacity-40" />
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(45% 45% at 85% 20%, color-mix(in oklab, var(--mc-orange) 14%, transparent), transparent 70%)",
        }}
      />

      <div className="relative z-10 mx-auto w-full max-w-7xl">
        <SectionTitle
          eyebrow="02 · Red team"
          title="Train against attacks that do not exist yet."
          description="Generate realistic payment, language, graph, and evasion data with measurable fidelity—not generic synthetic noise."
          accent="orange"
        />

        <div className="grid grid-cols-1 items-stretch gap-6 lg:grid-cols-2">
          <Reveal className="h-full">
            <TerminalWindow />
          </Reveal>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:auto-rows-fr">
            {datasets.map((d, i) => {
              const Icon = icons[d.icon] ?? Table2;
              return (
                <Reveal key={d.title} delay={i * 0.1} className="h-full">
                  <div className="glass-panel tilt-card h-full rounded-2xl p-5">
                    <Icon className={`mb-3 h-5 w-5 ${accentText[d.accent]}`} strokeWidth={1.75} />
                    <h3 className="text-sm font-semibold">{d.title}</h3>
                    <div className="mt-3 font-mono text-2xl font-semibold text-glow-cyan">
                      <Counter value={d.count} />
                    </div>
                    <div className="font-mono text-[10px] tracking-wider text-muted-foreground uppercase">
                      {d.unit}
                    </div>
                    <ul className="mt-3 space-y-1 text-xs text-muted-foreground">
                      {d.lines.map((l) => (
                        <li key={l}>{l}</li>
                      ))}
                    </ul>
                  </div>
                </Reveal>
              );
            })}
          </div>
        </div>

        <Reveal delay={0.15} className="mt-6">
          <div className="glass-panel rounded-2xl p-6">
            <h3 className="font-mono text-xs tracking-[0.24em] text-cyan uppercase">
              Fidelity Benchmark
            </h3>
            <div className="mt-5 grid grid-cols-1 gap-6 md:grid-cols-3">
              <div>
                <div className="text-sm font-semibold">TSTR Score</div>
                <p className="mt-1 text-xs text-muted-foreground">
                  Trained on Synthetic → Tested on 20,000 Real IEEE-CIS Production Transactions
                </p>
              </div>
              <div>
                <div className="text-sm font-semibold">Domain Constraint Pass Rate</div>
                <div className="mt-1 font-mono text-2xl font-semibold text-glow-cyan">
                  <Counter value={100} suffix="%" />
                </div>
                <p className="text-xs text-muted-foreground">across all 4 vectors</p>
              </div>
              <div>
                <div className="text-sm font-semibold">Wasserstein Distance</div>
                <dl className="mt-2 space-y-1 font-mono text-xs text-muted-foreground">
                  <div className="flex justify-between gap-4">
                    <dt>amount</dt>
                    <dd className="text-foreground">21.36</dd>
                  </div>
                  <div className="flex justify-between gap-4">
                    <dt>velocity</dt>
                    <dd className="text-foreground">4.18</dd>
                  </div>
                  <div className="flex justify-between gap-4">
                    <dt>device_risk</dt>
                    <dd className="text-foreground">0.27</dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
