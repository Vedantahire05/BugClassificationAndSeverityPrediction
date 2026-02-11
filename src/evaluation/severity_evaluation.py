# src/evaluation/severity_evaluation.py

import pandas as pd

def run():
    df = pd.read_csv("dataset/cleaned/github_with_severity.csv")
    print(df["severity"].value_counts())
    print("\nDistribution good/bad check done.")

if __name__ == "__main__":
    run()
