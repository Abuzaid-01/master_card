export function MastercardMark({
  className = "",
  pulse = false,
}: {
  className?: string;
  pulse?: boolean;
}) {
  return (
    <svg viewBox="0 0 64 40" className={className} aria-hidden="true">
      <circle
        cx="24"
        cy="20"
        r="16"
        fill="var(--mc-red)"
        opacity="0.9"
        className={pulse ? "animate-pulse" : undefined}
      />
      <circle
        cx="40"
        cy="20"
        r="16"
        fill="var(--mc-orange)"
        opacity="0.9"
        className={pulse ? "animate-pulse" : undefined}
      />
      <path
        d="M32 7a16 16 0 000 26 16 16 0 000-26z"
        fill="var(--mc-orange)"
        opacity="0.75"
      />
    </svg>
  );
}
