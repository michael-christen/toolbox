import unittest

import networkx

from utils import graph_algorithms


class TestGroupProbability(unittest.TestCase):
    def test_basic(self):
        g = networkx.DiGraph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        # Multiple parents are allowed
        g.add_edge(8, 3)
        g.add_edge(2, 4)
        g.add_node(5)
        g.add_edge(6, 7)
        g.add_edge(3, 9)
        g.add_edge(4, 9)
        node_probability = {
            1: 0.6,
            2: 0.2,
            3: 0.3,
            4: 0.4,
            # 5 Is a lone one
            5: 0.5,
            6: 0.3,
            # Intentionally leaving 7 empty
            8: 0.4,
            9: 0.5,
        }
        # each should be itself times the group probability of its children
        p3 = node_probability[3] * node_probability[9]
        p4 = node_probability[4] * node_probability[9]
        # Shared descendant
        p2 = node_probability[2] * (p3 * p4 / node_probability[9])
        p1 = p2 * node_probability[1]
        expected_group_probability = {
            # Leaves
            3: p3,
            4: p4,
            5: node_probability[5],
            # Unspecified becomes 1
            7: 1.0,
            # Child was 1
            6: node_probability[6],
            # each should be itself times the group probability of its children
            2: p2,
            1: p1,
            8: p3 * node_probability[8],
            9: node_probability[9],
        }
        group_probability = graph_algorithms.compute_group_probability(
            graph=g, node_probability=node_probability
        )
        self.assertEqual(group_probability, expected_group_probability)


class TestGroupDurations(unittest.TestCase):
    def test_basic(self):
        g = networkx.DiGraph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        # Multiple parents are allowed
        g.add_edge(8, 3)
        g.add_edge(2, 4)
        g.add_node(5)
        g.add_edge(6, 7)
        # Common ancestor (2)
        g.add_edge(3, 9)
        g.add_edge(4, 9)
        node_duration = {
            1: 1,
            2: 2,
            3: 3,
            # Leaving 4 empty
            5: 5,
            # Leaving 6 empty
            7: 0.1,
            8: 8,
            # Leaving 9 empty
        }
        d2 = node_duration[1] + node_duration[2]
        d3 = node_duration[3] + node_duration[8] + d2
        d4 = 0.0 + d2
        # Common ancestor d2
        d9 = d4 + d3 - d2

        expected_group_duration = {
            # Roots
            1: node_duration[1],
            5: node_duration[5],
            8: node_duration[8],
            # Unspecified
            6: 0.0,
            # Parent was 0
            7: node_duration[7],
            # Computed
            2: d2,
            3: d3,
            4: d4,
            9: d9,
        }
        group_duration = graph_algorithms.compute_group_duration(
            graph=g, node_duration_s=node_duration
        )
        self.assertEqual(group_duration, expected_group_duration)

    def test_cycle(self):
        g = networkx.DiGraph()
        g.add_edge(1, 2)
        g.add_edge(2, 1)
        self.assertIsNotNone(networkx.find_cycle(g))
