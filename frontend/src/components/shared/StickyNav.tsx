import { useEffect, useRef, useState } from "react";
import { Menu, Moon, Sun, X } from "lucide-react";
import { navSections } from "@/data/content";
import { SentrixMark } from "./SentrixMark";

export function StickyNav() {
  const [active, setActive] = useState("hero");
  const [menuOpen, setMenuOpen] = useState(false);
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const progressRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    setTheme(document.documentElement.classList.contains("dark") ? "dark" : "light");
  }, []);

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

  useEffect(() => {
    let frame = 0;
    const updateProgress = () => {
      if (frame) return;
      frame = window.requestAnimationFrame(() => {
        const scrollable = document.documentElement.scrollHeight - window.innerHeight;
        const progress = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
        if (progressRef.current) progressRef.current.style.transform = `scaleX(${progress / 100})`;
        frame = 0;
      });
    };
    updateProgress();
    window.addEventListener("scroll", updateProgress, { passive: true });
    return () => {
      window.removeEventListener("scroll", updateProgress);
      if (frame) window.cancelAnimationFrame(frame);
    };
  }, []);

  return (
    <nav className="fixed inset-x-0 top-0 z-50 px-3 pt-3 sm:px-6" aria-label="Primary navigation">
      <div
        className="immersive-nav glass-panel relative mx-auto max-w-7xl rounded-2xl px-3 py-2.5 shadow-[0_18px_60px_-38px_rgba(0,0,0,0.85)] transition-colors duration-500"
      >
        <div className="flex items-center justify-between gap-4">
          <a
            href="#hero"
            className="flex shrink-0 items-center gap-2.5 rounded-xl px-1.5 py-1 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-mc-red"
            aria-label="SENTRIX AI home"
            onClick={() => setMenuOpen(false)}
          >
            <SentrixMark className="h-9 w-9" />
            <span className="text-sm font-semibold tracking-[-0.02em] text-foreground">
              Sentrix <span className="font-normal text-muted-foreground">AI</span>
            </span>
          </a>
          <div className="hidden items-center gap-1 lg:flex">
            {navSections.slice(1, 5).map((s) => (
              <a
                key={s.id}
                href={`#${s.id}`}
                aria-current={active === s.id ? "location" : undefined}
                className={`rounded-lg px-3 py-2 text-sm font-medium transition-colors ${active === s.id ? "bg-mc-red/10 text-mc-red ring-1 ring-mc-red/10" : "text-muted-foreground hover:bg-mc-red/[0.06] hover:text-mc-red"}`}
              >
                {s.label}
              </a>
            ))}
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              className="inline-flex h-10 items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/[0.06] px-3 text-xs font-semibold text-white transition hover:bg-white/[0.11]"
              aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
              title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
              onClick={() => {
                const nextTheme = theme === "dark" ? "light" : "dark";
                document.documentElement.classList.toggle("dark", nextTheme === "dark");
                document.documentElement.style.colorScheme = nextTheme;
                localStorage.setItem("sentrix-theme", nextTheme);
                setTheme(nextTheme);
              }}
            >
              {theme === "dark" ? <Sun aria-hidden="true" /> : <Moon aria-hidden="true" />}
              <span className="hidden sm:inline">{theme === "dark" ? "Light" : "Dark"}</span>
            </button>
            <a
              href="#demo"
              className="hidden rounded-xl bg-mc-red px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-[#c90018] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-mc-red sm:inline-flex"
            >
              Open live lab
            </a>
            <button
              type="button"
              className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-border bg-white/70 lg:hidden"
              aria-label={menuOpen ? "Close navigation" : "Open navigation"}
              aria-expanded={menuOpen}
              onClick={() => setMenuOpen((value) => !value)}
            >
              {menuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>
        {menuOpen ? (
          <div className="mt-2 grid gap-1 border-t border-border pt-2 lg:hidden">
            {navSections.slice(1).map((s) => (
              <a
                key={s.id}
                href={`#${s.id}`}
                onClick={() => setMenuOpen(false)}
                className={`rounded-xl px-3 py-2.5 text-sm font-medium transition-colors ${active === s.id ? "bg-mc-red/10 text-mc-red" : "text-muted-foreground hover:bg-mc-red/[0.06] hover:text-mc-red"}`}
              >
                {s.label}
              </a>
            ))}
          </div>
        ) : null}
        <span className="absolute inset-x-3 bottom-0 h-px overflow-hidden rounded-full bg-border">
          <span
            ref={progressRef}
            className="block h-full origin-left scale-x-0 bg-mc-red will-change-transform"
          />
        </span>
      </div>
    </nav>
  );
}
