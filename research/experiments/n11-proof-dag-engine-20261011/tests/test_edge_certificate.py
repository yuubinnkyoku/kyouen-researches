import copy
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from dag_builder import ProofLimitExceeded, build_certificate
from dag_verifier import verify_certificate
from independent import Board, aggregate


class EdgeCertificateTests(unittest.TestCase):
    def test_one_by_one_empty_root_and_terminal_child(self):
        cert, stats = build_certificate(1, 0)
        checked = verify_certificate(cert)
        self.assertEqual(checked["verdict"], 1)
        self.assertEqual(stats["node_count"], 2)
        root = cert["nodes"][cert["root"]]
        self.assertEqual(root["edges"], [{"move": 0, "child": "1"}])
        terminal = cert["nodes"]["1"]
        self.assertTrue(terminal["terminal"])
        self.assertEqual(terminal["edges"], [])

    def test_four_by_four_loss_requires_every_root_move(self):
        cert, _ = build_certificate(4, 0)
        self.assertEqual(verify_certificate(cert)["verdict"], 2)
        root = cert["nodes"][cert["root"]]
        self.assertEqual({e["move"] for e in root["edges"]}, set(range(16)))
        self.assertTrue(all(cert["nodes"][e["child"]]["verdict"] == 2
                            for e in root["edges"]))

        damaged = copy.deepcopy(cert)
        damaged["nodes"][damaged["root"]]["edges"].pop()
        with self.assertRaisesRegex(ValueError, "omits"):
            verify_certificate(damaged)

    def test_six_stone_loss_requires_all_seven_stone_loss_children(self):
        board = Board(4)
        values = {}

        def solve(mask):
            if mask not in values:
                children = board.children(mask)
                values[mask] = aggregate(mask.bit_count(),
                                         [solve(child) for child in children])
            return values[mask]

        solve(0)
        root = min(mask for mask, value in values.items()
                    if mask.bit_count() == 6 and value == 2)
        cert, _ = build_certificate(4, root)
        self.assertEqual(verify_certificate(cert)["verdict"], 2)
        node = cert["nodes"][cert["root"]]
        self.assertEqual({edge["move"] for edge in node["edges"]},
                         set(board.points(board.legal(root))))
        self.assertTrue(all(cert["nodes"][edge["child"]]["verdict"] == 2
                            for edge in node["edges"]))

    def test_rejects_wrong_outcome_illegal_edge_cycle_and_trust_leaf(self):
        cert, _ = build_certificate(4, 0)
        damaged = copy.deepcopy(cert)
        damaged["nodes"][damaged["root"]]["verdict"] = 1
        with self.assertRaises(ValueError):
            verify_certificate(damaged)

        damaged = copy.deepcopy(cert)
        damaged["nodes"][damaged["root"]]["edges"][0]["move"] = 16
        with self.assertRaisesRegex(ValueError, "illegal move"):
            verify_certificate(damaged)

        damaged = copy.deepcopy(cert)
        damaged["nodes"][damaged["root"]]["edges"][0]["child"] = damaged["root"]
        with self.assertRaises(ValueError):
            verify_certificate(damaged)

        damaged = copy.deepcopy(cert)
        child = damaged["nodes"][damaged["root"]]["edges"][0]["child"]
        damaged["nodes"][child]["trusted"] = True
        with self.assertRaisesRegex(ValueError, "trusted leaves"):
            verify_certificate(damaged)

    def test_rejects_unreachable_nodes_and_wrong_terminal_marker(self):
        cert, _ = build_certificate(1, 0)
        damaged = copy.deepcopy(cert)
        damaged["nodes"]["unused"] = dict(mask="0", stones=0, verdict=1,
                                           terminal=False, legal_count=1, edges=[])
        with self.assertRaisesRegex(ValueError, "unreachable"):
            verify_certificate(damaged)

        damaged = copy.deepcopy(cert)
        damaged["nodes"]["1"]["terminal"] = False
        with self.assertRaisesRegex(ValueError, "terminal marker"):
            verify_certificate(damaged)

        missing = copy.deepcopy(cert)
        edge = missing["nodes"][missing["root"]]["edges"][0]
        del missing["nodes"][edge["child"]]
        with self.assertRaisesRegex(ValueError, "missing child"):
            verify_certificate(missing)

    def test_budget_exhaustion_never_returns_a_partial_certificate(self):
        with self.assertRaises(ProofLimitExceeded):
            build_certificate(4, 0, node_limit=1)

    def test_sharing_off_agrees_on_a_small_solved_position(self):
        shared, _ = build_certificate(4, 0, state_sharing="d4")
        plain, stats = build_certificate(4, 0, state_sharing="none")
        self.assertEqual(verify_certificate(shared)["verdict"], 2)
        self.assertEqual(verify_certificate(plain)["verdict"], 2)
        self.assertGreaterEqual(stats["calls"], stats["unique_positions"])


if __name__ == "__main__":
    unittest.main()
