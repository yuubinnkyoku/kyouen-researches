#!/usr/bin/env python3
"""Exact <=2-witness neighborhood after the N11 central49 1985-class chain.

The 3x3 integer determinant generates candidate frontiers.  This is a
conditional geometric cover search, not a WIN/LOSS certificate.
"""
from collections import Counter, defaultdict
from itertools import combinations, product
import json

import verify_central49_2092_two_swap_local_optimum as local
import verify_second_s7_repair_2092 as prior
import verify_terminal_s7_second_seven_win6 as second


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def audit():
    doc = local.read("conditional_s6_cover_46_three_swap_chain.json")
    selected = set(local.reconstruct())
    for step in doc["steps"]:
        rm = {int(k, 16) for k in step["removed"]}
        ad = {int(k, 16) for k in step["added"]}
        need(len(rm) == len(ad) == 3 and rm <= selected and not (ad & selected),
             "invalid chain")
        selected = (selected - rm) | ad
    need(len(selected) == 46 and local.digest(selected)
         == doc["final_selected_s6_sha256"]
         == "f72c587537cbe2239b0f077545dfd14628298d2fe6d7c6b80ac7345ff46b6026",
         "1985 selection identity changed")
    selected = sorted(selected)
    s4 = int(local.read("conditional_s6_cover_46.json")["s4_key"], 16)
    s5 = {local.canonical(c) for c in local.children(s4)}
    exceptions = {int(k, 16) for k in local.read("conditional_s6_cover_46.json")[
        "excluded_s5_for_cardinality_dual"]}
    incidence = defaultdict(set)
    for p in s5:
        for c in local.children(p):
            incidence[local.canonical(c)].add(p)
    need(len(s5) == 94 and len(exceptions) == 2 and len(incidence) == 3868,
         "S5/S6 incidence changed")
    ordinary = s5 - exceptions
    pair = {k: tuple(sorted(v & ordinary)) for k, v in incidence.items()}
    need(all(len(v) == 2 for v in pair.values()), "not dual-tight")
    by_pair = defaultdict(list)
    for k, edge in pair.items():
        by_pair[edge].append(k)
    need(len(by_pair) == 3792, "candidate graph changed")
    need(len({v for k in selected for v in pair[k]}) == 92,
         "selection is not a perfect matching")
    _, _, _, old_win6, first_parents, old_win7 = prior.previous.previous.reconstruct()
    win6 = old_win6 | first_parents | local.certified_win6()
    first_s7 = int("00000000000200801002000081000000", 16) | (1 << 43)
    win7 = {int(k, 16) for k in old_win7} | {
        local.canonical(first_s7), local.canonical(second.S7)}
    need(len(win6) == 139 and len(win7) == 22, "WIN inventory changed")
    memo = {}
    def frontier(k):
        if k not in memo:
            memo[k] = {local.canonical(c) for c in local.children(k)}
        return memo[k]
    baseline = Counter(q for k in selected for q in frontier(k))
    need(len(baseline) == 1985 and not (set(baseline) & win7),
         "1985 S7 frontier changed")
    kept_selection = set(selected)
    exmask = {k: sum(1 << j for j, ex in enumerate(sorted(exceptions))
                     if ex in incidence[k]) for k in incidence}
    total = feasible = rejected_known = valid = better = ties = 0
    minimum = len(baseline)
    best = None
    for a, b in combinations(selected, 2):
        endpoints = pair[a] + pair[b]
        need(len(set(endpoints)) == 4, "nonmatching selected edges")
        kept = kept_selection - {a, b}
        kept_ex = 0
        for k in kept:
            kept_ex |= exmask[k]
        affected = frontier(a) | frontier(b)
        lost = {q for q in affected if baseline[q] ==
                int(q in frontier(a)) + int(q in frontier(b))}
        kept_s7 = set(baseline) - lost
        u, v, w, z = endpoints
        for matching in (((u, v), (w, z)), ((u, w), (v, z)),
                         ((u, z), (v, w))):
            opts = [by_pair.get(tuple(sorted(edge)), ()) for edge in matching]
            for x, y in product(*opts):
                if x == y or x in kept or y in kept or {x, y} == {a, b}:
                    continue
                total += 1
                if (kept_ex | exmask[x] | exmask[y]) != 3:
                    continue
                feasible += 1
                if x in win6 or y in win6 or (frontier(x) | frontier(y)) & win7:
                    rejected_known += 1
                    continue
                valid += 1
                cost = len(kept_s7 | frontier(x) | frontier(y))
                if cost < len(baseline):
                    better += 1
                elif cost == len(baseline):
                    ties += 1
                proposal = (tuple(sorted((a, b))), tuple(sorted((x, y))))
                if cost < minimum or (cost == minimum and best is not None
                                      and proposal < best):
                    minimum = cost
                    best = proposal
    need(total == feasible + (total - feasible)
         and feasible == rejected_known + valid, "accounting mismatch")
    return {
        "schema": "n11-central49-1985-exact-up-to-two-swap-audit-v1",
        "source_selected_s6_sha256": local.digest(selected),
        "baseline_distinct_s7": 1985,
        "removed_pairs": 1035,
        "nontrivial_candidate_pairs": total,
        "exception_cover_feasible": feasible,
        "excluded_known_win6_or_win7": rejected_known,
        "valid_candidate_pairs": valid,
        "improving_candidates": better,
        "equal_cost_candidates": ties,
        "best_distinct_s7": minimum,
        "best_swap": None if best is None else {
            "removed": [f"{k:032x}" for k in best[0]],
            "added": [f"{k:032x}" for k in best[1]]
        },
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
        "scope": "Exact <=2 witness replacements of the 1985 S7 conditional cover; no game verdict."
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
