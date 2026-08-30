import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Section, SectionTitle, Reveal } from "@/components/shared/Section";
import { faqItems, type FAQItem } from "@/data/content";
import { ChevronDown, HelpCircle, Sparkles, Search, Layers, Zap, RefreshCw, ShieldCheck } from "lucide-react";

type CategoryFilter = "All" | "Architecture & Workflow" | "ML & ONNX Engine" | "Closed Loop" | "Compliance & Defense";

const categoryIcons: Record<string, typeof Layers> = {
  "Architecture & Workflow": Layers,
  "ML & ONNX Engine": Zap,
  "Closed Loop": RefreshCw,
  "Compliance & Defense": ShieldCheck,
};

export function FAQ() {
  const [openId, setOpenId] = useState<string | null>("faq-1");
  const [selectedCategory, setSelectedCategory] = useState<CategoryFilter>("All");
  const [searchQuery, setSearchQuery] = useState("");

  const categories: CategoryFilter[] = [
    "All",
    "Architecture & Workflow",
    "ML & ONNX Engine",
    "Closed Loop",
    "Compliance & Defense",
  ];

  const filteredItems = faqItems.filter((item) => {
    const matchesCategory = selectedCategory === "All" || item.category === selectedCategory;
    const matchesSearch =
      item.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.answer.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (item.highlight && item.highlight.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const toggleAccordion = (id: string) => {
    setOpenId((prev) => (prev === id ? null : id));
  };

  return (
    <Section id="faq" className="bg-background/95">
      <SectionTitle
        eyebrow="06 // ARCHITECTURE & WORKFLOW FAQ"
        title="Frequently Asked Questions"
        accent="cyan"
      />

      {/* ── Controls: Search & Category Pills ── */}
      <Reveal delay={0.1} className="mb-8 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        {/* Category Pills */}
        <div className="flex flex-wrap items-center gap-1.5">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`rounded-full px-3.5 py-1.5 text-xs font-medium transition-all duration-200 ${
                selectedCategory === cat
                  ? "bg-cyan/20 text-cyan shadow-[0_0_12px_rgba(0,229,255,0.25)] ring-1 ring-cyan/50"
                  : "bg-muted/30 text-muted-foreground hover:bg-muted/50 hover:text-foreground"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Search Bar */}
        <div className="relative w-full max-w-xs">
          <Search className="text-muted-foreground absolute top-1/2 left-3 h-3.5 w-3.5 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search architecture & workflow..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="focus:border-cyan/50 focus:ring-cyan/20 w-full rounded-full border border-white/10 bg-black/40 py-1.5 pr-4 pl-9 text-xs text-foreground placeholder:text-muted-foreground/60 focus:ring-2 focus:outline-none"
          />
        </div>
      </Reveal>

      {/* ── Accordion List ── */}
      <div className="space-y-3">
        {filteredItems.length === 0 ? (
          <div className="glass-panel flex flex-col items-center justify-center rounded-2xl py-12 text-center">
            <HelpCircle className="text-muted-foreground mb-3 h-8 w-8 opacity-40" />
            <p className="text-sm text-muted-foreground">No questions found matching your search query.</p>
          </div>
        ) : (
          filteredItems.map((item, idx) => {
            const isOpen = openId === item.id;
            const CategoryIcon = categoryIcons[item.category] || HelpCircle;

            return (
              <Reveal key={item.id} delay={0.05 * idx}>
                <div
                  className={`glass-panel overflow-hidden rounded-2xl transition-all duration-300 ${
                    isOpen
                      ? "border-cyan/35 bg-card/80 shadow-[0_0_24px_rgba(0,229,255,0.08)]"
                      : "border-white/5 hover:border-white/15 bg-card/40"
                  }`}
                >
                  {/* Header Button */}
                  <button
                    onClick={() => toggleAccordion(item.id)}
                    className="flex w-full items-center justify-between gap-4 p-5 text-left transition-colors sm:p-6"
                    aria-expanded={isOpen}
                  >
                    <div className="flex items-start gap-3.5 sm:items-center">
                      <div
                        className={`mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg transition-colors sm:mt-0 ${
                          isOpen
                            ? "bg-cyan/20 text-cyan ring-1 ring-cyan/40"
                            : "bg-muted/40 text-muted-foreground"
                        }`}
                      >
                        <CategoryIcon className="h-4 w-4" />
                      </div>
                      <div>
                        <div className="mb-1 flex items-center gap-2">
                          <span className="font-mono text-[10px] tracking-wider text-muted-foreground uppercase">
                            {item.category}
                          </span>
                        </div>
                        <h3 className={`text-sm font-semibold tracking-tight transition-colors sm:text-base ${
                          isOpen ? "text-cyan" : "text-foreground"
                        }`}>
                          {item.question}
                        </h3>
                      </div>
                    </div>

                    <div
                      className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full border transition-all duration-300 ${
                        isOpen
                          ? "rotate-180 border-cyan/40 bg-cyan/15 text-cyan"
                          : "border-white/10 text-muted-foreground"
                      }`}
                    >
                      <ChevronDown className="h-3.5 w-3.5" />
                    </div>
                  </button>

                  {/* Expandable Content */}
                  <AnimatePresence initial={false}>
                    {isOpen && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.28, ease: [0.16, 1, 0.3, 1] }}
                      >
                        <div className="border-t border-white/5 px-5 pt-3 pb-5 sm:px-6 sm:pb-6">
                          <p className="text-sm leading-relaxed text-muted-foreground">
                            {item.answer}
                          </p>

                          {item.highlight && (
                            <div className="mt-4 flex items-center gap-2.5 rounded-xl border border-cyan/20 bg-cyan/5 px-3.5 py-2.5 text-xs text-cyan">
                              <Sparkles className="h-3.5 w-3.5 shrink-0" />
                              <span className="font-mono text-[11px] leading-tight">
                                <strong className="font-semibold text-white">Key Takeaway:</strong> {item.highlight}
                              </span>
                            </div>
                          )}
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </Reveal>
            );
          })
        )}
      </div>
    </Section>
  );
}
