#!/usr/bin/env python3
"""Exact three-witness exchange audit for the conditional N11 central49 S6 cover.

Every candidate is a perfect matching on the six ordinary S5 vertices freed
by removing three selected S6 witnesses.  This is a GEOMETRIC cover search,
not a WIN/LOSS proof.  Known WIN6 and known WIN7 evidence is exclusion-only.
"""
from collections import Counter, defaultdict
from itertools import combinations, product
import json

import verify_central49_2092_two_swap_local_optimum as local
import verify_second_s7_repair_2092 as prior
import verify_terminal_s7_second_seven_win6 as second


def need(test, msg):
    if not test:
        raise ValueError(msg)


def matchings(vertices):
    """All 15 unordered perfect matchings of six distinct vertices."""
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for j in range(1, len(vertices)):
        b = vertices[j]
        rest = vertices[1:j] + vertices[j+1:]
        for tail in matchings(rest):
            yield ((a, b),) + tail


def audit():
    selected = local.reconstruct()
    need(len(selected) == 46, "wrong selected witness count")
    original = local.read("conditional_s6_cover_46.json")
    s4 = int(original["s4_key"], 16)
    s5 = sorted({local.canonical(c) for c in local.children(s4)})
    need(len(s5) == 94, "priority S5 frontier changed")
    exceptions = {int(k, 16) for k in original["excluded_s5_for_cardinality_dual"]}
    need(len(exceptions) == 2 and exceptions <= set(s5), "dual exceptions changed")
    incidence = defaultdict(set)
    for p in s5:
        for c in local.children(p):
            incidence[local.canonical(c)].add(p)
    need(len(incidence) == 3868, "candidate S6 inventory changed")
    ordinary = set(s5) - exceptions
    need(len(ordinary) == 92, "ordinary S5 vertex count changed")
    need(all(len(covered & ordinary) == 2 for covered in incidence.values()),
         "candidate incidence no longer a 92-vertex edge")
    pair = {k: tuple(sorted(incidence[k] & ordinary)) for k in incidence}
    by_pair = defaultdict(list)
    for k, edge in pair.items():
        by_pair[edge].append(k)
    need(len(by_pair) == 3792, "ordinary S5 graph changed")
    need(len({v for k in selected for v in pair[k]}) == 92,
         "selected witnesses no longer a perfect matching")

    # Historical comparison WIN7 set plus two independently terminal-audited S7.
    # Same evidence inventory as verify_second_s7_repair_2092.py.
    _, _, _, _, _, old_win7 = prior.previous.previous.reconstruct()
    first_terminal = int("00000000000200801002000081000000", 16) | (1 << 43)
    win7 = {int(k, 16) for k in old_win7} | {
        local.canonical(first_terminal), local.canonical(second.S7)
    }
    need(len(win7) == 22, "known WIN7 inventory changed")
    win6 = local.certified_win6()
    need(len(win6) == 21 and not win6.intersection(selected),
         "terminal-certified WIN6 inventory changed")

    # Compute all legal children independently using the 3x3 integer determinant.
    # No search-derived verdict or partial proof number is used.
    frontiers = {k: {local.canonical(c) for c in local.children(k)}
                 for k in sorted(incidence)}
    need(not any(frontiers[k] & win7 for k in selected),
         "baseline contains known WIN7")
    eligible = {k for k in incidence
                if k not in win6 and not (frontiers[k] & win7)}
    need(set(selected) <= eligible, "baseline includes excluded witness")
    choices = defaultdict(list)
    for edge, keys in by_pair.items():
        choices[edge] = sorted(k for k in keys if k in eligible)

    selected_set = set(selected)
    counts = Counter(q for k in selected for q in frontiers[k])
    need(len(counts) == 2092, "baseline S7 union changed")
    baseline = set(counts)
    exmask = {k: sum(1 << j for j, ex in enumerate(sorted(exceptions))
                     if ex in incidence[k]) for k in incidence}
    total = 0
    valid = 0
    improvement = 0
    ties = 0
    minimum = len(baseline)
    best = None
    pairing_count = 0
    possible = 0
    excluded_known = 0
    invalid_exceptions = 0
    # Removing three matched edges frees exactly six ordinary vertices.
    for rem in combinations(selected, 3):
        vertices = tuple(v for k in rem for v in pair[k])
        need(len(set(vertices)) == 6, "nonmatching baseline")
        removed = set(rem)
        kept = selected_set - removed
        # Only S7 classes covered entirely by removed witnesses can disappear.
        affected = frontiers[rem[0]] | frontiers[rem[1]] | frontiers[rem[2]]
        lost = {q for q in affected
                if counts[q] == sum(q in frontiers[k] for k in rem)}
        kept_s7 = baseline - lost
        kept_ex = 0
        for k in kept:
            kept_ex |= exmask[k]
        for matching in matchings(vertices):
            pairing_count += 1
            options = [by_pair.get(tuple(sorted(e)), ()) for e in matching]
            if any(not option for option in options):
                continue
            for ad in product(*options):
                if len(set(ad)) != 3 or any(k in selected_set for k in ad):
                    continue  # Exact three-for-three exchange only.
                total += 1
                if any(k not in eligible for k in ad):
                    excluded_known += 1
                    continue
                if (kept_ex | exmask[ad[0]] | exmask[ad[1]] | exmask[ad[2]]) != 3:
                    invalid_exceptions += 1
                    continue
                valid += 1
                new_s7 = kept_s7 | frontiers[ad[0]] | frontiers[ad[1]] | frontiers[ad[2]]
                cost = len(new_s7)
                if cost < len(baseline):
                    improvement += 1
                elif cost == len(baseline):
                    ties += 1
                proposal = (tuple(sorted(rem)), tuple(sorted(ad)))
                if cost < minimum or (cost == minimum and best is not None
                                      and proposal < best):
                    minimum = cost
                    best = proposal
        possible += 1
    need(possible == 15180 and pairing_count == 227700,
         "three-swap enumeration incomplete")
    result = {
        "schema": "n11-central49-2092-exact-three-swap-audit-v1",
        "selected_s6": 46,
        "ordinary_s5": 92,
        "exceptional_s5": 2,
        "candidate_s6": len(incidence),
        "baseline_distinct_s7": len(baseline),
        "removed_triples": possible,
        "six_vertex_matchings": pairing_count,
        "nontrivial_exact_three_swap_candidates": total,
        "excluded_known_win6_or_win7": excluded_known,
        "excluded_missing_exceptional_s5": invalid_exceptions,
        "valid_exact_three_swap_candidates": valid,
        "improving_candidates": improvement,
        "equal_cost_candidates": ties,
        "best_distinct_s7": minimum,
        "best_swap": None if best is None else {
            "removed": [f"{k:032x}" for k in best[0]],
            "added": [f"{k:032x}" for k in best[1]]
        },
        "conditional_s6_verdict": "UNKNOWN",
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
        "scope": "Exact 3-for-3 neighborhood of the fixed 2092-class matching; not global optimality or a game verdict."
    }
    need(total == valid + excluded_known + invalid_exceptions,
         "candidate accounting mismatch")
    return result


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
