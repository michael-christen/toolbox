import networkx as nx
import pygraphviz
from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.models import Circle
from bokeh.models import ColumnDataSource
from bokeh.models import DataTable
from bokeh.models import MultiLine
from bokeh.models import TableColumn
from bokeh.models import TapTool
from bokeh.models import Toggle
from bokeh.plotting import curdoc
from bokeh.plotting import figure
from bokeh.plotting import from_networkx

# Step 1: Create a directed acyclic graph (DAG)
G = nx.DiGraph()
G.add_edges_from(
    [
        ("A", "B"),
        ("A", "C"),
        ("B", "D"),
        ("B", "E"),
        ("C", "F"),
        ("E", "G"),
        ("F", "H"),
    ]
)

# Step 2: Apply a Graphviz layout (using PyGraphviz) with tighter spacing
graphviz_layout = nx.nx_agraph.graphviz_layout(
    G, prog="dot", args="-Gnodesep=0.2 -Granksep=0.4"
)

# Step 3: Initialize graph and layout in Bokeh
plot = figure(
    title="Directed Acyclic Graph",
    tools="pan,box_zoom,reset,tap,wheel_zoom",
    active_scroll="wheel_zoom",
    x_range=(-100, 300),
    y_range=(-200, 100),
)

graph_renderer = from_networkx(G, graphviz_layout)
graph_renderer.node_renderer.glyph = Circle(radius=1, fill_color="skyblue")
graph_renderer.node_renderer.selection_glyph = Circle(
    radius=1, fill_color="orange"
)
graph_renderer.edge_renderer.glyph = MultiLine(line_color="gray", line_width=2)

plot.renderers.append(graph_renderer)

# Step 4: Create a data table for graph nodes
node_data = {"name": list(G.nodes)}
node_source = ColumnDataSource(node_data)

columns = [TableColumn(field="name", title="Node")]
data_table = DataTable(
    source=node_source, columns=columns, width=300, height=200
)

# Step 5: Toggle button for filtering nodes
toggle_button = Toggle(
    label="Show Subgraph", button_type="success", active=False
)


# Step 6: Add Python-based interactivity
def update_graph_colors(selected_node):
    """Update graph colors based on the selected node's ancestors and descendants."""
    if not selected_node:
        return

    node_renderer = graph_renderer.node_renderer.data_source
    edge_renderer = graph_renderer.edge_renderer.data_source
    node_renderer.data["fill_color"] = ["skyblue"] * len(
        node_renderer.data["index"]
    )
    edge_renderer.data["line_color"] = ["gray"] * len(
        edge_renderer.data["start"]
    )

    ancestors = nx.ancestors(G, selected_node)
    descendants = nx.descendants(G, selected_node)

    for idx, node in enumerate(node_renderer.data["index"]):
        if node == selected_node:
            node_renderer.data["fill_color"][idx] = "orange"
        elif node in ancestors:
            node_renderer.data["fill_color"][idx] = "blue"
        elif node in descendants:
            node_renderer.data["fill_color"][idx] = "green"

    for idx, (start, end) in enumerate(
        zip(edge_renderer.data["start"], edge_renderer.data["end"])
    ):
        if start in ancestors and end in ancestors:
            edge_renderer.data["line_color"][idx] = "blue"
        elif start in descendants and end in descendants:
            edge_renderer.data["line_color"][idx] = "green"

    node_renderer.trigger("data", None, node_renderer.data)
    edge_renderer.trigger("data", None, edge_renderer.data)


def select_node_from_table(attr, old, new):
    """Highlight node and ancestors/descendants when a table row is selected."""
    if not new:
        return

    selected_index = new[0]
    selected_node = node_data["name"][selected_index]
    update_graph_colors(selected_node)


def toggle_subgraph(active):
    """Filter graph to show only the selected node and its ancestors/descendants."""
    selected_indices = node_source.selected.indices
    if not selected_indices:
        return

    selected_node = node_data["name"][selected_indices[0]]

    if active:
        subgraph_nodes = set(nx.ancestors(G, selected_node))
        subgraph_nodes.add(selected_node)
        subgraph_nodes.update(nx.descendants(G, selected_node))

        subgraph = G.subgraph(subgraph_nodes)
        layout_subgraph = nx.nx_agraph.graphviz_layout(
            subgraph, prog="dot", args="-Gnodesep=0.2 -Granksep=0.4"
        )

        graph_renderer.node_renderer.data_source.data = {
            "index": list(subgraph.nodes),
            "fill_color": ["skyblue"] * len(subgraph.nodes),
        }
        graph_renderer.edge_renderer.data_source.data = {
            "start": [u for u, v in subgraph.edges],
            "end": [v for u, v in subgraph.edges],
            "line_color": ["gray"] * len(subgraph.edges),
        }

        graph_renderer.layout_provider.graph_layout = layout_subgraph
    else:
        graph_renderer.node_renderer.data_source.data = {
            "index": list(G.nodes),
            "fill_color": ["skyblue"] * len(G.nodes),
        }
        graph_renderer.edge_renderer.data_source.data = {
            "start": [u for u, v in G.edges],
            "end": [v for u, v in G.edges],
            "line_color": ["gray"] * len(G.edges),
        }

        graph_renderer.layout_provider.graph_layout = graphviz_layout


node_source.selected.on_change("indices", select_node_from_table)
toggle_button.on_click(lambda active: toggle_subgraph(active))

# Step 7: Combine layout and add to document
layout = column(row(plot, column(data_table, toggle_button)))
curdoc().add_root(layout)
