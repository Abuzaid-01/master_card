import { Github } from "lucide-react";
import { Reveal } from "@/components/shared/Section";
import { MastercardMark } from "@/components/shared/MastercardMark";

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
            "radial-gradient(55% 45% at 50% 100%, color-mix(in oklab, var(--mc-orange) 16%, transparent), transparent 70%)",
        }}
      />

      <div className="relative z-10 mx-auto w-full max-w-3xl">
        <Reveal>
          <div className="flex justify-center">
            <MastercardMark className="h-14 w-24" pulse />
          </div>
          <div className="mt-6 font-mono text-xs tracking-[0.28em] text-muted-foreground uppercase">
            Team
          </div>
          <h2 className="mt-4 text-3xl font-bold tracking-tight sm:text-5xl">
            <span className="text-glow-cyan">GenAI Fraud Shield</span>
          </h2>
          <p className="mt-4 text-sm text-foreground/85 sm:text-base">
            Mastercard Innovation Challenge 2026
          </p>
          <p className="mt-1 font-mono text-xs text-muted-foreground sm:text-sm">
            Global Fintech Fest, Mumbai · Sep 8–11, 2026
          </p>

          <div className="mt-10 flex justify-center">
            <a
              href="https://github.com/Abuzaid-01/master_card"
              target="_blank"
              rel="noreferrer"
              className="glass-panel glow-cyan inline-flex items-center gap-2 rounded-full px-6 py-3 text-sm font-medium transition-transform duration-300 hover:-translate-y-0.5"
            >
              <Github className="h-4 w-4 text-cyan" />
              View on GitHub
            </a>
          </div>

          <p className="mt-12 font-mono text-[11px] tracking-[0.2em] text-muted-foreground uppercase">
            Built with <span className="text-mc-red">♥</span> for Mastercard
          </p>
        </Reveal>
      </div>
    </section>
  );
}
