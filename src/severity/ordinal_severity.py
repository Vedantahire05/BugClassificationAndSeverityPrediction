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
    final_score = ML + 0.6 * rule_boost
    """
    explanations = []

    base = round(ml_score)
    boost = rule_severity_boost(text, types)

    if boost > 0:
        explanations.append("rule escalation")

    final_score = clamp(round(base + 0.6 * boost))

    return (
        score_to_label(final_score),
        final_score,
        explanations
    )
