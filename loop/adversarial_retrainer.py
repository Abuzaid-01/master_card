"""
Adversarial Retrainer: Augments original training pool with mined adversarial failures
and trains Round 2 defense models.
"""

import os
import numpy as np
import pandas as pd
import joblib
from typing import Dict, Any

DEFEND_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "defend")
LOOP_MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "loop", "models")


def retrain_round2(
    blind_spot_results: dict,
    original_training_data: dict,
) -> Dict[str, Any]:
    """
    Augments original Step 3 training data with mined adversarial failure samples.
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
        df_augmented = df_augmented.drop_duplicates().sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        feature_cols = ["amount", "velocity", "device_risk_score", "is_decline"]
        X_train = df_augmented[feature_cols].values.astype(float)
        y_train = df_augmented["is_fraud"].values
        
        n_pos = (y_train == 1).sum()
        n_neg = (y_train == 0).sum()
        spw = max(1.0, n_neg / max(1, n_pos))
        
        import xgboost as xgb
        model_r2 = xgb.XGBClassifier(
            n_estimators=200, max_depth=5, learning_rate=0.1,
            scale_pos_weight=spw, eval_metric="aucpr",
            random_state=42, use_label_encoder=False
        )
        model_r2.fit(X_train, y_train)
        
        # Export ONNX
        onnx_path = os.path.join(LOOP_MODELS_DIR, "card_testing_xgb_round2.onnx")
        try:
            import onnxmltools
            from onnxmltools.convert.common.data_types import FloatTensorType
            onnx_model = onnxmltools.convert_xgboost(
                model_r2.get_booster(),
                initial_types=[("features", FloatTensorType([None, len(feature_cols)]))]
            )
            onnxmltools.utils.save_model(onnx_model, onnx_path)
            print(f"      -> Round 2 ONNX exported: {onnx_path}")
        except Exception as e:
            print(f"      -> ONNX export warning: {e}")
        
        # Save joblib
        joblib_path = os.path.join(LOOP_MODELS_DIR, "card_testing_xgb_round2.joblib")
        joblib.dump({"xgb_model": model_r2}, joblib_path)
        
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
        df_augmented = df_augmented.drop_duplicates().sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        graph_features = [c for c in ["amount", "sender_in_degree", "sender_out_degree",
                                       "receiver_in_degree", "receiver_out_degree",
                                       "receiver_mule_funnel_score",
                                       "pass_through_delay_sec"] if c in df_augmented.columns]
        
        X_train = df_augmented[graph_features].values.astype(float)
        y_train = df_augmented["is_fraud"].values
        
        from sklearn.ensemble import HistGradientBoostingClassifier
        n_pos = (y_train == 1).sum()
        n_neg = (y_train == 0).sum()
        
        sample_weights = np.where(y_train == 1, n_neg / max(1, n_pos), 1.0)
        
        model_r2 = HistGradientBoostingClassifier(
            max_iter=200, max_depth=5, learning_rate=0.1, random_state=42
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
        print("\n[Round 2 Retraining] TEXT: Expanding attack embedding index with missed prompts...")
        
        df_orig_train = original_training_data["text"]
        text_result = blind_spot_results["text"]
        missed_indices = text_result["missed_indices"]
        df_missed = text_result["df_mine_fraud"].iloc[missed_indices] if missed_indices else pd.DataFrame()
        
        # Augment training data with the missed prompts (preserve original dataset integrity)
        df_augmented = pd.concat([df_orig_train, df_missed], ignore_index=True)
        
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
            "adversarial_samples_added": len(df_missed),
            "missed_prompts_added": len(df_missed),
        }
        print(f"      -> Round 2 Text Detector trained on {len(df_augmented)} prompts "
              f"(+{len(df_missed)} missed attack prompts)")

    return round2_models
