import { Github, Linkedin } from "lucide-react";
import { Reveal } from "@/components/shared/Section";
import { SentrixMark } from "@/components/shared/SentrixMark";

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
            "radial-gradient(45% 42% at 38% 100%, rgb(235 0 27 / 9%), transparent 72%), radial-gradient(45% 42% at 62% 100%, rgb(247 158 27 / 13%), transparent 72%)",
        }}
      />

      <div className="relative z-10 mx-auto w-full max-w-3xl">
        <Reveal>
          <div className="flex justify-center">
            <SentrixMark className="h-16 w-16" />
          </div>
          <div className="mt-6 text-xs font-semibold tracking-[0.18em] text-mc-red uppercase">
            Built for explainable protection
          </div>
          <h2 className="mt-4 text-3xl font-medium tracking-[-0.035em] sm:text-5xl">
            <span>Sentrix AI</span>
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-sm text-foreground/90 sm:text-base font-normal leading-relaxed">
            A research-backed defense platform that makes complex fraud signals understandable,
            testable, and useful to the people responsible for payment safety.
          </p>
          <p className="mt-3 text-xs font-semibold text-mc-red uppercase tracking-[0.18em]">
            SIMULATE → EXPLAIN → ADAPT
          </p>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <a
              href="https://github.com/Abuzaid-01/master_card"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-full bg-foreground px-6 py-3 text-sm font-medium text-background shadow-sm transition-transform duration-300 hover:-translate-y-0.5"
            >
              <Github className="h-4 w-4" />
              View Source Repository
            </a>
            <a
              href="https://www.linkedin.com/in/abuzaid01"
              target="_blank"
              rel="noreferrer"
              className="glass-panel inline-flex items-center gap-2 rounded-full border border-border px-6 py-3 text-sm font-medium transition-transform duration-300 hover:-translate-y-0.5 hover:border-mc-orange/50"
            >
              <Linkedin className="h-4 w-4 text-mc-red" />
              Connect on LinkedIn
            </a>
          </div>

          <p className="mt-12 font-mono text-xs tracking-wider text-muted-foreground">
            Made with <span className="text-red-500 animate-pulse inline-block">❤️</span> by{" "}
            <a
              href="https://www.linkedin.com/in/abuzaid01"
              target="_blank"
              rel="noreferrer"
              className="font-semibold text-mc-red hover:underline decoration-mc-red underline-offset-4 transition-colors"
            >
              Abuzaid
            </a>
          </p>
        </Reveal>
      </div>
    </section>
  );
}
