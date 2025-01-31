
import pathlib

import networkx

from networkx.drawing import nx_agraph
from bokeh.models import ColumnDataSource, MultiLine, Circle, CustomJS, TapTool, HoverTool, CheckboxGroup, RadioGroup
from bokeh.plotting import figure, from_networkx
from bokeh.layouts import column
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.io import show
import panel as pn
from panel.io import save


SIZING_MODE = 'fixed'


def run_panel(graph: networkx.DiGraph, html_out: pathlib.Path | None) -> None:
    # Initialize Panel for interactive layout
    pn.extension(sizing_mode=SIZING_MODE)
    layout = get_panel_layout(graph=graph)
    if html_out:
        save.save(layout, html_out)
    pn.serve(layout)


def get_panel_layout(graph: networkx.DiGraph) -> pn.layout.base.Panel:
    """Get Panel Layout

    References

    # network_graph = from_networkx(graph, networkx.spring_layout, scale=1, center=(0, 0))
    # neato
    # dot
    # twopi
    # fdp
    # sfdp
    # circo
    """
    # Prepare Bokeh graph layout
    plot = figure(
                  height=800,
                  width=800,
                  tools="tap,box_zoom,wheel_zoom,reset,pan",
                  active_scroll="wheel_zoom",
                  sizing_mode=SIZING_MODE,
                  title="Network Graph")
    plot.axis.visible = False
    # pos = nx_agraph.graphviz_layout(graph, prog='dot')
    # network_graph = from_networkx(graph, pos)  # type: ignore
    network_graph = from_networkx(graph, networkx.spring_layout)  # type: ignore
    # Node
    network_graph.node_renderer.data_source.data['color'] = ['skyblue'] * len(graph.nodes)
    network_graph.node_renderer.data_source.data['alpha'] = [1.0] * len(graph.nodes)
    # Edge
    network_graph.edge_renderer.data_source.data['line_color'] = ['gray' for edge in graph.edges]
    network_graph.edge_renderer.data_source.data['alpha'] = [1.0] * len(graph.edges)

    # Create a DataTable to view source
    # XXX: How to keep this in sync with Node?
    fields = [
        'Node',
        'Highlight',
        'node_class',
        'num_descendants',
        'num_source_descendants',
        'num_children',
        'num_ancestors',
        'num_duration_ancestors',
        'num_parents',
        'pagerank',
        'hubs_metric',
        'authorities_metric',
        'node_duration_s',
        'group_duration_s',
        'expected_duration_s',
        'node_probability_cache_hit',
        'group_probability_cache_hit',
    ]
    columns = [TableColumn(field=k, title=k) for k in fields]
    data_table = DataTable(source=network_graph.node_renderer.data_source,
                           columns=columns,
                           height=800,
                           width=800,
                           sizing_mode=SIZING_MODE,
                           fit_columns=True,
                           )
    # Create a CheckboxGroup for toggling columns
    checkbox_group = CheckboxGroup(labels=fields, active=list(range(len(fields))))

    # CustomJS to toggle column visibility
    check_callback = CustomJS(args=dict(data_table=data_table, columns=columns), code="""
        const active = cb_obj.active;  // Indices of selected checkboxes

        const visible_columns = [];
        for (let i = 0; i < columns.length; i++) {
          if (active.includes(i)) {
            visible_columns.push(columns[i]);
          }
        }

        data_table.columns = visible_columns;  // Update DataTable's columns
    """)
    checkbox_group.js_on_change("active", check_callback)

    radio_labels = fields + ["NONE"]
    radio_group = RadioGroup(labels=radio_labels, active=len(radio_labels) - 1)
    radio_callback = CustomJS(args=dict(labels=radio_labels,
                                        data_table=data_table, columns=columns,
                                        node_source=network_graph.node_renderer.data_source,
    ), code="""
        const active = cb_obj.active;  // Indices of selected checkboxes
        const label = labels[active];
        console.log(label);
        if (label === "NONE") {
          // XXX: Need to de-select all and when unselected, go back to this
          return;
        }

        const n_data = node_source.data;
        const values = n_data[label];
        const colors = n_data['color'];

        // Determine min and max of the node attribute
        const minVal = Math.min(...values);
        const maxVal = Math.max(...values);

        // Define a Viridis256 color palette (you can replace this with other palettes)
        const palette = [
            '#440154', '#481567', '#482677', '#453781', '#404788', '#39568c', '#33638d', '#2d708e',
            '#287d8e', '#238a8d', '#1f968b', '#20a387', '#29af7f', '#3cbc75', '#55c667', '#73d055',
            '#95d840', '#b8de29', '#dce319', '#fde725'
        ];

        // Map each value to a color based on its normalized position
        for (let i = 0; i < values.length; i++) {
            const normalized = (values[i] - minVal) / (maxVal - minVal); // Normalize to [0, 1]
            const paletteIndex = Math.floor(normalized * (palette.length - 1)); // Map to palette index
            colors[i] = palette[paletteIndex]; // Assign color
        }

        // Trigger the update
        node_source.change.emit();
    """)
    radio_group.js_on_change("active", radio_callback)

    hover = HoverTool(tooltips=[
        ("Name", "@index"),
        ("Class", "@node_class"),
        ("num_descendants", "@num_descendants"),
        ("num_ancestors", "@num_ancestors"),
        ("node_duration_s", "@node_duration_s"),
        ("group_duration_s", "@group_duration_s"),
        ("node_probability_cache_hit", "@node_probability_cache_hit"),
        ("group_probability_cache_hit", "@group_probability_cache_hit"),
        ("expected_duration_s", "@expected_duration_s"),
    ])
    plot.add_tools(hover)


    # Don't let selection overwrite our properties
    network_graph.node_renderer.selection_glyph = None
    network_graph.node_renderer.nonselection_glyph = None
    network_graph.edge_renderer.selection_glyph = None
    network_graph.edge_renderer.nonselection_glyph = None
    # Add visual properties to the graph
    network_graph.node_renderer.glyph = Circle(radius=150,
                                               fill_color="skyblue",
                                               # line_color="skyblue",
                                               )
    network_graph.edge_renderer.glyph = MultiLine(line_color="gray", line_alpha=0.5, line_width=1)

    network_graph.node_renderer.glyph.update(fill_color="color",
                                             fill_alpha="alpha",
                                             # This allows us to hide completely
                                             line_alpha="alpha",
                                             )
    network_graph.edge_renderer.glyph.update(line_color="line_color", line_alpha="alpha")
    plot.renderers.append(network_graph)

    # Precompute ancestors and descendants
    label_to_index = {n: i for i, n in enumerate(graph.nodes)}
    ancestors = {index: list(label_to_index[l] for l in networkx.ancestors(graph, node)) for index, node in enumerate(graph.nodes)}
    descendants = {index: list(label_to_index[l] for l in networkx.descendants(graph, node)) for index, node in enumerate(graph.nodes)}

    # JavaScript callback for interactivity
    # XXX: Likely define the type of the input graph a little better, TypedDict
    callback = CustomJS(
        args=dict(graph_renderer=network_graph,
                  ancestors=ancestors,
                  descendants=descendants,
                  label_to_index=label_to_index,
                  ),
        code="""
        const selected_index = graph_renderer.node_renderer.data_source.selected.indices[0];
        const node_data = graph_renderer.node_renderer.data_source.data;
        const edge_data = graph_renderer.edge_renderer.data_source.data;
        if (selected_index !== undefined) {
            const selected_ancestors = ancestors.get(selected_index);
            const selected_descendants = descendants.get(selected_index);
            const subgraph_nodes = new Set([[selected_index], selected_ancestors, selected_descendants].flat());
            const ancestor_nodes = new Set(selected_ancestors);
            const descendant_nodes = new Set(selected_descendants);

            for (let i = 0; i < node_data['Highlight'].length; i++) {
                node_data['Highlight'][i] = (i === selected_index) ? "Yes" : "No";
                var color = "skyblue";
                if (i === selected_index) {
                  color = "skyblue";
                } else if (ancestor_nodes.has(i)) {
                  color = "orange";
                } else if (descendant_nodes.has(i)) {
                  color = "gold";
                } else {
                  color = "skyblue";
                }
                node_data['color'][i] = color;
                node_data['alpha'][i] = subgraph_nodes.has(i) ? 1.0 : 0.0;
            }

            for (let i = 0; i < edge_data['start'].length; i++) {
                const edge_start = label_to_index[edge_data['start'][i]];
                const edge_end = label_to_index[edge_data['end'][i]];
                const in_subgraph = subgraph_nodes.has(edge_start) && subgraph_nodes.has(edge_end);
                edge_data['alpha'][i] = in_subgraph ? 1.0 : 0.0;
            }
        } else {
            for (let i = 0; i < node_data['Highlight'].length; i++) {
                node_data['color'][i] = "skyblue";
                node_data['alpha'][i] = 1.0;
            }
            for (let i = 0; i < edge_data['start'].length; i++) {
                edge_data['alpha'][i] = 1.0;
            }
        }
        graph_renderer.node_renderer.data_source.change.emit();
        graph_renderer.edge_renderer.data_source.change.emit();
    """
    )
    network_graph.node_renderer.data_source.selected.js_on_change("indices", callback)


    # Combine the plot and table into a Panel layout
    layout = pn.Column(
        pn.Row(pn.pane.Bokeh(plot), pn.pane.Bokeh(data_table)),
        pn.Row(pn.pane.Bokeh(checkbox_group), pn.pane.Bokeh(radio_group)),
    )
    return layout
