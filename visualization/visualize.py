
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

# Load username mapping
with open("dataset/congress_network_data.json", "r",
          encoding="utf-8") as file:
    data = json.load(file)[0]

usernames = data["usernameList"]

# Load GraphX metrics with usernames
df = pd.read_csv("results/graph_metrics_with_usernames.csv")

# Create output folder
os.makedirs("visualization/charts", exist_ok=True)

sns.set_theme(style="whitegrid")

# Chart 1: Top 10 In-Degree
top_in = df.nlargest(10, "In_Degree").copy()

plt.figure(figsize=(12, 7))
sns.barplot(
    data=top_in,
    x="In_Degree",
    y="Twitter_Username"
)
plt.title("Top 10 Twitter Accounts by In-Degree")
plt.xlabel("In-Degree")
plt.ylabel("Twitter Username")
plt.tight_layout()
plt.savefig(
    "visualization/charts/top_in_degree.png",
    dpi=300
)
plt.close()

# Chart 2: Top 10 Out-Degree
top_out = df.nlargest(10, "Out_Degree").copy()

plt.figure(figsize=(12, 7))
sns.barplot(
    data=top_out,
    x="Out_Degree",
    y="Twitter_Username"
)
plt.title("Top 10 Twitter Accounts by Out-Degree")
plt.xlabel("Out-Degree")
plt.ylabel("Twitter Username")
plt.tight_layout()
plt.savefig(
    "visualization/charts/top_out_degree.png",
    dpi=300
)
plt.close()

# Chart 3: PageRank vs In-Degree
plt.figure(figsize=(11, 7))

sns.scatterplot(
    data=df,
    x="In_Degree",
    y="PageRank",
    s=70
)

# Highlight and label top 10 PageRank accounts
top_rank = df.nlargest(10, "PageRank")

for _, row in top_rank.iterrows():
    plt.annotate(
        row["Twitter_Username"],
        (row["In_Degree"], row["PageRank"]),
        fontsize=8,
        xytext=(5, 5),
        textcoords="offset points"
    )

plt.title("PageRank vs In-Degree")
plt.xlabel("In-Degree")
plt.ylabel("PageRank")
plt.tight_layout()
plt.savefig(
    "visualization/charts/pagerank_vs_indegree.png",
    dpi=300
)
plt.close()

print("All three username-based visualizations generated!")
