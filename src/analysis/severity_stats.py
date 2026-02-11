import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


P_MAP = {
    "Critical": "P1",
    "High": "P2",
    "Medium": "P3",
    "Low": "P4"
}


def severity_stats():
    path = "dataset/cleaned/github_severity_synth.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")

    df = pd.read_csv(path)

    # apply dual mapping
    df["priority"] = df["severity"].map(P_MAP)

    print("\n=== SEVERITY DISTRIBUTION ===")
    print(df["severity"].value_counts(), "\n")

    print("=== PRIORITY DISTRIBUTION (P-level) ===")
    print(df["priority"].value_counts(), "\n")

    # severity histogram
    plt.figure(figsize=(6,4))
    df["severity"].value_counts().plot(kind="bar", color="steelblue")
    plt.title("Severity Frequency")
    plt.xlabel("Severity")
    plt.ylabel("Count")
    plt.show()

    # P-level histogram
    plt.figure(figsize=(6,4))
    df["priority"].value_counts().sort_index().plot(kind="bar", color="darkblue")
    plt.title("Priority Frequency")
    plt.xlabel("Priority (P1=Critical → P4=Low)")
    plt.ylabel("Count")
    plt.show()

    # severity × type heatmap
    explode = df["type"].apply(eval).explode()
    heat = explode.to_frame().join(df["severity"])
    pivot = heat.pivot_table(index="type", columns="severity", aggfunc=len, fill_value=0)

    plt.figure(figsize=(10,6))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="Blues")
    plt.title("Type × Severity Correlation")
    plt.show()

    print("\n=== TYPE × SEVERITY TABLE ===")
    print(pivot, "\n")

    print("[STATS] Done.\n")


if __name__ == "__main__":
    severity_stats()
