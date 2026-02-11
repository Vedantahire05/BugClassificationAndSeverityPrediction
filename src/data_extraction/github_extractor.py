import os
import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
TOKEN = os.getenv("TOKEN")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def fetch_issues(repo, max_pages=100):
    issues = []
    for page in tqdm(range(1, max_pages + 1), desc=f"Fetching from {repo}"):
        url = f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={page}"
        r = requests.get(url, headers=HEADERS)
        data = r.json()

        if not isinstance(data, list):
            break

        if not data:
            break

        for item in data:
            if "pull_request" in item:
                continue

            issues.append({
                "repo": repo,
                "id": item["id"],
                "number": item["number"],
                "title": item.get("title", ""),
                "body": item.get("body", ""),
                "labels": [l["name"] for l in item.get("labels", [])],
                "state": item.get("state", ""),
                "created_at": item.get("created_at", ""),
                "closed_at": item.get("closed_at", "")
            })
    return issues
