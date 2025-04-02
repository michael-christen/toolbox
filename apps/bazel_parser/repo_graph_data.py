"""Contain the core data-classes for analyzing repo's and their composition."""

import logging
import pathlib
from typing import TypedDict

import networkx
import pandas

from utils import graph_algorithms

logger = logging.getLogger(__name__)


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

    # A more node specific version of
    # rebuilt_targets_by_transitive_dependencies
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


# XXX: Setup pandera type-hinting with mypy
# https://pandera.readthedocs.io/en/stable/mypy_integration.html
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


class GraphMetrics(TypedDict):
    """Graph-wide metrics."""

    longest_path: int
    max_depth: int
    # aka) order
    num_nodes: int
    # aka) size
    num_edges: int
    density: float
    num_connected_components: int
    total_duration_s: float
    expected_duration_s: float
    avg_files_changed_per_commit: float
    avg_nodes_affected_per_commit: float

    # Proposal for new attributes
    # XXX: max/aggregation of most of the node attributes
    # - networkx.average_shortest_path_length
    # Not defining
    # unable to capture these since requires strongly connected components
    # diameter: int
    # radius: int


# Put graph and dataframe into a class to make it a bit easier to work with
class RepoGraphData:
    graph: networkx.DiGraph
    df: pandas.DataFrame

    def __init__(
        self,
        graph: networkx.DiGraph,
        node_to_class: dict[str, str],
        node_probability: dict[str, float],
        node_duration_s: dict[str, float],
    ):
        self.graph = graph
        data = {}
        for node_name, node_class in node_to_class.items():
            data[node_name] = {
                "node_class": node_class,
                "node_name": node_name,
                "node_probability_cache_hit": node_probability.get(
                    node_name, 1.0
                ),
                "node_duration_s": node_duration_s.get(node_name, 0.0),
            }
        self.df = pandas.DataFrame.from_dict(data, orient="index")
        self.refresh()

    def refresh(self) -> None:
        """Update .df based on updates to graph, etc."""
        nodes = dependency_analysis(
            node_to_class=self.df["node_class"].to_dict(),
            graph=self.graph,
            # XXX: We use presence in these to determine source or test, etc
            # ... should we do otherwise?
            node_probability=self.df["node_probability_cache_hit"].to_dict(),
            node_duration_s=self.df["node_duration_s"].to_dict(),
        )
        self.df = pandas.DataFrame.from_dict(nodes, orient="index")

    def get_node(self, node: str) -> Node:
        return self.df.loc[node].to_dict()

    def get_graph_metrics(self) -> GraphMetrics:
        # XXX: Maybe we should remove weakly connected components < some
        # threshold size
        expected_duration_s = (
            self.df["node_duration_s"]
            * (1 - self.df["group_probability_cache_hit"])
        ).sum()

        metrics: GraphMetrics = {
            # longest path can be more than max depth
            "longest_path": networkx.dag_longest_path_length(self.graph),
            "max_depth":
            # Equivalent of max descendant_depth
            self.df["ancestor_depth"].max(),
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
            "density": networkx.density(self.graph),
            "num_connected_components": (
                networkx.number_weakly_connected_components(self.graph)
            ),
            "total_duration_s": self.df["node_duration_s"].sum(),
            "expected_duration_s": expected_duration_s,
            "avg_files_changed_per_commit": (
                1 - self.df["node_probability_cache_hit"]
            ).sum(),
            "avg_nodes_affected_per_commit": (
                1 - self.df["group_probability_cache_hit"]
            ).sum(),
        }
        return metrics

    # XXX: label, node_name, Node are all doing the same thing
    def to_gml(self, out_gml: pathlib.Path) -> None:
        # Add node attributes to copy of the graph
        graph = self.graph.copy()
        for name, row in self.df.iterrows():
            for k, v in row.items():
                graph.nodes[name][k] = v
            # Additional fields for visualization
            graph.nodes[name]["Node"] = row["node_name"]
            graph.nodes[name]["Highlight"] = "No"
        # Write the graph
        networkx.write_gml(graph, out_gml)

    # XXX: Maybe don't even
    # XXX: index column is empty
    def to_csv(self, out_csv: pathlib.Path) -> None:
        # node_name is preserved, so don't need to re-emit
        self.df.to_csv(out_csv, index=False)


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
        networkx.all_pairs_shortest_path_length(graph)
    )
    reverse_all_pairs_shortest_path_length = (
        networkx.all_pairs_shortest_path_length(reversed_graph)
    )
    descendant_depth: dict[str, int] = {}
    ancestor_depth: dict[str, int] = {}
    for node_name, pair_len_dict in forward_all_pairs_shortest_path_length:
        descendant_depth[node_name] = max(pair_len_dict.values())
    for node_name, pair_len_dict in reverse_all_pairs_shortest_path_length:
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
            # XXX: Do we want presence or not ...
            [a for a in ancestors if a in node_duration_s]
        )
        descendants = list(networkx.descendants(graph, node_name))
        num_descendants = len(descendants)
        num_source_descendants = len(
            # XXX: Do we want presence or not ... can we store null?
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
            "ancestors_by_descendants": num_ancestors * num_descendants,
            "betweenness_centrality": betweenness[node_name],
            "closeness_centrality": closeness[node_name],
        }
        nodes[node_name] = row
    return nodes
