
import json
import pandas as pd

# Load username mapping from JSON
with open("dataset/congress_network_data.json", "r",
          encoding="utf-8") as file:
    data = json.load(file)[0]

usernames = data["usernameList"]

# Create mapping: Vertex ID -> Twitter Username
username_map = {
    vertex_id: username
    for vertex_id, username in enumerate(usernames)
}

# Load GraphX metrics
df = pd.read_csv("results/graph_metrics.csv")

# Add Twitter usernames
df["Twitter_Username"] = df["Vertex_ID"].map(username_map)

# Save updated metrics
df.to_csv(
    "results/graph_metrics_with_usernames.csv",
    index=False
)

# Update top account rankings
top = pd.read_csv("results/top_accounts.csv")
top["Twitter_Username"] = top["Vertex_ID"].map(username_map)

top.to_csv(
    "results/top_accounts_with_usernames.csv",
    index=False
)

print("Username mapping completed successfully!")
print("\nTop 10 accounts by PageRank:")

print(
    df.nlargest(10, "PageRank")[
        ["Vertex_ID", "Twitter_Username", "In_Degree", "Out_Degree", "PageRank"]
    ].to_string(index=False)
)
