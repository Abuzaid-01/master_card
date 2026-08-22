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
  className,
}: Props) {
  return (
    <span className={className}>
      {prefix}
      {format(value, decimals)}
      {suffix}
    </span>
  );
}
