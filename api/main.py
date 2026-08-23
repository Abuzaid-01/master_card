"""
FastAPI Backend for SENTRIX AI — Tri-Vector Compound Fraud Defense Platform
Serves real-time data from Step 2 (Generation), Step 3 (Defense), and Step 4 (Closed-Loop Retraining).
"""

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import sys
import json
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# Ensure project root is importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from generate.generator_tabular import TABULAR_FEATURE_COLS

app = FastAPI(title="SENTRIX AI API", version="2.0.0")

# CORS for React frontend (Localhost & Cloud deployments)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Paths ──
DEFEND_DIR = os.path.join(PROJECT_ROOT, "data", "defend")
LOOP_DIR = os.path.join(PROJECT_ROOT, "data", "loop")
SYNTHETIC_DIR = os.path.join(PROJECT_ROOT, "data", "synthetic")
MODELS_DIR = os.path.join(PROJECT_ROOT, "defend", "models")

# ── Dynamic MTime-Aware Model Loaders ──
_tabular_model = None
_tabular_mtime = 0
_text_detector = None
_text_mtime = 0
_graph_model = None
_graph_mtime = 0


def _load_tabular_model():
    global _tabular_model, _tabular_mtime
    path = os.path.join(MODELS_DIR, "card_testing_xgb.joblib")
    if os.path.exists(path):
        current_mtime = os.path.getmtime(path)
        if _tabular_model is None or current_mtime > _tabular_mtime:
            import joblib
            import xgboost as xgb
            data = joblib.load(path)
            if isinstance(data, xgb.XGBClassifier):
                _tabular_model = data
            elif isinstance(data, dict):
                _tabular_model = data.get("xgb_model", data.get("model"))
            else:
                _tabular_model = data
            _tabular_mtime = current_mtime
    return _tabular_model


def _load_text_detector():
    global _text_detector, _text_mtime
    path = os.path.join(MODELS_DIR, "text_detector.joblib")
    if os.path.exists(path):
        current_mtime = os.path.getmtime(path)
        if _text_detector is None or current_mtime > _text_mtime:
            import joblib
            data = joblib.load(path)
            from defend.detector_text import TextPromptInjectionDetector
            det = TextPromptInjectionDetector()
            if isinstance(data, dict):
                det.tfidf_vectorizer = data.get("tfidf_vectorizer")
                det.tfidf_model = data.get("tfidf_model")
                det.calibrated_classifier = data.get("calibrated_classifier")
                det.optimal_threshold = data.get("optimal_threshold", 0.50)
                det.attack_embeddings = data.get("attack_embeddings")
                det.legit_embeddings = data.get("legit_embeddings")
                det._init_sentence_transformer()
            _text_detector = det
            _text_mtime = current_mtime
    return _text_detector


def _load_graph_model():
    global _graph_model, _graph_mtime
    path = os.path.join(MODELS_DIR, "graph_detector.joblib")
    if os.path.exists(path):
        current_mtime = os.path.getmtime(path)
        if _graph_model is None or current_mtime > _graph_mtime:
            import joblib
            data = joblib.load(path)
            if isinstance(data, dict):
                _graph_model = data.get("model", data)
            else:
                _graph_model = data
            _graph_mtime = current_mtime
    return _graph_model


def _load_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


# ══════════════════════════════════════════
# GET ENDPOINTS — Serve live metrics
# ══════════════════════════════════════════

@app.get("/api/metrics")
def get_metrics():
    """Returns Step 3 defense metrics from metrics_report.json."""
    data = _load_json(os.path.join(DEFEND_DIR, "metrics_report.json"))
    if not data:
        raise HTTPException(404, "metrics_report.json not found. Run defend pipeline first.")
    return data


@app.get("/api/closed-loop")
def get_closed_loop():
    """Returns Step 4 closed-loop report from closed_loop_report.json."""
    data = _load_json(os.path.join(LOOP_DIR, "closed_loop_report.json"))
    if not data:
        raise HTTPException(404, "closed_loop_report.json not found. Run closed loop first.")
    return data


@app.get("/api/fidelity")
def get_fidelity():
    """Returns Step 2 fidelity report from fidelity_report.json."""
    data = _load_json(os.path.join(SYNTHETIC_DIR, "fidelity_report.json"))
    if not data:
        raise HTTPException(404, "fidelity_report.json not found. Run generation pipeline first.")
    return data


@app.get("/")
@app.get("/health")
@app.get("/api/health")
def health():
    """Health check endpoint."""
    models_loaded = {
        "tabular_model": os.path.exists(os.path.join(MODELS_DIR, "card_testing_xgb.joblib")),
        "text_detector": os.path.exists(os.path.join(MODELS_DIR, "text_detector.joblib")),
        "graph_detector": os.path.exists(os.path.join(MODELS_DIR, "graph_detector.joblib")),
    }
    reports = {
        "metrics_report": os.path.exists(os.path.join(DEFEND_DIR, "metrics_report.json")),
        "closed_loop_report": os.path.exists(os.path.join(LOOP_DIR, "closed_loop_report.json")),
        "fidelity_report": os.path.exists(os.path.join(SYNTHETIC_DIR, "fidelity_report.json")),
    }
    return {"status": "ok", "service": "sentrix-ai", "models": models_loaded, "reports": reports}


# ══════════════════════════════════════════
# POST ENDPOINTS — Live Demo Inference
# ══════════════════════════════════════════

class TabularRequest(BaseModel):
    amount: float = Field(default=250.0, ge=0, description="Transaction amount in USD")
    velocity: float = Field(default=3.0, ge=0, description="Transactions per hour")
    device_risk_score: float = Field(default=0.5, ge=0, le=1, description="Device risk 0-1")
    is_decline: int = Field(default=0, ge=0, le=1, description="Previous decline flag")
    hour_of_day_sin: float = Field(default=0.0, description="Cyclical diurnal sin")
    hour_of_day_cos: float = Field(default=1.0, description="Cyclical diurnal cos")
    mcc_risk_weight: float = Field(default=0.40, description="Merchant category risk weight (0-1)")
    geo_distance_km: float = Field(default=12.5, ge=0, description="Distance from home address (km)")
    card_age_days: float = Field(default=365.0, ge=0, description="Account card age in days")
    failed_attempts_24h: int = Field(default=0, ge=0, description="Failed CVV/PIN attempts in last 24h")


class TextRequest(BaseModel):
    prompt_text: str = Field(default="What is my account balance?", description="Chat prompt to analyze")


@app.post("/api/demo/tabular")
def demo_tabular(req: TabularRequest):
    """Live XGBoost fraud detection inference with SHAP explanation across 9 features."""
    model = _load_tabular_model()
    if model is None:
        raise HTTPException(503, "Tabular model not loaded. Run defend pipeline first.")

    feature_names = list(TABULAR_FEATURE_COLS)
    req_dict = req.model_dump()
    features = np.array([[req_dict.get(f, 0.0) for f in feature_names]], dtype=np.float32)
    prob = float(model.predict_proba(features)[0][1])
    verdict = "FRAUD" if prob >= 0.5 else "SAFE"

    # SHAP explanation
    shap_values = []
    try:
        import shap
        explainer = shap.TreeExplainer(model)
        sv = explainer.shap_values(features)
        for i, fn in enumerate(feature_names):
            s_val = float(sv[0][i])
            shap_values.append({
                "feature": fn,
                "value": float(req_dict.get(fn, 0.0)),
                "shap": s_val,
                "impact": "Increases Risk" if s_val > 0 else "Decreases Risk"
            })
        shap_values.sort(key=lambda x: abs(x["shap"]), reverse=True)
    except Exception:
        pass

    return {
        "fraud_probability": round(prob, 4),
        "verdict": verdict,
        "threshold": 0.5,
        "optimal_threshold": 0.35,
        "verdict_optimized": "FRAUD" if prob >= 0.35 else "SAFE",
        "shap_explanation": shap_values,
        "input": req.model_dump(),
    }


@app.post("/api/demo/text")
def demo_text(req: TextRequest):
    """Live prompt injection detection using Calibrated Semantic model vs TF-IDF."""
    detector = _load_text_detector()
    if detector is None:
        raise HTTPException(503, "Text detector not loaded. Run defend pipeline first.")

    df_input = pd.DataFrame([{"prompt_text": req.prompt_text}])

    # TF-IDF score
    tfidf_prob = 0.0
    try:
        if hasattr(detector, "tfidf_vectorizer") and detector.tfidf_vectorizer is not None:
            tfidf_prob = float(detector.predict_proba_tfidf(df_input)[0])
    except Exception:
        pass

    # Semantic score
    semantic_prob = 0.0
    try:
        if hasattr(detector, "predict_proba_semantic"):
            semantic_prob = float(detector.predict_proba_semantic(df_input)[0])
    except Exception:
        pass

    # Decision threshold from calibrated detector
    eff_threshold = getattr(detector, "optimal_threshold", 0.50)
    verdict = "BLOCKED" if semantic_prob >= eff_threshold else "SAFE"

    return {
        "tfidf_score": round(tfidf_prob, 4),
        "semantic_score": round(semantic_prob, 4),
        "combined_score": round(semantic_prob, 4),
        "optimal_threshold": round(eff_threshold, 4),
        "verdict": verdict,
        "prompt_text": req.prompt_text,
        "analysis": {
            "tfidf_verdict": "BLOCKED" if tfidf_prob >= 0.5 else "SAFE",
            "semantic_verdict": "BLOCKED" if semantic_prob >= eff_threshold else "SAFE",
            "semantic_advantage": round(semantic_prob - tfidf_prob, 4),
        }
    }


# ══════════════════════════════════════════
# CROSS-VECTOR COMPOUND FRAUD SIMULATION (#7)
# ══════════════════════════════════════════

@app.get("/api/simulate/cross_vector")
def simulate_cross_vector_scenario(scenario_id: int = 0):
    """Simulates and dynamically evaluates a coordinated multi-stage cross-vector fraud attack scenario."""
    from generate.generator_cross_vector import generate_compound_fraud_scenario
    from defend.cross_vector_fusion import evaluate_cross_vector_scenario
    
    raw_scenario = generate_compound_fraud_scenario(scenario_id=scenario_id, evaluate_live=False)
    result = evaluate_cross_vector_scenario(
        raw_scenario,
        text_detector=_load_text_detector(),
        tabular_detector=_load_tabular_model(),
        graph_detector=_load_graph_model()
    )
    return result


@app.post("/api/simulate/cross_vector_evaluate")
def evaluate_custom_cross_vector_scenario(scenario: dict):
    """Dynamically evaluates a custom cross-vector attack scenario submitted by the user."""
    from defend.cross_vector_fusion import evaluate_cross_vector_scenario
    return evaluate_cross_vector_scenario(
        scenario,
        text_detector=_load_text_detector(),
        tabular_detector=_load_tabular_model(),
        graph_detector=_load_graph_model()
    )


# ══════════════════════════════════════════
# LLM MODEL CATALOG & RED TEAM GENERATION
# ══════════════════════════════════════════

def _get_available_llm_models():
    from generate.generator_text import load_env_file
    load_env_file()
    has_groq = bool(os.getenv("GROQ_API_KEY"))
    has_gemini = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))

    return [
        {
            "id": "openai/gpt-oss-120b",
            "name": "GPT OSS 120B",
            "provider": "groq",
            "provider_display": "Groq Cloud",
            "badge": "120B Open Weights",
            "description": "High-capacity 120-billion parameter reasoning model on Groq LPU inference.",
            "speed": "Fast (Groq LPU)",
            "available": has_groq,
        },
        {
            "id": "gemini-3.5-flash-lite",
            "name": "Gemini 3.5 Flash Lite",
            "provider": "gemini",
            "provider_display": "Google Gemini",
            "badge": "Flagship Lite",
            "description": "Google's newest 3.5 Flash Lite model with high reasoning speed and low latency.",
            "speed": "Ultra-Fast (Google API)",
            "available": has_gemini,
        },
        {
            "id": "gemini-3.1-flash-lite",
            "name": "Gemini 3.1 Flash Lite",
            "provider": "gemini",
            "provider_display": "Google Gemini",
            "badge": "High Efficiency",
            "description": "Google's 3.1 Flash Lite architecture optimized for high-throughput stress testing.",
            "speed": "Ultra-Fast (Google API)",
            "available": has_gemini,
        },
        {
            "id": "llama-3.3-70b-versatile",
            "name": "Llama 3.3 70B",
            "provider": "groq",
            "provider_display": "Groq Cloud",
            "badge": "70B Versatile",
            "description": "Meta's flagship 70B instruction model on Groq's high-speed tensor engine.",
            "speed": "Ultra-Fast (Groq LPU)",
            "available": has_groq,
        },
    ]


class LLMGenerateRequest(BaseModel):
    provider: str = Field(default="auto", description="'groq', 'gemini', or 'auto'")
    model: str = Field(default="openai/gpt-oss-120b", description="Model ID")
    num_samples: int = Field(default=3, ge=1, le=10, description="Number of attacks to generate")


@app.get("/api/llm/models")
def get_llm_models():
    """Returns available LLM red-team models across Groq and Google Gemini."""
    return {"models": _get_available_llm_models()}


@app.post("/api/llm/generate")
def generate_llm_prompts(req: LLMGenerateRequest):
    """Generates synthetic adversarial prompt injections on demand using the chosen LLM."""
    from generate.generator_text import (
        generate_via_groq,
        generate_via_gemini,
        FALLBACK_INJECTION_TEMPLATES,
        load_env_file,
    )
    load_env_file()
    groq_key = os.getenv("GROQ_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    provider = req.provider.lower()
    if provider == "auto":
        if "gemini" in req.model.lower():
            provider = "gemini"
        else:
            provider = "groq"

    try:
        if provider == "gemini" and gemini_key:
            prompts = generate_via_gemini(gemini_key, model=req.model, num_samples=req.num_samples)
        elif provider == "groq" and groq_key:
            prompts = generate_via_groq(groq_key, model=req.model, num_samples=req.num_samples)
        elif gemini_key:
            prompts = generate_via_gemini(gemini_key, model="gemini-3.5-flash-lite", num_samples=req.num_samples)
        elif groq_key:
            prompts = generate_via_groq(groq_key, model="openai/gpt-oss-120b", num_samples=req.num_samples)
        else:
            prompts = FALLBACK_INJECTION_TEMPLATES[:req.num_samples]

        return {
            "status": "success",
            "provider": provider,
            "model": req.model,
            "prompts": prompts,
            "count": len(prompts),
        }
    except Exception as e:
        raise HTTPException(500, f"LLM Generation failed: {str(e)}")


# ══════════════════════════════════════════
# LIVE PIPELINE ENDPOINTS
# ══════════════════════════════════════════

from api.pipeline_runner import PipelineRunner

_pipeline = PipelineRunner()


class PipelineGenerateRequest(BaseModel):
    vector: str = Field(default="tabular", description="Attack vector to generate (tabular / text / cross_vector)")
    n_samples: int = Field(default=30000, ge=50, le=100000, description="Number of samples")
    fraud_pct: float = Field(default=0.15, ge=0.05, le=0.50, description="Fraud ratio")
    llm_model: Optional[str] = Field(default=None, description="LLM model ID when vector is text")


@app.post("/api/pipeline/generate")
def pipeline_generate(req: PipelineGenerateRequest):
    """Step B: Generate synthetic attack data."""
    try:
        _pipeline.reset()
        result = _pipeline.generate(req.vector, req.n_samples, req.fraud_pct, req.llm_model)
        return {"step": "generate", "status": "success", **result}
    except Exception as e:
        raise HTTPException(500, f"Generation failed: {str(e)}")


@app.post("/api/pipeline/train")
def pipeline_train():
    """Step C: Train Round 1 defender."""
    try:
        result = _pipeline.train_round1()
        return {"step": "train_r1", "status": "success", **result}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Training failed: {str(e)}")


@app.post("/api/pipeline/attack")
def pipeline_attack():
    """Step D: Run adversarial probing against Round 1."""
    try:
        result = _pipeline.attack_round1()
        return {"step": "attack", "status": "success", **result}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Attack failed: {str(e)}")


@app.post("/api/pipeline/retrain")
def pipeline_retrain():
    """Step E: Retrain Round 2 with augmented data."""
    try:
        result = _pipeline.retrain_round2()
        return {"step": "retrain_r2", "status": "success", **result}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Retrain failed: {str(e)}")


@app.post("/api/pipeline/evaluate")
def pipeline_evaluate():
    """Step F: Final R1 vs R2 comparison on unseen holdout."""
    try:
        result = _pipeline.evaluate()
        return {"step": "evaluate", "status": "success", **result}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Evaluation failed: {str(e)}")


@app.post("/api/pipeline/reset")
def pipeline_reset():
    """Reset the pipeline state for a fresh run."""
    _pipeline.reset()
    return {"status": "reset"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, log_level="info")
