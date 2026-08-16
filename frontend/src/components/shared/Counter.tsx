import { useEffect, useRef, useState } from "react";
import { useInView } from "motion/react";

type Props = {
  value: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
  duration?: number;
  delay?: number;
  className?: string;
};

const format = (n: number, decimals: number) =>
  decimals > 0
    ? n.toFixed(decimals)
    : Math.round(n).toLocaleString("en-US");

export function Counter({
  value,
  decimals = 0,
  prefix = "",
  suffix = "",
  duration = 1600,
  delay = 0,
  className,
}: Props) {
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true, margin: "-15% 0px" });
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    if (!inView) return;
    let raf = 0;
    let start = 0;
    const timer = window.setTimeout(() => {
      const step = (t: number) => {
        if (!start) start = t;
        const p = Math.min((t - start) / duration, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        setDisplay(value * eased);
        if (p < 1) raf = requestAnimationFrame(step);
      };
      raf = requestAnimationFrame(step);
    }, delay);

    return () => {
      window.clearTimeout(timer);
      cancelAnimationFrame(raf);
    };
  }, [inView, value, duration, delay]);

  return (
    <span ref={ref} className={className}>
      {prefix}
      {format(display, decimals)}
      {suffix}
    </span>
  );
}
