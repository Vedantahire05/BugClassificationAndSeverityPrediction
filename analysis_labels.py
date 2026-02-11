import pandas as pd
from collections import Counter

df = pd.read_csv("dataset/cleaned/github_cleaned.csv")

# convert string list to python list
df["type"] = df["type"].apply(eval)

# frequency
flat = [lbl for labels in df["type"] for lbl in labels]
freq = Counter(flat)
print("Label Frequency:\n", freq)

# multi-label density
density = df["type"].map(len).value_counts().sort_index()
print("\nMulti-label Density:\n", density)

# co-occurrence matrix
labels = sorted(freq.keys())
matrix = {l: {m: 0 for m in labels} for l in labels}

for labels_set in df["type"]:
    for a in labels_set:
        for b in labels_set:
            if a != b:
                matrix[a][b] += 1

print("\nCo-occurrence Matrix:\n")
for a in labels:
    print(a, matrix[a])
