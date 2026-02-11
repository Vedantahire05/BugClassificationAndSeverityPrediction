import pandas as pd
import ast
from src.preprocessing.cleaner import clean_text
from src.preprocessing.label_mapper import normalize_labels


def parse_list(value):
    """
    Converts:
        - python list
        - "['a','b']" string list
        - empty string
        - single string
    into python list
    """
    if isinstance(value, list):
        return value
    if value is None:
        return []
    if isinstance(value, str):
        s = value.strip()
        if s == "":
            return []
        try:
            parsed = ast.literal_eval(s)
            if isinstance(parsed, list):
                return parsed
        except:
            return [s]
    return []


def ensure_github_columns(df):
    """
    Guarantee that all expected columns exist even if missing
    Useful for incremental dataset merges where fields may be absent.
    """
    expected = [
        "repo", "number", "title", "body", "labels",
        "created_at", "closed_at", "fix_pr_titles"
    ]
    for col in expected:
        if col not in df.columns:
            df[col] = None
    return df


def process_github(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = ensure_github_columns(df)

    # ------------------------------
    # CLEAN LABELS & PR TITLES
    # ------------------------------
    df["labels"] = df["labels"].apply(parse_list)
    df["fix_pr_titles"] = df["fix_pr_titles"].apply(parse_list)

    # ------------------------------
    # TEXT CLEANING
    # ------------------------------
    df["summary"] = df["title"].fillna("").apply(clean_text)
    df["description"] = df["body"].fillna("").apply(clean_text)

    # optional PR title text merge
    df["fix_pr"] = df["fix_pr_titles"].apply(
        lambda x: " ".join(clean_text(str(t)) for t in x) if isinstance(x, list) else ""
    )

    # remove rows that are truly empty text
    df = df[(df["summary"] != "") | (df["description"] != "")]

    # ------------------------------
    # MULTI-LABEL TYPE MAPPING
    # ------------------------------
    df["type"] = df["labels"].apply(normalize_labels)
    df = df[df["type"].map(len) > 0]

    # ------------------------------
    # BUG_ID & SOURCE
    # ------------------------------
    df["bug_id"] = df.apply(
        lambda x: f"{x['repo']}#{x['number']}", axis=1
    )
    df["source"] = "github"

    # ------------------------------
    # MERGED TEXT FIELD (for ML)
    # summary + description + PR-fix context
    # ------------------------------
    df["text"] = (
        df["summary"] + " " +
        df["description"] + " " +
        df["fix_pr"]
    ).str.strip()

    # IMPORTANT:
    # do not drop summary/description — some models use them separately

    cleaned = df[[
        "bug_id",
        "summary",
        "description",
        "fix_pr_titles",
        "type",
        "labels",
        "source",
        "created_at",
        "closed_at",
        "text"
    ]]

    return cleaned
