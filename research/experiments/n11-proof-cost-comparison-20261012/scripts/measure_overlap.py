#!/usr/bin/env python3
"""Overlap of corrected WIN witnesses with the LOSS-side joint plan + pilots.

Under the corrected K0371 polarity the two frontiers demand opposite
verdicts, so any shared S5 is a polarity CONFLICT (at most one side can use
it), not dual-use evidence.  This script measures the conflict set, rebuilds
the frontier legal-move histogram and cheapest pilot targets, and regenerates
pilot-candidates.json.  No solver search is involved.
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
from independent import Board  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=NEW_EXPERIMENT / "output/overlap-and-pilots.json")
    parser.add_argument("--pilots", type=Path,
                        default=NEW_EXPERIMENT / "output/pilot-candidates.json")
    args = parser.parse_args()
    started = time.time()

    with gzip.open(OLD_EXPERIMENT / "output/dependency-graph.json.gz",
                   "rt", encoding="utf-8") as stream:
        graph = json.load(stream)
    joint = json.loads((OLD_EXPERIMENT / "output/chosen-plans.json").read_text(
        encoding="utf-8"))["plans"]["_joint_19_roots"]["required_new_s5"]
    joint_masks = {tuple(graph["s5_masks"][e]) for e in joint}
    universe = {tuple(m) for m in graph["s5_masks"]}
    wit = json.loads((NEW_EXPERIMENT / "output/win-witness-masks.json").read_text(
        encoding="utf-8"))
    assert wit["schema"] == "n11-win-witness-masks-v2" and wit["passed"]
    win_masks = {tuple(m) for m in wit["witness_masks"]}

    conflict = win_masks & joint_masks
    win_in_universe = win_masks & universe

    board = Board(11)
    hist: Counter[int] = Counter()
    recs = []
    index_of = {tuple(m): e for e, m in enumerate(graph["s5_masks"])}
    for e in joint:
        m = graph["s5_masks"][e]
        mask = m[0] | (m[1] << 64)
        n = len(board.points(board.legal(mask)))
        hist[n] += 1
        recs.append((n, e, m))
    recs.sort()
    conflicts = sorted((n, e, m) for n, e, m in recs if tuple(m) in conflict)

    result = {
        "schema": "n11-overlap-and-pilots-v1",
        "win_witnesses": len(win_masks),
        "joint_required": len(joint_masks),
        "polarity_conflicts": len(conflict),
        "conflict_fraction_of_win": round(len(conflict) / len(win_masks), 4),
        "win_witnesses_inside_central_universe": len(win_in_universe),
        "meaning": ("shared S5s are demanded LOSS by the joint plan and WIN "
                    "by the WIN-side cover: at most one side can use each. "
                    "These are decision points, not shared assets."),
        "pilot_histogram": {str(k): v for k, v in sorted(hist.items())},
        "cheapest10": [{"legal": n, "s5_index": e, "mask": m}
                       for n, e, m in recs[:10]],
        "polarity_conflicts": [{"legal": n, "s5_index": e, "mask": m}
                               for n, e, m in conflicts],
        "seconds": round(time.time() - started, 1),
    }
    with args.output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    pilots = {"histogram": result["pilot_histogram"],
              "cheapest10": result["cheapest10"],
              "polarity_conflicts": result["polarity_conflicts"]}
    with args.pilots.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(pilots, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in ("win_witnesses", "joint_required",
                                            "polarity_conflicts",
                                            "conflict_fraction_of_win",
                                            "win_witnesses_inside_central_universe",
                                            "seconds")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
