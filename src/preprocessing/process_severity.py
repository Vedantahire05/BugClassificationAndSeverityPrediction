import pandas as pd
from src.preprocessing.cleaner import clean_text

def process_severity(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # TEXT CLEANING (null-safe)
    df["summary"] = df["summary"].fillna("").apply(clean_text)
    df["description"] = df["description"].fillna("").apply(clean_text)

    # DROP EMPTY TEXT ROWS
    df = df[(df["summary"] != "") | (df["description"] != "")]

    # DROP type_hint (MVP choice)
    if "type_hint" in df.columns:
        df = df.drop(columns=["type_hint"])

    # ENSURE REQUIRED COLUMNS EXIST
    required = [
        "bug_id",
        "summary",
        "description",
        "severity_raw",
        "severity",
        "source",
        "created_at",
        "closed_at",
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in severity dataset: {missing}")

    # UNIFIED SCHEMA ORDERING
    df = df[required]

    return df
