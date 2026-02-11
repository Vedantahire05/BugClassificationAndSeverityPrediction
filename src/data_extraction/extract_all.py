import pandas as pd
from tqdm import tqdm
import os
import ast

from src.data_extraction.repo_list import (
    REPOSITORIES_ORDERED,
    PR_REPOS
)
from src.data_extraction.github_extractor import fetch_issues
from src.data_extraction.pr_fetcher import get_fix_pr_titles


# -----------------------------
# Normalization utilities
# -----------------------------

def to_list(val):
    """
    Converts:
    - NaN
    - string list, e.g. "['bug', 'ui']"
    - single string
    - list
    into python list
    """
    if val is None:
        return []
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        s = val.strip()
        if s == "":
            return []
        try:
            if s.startswith("[") and s.endswith("]"):
                parsed = ast.literal_eval(s)
                if isinstance(parsed, list):
                    return parsed
        except:
            return [s]
        return [s]
    return []


# -----------------------------
# Merge logic
# -----------------------------

def merge_records(old, new):
    merged = old.copy()

    # TEXT FIELDS (prefer newer if non-empty)
    if new.get("title"):
        merged["title"] = new.get("title")
    if new.get("body"):
        merged["body"] = new.get("body")

    # LABEL MERGE
    old_labels = to_list(old.get("labels"))
    new_labels = to_list(new.get("labels"))
    merged["labels"] = list(set(old_labels + new_labels))

    # PR TITLES MERGE
    old_pr = to_list(old.get("fix_pr_titles"))
    new_pr = to_list(new.get("fix_pr_titles"))
    merged["fix_pr_titles"] = list(set(old_pr + new_pr))

    # STATE — prefer newer
    merged["state"] = new.get("state", old.get("state"))

    # CREATED — earliest
    merged["created_at"] = min(
        old.get("created_at"),
        new.get("created_at")
    )

    # CLOSED — latest
    old_c = old.get("closed_at")
    new_c = new.get("closed_at")
    merged["closed_at"] = new_c or old_c

    return merged


# -----------------------------
# Extraction Logic
# -----------------------------

def run_extraction(max_pages=10):
    collected = []

    for repo in REPOSITORIES_ORDERED:
        print(f"\n[EXTRACT] Fetching issues from: {repo}")
        issues = fetch_issues(repo, max_pages=max_pages)

        needs_pr = any(x in repo.lower() for x in PR_REPOS)
        iterable = tqdm(issues, desc=f"[PR] {repo}", ncols=100) if needs_pr else issues

        for it in iterable:
            num = it.get("number")
            fix_titles = []

            if num and needs_pr:
                try:
                    fix_titles = get_fix_pr_titles(repo, num) or []
                except Exception as e:
                    print(f"[WARN] PR fetch failed for {repo} #{num}: {e}")

            # Normalize label extraction
            raw_labels = it.get("labels", [])
            labels = []

            if raw_labels:
                first = raw_labels[0]
                if isinstance(first, str):
                    labels = raw_labels
                elif isinstance(first, dict):
                    labels = [l.get("name") for l in raw_labels if "name" in l]

            collected.append({
                "repo": repo,
                "number": num,
                "title": it.get("title", ""),
                "body": it.get("body", ""),
                "labels": labels,
                "state": it.get("state"),
                "created_at": it.get("created_at"),
                "closed_at": it.get("closed_at"),
                "fix_pr_titles": fix_titles,
            })

    df_new = pd.DataFrame(collected)
    save_path = "dataset/raw/github_issues_raw.csv"

    # -----------------------------
    # Merge with previous dataset
    # -----------------------------
    if os.path.exists(save_path):
        print("[MERGE] Loading existing dataset...")
        df_old = pd.read_csv(save_path)

        df_old["key"] = df_old["repo"] + "#" + df_old["number"].astype(str)
        df_new["key"] = df_new["repo"] + "#" + df_new["number"].astype(str)

        merged_dict = {k: row.to_dict() for k, row in df_old.set_index("key").iterrows()}

        for _, row in df_new.iterrows():
            key = row["key"]
            if key in merged_dict:
                merged_dict[key] = merge_records(merged_dict[key], row.to_dict())
            else:
                merged_dict[key] = row.to_dict()

        df_final = pd.DataFrame(merged_dict.values()).drop(columns=["key"])

    else:
        print("[INIT] Creating new dataset...")
        df_final = df_new

    df_final.to_csv(save_path, index=False)

    print(f"[SAVED] Dataset size: {len(df_final)}")
    print("[DONE] Incremental Extraction + Merge Complete!")


if __name__ == "__main__":
    run_extraction(max_pages=10)
