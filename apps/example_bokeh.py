import networkx
import panel as pn
from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import Circle
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS
from bokeh.models import MultiLine
from bokeh.models import TapTool
from bokeh.models.widgets import DataTable
from bokeh.models.widgets import TableColumn
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from networkx.drawing import nx_agraph


def main() -> None:
    # Create a NetworkX graph
    # G = networkx.fast_gnp_random_graph(100, 0.1, directed=True)
    G = networkx.gnr_graph(100, 0.1)
    # G = networkx.Graph()
    # G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])
    # for i in G.nodes:
    #     G.nodes[i]["name"] = f"Node {i}"

    # Prepare data for the table
    node_data = {
        "Node": [f"Node {i}" for i in G.nodes],
        "Highlight": ["No" for _ in G.nodes],
    }

    # Initialize Panel for interactive layout
    pn.extension()
    layout = get_panel_layout(G=G, node_data=node_data)
    pn.serve(layout)


def get_panel_layout(
    G: networkx.DiGraph, node_data: dict[str, list[str]]
) -> pn.layout.base.Panel:
    """Get Panel Layout

    References

    # network_graph = from_networkx(G, networkx.spring_layout, scale=1, center=(0, 0))
    # neato
    # dot
    # twopi
    # fdp
    # sfdp
    # circo
    """
    # Prepare Bokeh graph layout
    plot = figure(
        width=800,
        height=800,
        tools="tap,box_zoom,wheel_zoom,reset,pan",
        active_scroll="wheel_zoom",
        title="Network Graph",
    )
    network_graph = from_networkx(G, nx_agraph.graphviz_layout, prog="dot")

    # Add visual properties to the graph
    network_graph.node_renderer.glyph = Circle(radius=5, fill_color="skyblue")
    network_graph.edge_renderer.glyph = MultiLine(
        line_color="gray", line_alpha=0.5, line_width=1
    )
    plot.renderers.append(network_graph)

    source = ColumnDataSource(node_data)

    # JavaScript callback for interactivity
    # XXX: Likely define the type of the input graph a little better, TypedDict
    callback = CustomJS(
        args=dict(source=source, graph_renderer=network_graph),
        code="""
        const selected_index = graph_renderer.node_renderer.data_source.selected.indices[0];
        const data = source.data;
        if (selected_index !== undefined) {
            for (let i = 0; i < data['Highlight'].length; i++) {
                data['Highlight'][i] = (i === selected_index) ? "Yes" : "No";
            }
            source.change.emit();
        }
    """,
    )
    # Callback for clicking a row (table -> graph)
    table_to_graph_callback = CustomJS(
        args=dict(source=source, graph_renderer=network_graph),
        code="""
        const selected_index = cb_obj.indices[0];
        if (selected_index !== undefined) {
            graph_renderer.node_renderer.data_source.selected.indices = [selected_index];
        }
    """,
    )

    network_graph.node_renderer.data_source.selected.js_on_change(
        "indices", callback
    )
    source.selected.js_on_change("indices", table_to_graph_callback)

    # Create a DataTable to view source
    columns = [TableColumn(field=k, title=k) for k in node_data.keys()]
    data_table = DataTable(
        source=source, columns=columns, width=400, height=800
    )

    # Combine the plot and table into a Panel layout
    layout = pn.Row(pn.pane.Bokeh(plot), pn.pane.Bokeh(data_table))
    return layout


if __name__ == "__main__":
    main()
