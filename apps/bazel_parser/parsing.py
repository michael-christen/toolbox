"""Handle converting raw types to the data structures that get used."""

import datetime
import pathlib

import networkx

from apps.bazel_parser import repo_graph_data
from third_party.bazel.src.main.protobuf import build_pb2
from tools import git_pb2
from tools import git_utils


def _get_rules(
    query_result: build_pb2.QueryResult,
) -> dict[str, build_pb2.Rule]:
    """Get rules by name"""
    rules = {}

    for i, target in enumerate(query_result.target):
        type_name = build_pb2.Target.Discriminator.Name(
            target.type
        )  # type: ignore
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


def _get_node_probability(
    nodes: list[str],
    file_commit_map: git_utils.FileCommitMap,
) -> dict[str, float]:
    # XXX: Test case with BUILD further up, ensure we still get the right match
    bazel_intermediates = _normalize_paths_to_bazel_intermediates(
        list(file_commit_map.file_map.keys())
    )
    bazel_src_target_to_file = {}
    for node in nodes:
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


def _get_node_to_class(
    nodes: list[str],
    node_probability: dict[str, float],
    rules: dict[str, build_pb2.Rule],
) -> dict[str, str]:

    node_to_class: dict[str, str] = {}
    # Gotta make table for all, in a consistent order, otherwise table, etc.
    # won't line up:
    # Note that we're not selecting which nodes to view
    for node_name in nodes:
        node_rule = rules.get(node_name)
        if node_name in node_probability:
            # Probably want the source files too
            node_to_class[node_name] = "source_file"
        elif node_rule:
            node_to_class[node_name] = node_rule.rule_class
        else:
            node_to_class[node_name] = "unknown"
    return node_to_class


def get_repo_graph_data(
    query_result: build_pb2.QueryResult,
    label_to_runtime: dict[str, datetime.timedelta],
    file_commit_proto: git_pb2.FileCommitMap,
) -> repo_graph_data.RepoGraphData:
    file_commit_map = git_utils.FileCommitMap.from_proto(file_commit_proto)
    node_duration_s = {
        label: dt.total_seconds() for label, dt in label_to_runtime.items()
    }
    rules = _get_rules(query_result)
    graph = get_dependency_digraph(rules, ignore_external=True)
    node_probability = _get_node_probability(
        nodes=list(graph.nodes), file_commit_map=file_commit_map
    )
    node_to_class = _get_node_to_class(
        nodes=list(graph.nodes), node_probability=node_probability, rules=rules
    )
    return repo_graph_data.RepoGraphData(
        graph=graph,
        node_to_class=node_to_class,
        node_probability=node_probability,
        node_duration_s=node_duration_s,
    )
