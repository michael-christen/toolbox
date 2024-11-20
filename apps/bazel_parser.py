import csv
import sys

import networkx

from third_party.bazel.src.main.protobuf import build_pb2

from tools import bazel_utils


def dependency_analysis(query_result: build_pb2.QueryResult) -> None:
    """Analyze the dependencies that we're getting to understant them.

    """
    graph = networkx.DiGraph()
    rules = {}

    for i, target in enumerate(query_result.target):
        type_name = build_pb2.Target.Discriminator.Name(target.type)
        if target.type == build_pb2.Target.Discriminator.RULE:
            pass
        elif target.type in {build_pb2.Target.Discriminator.SOURCE_FILE,
                             build_pb2.Target.Discriminator.GENERATED_FILE,
                             build_pb2.Target.Discriminator.PACKAGE_GROUP,
                             build_pb2.Target.Discriminator.ENVIRONMENT_GROUP}:
            # print(i, type_name)
            continue
        else:
            raise ValueError(
                f'Invalid target type: {type_name}({target.type})')
        # We are a rule type now
        rule = target.rule

        # print(f'{rule.name}({rule.rule_class})')
        rules[rule.name] = rule
        for i in rule.rule_input:
            graph.add_edge(i, rule.name)
        for output in rule.rule_output:
            graph.add_edge(rule.name, output)
        # Didn't see much use with these:
        # - rule.configured_rule_input
        # - rule.default_setting

    # XXX: What should the order be (is depended by or depends on?
    graph = graph.reverse()

    # print('nodes', len(graph.nodes))
    # print('edges', len(graph.edges))

    pagerank = networkx.pagerank(graph)
    hubs, authorities = networkx.hits(graph)

    fieldnames = [
        'rule_name',
        'rule_class',
        'num_parents',
        'num_ancestors',
        'num_children',
        'num_descendants',
        'pagerank',
        'hubs_metric',
        'authorities_metric',
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
                'rule_name': rule_name,
                'rule_class': rule.rule_class,
                'num_parents': num_parents,
                'num_ancestors': num_ancestors,
                'num_children': num_children,
                'num_descendants': num_descendants,
                'pagerank': pagerank[rule_name],
                'hubs_metric': hubs[rule_name],
                'authorities_metric': authorities[rule_name],
            }
            writer.writerow(row)

            # print(f'{rule_name}: {num_parents}/{num_ancestors}'
            #       f' {num_children}/{num_descendants}'
            #       f' {pagerank[rule_name]}'
            #       f' {hubs[rule_name]},{authorities[rule_name]}')
        except networkx.NetworkXError:
            # print(f'Exception with {rule_name}')
            ...

    # predecessors, successors is immediate
    # ancestors, descendants is all
    # print(query_result)


def main():
    query_result = bazel_utils.parse_build_output(sys.stdin.buffer.read())
    dependency_analysis(query_result)


if __name__ == "__main__":
    main()
