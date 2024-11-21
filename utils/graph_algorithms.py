"""Describe a few graph algorithms I am running.

The current (as of 2024-11-20) set of functions is intended for analyzing
depency graphs. In particular for bazel dependency trees, I'd like to represent
dependencies as children and I want to be able to answer the likelihood that a
target is re-built given the likelihood that the children are changed as well
as the duration of time spent from reverse dependencies if a given dependency
changes.
"""
from typing import Any

import networkx


def compute_group_probability(
        graph: networkx.DiGraph,
        node_probability: dict[Any, float],
    ) -> dict[Any, float]:
    """Compute a group probability for a parent node.

    Group probability for a node can be defined for node
    N as a function GP as such:

    GP(N) = P(N) * PRODUCT{CHILDREN(N)}

    Arguments:
    - graph: A directed acyclic graph with any type of node naming
    - node_probability: Individual probability for each node, if not specified
      will assume 1.0. Valid values will be [0, 1.0]

    Precondition:
    - graph has no cycles
    - node_probability values are between 0 and 1.0

    Returns: The group probability for each node.
    """
    node_group_probability = {}
    for node in networkx.dfs_postorder_nodes(graph):
        # Get our own probability, assume 100% if not specified
        product = node_probability.get(node, 1.0)
        # Get product of each child
        for child in graph.successors(node):
            # If postorder traversal is correct this should already be set.
            product *= node_group_probability[child]
        node_group_probability[node] = product
    return node_group_probability


def compute_group_duration(
        graph: networkx.DiGraph,
        node_duration_s: dict[Any, float],
    ) -> dict[Any, float]:
    """Compute a group duration for a child node.

    Reversed from `compute_group_probability`, we want to know the accumulated
    durations of parent nodes on our children.

    Group duration for a node N as a function GD:

    GD(N) = D(N) * SUM{PARENTS(N)}

    Arguments:
    - graph: A directed acyclic graph
    - node_duration_s: A mapping of node id to duration for that node to
      execute. If not present will assume 0. Expects all are >= 0.

    Returns: Group duration for each node.
    """
    node_group_durations = {}
    # Reverse the graph in order to do a "proper" traversal and don't end up
    # with unvisited parents. If we didn't reverse and did a preorder traversal
    # we could end up traversing from one parent down to a child without having
    # visited the other parent. Doing this allows us to avoid that
    # possibility
    graph = graph.reverse(copy=True)
    for node in networkx.dfs_postorder_nodes(graph):
        # Get our own duration
        total = node_duration_s.get(node, 0.0)
        # Get sum of parents (referring to as succssors becasue we've reversed
        # the graph in order to handle multiple parents)
        for parent in graph.successors(node):
            # If preorder traversal is correct this should already be set.
            total += node_group_durations[parent]
        node_group_durations[node] = total
    return node_group_durations
