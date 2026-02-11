# # src/models/predict_pipeline.py

# import joblib
# import ast
# import numpy as np


# def safe_parse_list(val):
#     if isinstance(val, list):
#         return val
#     if isinstance(val, str):
#         try:
#             return ast.literal_eval(val)
#         except:
#             return [val]
#     return []


# def load_artifacts():
#     type_model = joblib.load("saved_models/type_model.pkl")
#     type_vec = joblib.load("saved_models/type_vectorizer.pkl")
#     type_mlb = joblib.load("saved_models/type_mlb.pkl")

#     sev_lr = joblib.load("saved_models/severity_lr.pkl")
#     sev_xgb = joblib.load("saved_models/severity_xgb.pkl")
#     sev_vec = joblib.load("saved_models/severity_vectorizer.pkl")
#     sev_le = joblib.load("saved_models/severity_label_encoder.pkl")
#     sev_tab_cols = joblib.load("saved_models/severity_tab_cols.pkl")

#     return {
#         "type_model": type_model,
#         "type_vec": type_vec,
#         "type_mlb": type_mlb,
#         "sev_lr": sev_lr,
#         "sev_xgb": sev_xgb,
#         "sev_vec": sev_vec,
#         "sev_le": sev_le,
#         "sev_tab_cols": sev_tab_cols
#     }


# def compute_severity_tab(type_list, sev_tab_cols):
#     base = {}
#     for col in sev_tab_cols:

#         # one-hot type features
#         if col.startswith("T::"):
#             t = col.split("T::")[1]
#             base[col] = 1 if t in type_list else 0
#             continue

#         # engineered features (placeholders)
#         if col == "severity_raw_enc":
#             base[col] = 1
#             continue
#         if col == "confidence":
#             base[col] = 0.5
#             continue
#         if col == "days_open":
#             base[col] = 30
#             continue

#         base[col] = 0

#     return np.array([[base[c] for c in sev_tab_cols]])


# def apply_hybrid_rules(type_list, text, model_sev):
#     t = text.lower()
#     reasons = []

#     # === DOMAIN RULES ===
#     if "SECURITY" in type_list:
#         return "High", ["security domain (type-level)"]

#     if "PERFORMANCE" in type_list:
#         return "Medium", ["performance domain (type-level)"]

#     if "NETWORK" in type_list and "BUG" in type_list:
#         reasons.append("network failure + bug domain")
#         return "High", reasons

#     if "DOCUMENTATION" in type_list:
#         return "Low", ["documentation domain"]

#     if "UI" in type_list:
#         return "Low", ["visual/UI domain"]

#     # === KEYWORD RULES ===
#     if any(w in t for w in ["crash", "panic", "segfault", "kernel panic", "core dump"]):
#         return "Critical", ["crash keyword"]

#     if any(w in t for w in ["vulnerability", "exploit", "jwt", "xss", "csrf", "security"]):
#         return "High", ["security keyword"]

#     if any(w in t for w in ["slow", "latency", "timeout", "lag", "performance"]):
#         return "Medium", ["performance keyword"]

#     # === HYBRID CONFLICT FIXER ===
#     if model_sev == "Low" and "BUG" in type_list:
#         if any(w in t for w in ["fail", "error", "broken", "does not work", "hang"]):
#             return "Medium", ["functional failure override"]

#     # fallback (no change)
#     return model_sev, []


# def predict(text: str):
#     A = load_artifacts()

#     # === TYPE MODEL ===
#     X_t = A["type_vec"].transform([text])
#     Y_t = A["type_model"].predict(X_t)
#     type_labels = A["type_mlb"].inverse_transform(Y_t)[0]

#     # === SEVERITY MODEL (Hybrid) ===
#     X_s = A["sev_vec"].transform([text])
#     X_tab = compute_severity_tab(type_labels, A["sev_tab_cols"])

#     lr_probs = A["sev_lr"].predict_proba(X_s)
#     xgb_probs = A["sev_xgb"].predict_proba(X_tab)

#     final = (0.55 * xgb_probs + 0.45 * lr_probs)
#     sev_pred = final.argmax(axis=1)
#     model_sev = A["sev_le"].inverse_transform(sev_pred)[0]

#     # === APPLY HYBRID RULES ===
#     severity, reasons = apply_hybrid_rules(type_labels, text, model_sev)

#     return {
#         "type": list(type_labels),
#         "severity": severity,
#         "model_severity": model_sev,
#         "explanation": reasons
#     }


# if __name__ == "__main__":
#     test_samples = [
#         "UI alignment broken on dashboard",
#         "node fails under heavy load leading to crash",
#         "security vulnerability in jwt handler",
#         "docs missing for installation",
#         "slow inference performance in training pipeline"
#     ]

#     for t in test_samples:
#         print("\nTEXT:", t)
#         print("PRED:", predict(t))


# src/models/predict_pipeline.py

import joblib
from src.severity.ordinal_severity import compute_severity_score

type_model = joblib.load("saved_models/type_model.pkl")
type_vec = joblib.load("saved_models/type_vectorizer.pkl")
type_mlb = joblib.load("saved_models/type_mlb.pkl")

sev_model = joblib.load("saved_models/severity_ordinal.pkl")
sev_vec = joblib.load("saved_models/severity_vectorizer.pkl")

def predict(text: str):
    # ---- TYPE ----
    Xt = type_vec.transform([text])
    yt = type_model.predict(Xt)
    types = list(type_mlb.inverse_transform(yt)[0])

    # ---- SEVERITY ----
    Xs = sev_vec.transform([text])
    ml_score = sev_model.predict(Xs)[0]

    severity, score, explain = compute_severity_score(
        ml_score, text, types
    )

    return {
        "type": types,
        "severity": severity,
        "severity_score": score,
        "explanation": explain
    }
