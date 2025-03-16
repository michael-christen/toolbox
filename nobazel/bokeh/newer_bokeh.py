import networkx as nx
from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.models import Circle
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS
from bokeh.models import DataTable
from bokeh.models import MultiLine
from bokeh.models import TableColumn
from bokeh.models import Toggle
from bokeh.plotting import curdoc
from bokeh.plotting import figure
from bokeh.plotting import from_networkx

# Create a simple DAG
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

# Generate a layout
layout = nx.spring_layout(G)

# Create a plot and renderer
plot = figure(
    title="Directed Acyclic Graph",
    tools="tap,pan,box_zoom,reset,wheel_zoom",
    active_scroll="wheel_zoom",
    x_range=(-2, 2),
    y_range=(-2, 2),
)

graph_renderer = from_networkx(G, layout)
graph_renderer.node_renderer.glyph = Circle(radius=0.1, fill_color="skyblue")
graph_renderer.edge_renderer.glyph = MultiLine(line_color="gray", line_width=2)
plot.renderers.append(graph_renderer)

# Create a data table for nodes
node_data = {"name": list(G.nodes)}
node_source = ColumnDataSource(data=node_data)

columns = [TableColumn(field="name", title="Node")]
data_table = DataTable(
    source=node_source, columns=columns, width=300, height=200
)

# JS Callback for hiding nodes and edges
hide_callback = CustomJS(
    args=dict(
        graph_renderer=graph_renderer,
        node_source=node_source,
        toggle=None,  # Placeholder for the toggle button
    ),
    code="""
    const selected_index = node_source.selected.indices[0];
    if (selected_index == null) {
        return;
    }

    const selected_node = node_source.data['name'][selected_index];
    const ancestors = new Set();
    const descendants = new Set();

    // Find ancestors and descendants using the adjacency relationships
    const edges = graph_renderer.edge_renderer.data_source.data;
    const nodes = graph_renderer.node_renderer.data_source.data['index'];

    function findAncestors(node) {
        for (let i = 0; i < edges['end'].length; i++) {
            if (edges['end'][i] === node) {
                ancestors.add(edges['start'][i]);
                findAncestors(edges['start'][i]);
            }
        }
    }

    function findDescendants(node) {
        for (let i = 0; i < edges['start'].length; i++) {
            if (edges['start'][i] === node) {
                descendants.add(edges['end'][i]);
                findDescendants(edges['end'][i]);
            }
        }
    }

    findAncestors(selected_node);
    findDescendants(selected_node);

    // Toggle state
    const isSubgraph = toggle.active;

    // Update visibility of nodes
    const node_visibility = graph_renderer.node_renderer.glyph.size;
    const edge_visibility = graph_renderer.edge_renderer.glyph.line_alpha;

    for (let i = 0; i < nodes.length; i++) {
        if (isSubgraph) {
            if (nodes[i] === selected_node || ancestors.has(nodes[i]) || descendants.has(nodes[i])) {
                node_visibility[i] = 15; // Visible size
            } else {
                node_visibility[i] = 0; // Hidden size
            }
        } else {
            node_visibility[i] = 15; // Reset visibility
        }
    }

    // Update visibility of edges
    for (let i = 0; i < edges['start'].length; i++) {
        if (isSubgraph && (ancestors.has(edges['start'][i]) || descendants.has(edges['end'][i]))) {
            edge_visibility[i] = 1; // Visible
        } else {
            edge_visibility[i] = 0; // Hidden
        }
    }

    graph_renderer.node_renderer.data_source.change.emit();
    graph_renderer.edge_renderer.data_source.change.emit();
""",
)

# Toggle Button
toggle_button = Toggle(
    label="Show Subgraph", button_type="success", active=False
)
hide_callback.args["toggle"] = toggle_button

# Link the callback to both table selection and the toggle button
node_source.selected.js_on_change("indices", hide_callback)
toggle_button.js_on_click(hide_callback)

# Layout
layout = column(row(plot, column(data_table, toggle_button)))
curdoc().add_root(layout)
