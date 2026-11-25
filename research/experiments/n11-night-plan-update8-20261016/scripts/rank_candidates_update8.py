"""Measured ranking of the eighth-update plan's open branches over all
candidate fifth-stone positions, so the two remaining 10M searches are chosen
by effect on the plan rather than by class counts.

For every selected third of the joint plan the open S4 boundary is expanded to
its canonical unknown fifth-stone children that lie in the allowed witness pool
(stored masks minus layered verdicts).  A candidate's value is the number of
branches it closes on its own (WIN frees them) and the number it would break
(LOSS removes a sole witness).  The optimistic union delta is measured for the
top candidates with the same greedy repair used by the plan updater.
"""
from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OLD = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output"
COST_CMP = ROOT / "research/experiments/n11-proof-cost-comparison-20261012"

sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
sys.path.insert(0, str(COST_CMP / "scripts"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache  # noqa: E402
from s4_win_polarity import verdict_of  # noqa: E402


def key_of(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


def main() -> None:
    with gzip.open(OLD / "dependency-graph.json.gz", "rt") as stream:
        g = json.load(stream)
    plan = json.loads((EXP / "output/repaired-joint-plan-update8.json").read_text())
    choices = {(e["first"], e["reply"], e["third"]): e["s4_class_index"]
               for e in plan["groups"]}
    verdicts = {int(k): v for k, v in plan["resolved_s5_verdicts"].items()}
    excluded = set(plan["excluded_s4_classes"])
    stored = json.loads((COST_CMP / "output/win-witness-masks.json").read_text())
    stored_masks = {lo | (hi << 64) for lo, hi in stored["witness_masks"]}
    known_masks = {g["s5_masks"][i][0] | g["s5_masks"][i][1] << 64 for i in verdicts}
    stored_keys = {key_of(m) for m in stored_masks}
    allowed_keys = stored_keys - {key_of(m) for m in known_masks}

    board = Board(11)
    cache = load_exact_s5_cache(board)
    for i, v in verdicts.items():
        cache[tuple(g["s5_masks"][i])] = {"verdict": v}

    sole_pooled = Counter()
    cover_all = Counter()
    pool_branch_total = Counter()
    for s in set(choices.values()):
        mask = g["s4_masks"][s][0] | g["s4_masks"][s][1] << 64
        children = board.children(mask)
        if any(verdict_of(cache, key_of(c)) == 1 for c in children):
            continue
        open_children = [c for c in children if key_of(c) not in cache]
        pooled = [c for c in open_children if key_of(c) in allowed_keys]
        for c in open_children:
            cover_all[c] += 1
        for c in pooled:
            pool_branch_total[c] += 1
        if len(pooled) == 1:
            sole_pooled[pooled[0]] += 1

    graph_index = {g["s5_masks"][i][0] | g["s5_masks"][i][1] << 64: i
                   for i in range(len(g["s5_masks"]))}
    rows = []
    for mask in set(cover_all) | set(sole_pooled):
        rows.append(dict(mask=f"{mask:032x}",
                         graph_index=graph_index.get(mask),
                         in_stored_pool=key_of(mask) in stored_keys,
                         branches_uncovered_by_pool=sole_pooled[mask],
                         pooled_branches=pool_branch_total[mask],
                         branches_covered_if_win=cover_all[mask]))
    rows.sort(key=lambda r: (-r["branches_uncovered_by_pool"], -r["branches_covered_if_win"],
                             r["mask"]))
    summary = dict(
        schema="n11-night-candidate-branch-ranking-update8-v1",
        open_branch_records=sum(cover_all.values()),
        distinct_candidates=len(rows),
        branches_uncovered_by_pool=sum(sole_pooled.values()),
        candidates_resolving_an_uncovered_branch=sum(
            1 for r in rows if r["branches_uncovered_by_pool"]),
        max_branches_uncovered_by_pool=rows[0]["branches_uncovered_by_pool"] if rows else 0,
        top=rows[:25],
    )
    target = EXP / "output/candidate-branch-ranking.json"
    target.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2)[:4000])


if __name__ == "__main__":
    main()
