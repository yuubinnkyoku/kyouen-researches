#!/usr/bin/env python3
"""Recover board masks for the WIN-side witness S5 sets (cheap targeted pass).

win_side.py stored per-reply witness *indices* into its session-local S5
array, which was not persisted.  This script re-enumerates only the 65 chosen
(reply, third) pairs of first 49, rebuilds the same greedy witness covers,
checks the per-reply witness counts against the stored analysis, and saves
the witness board masks for overlap measurement against the LOSS-side joint
plan.  No solver search is involved.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NEW_EXPERIMENT = ROOT / "research/experiments/n11-proof-cost-comparison-20261012"
OLD_EXPERIMENT = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"

sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache  # noqa: E402


def key_of(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


def greedy_witness_cover(needs: list[set[int]]) -> set[int]:
    uncovered = [s for s in needs if s]
    chosen: set[int] = set()
    while uncovered:
        freq: Counter[int] = Counter()
        for s in uncovered:
            for e in s:
                freq[e] += 1
        best = max(freq, key=lambda e: (freq[e], e))
        chosen.add(best)
        uncovered = [s for s in uncovered if best not in s]
    return chosen


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis", type=Path,
                        default=NEW_EXPERIMENT / "output/win-side-analysis.json")
    parser.add_argument("--output", type=Path,
                        default=NEW_EXPERIMENT / "output/win-witness-masks.json")
    args = parser.parse_args()
    started = time.time()

    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    first_row = next(a for a in analysis["firsts"] if a["first"] == 49)
    board = Board(11)
    cache = load_exact_s5_cache(board)

    masks: set[int] = set()
    mismatches = []
    for rep in first_row["replies"]:
        if not rep["closable"]:
            continue
        pair = (1 << 49) | (1 << rep["reply"])
        s3 = pair | (1 << rep["chosen_third"])
        fourths = board.points(board.legal(s3))
        assert len(fourths) == rep["chosen_fourths"], "fourth count drift"
        needs: list[set[int]] = []
        for u in fourths:
            m = board.canonical(s3 | (1 << u))
            children = board.children(m)
            cached = [cache[key_of(c)]["verdict"] for c in children
                      if key_of(c) in cache]
            unknown = {c for c in children if key_of(c) not in cache}
            if 2 in cached:
                continue
            assert unknown, "dead S4 in stored viable third"
            needs.append(unknown)
        wit = greedy_witness_cover(needs)
        if len(wit) != len(rep["witnesses"]):
            mismatches.append({"reply": rep["reply"], "stored": len(rep["witnesses"]),
                               "recomputed": len(wit)})
        masks |= wit

    result = {
        "schema": "n11-win-witness-masks-v1",
        "first": 49,
        "recomputed_witness_s5": len(masks),
        "stored_witness_s5": first_row["optimistic_witness_s5"],
        "count_mismatches": mismatches,
        "witness_masks": sorted([[m & ((1 << 64) - 1), m >> 64] for m in masks]),
        "seconds": round(time.time() - started, 1),
    }
    with args.output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({k: result[k] for k in ("recomputed_witness_s5",
                                            "stored_witness_s5",
                                            "count_mismatches",
                                            "seconds")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
