export function SentrixMark({
  className = "",
  pulse = false,
}: {
  className?: string;
  pulse?: boolean;
}) {
  return (
    <svg
      viewBox="0 0 48 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="sentrix-cyan-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#00F0FF" />
          <stop offset="100%" stopColor="#3B82F6" />
        </linearGradient>
        <linearGradient id="sentrix-violet-grad" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#8B5CF6" />
          <stop offset="100%" stopColor="#00F0FF" />
        </linearGradient>
        <linearGradient id="sentrix-glow" x1="50%" y1="0%" x2="50%" y2="100%">
          <stop offset="0%" stopColor="#00F0FF" stopOpacity="0.8" />
          <stop offset="100%" stopColor="#8B5CF6" stopOpacity="0.2" />
        </linearGradient>
        <filter id="sentrix-blur" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="2" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>

      {/* Ambient background glow */}
      <circle
        cx="24"
        cy="24"
        r="18"
        fill="url(#sentrix-glow)"
        opacity={pulse ? "0.35" : "0.2"}
        className={pulse ? "animate-pulse" : undefined}
      />

      {/* Hexagonal Outer Tri-Vector Shield */}
      <path
        d="M24 3L42 13.5V34.5L24 45L6 34.5V13.5L24 3Z"
        stroke="url(#sentrix-cyan-grad)"
        strokeWidth="2.5"
        strokeLinejoin="round"
        fill="none"
        opacity="0.9"
      />

      {/* Inner Tri-Vector Stylized "S" / Nexus Defense Core */}
      <path
        d="M32 14H18C15.7909 14 14 15.7909 14 18V21C14 23.2091 15.7909 25 18 25H30C32.2091 25 34 26.7909 34 29V32C34 34.2091 32.2091 36 30 36H16"
        stroke="url(#sentrix-cyan-grad)"
        strokeWidth="3.2"
        strokeLinecap="round"
        strokeLinejoin="round"
        filter="url(#sentrix-blur)"
      />

      {/* Center Tri-Vector Power Nodes */}
      <circle cx="24" cy="14" r="2" fill="#00F0FF" />
      <circle cx="24" cy="25" r="2.5" fill="#FFFFFF" />
      <circle cx="24" cy="36" r="2" fill="#8B5CF6" />
    </svg>
  );
}
