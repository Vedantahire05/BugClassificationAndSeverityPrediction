import pandas as pd
import joblib
import ast
from sklearn.metrics import f1_score, hamming_loss
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from collections import Counter
import numpy as np
import json
import os


def safe_parse(val):
    if isinstance(val, list): return val
    if isinstance(val, str):
        try: return ast.literal_eval(val)
        except: return [val]
    return []


def run_type_validation():
    df = pd.read_csv("dataset/cleaned/github_cleaned.csv")
    df["type"] = df["type"].apply(safe_parse)

    X = df["text"].fillna("")
    y = df["type"]

    mlb = MultiLabelBinarizer()
    Y = mlb.fit_transform(y)

    X_train, X_val, Y_train, Y_val = train_test_split(
        X, Y, test_size=0.2, random_state=42
    )

    model = joblib.load("saved_models/type_model.pkl")
    vec = joblib.load("saved_models/type_vectorizer.pkl")

    X_val_tfidf = vec.transform(X_val)
    Y_pred = model.predict(X_val_tfidf)

    micro = f1_score(Y_val, Y_pred, average="micro")
    macro = f1_score(Y_val, Y_pred, average="macro")
    h_loss = hamming_loss(Y_val, Y_pred)

    results = {
        "micro_f1": float(micro),
        "macro_f1": float(macro),
        "hamming_loss": float(h_loss),
        "label_support": Counter([l for labels in y for l in labels])
    }

    os.makedirs("reports/type", exist_ok=True)
    with open("reports/type/validation.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n=== TYPE VALIDATION RESULTS ===")
    print(results)


if __name__ == "__main__":
    run_type_validation()
