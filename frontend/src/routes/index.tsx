import { createFileRoute } from "@tanstack/react-router";
import { StickyNav } from "@/components/shared/StickyNav";
import { Hero } from "@/components/sections/Hero";
import { Identify } from "@/components/sections/Identify";
import { Generate } from "@/components/sections/Generate";
import { Defend } from "@/components/sections/Defend";
import { ClosedLoop } from "@/components/sections/ClosedLoop";
import { LiveDemo } from "@/components/sections/LiveDemo";
import { Team } from "@/components/sections/Team";

const title = "Sentrix AI — Adaptive Fraud Defense";
const description =
  "Fraud defense that learns from the attack. Simulate emerging payment threats, explain every decision, and adapt through closed-loop learning.";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
      { property: "og:type", content: "website" },
      {
        property: "og:image",
        content: "https://master-card-coral.vercel.app/og.png",
      },
      { name: "twitter:card", content: "summary_large_image" },
      {
        name: "twitter:image",
        content: "https://master-card-coral.vercel.app/og.png",
      },
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
