# # src/validation/validate.py

# import pandas as pd
# from sklearn.metrics import classification_report, f1_score
# from src.validation.triage_eval import triage_eval
# from src.models.predict_pipeline import predict
# import numpy as np


# def run_validation():
#     df = pd.read_csv("dataset/cleaned/github_severity_synth.csv")

#     # temporal split (sorted by created_at)
#     df = df.sort_values("created_at")
#     split = int(len(df) * 0.8)

#     df_train = df.iloc[:split]
#     df_valid = df.iloc[split:]

#     print(f"[TEMPORAL SPLIT]")
#     print(f"Train: {len(df_train)} rows | Valid: {len(df_valid)} rows\n")

#     # ----- FULL PIPELINE INFERENCE -----
#     preds = []
#     for text in df_valid["text"]:
#         out = predict(text)
#         preds.append(out["severity"])

#     df_valid["model_severity"] = preds

#     # ----- EVALUATE -----
#     y_true = df_valid["severity"]
#     y_pred = df_valid["model_severity"]

#     print("\n=== SEVERITY VALIDATION (Production Mode) ===")
#     print(classification_report(y_true, y_pred))
#     print("Macro-F1:", f1_score(y_true, y_pred, average="macro"))

#     # ----- TRIAGE COST METRICS -----
#     triage_eval(df_valid)

#     return df_valid


# if __name__ == "__main__":
#     run_validation()

# src/validation/validate.py

import pandas as pd
from tqdm import tqdm
from sklearn.metrics import classification_report, f1_score
from src.models.predict_pipeline import predict
from src.validation.triage_eval import triage_eval

def run_validation():
    df = pd.read_csv("dataset/cleaned/github_severity_synth.csv")
    df = df.sort_values("created_at")

    split = int(len(df) * 0.8)
    valid = df.iloc[split:].copy()

    preds = []
    for text in tqdm(valid["text"], desc="[VALIDATING]", ncols=100):
        preds.append(predict(text)["severity"])

    valid["model_severity"] = preds

    print("\n=== SEVERITY VALIDATION (ORDINAL + RULES) ===")
    print(classification_report(valid["severity"], valid["model_severity"]))
    print("Macro-F1:", f1_score(valid["severity"], valid["model_severity"], average="macro"))

    triage_eval(valid)

if __name__ == "__main__":
    run_validation()

