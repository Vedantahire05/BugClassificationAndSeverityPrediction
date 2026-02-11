# import re
# import math
# import random
# from datetime import datetime


# # -------------------------------------------------------
# # 1. DOMAIN → DEFAULT IMPACT
# # -------------------------------------------------------
# TYPE_BASE_IMPACT = {
#     "BUG": 2.4,
#     "NETWORK": 3.0,
#     "PERFORMANCE": 3.2,
#     "SECURITY": 3.8,
#     "UI": 1.8,
#     "FEATURE": 1.4,
#     "TESTING": 1.6,
#     "DOCUMENTATION": 1.2,
#     "CLEANUP": 1.2,
#     "ACCESSIBILITY": 2.8,
#     "COMPATIBILITY": 2.6,
# }


# # -------------------------------------------------------
# # 2. KEYWORD BOOST TABLES
# # -------------------------------------------------------
# CRITICAL_KEYWORDS = [
#     "crash", "panic", "segfault", "fatal", "data loss",
#     "memory corruption", "corrupt", "kernel", "freeze",
#     "exploit", "overflow", "dos", "hang", "deadlock"
# ]

# SECURITY_KEYWORDS = [
#     "xss", "csrf", "rce", "buffer overflow", "0day",
#     "exploit", "vulnerability", "privilege escalation"
# ]

# PERF_KEYWORDS = [
#     "slow", "latency", "throughput", "performance",
#     "cpu", "memory leak", "network latency"
# ]


# # -------------------------------------------------------
# # 3. TIME BOOSTS
# # -------------------------------------------------------
# def days_open(created, closed=None):
#     try:
#         c0 = datetime.fromisoformat(created.replace("Z", ""))
#         if closed:
#             c1 = datetime.fromisoformat(closed.replace("Z", ""))
#         else:
#             c1 = datetime.now()
#         return max(1, (c1 - c0).days)
#     except:
#         return 1


# # -------------------------------------------------------
# # 4. HYBRID RAW SCORING
# # -------------------------------------------------------
# def compute_raw_severity(types, text, created, closed):
#     base = 0.0

#     # type-based weighting
#     for t in types:
#         base += TYPE_BASE_IMPACT.get(t, 1.4)

#     # keyword boosts
#     low = text.lower()
#     if any(k in low for k in CRITICAL_KEYWORDS):
#         base += 2.2

#     if any(k in low for k in SECURITY_KEYWORDS):
#         base += 1.8

#     if any(k in low for k in PERF_KEYWORDS):
#         base += 1.4

#     # time factor
#     d = days_open(created, closed)
#     if d > 60:
#         base += 0.8
#     elif d > 180:
#         base += 1.4

#     # normalize
#     base = base / max(1, len(types))

#     # hybrid randomness for ambiguous cases
#     # -------------------------------------
#     if 2.0 < base < 3.4:   # grey zone
#         base += random.uniform(-0.2, 0.3)

#     return base


# # -------------------------------------------------------
# # 5. FINAL MAPPING
# # -------------------------------------------------------
# def map_severity_level(raw):
#     if raw >= 3.6:
#         return "Critical"
#     elif raw >= 3.0:
#         return "High"
#     elif raw >= 2.0:
#         return "Medium"
#     else:
#         return "Low"


# # -------------------------------------------------------
# # 6. CONFIDENCE
# # -------------------------------------------------------
# def compute_confidence(raw):
#     return round(min(1.0, 0.22 + (raw / 4.4)), 3)


# # -------------------------------------------------------
# # 7. EXPLANATION
# # -------------------------------------------------------
# def explain(types, text, raw):
#     reasons = []

#     if "SECURITY" in types:
#         reasons.append("security risk")

#     if "NETWORK" in types:
#         reasons.append("affects communication layer")

#     if "PERFORMANCE" in types:
#         reasons.append("performance degradation")

#     if "UI" in types:
#         reasons.append("user-visible issue")

#     if any(k in text.lower() for k in CRITICAL_KEYWORDS):
#         reasons.append("crash-like behavior")

#     if not reasons:
#         if raw > 3.2:
#             reasons.append("system-wide impact")
#         elif raw > 2.2:
#             reasons.append("functional impact")
#         else:
#             reasons.append("localized low-impact")

#     return ", ".join(reasons)


# src/severity/severity_rules.py

import re

# keyword → severity score boost
KEYWORD_RULES = {
    r"(crash|panic|segfault|core dump)": 2,
    r"(data loss|corruption|inconsistent data)": 3,
    r"(security|vulnerability|exploit|cve)": 2,
    r"(deadlock|race condition)": 2,
    r"(network partition|connection lost|unreachable)": 2,
    r"(timeout|latency|slow)": 1,
    r"(memory leak|oom)": 2,
}

# type-based base severity
TYPE_PRIORS = {
    "SECURITY": 2,
    "BUG": 1,
    "NETWORK": 1,
    "PERFORMANCE": 1,
    "UI": 0,
    "DOCUMENTATION": -1,
    "FEATURE": 0,
    "TESTING": 0,
}

def rule_severity_boost(text: str, types: list[str]) -> int:
    boost = 0
    text = text.lower()

    for pattern, score in KEYWORD_RULES.items():
        if re.search(pattern, text):
            boost += score

    for t in types:
        boost += TYPE_PRIORS.get(t, 0)

    return boost
