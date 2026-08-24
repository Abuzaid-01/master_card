"""
Adversarial Retrainer: Augments training pool with mined adversarial failures
and trains Round 2 & Round 3 defense models across Tabular, Text, and Graph vectors.
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
from typing import Dict, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from generate.generator_tabular import TABULAR_FEATURE_COLS

DEFEND_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "defend")
LOOP_MODELS_DIR = os.path.join(PROJECT_ROOT, "data", "loop", "models")


def retrain_round2(
    blind_spot_results: dict,
    original_training_data: dict,
) -> Dict[str, Any]:
    """
    Augments original training data with mined adversarial failure samples.
    Retrains Round 2 models and exports them.
    """
    os.makedirs(LOOP_MODELS_DIR, exist_ok=True)
    round2_models = {}

    # ── TABULAR ROUND 2 ──
    if "tabular" in blind_spot_results and "tabular" in original_training_data:
        print("\n[Round 2 Retraining] TABULAR: Augmenting training data with adversarial failures...")
        
        df_orig_train = original_training_data["tabular"]
        df_failures = blind_spot_results["tabular"]["df_failures"]
        
        # Augment: combine original training + evaded adversarial samples
        df_augmented = pd.concat([df_orig_train, df_failures], ignore_index=True)
        df_augmented = df_augmented.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        feature_cols = list(TABULAR_FEATURE_COLS)
        for col in feature_cols:
            if col not in df_augmented.columns:
                df_augmented[col] = 0.0

        X_train = df_augmented[feature_cols].values.astype(np.float32)
        y_train = df_augmented["is_fraud"].values
        
        n_pos = (y_train == 1).sum()
        n_neg = (y_train == 0).sum()
        spw = max(1.0, float(n_neg / max(1, n_pos)))
        
        import xgboost as xgb
        model_r2 = xgb.XGBClassifier(
            n_estimators=300, max_depth=6, learning_rate=0.06,
            subsample=0.85, colsample_bytree=0.85,
            scale_pos_weight=spw, eval_metric="aucpr",
            random_state=42
        )
        model_r2.fit(X_train, y_train)
        
        # Export ONNX
        onnx_path = os.path.join(LOOP_MODELS_DIR, "card_testing_xgb_round2.onnx")
        try:
            import onnxmltools
            from onnxmltools.convert.common.data_types import FloatTensorType
            booster = model_r2.get_booster()
            orig_names = booster.feature_names
            booster.feature_names = [f"f{i}" for i in range(len(feature_cols))]
            initial_types = [("input", FloatTensorType([None, len(feature_cols)]))]
            onnx_model = onnxmltools.convert_xgboost(booster, initial_types=initial_types)
            with open(onnx_path, "wb") as f:
                f.write(onnx_model.SerializeToString())
            booster.feature_names = orig_names
            print(f"      -> Round 2 ONNX exported: {onnx_path}")
        except Exception as e:
            print(f"      -> ONNX export warning: {e}")
        
        # Save joblib
        joblib_path = os.path.join(LOOP_MODELS_DIR, "card_testing_xgb_round2.joblib")
        joblib.dump({"xgb_model": model_r2, "feature_cols": feature_cols}, joblib_path)
        
        round2_models["tabular"] = {
            "model": model_r2,
            "onnx_path": onnx_path,
            "joblib_path": joblib_path,
            "augmented_train_size": len(df_augmented),
            "original_train_size": len(df_orig_train),
            "adversarial_samples_added": len(df_failures),
        }
        print(f"      -> Round 2 XGBoost trained on {len(df_augmented)} samples "
              f"(+{len(df_failures)} adversarial)")

    # ── GRAPH ROUND 2 ──
    if "graph" in blind_spot_results and "graph" in original_training_data:
        print("\n[Round 2 Retraining] GRAPH: Augmenting training data with adversarial failures...")
        
        df_orig_train = original_training_data["graph"]
        df_failures = blind_spot_results["graph"]["df_failures"]
        
        df_augmented = pd.concat([df_orig_train, df_failures], ignore_index=True)
        df_augmented = df_augmented.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        from generate.generator_graph import GRAPH_FEATURE_COLS
        graph_features = list(GRAPH_FEATURE_COLS)
        X_train = df_augmented[graph_features].astype(float)
        y_train = df_augmented["is_fraud"].values
        
        from sklearn.ensemble import HistGradientBoostingClassifier
        n_pos = (y_train == 1).sum()
        n_neg = (y_train == 0).sum()
        
        sample_weights = np.where(y_train == 1, float(n_neg / max(1, n_pos)), 1.0)
        
        model_r2 = HistGradientBoostingClassifier(
            max_iter=300, min_samples_leaf=5, learning_rate=0.06, random_state=42
        )
        model_r2.fit(X_train, y_train, sample_weight=sample_weights)
        
        joblib_path = os.path.join(LOOP_MODELS_DIR, "graph_detector_round2.joblib")
        joblib.dump(model_r2, joblib_path)
        
        round2_models["graph"] = {
            "model": model_r2,
            "joblib_path": joblib_path,
            "augmented_train_size": len(df_augmented),
            "original_train_size": len(df_orig_train),
            "adversarial_samples_added": len(df_failures),
        }
        print(f"      -> Round 2 GBDT trained on {len(df_augmented)} samples "
              f"(+{len(df_failures)} adversarial)")

    # ── TEXT ROUND 2 ──
    if "text" in blind_spot_results and "text" in original_training_data:
        print("\n[Round 2 Retraining] TEXT: Expanding attack embedding index with evaded adversarial prompts...")
        
        df_orig_train = original_training_data["text"]
        text_result = blind_spot_results["text"]
        df_failures = text_result.get("df_failures", pd.DataFrame())
        
        if not df_failures.empty:
            df_evaded_attacks = df_failures[df_failures["is_fraud"] == 1].copy()
        else:
            df_evaded_attacks = pd.DataFrame()
        
        # Deduplicate against original training prompts
        if not df_evaded_attacks.empty and "prompt_text" in df_orig_train.columns:
            orig_prompts = set(df_orig_train["prompt_text"].dropna().unique())
            df_evaded_attacks = df_evaded_attacks[~df_evaded_attacks["prompt_text"].isin(orig_prompts)]
        
        # Augment training data with the newly evaded adversarial prompts
        df_augmented = pd.concat([df_orig_train, df_evaded_attacks], ignore_index=True)
        
        # Retrain text detector with expanded embedding index
        from defend.detector_text import TextPromptInjectionDetector
        det_r2 = TextPromptInjectionDetector()
        det_r2.fit(df_augmented)
        text_model_path = os.path.join(LOOP_MODELS_DIR, "text_detector_round2.joblib")
        det_r2.save_model(text_model_path)
        
        round2_models["text"] = {
            "detector": det_r2,
            "joblib_path": text_model_path,
            "augmented_train_size": len(df_augmented),
            "original_train_size": len(df_orig_train),
            "adversarial_samples_added": len(df_evaded_attacks),
            "missed_prompts_added": len(df_evaded_attacks),
        }
        print(f"      -> Round 2 Text Detector trained on {len(df_augmented)} prompts "
              f"(+{len(df_evaded_attacks)} evaded adversarial prompts)")

    return round2_models
