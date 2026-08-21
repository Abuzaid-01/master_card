import { Reveal, SectionTitle } from "@/components/shared/Section";
import { Counter } from "@/components/shared/Counter";
import { loopRows } from "@/data/content";

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
          eyebrow="04 · Learning loop"
          title="Every evasion becomes the next defense."
          description="Sentrix promotes the hardest missed attacks into training while preserving performance on legitimate transactions."
          accent="violet"
        />

        <Reveal className="mt-8 text-center">
          <div className="font-mono text-3xl leading-tight font-bold sm:text-5xl">
            <span className="text-glow-red">
              Round 1: <Counter value={518} />
            </span>
            <span className="text-muted-foreground">/750 caught</span>
            <span className="mx-3 text-muted-foreground">→</span>
            <span className="text-glow-cyan">
              Round 2: <Counter value={722} delay={1200} />
            </span>
            <span className="text-muted-foreground">/750 caught</span>
          </div>
          <p className="mt-4 font-mono text-lg text-glow-orange sm:text-2xl">
            +204 more adversarial attacks caught
          </p>
          <p className="mt-2 font-mono text-sm text-muted-foreground sm:text-base">
            AUC-PR: 0.985 → 1.000 (+1.5% lift on hard holdouts)
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
                      <span className="text-[11px] text-mc-orange">{r.delta}</span>
                    </dd>
                  </div>
                ))}
              </dl>
            </div>
          </Reveal>
        </div>

        <Reveal delay={0.15} className="mt-6">
          <blockquote className="glass-panel glow-orange rounded-2xl border-l-4 border-mc-orange p-6 text-sm leading-relaxed text-foreground/90 sm:text-base">
            Round 2 catches 204 more unseen adversarial evasion attacks across the holdout
            validation suite while maintaining a{" "}
            <span className="text-glow-orange">0.00% False Positive Rate</span> on legitimate
            cardholders. Zero catastrophic forgetting verified.
          </blockquote>
        </Reveal>
      </div>
    </section>
  );
}
