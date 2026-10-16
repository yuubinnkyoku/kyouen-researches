"""Measured WIN/LOSS effect on the eighth-update plan for every eligible
candidate that is the sole pooled witness of a currently uncovered branch.

The exploration shortlist is 143718, 150871, 196002, 221294, 103564, 211133 and
144774.  144019, 193768 and 144692 resolve an uncovered branch too but already
have a 10M run under the same conditions, so they are excluded (K0418).
"""
from __future__ import annotations

import gzip
import json
import sys
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

ELIGIBLE = [143718, 196002, 221294, 103564, 211133, 144774]
ALREADY_10M = {144019, 193768, 144692, 150871}


def key_of(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


def main() -> None:
    with gzip.open(OLD / "dependency-graph.json.gz", "rt") as stream:
        g = json.load(stream)
    plan = json.loads((EXP / "output/repaired-joint-plan-update8.json").read_text())
    assert plan["verification"]["passed"]
    choices = {(e["first"], e["reply"], e["third"]): e["s4_class_index"]
               for e in plan["groups"]}
    baseline_union = set(plan["required_new_s5"])
    excluded = set(plan["excluded_s4_classes"])
    verdicts = {int(k): v for k, v in plan["resolved_s5_verdicts"].items()}
    losses = {i for i, v in verdicts.items() if v == 2}
    cost = [set(c) - losses for c in g["s4_cost"]]
    stored = json.loads((COST_CMP / "output/win-witness-masks.json").read_text())
    stored_masks = {lo | (hi << 64) for lo, hi in stored["witness_masks"]}
    known_masks = {g["s5_masks"][i][0] | g["s5_masks"][i][1] << 64 for i in verdicts}
    allowed_keys = {key_of(m) for m in (stored_masks - known_masks)}

    options = {}
    for root in g["roots"]:
        if root["role"] == "known-loss-baseline":
            continue
        for row in root["thirds"]:
            options[(root["origin_first"], root["origin_reply"], row["third"])] = \
                [s for s in row["options"] if s not in excluded]
    assert set(options) == set(choices)
    assert set().union(*(cost[s] for s in choices.values())) == baseline_union

    def select(seed, cost_table, excluded_set):
        chosen = {ident: s for ident, s in seed.items() if s not in excluded_set}
        union = set().union(*(cost_table[s] for s in chosen.values()))
        changed = 0
        for ident in sorted(seed):
            if ident in chosen:
                continue
            s = min((t for t in options[ident] if t not in excluded_set),
                    key=lambda t: (len(cost_table[t] - union), len(cost_table[t]), t))
            chosen[ident] = s
            union |= cost_table[s]
            changed += 1
        return union, changed

    board = Board(11)
    cache = load_exact_s5_cache(board)
    for i, v in verdicts.items():
        cache[tuple(g["s5_masks"][i])] = {"verdict": v}
    uncovered = {}
    for s in set(choices.values()):
        mask = g["s4_masks"][s][0] | g["s4_masks"][s][1] << 64
        children = board.children(mask)
        if any(verdict_of(cache, key_of(c)) == 1 for c in children):
            continue
        pooled = [c for c in children if key_of(c) not in cache and key_of(c) in allowed_keys]
        if len(pooled) == 1:
            uncovered.setdefault(key_of(pooled[0]), 0)
            uncovered[key_of(pooled[0])] += 1

    rows = []
    for index in ELIGIBLE:
        assert index not in ALREADY_10M
        mask = g["s5_masks"][index][0] | g["s5_masks"][index][1] << 64
        invalidated = sorted(s for s, c in enumerate(g["s4_cost"]) if index in c)
        affected = sorted(i2 for i2, s in choices.items() if s in invalidated)
        win_union, win_changed = select(choices, cost, excluded | set(invalidated))
        loss_cost = [set(c) - losses - ({index} if index in c else set())
                     for c in g["s4_cost"]]
        loss_union, loss_changed = select(choices, loss_cost, excluded)
        rows.append(dict(
            index=index, mask=f"{mask:032x}",
            in_plan_union=index in baseline_union,
            uncovered_branches_resolved=uncovered.get(key_of(mask), 0),
            invalidated_classes=len(invalidated),
            affected_choices=len(affected),
            if_win_delta=len(win_union) - len(baseline_union), if_win_changed=win_changed,
            if_loss_delta=len(loss_union) - len(baseline_union), if_loss_changed=loss_changed,
            score=dict(win_cost=len(win_union) - len(baseline_union),
                       loss_benefit=len(baseline_union) - len(loss_union))))
    rows.sort(key=lambda r: (-r["uncovered_branches_resolved"], r["if_win_delta"],
                             r["index"]))
    result = dict(schema="n11-night-candidate-effects-update8-v1",
                  baseline_plan_union=len(baseline_union),
                  already_10m_excluded=sorted(ALREADY_10M),
                  uncovered_branches_total=sum(uncovered.values()),
                  rows=rows,
                  note="if_win_delta is the optimistic union growth when the candidate is a WIN; if_loss_delta is the change when it is a LOSS; both measured on the frozen eighth-update instance")
    target = EXP / "output/candidate-effects.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
