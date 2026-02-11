import pandas as pd
import joblib
from sklearn.metrics import classification_report, f1_score, confusion_matrix
import numpy as np
import os
import json


ORDER = ["Low", "Medium", "High", "Critical"]
order_idx = {k:i for i,k in enumerate(ORDER)}


def ordering_penalty(y_true, y_pred):
    penalty = 0
    for t, p in zip(y_true, y_pred):
        penalty += abs(order_idx[t] - order_idx[p])
    return penalty / len(y_true)


def run_severity_validation():
    df = pd.read_csv("dataset/cleaned/github_severity_synth.csv")

    sev_lr = joblib.load("saved_models/severity_lr.pkl")
    sev_xgb = joblib.load("saved_models/severity_xgb.pkl")
    sev_vec = joblib.load("saved_models/severity_vectorizer.pkl")
    sev_le = joblib.load("saved_models/severity_label_encoder.pkl")

    X_s = sev_vec.transform(df["text"].fillna(""))
    X_tab = df[joblib.load("saved_models/severity_tab_cols.pkl")].values

    lr_prob = sev_lr.predict_proba(X_s)
    xgb_prob = sev_xgb.predict_proba(X_tab)
    probs = (0.55 * xgb_prob + 0.45 * lr_prob)

    y_pred = sev_le.inverse_transform(probs.argmax(axis=1))
    y_true_raw = df["severity_raw"]
    y_true_final = df["severity"]

    report = classification_report(y_true_final, y_pred, output_dict=True)
    ord_penalty = ordering_penalty(y_true_final.values, y_pred)

    os.makedirs("reports/severity", exist_ok=True)
    with open("reports/severity/validation.json", "w") as f:
        json.dump({
            "macro_f1": f1_score(y_true_final, y_pred, average="macro"),
            "accuracy": (y_true_final == y_pred).mean(),
            "ordering_penalty": float(ord_penalty),
            "confusion": confusion_matrix(y_true_final, y_pred, labels=ORDER).tolist(),
        }, f, indent=2)

    print("\n=== SEVERITY VALIDATION ===")
    print(classification_report(y_true_final, y_pred))
    print("Ordering penalty:", ord_penalty)


if __name__ == "__main__":
    run_severity_validation()
