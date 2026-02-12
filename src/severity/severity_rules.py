import re
from datetime import datetime


# -------------------------------------------------------
# 1. TYPE BASE PRIORS
# -------------------------------------------------------
TYPE_PRIORS = {
    "SECURITY": 2.5,
    "BUG": 2.0,
    "NETWORK": 2.2,
    "PERFORMANCE": 2.1,
    "ACCESSIBILITY": 1.9,
    "COMPATIBILITY": 1.8,
    "UI": 1.6,
    "FEATURE": 1.4,
    "TESTING": 1.3,
    "DOCUMENTATION": 1.1,
    "CLEANUP": 1.0,
}


# -------------------------------------------------------
# 2. KEYWORD BOOST RULES
# -------------------------------------------------------
KEYWORD_RULES = {
    r"(crash|panic|segfault|core dump|fatal)": 2.0,
    r"(data loss|corruption|inconsistent data)": 2.5,
    r"(security|vulnerability|exploit|cve)": 2.0,
    r"(deadlock|race condition|hang)": 1.8,
    r"(network partition|connection lost|unreachable)": 1.6,
    r"(timeout|latency|slow)": 1.2,
    r"(memory leak|oom)": 1.8,
}


# -------------------------------------------------------
# 3. TIME FACTOR
# -------------------------------------------------------
def days_open(created, closed=None):
    try:
        c0 = datetime.fromisoformat(created.replace("Z", ""))
        if closed:
            c1 = datetime.fromisoformat(closed.replace("Z", ""))
        else:
            c1 = datetime.now()

        return max(1, (c1 - c0).days)
    except:
        return 1


# -------------------------------------------------------
# 4. RULE BOOST FUNCTION
# -------------------------------------------------------
def rule_severity_boost(text: str, types):
    boost = 0.0
    text = text.lower()

    for pattern, score in KEYWORD_RULES.items():
        if re.search(pattern, text):
            boost += score

    for t in types:
        boost += TYPE_PRIORS.get(t, 1.0)

    return boost


# -------------------------------------------------------
# 5. RAW SEVERITY SCORE
# -------------------------------------------------------
def compute_raw_severity(types, text, created, closed):
    base = rule_severity_boost(text, types)

    d = days_open(created, closed)

    # older issues → larger impact
    if d > 180:
        base += 1.0
    elif d > 60:
        base += 0.6

    # normalize by type count
    base = base / max(1, len(types))

    return base


# -------------------------------------------------------
# 6. MAP RAW SCORE → LEVEL
# -------------------------------------------------------
def map_severity_level(raw):
    if raw >= 3.4:
        return "Critical"
    elif raw >= 2.6:
        return "High"
    elif raw >= 1.8:
        return "Medium"
    else:
        return "Low"


# -------------------------------------------------------
# 7. CONFIDENCE
# -------------------------------------------------------
def compute_confidence(raw):
    return round(min(1.0, 0.25 + raw / 4.5), 3)


# -------------------------------------------------------
# 8. EXPLANATION
# -------------------------------------------------------
def explain(types, text, raw):
    reasons = []

    text_l = text.lower()

    if "SECURITY" in types:
        reasons.append("security impact")

    if "NETWORK" in types:
        reasons.append("network impact")

    if "PERFORMANCE" in types:
        reasons.append("performance degradation")

    if "UI" in types:
        reasons.append("user-visible issue")

    for pattern in KEYWORD_RULES:
        if re.search(pattern, text_l):
            reasons.append("critical keyword detected")
            break

    if not reasons:
        if raw > 3:
            reasons.append("system-wide impact")
        elif raw > 2:
            reasons.append("functional impact")
        else:
            reasons.append("localized issue")

    return ", ".join(reasons)