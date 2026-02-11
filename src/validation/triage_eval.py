import pandas as pd

# Severity ordering
sev_map = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}

def triage_eval(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes triage evaluation cost:
    - Underestimating severity is penalized ×3
    - Overestimation ×1
    - Correct prediction = 0 cost
    """

    # ---- SAFETY CHECKS ----
    required_cols = ["severity", "model_severity"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # ---- ENCODE TRUE + PREDICTED ----
    df["true_int"] = df["severity"].map(sev_map)
    df["pred_int"] = df["model_severity"].map(sev_map)

    # Remove rows we cannot map
    df = df.dropna(subset=["true_int", "pred_int"])

    # ---- DELTA (direction of error) ----
    df["delta"] = df["true_int"] - df["pred_int"]

    # ---- COST FUNCTION ----
    def cost(row):
        d = row.delta
        if d == 0:
            return 0
        if d > 0:  # model underestimates
            return 3 * abs(d)
        else:      # model overestimates
            return 1 * abs(d)

    df["cost"] = df.apply(cost, axis=1)

    # ---- SUMMARY ----
    correct = (df.delta == 0).mean()
    under = (df.delta > 0).mean()
    over = (df.delta < 0).mean()
    total_cost = df.cost.sum()

    print("\n=== TRIAGE EVALUATION ===")
    print(f"Correct:      {correct*100:.1f}%")
    print(f"Under-shot:   {under*100:.1f}%")
    print(f"Over-shot:    {over*100:.1f}%")
    print(f"Triage Cost:  {total_cost}")

    return df
