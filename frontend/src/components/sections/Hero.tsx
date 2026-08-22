import { useLayoutEffect, useRef } from "react";
import { ArrowRight, CheckCircle2, ChevronDown, Radio } from "lucide-react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

export function Hero() {
  const rootRef = useRef<HTMLElement>(null);
  const stageRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (!rootRef.current || !stageRef.current) return;

    gsap.registerPlugin(ScrollTrigger);
    const context = gsap.context(() => {
      gsap.set(".js-terminal-approved", { autoAlpha: 0, y: 8 });
      gsap.set(".js-hero-reveal", { autoAlpha: 0, y: 28 });
      gsap.set(".js-risk-progress", { scaleX: 0, transformOrigin: "left center" });
      gsap.set(".js-sequence-path", { scaleX: 0, transformOrigin: "left center" });
      gsap.set(".js-transaction-step", { autoAlpha: 0, y: 18 });

      gsap
        .timeline({
          defaults: { ease: "none" },
          scrollTrigger: {
            trigger: rootRef.current,
            start: "top top",
            end: () => `+=${Math.round(window.innerHeight * 1.65)}`,
            scrub: 0.65,
            pin: rootRef.current,
            pinSpacing: true,
            anticipatePin: 1,
            invalidateOnRefresh: true,
          },
        })
        .to(".js-scroll-cue", { autoAlpha: 0, duration: 0.08 }, 0)
        .to(".js-hero-copy", { autoAlpha: 0, x: -54, duration: 0.18 }, 0.03)
        .to(".js-swipe-card", { left: "78%", top: "54%", rotate: 3, duration: 0.18 }, 0.09)
        .to(".js-swipe-card", { left: "72%", top: "61%", rotate: -1, scale: 0.7, duration: 0.2 }, 0.27)
        .to(".js-card-shine", { xPercent: 115, duration: 0.18 }, 0.29)
        .set(".js-swipe-card", { zIndex: 2 }, 0.46)
        .to(".js-swipe-card", { top: "70%", scale: 0.56, rotate: -2, duration: 0.17 }, 0.46)
        .to(".js-terminal-waiting", { autoAlpha: 0, y: -8, duration: 0.08 }, 0.5)
        .to(".js-terminal-approved", { autoAlpha: 1, y: 0, duration: 0.12 }, 0.56)
        .to(".js-terminal-glow", { opacity: 0.34, scale: 1, duration: 0.16 }, 0.51)
        .to(".js-swipe-card", { top: "75%", autoAlpha: 0, duration: 0.12 }, 0.61)
        .to(".js-card-scene", { autoAlpha: 0, scale: 0.97, duration: 0.14 }, 0.72)
        .to(".js-hero-reveal", { autoAlpha: 1, y: 0, duration: 0.16 }, 0.76)
        .to(".js-risk-progress", { scaleX: 1, duration: 0.16 }, 0.82)
        .to(".js-sequence-path", { scaleX: 1, duration: 0.2 }, 0.84)
        .to(
          ".js-transaction-step",
          { autoAlpha: 1, y: 0, duration: 0.08, stagger: 0.045 },
          0.84,
        );
    }, rootRef);

    return () => context.revert();
  }, []);

  return (
    <section ref={rootRef} id="hero" className="surreal-hero">
      <div ref={stageRef} className="surreal-hero__stage">
        <div className="surreal-noise" aria-hidden="true" />
        <div className="surreal-orbit surreal-orbit--one" aria-hidden="true" />
        <div className="surreal-orbit surreal-orbit--two" aria-hidden="true" />

        <div className="surreal-hero__copy js-hero-copy">
          <p className="surreal-kicker"><span /> Adaptive payment intelligence</p>
          <h1>
            Fraud evolves.<br />
            <em>Your defense should too.</em>
          </h1>
          <p className="surreal-hero__lede">
            Sentrix connects every authorization, message, and beneficiary hop—then learns from the
            attack before the next payment arrives.
          </p>
          <div className="surreal-hero__actions">
            <a href="#demo" className="surreal-button surreal-button--primary">
              Open live defender <ArrowRight aria-hidden="true" />
            </a>
            <a href="#identify" className="surreal-button surreal-button--ghost">
              Explore the threat journey
            </a>
          </div>
        </div>

        <div className="surreal-card-scene js-card-scene" aria-label="Card authorization animation">
          <div className="surreal-terminal-glow js-terminal-glow" aria-hidden="true" />
          <div className="surreal-terminal js-terminal">
            <div className="surreal-terminal__screen">
              <div className="js-terminal-waiting">
                <Radio aria-hidden="true" />
                <strong>INSERT CARD</strong>
                <small>WAITING FOR PAYMENT</small>
              </div>
              <div className="surreal-terminal__approved js-terminal-approved">
                <CheckCircle2 aria-hidden="true" />
                <strong>APPROVED</strong>
                <small>RISK SIGNAL CAPTURED</small>
              </div>
            </div>
            <div className="surreal-terminal__keys" aria-hidden="true">
              {Array.from({ length: 9 }).map((_, index) => <span key={index} />)}
            </div>
            <div className="surreal-terminal__slot" aria-hidden="true" />
          </div>

          <div className="surreal-payment-card js-swipe-card">
            <div className="surreal-payment-card__shine js-card-shine" aria-hidden="true" />
            <div className="surreal-payment-card__topline">
              <span>SENTRIX</span>
              <Radio aria-hidden="true" />
            </div>
            <div className="surreal-payment-card__chip" aria-hidden="true" />
            <div className="surreal-payment-card__digits">5412&nbsp; •••• &nbsp;••••&nbsp; 4921</div>
            <div className="surreal-payment-card__footer">
              <span>A. SHARMA&nbsp;&nbsp; 09/29</span>
              <span className="surreal-payment-card__circles" aria-hidden="true"><i /><i /></span>
            </div>
          </div>
        </div>

        <div className="surreal-hero__reveal js-hero-reveal">
          <p>The payment looked ordinary</p>
          <h2>
            The sequence did not.
            <span>Five attempts. Seventeen seconds. One connected fraud campaign.</span>
          </h2>
          <div className="surreal-risk-line"><span className="js-risk-progress" /></div>
          <div className="surreal-risk-labels">
            <span>AUTHORIZATION</span>
            <span>BEHAVIOR</span>
            <span>NETWORK</span>
            <span>DECISION</span>
          </div>

          <div className="surreal-transaction-story" aria-label="Five connected transaction attempts escalating from 199 rupees to 94,000 rupees in 17 seconds">
            <div className="surreal-transaction-story__header">
              <span>Same card · same device · same beneficiary path</span>
              <strong>472× value escalation</strong>
            </div>
            <div className="surreal-transaction-story__track">
              <span className="surreal-transaction-story__path js-sequence-path" aria-hidden="true" />
              <ol>
                <li className="js-transaction-step">
                  <i>01</i>
                  <time>00:00</time>
                  <strong>₹199</strong>
                  <small>Probe</small>
                </li>
                <li className="js-transaction-step">
                  <i>02</i>
                  <time>00:03</time>
                  <strong>₹499</strong>
                  <small>Confirm</small>
                </li>
                <li className="js-transaction-step">
                  <i>03</i>
                  <time>00:07</time>
                  <strong>₹2,499</strong>
                  <small>Build trust</small>
                </li>
                <li className="js-transaction-step">
                  <i>04</i>
                  <time>00:12</time>
                  <strong>₹18,500</strong>
                  <small>Escalate</small>
                </li>
                <li className="js-transaction-step surreal-transaction-story__critical">
                  <i>05</i>
                  <time>00:17</time>
                  <strong>₹94,000</strong>
                  <small>Cash-out request</small>
                </li>
              </ol>
            </div>
            <div className="surreal-transaction-story__footer">
              <span>Each payment looked plausible alone.</span>
              <strong>Sequence risk · Critical</strong>
            </div>
          </div>
        </div>

        <div className="surreal-scroll-cue js-scroll-cue">
          Scroll to swipe
          <ChevronDown aria-hidden="true" />
        </div>
      </div>
    </section>
  );
}
