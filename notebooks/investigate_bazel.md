---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
%load_ext autoreload
%autoreload 2
```

```{code-cell} ipython3
import networkx
import pandas
from networkx.drawing import nx_agraph
```

```{code-cell} ipython3
%matplotlib inline
```

```{code-cell} ipython3
g = networkx.read_gml("/home/mchristen/devel/toolbox/my.gml")
```

```{code-cell} ipython3
from apps.bazel_parser import bazel_parser
```

```{code-cell} ipython3
bazel_parser.get_node_field_names()
```

```{code-cell} ipython3
nodes = g.nodes(data=True)
```

```{code-cell} ipython3
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
```

```{code-cell} ipython3
df_nodes
```

```{code-cell} ipython3
df_nodes.nlargest(50, "num_source_descendants")
```

```{code-cell} ipython3
# 5 nodes that take time, sorted by largest number of source_descendants
# XXX: How to select based on this weighted by node_duration_s
df_nodes.loc[df_nodes["node_duration_s"] > 0].sort_values(
    ["num_source_descendants", "node_duration_s"], ascending=False
)[:5]
```

```{code-cell} ipython3
df_nodes["weighted_source"] = (
    df_nodes["node_duration_s"] * df_nodes["num_source_descendants"]
)
```

```{code-cell} ipython3
# Find the most impacted tests
df_nodes.nlargest(10, "weighted_source")
```

```{code-cell} ipython3
# Find the most impacting source files
df_nodes.loc[df_nodes["node_probability_cache_hit"] < 1].nlargest(
    10, "num_duration_ancestors"
)
```

```{code-cell} ipython3
networkx.ancestors(g, "//hw_drivers/lis3mdl:lis3mdl.proto")
```

```{code-cell} ipython3
df_nodes["num_parents"].plot.hist()
```

```{code-cell} ipython3
import matplotlib.pyplot as plt

ax = df_nodes['num_parents'].nlargest(20).sort_values().plot.barh(legend=False)
# Align the y-axis labels to the left and adjust spacing
# ax.set_yticklabels(ax.get_yticklabels(), ha='left', position=(-0.75, 0))  # Adjust position to the left

# Adjust the left margin to create space for the labels
# plt.subplots_adjust(left=0.2)
ax
```

```{code-cell} ipython3
def get_subgraph(label: str, graph: networkx.DiGraph) -> networkx.DiGraph:
    return graph.subgraph(
        networkx.ancestors(graph, label)
        | networkx.descendants(graph, label)
        | set([label])
    )
```

```{code-cell} ipython3
def show_graph(graph: networkx.DiGraph, include_labels: bool = True, show_numbers: bool = False) -> None:
    if include_labels:
        a = nx_agraph.to_agraph(graph)
        a.layout("dot")
        display(a)
    elif show_numbers:
        number_labels = {name: idx for idx, name in enumerate(graph.nodes)}
        networkx.draw(graph, pos=nx_agraph.graphviz_layout(graph, prog="dot"), labels=number_labels)
        for name, idx in sorted(number_labels.items(), key=lambda x: x[1]):
            print(f'- {idx}: {name}')
    else:
          networkx.draw(graph, pos=nx_agraph.graphviz_layout(graph, prog="dot"))
```

```{code-cell} ipython3
def show_subgraph(whole_graph: networkx.DiGraph, node_label: str, include_labels: bool = True, show_numbers: bool = False) -> None:
    ancestors = networkx.ancestors(whole_graph, node_label)
    descendants = networkx.descendants(whole_graph, node_label)
    graph = whole_graph.subgraph(
        ancestors | descendants | set([node_label])
    )
    if include_labels:
        a = nx_agraph.to_agraph(graph)
        a.layout("dot")
        display(a)
    elif show_numbers:
        # XXX: Print adjacency list
        idx = 0
        number_labels = {
            node_label: idx,
        }
        idx += 1
        for src_node, next_nodes in networkx.bfs_successors(whole_graph, source=node_label):
            print(f'{src_node} ->')
            for node in next_nodes:
                print(f'- {node}')
                if node in number_labels:
                    continue
                # XXX: Print adjacency list as well
                number_labels[node] = idx
                idx += 1

        for src_node, next_nodes in networkx.bfs_successors(networkx.reverse(whole_graph), source=node_label):
            print(f'{src_node} <-')
            for node in next_nodes:
                print(f'- {node}')
                if node in number_labels:
                    continue
                number_labels[node] = idx
                idx += 1
        print()
        # number_labels = {name: idx for idx, name in enumerate(graph.nodes)}
        # XXX: Doesn't look great w/ 3-digit node numbers and greater
        networkx.draw(graph, pos=nx_agraph.graphviz_layout(graph, prog="dot"), labels=number_labels)
        for name, idx in sorted(number_labels.items(), key=lambda x: x[1]):
            print(f'- {idx}: {name}')
    else:
          networkx.draw(graph, pos=nx_agraph.graphviz_layout(graph, prog="dot"))
```

```{code-cell} ipython3
xyz = networkx.DiGraph([[0, 1], [0, 2], [1, 3]])
print(dict(networkx.bfs_successors(xyz, source=0)))
print(dict(networkx.bfs_successors(networkx.reverse(xyz), source=3)))
```

```{code-cell} ipython3
H = get_subgraph("//apps/sbr:simulator_sbr", g)
```

```{code-cell} ipython3
show_subgraph(g, "//apps/sbr:simulator_sbr", include_labels=False, show_numbers=True)
```

```{code-cell} ipython3
show_graph(H, include_labels=True)
```

```{code-cell} ipython3
import numpy as np
import pandas as pd
```

```{code-cell} ipython3
df_nodes["num_parents"].mean()
```

```{code-cell} ipython3
df_nodes.groupby("node_class").mean().sort_values(
    "num_descendants", ascending=False
)
```

```{code-cell} ipython3
df_nodes.groupby("node_class").describe()["num_ancestors"].sort_values(
    ["max", "75%"], ascending=False
)[:10]
```

```{code-cell} ipython3
df_nodes.groupby("node_class").describe()["num_duration_ancestors"][
    "mean"
].sort_values(ascending=False)[:40].plot.bar()
```

```{code-cell} ipython3
df_nodes.groupby("node_class").describe()["num_source_descendants"][
    "mean"
].sort_values(ascending=False)[:40].plot.bar()
```

```{code-cell} ipython3
df_nodes.loc[df_nodes["node_class"].str.endswith("_test")].sort_values(
    "num_source_descendants", ascending=False
)["num_source_descendants"].plot.bar(subplots=True)
```

```{code-cell} ipython3
df_nodes.loc[df_nodes["node_class"].str.endswith("_test")].sort_values(
    "group_probability_cache_hit", ascending=True
)["group_probability_cache_hit"].plot.bar(subplots=True)
```

```{code-cell} ipython3
show_graph(get_subgraph("//examples/basic:grpc_test", g), include_labels=True)
```

```{code-cell} ipython3
df_nodes.loc[df_nodes["node_class"] == "source_file"]
```

```{code-cell} ipython3
show_graph(get_subgraph("//:requirements_lock.txt", g), include_labels=True)
```

```{code-cell} ipython3
show_graph(get_subgraph("//:requirements_test", g), include_labels=True)
```

```{code-cell} ipython3
df_nodes.loc["//:requirements_test"]
```

```{code-cell} ipython3
df_nodes.loc["//:requirements_lock.txt"]
```

```{code-cell} ipython3
from apps.bazel_parser import panel
import panel as pn

pn.extension()
```

```{code-cell} ipython3
layout = panel.get_panel_layout(g)
layout.servable()
# Show in a separate window, helps with servable content
# layout.show()
# Displays inline
# display(layout)
```

```{code-cell} ipython3
import matplotlib.pyplot as plt
import numpy as np

# Sample data
data = np.random.rand(50)

# Create the scatter plot on a single axis (y-axis in this case)
plt.scatter(np.zeros_like(data), data)

# Customize the plot
plt.title("Scatter Plot on a Single Axis")
plt.xlabel("Constant Value (e.g., 0)")
plt.ylabel("Data Values")

# Remove x-axis ticks for cleaner look
plt.xticks([])

# Display the plot
plt.show()
```

```{code-cell} ipython3

```
