"""Parse bazel query outputs

A larger system description:
- inputs:
  - bazel query //... --ouput proto > query_result.pb
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
from bokeh.models import ColumnDataSource, MultiLine, Circle, CustomJS, TapTool
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
    rule_name: str
    rule_class: str
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
        'rule_name',
        'rule_class',
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


def dependency_analysis(
    query_result: build_pb2.QueryResult, ignore_external: bool,
    repo_dir: pathlib.Path, git_query_after: datetime.datetime,
    bep_path: pathlib.Path,
) -> tuple[networkx.DiGraph, list[Node]]:
    """Analyze the dependencies that we're getting to understand them."""
    # Get execution times
    with bep_path.open('rb') as bep_buf:
        node_duration = bep_reader.get_label_to_runtime(bep_buf)
        node_duration_s = {label: dt.total_seconds()
                           for label, dt in node_duration.items()}

    # Get FileCommitMap
    file_commit_map = git_utils.get_file_commit_map_from_follow(
        git_directory=repo_dir,
        after=git_query_after)
    bazel_intermediates = _normalize_paths_to_bazel_intermediates(file_commit_map.file_map.keys())

    # Get rules and graph
    rules = _get_rules(query_result)
    graph = get_dependency_digraph(rules, ignore_external=ignore_external)

    # XXX: Test case with BUILD further up, ensure we still get the right match
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
    group_probability = graph_algorithms.compute_group_probability(
        graph=graph,
        node_probability=node_probability)

    group_duration = graph_algorithms.compute_group_duration(
        graph=graph,
        node_duration_s=node_duration_s)

    # XXX: Setup cli arguments and overall workflow

    logger.debug(f"nodes: {len(graph.nodes)}")
    logger.debug(f"edges: {len(graph.edges)}")
    logger.debug(f"rules: {len(rules)}")

    pagerank = networkx.pagerank(graph)
    hubs, authorities = networkx.hits(graph)

    writer = csv.DictWriter(sys.stdout, fieldnames=get_node_field_names())
    writer.writeheader()
    rule_and_class: list[tuple[str, str]] = []
    for rule_name, rule in rules.items():
        rule_and_class.append((rule_name, rule.rule_class))
    # Probably want the source files too
    for bazel_src in node_probability.keys():
        rule_and_class.append((bazel_src, 'source_file'))
    nodes: list[Node] = []
    for rule_name, rule_class in rule_and_class:
        try:
            num_parents = len(list(graph.predecessors(rule_name)))
            num_children = len(list(graph.successors(rule_name)))
            num_ancestors = len(list(networkx.ancestors(graph, rule_name)))
            num_descendants = len(list(networkx.descendants(graph, rule_name)))
            gp = group_probability.get(rule_name, 1.0)
            gd = group_duration.get(rule_name, 0)
            row: Node = {
                "rule_name": rule_name,
                "rule_class": rule_class,
                "num_parents": num_parents,
                "num_ancestors": num_ancestors,
                "num_children": num_children,
                "num_descendants": num_descendants,
                "pagerank": pagerank[rule_name],
                "hubs_metric": hubs[rule_name],
                "authorities_metric": authorities[rule_name],
                "node_duration_s": node_duration_s.get(rule_name, 0),
                # XXX: determine_main is getting the attribution, but not the
                # main library, etc. not sure
                "group_duration_s": gd,
                "expected_duration_s": gd * (1 - gp),
                "node_probability_cache_hit": node_probability.get(rule_name, 1.0),
                "group_probability_cache_hit": gp,
            }
            nodes.append(row)
            writer.writerow(row)

        except networkx.NetworkXError as e:
            raise AssertionError(f"Exception with {rule_name}") from e
    # Temporary way to export
    networkx.write_gml(graph, "/tmp/my.gml")
    return graph, nodes


def run_bokeh(graph: networkx.DiGraph, nodes: list[Node]) -> None:
    # Prepare data for the table
    # XXX: Hook up nodes
    node_data = {
        "Node": [f"Node {i}" for i in graph.nodes],
        "Highlight": ["No" for _ in graph.nodes],
    }

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
    # XXX: probably just make pos
    network_graph = from_networkx(graph, nx_agraph.graphviz_layout, prog='dot')  # type: ignore

    # Add visual properties to the graph
    network_graph.node_renderer.glyph = Circle(radius=5, fill_color="skyblue")
    network_graph.edge_renderer.glyph = MultiLine(line_color="gray", line_alpha=0.5, line_width=1)
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
    """
    )
    # Callback for clicking a row (table -> graph)
    table_to_graph_callback = CustomJS(
        args=dict(source=source, graph_renderer=network_graph),
        code="""
        const selected_index = cb_obj.indices[0];
        if (selected_index !== undefined) {
            graph_renderer.node_renderer.data_source.selected.indices = [selected_index];
        }
    """
    )

    network_graph.node_renderer.data_source.selected.js_on_change("indices", callback)
    source.selected.js_on_change("indices", table_to_graph_callback)


    # Create a DataTable to view source
    columns = [TableColumn(field=k, title=k) for k in node_data.keys()]
    data_table = DataTable(source=source, columns=columns, width=400, height=800)

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
    git_query_after = datetime.datetime.now() - datetime.timedelta(days=2100) # XXX
    bep_path = repo_dir / 'test_all.pb'
    graph, nodes = dependency_analysis(query_result, ignore_external=True, repo_dir=repo_dir,
                                       git_query_after=git_query_after, bep_path=bep_path)
    run_bokeh(graph=graph, nodes=nodes)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    main()
