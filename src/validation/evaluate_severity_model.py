# src/validation/evaluate_severity_model.py

import pandas as pd
import joblib
from sklearn.metrics import classification_report, f1_score

def evaluate_severity():
    df = pd.read_csv("dataset/cleaned/valid.csv")

    lr = joblib.load("saved_models/severity_lr.pkl")
    xgb = joblib.load("saved_models/severity_xgb.pkl")
    vec = joblib.load("saved_models/severity_vectorizer.pkl")
    le  = joblib.load("saved_models/severity_label_encoder.pkl")
    tab_cols = joblib.load("saved_models/severity_tab_cols.pkl")

    from src.models.predict_pipeline import compute_severity_tab

    X_text = vec.transform(df["text"])
    X_tab = compute_severity_tab(df["type"].apply(eval), tab_cols)

    lr_probs = lr.predict_proba(X_text)
    xgb_probs = xgb.predict_proba(X_tab)

    final_probs = 0.55 * xgb_probs + 0.45 * lr_probs
    preds = final_probs.argmax(axis=1)

    true = le.transform(df["severity"])

    print("\n=== SEVERITY MODEL VALIDATION ===")
    print(classification_report(true, preds, target_names=le.classes_))
    print(f"Macro-F1: {f1_score(true, preds, average='macro'):.4f}\n")

if __name__ == "__main__":
    evaluate_severity()
