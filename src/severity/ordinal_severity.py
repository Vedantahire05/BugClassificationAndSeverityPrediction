# src/severity/ordinal_severity.py

from src.severity.severity_rules import rule_severity_boost

SEVERITY_LABELS = ["Low", "Medium", "High", "Critical"]


def clamp(val, low=0, high=3):
    return max(low, min(high, val))


def score_to_label(score: int) -> str:
    return SEVERITY_LABELS[clamp(score)]


def compute_severity_score(
    ml_score: float,
    text: str,
    types: list[str]
) -> tuple[str, int, list[str]]:
    """
    Balanced severity decision:

    - ML gives base severity
    - Rules can increase severity only by +1
    - Prevents everything becoming Critical
    """

    explanations = []

    # ---- ML base ----
    base = clamp(round(ml_score))

    # ---- rule boost ----
    boost = rule_severity_boost(text, types)

    if boost > 0:
        explanations.append("rule adjustment")

    # ---- LIMIT RULE IMPACT ----
    if boost > 0:
        final_score = base + 1
    else:
        final_score = base

    final_score = clamp(final_score)

    return (
        score_to_label(final_score),
        final_score,
        explanations
    )