"""A collecion of graph algorihms.

Some set of functions is intended for analyzing depency graphs. In particular
for bazel dependency trees, I'd like to represent dependencies as children and
I want to be able to answer the likelihood that a target is re-built given the
likelihood that the children are changed as well as the duration of time spent
from reverse dependencies if a given dependency changes.
"""

from typing import TypeVar

import networkx
import tqdm

T = TypeVar("T")


def compute_group_probability(
    graph: networkx.DiGraph,
    node_probability: dict[T, float],
) -> dict[T, float]:
    """Compute a group probability for a parent node.

    Group probability for a node can be defined for node
    N as a function GP as such:

    GP(N) = P(N) * PRODUCT{DESCENDANTS(N)}

    Arguments:
    - graph: A directed acyclic graph with any type of node naming
    - node_probability: Individual probability for each node, if not specified
      will assume 1.0. Valid values will be [0, 1.0]

    Precondition:
    - graph has no cycles
    - node_probability values are between 0 and 1.0

    Returns: The group probability for each node.
    """
    node_group_probability: dict[T, float] = {}
    for node in tqdm.tqdm(graph.nodes):
        # Get our own probability, assume 100% if not specified
        product = node_probability.get(node, 1.0)
        # Get product of each child
        for descendant in networkx.descendants(graph, node):
            product *= node_probability.get(descendant, 1.0)
        node_group_probability[node] = product
    return node_group_probability


def compute_group_duration(
    graph: networkx.DiGraph,
    node_duration_s: dict[T, float],
) -> dict[T, float]:
    """Compute a group duration for a child node.

    Reversed from `compute_group_probability`, we want to know the accumulated
    durations of parent nodes on our children.

    Group duration for a node N as a function GD:

    GD(N) = D(N) + SUM{ANCESTORS(N)}

    Arguments:
    - graph: A directed acyclic graph
    - node_duration_s: A mapping of node id to duration for that node to
      execute. If not present will assume 0. Expects all are >= 0.

    Returns: Group duration for each node.
    """
    node_group_durations: dict[T, float] = {}
    # xXX: Maybe I could make it quicker by only defining the graph as elements
    # w/ nodes that have duration?
    for node in tqdm.tqdm(graph.nodes):
        # Get our own duration

        total = node_duration_s.get(node, 0.0)
        for ancestor in networkx.ancestors(graph, node):
            total += node_duration_s.get(ancestor, 0.0)
        node_group_durations[node] = total
    return node_group_durations
