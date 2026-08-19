import { useQuery, useMutation } from "@tanstack/react-query";

const DEFAULT_REMOTE_API = "https://master-card.onrender.com";
const API_BASE = (
  import.meta.env.VITE_API_URL
    ? String(import.meta.env.VITE_API_URL).replace(/\/$/, "")
    : import.meta.env.PROD
      ? DEFAULT_REMOTE_API
      : ""
) + "/api";

// ── Types ──
export interface TabularDemoInput {
  amount: number;
  velocity: number;
  device_risk_score: number;
  is_decline: number;
  hour_of_day_sin?: number;
  hour_of_day_cos?: number;
  mcc_risk_weight?: number;
  geo_distance_km?: number;
  card_age_days?: number;
  failed_attempts_24h?: number;
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

// ── Pipeline Hooks ──

export interface PipelineGenerateInput {
  vector: string;
  n_samples: number;
  fraud_pct: number;
  llm_model?: string;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function usePipelineMutation<TInput = void>(endpoint: string) {
  return useMutation({
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    mutationFn: async (input?: TInput): Promise<any> => {
      const res = await fetch(`${API_BASE}/pipeline/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: input ? JSON.stringify(input) : "{}",
      });
      if (!res.ok) {
        const err = await res.text();
        throw new Error(err);
      }
      return res.json();
    },
  });
}

export function usePipelineGenerate() {
  return usePipelineMutation<PipelineGenerateInput>("generate");
}
export function usePipelineTrain() {
  return usePipelineMutation("train");
}
export function usePipelineAttack() {
  return usePipelineMutation("attack");
}
export function usePipelineRetrain() {
  return usePipelineMutation("retrain");
}
export function usePipelineEvaluate() {
  return usePipelineMutation("evaluate");
}
export function usePipelineReset() {
  return usePipelineMutation("reset");
}

// ── LLM Red Team Model Hooks ──

export interface LLMModel {
  id: string;
  name: string;
  provider: "groq" | "gemini";
  provider_display: string;
  badge: string;
  description: string;
  speed: string;
  available: boolean;
}

export interface LLMGenerateInput {
  provider: string;
  model: string;
  num_samples?: number;
}

export interface GeneratedPrompt {
  prompt_text: string;
  attack_type: string;
  severity: string;
}

export interface LLMGenerateResult {
  status: string;
  provider: string;
  model: string;
  prompts: GeneratedPrompt[];
  count: number;
}

export function useLLMModels() {
  return useQuery<{ models: LLMModel[] }>({
    queryKey: ["llm-models"],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/llm/models`);
      if (!res.ok) throw new Error(`API error: ${res.status}`);
      return res.json();
    },
    staleTime: 60_000,
  });
}

export function useLLMGenerate() {
  return useMutation({
    mutationFn: async (input: LLMGenerateInput): Promise<LLMGenerateResult> => {
      const res = await fetch(`${API_BASE}/llm/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input),
      });
      if (!res.ok) {
        const err = await res.text();
        throw new Error(err);
      }
      return res.json();
    },
  });
}

// ── Cross-Vector Compound Simulation Hooks ──

export interface CrossVectorScenarioResult {
  scenario_id: string;
  name: string;
  target_account: string;
  phase_1_result: {
    prompt_text: string;
    attack_type: string;
    risk_score: number;
    threshold: number;
    verdict: string;
    model: string;
  };
  phase_2_result: {
    attack_type: string;
    risk_score: number;
    threshold: number;
    verdict: string;
    transactions: {
      step: string;
      amount: number;
      velocity: number;
      device_risk_score: number;
      fraud_probability?: number;
      verdict?: string;
    }[];
    model: string;
  };
  phase_3_result: {
    attack_type: string;
    risk_score: number;
    threshold: number;
    verdict: string;
    hops: {
      hop: number;
      sender: string;
      receiver: string;
      amount: number;
      delay_sec: number;
    }[];
    model: string;
  };
  fusion_breakdown: {
    text_risk: number;
    tabular_risk: number;
    graph_risk: number;
    joint_formula: string;
    synergy_boost: number;
    correlated_risk_score: number;
    correlated_risk_pct: number;
  };
  autonomous_enforcement: {
    action: string;
    severity: string;
    description: string;
    interception_timeline_ms: number;
  };
}

export function useCrossVectorSimulation(scenarioId: number) {
  return useQuery<CrossVectorScenarioResult>({
    queryKey: ["cross-vector-sim", scenarioId],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/simulate/cross_vector?scenario_id=${scenarioId}`);
      if (!res.ok) throw new Error(`API error: ${res.status}`);
      return res.json();
    },
    staleTime: 10_000,
  });
}

export function useCrossVectorEvaluate() {
  return useMutation<CrossVectorScenarioResult, Error, any>({
    mutationFn: async (customScenario: any) => {
      const res = await fetch(`${API_BASE}/simulate/cross_vector_evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(customScenario),
      });
      if (!res.ok) {
        const err = await res.text();
        throw new Error(err);
      }
      return res.json();
    },
  });
}




