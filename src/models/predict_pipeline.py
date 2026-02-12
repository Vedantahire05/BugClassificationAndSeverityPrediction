# src/models/predict_pipeline.py

import joblib
import numpy as np
from src.severity.ordinal_severity import compute_severity_score


# -----------------------------
# LOAD MODELS
# -----------------------------
try:
    type_model = joblib.load("saved_models/type_model.pkl")
    type_vec = joblib.load("saved_models/type_vectorizer.pkl")
    type_mlb = joblib.load("saved_models/type_mlb.pkl")

    sev_model = joblib.load("saved_models/severity_ordinal.pkl")
    sev_vec = joblib.load("saved_models/severity_vectorizer.pkl")

except FileNotFoundError as e:
    raise RuntimeError(
        "Saved models not found. Train models locally and push saved_models/ folder."
    ) from e


# -----------------------------
# TYPE INFERENCE
# -----------------------------
def predict_types(text: str, threshold: float = 0.30):
    Xt = type_vec.transform([text])
    probs = type_model.predict_proba(Xt)[0]

    labels = [
        type_mlb.classes_[i]
        for i, p in enumerate(probs)
        if p >= threshold
    ]

    if not labels:
        labels = [type_mlb.classes_[probs.argmax()]]

    return labels


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def predict(text: str):

    # TYPE
    types = predict_types(text)

    # SEVERITY
    Xs = sev_vec.transform([text])
    ml_score = sev_model.predict(Xs)[0]

    severity, score, explain = compute_severity_score(
        ml_score,
        text,
        types
    )

    return {
        "type": types,
        "severity": severity,
        "severity_score": score,
        "explanation": explain
    }


# -----------------------------
# LOCAL TEST
# -----------------------------
if __name__ == "__main__":
    samples = [
        "UI alignment broken on dashboard",
        "node fails under heavy load leading to crash",
        "security vulnerability in jwt handler",
        "docs missing for installation",
        "slow inference performance in training pipeline"
    ]

    for s in samples:
        print("\nTEXT:", s)
        print("PRED:", predict(s))