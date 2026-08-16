import { motion } from "motion/react";
import { RefreshCw } from "lucide-react";
import { Reveal, SectionTitle } from "@/components/shared/Section";
import { techGroups } from "@/data/content";

const pipeline = ["Identify", "Generate", "Defend", "Close the Loop"];

const accentBorder = {
  cyan: "hover:border-cyan/60 hover:text-cyan",
  violet: "hover:border-ai-violet/60 hover:text-ai-violet",
  orange: "hover:border-mc-orange/60 hover:text-mc-orange",
  red: "hover:border-mc-red/60 hover:text-mc-red",
};

export function Stack() {
  return (
    <section
      id="stack"
      className="snap-section relative flex min-h-screen w-full flex-col justify-center overflow-hidden px-5 py-24 sm:px-8 lg:px-16"
    >
      <div className="grid-backdrop absolute inset-0 opacity-40" />

      <div className="relative z-10 mx-auto w-full max-w-6xl">
        <SectionTitle
          eyebrow="Architecture"
          title="Architecture & Technology Stack"
          accent="cyan"
        />

        <Reveal>
          <div className="glass-panel rounded-2xl p-6 sm:p-10">
            <div className="flex flex-wrap items-center justify-center gap-3">
              {pipeline.map((p, i) => (
                <div key={p} className="flex items-center gap-3">
                  <motion.div
                    initial={{ opacity: 0, y: 14 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.15, duration: 0.45 }}
                    className="glass-panel rounded-xl px-4 py-3 font-mono text-xs tracking-wider uppercase sm:text-sm"
                  >
                    {p}
                  </motion.div>
                  {i < pipeline.length - 1 && (
                    <motion.span
                      className="text-cyan"
                      animate={{ x: [0, 4, 0] }}
                      transition={{
                        duration: 1.6,
                        repeat: Infinity,
                        delay: i * 0.2,
                      }}
                    >
                      →
                    </motion.span>
                  )}
                </div>
              ))}
            </div>

            <div className="mt-6 flex items-center justify-center gap-3">
              <div className="h-px flex-1 bg-glass-border" />
              <div className="flex items-center gap-2 font-mono text-[10px] tracking-[0.24em] text-mc-orange uppercase">
                <motion.span
                  animate={{ rotate: 360 }}
                  transition={{ duration: 6, repeat: Infinity, ease: "linear" }}
                  className="inline-flex"
                >
                  <RefreshCw className="h-3.5 w-3.5" />
                </motion.span>
                Continuous Improvement
              </div>
              <div className="h-px flex-1 bg-glass-border" />
            </div>
          </div>
        </Reveal>

        <div className="mt-8 space-y-6">
          {techGroups.map((g, gi) => (
            <Reveal key={g.group} delay={gi * 0.08}>
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <div className="w-40 shrink-0 font-mono text-[11px] tracking-[0.2em] text-muted-foreground uppercase">
                  {g.group}
                </div>
                <div className="flex flex-wrap gap-2">
                  {g.items.map((item) => (
                    <span
                      key={item}
                      className={`glass-panel rounded-full px-3 py-1.5 font-mono text-[11px] transition-colors duration-300 sm:text-xs ${accentBorder[g.accent]}`}
                    >
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
