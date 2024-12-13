import networkx as nx
from bokeh.plotting import figure, show, from_networkx
from bokeh.models import ColumnDataSource, CustomJS, Button
from bokeh.layouts import column

# Create a sample graph
G = nx.karate_club_graph()

# Add custom attributes
for node in G.nodes:
    G.nodes[node]['group'] = node % 3

for edge in G.edges:
    G.edges[edge]['weight'] = edge[0] % 2

# Set up the Bokeh plot
plot = figure(title="Interactive NetworkX Graph",
              x_range=(-1.5, 1.5), y_range=(-1.5, 1.5),
              width=800, height=800)

# Convert NetworkX graph to Bokeh
graph_renderer = from_networkx(G, nx.spring_layout)

# Customize initial node and edge appearances
node_colors = {0: "red", 1: "green", 2: "blue"}
graph_renderer.node_renderer.data_source.data['color'] = [
    node_colors[G.nodes[node]['group']] for node in G.nodes
]

edge_colors = ["black", "gray"]
graph_renderer.edge_renderer.data_source.data['line_color'] = [
    edge_colors[G.edges[edge]['weight']] for edge in G.edges
]

# Set visual properties using the ColumnDataSource data
graph_renderer.node_renderer.glyph.update(fill_color="color")
graph_renderer.edge_renderer.glyph.update(line_color="line_color")

# Add graph to plot
plot.renderers.append(graph_renderer)

# Add a button to toggle visibility
button = Button(label="Toggle Colors", button_type="success")

# JavaScript callback
callback = CustomJS(args=dict(node_source=graph_renderer.node_renderer.data_source,
                              edge_source=graph_renderer.edge_renderer.data_source),
                    code="""
    // Access the data sources
    let node_data = node_source.data;
    let edge_data = edge_source.data;

    // Modify node colors
    for (let i = 0; i < node_data['color'].length; i++) {
        node_data['color'][i] = node_data['color'][i] === 'red' ? 'blue' : 'red';
    }

    // Modify edge colors
    for (let i = 0; i < edge_data['line_color'].length; i++) {
        edge_data['line_color'][i] = edge_data['line_color'][i] === 'black' ? 'gray' : 'black';
    }

    // Emit changes
    node_source.change.emit();
    edge_source.change.emit();
""")
button.js_on_click(callback)

# Display the plot with the button
layout = column(plot, button)
show(layout)
