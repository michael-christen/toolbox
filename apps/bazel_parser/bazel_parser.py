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

Example Script:

repo_dir=`pwd`
file_commit_pb=$repo_dir/file_commit.pb
query_pb=$repo_dir/s_result.pb
bep_pb=$repo_dir/test_all.pb
out_gml=$repo_dir/my.gml
out_csv=$repo_dir/my.csv
out_html=$repo_dir/my.html

# Prepare data
bazel query "//... - //docs/... - //third_party/bazel/..." --output proto > $query_pb
bazel test //... --build_event_binary_file=$bep_pb
bazel run //apps/bazel_parser --output_groups=-mypy -- git-capture --repo-dir $repo_dir --days-ago 400 --file-commit-pb $file_commit_pb

# Process and visualize the data
bazel run //apps/bazel_parser --output_groups=-mypy -- process --file-commit-pb $file_commit_pb --query-pb $query_pb --bep-pb $bep_pb --out-gml $out_gml --out-csv $out_csv
bazel run //apps/bazel_parser --output_groups=-mypy -- visualize --gml $out_gml --out-html $out_html
"""
import csv
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
from tools import git_utils
from tools import git_pb2
from utils import bep_reader
from utils import graph_algorithms

logger = logging.getLogger(__name__)

PATH_TYPE = click.Path(exists=True, path_type=pathlib.Path)
OUT_PATH_TYPE = click.Path(exists=False, path_type=pathlib.Path)


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
        files: list[pathlib.Path]) -> dict[str, pathlib.Path]:
    normalized_map = {}
    for f in files:
        normalized = f'//{f}'
        normalized_map[normalized] = f
    return normalized_map


def _normalize_bazel_target_to_intermediate(target: str) -> str:
    if target.startswith('//:'):
        return target.replace(':', '')
    else:
        return target.replace(':', '/')


class Node(TypedDict):
    node_name: str
    node_class: str
    num_parents: int
    num_ancestors: int
    num_duration_ancestors: int
    num_children: int
    num_descendants: int
    num_source_descendants: int
    pagerank: float
    hubs_metric: float
    authorities_metric: float
    node_duration_s: float
    group_duration_s: float
    expected_duration_s: float
    node_probability_cache_hit: float
    group_probability_cache_hit: float
    # Keep in sync with get_node_field_names, and panel.py


def get_node_field_names() -> list[str]:
    """Get ordered list of field names to display.

    Keep in sync with Node
    """
    return [
        'node_name',
        'node_class',
        'num_parents',
        'num_ancestors',
        'num_duration_ancestors',
        'num_children',
        'num_descendants',
        'num_source_descendants',
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

    # logger.debug(f"nodes: {len(graph.nodes)}")
    # logger.debug(f"edges: {len(graph.edges)}")
    # XXX: Show graph density


    nodes: dict[str, Node] = {}
    for node_name, node_class in node_to_class.items():
        num_parents = len(list(graph.predecessors(node_name)))
        num_children = len(list(graph.successors(node_name)))
        ancestors = list(networkx.ancestors(graph, node_name))
        num_ancestors = len(ancestors)
        num_duration_ancestors = len([a for a in ancestors if a in node_duration_s])
        descendants = list(networkx.descendants(graph, node_name))
        num_descendants = len(descendants)
        num_source_descendants = len([d for d in descendants if d in node_probability])
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
            "node_probability_cache_hit": node_probability.get(node_name, 1.0),
            "group_probability_cache_hit": gp,
        }
        nodes[node_name] = row
    return nodes


@click.group()
def cli():
    pass


@click.command()
@click.option('--repo-dir', type=PATH_TYPE, required=True)
@click.option('--days-ago', type=int, required=True)
@click.option('--file-commit-pb', type=OUT_PATH_TYPE, required=True)
def git_capture(repo_dir: pathlib.Path,
                days_ago: int,
                file_commit_pb: pathlib.Path,
                ) -> None:
    git_query_after = (
        datetime.datetime.now() - datetime.timedelta(days=days_ago))
    file_commit_map = git_utils.get_file_commit_map_from_follow(
        git_directory=repo_dir,
        after=git_query_after)
    file_commit_pb.write_bytes(file_commit_map.to_proto()
                               .SerializeToString(deterministic=True))


@click.command()
@click.option('--query-pb', type=PATH_TYPE, required=True)
@click.option('--bep-pb', type=PATH_TYPE, required=True)
@click.option('--file-commit-pb', type=PATH_TYPE, required=True)
@click.option('--out-gml', type=OUT_PATH_TYPE, required=True)
@click.option('--out-csv', type=OUT_PATH_TYPE, required=True)
def process(query_pb: pathlib.Path,
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
    with bep_pb.open('rb') as bep_buf:
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
    # Note that we're not selecting which nodes to view
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
    # Add node attributes to graph
    for name, node in nodes.items():
        for k, v in node.items():
            graph.nodes[name][k] = v
        graph.nodes[name]['Node'] = node['node_name']
        graph.nodes[name]['Highlight'] = 'No'
    # Write the nodes
    with open(out_csv, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=get_node_field_names())
        writer.writeheader()
        for row in nodes.values():
            writer.writerow(row)
    # Write the graph
    networkx.write_gml(graph, out_gml)


@click.command()
@click.option('--gml', type=PATH_TYPE, required=True)
@click.option('--out-html', type=OUT_PATH_TYPE, required=False)
def visualize(gml: pathlib.Path,
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
