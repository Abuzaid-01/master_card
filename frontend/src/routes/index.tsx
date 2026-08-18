import { createFileRoute } from "@tanstack/react-router";
import { StickyNav } from "@/components/shared/StickyNav";
import { Hero } from "@/components/sections/Hero";
import { Identify } from "@/components/sections/Identify";
import { Generate } from "@/components/sections/Generate";
import { Defend } from "@/components/sections/Defend";
import { ClosedLoop } from "@/components/sections/ClosedLoop";
import { LiveDemo } from "@/components/sections/LiveDemo";
import { Team } from "@/components/sections/Team";

const title = "GenAI Fraud Shield — Adversarial Fraud Defense Engine";
const description =
  "Red–blue team AI engine for next-gen payment fraud: 8 GenAI attack vectors, synthetic attack generation, 97.5% AUC-PR ONNX defense, and adversarial active learning.";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

function Index() {
  return (
    <main className="relative w-full bg-background">
      <StickyNav />
      <Hero />
      <Identify />
      <Generate />
      <Defend />
      <ClosedLoop />
      <LiveDemo />
      <Team />
    </main>
  );
}

