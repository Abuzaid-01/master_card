import { lazy, Suspense, useEffect, useRef, useState } from "react";
import { motion, useReducedMotion } from "motion/react";
import { ChevronDown, Database, DollarSign, Shield, Zap, Sparkles, ArrowRight } from "lucide-react";
import { Counter } from "@/components/shared/Counter";
import { heroStats } from "@/data/content";

const ParticleField = lazy(() => import("@/components/shared/ParticleField"));

const icons = {
  shield: Shield,
  database: Database,
  zap: Zap,
  dollar: DollarSign,
};

const TITLE = "SENTRIX AI";

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
    <h1 className="relative text-4xl leading-[0.95] font-extrabold tracking-tight sm:text-6xl lg:text-7xl drop-shadow-[0_4px_24px_rgba(0,0,0,0.95)]">
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
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.play().catch(() => {
        // Autoplay may need user gesture in strict browser modes
      });
    }
  }, []);

  return (
    <section
      id="hero"
      className="snap-section relative flex min-h-screen w-full flex-col items-center justify-center overflow-hidden px-5 pt-16 pb-20 sm:px-8 sm:pt-20 sm:pb-28"
    >
      {/* ── Background Video Layer (Moon & Ocean Waves) ── */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden select-none z-0">
        <video
          ref={videoRef}
          autoPlay
          loop
          muted
          playsInline
          preload="auto"
          className="absolute inset-0 h-full w-full object-cover object-center opacity-80 transition-opacity duration-700"
          style={{
            filter: "contrast(1.15) brightness(0.95) saturate(1.1)",
          }}
        >
          <source src="/hero_bg.mp4" type="video/mp4" />
        </video>
      </div>

      {/* ── Top Nav Shadow Scrim ── */}
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-32 z-[1]"
        style={{
          background:
            "linear-gradient(to top, transparent 0%, rgba(3, 7, 18, 0.7) 100%)",
        }}
      />

      {/* ── Atmospheric Radial Glow & Soft Center Scrim ── */}
      <div
        className="pointer-events-none absolute inset-0 z-[2]"
        style={{
          background:
            "radial-gradient(ellipse 90% 75% at 50% 30%, rgba(0, 240, 255, 0.06) 0%, rgba(3, 7, 18, 0.25) 40%, rgba(3, 7, 18, 0.75) 80%, rgba(3, 7, 18, 0.95) 100%)",
        }}
      />

      {/* ── Particle Field (Ethereal Nocturnal Stars) ── */}
      <div className="pointer-events-none absolute inset-0 z-[3]">
        <Suspense fallback={null}>
          <ParticleField />
        </Suspense>
      </div>

      {/* ── Bottom Section Seamless Transition into Dark Theme ── */}
      <div
        className="pointer-events-none absolute inset-x-0 bottom-0 h-56 z-[4]"
        style={{
          background:
            "linear-gradient(to bottom, transparent 0%, rgba(3, 7, 18, 0.5) 40%, rgba(3, 7, 18, 0.9) 80%, var(--background) 100%)",
        }}
      />

      {/* ── Foreground Hero Content ── */}
      <div className="relative z-10 mx-auto flex w-full max-w-6xl flex-col items-center text-center">
        {/* Brand Shield Icon */}
        <motion.div
          initial={{ opacity: 0, scale: 0.85 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="relative mb-5 flex items-center justify-center"
        >
          <div className="absolute -inset-4 rounded-3xl bg-cyan/30 blur-2xl animate-pulse" />
          <img
            src="/sentrix_logo.png"
            alt="SENTRIX AI"
            className="relative h-20 w-20 rounded-2xl ring-1 ring-cyan/50 filter drop-shadow-[0_0_35px_rgba(0,240,255,0.65)] transition-transform duration-300 hover:scale-105"
          />
        </motion.div>

        {/* Main Title */}
        <GlitchTitle />

        {/* Subtitle / Value Proposition */}
        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.6 }}
          className="mt-6 max-w-3xl text-balance font-medium text-foreground/95 text-lg leading-relaxed sm:text-2xl drop-shadow-[0_2px_12px_rgba(0,0,0,0.9)]"
        >
          They Attack, We Defend: An AI Security Engine That Simulates Next-Gen Scams and Trains Itself to Stop Them.
        </motion.p>

        {/* Tagline Pill */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.0, duration: 0.6 }}
          className="mt-5 inline-flex items-center gap-2 rounded-full border border-glass-border/70 bg-background/50 px-5 py-2 backdrop-blur-md shadow-lg"
        >
          <Sparkles className="h-3.5 w-3.5 text-cyan animate-pulse" />
          <span className="font-mono text-[10px] font-semibold tracking-[0.2em] text-glow-cyan uppercase sm:text-xs">
            AI ATTACK SIMULATION → REAL-TIME DEFENSE → SELF-HEALING LEARNING LOOP
          </span>
        </motion.div>

        {/* Interactive Stats Grid */}
        <div className="mt-12 grid w-full grid-cols-2 gap-4 lg:grid-cols-4">
          {heroStats.map((s, i) => {
            const Icon = icons[s.icon];
            return (
              <motion.div
                key={s.label}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.15 + i * 0.1, duration: 0.6 }}
                className="glass-panel tilt-card rounded-2xl p-5 text-left backdrop-blur-2xl bg-card/65 border border-glass-border/80 shadow-[0_8px_32px_rgba(0,0,0,0.6)] hover:border-cyan/40 transition-all group"
              >
                <div className="mb-3 flex items-center justify-between">
                  <Icon className="h-5 w-5 text-cyan transition-transform group-hover:scale-110" strokeWidth={1.75} />
                  <div className="h-1.5 w-1.5 rounded-full bg-cyan/40 group-hover:bg-cyan group-hover:shadow-[0_0_8px_rgba(0,240,255,0.8)]" />
                </div>
                <div className="font-mono text-2xl font-bold text-glow-cyan sm:text-3xl">
                  <Counter
                    value={s.value}
                    decimals={s.decimals ?? 0}
                    prefix={s.prefix ?? ""}
                    suffix={s.suffix ?? ""}
                    delay={1300 + i * 120}
                  />
                </div>
                <div className="mt-1 text-xs text-muted-foreground sm:text-sm font-medium">
                  {s.label}
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Explore CTA and Scroll Indicator */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.6, duration: 0.6 }}
          className="mt-12 flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <a
            href="#demo"
            className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-cyan/90 to-blue-600 px-6 py-2.5 font-mono text-xs font-semibold tracking-wider text-black uppercase shadow-[0_0_25px_rgba(0,240,255,0.4)] transition-all hover:scale-105 hover:shadow-[0_0_35px_rgba(0,240,255,0.6)]"
          >
            Launch Live Sandbox <ArrowRight className="h-3.5 w-3.5" />
          </a>
          <a
            href="#identify"
            className="inline-flex items-center gap-2 rounded-full border border-glass-border bg-background/50 px-6 py-2.5 font-mono text-xs font-medium tracking-wider text-muted-foreground uppercase backdrop-blur-md transition-all hover:text-foreground hover:border-cyan/40"
          >
            View 8 Attack Vectors
          </a>
        </motion.div>

        <motion.a
          href="#identify"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2.0 }}
          className="mt-12 flex flex-col items-center gap-2 font-mono text-[10px] tracking-[0.24em] text-muted-foreground uppercase transition-colors hover:text-cyan"
        >
          Scroll to explore
          <motion.span
            animate={{ y: [0, 6, 0] }}
            transition={{ duration: 1.6, repeat: Infinity }}
          >
            <ChevronDown className="h-4 w-4 text-cyan/70" />
          </motion.span>
        </motion.a>
      </div>
    </section>
  );
}

