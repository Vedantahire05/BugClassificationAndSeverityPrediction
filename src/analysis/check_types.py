# src/analysis/check_types.py

import pandas as pd
import ast
from collections import Counter

def run():
    df = pd.read_csv("dataset/cleaned/github_cleaned.csv")

    # Convert string list -> actual list
    df["type"] = df["type"].apply(lambda x: ast.literal_eval(x))

    flat = [t for arr in df["type"] for t in arr]
    cnt = Counter(flat)

    print("\n=== TYPE DISTRIBUTION ===")
    for k, v in cnt.most_common():
        print(f"{k:15} {v}")

    print("\n=== MULTI-LABEL DENSITY ===")
    print(df["type"].apply(len).value_counts())

    print("\nRows:", len(df))

if __name__ == "__main__":
    run()
