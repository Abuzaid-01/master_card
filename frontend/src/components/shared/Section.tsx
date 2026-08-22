import type { ReactNode } from "react";

export function Section({
  id,
  children,
  className = "",
}: {
  id: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section
      id={id}
      className={`snap-section relative flex min-h-screen w-full flex-col justify-center overflow-hidden px-5 py-24 sm:px-8 lg:px-16 ${className}`}
    >
      {children}
    </section>
  );
}

export function SectionTitle({
  eyebrow,
  title,
  description,
  accent = "cyan",
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  accent?: "cyan" | "orange" | "red" | "violet";
}) {
  const bar = {
    cyan: "bg-cyan",
    orange: "bg-mc-orange",
    red: "bg-mc-red",
    violet: "bg-ai-violet",
  }[accent];

  return (
    <div className="mb-10 max-w-4xl">
      {eyebrow ? (
        <div className="mb-3 flex items-center gap-3">
          <span className={`h-px w-10 ${bar}`} />
          <span className="text-xs font-semibold tracking-[0.18em] text-muted-foreground uppercase">
            {eyebrow}
          </span>
        </div>
      ) : null}
      <h2 className="text-3xl leading-[1.05] font-medium tracking-[-0.035em] text-balance sm:text-4xl lg:text-5xl">
        {title}
      </h2>
      {description ? (
        <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted-foreground sm:text-lg">
          {description}
        </p>
      ) : null}
    </div>
  );
}

export function Reveal({
  children,
  className = "",
}: {
  children: ReactNode;
  delay?: number;
  className?: string;
}) {
  return (
    <div className={className}>
      {children}
    </div>
  );
}
