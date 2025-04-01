r"""Parse bazel query outputs

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

XXX:
 - bazel query --keep_going --noimplicit_deps --output proto "deps(//...)"
   is much bigger than "//..." alone, compare what the differences are
- git log --since="10 years ago" --name-only --pretty=format: | sort \
        | uniq -c | sort -nr
  - this is much faster
  - could identify renames via:
    - git log --since="1 month ago" --name-status --pretty=format: \
            | grep -P 'R[0-9]*\t' | awk '{print $2, "->", $3}'
    - then correct
    - can get commit association via
      - git log --since="1 month ago" --name-status --pretty=format:"%H"
    - statuses are A,M,D,R\d\d\d
```
# Regex pattern to match the git log output
pattern = r"^([AMD])\s+(.+?)(\s*->\s*(.+))?$|^R(\d+)\s+(.+?)\s*->\s*(.+)$"
# Parse each line using the regex
for line in git_log_output.strip().split('\n'):
    match = re.match(pattern, line.strip())
    if match:
        if match.group(1):  # For A, M, D statuses
            change_type = match.group(1)
            old_file = match.group(2)
            new_file = match.group(4) if match.group(4) else None
            print(f"Change type: {change_type}, Old file: {old_file}, "
                  f"New file: {new_file}")
        elif match.group(5):  # For R status (renames)
            change_type = 'R'
            similarity_index = match.group(5)
            old_file = match.group(6)
            new_file = match.group(7)
            print(f"Change type: {change_type}, Similarity index:"
                  f" {similarity_index}, Old file: {old_file}, New file:"
                  f" {new_file}")
```

Example Script:

repo_dir=`pwd`
file_commit_pb=$repo_dir/file_commit.pb
query_pb=$repo_dir/s_result.pb
bep_pb=$repo_dir/test_all.pb
out_gml=$repo_dir/my.gml
out_csv=$repo_dir/my.csv
out_html=$repo_dir/my.html

# Prepare data
bazel query "//... - //docs/... - //third_party/bazel/..." --output proto \
        > $query_pb
bazel test //... --build_event_binary_file=$bep_pb
bazel run //apps/bazel_parser --output_groups=-mypy -- git-capture --repo-dir \
        $repo_dir --days-ago 400 --file-commit-pb $file_commit_pb
# Separate step if we want build timing data
bazel clean
bazel build --noremote_accept_cached \
    --experimental_execution_log_compact_file=exec_log.pb.zst \
    --generate_json_trace_profile --profile=example_profile_new.json \
    //...
# Would then need to process the exec_log.pb.zst file to get timing from it and
# then add to the other timing information

# Process and visualize the data
bazel run //apps/bazel_parser --output_groups=-mypy -- process \
        --file-commit-pb $file_commit_pb --query-pb $query_pb --bep-pb \
        $bep_pb --out-gml $out_gml --out-csv $out_csv
bazel run //apps/bazel_parser --output_groups=-mypy -- visualize \
        --gml $out_gml --out-html $out_html
"""

import csv
import dataclasses
import datetime
import logging
import pathlib
import sys
from typing import TypedDict

import click
import networkx

from apps.bazel_parser import panel
from third_party.bazel.src.main.protobuf import build_pb2
from tools import bazel_utils
from tools import git_pb2
from tools import git_utils
from utils import bep_reader
from utils import graph_algorithms

logger = logging.getLogger(__name__)

PATH_TYPE = click.Path(exists=True, path_type=pathlib.Path)
OUT_PATH_TYPE = click.Path(exists=False, path_type=pathlib.Path)


def _get_rules(
    query_result: build_pb2.QueryResult,
) -> dict[str, build_pb2.Rule]:
    """Get rules by name"""
    rules = {}

    for i, target in enumerate(query_result.target):
        type_name = build_pb2.Target.Discriminator.Name(target.type)  # type: ignore
        if target.type == build_pb2.Target.RULE:
            pass
        elif target.type in {
            build_pb2.Target.SOURCE_FILE,
            build_pb2.Target.GENERATED_FILE,
            build_pb2.Target.PACKAGE_GROUP,
            build_pb2.Target.ENVIRONMENT_GROUP,
        }:
            # logger.debug(f"{i}, {type_name}")
            # XXX: Should we allow SOURCE_FILE?
            continue
        else:
            raise ValueError(
                f"Invalid target type: {type_name}({target.type})"
            )
        # We are a rule type now
        rule = target.rule

        # logger.debug(f"{rule.name}({rule.rule_class})")
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
    files: list[pathlib.Path],
) -> dict[str, pathlib.Path]:
    normalized_map = {}
    for f in files:
        normalized = f"//{f}"
        normalized_map[normalized] = f
    return normalized_map


def _normalize_bazel_target_to_intermediate(target: str) -> str:
    if target.startswith("//:"):
        return target.replace(":", "")
    else:
        return target.replace(":", "/")


class GraphMetrics(TypedDict):
    """Graph-wide metrics.
    """
    max_depth: int
    # aka) order
    num_nodes: int
    # aka) size
    num_edges: int
    density: float
    diameter: int
    radius: int
    num_connected_components: int
    total_duration_s: float
    expected_duration_s: float
    probable_nodes_affected_per_change_by_node: float
    probable_nodes_affected_per_change_by_group: float

    # Proposal for new attributes
    # XXX: max/aggregation of most of the node attributes


class Node(TypedDict):
    """The fields of a given node.

    These can be used as columns of panda dataframes
    """

    # The bazel label
    node_name: str
    # The class of the rule, eg. java_library
    node_class: str

    # How many things depend on you, in_degree
    num_parents: int
    # Total number of nodes that transitively depend on you
    num_ancestors: int
    # Total number of nodes that transitively depend on you and have a defined
    # execution time (such as tests)
    num_duration_ancestors: int

    # How many things you depend on, out_degree
    num_children: int
    # Total number of nodes that you transitively depend on
    num_descendants: int
    # Total number of nodes that you transitively depend on and have a < 100%
    # chance of being cached
    num_source_descendants: int

    # ===== Link Analysis =====
    pagerank: float
    hubs_metric: float
    authorities_metric: float

    # ===== Node Specific =====
    # How long this node took to "execute"
    # - mostly capturing test time at the moment
    node_duration_s: float
    # (1 - (# of commits this file changed / Total # of commits))
    node_probability_cache_hit: float

    # ===== Accumulated   =====
    # Sum of ancestors' node durations + your own
    group_duration_s: float
    # node_probability_cache_hit * PRODUCT{descendants}
    # - This makes the simplifying assumption that all changes are independent
    # of one another, which isn't true, but convenient.
    group_probability_cache_hit: float
    # group_duration_s * (1 - group_probability_cache_hit)
    expected_duration_s: float

    # XXX: Move these back and add them where necessarry
    # ==== New =====
    # Max ancestor depth from this node
    # - The max shortest path of this node in a reversed graph
    ancestor_depth: int
    # ancestor_depth, but descendant
    # - The max shortest path of this node in a graph
    descendant_depth: int

    # A more node specific version of rebuilt_targets_by_transitive_dependencies
    # XXX: May not be too helpful?
    # (1 - node_probability_cache_hit) * num_ancestors
    # > Score for how much changes to a single target affects others due to
    # > cache invalidations
    # > A high score means that you are a top cache invalidator in the graph.
    # > E.g. “ios_pill” that we saw in the beginning.
    # related to rebuilt_target
    ancestors_by_node_p: float

    # An unweighted version of expected_duration_s wrt duration
    # (1 - group_probability_cache_hit) * num_ancestors
    # > This can be interpreted as a score for bottleneck-ness, and captures
    # > how a single target act as a force multiplier of graph invalidations in
    # > the graph. This is an improved way to identify bottlenecks that could
    # > benefit from isolation and cutting off the dependencies between the
    # > upstream and downstream side.
    # related to rebuilt_targets_by_transitive_dependencies
    ancestors_by_group_p: float

    # An unweighted version of expected_duration_s wrt probability
    # num_descendants * num_ancestors
    ancestors_by_descendants: int

    # Betweenness centrality of a node is the sum of the fraction of all-pairs
    # shortest paths that pass through
    #
    # >
    # Related to this metric, an important centrality measure from the research
    # field of graph structures is “Betweenness centrality”.
    #
    # This is the fraction of all dependency chains between other targets that
    # passes through a single build target like A.
    #
    # This can be seen as a score for the broker-ness in the dependency network
    # and that could also benefit from isolation.
    betweenness_centrality: float

    # Closeness centrality of a node u is the reciprocal of the average
    # shortest path distance to u over all n-1 reachable nodes.
    closeness_centrality: float

    # Proposed new fields
    # - sum(num_ancestors + num_descendants), can get an idea of size of
    # sub-graph

def get_node_field_names() -> list[str]:
    """Get ordered list of field names to display.

    Keep in sync with Node
    """
    return [
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
        "node_probability_cache_hit",
        "group_duration_s",
        "group_probability_cache_hit",
        "expected_duration_s",
        "ancestor_depth",
        "descendant_depth",
        "ancestors_by_node_p",
        "ancestors_by_group_p",
        "ancestors_by_descendants",
        "betweenness_centrality",
        "closeness_centrality",
    ]


def _get_node_probability(
    graph: networkx.DiGraph,
    file_commit_map: git_utils.FileCommitMap,
) -> dict[str, float]:
    # XXX: Test case with BUILD further up, ensure we still get the right match
    bazel_intermediates = _normalize_paths_to_bazel_intermediates(
        list(file_commit_map.file_map.keys())
    )
    bazel_src_target_to_file = {}
    for node in graph.nodes:
        src_path = bazel_intermediates.get(
            _normalize_bazel_target_to_intermediate(node)
        )
        if src_path is not None:
            bazel_src_target_to_file[node] = src_path

    node_probability = {}
    total_commits = len(file_commit_map.commit_map)
    for node, f in bazel_src_target_to_file.items():
        node_probability[node] = 1 - (
            len(file_commit_map.file_map[f]) / total_commits
        )
    return node_probability


def get_graph_metrics(
    graph: networkx.DiGraph,
    node_probability: dict[str, float],
    node_duration_s: dict[str, float],
) -> GraphMetrics:
    weakly_connected_components = networkx.weakly_connected_components(graph)
    # XXX: Maybe we should remove weakly connected components < some threshold
    # size
    NODE_THRESHOLD = 10
    max_diameter = 0
    max_radius = 0
    # XXX: Even this doesn't work ... since it expects strong connections
    # for c in weakly_connected_components:
    #     if len(c) < NODE_THRESHOLD:
    #         continue
    #     subgraph = graph.subgraph(c)
    #     diameter = networkx.diameter(subgraph)
    #     radius = networkx.radius(subgraph)
    #     if diameter > max_diameter:
    #         max_diameter = diameter
    #         max_radius = radius

    metrics: GraphMetrics = {
        # XXX: Compare to max of all nodes
        # XXX: we also want the max shortest path
        "max_depth": networkx.dag_longest_path_length(graph),
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "density": networkx.density(graph),
        "diameter": max_diameter,
        "radius": max_radius,
        "num_connected_components": networkx.number_weakly_connected_components(graph),
        # XXX: Add these later:
        # "total_duration_s": 0,
        # "expected_duration_s": 0,
        # "probable_nodes_affected_per_change_by_node": 0,
        # "probable_nodes_affected_per_change_by_group": 0,
    }
    return metrics


def dependency_analysis(
    node_to_class: dict[str, str],
    graph: networkx.DiGraph,
    node_probability: dict[str, float],
    node_duration_s: dict[str, float],
) -> dict[str, Node]:
    """Analyze the dependencies that we're getting to understand them."""

    group_probability = graph_algorithms.compute_group_probability(
        graph=graph, node_probability=node_probability
    )

    group_duration = graph_algorithms.compute_group_duration(
        graph=graph, node_duration_s=node_duration_s
    )

    pagerank = networkx.pagerank(graph)
    hubs, authorities = networkx.hits(graph)
    # XXX: Should we have a data structure that's just a big collection of
    # components
    # - use cases:
    #  - dictionary of node-specific info for js callbacks
    #  - set of lists / DataFrame for csv or DataSource

    # XXX: Setup cli arguments and overall workflow

    # logger.debug(f"nodes: {len(graph.nodes)}")
    # logger.debug(f"edges: {len(graph.edges)}")
    # XXX: Show graph density
    in_degree = graph.in_degree()
    out_degree = graph.out_degree()

    reversed_graph = graph.reverse()

    # Compute depths
    forward_all_pairs_shortest_path_length = (
        networkx.all_pairs_shortest_path_length(graph))
    reverse_all_pairs_shortest_path_length = (
        networkx.all_pairs_shortest_path_length(reversed_graph))
    descendant_depth: dict[str, int] = {}
    ancestor_depth: dict[str, int] = {}
    for node_name, pair_len_dict in (
            forward_all_pairs_shortest_path_length):
        descendant_depth[node_name] = max(pair_len_dict.values())
    for node_name, pair_len_dict in (
            reverse_all_pairs_shortest_path_length):
        ancestor_depth[node_name] = max(pair_len_dict.values())

    # Compute centrality metrics
    betweenness = networkx.betweenness_centrality(graph)
    closeness = networkx.closeness_centrality(graph)

    nodes: dict[str, Node] = {}
    for node_name, node_class in node_to_class.items():
        num_parents = in_degree[node_name]
        num_children = out_degree[node_name]
        ancestors = list(networkx.ancestors(graph, node_name))
        num_ancestors = len(ancestors)
        num_duration_ancestors = len(
            [a for a in ancestors if a in node_duration_s]
        )
        descendants = list(networkx.descendants(graph, node_name))
        num_descendants = len(descendants)
        num_source_descendants = len(
            [d for d in descendants if d in node_probability]
        )
        np = node_probability.get(node_name, 1.0)
        gp = group_probability.get(node_name, 1.0)
        gd = group_duration.get(node_name, 0)
        row: Node = {
            "node_name": node_name,
            "node_class": node_class,
            "num_parents": num_parents,
            "num_ancestors": num_ancestors,
            "num_duration_ancestors": num_duration_ancestors,
            "num_children": num_children,
            "num_descendants": num_descendants,
            "num_source_descendants": num_source_descendants,
            "pagerank": pagerank[node_name],
            "hubs_metric": hubs[node_name],
            "authorities_metric": authorities[node_name],
            "node_duration_s": node_duration_s.get(node_name, 0),
            # XXX: determine_main is getting the attribution, but not the
            # main library, etc. not sure
            "group_duration_s": gd,
            "expected_duration_s": gd * (1 - gp),
            "node_probability_cache_hit": np,
            "group_probability_cache_hit": gp,
            "ancestor_depth": ancestor_depth[node_name],
            "descendant_depth": descendant_depth[node_name],
            "ancestors_by_node_p": num_ancestors * (1 - np),
            "ancestors_by_group_p": num_ancestors * (1 - gp),
            "ancestors_by_descendants":
            num_ancestors * num_descendants,
            "betweenness_centrality":
            betweenness[node_name],
            "closeness_centrality":
            closeness[node_name],
        }
        nodes[node_name] = row
    return nodes


@click.group()
def cli():
    pass


@click.command()
@click.option("--repo-dir", type=PATH_TYPE, required=True)
@click.option("--days-ago", type=int, required=True)
@click.option("--file-commit-pb", type=OUT_PATH_TYPE, required=True)
def git_capture(
    repo_dir: pathlib.Path,
    days_ago: int,
    file_commit_pb: pathlib.Path,
) -> None:
    git_query_after = datetime.datetime.now() - datetime.timedelta(
        days=days_ago
    )
    file_commit_map = git_utils.get_file_commit_map_from_follow(
        git_directory=repo_dir, after=git_query_after
    )
    file_commit_pb.write_bytes(
        file_commit_map.to_proto().SerializeToString(deterministic=True)
    )


@click.command()
@click.option("--query-pb", type=PATH_TYPE, required=True)
@click.option("--bep-pb", type=PATH_TYPE, required=True)
@click.option("--file-commit-pb", type=PATH_TYPE, required=True)
@click.option("--out-gml", type=OUT_PATH_TYPE, required=True)
@click.option("--out-csv", type=OUT_PATH_TYPE, required=True)
def process(
    query_pb: pathlib.Path,
    bep_pb: pathlib.Path,
    file_commit_pb: pathlib.Path,
    out_gml: pathlib.Path,
    out_csv: pathlib.Path,
) -> None:
    # Get query result
    query_result = bazel_utils.parse_build_output(query_pb.read_bytes())

    # Get file commit map
    file_commit_proto = git_pb2.FileCommitMap()
    file_commit_proto.ParseFromString(file_commit_pb.read_bytes())
    file_commit_map = git_utils.FileCommitMap.from_proto(file_commit_proto)

    # Get execution times
    with bep_pb.open("rb") as bep_buf:
        node_duration = bep_reader.get_label_to_runtime(bep_buf)
        node_duration_s = {
            label: dt.total_seconds() for label, dt in node_duration.items()
        }

    # Get rules and graph
    rules = _get_rules(query_result)
    graph = get_dependency_digraph(rules, ignore_external=True)

    node_probability = _get_node_probability(
        graph=graph, file_commit_map=file_commit_map
    )

    node_to_class: dict[str, str] = {}
    # Gotta make table for all, in a consistent order, otherwise table, etc.
    # won't line up:
    # Note that we're not selecting which nodes to view
    for node_name in graph.nodes:
        node_rule = rules.get(node_name)
        if node_name in node_probability:
            # Probably want the source files too
            node_to_class[node_name] = "source_file"
        elif node_rule:
            node_to_class[node_name] = node_rule.rule_class
        else:
            node_to_class[node_name] = "unknown"
    nodes = dependency_analysis(
        node_to_class=node_to_class,
        graph=graph,
        node_duration_s=node_duration_s,
        node_probability=node_probability,
    )
    # Add node attributes to graph
    for name, node in nodes.items():
        for k, v in node.items():
            graph.nodes[name][k] = v
        graph.nodes[name]["Node"] = node["node_name"]
        graph.nodes[name]["Highlight"] = "No"
    # Write the nodes
    with open(out_csv, "w") as f:
        writer = csv.DictWriter(f, fieldnames=get_node_field_names())
        writer.writeheader()
        for row in nodes.values():
            writer.writerow(row)
    # Write the graph
    networkx.write_gml(graph, out_gml)


@click.command()
@click.option("--gml", type=PATH_TYPE, required=True)
@click.option("--out-html", type=OUT_PATH_TYPE, required=False)
def visualize(
    gml: pathlib.Path,
    out_html: pathlib.Path | None,
) -> None:
    graph = networkx.read_gml(gml)
    panel.run_panel(graph=graph, html_out=out_html)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    cli.add_command(git_capture)
    cli.add_command(process)
    cli.add_command(visualize)
    cli()
