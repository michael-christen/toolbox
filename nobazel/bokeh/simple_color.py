import networkx as nx
import random
from bokeh.plotting import figure, show
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.io import curdoc
from bokeh.models.graphs import NodesAndLinkedEdges
from bokeh.plotting import from_networkx

# Create a NetworkX graph
G = nx.erdos_renyi_graph(10, 0.3)

# Define a color palette
colors = ["red", "green", "blue", "orange", "purple", "pink", "yellow"]

# Add a random color attribute to each node
for node in G.nodes:
    G.nodes[node]["color"] = random.choice(colors)

# Create a Bokeh plot
plot = figure(title="Interactive Network Graph", x_range=(-1.5, 1.5), y_range=(-1.5, 1.5),
              tools="tap", tooltips="Node: @index")

# Convert NetworkX graph to a Bokeh graph
graph = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))

# Add node attributes to the graph's data source
node_renderer = graph.node_renderer
node_renderer.data_source.data["color"] = [G.nodes[node]["color"] for node in G.nodes]

# Set node properties
node_renderer.glyph.size = 15
node_renderer.glyph.fill_color = "color"

# Define a callback to randomly change node colors on click
callback = CustomJS(args=dict(source=node_renderer.data_source, colors=colors), code="""
    const data = source.data;
    const color_list = colors;
    for (let i = 0; i < data['color'].length; i++) {
        data['color'][i] = color_list[Math.floor(Math.random() * color_list.length)];
    }
    source.change.emit();
""")

# Add the callback to the plot
plot.js_on_event('tap', callback)

# Add the graph to the plot
plot.renderers.append(graph)

# Show the plot
show(plot)
