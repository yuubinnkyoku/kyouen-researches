#!/usr/bin/env python3
"""Exhaust exact one/two-witness exchanges of the current 2090 N11 cover.

Only the 92 ordinary five-stone classes form a perfect matching; replacing
two six-stone witnesses can therefore use only the three matchings of their
four freed endpoints. This audits the current, terminal-gated 2090 plan, not
the superseded 2091 plan. Every reported improvement is replayed with the
independent 4x4 integer geometry, never with worker-reported outcomes.
"""
from collections import defaultdict
from itertools import combinations, product
import json

import focus_s7_worker_2090 as focus
import verify_central49_2094_three_swap_descent as geometry
import verify_central49_2154_two_swap_descent as fast
import verify_conditional_s6_cover_46 as base


def need(ok, message):
    if not ok:
        raise ValueError(message)


def audit():
    frontiers, counts, secured = focus.geometry()
    _, s5, incidence, costs, win6, win7, loss7, _ = geometry.context()
    selected = sorted(frontiers)
    chosen = set(selected)
    need(len(chosen) == 46 and len(s5) == 94
         and len(incidence) == 3868 and len(counts) == 2090
         and sum(counts.values()) == 2983 and len(secured) == 6,
         "2090 audited baseline changed")
    need(secured == set(counts) & loss7 and not (chosen & win6)
         and not (set(counts) & win7), "certified evidence conflict")

    source = json.loads((base.HERE / "conditional_s6_cover_46.json").read_text())
    exceptional = {s5.index(base.decode(k))
                   for k in source["excluded_s5_for_cardinality_dual"]}
    need(len(exceptional) == 2, "two exceptional five-stone classes changed")
    ordinary = {s: tuple(sorted(incidence[s] - exceptional))
                for s in incidence}
    need(all(len(pair) == 2 for pair in ordinary.values()),
         "ordinary incidence graph changed")
    need(len({v for s in chosen for v in ordinary[s]}) == 92,
         "selected witnesses no longer form a perfect matching")
    by_pair = defaultdict(list)
    for s, pair in ordinary.items():
        by_pair[pair].append(s)
    need(len(by_pair) == 3792, "candidate pair inventory changed")

    memo = {}
    def frontier(s):
        if s in frontiers:
            return frontiers[s]
        if s not in memo:
            children = fast.fast_frontier(s)
            need(len(children) == costs[s], "3x3 child count changed")
            memo[s] = children
        return memo[s]

    baseline = set(counts)
    checked = feasible = excluded6 = excluded7 = lost_secured = valid = 0
    improving = 0
    best_cost = len(baseline)
    best = None
    for a, b in combinations(selected, 2):
        removed = {a, b}
        vertices = tuple(sorted(ordinary[a] + ordinary[b]))
        need(len(set(vertices)) == 4, "removed ordinary endpoints overlap")
        kept = chosen - removed
        affected = frontiers[a] | frontiers[b]
        lost = {c for c in affected
                if counts[c] == (c in frontiers[a]) + (c in frontiers[b])}
        kept7 = baseline - lost
        kept_exceptional = set().union(*(incidence[s] & exceptional for s in kept))
        pairings = ((vertices[:2], vertices[2:]),
                    ((vertices[0], vertices[2]), (vertices[1], vertices[3])),
                    ((vertices[0], vertices[3]), (vertices[1], vertices[2])))
        for p, q in pairings:
            for x, y in product(by_pair.get(p, ()), by_pair.get(q, ())):
                checked += 1
                additions = {x, y}
                if len(additions) != 2 or additions & kept or additions == removed:
                    continue
                if not exceptional <= (kept_exceptional |
                                       incidence[x] | incidence[y]):
                    continue
                feasible += 1
                if additions & win6:
                    excluded6 += 1
                    continue
                candidate = kept7 | frontier(x) | frontier(y)
                if candidate & win7:
                    excluded7 += 1
                    continue
                if not secured <= candidate:
                    lost_secured += 1
                    continue
                valid += 1
                cost = len(candidate)
                if cost < 2090:
                    improving += 1
                proposal = (tuple(sorted(removed)), tuple(sorted(additions)))
                if cost < best_cost or (cost == best_cost and best is not None
                                       and proposal < best):
                    best_cost, best = cost, proposal

    need(checked >= feasible == excluded6 + excluded7 + lost_secured + valid,
         "candidate accounting mismatch")
    need(valid > 0 and best_cost <= 2090, "no valid audited candidates")
    best_record = None
    if best is not None:
        rm, ad = best
        # Recompute all 46 witness frontiers, using the independent 4x4
        # determinant for both added witnesses; no unverified worker cache.
        independent = {}
        for s in (chosen - set(rm)) | set(ad):
            if s in frontiers:
                independent[s] = frontiers[s]
            else:
                independent[s] = geometry.four_frontier(s)
                need(set(independent[s]) == set(frontier(s)),
                     "3x3/4x4 candidate frontier mismatch")
        union = set().union(*independent.values())
        need(len(union) == best_cost and secured <= union
             and not (union & win7), "independent best-swap check failed")
        best_record = {
            "removed": [f"{s:032x}" for s in rm],
            "added": [f"{s:032x}" for s in ad],
        }
    return {
        "schema": "n11-central49-2090-exact-two-swap-neighborhood-v1",
        "baseline_distinct_s7": 2090,
        "selected_s6": 46,
        "covered_s5": 94,
        "certified_loss7_in_baseline": 6,
        "removed_pairs": 1035,
        "candidate_combinations": checked,
        "rejected_nontrivial_or_exceptional": checked - feasible,
        "geometrically_feasible_nontrivial": feasible,
        "excluded_known_win6": excluded6,
        "excluded_known_win7": excluded7,
        "excluded_lost_certified_loss7": lost_secured,
        "valid_nontrivial": valid,
        "improving_valid_two_swaps": improving,
        "best_distinct_s7": best_cost,
        "best_swap": best_record,
        "conditional_only": True,
        "outcomes": {"s6": "UNKNOWN", "s4": "UNKNOWN",
                     "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"},
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False))
