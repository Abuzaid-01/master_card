import { useEffect, useRef, useState } from "react";
import { motion, useInView, useReducedMotion } from "motion/react";
import {
  Crosshair,
  MessageSquareCode,
  Network,
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
    <div ref={ref} className="glass-panel overflow-hidden rounded-2xl">
      <div className="flex items-center gap-2 border-b border-glass-border px-4 py-3">
        <span className="h-2.5 w-2.5 rounded-full bg-mc-red/80" />
        <span className="h-2.5 w-2.5 rounded-full bg-mc-orange/80" />
        <span className="h-2.5 w-2.5 rounded-full bg-cyan/80" />
        <span className="ml-2 font-mono text-[11px] text-muted-foreground">
          redteam@fraud-shield — generate.py
        </span>
      </div>
      <div className="min-h-[320px] p-4 font-mono text-[11px] leading-relaxed sm:text-xs">
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
          eyebrow="Pillar 2 · Generate"
          title="AI Red Team Attack Engine"
          accent="orange"
        />

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <Reveal>
            <TerminalWindow />
          </Reveal>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {datasets.map((d, i) => {
              const Icon = icons[d.icon] ?? Table2;
              return (
                <Reveal key={d.title} delay={i * 0.1}>
                  <div className="glass-panel tilt-card h-full rounded-2xl p-5">
                    <Icon
                      className={`mb-3 h-5 w-5 ${accentText[d.accent]}`}
                      strokeWidth={1.75}
                    />
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
                  Trained on Synthetic → Tested on 20,000 Real IEEE-CIS
                  Mastercard Transactions
                </p>
              </div>
              <div>
                <div className="text-sm font-semibold">
                  Domain Constraint Pass Rate
                </div>
                <div className="mt-1 font-mono text-2xl font-semibold text-glow-cyan">
                  <Counter value={100} suffix="%" />
                </div>
                <p className="text-xs text-muted-foreground">
                  across all 4 vectors
                </p>
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
