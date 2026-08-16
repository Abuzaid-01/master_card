import { lazy, Suspense, useEffect, useState } from "react";
import { motion, useReducedMotion } from "motion/react";
import { ChevronDown, Database, DollarSign, Shield, Zap } from "lucide-react";
import { Counter } from "@/components/shared/Counter";
import { MastercardMark } from "@/components/shared/MastercardMark";
import { heroStats } from "@/data/content";

const ParticleField = lazy(() => import("@/components/shared/ParticleField"));

const icons = {
  shield: Shield,
  database: Database,
  zap: Zap,
  dollar: DollarSign,
};

const TITLE = "GenAI Fraud Shield";

function GlitchTitle() {
  const reduce = useReducedMotion();
  const [len, setLen] = useState(reduce ? TITLE.length : 0);

  useEffect(() => {
    if (reduce) return;
    let i = 0;
    const id = window.setInterval(() => {
      i += 1;
      setLen(i);
      if (i >= TITLE.length) window.clearInterval(id);
    }, 55);
    return () => window.clearInterval(id);
  }, [reduce]);

  const done = len >= TITLE.length;

  return (
    <h1 className="relative text-4xl leading-[0.95] font-bold tracking-tight sm:text-6xl lg:text-7xl">
      <span className="text-glow-cyan">{TITLE.slice(0, len)}</span>
      {!done && (
        <span className="ml-1 inline-block h-[0.85em] w-[3px] translate-y-[0.08em] bg-cyan align-middle motion-safe:animate-pulse" />
      )}
      {done && (
        <span
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 text-mc-red opacity-30 mix-blend-screen motion-safe:animate-[pulse_2.6s_ease-in-out_infinite]"
          style={{ transform: "translate(2px, -2px)" }}
        >
          {TITLE}
        </span>
      )}
    </h1>
  );
}

export function Hero() {
  return (
    <section
      id="hero"
      className="snap-section relative flex min-h-screen w-full flex-col items-center justify-center overflow-hidden px-5 py-28 sm:px-8"
    >
      <div className="dot-backdrop absolute inset-0 opacity-70" />
      <Suspense fallback={null}>
        <ParticleField />
      </Suspense>
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(60% 55% at 50% 40%, color-mix(in oklab, var(--ai-violet) 22%, transparent), transparent 70%)",
        }}
      />
      <div
        className="absolute inset-x-0 bottom-0 h-40"
        style={{
          background:
            "linear-gradient(to bottom, transparent, var(--background))",
        }}
      />

      <div className="relative z-10 mx-auto flex w-full max-w-6xl flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.85 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7 }}
          className="mb-8"
        >
          <MastercardMark className="h-12 w-20" pulse />
        </motion.div>

        <GlitchTitle />

        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9, duration: 0.6 }}
          className="mt-6 max-w-3xl text-base text-balance text-foreground/85 sm:text-xl"
        >
          Adversarial Red–Blue Team Defense Engine for Next-Generation Payment
          Fraud
        </motion.p>

        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.1, duration: 0.6 }}
          className="mt-4 font-mono text-[11px] tracking-[0.24em] text-muted-foreground uppercase sm:text-xs"
        >
          Mastercard Innovation Challenge 2026 — Global Fintech Fest, Mumbai
        </motion.p>

        <div className="mt-14 grid w-full grid-cols-2 gap-4 lg:grid-cols-4">
          {heroStats.map((s, i) => {
            const Icon = icons[s.icon];
            return (
              <motion.div
                key={s.label}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.25 + i * 0.12, duration: 0.6 }}
                className="glass-panel tilt-card rounded-2xl p-5 text-left"
              >
                <Icon className="mb-4 h-5 w-5 text-cyan" strokeWidth={1.75} />
                <div className="font-mono text-2xl font-semibold text-glow-cyan sm:text-3xl">
                  <Counter
                    value={s.value}
                    decimals={s.decimals ?? 0}
                    prefix={s.prefix ?? ""}
                    suffix={s.suffix ?? ""}
                    delay={1400 + i * 120}
                  />
                </div>
                <div className="mt-1 text-xs text-muted-foreground sm:text-sm">
                  {s.label}
                </div>
              </motion.div>
            );
          })}
        </div>

        <motion.a
          href="#identify"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2 }}
          className="mt-16 flex flex-col items-center gap-2 font-mono text-[11px] tracking-[0.24em] text-muted-foreground uppercase transition-colors hover:text-cyan"
        >
          Scroll to explore
          <motion.span
            animate={{ y: [0, 7, 0] }}
            transition={{ duration: 1.6, repeat: Infinity }}
          >
            <ChevronDown className="h-4 w-4" />
          </motion.span>
        </motion.a>
      </div>
    </section>
  );
}
