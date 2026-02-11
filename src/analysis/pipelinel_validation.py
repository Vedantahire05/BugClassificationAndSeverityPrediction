import pandas as pd
import json
from tqdm import tqdm
from src.models.predict_pipeline import predict

def run_pipeline_validation(n=600):
    df = pd.read_csv("dataset/cleaned/github_severity_synth.csv")
    df = df.sample(n=min(n, len(df)), random_state=42)

    failures = []
    for _, row in tqdm(df.iterrows(), total=len(df)):
        text = row["summary"]
        truth_t = row["type"]
        truth_s = row["severity"]

        pred = predict(text)
        if truth_s != pred["severity"]:
            failures.append({
                "text": text,
                "truth_type": truth_t,
                "truth_severity": truth_s,
                "pred_type": pred["type"],
                "pred_severity": pred["severity"]
            })

    report = {
        "total": len(df),
        "failures": len(failures),
        "failure_rate": len(failures)/len(df),
        "samples": failures[:30]
    }

    import os
    os.makedirs("reports/pipeline", exist_ok=True)
    with open("reports/pipeline/validation.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n=== PIPELINE VALIDATION ===")
    print(f"Failures: {report['failures']} / {report['total']}")
    print(f"Failure Rate: {report['failure_rate']:.3f}")


if __name__ == "__main__":
    run_pipeline_validation()
