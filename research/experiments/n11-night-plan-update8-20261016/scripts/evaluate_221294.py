"""Priority re-evaluation of the conflict candidate 221294 on the eighth-update
plan (WIN and LOSS counterfactuals, measured -- not the old update7 ranking).

Both directions are measured on the frozen update8 instance:

* WIN: every S4 class whose legal-child cost contains 221294 is excluded, the
  affected selected groups are re-selected by the same greedy repair, and the
  optimistic union delta plus the freed stored branches are reported.
* LOSS: 221294 leaves every cost set, and the union delta plus the branches
  that lose their sole stored witness are reported.

Branches are the open S4 boundaries of the plan's chosen thirds; a branch's
allowed witnesses are its canonical unknown fifth-stone children inside the
update8 allowed pool (stored masks minus layered verdicts).  Winning a
candidate is only useful if it frees or closes such a branch; the exploration
decision is therefore based on the measured effect, not on the raw count of
S4 classes that mention the candidate.
"""
from __future__ import annotations

import gzip
import hashlib
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
sys.path.insert(0, str(ROOT / "research/experiments/n11-s7-fifth-terminal-20261015"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache  # noqa: E402
from s4_win_polarity import verdict_of, classify_s4, OPEN  # noqa: E402
from fifth_verify_standalone import canonical, points  # noqa: E402

CANDIDATE = 221294


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
    wins = {i for i, v in verdicts.items() if v == 1}
    cost = [set(c) - losses for c in g["s4_cost"]]
    stored = json.loads((COST_CMP / "output/win-witness-masks.json").read_text())
    stored_masks = {lo | (hi << 64) for lo, hi in stored["witness_masks"]}
    known_masks = {g["s5_masks"][i][0] | g["s5_masks"][i][1] << 64 for i in verdicts}
    allowed = stored_masks - known_masks
    candidate_mask = g["s5_masks"][CANDIDATE][0] | g["s5_masks"][CANDIDATE][1] << 64

    def select(seed, cost_table, excluded_set):
        chosen = {ident: s for ident, s in seed.items() if s not in excluded_set}
        union = set().union(*(cost_table[s] for s in chosen.values()))
        changed = 0
        for ident in sorted(seed):
            if ident in chosen:
                continue
            before = len(union)
            s = min((t for t in options[ident] if t not in excluded_set),
                    key=lambda t: (len(cost_table[t] - union), len(cost_table[t]), t))
            chosen[ident] = s
            union |= cost_table[s]
            changed += 1
        return chosen, union, changed

    options = {}
    for root in g["roots"]:
        if root["role"] == "known-loss-baseline":
            continue
        for row in root["thirds"]:
            options[(root["origin_first"], root["origin_reply"], row["third"])] = \
                [s for s in row["options"] if s not in excluded]
    assert set(options) == set(choices)

    base_union = set().union(*(cost[s] for s in choices.values()))
    assert base_union == baseline_union

    invalidated = sorted(s for s, c in enumerate(g["s4_cost"]) if CANDIDATE in c)
    affected = sorted(ident for ident, s in choices.items() if s in invalidated)
    win_choices, win_union, win_changed = select(choices, cost,
                                                 excluded | set(invalidated))
    loss_cost = [set(c) - losses - ({CANDIDATE} if CANDIDATE in c else set())
                 for c in g["s4_cost"]]
    loss_choices, loss_union, loss_changed = select(choices, loss_cost, excluded)

    board = Board(11)
    cache = load_exact_s5_cache(board)
    for i, v in verdicts.items():
        cache[tuple(g["s5_masks"][i])] = {"verdict": v}
    allowed_keys = {key_of(m) for m in allowed}
    sole_witness_branches = 0
    freed_or_broken_classes = set()
    pairs_of = {}
    for root in g["roots"]:
        if root["role"] == "known-loss-baseline":
            continue
        pairs_of[(root["origin_first"], root["origin_reply"])] = \
            root["pair_mask"][0] | root["pair_mask"][1] << 64
    for ident, s in choices.items():
        mask = g["s4_masks"][s][0] | g["s4_masks"][s][1] << 64
        children = board.children(mask)
        if any(verdict_of(cache, key_of(c)) == 1 for c in children):
            continue
        unknown = [c for c in children if key_of(c) not in cache
                   and key_of(c) in allowed_keys]
        if unknown == [candidate_mask]:
            sole_witness_branches += 1
            freed_or_broken_classes.add(s)
    baseline_broken = sum(1 for s in choices.values() if s in wins)

    result = dict(
        schema="n11-night-candidate-recheck-221294-update8-v1",
        candidate=dict(index=CANDIDATE, mask=f"{candidate_mask:032x}",
                       in_plan_union=CANDIDATE in baseline_union,
                       in_cost_classes=len(invalidated),
                       invalidated_classes=invalidated,
                       affected_selected_choices=len(affected),
                       affected_choices=[list(a) for a in affected]),
        measured_on="repaired-joint-plan-update8.json",
        baseline=dict(plan_union=len(baseline_union),
                      plan_union_sha=hashlib.sha256(
                          ",".join(map(str, sorted(baseline_union))).encode()).hexdigest(),
                      broken_selected_classes=baseline_broken,
                      changed_choice_count=plan["changed_choice_count"]),
        if_win=dict(union_size=len(win_union), union_delta=len(win_union) - len(baseline_union),
                    changed_choices=win_changed,
                    newly_excluded_classes=sorted(set(invalidated) - excluded),
                    freed_stored_branches=sole_witness_branches,
                    freed_branch_classes=sorted(freed_or_broken_classes)),
        if_loss=dict(union_size=len(loss_union), union_delta=len(loss_union) - len(baseline_union),
                     changed_choices=loss_changed,
                     broken_stored_branches=sole_witness_branches),
        interpretation=(
            "these are the update8-relative measured effects; the earlier "
            "update7 ranking values (8 affected choices, greedy delta +111) are "
            "not valid deltas for the joint plan and are not reused"),
        seconds=None,
    )
    target = EXP / "output/candidate-recheck-221294.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
