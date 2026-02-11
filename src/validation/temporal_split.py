# src/validation/temporal_split.py

import pandas as pd
import os

def temporal_split(path="dataset/cleaned/github_severity_synth.csv", ratio=0.8):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing dataset: {path}")

    df = pd.read_csv(path)

    if "created_at" not in df.columns:
        raise ValueError("Dataset missing created_at column.")

    df = df.sort_values("created_at")

    split = int(len(df) * ratio)
    train = df.iloc[:split].reset_index(drop=True)
    valid = df.iloc[split:].reset_index(drop=True)

    print(f"[TEMPORAL SPLIT]")
    print(f"Train: {len(train)} rows | Valid: {len(valid)} rows")

    train.to_csv("dataset/cleaned/train.csv", index=False)
    valid.to_csv("dataset/cleaned/valid.csv", index=False)

    return train, valid


if __name__ == "__main__":
    temporal_split()
