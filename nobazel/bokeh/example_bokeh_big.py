import networkx as nx
from networkx.drawing import nx_agraph
from bokeh.models import ColumnDataSource, CustomJS, Circle, MultiLine, Tabs, TabPanel
from bokeh.plotting import figure, from_networkx
from bokeh.layouts import layout
from bokeh.io import show

# Create a sample directed graph
# G = nx.DiGraph()
# G.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 6)])

G = nx.gnr_graph(1_000, 0.1)

# Precompute ancestors and descendants
ancestors = {node: list(nx.ancestors(G, node)) for node in G.nodes}
descendants = {node: list(nx.descendants(G, node)) for node in G.nodes}

# Create a Bokeh figure for the main graph
main_plot = figure(
    width=600,
    height=600,
    tools="tap,box_zoom,wheel_zoom,reset,pan",
    active_scroll="wheel_zoom",
    title="Main Graph",
)

# Convert the graph to Bokeh's format
layout = nx.spring_layout(G)
main_graph = from_networkx(G, nx_agraph.graphviz_layout, prog='dot')

# Node renderer
RADIUS = 5
main_graph.node_renderer.glyph = Circle(radius=RADIUS, fill_color="skyblue")
main_graph.node_renderer.selection_glyph = Circle(radius=RADIUS, fill_color="orange")

# Edge renderer
main_graph.edge_renderer.glyph = MultiLine(line_color="gray", line_width=2)

# Add the main graph to the main plot
main_plot.renderers.append(main_graph)

# Subgraph placeholder
sub_plot = figure(
    width=600,
    height=600,
    tools="tap,box_zoom,wheel_zoom,reset,pan",
    active_scroll="wheel_zoom",
    title="Subgraph",
)

sub_graph = from_networkx(nx.DiGraph(), nx_agraph.graphviz_layout, prog='dot')
sub_plot.renderers.append(sub_graph)

# Create Tabs
main_tab = TabPanel(child=main_plot, title="Main Graph")
sub_tab = TabPanel(child=sub_plot, title="Subgraph")
tabs = Tabs(tabs=[main_tab, sub_tab])

# JavaScript callback for dynamic subgraph
callback = CustomJS(
    args=dict(
        main_graph=main_graph,
        sub_plot=sub_plot,
        sub_graph=sub_graph,
        ancestors=ancestors,
        descendants=descendants,
        edges=[(u, v) for u, v in G.edges],
        #G=G,
    ),
    code="""
    const selected_indices = main_graph.node_renderer.data_source.selected.indices;
    const sub_renderer = sub_graph.edge_renderer.data_source;

    // Clear previous subgraph
    sub_renderer.data = { start: [], end: [] };

    if (selected_indices.length > 0) {
        const selected_node = selected_indices[0];

        // Find nodes in the subgraph (ancestors, descendants, and the node itself)
        const ancestor_nodes = ancestors[selected_node];
        const descendant_nodes = descendants[selected_node];
        const subgraph_nodes = new Set([selected_node, ...ancestor_nodes, ...descendant_nodes]);

        // Extract edges within the subgraph
        const sub_edges = [];
        for (const [u, v] of edges) {
            if (subgraph_nodes.has(u) && subgraph_nodes.has(v)) {
                sub_edges.push([u, v]);
            }
        }

        // Update the subgraph renderer
        const start = sub_edges.map(e => e[0]);
        const end = sub_edges.map(e => e[1]);
        sub_renderer.data = { start, end };
        sub_renderer.change.emit();
    }
    """
)

# Attach callback to the selection change
main_graph.node_renderer.data_source.selected.js_on_change("indices", callback)

# Show the tabs
show(tabs)
