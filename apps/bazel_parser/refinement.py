import dataclasses
import enum

import networkx
import numpy as np
import pandas


class Verbosity(enum.Enum):
    SILENT = "SILENT"
    COUNT = "COUNT"
    LIST = "LIST"


# XXX: Maybe load from yaml or something other than json for comments?
@dataclasses.dataclass
class RefinementConfig:
    """This specifies how to refine a dataframe of nodes to a smaller set.

    We expect node_name to be the index of the dataframe.

    All of these fields are exclusionary.
    """

    name_patterns: list[str]
    class_patterns: list[str]
    class_pattern_to_name_patterns: dict[str, list[str]]


def _show_exclusions(
    pattern: str,
    exclusion: np.ndarray,
    df: pandas.DataFrame,
    verbosity: Verbosity,
) -> None:
    # XXX: print/log/ or return string?
    if verbosity == Verbosity.SILENT:
        return
    elif verbosity == Verbosity.COUNT:
        count = len(np.where(exclusion == True)[0])
        print(f"{pattern} = {count}")
    elif verbosity == Verbosity.LIST:
        print(f"{pattern} ->")
        for node in sorted(df.loc[exclusion].index.tolist()):
            print(f"- {node}")
    else:
        raise ValueError(f"Unhandled verbosity: {verbosity}")


def refine_dataframe(
    df: pandas.DataFrame,
    refinement: RefinementConfig,
    verbosity: Verbosity,
) -> pandas.DataFrame:
    include = np.full(len(df), True, dtype=bool)
    exclude_by_name = []
    for pattern in refinement.name_patterns:
        match = df.index.str.fullmatch(pattern)
        exclude_by_name.append(match)
        include &= ~match
    exclude_by_class = []
    for pattern in refinement.class_patterns:
        match = df["node_class"].str.fullmatch(pattern)
        exclude_by_class.append(match)
        include &= ~match
    exclude_by_class_then_name = {}
    for (
        class_pattern,
        name_patterns,
    ) in refinement.class_pattern_to_name_patterns.items():
        name_exclusions = np.full(len(df), False, dtype=bool)
        for name_pattern in name_patterns:
            name_exclusions |= df.index.str.fullmatch(name_pattern)
        match = df["node_class"].str.fullmatch(class_pattern) & name_exclusions
        exclude_by_class_then_name[class_pattern] = match
        include &= ~match
    for pattern, exclusion in zip(refinement.name_patterns, exclude_by_name):
        _show_exclusions(
            pattern=pattern, exclusion=exclusion, df=df, verbosity=verbosity
        )
    for pattern, exclusion in zip(refinement.class_patterns, exclude_by_class):
        _show_exclusions(
            pattern=pattern, exclusion=exclusion, df=df, verbosity=verbosity
        )
    for pattern, exclusion in exclude_by_class_then_name.items():
        # XXX: Maybe display more than just the top-level class pattern
        _show_exclusions(
            pattern=pattern, exclusion=exclusion, df=df, verbosity=verbosity
        )
    # XXX: Log / return the individual exclusions
    return df.loc[include]


def remove_node_from_graph(node: str, graph: networkx.DiGraph) -> None:
    """Modify graph by removing node, but preserving edges.

    XXX: How to handle probability / duration attributes of removed nodes?
    """
    for parent in graph.predecessors(node):
        for child in graph.successors(node):
            graph.add_edge(parent, child)
    graph.remove_node(node)


def full_refinement(
    graph: networkx.DiGraph,
    df: pandas.DataFrame,
    refinement: RefinementConfig,
    verbosity: Verbosity,
) -> pandas.DataFrame:
    refined_df = refine_dataframe(
        df=df,
        refinement=refinement,
        verbosity=verbosity,
    )
    removed_nodes = set(df.index.tolist()) - set(refined_df.index.tolist())
    for node in removed_nodes:
        remove_node_from_graph(node, graph)
    return refined_df
