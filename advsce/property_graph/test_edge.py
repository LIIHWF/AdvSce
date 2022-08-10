

from advsce.property_graph.edge import add_edge_appearing_twice, edge_book
from advsce.property_graph import graph
import unittest


def str_to_regex(s):
    return s.replace('[', '\[').replace(']', '\]').replace('(', '\(').replace(')', '\)')


class TestAddEdgeAppearingTwice(unittest.TestCase):
    def setUp(self):
        self.g = graph.Graph()
        self.g.add_vertex('v1', {})
        self.g.add_vertex('v2', {})

    def test_add_two_same_edges(self):
        add_edge_appearing_twice(self.g, graph.Edge('edge_1', 'v1', 'v2', {'a': 1}))
        add_edge_appearing_twice(self.g, graph.Edge('edge_1', 'v1', 'v2', {'a': 1}))
        self.assertEqual(2, edge_book['edge_1'])
        self.assertEqual(str(graph.Edge('edge_1', 'v1', 'v2', {'a': 1})), str(self.g.edges['edge_1']))

    def test_add_two_reverse_edges(self):
        add_edge_appearing_twice(self.g, graph.Edge('edge_2', 'v1', 'v2', {'b': 2}))
        with self.assertRaisesRegex(NameError, str_to_regex("Edge<edge_2> provided and existing inconsistent, "
                                                            "provided:Edge[edge_2](v2->v1){properties={'b': 2}}, "
                                                            "existing:Edge[edge_2](v1->v2){properties={'b': 2}}")):
            add_edge_appearing_twice(self.g, graph.Edge('edge_2', 'v2', 'v1', {'b': 2}))

        self.assertEqual(1, edge_book['edge_2'])
        self.assertEqual(str(graph.Edge('edge_2', 'v1', 'v2', {'b': 2})), str(self.g.edges['edge_2']))

    def test_add_two_edges_with_different_properties(self):
        add_edge_appearing_twice(self.g, graph.Edge('edge_3', 'v1', 'v2', {'c': 3}))
        with self.assertRaisesRegex(NameError, str_to_regex("Edge<edge_3> provided and existing inconsistent, "
                                                            "provided:Edge[edge_3](v1->v2){properties={'d': 3}}, "
                                                            "existing:Edge[edge_3](v1->v2){properties={'c': 3}}")):
            add_edge_appearing_twice(self.g, graph.Edge('edge_3', 'v1', 'v2', {'d': 3}))

        self.assertEqual(1, edge_book['edge_3'])
        self.assertEqual(str(graph.Edge('edge_3', 'v1', 'v2', {'c': 3})), str(self.g.edges['edge_3']))

    def test_add_three_edges_with_same_id(self):
        add_edge_appearing_twice(self.g, graph.Edge('edge_4', 'v1', 'v2', {'e': 5}))
        add_edge_appearing_twice(self.g, graph.Edge('edge_4', 'v1', 'v2', {'e': 5}))
        with self.assertRaisesRegex(NameError, "Edge<edge_4> appear more than twice"):
            add_edge_appearing_twice(self.g, graph.Edge('edge_4', 'v1', 'v2', {'e': 5}))
        self.assertEqual(2, edge_book['edge_4'])
        self.assertEqual(str(graph.Edge('edge_4', 'v1', 'v2', {'e': 5})), str(self.g.edges['edge_4']))
