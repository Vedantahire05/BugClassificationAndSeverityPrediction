import pandas as pd
import ast
import os

from src.severity.severity_rules import (
    compute_raw_severity,
    map_severity_level,
    compute_confidence,
    explain
)


def safe_parse_list(x):
    if isinstance(x, list):
        return x
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except:
            return [x]
    return []


def synthesize_severity():
    src_path = "dataset/cleaned/github_cleaned.csv"
    out_path = "dataset/cleaned/github_severity_synth.csv"

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Missing file: {src_path}")

    df = pd.read_csv(src_path)

    # parse types
    df["type"] = df["type"].apply(safe_parse_list)

    # parse PR titles (optional)
    df["fix_pr_titles"] = df.get("fix_pr_titles", "").apply(safe_parse_list)

    # merged text
    df["text"] = (
        df["summary"].fillna("") + " " +
        df["description"].fillna("") + " " +
        df["fix_pr_titles"].apply(lambda x: " ".join(x))
    ).str.strip()

    # compute severity fields
    raw_scores = []
    sev_levels = []
    confs = []
    exps = []

    for _, row in df.iterrows():
        types = row["type"]
        text = row["text"]
        created = row.get("created_at")
        closed = row.get("closed_at")

        raw = compute_raw_severity(types, text, created, closed)
        sev = map_severity_level(raw)
        conf = compute_confidence(raw)
        exp = explain(types, text, raw)

        raw_scores.append(round(raw, 3))
        sev_levels.append(sev)
        confs.append(conf)
        exps.append(exp)

    df["severity_raw"] = raw_scores
    df["severity"] = sev_levels
    df["confidence"] = confs
    df["explanation"] = exps

    # save
    df.to_csv(out_path, index=False)
    print(f"[SEVERITY] Synthesis complete.")
    print(f"[SEVERITY] Output -> {out_path}")
    print(df.head(5))
    print(f"Rows = {len(df)}")


if __name__ == "__main__":
    synthesize_severity()
