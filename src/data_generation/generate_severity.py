import random
import pandas as pd
from datetime import datetime, timedelta

SEVERITY_RAW_CLASSES = [
    "blocker", "critical", "major",
    "normal",
    "minor", "trivial"
]

SEVERITY_MAP = {
    "blocker": "High",
    "critical": "High",
    "major": "High",
    "normal": "Medium",
    "minor": "Low",
    "trivial": "Low"
}

# Weighted realistic distribution
SEVERITY_WEIGHTS = {
    "blocker": 0.08,
    "critical": 0.12,
    "major":   0.08,
    "normal":  0.55,
    "minor":   0.12,
    "trivial": 0.05
}

# Some realistic text patterns
HIGH_TEXT = [
    "application crashes immediately on launch",
    "blocking production deployment",
    "critical security vulnerability allows privilege escalation",
    "major performance degradation under high load",
    "data loss observed when saving file",
    "system freeze during execution",
    "outage impacting multiple users",
    "network failure causing cluster downtime",
    "crash when accessing memory buffer"
]

MEDIUM_TEXT = [
    "unexpected behavior under specific conditions",
    "inconsistent results returned from API call",
    "performance slowdown noticed",
    "incorrect output produced in edge cases",
    "fails to connect intermittently",
    "partial regression observed after update",
    "warning message displayed incorrectly",
    "module fails validation test"
]

LOW_TEXT = [
    "typo in documentation",
    "UI alignment issue in settings dialog",
    "minor layout bug in window rendering",
    "improvement suggestion added by user",
    "documentation missing examples",
    "cosmetic styling inconsistency",
    "minor usability enhancement requested"
]

# Optional type categories (mixed correlation)
TYPE_HINTS = {
    "BUG": ["blocker", "critical", "major", "normal", "minor"],
    "FEATURE": ["normal", "minor", "major"],
    "TESTING": ["major", "normal"],
    "DOCUMENTATION": ["trivial", "minor", "normal"],
    "UI": ["minor", "normal", "major"],
    "NETWORK": ["major", "critical", "normal"],
    "PERFORMANCE": ["major", "critical", "normal"],
    "SECURITY": ["blocker", "critical"],
    "CLEANUP": ["trivial", "minor", "normal"]
}

def generate_synthetic_severity(n=6500):
    rows = []

    for i in range(n):
        # optional type for correlation (probabilistic)
        type_label = random.choice(list(TYPE_HINTS.keys()))

        # pick severity class with correlation bias
        candidates = TYPE_HINTS[type_label]
        severity_raw = random.choices(
            SEVERITY_RAW_CLASSES,
            weights=[SEVERITY_WEIGHTS[s] if s in candidates else 0.01 for s in SEVERITY_RAW_CLASSES]
        )[0]

        severity = SEVERITY_MAP[severity_raw]

        # choose summary + description
        if severity == "High":
            text = random.choice(HIGH_TEXT)
        elif severity == "Medium":
            text = random.choice(MEDIUM_TEXT)
        else:
            text = random.choice(LOW_TEXT)

        # generate bug id
        bug_id = f"synthetic#{i+1}"

        # timestamps
        created_at = datetime.now() - timedelta(days=random.randint(0, 1200))
        closed_at = created_at + timedelta(days=random.randint(0, 90))

        rows.append({
            "bug_id": bug_id,
            "summary": text,
            "description": text,
            "type_hint": type_label,
            "severity_raw": severity_raw,
            "severity": severity,
            "source": "synthetic_severity",
            "created_at": created_at.isoformat(),
            "closed_at": closed_at.isoformat()
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_synthetic_severity()
    df.to_csv("dataset/raw/severity_synthetic.csv", index=False)
    print("Synthetic severity dataset generated!")
