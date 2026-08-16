import { motion } from "motion/react";

export function GaugeRing({
  percent,
  label,
  value,
  accent = "cyan",
}: {
  percent: number;
  label: string;
  value: string;
  accent?: "cyan" | "orange" | "violet";
}) {
  const stroke = {
    cyan: "var(--neon-cyan)",
    orange: "var(--mc-orange)",
    violet: "var(--ai-violet)",
  }[accent];
  const r = 26;
  const c = 2 * Math.PI * r;

  return (
    <div className="flex items-center gap-3">
      <svg viewBox="0 0 64 64" className="h-14 w-14 -rotate-90">
        <circle
          cx="32"
          cy="32"
          r={r}
          fill="none"
          stroke="var(--border)"
          strokeWidth="5"
        />
        <motion.circle
          cx="32"
          cy="32"
          r={r}
          fill="none"
          stroke={stroke}
          strokeWidth="5"
          strokeLinecap="round"
          strokeDasharray={c}
          initial={{ strokeDashoffset: c }}
          whileInView={{ strokeDashoffset: c * (1 - percent / 100) }}
          viewport={{ once: true, margin: "-10% 0px" }}
          transition={{ duration: 1.4, ease: "easeOut" }}
        />
      </svg>
      <div>
        <div className="font-mono text-lg font-semibold">{value}</div>
        <div className="text-xs text-muted-foreground">{label}</div>
      </div>
    </div>
  );
}
