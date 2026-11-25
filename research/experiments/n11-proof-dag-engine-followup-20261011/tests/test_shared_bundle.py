import copy
import csv
import gzip
import io
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-dag-engine-20261011/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-dag-engine-followup-20261011/scripts"))
from dag_builder import build_certificate  # noqa: E402
from dag_verifier import verify_certificate  # noqa: E402
from verify_shared_bundle import read_trace_bundle, verify_bundle  # noqa: E402


class SharedBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cert, _ = build_certificate(4, 0, order="count-asc",
                                   state_sharing="d4", node_limit=100000)
        cls.bundle = {
            "schema": "kyouen-proof-dag-multi-root-v1",
            "board_size": 4,
            "proposition": "original_first_player_wins",
            "roots": [{"id": "s0", "root": cert["root"],
                       "verdict": verify_certificate(cert)["verdict"]}],
            "nodes": cert["nodes"],
        }

    def test_bundle_and_established_verifier_agree(self):
        receipt = verify_bundle(self.bundle)
        self.assertEqual(receipt["roots"][0]["verdict"], 2)
        established = {"schema": "kyouen-proof-dag-edge-v1", "board_size": 4,
                       "proposition": "original_first_player_wins",
                       "root": self.bundle["roots"][0]["root"],
                       "nodes": self.bundle["nodes"]}
        self.assertEqual(verify_certificate(established)["verdict"],
                         receipt["roots"][0]["verdict"])

    def test_rejects_missing_universal_child(self):
        broken = copy.deepcopy(self.bundle)
        broken["nodes"][broken["roots"][0]["root"]]["edges"].pop()
        with self.assertRaisesRegex(ValueError, "omits or duplicates"):
            verify_bundle(broken)

    def test_rejects_illegal_transition_and_wrong_outcome(self):
        broken = copy.deepcopy(self.bundle)
        broken["nodes"][broken["roots"][0]["root"]]["edges"][0]["move"] = 99
        with self.assertRaisesRegex(ValueError, "illegal move"):
            verify_bundle(broken)
        broken = copy.deepcopy(self.bundle)
        broken["roots"][0]["verdict"] = 1
        with self.assertRaisesRegex(ValueError, "root verdict"):
            verify_bundle(broken)

    def test_rejects_trust_leaf_unreachable_node_and_bad_rank_cycle(self):
        broken = copy.deepcopy(self.bundle)
        terminal = next(k for k, node in broken["nodes"].items() if node["terminal"])
        broken["nodes"][terminal]["trusted"] = True
        with self.assertRaisesRegex(ValueError, "trusted leaves"):
            verify_bundle(broken)
        broken = copy.deepcopy(self.bundle)
        broken["nodes"]["999999999999999999999"] = {
                                  "mask": "999999999999999999999", "stones": 4, "verdict": 2,
                                  "terminal": True, "legal_count": 0, "edges": []}
        with self.assertRaisesRegex(ValueError, "unreachable"):
            verify_bundle(broken)
        broken = copy.deepcopy(self.bundle)
        root = broken["roots"][0]["root"]
        broken["nodes"][root]["edges"][0]["child"] = root
        with self.assertRaisesRegex(ValueError, "nonlegal or incorrectly ranked"):
            verify_bundle(broken)

    def test_gzipped_trace_round_trip_and_bad_terminal_marker(self):
        rows = [["R", "s0", "0", "0", "2"]]
        for ident, node in sorted(self.bundle["nodes"].items(), key=lambda pair: int(pair[0])):
            mask = int(ident)
            rows.append(["N", str(mask & ((1 << 64) - 1)), str(mask >> 64),
                         str(node["verdict"]), str(int(node["terminal"])),
                         str(node["legal_count"])])
            for edge in node["edges"]:
                child = int(edge["child"])
                rows.append(["E", str(mask & ((1 << 64) - 1)), str(mask >> 64),
                             str(edge["move"]), str(child & ((1 << 64) - 1)),
                             str(child >> 64)])
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "trace.csv.gz"
            with gzip.open(path, "wt", encoding="utf-8", newline="") as stream:
                stream.write("# kyouen-proof-trace-bundle-v1,n=4\n")
                writer = csv.writer(stream, lineterminator="\n")
                writer.writerows(rows)
            parsed = read_trace_bundle(path)
            self.assertEqual(verify_bundle(parsed)["roots"][0]["verdict"], 2)
            bad = Path(temp) / "bad-terminal.csv.gz"
            bad_rows = copy.deepcopy(rows)
            terminal_row = next(row for row in bad_rows
                                if row[0] == "N" and row[4] == "1")
            terminal_row[4] = "2"
            with gzip.open(bad, "wt", encoding="utf-8", newline="") as stream:
                stream.write("# kyouen-proof-trace-bundle-v1,n=4\n")
                writer = csv.writer(stream, lineterminator="\n")
                writer.writerows(bad_rows)
            with self.assertRaisesRegex(ValueError, "invalid terminal marker"):
                read_trace_bundle(bad)


if __name__ == "__main__":
    unittest.main()
