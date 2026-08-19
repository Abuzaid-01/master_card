import { Github, ShieldCheck, Cpu, Network } from "lucide-react";
import { Reveal } from "@/components/shared/Section";

export function Team() {
  return (
    <section
      id="team"
      className="snap-section relative flex min-h-screen w-full flex-col items-center justify-center overflow-hidden px-5 py-24 text-center sm:px-8"
    >
      <div className="dot-backdrop absolute inset-0 opacity-50" />
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(55% 45% at 50% 100%, color-mix(in oklab, var(--ai-violet) 20%, transparent), transparent 70%)",
        }}
      />

      <div className="relative z-10 mx-auto w-full max-w-3xl">
        <Reveal>
          <div className="flex justify-center">
            <img
              src="/sentrix_logo.png"
              alt="SENTRIX AI"
              className="h-20 w-20 rounded-2xl shadow-2xl ring-1 ring-cyan/40 filter drop-shadow-[0_0_25px_rgba(0,240,255,0.45)]"
            />
          </div>
          <div className="mt-6 font-mono text-xs tracking-[0.28em] text-cyan uppercase">
            Platform Architecture
          </div>
          <h2 className="mt-4 text-3xl font-bold tracking-tight sm:text-5xl">
            <span className="text-glow-cyan">SENTRIX AI</span>
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-sm text-foreground/90 sm:text-base font-normal leading-relaxed">
            We use AI to create realistic cyber attacks, train our defenses to block them in real-time, and make the system smarter every round.
          </p>
          <p className="mt-3 font-mono text-xs text-glow-cyan uppercase tracking-[0.25em]">
            ATTACK → DEFEND → EVOLVE
          </p>

          <div className="mt-10 flex justify-center">
            <a
              href="https://github.com/Abuzaid-01/master_card"
              target="_blank"
              rel="noreferrer"
              className="glass-panel glow-cyan inline-flex items-center gap-2 rounded-full px-6 py-3 text-sm font-medium transition-transform duration-300 hover:-translate-y-0.5"
            >
              <Github className="h-4 w-4 text-cyan" />
              View Source Repository
            </a>
          </div>

          <p className="mt-12 font-mono text-[11px] tracking-[0.2em] text-muted-foreground uppercase">
            SENTRIX AI · Next-Generation Autonomous Fraud Intelligence Head
          </p>
        </Reveal>
      </div>
    </section>
  );
}
