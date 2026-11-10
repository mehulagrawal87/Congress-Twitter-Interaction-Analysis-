# Congress Twitter Interaction Analysis

A directed social-network analysis project built with **Apache Spark
GraphX and Scala**. The project studies interaction patterns among U.S.
Congress Twitter accounts by constructing a directed graph, calculating
degree metrics, identifying influential accounts with PageRank,
analyzing connected components, and visualizing the network.

## Project Overview

This project uses the Stanford SNAP Congress Twitter dataset to examine
how accounts interact with one another.

### Objectives

1.  Construct a directed graph from the interaction edge list.
2.  Calculate the in-degree and out-degree of each account.
3.  Identify accounts receiving and generating the highest number of
    interactions.
4.  Analyze connected components in the interaction network.
5.  Compare PageRank rankings with in-degree rankings.
6.  Visualize the interaction network and highlight central accounts.

## Technology Stack

-   **Apache Spark 3.5.9**
-   **GraphX** for graph processing and graph algorithms
-   **Scala 2.13.8**
-   **Java 17**
-   **SBT** for project build and execution
-   **Python** for supplementary visualizations
-   **Pandas, Matplotlib, Seaborn, NetworkX** for data handling and
    plotting

## Dataset

**Source:** [SNAP -- Congress
Twitter](https://snap.stanford.edu/data/congress-twitter.html)

The downloaded dataset includes a weighted, directed edge list and a
JSON file containing account information and username mappings.

  Dataset property          Value
  ---------------------- --------
  Vertices (accounts)         475
  Directed edges           13,289
  Connected components          1

The edge-list format stores a source account, destination account, and
edge weight. An edge from `source` to `destination` represents a
directed interaction from the source account to the destination account.

> **Note on metrics:** GraphX `inDegrees` and `outDegrees` count
> incoming and outgoing edges. The edge weights are retained while
> parsing the input, but the degree calculations and the
> `staticPageRank(10)` call in this implementation are not weighted by
> those edge values. The reported PageRank is therefore a relative
> ranking score, not a probability.

## Repository Structure

``` text
Congress-Twitter-Analysis/
│
├── dataset/
│   ├── congress.edgelist
│   ├── congress_network_data.json
│   └── README.txt
│
├── project/
│   └── build.properties
│
├── src/
│   ├── main/
│   │   └── scala/
│   │       └── CongressTwitterAnalysis.scala
│   └── username_mapping.py
│
├── results/
│   ├── graph_metrics.csv
│   ├── top_accounts.csv
│   ├── graph_metrics_with_usernames.csv
│   └── top_accounts_with_usernames.csv
│
├── visualization/
│   ├── visualize.py
│   ├── network_graph.py
│   └── charts/
│       ├── top_in_degree.png
│       ├── top_out_degree.png
│       ├── pagerank_vs_indegree.png
│       └── twitter_network.png
│
├── build.sbt
└── README.md
```

The structure above describes the expected project layout. Include the
files that are present in your local project when uploading the
repository.

## Prerequisites

Install the following software before running the project:

-   Java Development Kit (JDK) 17
-   SBT
-   Python 3
-   Apache Spark 3.5.9 (required if you also want to run the Spark shell
    separately; the SBT project declares Spark dependencies)

Check installations:

``` cmd
java -version
sbt --version
python --version
```

## Setup and Execution

### 1. Clone the repository

``` bash
git clone https://github.com/<your-username>/Congress-Twitter-Analysis.git
cd Congress-Twitter-Analysis
```

Replace `<your-username>` with your GitHub username.

### 2. Compile the Scala project

``` bash
sbt compile
```

### 3. Run the GraphX analysis

Run this command from the repository root:

``` bash
sbt run
```

The Scala application reads `dataset/congress.edgelist`, performs the
graph analysis, prints the summary and top-account rankings, and writes
CSV outputs to the `results/` directory.

### 4. Install Python visualization dependencies

``` bash
python -m pip install pandas matplotlib seaborn networkx
```

### 5. Generate the username mapping

``` bash
python src/username_mapping.py
```

This maps numeric vertex IDs to Twitter usernames using
`dataset/congress_network_data.json` and creates username-enriched CSV
files in `results/`.

### 6. Generate the charts

``` bash
python visualization/visualize.py
python visualization/network_graph.py
```

Generated chart images are saved in `visualization/charts/`.

## Analysis Performed

### Directed graph construction

The Scala program parses each source--destination pair from the weighted
edge list and constructs a GraphX graph. The direction of each edge is
preserved.

### Degree analysis

-   **In-degree:** Number of incoming edges to an account.
-   **Out-degree:** Number of outgoing edges from an account.

The program ranks accounts separately by in-degree and out-degree to
identify accounts receiving and generating the most interactions.

### Connected components

GraphX connected-components analysis returned **one component** for this
dataset. GraphX's `connectedComponents()` identifies connectivity
without considering edge direction; this result should be interpreted as
one weakly connected component, not proof that every account can reach
every other account by following directed edges.

### PageRank

The project calculates PageRank using GraphX `staticPageRank(10)` and
compares the resulting ranking with the in-degree ranking. The
comparison helps identify accounts that are prominent both by incoming
connections and by their position in the wider network.

## Key Results

The following values were produced by the Spark execution:

-   **475** vertices
-   **13,289** directed edges
-   **1** connected component
-   Highest in-degree: **GOPLeader** --- **127**
-   Highest out-degree: **SpeakerPelosi** --- **210**
-   Highest PageRank: **GOPLeader** --- **4.418292**

The top-ten PageRank accounts also appear in the top-ten in-degree
results in this run. See the CSV result files for the full rankings and
metric values.

## Visualizations

The Python scripts generate the following figures:

1.  **Top 10 Accounts by In-Degree** -- accounts with the largest number
    of incoming connections.
2.  **Top 10 Accounts by Out-Degree** -- accounts with the largest
    number of outgoing connections.
3.  **PageRank vs In-Degree** -- a scatter plot comparing the two
    centrality measures.
4.  **Directed Congress Twitter Network** -- a network view highlighting
    the top PageRank accounts.

The network visualization is supplementary and is generated with
NetworkX. The graph metrics and graph algorithms are calculated in Spark
GraphX.

## Output Files

  --------------------------------------------------------------------------------
  File                                         Description
  -------------------------------------------- -----------------------------------
  `results/graph_metrics.csv`                  Vertex-level in-degree, out-degree,
                                               component ID, and PageRank

  `results/top_accounts.csv`                   Combined top-account rankings

  `results/graph_metrics_with_usernames.csv`   Graph metrics with Twitter
                                               usernames

  `results/top_accounts_with_usernames.csv`    Top-account results with usernames

  `visualization/charts/`                      Generated PNG charts
  --------------------------------------------------------------------------------

## Limitations

-   The dataset represents a particular snapshot and may not reflect
    current Twitter interactions.
-   Numeric vertex IDs require the supplied JSON username mapping to be
    interpreted as account names.
-   Degree metrics count edges and do not sum edge weights.
-   The current PageRank calculation uses GraphX's standard unweighted
    `staticPageRank(10)` method.
-   The full network plot is dense, so individual edges may be difficult
    to distinguish visually.

## Future Improvements

-   Add weighted in-degree and out-degree (interaction strength)
    analysis.
-   Compare weighted and unweighted PageRank.
-   Explore strongly connected components and community detection.
-   Create an interactive network visualization with Gephi.
-   Add further centrality measures such as betweenness and closeness
    centrality.

## References

1.  SNAP, **Congress Twitter Dataset**:
    https://snap.stanford.edu/data/congress-twitter.html
2.  Apache Spark GraphX Documentation: https://spark.apache.org/graphx/
3.  Apache Spark Documentation: https://spark.apache.org/docs/3.5.9/
4.  Scala Documentation: https://docs.scala-lang.org/
5.  NetworkX Documentation: https://networkx.org/documentation/stable/

## Author

**Mehul Agrawal**\
B.Tech -- Computer Science and Engineering\
Lovely Professional University

------------------------------------------------------------------------

If you use this repository, please cite the original SNAP dataset and
the relevant software documentation.
