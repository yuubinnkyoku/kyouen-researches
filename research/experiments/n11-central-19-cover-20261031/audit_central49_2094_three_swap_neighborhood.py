#!/usr/bin/env python3
"""Exhaust all exact three-witness exchanges from the certified 2094 cover.

The 92 ordinary five-stone classes form a perfect matching. Removing three
selected six-stone witnesses frees six endpoints with exactly 15 matchings.
All alternatives use exact integer 3x3 circle geometry and D4 reduction;
the 2094 baseline and the best 2093 replacement are separately checked
using 4x4 Bareiss and five complete terminal strategy replays.
"""
from collections import defaultdict
from itertools import combinations, product
import json

import focus_s7_worker_2094 as focus
import verify_central49_2094_three_swap_descent as source
import verify_central49_2154_two_swap_descent as geometry
import verify_central49_2093_three_swap as next_plan
import verify_conditional_s6_cover_46 as base


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    for i in range(1, len(vertices)):
        rest = vertices[1:i] + vertices[i + 1:]
        for tail in matchings(rest):
            yield ((vertices[0], vertices[i]),) + tail


def audit():
    frontiers, counts, secured = focus.geometry()
    _, s5, incidence, costs, win6, win7, loss7, _ = source.context()
    selected = sorted(frontiers)
    selected_set = set(selected)
    need(len(selected) == 46 and len(counts) == 2094
         and len(secured) == 6 and len(s5) == 94
         and len(incidence) == 3868, "2094 source changed")

    original = json.loads((base.HERE / "conditional_s6_cover_46.json").read_text())
    exceptional = {s5.index(base.decode(k))
                   for k in original["excluded_s5_for_cardinality_dual"]}
    need(len(exceptional) == 2, "cardinality exceptions changed")
    ordinary = {s: tuple(sorted(incidence[s] - exceptional))
                for s in incidence}
    need(all(len(pair) == 2 for pair in ordinary.values()),
         "ordinary five-stone graph changed")
    by_pair = defaultdict(list)
    for s, pair in ordinary.items():
        by_pair[pair].append(s)
    need(len(by_pair) == 3792 and
         len({p for s in selected for p in ordinary[s]}) == 92,
         "selected matching or candidate graph changed")

    memo = {}
    def frontier(s):
        if s in frontiers:
            return frontiers[s]
        if s not in memo:
            ch = geometry.fast_frontier(s)
            need(len(ch) == costs[s], "candidate frontier cost changed")
            memo[s] = ch
        return memo[s]

    checked = feasible = excluded6 = excluded7 = valid = improving = 0
    minimum = 2094
    best = None
    removed_triples = matching_count = 0
    baseline = set(counts)
    for rem in combinations(selected, 3):
        removed_triples += 1
        vertices = tuple(sorted(p for s in rem for p in ordinary[s]))
        need(len(vertices) == len(set(vertices)) == 6,
             "removed matching has duplicate endpoint")
        remset = set(rem)
        kept = selected_set - remset
        affected = set().union(*(frontiers[s] for s in rem))
        lost = {c for c in affected
                if counts[c] == sum(c in frontiers[s] for s in rem)}
        kept7 = baseline - lost
        kept_exc = set().union(*(incidence[s] & exceptional for s in kept))
        for matching in matchings(vertices):
            matching_count += 1
            options = [by_pair.get(tuple(sorted(pair)), ()) for pair in matching]
            for ad in product(*options):
                checked += 1
                adset = set(ad)
                if (len(adset) != 3
                        or any(s in selected_set and s not in remset for s in ad)
                        or adset == remset):
                    continue
                if not exceptional <= (
                    kept_exc | incidence[ad[0]] | incidence[ad[1]]
                    | incidence[ad[2]]
                ):
                    continue
                feasible += 1
                if adset & win6:
                    excluded6 += 1
                    continue
                children = [frontier(s) for s in ad]
                new = children[0] | children[1] | children[2]
                if new & win7:
                    excluded7 += 1
                    continue
                valid += 1
                cost = len(kept7) + len(new - kept7)
                if cost < 2094:
                    improving += 1
                if cost < minimum:
                    minimum = cost
                    best = (tuple(sorted(rem)), tuple(sorted(ad)))

    need(removed_triples == 15180 and matching_count == 227700,
         "three-witness neighborhood enumeration incomplete")
    need((checked, feasible, excluded6, excluded7, valid, improving,
          minimum) == (313629, 283361, 1455, 0, 281906, 1, 2093),
         "exact three-witness neighborhood counts changed")
    need(checked >= feasible == excluded6 + excluded7 + valid,
         "candidate accounting mismatch")
    certificate = json.loads(next_plan.CERT.read_text(encoding="utf-8"))
    next_plan.audit(certificate)  # Separate 4x4 + terminal independent replay.
    need(best is not None and
         [f"{s:032x}" for s in best[0]] == certificate["removed"] and
         [f"{s:032x}" for s in best[1]] == certificate["added"],
         "best improving three-swap disagrees with independent 2093 proof")
    return {
        "schema": "n11-central49-2094-exact-three-swap-neighborhood-v1",
        "removed_triples": removed_triples,
        "six_vertex_matchings": matching_count,
        "candidate_combinations": checked,
        "geometrically_feasible_nontrivial": feasible,
        "excluded_certified_win6": excluded6,
        "excluded_known_win7": excluded7,
        "valid_nontrivial": valid,
        "improving_valid_three_swaps": improving,
        "best_distinct_s7": minimum,
        "best_swap": {"removed": certificate["removed"],
                      "added": certificate["added"]},
        "conditional_only": True,
        "outcomes": {"s6": "UNKNOWN", "s4": "UNKNOWN",
                     "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"},
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
