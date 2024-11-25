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
import logging
import sys

import networkx

from third_party.bazel.src.main.protobuf import build_pb2
from tools import bazel_utils

logger = logging.getLogger(__name__)


def _get_rules(
    query_result: build_pb2.QueryResult
) -> dict[str, build_pb2.Rule]:
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


def dependency_analysis(
    query_result: build_pb2.QueryResult, ignore_external: bool
) -> None:
    """Analyze the dependencies that we're getting to understand them."""
    rules = _get_rules(query_result)
    graph = get_dependency_digraph(rules, ignore_external=ignore_external)

    for node in networkx.dfs_postorder_nodes(graph):
        logger.debug(node)

    logger.debug(f"nodes: {len(graph.nodes)}")
    logger.debug(f"edges: {len(graph.edges)}")
    logger.debug(f"rules: {len(rules)}")

    pagerank = networkx.pagerank(graph)
    hubs, authorities = networkx.hits(graph)

    fieldnames = [
        "rule_name",
        "rule_class",
        "num_parents",
        "num_ancestors",
        "num_children",
        "num_descendants",
        "pagerank",
        "hubs_metric",
        "authorities_metric",
    ]

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for rule_name, rule in rules.items():
        try:
            num_parents = len(list(graph.predecessors(rule_name)))
            num_children = len(list(graph.successors(rule_name)))
            num_ancestors = len(list(networkx.ancestors(graph, rule_name)))
            num_descendants = len(list(networkx.descendants(graph, rule_name)))
            row = {
                "rule_name": rule_name,
                "rule_class": rule.rule_class,
                "num_parents": num_parents,
                "num_ancestors": num_ancestors,
                "num_children": num_children,
                "num_descendants": num_descendants,
                "pagerank": pagerank[rule_name],
                "hubs_metric": hubs[rule_name],
                "authorities_metric": authorities[rule_name],
            }
            writer.writerow(row)

        except networkx.NetworkXError as e:
            raise AssertionError(f"Exception with {rule_name}") from e
    # Temporary way to export
    networkx.write_gml(graph, "/tmp/my.gml")

    # predecessors, successors is immediate
    # ancestors, descendants is all
    # logger.debug(query_result)


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
    dependency_analysis(query_result, ignore_external=True)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    main()
