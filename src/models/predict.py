import joblib
import pandas as pd
import ast

def load_models():
    type_model = joblib.load("saved_models/type_model.pkl")
    type_vectorizer = joblib.load("saved_models/type_vectorizer.pkl")
    type_mlb = joblib.load("saved_models/type_mlb.pkl")

    severity_model = joblib.load("saved_models/severity_model.pkl")
    severity_vectorizer = joblib.load("saved_models/severity_vectorizer.pkl")

    return type_model, type_vectorizer, type_mlb, severity_model, severity_vectorizer


def predict(text: str):
    (
        type_model,
        type_vectorizer,
        type_mlb,
        severity_model,
        severity_vectorizer,
    ) = load_models()

    # preprocess input
    text = text.strip()

    # type prediction
    X_type = type_vectorizer.transform([text])
    type_pred = type_model.predict(X_type)
    type_labels = type_mlb.inverse_transform(type_pred)[0]

    # severity prediction
    X_sev = severity_vectorizer.transform([text])
    severity_label = severity_model.predict(X_sev)[0]

    return {
        "type": list(type_labels),
        "severity": severity_label
    }


if __name__ == "__main__":
    sample = "Button alignment is broken on the dashboard"
    result = predict(sample)
    print(result)
