# import pandas as pd
# import joblib
# import ast
# import numpy as np
# import os

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import LabelEncoder
# from sklearn.metrics import classification_report, f1_score, accuracy_score
# from sklearn.model_selection import train_test_split
# from xgboost import XGBClassifier


# def safe_parse_list(val):
#     if isinstance(val, list):
#         return val
#     if isinstance(val, str):
#         try:
#             return ast.literal_eval(val)
#         except:
#             return [val]
#     return []


# def compute_days_open(created, closed):
#     import datetime
#     if not created:
#         return 1
#     try:
#         c0 = datetime.datetime.fromisoformat(created.replace("Z", ""))
#         if closed:
#             c1 = datetime.datetime.fromisoformat(closed.replace("Z", ""))
#         else:
#             c1 = datetime.datetime.now()
#         return max(1, (c1 - c0).days)
#     except:
#         return 1


# def train_severity_model():

#     src = "dataset/cleaned/github_severity_synth.csv"
#     if not os.path.exists(src):
#         raise FileNotFoundError(f"Missing file: {src}")

#     df = pd.read_csv(src)

#     # -------------------------
#     # TYPE PARSING
#     # -------------------------
#     df["type"] = df["type"].apply(safe_parse_list)

#     type_set = sorted({t for L in df["type"] for t in L})
#     for t in type_set:
#         df[f"T::{t}"] = df["type"].apply(lambda L: 1 if t in L else 0)

#     # -------------------------
#     # TABULAR FEATURES
#     # -------------------------
#     df["days_open"] = df.apply(
#         lambda r: compute_days_open(r["created_at"], r["closed_at"]), axis=1
#     )
#     df["confidence"] = df["confidence"].fillna(0).clip(0, 1)

#     # severity_raw → categorical encoding
#     raw_label_encoder = LabelEncoder()
#     df["severity_raw_enc"] = raw_label_encoder.fit_transform(df["severity_raw"])

#     tab_cols = (
#         ["severity_raw_enc", "confidence", "days_open"] +
#         [f"T::{t}" for t in type_set]
#     )

#     X_tab = df[tab_cols].values

#     # -------------------------
#     # TEXT FEATURES (TF-IDF)
#     # -------------------------
#     df["text"] = df["text"].fillna("")

#     vectorizer = TfidfVectorizer(
#         ngram_range=(1, 2),
#         min_df=3,
#         max_df=0.9,
#         stop_words="english",
#         sublinear_tf=True
#     )

#     X_text = vectorizer.fit_transform(df["text"])

#     # -------------------------
#     # TARGET ENCODING
#     # -------------------------
#     y = df["severity"]
#     severity_encoder = LabelEncoder()
#     y_enc = severity_encoder.fit_transform(y)

#     # -------------------------
#     # TRAIN/VAL SPLIT
#     # -------------------------
#     X_text_train, X_text_val, X_tab_train, X_tab_val, y_train, y_val = train_test_split(
#         X_text, X_tab, y_enc,
#         test_size=0.1,
#         random_state=42,
#         shuffle=True,
#         stratify=y_enc
#     )

#     # -------------------------
#     # MODEL A: LOGISTIC REGRESSION
#     # -------------------------
#     clf_lr = LogisticRegression(
#         max_iter=800,
#         n_jobs=-1,
#         class_weight="balanced"
#     )
#     clf_lr.fit(X_text_train, y_train)

#     # -------------------------
#     # MODEL B: XGB on tabular
#     # -------------------------
#     clf_xgb = XGBClassifier(
#         n_estimators=250,
#         max_depth=6,
#         learning_rate=0.08,
#         subsample=0.85,
#         colsample_bytree=0.85,
#         eval_metric="mlogloss"
#     )
#     clf_xgb.fit(X_tab_train, y_train)

#     # -------------------------
#     # PROB BLENDING
#     # -------------------------
#     lr_probs = clf_lr.predict_proba(X_text_val)
#     xgb_probs = clf_xgb.predict_proba(X_tab_val)

#     final_probs = (0.45 * lr_probs) + (0.55 * xgb_probs)
#     preds = final_probs.argmax(axis=1)

#     # -------------------------
#     # EVALUATION
#     # -------------------------
#     acc = accuracy_score(y_val, preds)
#     macro = f1_score(y_val, preds, average="macro")

#     print("\n=== HYBRID SEVERITY MODEL ===")
#     print(f"Accuracy:  {acc:.4f}")
#     print(f"Macro-F1:  {macro:.4f}\n")
#     print(classification_report(y_val, preds, target_names=severity_encoder.classes_))

#     # -------------------------
#     # SAVE ARTIFACTS FOR INFERENCE
#     # -------------------------
#     joblib.dump(clf_lr, "saved_models/severity_lr.pkl")
#     joblib.dump(clf_xgb, "saved_models/severity_xgb.pkl")
#     joblib.dump(vectorizer, "saved_models/severity_vectorizer.pkl")
#     joblib.dump(severity_encoder, "saved_models/severity_label_encoder.pkl")
#     joblib.dump(raw_label_encoder, "saved_models/severity_raw_encoder.pkl")
#     joblib.dump(tab_cols, "saved_models/severity_tab_cols.pkl")
#     joblib.dump(type_set, "saved_models/severity_type_set.pkl")

#     print("\n[SEVERITY MODEL SAVED]")
#     print("Artifacts stored in saved_models/\n")


# if __name__ == "__main__":
#     train_severity_model()

# src/models/severity_model.py

import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.preprocessing import LabelEncoder

def train_severity_model():
    df = pd.read_csv("dataset/cleaned/github_severity_synth.csv")

    sev_map = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}
    df["severity_int"] = df["severity"].map(sev_map)

    X_text = df["text"].fillna("")

    vec = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=3,
        max_df=0.9,
        stop_words="english",
        sublinear_tf=True,
    )
    X = vec.fit_transform(X_text)

    model = Ridge(alpha=1.5)
    model.fit(X, df["severity_int"])

    joblib.dump(model, "saved_models/severity_ordinal.pkl")
    joblib.dump(vec, "saved_models/severity_vectorizer.pkl")

    print("[SEVERITY] Ordinal model trained and saved.")

if __name__ == "__main__":
    train_severity_model()
