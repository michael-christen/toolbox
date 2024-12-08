"""Parse bazel query outputs

A larger system description:
- inputs:
  - bazel query //... --output proto > query_result.pb
    - the full dependency tree
  - bazel test //... --build_event_binary_file=test_all.pb
    - bazel run //utils:bep_reader < test_all.pb
    - the execution time related to each test target
  - git_utils.get_file_commit_map_from_follow
    - how files have changed over time, can be used to generate
      probabilities of files changing in the future
- intermediates:
  - representation for source files and bazel together
- outputs:
  - test targets:
    - likelihood of executing
      - expected value of runtime
  - source files:
    - cost in execution time of modification
    - expected cost of file change (based on probability of change * cost)
  - graph with the values above, we could take any set of file inputs and
    describe cost
  - graph that we could identify overly depended upon things
"""
import csv
import datetime
import logging
import pathlib
import sys
from typing import TypedDict

import networkx

from third_party.bazel.src.main.protobuf import build_pb2
from tools import bazel_utils
from tools import git_utils
from utils import bep_reader
from utils import graph_algorithms

logger = logging.getLogger(__name__)

from networkx.drawing import nx_agraph
from bokeh.models import ColumnDataSource, MultiLine, Circle, CustomJS, TapTool, HoverTool
from bokeh.plotting import figure, from_networkx
from bokeh.layouts import column
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.io import show
import panel as pn


def _get_rules(
    query_result: build_pb2.QueryResult
) -> dict[str, build_pb2.Rule]:
    """Get rules by name"""
    rules = {}

    for i, target in enumerate(query_result.target):
        type_name = build_pb2.Target.Discriminator.Name(target.type)
        if target.type == build_pb2.Target.RULE:
            pass
        elif target.type in {
            build_pb2.Target.SOURCE_FILE,
            build_pb2.Target.GENERATED_FILE,
            build_pb2.Target.PACKAGE_GROUP,
            build_pb2.Target.ENVIRONMENT_GROUP,
        }:
            logger.debug(f"{i}, {type_name}")
            continue
        else:
            raise ValueError(
                f"Invalid target type: {type_name}({target.type})"
            )
        # We are a rule type now
        rule = target.rule

        logger.debug(f"{rule.name}({rule.rule_class})")
        # Didn't see much use with these:
        # - rule.configured_rule_input
        # - rule.default_setting
        rules[rule.name] = rule

    return rules


def get_dependency_digraph(
    rules: dict[str, build_pb2.Rule], ignore_external: bool
) -> networkx.DiGraph:
    graph = networkx.DiGraph()
    for rule in rules.values():
        # Specify X depends on Y as X is a parent of Y
        for rule_input in rule.rule_input:
            if ignore_external and rule_input.startswith("@"):
                continue
            graph.add_edge(rule.name, rule_input)
        for output in rule.rule_output:
            graph.add_edge(output, rule.name)
        # Still add this to the graph, even if no edges
        if not graph.has_node(rule.name):
            graph.add_node(rule.name)
    return graph


def _normalize_paths_to_bazel_intermediates(
        files: list[pathlib.Path]) -> dict[str, pathlib.Path]:
    normalized_map = {}
    for f in files:
        normalized = f'//{f}'
        normalized_map[normalized] = f
    return normalized_map


def _normalize_bazel_target_to_intermediate(target: str) -> str:
    return target.replace(':', '/')


class Node(TypedDict):
    node_name: str
    node_class: str
    num_parents: int
    num_ancestors: int
    num_children: int
    num_descendants: int
    pagerank: float
    hubs_metric: float
    authorities_metric: float
    node_duration_s: float
    group_duration_s: float
    expected_duration_s: float
    node_probability_cache_hit: float
    group_probability_cache_hit: float
    # Keep in sync with get_node_field_names


def get_node_field_names() -> list[str]:
    """Get ordered list of field names to display.

    Keep in sync with Node
    """
    return [
        'node_name',
        'node_class',
        'num_parents',
        'num_ancestors',
        'num_children',
        'num_descendants',
        'pagerank',
        'hubs_metric',
        'authorities_metric',
        'node_duration_s',
        'group_duration_s',
        'expected_duration_s',
        'node_probability_cache_hit',
        'group_probability_cache_hit',
    ]


def _get_node_probability(
    graph: networkx.DiGraph,
    file_commit_map: git_utils.FileCommitMap,
) -> dict[str, float]:
    # XXX: Test case with BUILD further up, ensure we still get the right match
    bazel_intermediates = _normalize_paths_to_bazel_intermediates(file_commit_map.file_map.keys())
    bazel_src_target_to_file = {}
    for node in graph.nodes:
        src_path = bazel_intermediates.get(
            _normalize_bazel_target_to_intermediate(node))
        if src_path is not None:
            bazel_src_target_to_file[node] = src_path

    node_probability = {}
    total_commits = len(file_commit_map.commit_map)
    for node, f in bazel_src_target_to_file.items():
        node_probability[node] = 1 - (len(file_commit_map.file_map[f]) /
                                      total_commits)
    return node_probability


def dependency_analysis(
    node_to_class: dict[str, str],
    graph: networkx.DiGraph,
    node_probability: dict[str, float],
    node_duration_s: dict[str, float],
) -> dict[str, Node]:
    """Analyze the dependencies that we're getting to understand them."""

    group_probability = graph_algorithms.compute_group_probability(
        graph=graph,
        node_probability=node_probability)

    group_duration = graph_algorithms.compute_group_duration(
        graph=graph,
        node_duration_s=node_duration_s)

    pagerank = networkx.pagerank(graph)
    hubs, authorities = networkx.hits(graph)
    # XXX: Should we have a data structure that's just a big collection of
    # components
    # - use cases:
    #  - dictionary of node-specific info for js callbacks
    #  - set of lists / DataFrame for csv or DataSource

    # XXX: Setup cli arguments and overall workflow

    logger.debug(f"nodes: {len(graph.nodes)}")
    logger.debug(f"edges: {len(graph.edges)}")
    # XXX: Show graph density

    writer = csv.DictWriter(sys.stdout, fieldnames=get_node_field_names())
    writer.writeheader()


    nodes: dict[str, Node] = {}
    for node_name, node_class in node_to_class.items():
        try:
            num_parents = len(list(graph.predecessors(node_name)))
            num_children = len(list(graph.successors(node_name)))
            num_ancestors = len(list(networkx.ancestors(graph, node_name)))
            num_descendants = len(list(networkx.descendants(graph, node_name)))
            gp = group_probability.get(node_name, 1.0)
            gd = group_duration.get(node_name, 0)
            row: Node = {
                "node_name": node_name,
                "node_class": node_class,
                "num_parents": num_parents,
                "num_ancestors": num_ancestors,
                "num_children": num_children,
                "num_descendants": num_descendants,
                "pagerank": pagerank[node_name],
                "hubs_metric": hubs[node_name],
                "authorities_metric": authorities[node_name],
                "node_duration_s": node_duration_s.get(node_name, 0),
                # XXX: determine_main is getting the attribution, but not the
                # main library, etc. not sure
                "group_duration_s": gd,
                "expected_duration_s": gd * (1 - gp),
                "node_probability_cache_hit": node_probability.get(node_name, 1.0),
                "group_probability_cache_hit": gp,
            }
            nodes[node_name] = row
            writer.writerow(row)

        except networkx.NetworkXError as e:
            raise AssertionError(f"Exception with {node_name}") from e
    # Temporary way to export
    networkx.write_gml(graph, "/tmp/my.gml")
    return nodes


def run_bokeh(graph: networkx.DiGraph, nodes: dict[str, Node]) -> None:
    # Prepare data for the table
    # XXX: Hook up nodes
    node_data = {
        "Node": [n for n in nodes],
        "Highlight": ["No" for _ in nodes],
        "num_descendants": [v['num_descendants'] for v in nodes.values()],
    }
    # XXX: Apply Node information to graph
    for name, node in nodes.items():
        for k, v in node.items():
            graph.nodes[name][k] = v

    # Initialize Panel for interactive layout
    pn.extension()
    layout = get_panel_layout(graph=graph, node_data=node_data)
    pn.serve(layout)


def get_panel_layout(graph: networkx.DiGraph, node_data: dict[str, list[str]]
                     ) -> pn.layout.base.Panel:
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
    plot = figure(width=800, height=800,
                  tools="tap,box_zoom,wheel_zoom,reset,pan",
                  active_scroll="wheel_zoom",
                  title="Network Graph")
    plot.axis.visible = True
    # XXX: probably just make pos
    network_graph = from_networkx(graph, nx_agraph.graphviz_layout, prog='dot')  # type: ignore
    # Node
    network_graph.node_renderer.data_source.data['color'] = ['skyblue'] * len(graph.nodes)
    network_graph.node_renderer.data_source.data['alpha'] = [1.0] * len(graph.nodes)
    # Edge
    network_graph.edge_renderer.data_source.data['line_color'] = ['gray' for edge in graph.edges]
    network_graph.edge_renderer.data_source.data['alpha'] = [1.0] * len(graph.edges)

    hover = HoverTool(tooltips=[
        ("Node", "@index"),
        ("Name", "@node_name"),
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

    source = ColumnDataSource(node_data)

    # Precompute ancestors and descendants
    label_to_index = {n: i for i, n in enumerate(graph.nodes)}
    ancestors = {index: list(label_to_index[l] for l in networkx.ancestors(graph, node)) for index, node in enumerate(graph.nodes)}
    descendants = {index: list(label_to_index[l] for l in networkx.descendants(graph, node)) for index, node in enumerate(graph.nodes)}

    # JavaScript callback for interactivity
    # XXX: Likely define the type of the input graph a little better, TypedDict
    callback = CustomJS(
        args=dict(source=source,
                  graph_renderer=network_graph,
                  ancestors=ancestors,
                  descendants=descendants,
                  label_to_index=label_to_index,
                  ),
        code="""
        const selected_index = graph_renderer.node_renderer.data_source.selected.indices[0];
        const data = source.data;
        const node_data = graph_renderer.node_renderer.data_source.data;
        const edge_data = graph_renderer.edge_renderer.data_source.data;
        if (selected_index !== undefined) {
            const selected_ancestors = ancestors.get(selected_index);
            const selected_descendants = descendants.get(selected_index);
            const subgraph_nodes = new Set([[selected_index], selected_ancestors, selected_descendants].flat());
            const ancestor_nodes = new Set(selected_ancestors);
            const descendant_nodes = new Set(selected_descendants);

            for (let i = 0; i < data['Highlight'].length; i++) {
                data['Highlight'][i] = (i === selected_index) ? "Yes" : "No";
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

            console.log(subgraph_nodes);
            for (let i = 0; i < edge_data['start'].length; i++) {
                const edge_start = label_to_index[edge_data['start'][i]];
                const edge_end = label_to_index[edge_data['end'][i]];
                const in_subgraph = subgraph_nodes.has(edge_start) && subgraph_nodes.has(edge_end);
                console.log(edge_start);
                console.log(edge_end);
                console.log(in_subgraph);
                edge_data['alpha'][i] = in_subgraph ? 1.0 : 0.0;
            }
        } else {
            for (let i = 0; i < data['Highlight'].length; i++) {
                node_data['color'][i] = "skyblue";
                node_data['alpha'][i] = 1.0;
            }
            for (let i = 0; i < edge_data['start'].length; i++) {
                edge_data['alpha'][i] = 1.0;
            }
        }
        source.change.emit();
        graph_renderer.node_renderer.data_source.change.emit();
        graph_renderer.edge_renderer.data_source.change.emit();
    """
    )
    # XXX: The color change is only happening after the graph is manually
    # adjusted (eg, zooming in / out)
    # Callback for clicking a row (table -> graph)
    table_to_graph_callback = CustomJS(
        args=dict(source=source, graph_renderer=network_graph),
        code="""
        const selected_index = cb_obj.indices[0];
        console.log("Index: " + selected_index);
        if (selected_index !== undefined) {
            graph_renderer.node_renderer.data_source.selected.indices = [selected_index];
        }
    """
    )

    network_graph.node_renderer.data_source.selected.js_on_change("indices", callback)
    source.selected.js_on_change("indices", table_to_graph_callback)


    # Create a DataTable to view source
    # XXX: This and graph are disagreeing :scream:
    columns = [TableColumn(field=k, title=k) for k in node_data.keys()]
    data_table = DataTable(source=source, columns=columns, width=800, height=800)

    # Combine the plot and table into a Panel layout
    layout = pn.Row(pn.pane.Bokeh(plot), pn.pane.Bokeh(data_table))
    return layout


# def draw():
#     import matplotlib.pyplot as plt
#     from networkx.drawing import nx_agraph
#     import networkx as nx
#
#     g = nx.read_gml('/tmp/my.gml')
#     pos = nx_agraph.graphviz_layout(g, prog='dot')
#     nx.draw(g, pos, with_labels=True, arrows=True)
#     plt.show()


def main():
    query_result = bazel_utils.parse_build_output(sys.stdin.buffer.read())
    with open("/tmp/my.prototxt", "w") as f:
        f.write(str(query_result))
    repo_dir = pathlib.Path('/home/mchristen/devel/toolbox')  # XXX
    git_query_after = datetime.datetime.now() - datetime.timedelta(days=2) # XXX
    file_commit_map = git_utils.get_file_commit_map_from_follow(
        git_directory=repo_dir,
        after=git_query_after)
    # Get execution times
    bep_path = repo_dir / 'test_all.pb'
    with bep_path.open('rb') as bep_buf:
        node_duration = bep_reader.get_label_to_runtime(bep_buf)
        node_duration_s = {label: dt.total_seconds()
                           for label, dt in node_duration.items()}
    # Get rules and graph
    rules = _get_rules(query_result)
    graph = get_dependency_digraph(rules, ignore_external=True)
    node_probability = _get_node_probability(graph=graph,
                                             file_commit_map=file_commit_map)

    node_to_class: dict[str, str] = {}
    # Gotta make table for all, in a consistent order, otherwise table, etc. won't line up:
    # XXX: (not) Select which nodes to view
    for node_name in graph.nodes:
        node_rule = rules.get(node_name)
        if node_name in node_probability:
            # Probably want the source files too
            node_to_class[node_name] = 'source_file'
        elif node_rule:
            node_to_class[node_name] = node_rule.rule_class
        else:
            node_to_class[node_name] = 'unknown'

    nodes = dependency_analysis(node_to_class=node_to_class,
                                graph=graph,
                                node_duration_s=node_duration_s,
                                node_probability=node_probability,
                                )
    run_bokeh(graph=graph, nodes=nodes)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    main()
