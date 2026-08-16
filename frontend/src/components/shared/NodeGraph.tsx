import { motion } from "motion/react";

const nodes = [
  { x: 20, y: 50 },
  { x: 55, y: 22 },
  { x: 58, y: 76 },
  { x: 95, y: 40 },
  { x: 100, y: 82 },
  { x: 135, y: 58 },
];

const edges: [number, number][] = [
  [0, 1],
  [0, 2],
  [1, 3],
  [2, 4],
  [3, 5],
  [4, 5],
  [1, 2],
];

export function NodeGraph() {
  return (
    <svg viewBox="0 0 160 100" className="h-24 w-full" aria-hidden="true">
      {edges.map(([a, b], i) => (
        <motion.line
          key={i}
          x1={nodes[a]!.x}
          y1={nodes[a]!.y}
          x2={nodes[b]!.x}
          y2={nodes[b]!.y}
          stroke="var(--neon-cyan)"
          strokeWidth="0.8"
          opacity={0.5}
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: i * 0.12 }}
        />
      ))}
      {nodes.map((n, i) => (
        <motion.circle
          key={i}
          cx={n.x}
          cy={n.y}
          r={i === 5 ? 5 : 3.2}
          fill={i === 5 ? "var(--mc-red)" : "var(--neon-cyan)"}
          initial={{ opacity: 0, scale: 0 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.3 + i * 0.1 }}
        />
      ))}
    </svg>
  );
}
