import pandas as pd

df = pd.read_csv("dataset/raw/github_issues_raw.csv")
print(df.shape)
print(df.head())
print(df.labels.head())
