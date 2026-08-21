import { lazy, Suspense } from "react";
import { motion, useReducedMotion } from "motion/react";
import {
  ArrowRight,
  Check,
  Database,
  DollarSign,
  Shield,
  Sparkles,
  Target,
  Zap,
} from "lucide-react";
import { Counter } from "@/components/shared/Counter";
import { SentrixMark } from "@/components/shared/SentrixMark";
import { heroStats } from "@/data/content";

const ParticleField = lazy(() => import("@/components/shared/ParticleField"));

const icons = {
  shield: Shield,
  database: Database,
  target: Target,
  zap: Zap,
  dollar: DollarSign,
};

export function Hero() {
  const reduce = useReducedMotion();
  return (
    <section
      id="hero"
      className="snap-section relative flex min-h-screen w-full flex-col justify-center overflow-hidden px-5 pt-32 pb-20 sm:px-8 lg:px-16"
    >
      <div className="dot-backdrop absolute inset-0 opacity-45" />
      <Suspense fallback={null}>
        <ParticleField />
      </Suspense>
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(44% 46% at 35% 32%, rgb(235 0 27 / 10%), transparent 72%), radial-gradient(44% 46% at 66% 36%, rgb(247 158 27 / 16%), transparent 72%)",
        }}
      />
      <div
        className="absolute inset-x-0 bottom-0 h-40"
        style={{
          background: "linear-gradient(to bottom, transparent, var(--background))",
        }}
      />

      <div className="relative z-10 mx-auto grid w-full max-w-7xl items-center gap-14 lg:grid-cols-[1.08fr_0.92fr]">
        <div>
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            className="mb-7 inline-flex items-center gap-2 rounded-full border border-border bg-white/70 px-3 py-2 text-sm font-medium text-muted-foreground"
          >
            <Sparkles className="h-4 w-4 text-mc-red" /> Built for adaptive payment threats
          </motion.div>

          <h1 className="max-w-4xl text-5xl leading-[0.96] font-medium tracking-[-0.055em] text-balance sm:text-6xl lg:text-7xl">
            Fraud defense that <span className="text-mc-red">learns from the attack.</span>
          </h1>

          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9, duration: 0.6 }}
            className="mt-7 max-w-2xl text-base leading-relaxed text-foreground/70 sm:text-xl"
          >
            Sentrix simulates emerging scams across transactions, language, and money networks—then
            turns every missed attack into a stronger defense.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.1, duration: 0.6 }}
            className="mt-8 flex flex-wrap gap-3"
          >
            <a
              href="#demo"
              className="inline-flex items-center gap-2 rounded-xl bg-foreground px-5 py-3 text-sm font-semibold text-background transition hover:-translate-y-0.5"
            >
              Try the live defender <ArrowRight className="h-4 w-4" />
            </a>
            <a
              href="#identify"
              className="inline-flex items-center gap-2 rounded-xl border border-border bg-white/65 px-5 py-3 text-sm font-semibold text-foreground transition hover:bg-white"
            >
              Explore how it works
            </a>
          </motion.div>

          <div className="mt-10 flex flex-wrap gap-x-6 gap-y-2 text-sm text-muted-foreground">
            {["Three risk signals", "Explainable decisions", "Closed-loop learning"].map((item) => (
              <span key={item} className="inline-flex items-center gap-2">
                <Check className="h-4 w-4 text-mc-red" />
                {item}
              </span>
            ))}
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, x: reduce ? 0 : 24 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.25, duration: 0.7 }}
          className="glass-panel relative overflow-hidden rounded-[2rem] p-5 sm:p-7"
        >
          <div className="mb-6 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <SentrixMark className="h-12 w-12" />
              <div>
                <p className="text-sm font-semibold">Adaptive defense loop</p>
                <p className="text-xs text-muted-foreground">One decision, three signals</p>
              </div>
            </div>
            <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-[11px] font-semibold text-emerald-700">
              Live
            </span>
          </div>
          <div className="space-y-3">
            {[
              { n: "01", t: "Simulate", d: "Generate a realistic compound attack", c: "bg-mc-red" },
              {
                n: "02",
                t: "Detect",
                d: "Score text, transaction, and graph risk",
                c: "bg-mc-orange",
              },
              {
                n: "03",
                t: "Adapt",
                d: "Retrain on evasions without added friction",
                c: "bg-mc-yellow",
              },
            ].map((step) => (
              <div
                key={step.n}
                className="flex gap-4 rounded-2xl border border-border bg-white/65 p-4"
              >
                <span
                  className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${step.c} text-xs font-bold text-white`}
                >
                  {step.n}
                </span>
                <div>
                  <p className="text-sm font-semibold">{step.t}</p>
                  <p className="mt-0.5 text-sm text-muted-foreground">{step.d}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-5 rounded-2xl bg-foreground p-4 text-background">
            <div className="flex items-end justify-between gap-4">
              <div>
                <p className="text-xs text-background/60">Current protection</p>
                <p className="mt-1 text-2xl font-semibold">96.3% attacks caught</p>
              </div>
              <Shield className="h-7 w-7 text-mc-yellow" />
            </div>
          </div>
        </motion.div>

        <div className="mt-14 grid w-full grid-cols-2 gap-x-6 gap-y-5 border-t border-border pt-7 lg:col-span-2 lg:grid-cols-4">
          {heroStats.map((s, i) => {
            const Icon = icons[s.icon];
            return (
              <motion.div
                key={s.label}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.25 + i * 0.12, duration: 0.6 }}
                className="flex items-center gap-3 text-left"
              >
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white/70 shadow-sm">
                  <Icon className="h-5 w-5 text-mc-red" strokeWidth={1.75} />
                </div>
                <div>
                  <div className="text-xl font-semibold tracking-tight text-foreground sm:text-2xl">
                    <Counter
                      value={s.value}
                      decimals={s.decimals ?? 0}
                      prefix={s.prefix ?? ""}
                      suffix={s.suffix ?? ""}
                      delay={1400 + i * 120}
                    />
                  </div>
                  <div className="mt-0.5 text-xs text-muted-foreground">{s.label}</div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
