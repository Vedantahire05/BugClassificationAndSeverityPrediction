# src/validation/evaluate_type_model.py

import pandas as pd
import joblib
import ast
from sklearn.metrics import f1_score, hamming_loss

def safe_parse(val):
    try:
        return ast.literal_eval(val)
    except:
        return []

def evaluate_type():
    df = pd.read_csv("dataset/cleaned/valid.csv")

    model = joblib.load("saved_models/type_model.pkl")
    vec = joblib.load("saved_models/type_vectorizer.pkl")
    mlb = joblib.load("saved_models/type_mlb.pkl")

    df["text"] = df["text"].fillna("")
    df["type"] = df["type"].apply(safe_parse)

    X = vec.transform(df["text"])
    Y_true = mlb.transform(df["type"])

    Y_pred = model.predict(X)

    print("\n=== TYPE MODEL VALIDATION ===")
    print(f"Micro-F1   : {f1_score(Y_true, Y_pred, average='micro'):.4f}")
    print(f"Macro-F1   : {f1_score(Y_true, Y_pred, average='macro'):.4f}")
    print(f"HammingLoss: {hamming_loss(Y_true, Y_pred):.4f}")
    print()

if __name__ == "__main__":
    evaluate_type()
