import gzip
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-compact-20261011/scripts"))
from analyze_class_cover import reconstruct  # noqa: E402


class FrozenMainCoverTests(unittest.TestCase):
    def test_geometry_rebuilds_the_forced_31_class_cover(self):
        source = ROOT / "research/experiments/n11-independent-exact-audit-20261010/output"
        with gzip.open(source / "frontier.json.gz", "rt", encoding="utf-8") as stream:
            frontier = json.load(stream)
        with (source / "third-move-certificate.json").open(encoding="utf-8") as stream:
            certificate = json.load(stream)
        with (source / "audit.json").open(encoding="utf-8") as stream:
            audit = json.load(stream)
        result = reconstruct(frontier, certificate, audit)
        self.assertEqual(result["covered_third_moves"], 117)
        self.assertEqual(result["uncovered_third_moves"], [100, 108])
        self.assertEqual(result["incidence_histogram"], {"1": 112, "2": 4, "13": 1})
        self.assertEqual(result["forced_class_count"], 31)
        self.assertEqual(result["minimum_loss_classes_for_current_117_cover"], 31)
        self.assertEqual(result["raw_supported_loss_classes"], 1)


if __name__ == "__main__":
    unittest.main()
