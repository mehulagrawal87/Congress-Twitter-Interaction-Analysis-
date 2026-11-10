
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import json

# Step 1: Load username mapping
with open(
    "dataset/congress_network_data.json",
    "r",
    encoding="utf-8"
) as file:
    data = json.load(file)[0]

usernames = data["usernameList"]

username_map = {
    vertex_id: username
    for vertex_id, username in enumerate(usernames)
}

# Step 2: Load original directed edge list
file_path = "dataset/congress.edgelist"

edges = []

with open(file_path, "r") as file:
    for line in file:
        parts = line.strip().split()

        if len(parts) >= 3:
            source = int(parts[0])
            target = int(parts[1])
            edges.append((source, target))

# Step 3: Create directed graph
G = nx.DiGraph()
G.add_edges_from(edges)

# Step 4: Load GraphX metrics with usernames
df = pd.read_csv("results/graph_metrics_with_usernames.csv")

# Identify top 10 accounts by PageRank
top_nodes = set(
    df.nlargest(10, "PageRank")["Vertex_ID"].astype(int)
)

# Step 5: Create output directory
os.makedirs("visualization/charts", exist_ok=True)

# Node colors
node_colors = [
    "red" if node in top_nodes else "skyblue"
    for node in G.nodes()
]

# Node sizes based on In-Degree
in_degree = dict(G.in_degree())

node_sizes = [
    50 + in_degree[node] * 8
    for node in G.nodes()
]

# Step 6: Draw network
plt.figure(figsize=(18, 14))

pos = nx.spring_layout(G, seed=42, k=0.25)

nx.draw_networkx_edges(
    G, pos,
    alpha=0.12,
    arrows=True,
    arrowsize=5,
    width=0.5,
    edge_color="gray"
)

nx.draw_networkx_nodes(
    G, pos,
    node_color=node_colors,
    node_size=node_sizes,
    alpha=0.85
)

# Label top 10 accounts with Twitter usernames
labels = {
    node: username_map.get(node, str(node))
    for node in top_nodes
}

nx.draw_networkx_labels(
    G, pos,
    labels=labels,
    font_size=9,
    font_weight="bold"
)

plt.title(
    "Congress Twitter Directed Interaction Network",
    fontsize=16
)

plt.axis("off")
plt.tight_layout()

# Step 7: Save graph
plt.savefig(
    "visualization/charts/twitter_network.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Username-based network graph generated successfully!")
print("Total nodes:", G.number_of_nodes())
print("Total edges:", G.number_of_edges())
print("\nHighlighted Top 10 PageRank Accounts:")

for node in sorted(top_nodes):
    print(node, ":", username_map.get(node, "Unknown"))
