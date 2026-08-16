import { motion, useScroll, useTransform } from "motion/react";
import { useRef } from "react";
import {
  CreditCard,
  GitBranch,
  Mic,
  MessageSquareCode,
  ScanFace,
  Share2,
  Store,
  Terminal,
  UserRoundSearch,
} from "lucide-react";
import { SectionTitle } from "@/components/shared/Section";
import { attackVectors, type Severity } from "@/data/content";

const icons: Record<string, typeof Terminal> = {
  terminal: Terminal,
  "scan-face": ScanFace,
  mic: Mic,
  "user-round-search": UserRoundSearch,
  "credit-card": CreditCard,
  "share-2": Share2,
  store: Store,
  "git-branch": GitBranch,
  "message-square-code": MessageSquareCode,
};

const severityStyle: Record<Severity, string> = {
  Critical: "border-mc-red/50 bg-mc-red/15 text-mc-red",
  High: "border-mc-orange/50 bg-mc-orange/15 text-mc-orange",
  Medium: "border-ai-violet/50 bg-ai-violet/15 text-ai-violet",
};

export function Identify() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });
  const bgY = useTransform(scrollYProgress, [0, 1], ["-8%", "8%"]);

  return (
    <section
      id="identify"
      ref={ref}
      className="snap-section relative flex min-h-screen w-full flex-col justify-center overflow-hidden px-5 py-24 sm:px-8 lg:px-16"
    >
      <motion.div
        style={{ y: bgY }}
        className="grid-backdrop absolute -inset-y-24 inset-x-0 opacity-60"
      />
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(50% 40% at 15% 10%, color-mix(in oklab, var(--mc-red) 16%, transparent), transparent 70%)",
        }}
      />

      <div className="relative z-10 mx-auto w-full max-w-7xl">
        <SectionTitle
          eyebrow="Pillar 1 · Identify"
          title="8 Novel GenAI-Powered Attack Vectors"
          accent="red"
        />

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {attackVectors.map((v, i) => {
            const Icon = icons[v.icon] ?? Terminal;
            return (
              <motion.article
                key={v.name}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-6% 0px" }}
                transition={{
                  duration: 0.5,
                  delay: (i % 4) * 0.1,
                  ease: [0.2, 0.8, 0.2, 1],
                }}
                className="glass-panel group relative overflow-hidden rounded-2xl p-5 transition-transform duration-300 hover:-translate-y-1.5"
              >
                <div className="flex items-start justify-between gap-3">
                  <Icon
                    className="h-5 w-5 text-mc-orange"
                    strokeWidth={1.75}
                  />
                  <span
                    className={`rounded-full border px-2 py-0.5 font-mono text-[10px] tracking-wider uppercase ${severityStyle[v.severity]}`}
                  >
                    {v.severity}
                  </span>
                </div>
                <div className="mt-4 font-mono text-[10px] text-muted-foreground">
                  VECTOR {String(v.n).padStart(2, "0")}
                </div>
                <h3 className="mt-1 text-base leading-snug font-semibold">
                  {v.name}
                </h3>
                <p className="mt-2 text-sm text-muted-foreground">{v.desc}</p>

                <div className="mt-4 max-h-0 overflow-hidden opacity-0 transition-all duration-400 group-hover:max-h-40 group-hover:opacity-100 group-focus-within:max-h-40 group-focus-within:opacity-100">
                  <div className="border-t border-glass-border pt-3">
                    <div className="font-mono text-[10px] tracking-[0.2em] text-cyan uppercase">
                      GenAI Force Multiplier
                    </div>
                    <p className="mt-1.5 text-xs leading-relaxed text-foreground/80">
                      {v.multiplier}
                    </p>
                  </div>
                </div>
              </motion.article>
            );
          })}
        </div>
      </div>
    </section>
  );
}
