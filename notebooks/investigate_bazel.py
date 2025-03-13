# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import networkx
import pandas
from networkx.drawing import nx_agraph

# %%
# %matplotlib inline

# %%
g = networkx.read_gml("/home/mchristen/devel/toolbox/my.gml")

# %%
nodes = g.nodes(data=True)

# %%
df_nodes = pandas.DataFrame(
    [n[1] for n in nodes],
    columns=[
        "node_name",
        "node_class",
        "num_parents",
        "num_ancestors",
        "num_duration_ancestors",
        "num_children",
        "num_descendants",
        "num_source_descendants",
        "pagerank",
        "hubs_metric",
        "authorities_metric",
        "node_duration_s",
        "group_duration_s",
        "expected_duration_s",
        "node_probability_cache_hit",
        "group_probability_cache_hit",
    ],
)
df_nodes.set_index("node_name", inplace=True)

# %%
df_nodes

# %%
df_nodes.nlargest(50, "num_source_descendants")

# %%
# 5 nodes that take time, sorted by largest number of source_descendants
# XXX: How to select based on this weighted by node_duration_s
df_nodes.loc[df_nodes["node_duration_s"] > 0].sort_values(
    ["num_source_descendants", "node_duration_s"], ascending=False
)[:5]

# %%
df_nodes["weighted_source"] = (
    df_nodes["node_duration_s"] * df_nodes["num_source_descendants"]
)

# %%
# Find the most impacted tests
df_nodes.nlargest(10, "weighted_source")

# %%
# Find the most impacting source files
df_nodes.loc[df_nodes["node_probability_cache_hit"] < 1].nlargest(
    10, "num_duration_ancestors"
)

# %%
networkx.ancestors(g, "//hw_drivers/lis3mdl:lis3mdl.proto")

# %%
df_nodes["num_parents"].plot.hist()


# %%
def get_subgraph(label: str, graph: networkx.DiGraph) -> networkx.DiGraph:
    return graph.subgraph(
        networkx.ancestors(graph, label)
        | networkx.descendants(g, label)
        | set([label])
    )


# %%
def show_graph(graph: networkx.DiGraph, include_labels: bool = True) -> None:
    if include_labels:
        a = nx_agraph.to_agraph(graph)
        a.layout("dot")
        display(a)
    else:
        networkx.draw(graph, nx_agraph.graphviz_layout(graph, prog="dot"))


# %%
H = get_subgraph("//apps/sbr:simulator_sbr", g)

# %%
show_graph(H, include_labels=False)

# %%
show_graph(H, include_labels=True)

# %%
import numpy as np
import pandas as pd

# %%
df_nodes["num_parents"].mean()

# %%
df_nodes.groupby("node_class").mean().sort_values(
    "num_descendants", ascending=False
)

# %%
df_nodes.groupby("node_class").describe()["num_ancestors"].sort_values(
    ["max", "75%"], ascending=False
)[:10]

# %%
df_nodes.groupby("node_class").describe()["num_duration_ancestors"][
    "mean"
].sort_values(ascending=False)[:40].plot.bar()

# %%
df_nodes.groupby("node_class").describe()["num_source_descendants"][
    "mean"
].sort_values(ascending=False)[:40].plot.bar()

# %%
df_nodes.loc[df_nodes["node_class"].str.endswith("_test")].sort_values(
    "num_source_descendants", ascending=False
)["num_source_descendants"].plot.bar(subplots=True)

# %%
df_nodes.loc[df_nodes["node_class"].str.endswith("_test")].sort_values(
    "group_probability_cache_hit", ascending=True
)["group_probability_cache_hit"].plot.bar(subplots=True)

# %%
show_graph(get_subgraph("//examples/basic:grpc_test", g), include_labels=True)

# %%
df_nodes.loc[df_nodes["node_class"] == "source_file"]

# %%
show_graph(get_subgraph("//:requirements_lock.txt", g), include_labels=True)

# %%
show_graph(get_subgraph("//:requirements_test", g), include_labels=True)

# %%
df_nodes.loc["//:requirements_test"]

# %%
df_nodes.loc["//:requirements_lock.txt"]

# %%
