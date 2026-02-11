import joblib
import ast
import numpy as np

from src.severity.severity_rules import (
    compute_raw_severity,
    map_severity_level,
    compute_confidence,
    explain
)


P_MAP = {
    "Critical": "P1",
    "High": "P2",
    "Medium": "P3",
    "Low": "P4"
}


def load_type_models():
    clf = joblib.load("saved_models/type_model.pkl")
    vec = joblib.load("saved_models/type_vectorizer.pkl")
    mlb = joblib.load("saved_models/type_mlb.pkl")
    return clf, vec, mlb


def load_severity_models():
    clf_lr = joblib.load("saved_models/severity_lr.pkl")
    clf_xgb = joblib.load("saved_models/severity_xgb.pkl")
    vec = joblib.load("saved_models/severity_vectorizer.pkl")
    le = joblib.load("saved_models/severity_label_encoder.pkl")
    tab_cols = joblib.load("saved_models/severity_tab_cols.pkl")
    return clf_lr, clf_xgb, vec, le, tab_cols


def predict(text):
    # ---- TYPE PRED ----
    clf_t, vec_t, mlb = load_type_models()

    X = vec_t.transform([text])
    y = clf_t.predict(X)
    types = mlb.inverse_transform(y)[0] if len(y) else []

    # ---- RULE RAW SEVERITY ----
    raw = compute_raw_severity(types, text, None, None)
    sev_rule = map_severity_level(raw)
    conf_rule = compute_confidence(raw)
    exp_rule = explain(types, text, raw)

    # ---- HYBRID ML SEVERITY ----
    clf_lr, clf_xgb, vec_s, le, tab_cols = load_severity_models()

    X_text = vec_s.transform([text])

    tab = np.zeros((1, len(tab_cols)))
    for i, c in enumerate(tab_cols):
        if c.startswith("T::"):
            t = c.split("::")[1]
            tab[0,i] = 1 if t in types else 0
        elif c == "severity_raw":
            tab[0,i] = raw
        elif c == "confidence":
            tab[0,i] = conf_rule
        else:
            tab[0,i] = 12  # days_open default

    lr_probs = clf_lr.predict_proba(X_text)
    xgb_probs = clf_xgb.predict_proba(tab)
    final = (0.55 * xgb_probs) + (0.45 * lr_probs)

    sev_ml = le.inverse_transform(final.argmax(axis=1))[0]
    conf_ml = final.max()

    # ---- Fusion ----
    sev_final = sev_ml if conf_ml > conf_rule else sev_rule
    p_level = P_MAP[sev_final]

    return {
        "type": list(types),
        "severity": sev_final,
        "priority": p_level,
        "confidence": round(float(max(conf_ml, conf_rule)), 3),
        "explanation": exp_rule
    }


if __name__ == "__main__":
    print(predict("network latency regression after update"))
