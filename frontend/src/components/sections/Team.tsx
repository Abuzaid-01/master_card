import { useEffect, useRef } from "react";
import { Github, Linkedin } from "lucide-react";
import { Reveal } from "@/components/shared/Section";

export function Team() {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.play().catch(() => {
        // Autoplay may need user gesture in strict browser modes
      });
    }
  }, []);

  return (
    <section
      id="team"
      className="snap-section relative flex min-h-screen w-full flex-col items-center justify-center overflow-hidden px-5 py-24 text-center sm:px-8"
    >
      {/* ── Background Video Layer ── */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden select-none z-0">
        <video
          ref={videoRef}
          autoPlay
          loop
          muted
          playsInline
          preload="auto"
          className="absolute inset-0 h-full w-full object-cover object-center opacity-80 transition-opacity duration-700"
          style={{
            filter: "contrast(1.1) brightness(0.9) saturate(1.1)",
          }}
        >
          <source src="/footer_bg.mp4" type="video/mp4" />
        </video>
      </div>

      {/* ── Seamless Background Overlays ── */}
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-40 z-[1]"
        style={{
          background:
            "linear-gradient(to bottom, var(--background) 0%, rgba(3, 7, 18, 0.7) 50%, transparent 100%)",
        }}
      />
      <div
        className="pointer-events-none absolute inset-0 z-[2]"
        style={{
          background:
            "radial-gradient(ellipse 90% 75% at 50% 50%, rgba(0, 240, 255, 0.05) 0%, rgba(3, 7, 18, 0.4) 40%, rgba(3, 7, 18, 0.8) 80%, rgba(3, 7, 18, 0.95) 100%)",
        }}
      />
      <div
        className="pointer-events-none absolute inset-x-0 bottom-0 h-36 z-[3]"
        style={{
          background:
            "linear-gradient(to top, var(--background) 0%, rgba(3, 7, 18, 0.8) 50%, transparent 100%)",
        }}
      />

      {/* ── Original Foreground Content ── */}
      <div className="relative z-10 mx-auto w-full max-w-3xl">
        <Reveal>
          <div className="flex justify-center">
            <img
              src="/sentrix_logo.png"
              alt="SENTRIX AI"
              className="h-20 w-20 rounded-2xl shadow-2xl ring-1 ring-cyan/40 filter drop-shadow-[0_0_25px_rgba(0,240,255,0.45)]"
            />
          </div>
          <div className="mt-6 font-mono text-xs tracking-[0.28em] text-cyan uppercase">
            Platform Architecture
          </div>
          <h2 className="mt-4 text-3xl font-bold tracking-tight sm:text-5xl">
            <span className="text-glow-cyan">SENTRIX AI</span>
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-sm text-foreground/90 sm:text-base font-normal leading-relaxed">
            We use AI to create realistic cyber attacks, train our defenses to block them in real-time, and make the system smarter every round.
          </p>
          <p className="mt-3 font-mono text-xs text-glow-cyan uppercase tracking-[0.25em]">
            ATTACK → DEFEND → EVOLVE
          </p>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <a
              href="https://github.com/Abuzaid-01/master_card"
              target="_blank"
              rel="noreferrer"
              className="glass-panel glow-cyan inline-flex items-center gap-2 rounded-full px-6 py-3 text-sm font-medium transition-transform duration-300 hover:-translate-y-0.5"
            >
              <Github className="h-4 w-4 text-cyan" />
              View Source Repository
            </a>
            <a
              href="https://www.linkedin.com/in/abuzaid01"
              target="_blank"
              rel="noreferrer"
              className="glass-panel glow-cyan inline-flex items-center gap-2 rounded-full px-6 py-3 text-sm font-medium transition-transform duration-300 hover:-translate-y-0.5 border border-cyan/30 hover:border-cyan/60"
            >
              <Linkedin className="h-4 w-4 text-cyan" />
              Connect on LinkedIn
            </a>
          </div>

          <div className="mt-12 flex justify-center">
            <div className="group inline-flex items-center gap-2.5 rounded-full border border-white/10 bg-black/40 px-6 py-2.5 backdrop-blur-md transition-all duration-300 ease-out hover:scale-110 hover:-translate-y-1 hover:border-cyan/50 hover:bg-black/70 hover:shadow-[0_0_30px_rgba(0,229,255,0.3)] cursor-default">
              <span className="h-1.5 w-1.5 rounded-full bg-cyan animate-pulse" />
              <p className="font-mono text-xs sm:text-sm font-medium tracking-wide text-foreground/90 transition-colors duration-300 group-hover:text-cyan group-hover:text-glow-cyan">
                Protecting Payments with AI That Never Stops Learning
              </p>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
