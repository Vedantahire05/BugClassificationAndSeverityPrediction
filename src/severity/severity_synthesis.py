# src/severity/severity_synthesis.py

import pandas as pd
import ast

# Base mapping
TYPE_TO_SEVERITY = {
    "CRASH": "High",
    "SECURITY": "Critical",
    "NETWORK": "High",
    "STORAGE": "High",
    "PERFORMANCE": "Medium",
    "UI": "Low",
    "FEATURE": "Low",
    "DOCUMENTATION": "Low",
    "BUG": "Medium"
}

KEYWORDS = {
    "data loss": "Critical",
    "crash": "High",
    "hang": "High",
    "freeze": "High",
    "timeout": "Medium",
    "slow": "Medium",
    "security": "Critical",
    "memory leak": "High",
    "panic": "High",
    "corruption": "Critical",
    "inconsistent": "High"
}


def apply_severity(row):
    types = row["type"]
    text = row["text"].lower()

    scores = []

    # type → severity
    for t in types:
        if t in TYPE_TO_SEVERITY:
            scores.append(TYPE_TO_SEVERITY[t])

    # keyword adjustments
    for k, sev in KEYWORDS.items():
        if k in text:
            scores.append(sev)

    if not scores:
        return "Medium"   # default baseline

    # Critical > High > Medium > Low
    order = ["Low", "Medium", "High", "Critical"]
    return max(scores, key=lambda x: order.index(x))


def run():
    df = pd.read_csv("dataset/cleaned/github_cleaned.csv")

    # parse lists
    df["type"] = df["type"].apply(ast.literal_eval)

    df["text"] = (
        df["summary"].fillna("") + " " +
        df["description"].fillna("") + " " +
        df["fix_pr_titles"].apply(lambda x: " ".join(ast.literal_eval(x)) if isinstance(x,str) else "")
    ).str.lower()

    df["severity"] = df.apply(apply_severity, axis=1)

    df.to_csv("dataset/cleaned/github_with_severity.csv", index=False)
    print("[OK] Severity dataset generated.")

if __name__ == "__main__":
    run()
