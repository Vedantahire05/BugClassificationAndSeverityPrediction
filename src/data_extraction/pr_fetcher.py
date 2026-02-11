import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

# PR “fix intent” keyword filter (choice C)
FIX_KEYWORDS = [
    "fix", "resolve", "close", "repair", "correct",
    "address", "improve", "optimize", "prevent",
    "handle", "patch", "adjust", "refactor"
]


def contains_fix_intent(title: str) -> bool:
    title_l = title.lower()
    return any(k in title_l for k in FIX_KEYWORDS)


def get_fix_pr_titles(repo: str, issue_number: int):
    """
    Fetch PRs linked to an issue and return filtered fix-intent titles.
    """
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/events"
    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        return []

    pr_titles = []
    events = r.json()

    for ev in events:
        if ev.get("event") == "closed" and "commit_id" in ev:
            # commits often close issues - high signal
            commit_url = f"https://api.github.com/repos/{repo}/commits/{ev['commit_id']}"
            cr = requests.get(commit_url, headers=HEADERS)
            if cr.status_code == 200:
                msg = cr.json().get("commit", {}).get("message", "")
                first_line = msg.split("\n")[0]
                if contains_fix_intent(first_line):
                    pr_titles.append(first_line)

        # Also check PR links directly
        pr = ev.get("commit_id") or ev.get("commit_url") or ev.get("pr_url")
        if pr:
            # skip heavy fetch logic for MVP, optional
            pass

    return list(set(pr_titles))
