import { Origami } from "lucide-react";

export function SentrixMark({ className = "" }: { className?: string }) {
  return (
    <span
      className={`sentrix-mark relative inline-flex shrink-0 items-center justify-center ${className}`}
      aria-hidden="true"
    >
      <span className="sentrix-mark__fold" />
      <Origami className="relative z-10 h-[68%] w-[68%]" strokeWidth={1.65} />
    </span>
  );
}
