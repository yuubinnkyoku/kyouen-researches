#!/usr/bin/env python3
"""Regression tests for the WIN-side S4 polarity (K0371, audit of K0420).

The October K0420 analysis classified an S4 with a cached S5 LOSS child as
first-player WIN.  K0371 (S4 = OR layer, fixed-first-player view) requires
the opposite: S4 WIN iff >= 1 child is cached WIN; S4 LOSS (dead) iff every
legal child is cached LOSS or there is no legal child.

Run: ``uv run --locked python <this file>`` or ``python -m unittest`` here.
No solver search is involved.
"""
from __future__ import annotations

import gzip
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))

from independent import Board  # noqa: E402
from analyze_central_reply_frontier import (  # noqa: E402
    load_exact_s5_cache, s4_status, cache_key)
from s4_win_polarity import classify_s4, verdict_of, FREE, OPEN, DEAD  # noqa: E402

OLD_EXPERIMENT = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
K0414_S4 = (1297036692683752448, 0)


def board_cache():
    board = Board(11)
    return board, load_exact_s5_cache(board)


class WinPolarityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board, cls.cache = board_cache()
        with gzip.open(OLD_EXPERIMENT / "output/dependency-graph.json.gz",
                       "rt", encoding="utf-8") as stream:
            cls.graph = json.load(stream)

    def verdicts(self, mask: int) -> list[int]:
        return [verdict_of(self.cache, (c & ((1 << 64) - 1), c >> 64))
                for c in self.board.children(mask)]

    def test_k0414_all_loss_s4_is_dead(self):
        mask = K0414_S4[0] | (K0414_S4[1] << 64)
        children = self.board.children(mask)
        self.assertEqual(len(children), 106)
        verdicts = self.verdicts(mask)
        self.assertTrue(all(v == 2 for v in verdicts),
                        "every K0414 S4 child must be cached LOSS")
        self.assertEqual(classify_s4(verdicts), DEAD)

    def test_s4_with_cached_win_child_is_free(self):
        win_keys = sorted(k for k, v in self.cache.items() if v["verdict"] == 1)
        self.assertTrue(win_keys, "cache must contain WIN rows")
        found = None
        for key in win_keys:
            mask = key[0] | (key[1] << 64)
            try:
                preds = sorted(self.board.predecessors(mask))
            except ValueError:
                continue
            for pred in preds:
                if mask in self.board.children(pred):
                    found = pred
                    break
            if found is not None:
                break
        self.assertIsNotNone(found, "no safe S4 parent of a cached WIN S5")
        verdicts = self.verdicts(found)
        self.assertIn(1, verdicts)
        self.assertEqual(classify_s4(verdicts), FREE)

    def test_unknown_boundary_s4_is_open(self):
        masks = [(p[0] | (p[1] << 64)) for p in self.graph["s4_masks"]]
        target = next(i for i, s in enumerate(self.graph["s4_status"]) if s == 1)
        verdicts = self.verdicts(masks[target])
        self.assertNotIn(1, verdicts)
        self.assertIn(0, verdicts)
        self.assertEqual(classify_s4(verdicts), OPEN)

    def test_empty_child_set_is_terminal_loss(self):
        self.assertEqual(classify_s4([]), DEAD)

    def test_agrees_with_frontier_s4_status(self):
        masks = [(p[0] | (p[1] << 64)) for p in self.graph["s4_masks"]]
        checked = 0
        for mask in masks[:500]:
            status, _ = s4_status(self.board, mask, self.cache)
            mine = classify_s4(self.verdicts(mask))
            if status == "WIN_CACHE":
                self.assertEqual(mine, FREE, hex(mask))
            elif status in ("LOSS_CACHE", "LOSS_TERMINAL"):
                self.assertEqual(mine, DEAD, hex(mask))
            else:
                self.assertEqual(status, "UNKNOWN")
                self.assertEqual(mine, OPEN, hex(mask))
            checked += 1
        self.assertEqual(checked, 500)


if __name__ == "__main__":
    unittest.main(verbosity=2)
