import pathlib
import pprint
import unittest

import networkx

from apps.bazel_parser import repo_graph_data


class TestRepoGraphData(unittest.TestCase):

    def test_basics(self) -> None:
        g: networkx.DiGraph = networkx.DiGraph(
            [
                ("a", "b"),
                ("b", "c"),
                ("d", "e"),
                # Show longest path can be greater than max depth
                ("a", "f"),
                ("f", "g"),
                ("g", "c"),
                # Separate component
                ("h", "i"),
            ]
        )
        node_to_class = {
            "a": "T",
            "b": "T",
            "c": "F",
            "d": "G",
            "e": "F",
            "f": "H",
            "g": "H",
            "h": "H",
            "i": "H",
        }
        node_probability = {
            "c": 0.5,
            "e": 0.25,
        }
        node_duration_s = {
            "a": 1.5,
            "b": 2.5,
            "d": 3.5,
        }
        r = repo_graph_data.RepoGraphData(
            graph=g,
            node_to_class=node_to_class,
            node_probability=node_probability,
            node_duration_s=node_duration_s,
        )
        # XXX: Test the various computed values, etc.
        print(r.df)
        pprint.pprint(r.get_node("c"))
        self.assertEqual(r.get_node("c")["node_probability_cache_hit"], 0.5)
        self.assertEqual(r.get_node("c")["num_duration_ancestors"], 2)
        self.assertEqual(r.get_node("d")["num_duration_ancestors"], 0)
        self.assertEqual(r.get_node("i")["num_ancestors"], 1)
        self.assertEqual(r.get_node("i")["num_duration_ancestors"], 0)
        # XXX: num_source_descendants
        with self.assertRaisesRegex(KeyError, "not there"):
            r.get_node("not there")

        graph_metrics = r.get_graph_metrics()
        self.assertEqual(3, graph_metrics["longest_path"])
        self.assertEqual(2, graph_metrics["max_depth"])
        pprint.pprint(graph_metrics)
        # XXX
        r.to_gml(pathlib.Path("/tmp/mchristen_now.gml"))
        r.to_csv(pathlib.Path("/tmp/mchristen_now.csv"))
