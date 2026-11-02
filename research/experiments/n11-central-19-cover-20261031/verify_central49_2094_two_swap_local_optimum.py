#!/usr/bin/env python3
"""Exact 0/1/2-witness local-optimum audit of the current N11 2094 S7 plan.

The source 2094 certificate, the five complete LOSS7 terminal strategies,
and all selected S6 children are independently checked before this search.
Alternative S6 children use exact 3x3 integer determinants and D4, not
unverified worker receipts. This is a conditional proof-cost result only.
"""
from collections import defaultdict
from itertools import combinations
import json

import focus_s7_worker_2094 as focus
import verify_central49_2094_three_swap_descent as source
import verify_central49_2154_two_swap_descent as geometry
import verify_conditional_s6_cover_46 as base

EXPECTED = {
    "selected_s6": 46,
    "covered_s5": 94,
    "raw_s7_edges": 2987,
    "distinct_s7_classes": 2094,
    "secured_terminal_loss7": 6,
    "checked_two_swap_combinations": 4988,
    "geometrically_feasible_nontrivial": 3808,
    "excluded_certified_win6": 9,
    "excluded_known_win7": 0,
    "valid_nontrivial": 3799,
    "improving_valid_two_swaps": 0,
    "two_swap_local_minimum": 2094,
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def audit():
    # The 2094 source audit uses 4x4 Bareiss, cross-checks 3x3 geometry,
    # and replays all five pinned complete terminal strategies.
    frontiers, multiplicity, secured = focus.geometry()
    _, s5, incidence, costs, win6, win7, loss7, _ = source.context()
    selected = sorted(frontiers)
    need(len(selected) == 46 and len(s5) == 94
         and len(incidence) == 3868 and len(multiplicity) == 2094
         and sum(multiplicity.values()) == 2987 and len(secured) == 6,
         "current 2094 source or terminal evidence changed")
    need(not (set(selected) & win6)
         and not (set(multiplicity) & win7)
         and secured == set(multiplicity) & loss7,
         "certified outcome collision in source")

    source_doc = json.loads((base.HERE / "conditional_s6_cover_46.json").read_text())
    exceptional = {s5.index(base.decode(k))
                   for k in source_doc["excluded_s5_for_cardinality_dual"]}
    need(len(exceptional) == 2, "cardinality exceptions changed")
    ordinary = [p for s in selected for p in incidence[s] - exceptional]
    need(len(ordinary) == len(set(ordinary)) == 92,
         "selected witnesses no longer perfectly match 92 ordinary S5")
    by_pair = defaultdict(list)
    for s, parents in incidence.items():
        pair = tuple(sorted(parents - exceptional))
        need(len(pair) == 2, "candidate S6 has wrong ordinary incidence")
        by_pair[pair].append(s)
    need(len(by_pair) == 3792, "matching graph changed")

    alternative = {}

    def frontier(s):
        if s in frontiers:
            return frontiers[s]
        if s not in alternative:
            # Independent exact 3x3 difference determinant, with D4 quotient.
            ch = geometry.fast_frontier(s)
            need(len(ch) == costs[s],
                 "candidate S6 frontier disagrees with exact source cost")
            alternative[s] = ch
        return alternative[s]

    checked = feasible = rejected6 = rejected7 = valid = improving = 0
    minimum = len(multiplicity)
    for a, b in combinations(selected, 2):
        four = tuple(sorted((incidence[a] | incidence[b]) - exceptional))
        need(len(four) == 4, "ordinary S5 endpoints overlap")
        kept = set(selected) - {a, b}
        kept7 = set().union(*(frontiers[s] for s in kept))
        kept_exceptional = set().union(*(incidence[s] & exceptional
                                         for s in kept))
        pairings = (
            (four[:2], four[2:]),
            ((four[0], four[2]), (four[1], four[3])),
            ((four[0], four[3]), (four[1], four[2])),
        )
        for p1, p2 in pairings:
            for x in by_pair.get(p1, ()):
                for y in by_pair.get(p2, ()):
                    checked += 1
                    # A one-for-one swap is included as a two-for-two
                    # exchange with one original witness retained.
                    if (x == y or x in kept or y in kept
                            or {x, y} == {a, b}):
                        continue
                    if not exceptional <= (
                        kept_exceptional | incidence[x] | incidence[y]
                    ):
                        continue
                    feasible += 1
                    if x in win6 or y in win6:
                        rejected6 += 1
                        continue
                    cx, cy = frontier(x), frontier(y)
                    if (cx | cy) & win7:
                        rejected7 += 1
                        continue
                    valid += 1
                    candidate = kept7 | cx | cy
                    if len(candidate) < minimum:
                        improving += 1
                        minimum = len(candidate)
    result = {
        "selected_s6": len(selected),
        "covered_s5": len(s5),
        "raw_s7_edges": sum(map(len, frontiers.values())),
        "distinct_s7_classes": len(multiplicity),
        "secured_terminal_loss7": len(secured),
        "checked_two_swap_combinations": checked,
        "geometrically_feasible_nontrivial": feasible,
        "excluded_certified_win6": rejected6,
        "excluded_known_win7": rejected7,
        "valid_nontrivial": valid,
        "improving_valid_two_swaps": improving,
        "two_swap_local_minimum": minimum,
    }
    need(result == EXPECTED, "exact two-swap neighborhood changed: "
         + json.dumps(result, sort_keys=True))
    return {
        "schema": "n11-central49-2094-exact-two-swap-neighborhood-v1",
        **result,
        "candidate_frontiers_computed": len(alternative),
        "conditional_only": True,
        "outcomes": {"s6": "UNKNOWN", "s4": "UNKNOWN",
                     "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"},
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
