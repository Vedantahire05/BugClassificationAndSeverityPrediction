import re

CANONICAL_MAP = {
    r"(bug|kind/bug)": "BUG",
    r"(feature|enhancement|feature-request|kind/feature)": "FEATURE",
    r"(performance|perf|slow|lag)": "PERFORMANCE",
    r"(security|vulnerability|kind/security)": "SECURITY",
    r"(ui|ux|workbench|browser-window|graphics|terminal|renderer)": "UI",
    r"(docs|documentation)": "DOCUMENTATION",
    r"(test|testing)": "TESTING",
    r"(cleanup|refactor)": "CLEANUP",
    r"(network|networking)": "NETWORK",
    r"(accessibility|a11y)": "ACCESSIBILITY",
    r"(compatibility|compat|cross-platform)": "COMPATIBILITY",
}

# patterns we consider noise or meta-data
NOISE_LABELS = [
    "needs-triage",
    "needs-sig",
    "triage/",
    "priority/",
    "area/",
    "sig/",
    "status/",
    "lifecycle/",
    "component/",
    "type/",
    "os/",
    "platform/",
    "resolution/",
]


def normalize_labels(raw_labels):
    mapped = set()

    for lbl in raw_labels:
        lbl_lower = lbl.lower()

        matched = False
        for pattern, replacement in CANONICAL_MAP.items():
            if re.search(pattern, lbl_lower):
                mapped.add(replacement)
                matched = True
                break

        if matched:
            continue

        # skip noise/meta labels entirely
        if any(lbl_lower.startswith(n) for n in NOISE_LABELS):
            continue

        # fallback: ignore unknown labels for now (Phase-9.2 will use heuristic)
        # print(f"[WARN] unmapped label: {lbl_lower}")  # optional diagnostics

    return list(mapped)
