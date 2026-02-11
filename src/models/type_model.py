import pandas as pd
import ast
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score, hamming_loss


def safe_parse_list(value):
    if isinstance(value, list):
        return value
    if value is None:
        return []
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return []
        try:
            parsed = ast.literal_eval(s)
            if isinstance(parsed, list):
                return parsed
            return [parsed]
        except:
            return [s]
    return []


def train_type_model():
    df = pd.read_csv("dataset/cleaned/github_cleaned.csv")

    # ---- PARSE LABELS ----
    df["type"] = df["type"].apply(safe_parse_list)

    # ---- CLEAN TEXT FIELDS ----
    df["summary"] = df["summary"].fillna("")
    df["description"] = df["description"].fillna("")

    # ---- PARSE PR TITLES ----
    df["fix_pr_titles"] = df["fix_pr_titles"].apply(safe_parse_list)

    # ---- BUILD PR TEXT ----
    df["fix_pr"] = df["fix_pr_titles"].apply(
        lambda x: " ".join(str(t) for t in x)
    )

    # ---- MERGE TEXT WITH PR BOOST ----
    def merge_text(row):
        summary = row["summary"]
        desc = row["description"]
        pr = row["fix_pr"]
        if pr:
            pr = f"{pr} {pr}"   # double token for boosting
        return f"{summary} {desc} {pr}".strip()

    df["text"] = df.apply(merge_text, axis=1)

    # ---- DROP EMPTY TEXT ROWS ----
    df = df[df["text"] != ""]

    X = df["text"]
    y = df["type"]

    # ---- BINARY MULTI-LABEL ----
    mlb = MultiLabelBinarizer()
    Y = mlb.fit_transform(y)

    # ---- TRAIN/VAL SPLIT ----
    X_train, X_val, Y_train, Y_val = train_test_split(
        X, Y,
        test_size=0.1,
        random_state=42,
        shuffle=True
    )

    # ---- TF-IDF FEATURES ----
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=3,
        max_df=0.90,
        stop_words="english",
        sublinear_tf=True
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_val_tfidf = vectorizer.transform(X_val)

    # ---- MODEL ----
    model = OneVsRestClassifier(
        LogisticRegression(
            max_iter=800,
            class_weight="balanced",
            n_jobs=-1,
        )
    )

    model.fit(X_train_tfidf, Y_train)

    # ---- METRICS ----
    Y_pred = model.predict(X_val_tfidf)
    micro_f1 = f1_score(Y_val, Y_pred, average="micro")
    macro_f1 = f1_score(Y_val, Y_pred, average="macro")
    h_loss = hamming_loss(Y_val, Y_pred)

    print("\n========== TYPE MODEL RESULTS ==========")
    print(f"Micro-F1   : {micro_f1:.4f}")
    print(f"Macro-F1   : {macro_f1:.4f}")
    print(f"HammingLoss: {h_loss:.4f}")

    print("\nLabel Support:")
    print(df["type"].explode().value_counts())

    print("\n========================================\n")

    # ---- SAVE ARTIFACTS ----
    joblib.dump(model, "saved_models/type_model.pkl")
    joblib.dump(vectorizer, "saved_models/type_vectorizer.pkl")
    joblib.dump(mlb, "saved_models/type_mlb.pkl")

    print("Type Model Saved! Artifacts stored in saved_models/\n")


if __name__ == "__main__":
    train_type_model()
