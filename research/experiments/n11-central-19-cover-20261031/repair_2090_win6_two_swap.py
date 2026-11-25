#!/usr/bin/env python3
"""Search exact two-S6 replacements forced to remove certified WIN6 from 2090.

The old 2090 plan omitted K0105's terminal-certified 1984 WIN6 from its
145-class exclusion inventory. This search explicitly excludes that extra
root, preserves all 94 S5 classes and avoids certified WIN7 descendants.
Candidate costs are geometric obligations, not game outcomes.
"""
from collections import defaultdict
from itertools import product
import json

import focus_s7_worker_2090 as focus
import verify_central49_2094_three_swap_descent as geometry
import verify_central49_2154_two_swap_descent as fast
import verify_conditional_s6_cover_46 as base
import verify_focus_s6_win_strategy as win


def need(ok, message):
    if not ok:
        raise ValueError(message)


def audit():
    frontiers, counts, secured = focus.geometry()
    _, s5, incidence, costs, known_win6, known_win7, loss7, _ = geometry.context()
    selected = set(frontiers)
    refuted = win.ROOT
    need(len(selected) == 46 and len(counts) == 2090
         and sum(counts.values()) == 2983 and len(secured) == 6
         and refuted in selected and refuted not in known_win6,
         "2090 omission of terminal-certified WIN6 changed")
    need(secured == set(counts) & loss7 and not (set(counts) & known_win7),
         "2090 terminal-backed S7 baseline changed")
    excluded6 = known_win6 | {refuted}

    source = json.loads((base.HERE / "conditional_s6_cover_46.json").read_text())
    exceptional = {s5.index(base.decode(k))
                   for k in source["excluded_s5_for_cardinality_dual"]}
    need(len(exceptional) == 2, "exceptional S5 inventory changed")
    ordinary = {s: tuple(sorted(incidence[s] - exceptional))
                for s in incidence}
    need(all(len(pair) == 2 for pair in ordinary.values())
         and len({v for s in selected for v in ordinary[s]}) == 92,
         "ordinary perfect matching changed")
    by_pair = defaultdict(list)
    for s, pair in ordinary.items():
        by_pair[pair].append(s)
    need(len(by_pair) == 3792, "candidate incidence changed")

    memo = {}
    def frontier(s):
        if s in frontiers:
            return frontiers[s]
        if s not in memo:
            children = fast.fast_frontier(s)
            need(len(children) == costs[s], "3x3 child count mismatch")
            memo[s] = children
        return memo[s]

    checked = feasible = win6_rejected = win7_rejected = 0
    secured_lost = valid_preserving = valid_relaxed = 0
    best_preserving = best_relaxed = None
    baseline = set(counts)
    for other in sorted(selected - {refuted}):
        removed = {refuted, other}
        vertices = tuple(sorted(ordinary[refuted] + ordinary[other]))
        need(len(set(vertices)) == 4, "removed matching endpoints overlap")
        kept = selected - removed
        affected = frontiers[refuted] | frontiers[other]
        lost = {c for c in affected
                if counts[c] == (c in frontiers[refuted]) + (c in frontiers[other])}
        kept7 = baseline - lost
        exceptional_kept = set().union(*(incidence[s] & exceptional for s in kept))
        pairings = ((vertices[:2], vertices[2:]),
                    ((vertices[0], vertices[2]), (vertices[1], vertices[3])),
                    ((vertices[0], vertices[3]), (vertices[1], vertices[2])))
        for p, q in pairings:
            for x, y in product(by_pair.get(p, ()), by_pair.get(q, ())):
                checked += 1
                added = {x, y}
                if len(added) != 2 or added & kept or added == removed:
                    continue
                if not exceptional <= (exceptional_kept | incidence[x] | incidence[y]):
                    continue
                feasible += 1
                if added & excluded6:
                    win6_rejected += 1
                    continue
                union = kept7 | frontier(x) | frontier(y)
                if union & known_win7:
                    win7_rejected += 1
                    continue
                valid_relaxed += 1
                candidate = (len(union), -len(union & loss7),
                             tuple(sorted(removed)), tuple(sorted(added)))
                if best_relaxed is None or candidate < best_relaxed:
                    best_relaxed = candidate
                if not secured <= union:
                    secured_lost += 1
                    continue
                valid_preserving += 1
                if best_preserving is None or candidate < best_preserving:
                    best_preserving = candidate

    need(checked >= feasible ==
         win6_rejected + win7_rejected + valid_relaxed,
         "candidate rejection accounting changed")
    need(valid_relaxed == secured_lost + valid_preserving,
         "secured LOSS7 retention accounting changed")

    def checked_record(best):
        if best is None:
            return None
        cost, minus_secured, rm, ad = best
        new_selected = (selected - set(rm)) | set(ad)
        need(len(new_selected) == 46 and not (new_selected & excluded6)
             and set().union(*(incidence[s] for s in new_selected))
             == set(range(94)), "repaired 94-S5 cover invalid")
        independent = {}
        for s in new_selected:
            if s in frontiers:
                independent[s] = frontiers[s]
            else:
                independent[s] = geometry.four_frontier(s)
                need(set(independent[s]) == set(frontier(s)),
                     "4x4 and 3x3 new witness frontiers disagree")
        union = set().union(*independent.values())
        need(len(union) == cost and len(union & loss7) == -minus_secured
             and not (union & known_win7),
             "independent 4x4 repaired frontier mismatch")
        return {
            "removed": [f"{s:032x}" for s in rm],
            "added": [f"{s:032x}" for s in ad],
            "raw_s7_edges": sum(map(len, independent.values())),
            "distinct_s7_classes": cost,
            "terminal_proved_loss7": -minus_secured,
            "not_proved_s7": len(union - loss7),
        }

    return {
        "schema": "n11-central49-2090-certified-win6-two-swap-repair-search-v1",
        "source_distinct_s7": 2090,
        "refuted_s6": f"{refuted:032x}",
        "new_known_win6_exclusions": len(excluded6),
        "removed_pairs_examined": len(selected) - 1,
        "candidate_combinations": checked,
        "geometrically_feasible": feasible,
        "excluded_certified_win6": win6_rejected,
        "excluded_certified_win7": win7_rejected,
        "valid_relaxed": valid_relaxed,
        "lost_original_six_terminal_hits": secured_lost,
        "valid_preserving_all_six": valid_preserving,
        "best_preserving": checked_record(best_preserving),
        "best_relaxed": checked_record(best_relaxed),
        "evidence_level": "CONDITIONAL_GEOMETRY_ONLY_NOT_A_WIN_LOSS_VERDICT",
        "s6_outcome": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, sort_keys=True))
