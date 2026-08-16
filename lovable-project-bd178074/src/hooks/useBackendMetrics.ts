import { useQuery, useMutation } from "@tanstack/react-query";

const API_BASE = "/api";

// ── Types ──
export interface TabularDemoInput {
  amount: number;
  velocity: number;
  device_risk_score: number;
  is_decline: number;
}

export interface TabularDemoResult {
  fraud_probability: number;
  verdict: string;
  threshold: number;
  optimal_threshold: number;
  verdict_optimized: string;
  shap_explanation: {
    feature: string;
    value: number;
    shap: number;
    impact: string;
  }[] | null;
  input: TabularDemoInput;
}

export interface TextDemoInput {
  prompt_text: string;
}

export interface TextDemoResult {
  tfidf_score: number;
  semantic_score: number;
  combined_score: number;
  verdict: string;
  prompt_text: string;
  analysis: {
    tfidf_verdict: string;
    semantic_verdict: string;
    semantic_advantage: number;
  };
}

// ── Metric Hooks ──
export function useMetrics() {
  return useQuery({
    queryKey: ["metrics"],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/metrics`);
      if (!res.ok) return null;
      return res.json();
    },
    retry: 1,
    staleTime: 60_000,
  });
}

export function useClosedLoop() {
  return useQuery({
    queryKey: ["closed-loop"],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/closed-loop`);
      if (!res.ok) return null;
      return res.json();
    },
    retry: 1,
    staleTime: 60_000,
  });
}

export function useFidelity() {
  return useQuery({
    queryKey: ["fidelity"],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/fidelity`);
      if (!res.ok) return null;
      return res.json();
    },
    retry: 1,
    staleTime: 60_000,
  });
}

export function useHealthCheck() {
  return useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/health`);
      if (!res.ok) return { status: "offline" };
      return res.json();
    },
    retry: 1,
    staleTime: 10_000,
    refetchInterval: 30_000,
  });
}

// ── Live Demo Mutations ──
export function useTabularDemo() {
  return useMutation({
    mutationFn: async (input: TabularDemoInput): Promise<TabularDemoResult> => {
      const res = await fetch(`${API_BASE}/demo/tabular`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input),
      });
      if (!res.ok) throw new Error(`API error: ${res.status}`);
      return res.json();
    },
  });
}

export function useTextDemo() {
  return useMutation({
    mutationFn: async (input: TextDemoInput): Promise<TextDemoResult> => {
      const res = await fetch(`${API_BASE}/demo/text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input),
      });
      if (!res.ok) throw new Error(`API error: ${res.status}`);
      return res.json();
    },
  });
}
