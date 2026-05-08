# test_scoring.py
# Temporary script — run once to see CI score distribution across real data
# Delete after v0.1 is done

import pandas as pd
import glob
import os
from scoring.ci_score import score_title

# Pick the most recent CSV in data/
csv_files = glob.glob("data/*.csv")
latest = max(csv_files, key=os.path.getmtime)
print(f"Using: {latest}\n")

df = pd.read_csv(latest)

# Score every title
results = df["title"].apply(score_title)
df["score"] = results.apply(lambda x: x["score"])
df["grade"] = results.apply(lambda x: x["grade"])

# Distribution
print("Grade distribution:")
print(df["grade"].value_counts().sort_index())

print("\nScore stats:")
print(df["score"].describe())

print("\nSample — Grade A listings:")
print(df[df["grade"] == "A"][["title", "score", "price_usd"]].head(5).to_string())

print("\nSample — Grade D listings:")
print(df[df["grade"] == "D"][["title", "score", "price_usd"]].head(5).to_string())