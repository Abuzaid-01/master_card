import { motion } from "motion/react";
import { Reveal, SectionTitle } from "@/components/shared/Section";
import { Counter } from "@/components/shared/Counter";
import { loopRows, loopStages } from "@/data/content";

function LoopDiagram() {
  return (
    <div className="relative mx-auto w-full max-w-3xl">
      <svg viewBox="0 0 400 200" className="w-full" aria-hidden="true">
        <ellipse
          cx="200"
          cy="100"
          rx="160"
          ry="70"
          fill="none"
          stroke="var(--ai-violet)"
          strokeOpacity="0.35"
          strokeWidth="1.5"
          strokeDasharray="7 7"
        />
        <motion.ellipse
          cx="200"
          cy="100"
          rx="160"
          ry="70"
          fill="none"
          stroke="var(--ai-violet)"
          strokeWidth="2.5"
          strokeLinecap="round"
          style={{ filter: "drop-shadow(0 0 6px var(--ai-violet))" }}
          strokeDasharray="90 650"
          animate={{ strokeDashoffset: [0, -740] }}
          transition={{ duration: 6, repeat: Infinity, ease: "linear" }}
        />
        {[0, 1, 2].map((i) => {
          const steps = 24;
          const cx: number[] = [];
          const cy: number[] = [];
          for (let s = 0; s <= steps; s++) {
            const t = (s / steps) * Math.PI * 2;
            cx.push(200 + 160 * Math.cos(t));
            cy.push(100 + 70 * Math.sin(t));
          }
          return (
            <motion.circle
              key={i}
              r="4"
              fill={i === 1 ? "var(--mc-orange)" : "var(--neon-cyan)"}
              animate={{ cx, cy }}
              transition={{
                duration: 6,
                repeat: Infinity,
                ease: "linear",
                delay: i * 2,
              }}
            />
          );
        })}
      </svg>


      <div className="mt-6 flex flex-wrap items-center justify-center gap-2">
        {loopStages.map((s, i) => (
          <motion.div
            key={s}
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.12, duration: 0.4 }}
            className="glass-panel rounded-full px-3 py-1.5 font-mono text-[10px] tracking-wider uppercase sm:text-[11px]"
          >
            <span className={i >= 4 ? "text-cyan" : "text-foreground/80"}>
              {s}
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

export function ClosedLoop() {
  return (
    <section
      id="loop"
      className="snap-section relative flex min-h-screen w-full flex-col justify-center overflow-hidden px-5 py-24 sm:px-8 lg:px-16"
    >
      <div className="dot-backdrop absolute inset-0 opacity-50" />
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(55% 50% at 50% 50%, color-mix(in oklab, var(--ai-violet) 20%, transparent), transparent 72%)",
        }}
      />

      <div className="relative z-10 mx-auto w-full max-w-6xl">
        <SectionTitle
          eyebrow="Step 4 · Close the Loop"
          title="Adversarial Active Learning"
          accent="violet"
        />

        <LoopDiagram />

        <Reveal className="mt-12 text-center">
          <div className="font-mono text-3xl leading-tight font-bold sm:text-5xl">
            <span className="text-glow-red">
              Round 1: <Counter value={3} />
            </span>
            <span className="text-muted-foreground">/45 caught</span>
            <span className="mx-3 text-muted-foreground">→</span>
            <span className="text-glow-cyan">
              Round 2: <Counter value={29} delay={1200} />
            </span>
            <span className="text-muted-foreground">/45 caught</span>
          </div>
          <p className="mt-4 font-mono text-lg text-glow-orange sm:text-2xl">
            +26 more adversarial attacks caught
          </p>
          <p className="mt-2 font-mono text-sm text-muted-foreground sm:text-base">
            AUC-PR: 0.653 → 0.917 (+40.4%)
          </p>
        </Reveal>

        <div className="mt-12 grid grid-cols-1 gap-4 md:grid-cols-2">
          <Reveal>
            <div className="glass-panel h-full rounded-2xl border-mc-red/30 p-6">
              <h3 className="font-mono text-xs tracking-[0.24em] text-mc-red uppercase">
                Round 1 Defender
              </h3>
              <dl className="mt-4 space-y-3">
                {loopRows.map((r) => (
                  <div
                    key={r.metric}
                    className="flex items-baseline justify-between gap-4 border-b border-glass-border pb-2 text-sm last:border-0"
                  >
                    <dt className="text-muted-foreground">{r.metric}</dt>
                    <dd className="font-mono">{r.r1}</dd>
                  </div>
                ))}
              </dl>
            </div>
          </Reveal>

          <Reveal delay={0.2}>
            <div className="glass-panel glow-cyan h-full rounded-2xl p-6">
              <h3 className="font-mono text-xs tracking-[0.24em] text-cyan uppercase">
                Round 2 Defender
              </h3>
              <dl className="mt-4 space-y-3">
                {loopRows.map((r) => (
                  <div
                    key={r.metric}
                    className="flex items-baseline justify-between gap-4 border-b border-glass-border pb-2 text-sm last:border-0"
                  >
                    <dt className="text-muted-foreground">{r.metric}</dt>
                    <dd className="flex items-baseline gap-3 font-mono">
                      <span className="text-cyan">{r.r2}</span>
                      <span className="text-[11px] text-mc-orange">
                        {r.delta}
                      </span>
                    </dd>
                  </div>
                ))}
              </dl>
            </div>
          </Reveal>
        </div>

        <Reveal delay={0.15} className="mt-6">
          <blockquote className="glass-panel glow-orange rounded-2xl border-l-4 border-mc-orange p-6 text-sm leading-relaxed text-foreground/90 sm:text-base">
            Round 2 catches 26 more unseen adversarial evasion attacks while
            simultaneously <span className="text-glow-orange">REDUCING</span>{" "}
            false positives on legitimate cardholders from 2.82% → 1.72%. Zero
            catastrophic forgetting.
          </blockquote>
        </Reveal>
      </div>
    </section>
  );
}
