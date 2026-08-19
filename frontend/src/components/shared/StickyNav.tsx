import { useEffect, useState } from "react";
import { navSections } from "@/data/content";
import { SentrixMark } from "./SentrixMark";

export function StickyNav() {
  const [active, setActive] = useState("hero");

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible) setActive(visible.target.id);
      },
      { threshold: [0.2, 0.5, 0.75], rootMargin: "-20% 0px -30% 0px" },
    );
    navSections.forEach(({ id }) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });
    return () => observer.disconnect();
  }, []);

  return (
    <nav className="fixed inset-x-0 top-4 z-50 flex justify-center px-4">
      <div className="glass-panel flex max-w-full items-center gap-1 overflow-x-auto rounded-full px-3 py-2">
        <a
          href="#hero"
          className="mr-1 flex shrink-0 items-center gap-2 pr-2 pl-1"
          aria-label="SENTRIX AI home"
        >
          <img
            src="/sentrix_logo.png"
            alt="SENTRIX AI"
            className="h-5 w-5 rounded-md object-contain"
          />
          <span className="hidden font-mono text-[11px] font-bold tracking-[0.2em] text-glow-cyan uppercase sm:inline">
            SENTRIX AI
          </span>
        </a>
        {navSections.map((s) => (
          <a
            key={s.id}
            href={`#${s.id}`}
            className={`shrink-0 rounded-full px-3 py-1.5 text-xs font-medium tracking-wide transition-colors ${
              active === s.id
                ? "bg-cyan/15 text-cyan"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {s.label}
          </a>
        ))}
      </div>
    </nav>
  );
}
