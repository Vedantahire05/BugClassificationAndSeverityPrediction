import pandas as pd
import ast
from src.preprocessing.cleaner import clean_text
from src.preprocessing.label_mapper import normalize_labels
from src.preprocessing.schema import ensure_github_columns


def preprocess_github():
    df = pd.read_csv("dataset/raw/github_issues_raw.csv")

    # ensure columns exist
    df = ensure_github_columns(df)

    # -------- fix labels format --------
    def parse_labels(x):
        if isinstance(x, list):
            return x
        if isinstance(x, str):
            try:
                return ast.literal_eval(x)
            except:
                return []
        return []

    df["labels"] = df["labels"].apply(parse_labels)

    # -------- text cleaning --------
    df["summary"] = df["title"].apply(clean_text)
    df["description"] = df["body"].apply(clean_text)

    # -------- fix_pr_titles merge --------
    def merge_pr_titles(val):
        if isinstance(val, list):
            return " ".join(clean_text(str(t)) for t in val)
        if isinstance(val, str):
            try:
                arr = ast.literal_eval(val)
                if isinstance(arr, list):
                    return " ".join(clean_text(str(t)) for t in arr)
                return ""
            except:
                return ""
        return ""

    df["fix_pr"] = df["fix_pr_titles"].apply(merge_pr_titles)

    # remove empty text rows
    df = df[(df["summary"] != "") | (df["description"] != "")]

    # -------- multi-label type mapping --------
    df["type"] = df["labels"].apply(normalize_labels)
    df = df[df["type"].map(len) > 0]

    # -------- bug_id --------
    df["bug_id"] = df.apply(lambda x: f"{x['repo']}#{x['number']}", axis=1)

    # -------- source --------
    df["source"] = "github"

    # -------- merged text --------
    df["text"] = (df["summary"] + " " + df["description"] + " " + df["fix_pr"]).str.strip()

    cleaned = df[[
        "bug_id",
        "summary",
        "description",
        "fix_pr_titles",
        "type",
        "labels",
        "source",
        "created_at",
        "closed_at",
        "text"
    ]]

    cleaned.to_csv("dataset/cleaned/github_cleaned.csv", index=False)

    print("GitHub cleaned dataset saved!")
    print(cleaned.head(5))
    print(cleaned.shape)


if __name__ == "__main__":
    preprocess_github()
