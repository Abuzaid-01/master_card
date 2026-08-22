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

const journeyStages = [
  { number: "01", title: "Manipulate", detail: "Prompt, impersonation, or identity compromise" },
  { number: "02", title: "Test", detail: "Low-value authorizations establish access" },
  { number: "03", title: "Drain", detail: "Velocity and value escalate across channels" },
  { number: "04", title: "Launder", detail: "Funds disperse through beneficiary networks" },
];

export function Identify() {
  return (
    <section
      id="identify"
      className="snap-section relative flex min-h-screen w-full flex-col justify-center overflow-hidden px-5 py-24 sm:px-8 lg:px-16"
    >
      <div className="grid-backdrop absolute -inset-y-24 inset-x-0 opacity-60" />
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(50% 40% at 15% 10%, color-mix(in oklab, var(--mc-red) 16%, transparent), transparent 70%)",
        }}
      />

      <div className="relative z-10 mx-auto w-full max-w-7xl">
        <SectionTitle
          eyebrow="01 · Threat landscape"
          title="Eight attack families. One connected journey."
          description="SENTRIX links language, identity, transaction, merchant, and beneficiary evidence into a shared campaign instead of treating every alert as an isolated event."
          accent="red"
        />

        <div className="glass-panel relative mb-6 overflow-hidden rounded-2xl px-4 py-5 sm:px-6 sm:py-6">
          <div className="grid gap-3 sm:grid-cols-4 sm:gap-0">
            {journeyStages.map((stage, index) => (
              <article
                key={stage.number}
                className="rounded-xl border border-border/70 bg-[var(--surface-raised)] p-3 sm:border-0 sm:bg-transparent sm:p-0 sm:text-center"
              >
                <div className="relative hidden h-8 items-center justify-center sm:flex">
                  {index > 0 ? (
                    <span className="absolute top-1/2 right-1/2 left-0 h-px -translate-y-1/2 bg-gradient-to-r from-mc-red to-mc-orange" />
                  ) : null}
                  {index < journeyStages.length - 1 ? (
                    <span className="absolute top-1/2 right-0 left-1/2 h-px -translate-y-1/2 bg-gradient-to-r from-mc-orange to-mc-yellow" />
                  ) : null}
                  <span className="relative z-10 inline-grid h-8 min-w-8 place-items-center rounded-full border border-mc-orange/30 bg-background px-2 font-mono text-[10px] font-semibold text-mc-red shadow-[0_0_0_5px_var(--background)]">
                    {stage.number}
                  </span>
                </div>
                <div className="flex items-center gap-3 sm:hidden">
                  <span className="inline-grid h-8 min-w-8 place-items-center rounded-full border border-mc-orange/30 bg-background px-2 font-mono text-[10px] font-semibold text-mc-red">
                    {stage.number}
                  </span>
                  <h3 className="text-sm font-semibold">{stage.title}</h3>
                </div>
                <h3 className="mt-2 hidden text-sm font-semibold sm:block">{stage.title}</h3>
                <p className="mt-1 text-xs leading-relaxed text-muted-foreground">{stage.detail}</p>
              </article>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {attackVectors.map((v) => {
            const Icon = icons[v.icon] ?? Terminal;
            return (
              <article
                key={v.name}
                className="glass-panel relative overflow-hidden rounded-2xl p-5 transition-transform duration-300 hover:-translate-y-1"
              >
                <div className="flex items-start justify-between gap-3">
                  <Icon className="h-5 w-5 text-mc-orange" strokeWidth={1.75} />
                  <span
                    className={`rounded-full border px-2 py-0.5 font-mono text-[10px] tracking-wider uppercase ${severityStyle[v.severity]}`}
                  >
                    {v.severity}
                  </span>
                </div>
                <div className="mt-4 font-mono text-[10px] text-muted-foreground">
                  VECTOR {String(v.n).padStart(2, "0")}
                </div>
                <h3 className="mt-1 text-base leading-snug font-semibold">{v.name}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{v.desc}</p>

                <div className="mt-4">
                  <div className="border-t border-glass-border pt-3">
                    <div className="text-[10px] font-semibold tracking-[0.16em] text-cyan uppercase">
                      Why AI changes it
                    </div>
                    <p className="mt-1.5 text-xs leading-relaxed text-foreground/80">
                      {v.multiplier}
                    </p>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}
