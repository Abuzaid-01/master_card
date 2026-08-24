import { motion, useScroll, useTransform, AnimatePresence } from "motion/react";
import { useRef, useState, useMemo } from "react";
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
  Bot,
  ShieldAlert,
  Smartphone,
  RefreshCw,
  Zap,
  Lock,
  Globe,
  Activity,
  Cpu,
  FileText,
  Coins,
  Shuffle,
  Search,
  Layers,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { SectionTitle } from "@/components/shared/Section";
import { attackVectors, type Severity, type AttackPillar } from "@/data/content";

const icons: Record<string, any> = {
  terminal: Terminal,
  "scan-face": ScanFace,
  mic: Mic,
  "user-round-search": UserRoundSearch,
  "credit-card": CreditCard,
  "share-2": Share2,
  store: Store,
  "git-branch": GitBranch,
  "message-square-code": MessageSquareCode,
  bot: Bot,
  "shield-alert": ShieldAlert,
  smartphone: Smartphone,
  "refresh-cw": RefreshCw,
  zap: Zap,
  lock: Lock,
  globe: Globe,
  activity: Activity,
  cpu: Cpu,
  "file-text": FileText,
  coins: Coins,
  shuffle: Shuffle,
};

const severityStyle: Record<Severity, string> = {
  Critical: "border-mc-red/50 bg-mc-red/15 text-mc-red",
  High: "border-mc-orange/50 bg-mc-orange/15 text-mc-orange",
  Medium: "border-ai-violet/50 bg-ai-violet/15 text-ai-violet",
};

const PILLARS: { label: AttackPillar; short: string; count: number }[] = [
  { label: "All", short: "All (36)", count: 36 },
  { label: "Pillar 1: AI Red-Teaming", short: "1. AI Red-Team (8)", count: 8 },
  { label: "Pillar 2: Synthetic Data", short: "2. Obfuscation (7)", count: 7 },
  { label: "Pillar 3: Multi-Rail Payments", short: "3. Multi-Rail (7)", count: 7 },
  { label: "Pillar 4: Money Mule Networks", short: "4. Money Mules (7)", count: 7 },
  { label: "Pillar 5: Adversarial Evasion", short: "5. Evasion ML (7)", count: 7 },
];

const INITIAL_VISIBLE_COUNT = 8; // Exactly 2 rows on 4-column desktop grid

export function Identify() {
  const ref = useRef<HTMLElement>(null);
  const [selectedPillar, setSelectedPillar] = useState<AttackPillar>("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [isExpanded, setIsExpanded] = useState(false);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });
  const bgY = useTransform(scrollYProgress, [0, 1], ["-8%", "8%"]);

  const filteredVectors = useMemo(() => {
    return attackVectors.filter((v) => {
      const matchesPillar =
        selectedPillar === "All" || v.pillarShort === selectedPillar;
      const matchesSearch =
        searchQuery.trim() === "" ||
        v.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        v.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        v.desc.toLowerCase().includes(searchQuery.toLowerCase()) ||
        v.pillar.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesPillar && matchesSearch;
    });
  }, [selectedPillar, searchQuery]);

  const displayedVectors = useMemo(() => {
    if (isExpanded || filteredVectors.length <= INITIAL_VISIBLE_COUNT) {
      return filteredVectors;
    }
    return filteredVectors.slice(0, INITIAL_VISIBLE_COUNT);
  }, [filteredVectors, isExpanded]);

  const remainingCount = Math.max(0, filteredVectors.length - INITIAL_VISIBLE_COUNT);

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
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <SectionTitle
            eyebrow="Pillar 1 · Attack Taxonomy"
            title="36 Real-World GenAI Attack Vectors"
            accent="red"
          />

          {/* Search Bar */}
          <div className="relative mb-8 w-full max-w-xs">
            <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search 36 attack vectors..."
              className="w-full rounded-xl border border-glass-border bg-glass-bg/60 py-2 pl-10 pr-4 text-xs backdrop-blur-md transition-all focus:border-mc-orange focus:outline-none focus:ring-1 focus:ring-mc-orange"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] text-muted-foreground hover:text-foreground"
              >
                Clear
              </button>
            )}
          </div>
        </div>

        {/* Pillar Filter Tabs */}
        <div className="mb-8 flex flex-wrap items-center gap-2 border-b border-glass-border/60 pb-4">
          <div className="mr-2 flex items-center gap-1.5 text-xs text-muted-foreground">
            <Layers className="h-3.5 w-3.5 text-mc-orange" />
            <span className="font-mono text-[11px] uppercase tracking-wider">
              Pillars:
            </span>
          </div>
          {PILLARS.map((p) => {
            const isSelected = selectedPillar === p.label;
            return (
              <button
                key={p.label}
                onClick={() => {
                  setSelectedPillar(p.label);
                  // If changing pillars, keep natural view
                }}
                className={`relative rounded-lg px-3 py-1.5 text-xs font-medium transition-all ${
                  isSelected
                    ? "bg-mc-orange/20 text-mc-orange border border-mc-orange/40 shadow-sm"
                    : "border border-glass-border bg-glass-bg/40 text-muted-foreground hover:bg-glass-bg hover:text-foreground"
                }`}
              >
                {p.short}
              </button>
            );
          })}
          <div className="ml-auto font-mono text-[11px] text-muted-foreground">
            Showing {displayedVectors.length} of {filteredVectors.length} {filteredVectors.length < 36 ? `(filtered from 36)` : ""}
          </div>
        </div>

        {/* 2-Row Grid (Default) or Expanded */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <AnimatePresence mode="popLayout">
            {displayedVectors.map((v, i) => {
              const Icon = icons[v.icon] ?? Terminal;
              return (
                <motion.article
                  key={v.id || v.name}
                  layout
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  transition={{
                    duration: 0.35,
                    delay: Math.min(0.2, (i % 8) * 0.03),
                    ease: [0.2, 0.8, 0.2, 1],
                  }}
                  className="glass-panel group relative flex flex-col justify-between overflow-hidden rounded-2xl p-5 transition-all duration-300 hover:-translate-y-1.5 hover:border-mc-orange/40 hover:shadow-lg hover:shadow-mc-orange/5"
                >
                  <div>
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-glass-border bg-glass-bg text-mc-orange">
                        <Icon className="h-4 w-4" strokeWidth={2} />
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-[10px] text-muted-foreground">
                          {v.id}
                        </span>
                        <span
                          className={`rounded-full border px-2 py-0.5 font-mono text-[9px] tracking-wider uppercase ${severityStyle[v.severity]}`}
                        >
                          {v.severity}
                        </span>
                      </div>
                    </div>

                    <div className="mt-3 font-mono text-[9px] text-muted-foreground/80 tracking-wide uppercase">
                      {v.pillarShort}
                    </div>
                    <h3 className="mt-0.5 text-sm leading-snug font-semibold text-foreground">
                      {v.name}
                    </h3>
                    <p className="mt-1.5 text-xs leading-relaxed text-muted-foreground">
                      {v.desc}
                    </p>
                  </div>

                  <div className="mt-4 border-t border-glass-border/70 pt-3">
                    <div className="font-mono text-[9px] tracking-[0.15em] text-cyan uppercase">
                      GenAI Multiplier
                    </div>
                    <p className="mt-1 text-[11px] leading-relaxed text-foreground/80">
                      {v.multiplier}
                    </p>
                  </div>
                </motion.article>
              );
            })}
          </AnimatePresence>
        </div>

        {/* Show More / Show Less Toggle Button */}
        {filteredVectors.length > INITIAL_VISIBLE_COUNT && (
          <div className="mt-8 flex justify-center">
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="group relative flex items-center gap-2 rounded-xl border border-mc-orange/40 bg-mc-orange/10 px-6 py-2.5 font-mono text-xs font-semibold text-mc-orange backdrop-blur-md transition-all hover:bg-mc-orange/20 hover:border-mc-orange/70 hover:shadow-lg hover:shadow-mc-orange/10 active:scale-98"
            >
              {isExpanded ? (
                <>
                  <span>Show Less (Collapse to 2 Rows)</span>
                  <ChevronUp className="h-4 w-4 transition-transform group-hover:-translate-y-0.5" />
                </>
              ) : (
                <>
                  <span>Show All Vectors ({remainingCount} More)</span>
                  <ChevronDown className="h-4 w-4 transition-transform group-hover:translate-y-0.5" />
                </>
              )}
            </button>
          </div>
        )}

        {filteredVectors.length === 0 && (
          <div className="glass-panel flex flex-col items-center justify-center rounded-2xl p-12 text-center">
            <Search className="h-8 w-8 text-muted-foreground/50 mb-3" />
            <div className="text-sm font-semibold text-foreground">
              No attack vectors match your search
            </div>
            <p className="mt-1 text-xs text-muted-foreground">
              Try adjusting your search query or reset the pillar filter.
            </p>
            <button
              onClick={() => {
                setSelectedPillar("All");
                setSearchQuery("");
              }}
              className="mt-4 rounded-lg border border-mc-orange/40 bg-mc-orange/20 px-3 py-1.5 text-xs text-mc-orange"
            >
              Reset Filters
            </button>
          </div>
        )}
      </div>
    </section>
  );
}
