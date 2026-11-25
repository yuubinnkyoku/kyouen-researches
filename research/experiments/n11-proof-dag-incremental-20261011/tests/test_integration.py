import sys
import unittest
from array import array
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-dag-incremental-20261011/scripts"))
from integrate import DecisionGraph, exact_root_choices, greedy_add_roots, local_improve  # noqa: E402


def _shared_choice_graph():
    """Two roots can share a larger witness closure in the union DAG."""
    graph = object.__new__(DecisionGraph)
    graph.node_count = 7
    graph.existential = bytearray([1, 0, 0, 1, 0, 0, 0])
    graph.default_child = array("I", [1, 0, 0, 4, 0, 0, 0])
    graph.default_move = bytearray([10, 0, 0, 20, 0, 0, 0])
    graph.options = {0: [(1, 10), (4, 11)]}
    graph.universal_offsets = array("I", [0, 0, 1, 1, 1, 2, 3, 3])
    graph.universal_children = array("I", [2, 5, 6])
    graph.universal_moves = bytearray([1, 2, 3])
    graph.masks = bytearray(16 * graph.node_count)
    for index in range(graph.node_count):
        graph.masks[index * 16 + 15] = index
    graph.connection = None
    graph.roots = [{"id": "shared-root", "sequence": 0},
                   {"id": "reuse-root", "sequence": 3}]
    return graph


class JointWitnessOptimizationTests(unittest.TestCase):
    def test_greedy_prefers_already_reachable_larger_closure(self):
        graph = _shared_choice_graph()
        selected = array("I", graph.default_child)
        stats, steps = greedy_add_roots(
            graph, selected, [graph.roots[1]], [graph.roots[0]])
        self.assertEqual(selected[0], 4)
        self.assertEqual((stats["nodes"], stats["edges"]), (5, 4))
        self.assertEqual(steps[0]["new_reachable_nodes"], 1)

    def test_local_improvement_uses_global_union_not_standalone_size(self):
        graph = _shared_choice_graph()
        selected = array("I", graph.default_child)
        before = graph.stats(selected, graph.roots)
        after, audit = local_improve(graph, selected, graph.roots)
        self.assertEqual((before["nodes"], before["edges"]), (7, 5))
        self.assertEqual((after["nodes"], after["edges"]), (5, 4))
        self.assertEqual(selected[0], 4)
        self.assertEqual(audit["passes"], 1)

    def test_exact_root_choice_matches_enumerated_union_optimum(self):
        graph = _shared_choice_graph()
        selected = array("I", graph.default_child)
        stats, audit = exact_root_choices(graph, selected, graph.roots)
        self.assertEqual(audit["status"], "exact_root_choice_optimum")
        self.assertEqual(audit["evaluated"], 2)
        self.assertEqual((stats["nodes"], stats["edges"]), (5, 4))
        self.assertEqual(selected[0], 4)

    def test_exact_search_fails_closed_when_combination_limit_is_exceeded(self):
        graph = _shared_choice_graph()
        selected = array("I", graph.default_child)
        _, audit = exact_root_choices(graph, selected, graph.roots,
                                     max_combinations=1)
        self.assertEqual(audit["status"], "skipped_combination_limit")
        self.assertEqual(audit["combinations"], 2)


if __name__ == "__main__":
    unittest.main()
