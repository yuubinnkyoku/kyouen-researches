#!/usr/bin/env python3
"""Exact audit of distinct S7 obligations among raw-edge-optimal 46-S6 covers.

The older 3x3 integer-geometry verifier supplies all 3868 S6 candidates and
an independently checked LP dual. Complementary slackness restricts any
2897-edge optimum to tight columns with exact coverage of positive-dual S5.
We enumerate ALL such 46-column covers without an optimizer, then count
their distinct S7 children using the separate 4x4 Bareiss implementation.

This is a conditional geometry plan, NOT a game-outcome certificate.
"""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_s7_shared_frontier_46 as independent

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_shared_s7_optimal.json"
OLD = HERE / "conditional_s6_cover_46.json"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def tight_reduction(data, old):
    _, s5, incidence, cost, *_ = data
    dual = old["weighted_optimality_dual"]
    y = dual["s5_weights_by_sorted_key"]
    lam = dual["lambda_for_exactly_46"]
    need(len(s5) == len(y) == 94 and lam == 39, "dual identity")
    tight = {
        s6 for s6, parents in incidence.items()
        if cost[s6] == lam + sum(y[i] for i in parents)
    }
    need(len(tight) == 113, "tight-column count changed")
    positive = {i for i, weight in enumerate(y) if weight > 0}
    zero = set(range(94)) - positive
    need(len(positive) == 90 and len(zero) == 4, "dual support changed")

    # For an optimum meeting the dual bound, every positive-weight S5
    # must be covered EXACTLY once. A uniquely incident tight S6 is forced.
    remaining = set(tight)
    forced = set()
    covered = set()
    zero_covered = set()
    while True:
        newly_forced = set()
        for i in sorted(positive - covered):
            options = [s6 for s6 in remaining if i in incidence[s6]]
            need(options, f"uncoverable positive-dual S5 {i}")
            if len(options) == 1:
                newly_forced.add(options[0])
        if not newly_forced:
            break
        for s6 in sorted(newly_forced):
            pos = incidence[s6] & positive
            need(not (pos & covered), "forced positive-dual overlap")
            covered.update(pos)
            zero_covered.update(incidence[s6] & zero)
        forced.update(newly_forced)
        remaining = {
            s6 for s6 in remaining - newly_forced
            if not (incidence[s6] & covered)
        }

    need(len(forced) == 31 and len(remaining) == 39,
         "forced-column reduction changed")
    positive_left = sorted(positive - covered)
    need(len(positive_left) == 29, "residual dual support changed")
    need(all(incidence[s6] & positive for s6 in remaining),
         "zero-only tight column requires a separate enumeration")
    return forced, remaining, positive_left, zero, zero_covered


def enumerate_optima(data, reduction):
    _, _, incidence, _, *_ = data
    forced, remaining, positive_left, zero, zero_covered = reduction
    ordered = sorted(remaining)
    index = {i: bit for bit, i in enumerate(positive_left)}
    masks = {
        s6: sum(1 << index[i] for i in incidence[s6] if i in index)
        for s6 in ordered
    }
    by_bit = [
        [s6 for s6 in ordered if masks[s6] & (1 << bit)]
        for bit in range(len(positive_left))
    ]
    full = (1 << len(positive_left)) - 1
    required = 46 - len(forced)
    need(required == 15, "residual column count changed")
    solutions = []

    def search(covered_mask, selected):
        if covered_mask == full:
            if (len(selected) == required
                    and zero <= (zero_covered | set().union(
                        *(incidence[s6] & zero for s6 in selected)))):
                solutions.append(frozenset(selected))
            return
        if len(selected) >= required:
            return
        # Minimum remaining choices; exact positive-dual cover.
        best = None
        for bit in range(len(positive_left)):
            if covered_mask & (1 << bit):
                continue
            options = [
                s6 for s6 in by_bit[bit]
                if not (masks[s6] & covered_mask)
            ]
            if best is None or len(options) < len(best):
                best = options
                if len(best) <= 1:
                    break
        if not best:
            return
        for s6 in best:
            search(covered_mask | masks[s6], selected + [s6])

    search(0, [])
    need(len(solutions) == len(set(solutions)) == 12,
         "exact enumeration of dual-optimal covers changed")
    for sol in solutions:
        need(len(sol) == required, "invalid residual solution")
    return solutions


def verify(doc, old, data, reduction, solutions):
    _, s5, incidence, cost, *_ = data
    forced, remaining, positive_left, zero, _ = reduction
    need(doc["schema"] ==
         "n11-central49-conditional46-minimum-distinct-s7-among-raw-optima-v1"
         and doc["source_certificate"] == OLD.name
         and doc["priority_s4_key"] == base.key(data[0])
         and doc["evidence_level"] ==
         "GEOMETRY_ONLY_CONDITIONAL_PROOF_PLAN_NOT_VERDICTS"
         and doc["outcomes"] == {
             "s4": "UNKNOWN", "s6": "UNKNOWN",
             "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"
         }, "certificate identity, scope or verdict changed")
    need((doc["tight_s6_candidates"], doc["dual_forced_s6"],
          doc["residual_candidates"], doc["residual_positive_s5"],
          doc["residual_required_s6"], doc["all_dual_optimal_46_covers"])
         == (113, 31, 39, 29, 15, 12),
         "reduction summary changed")
    flex_keys = doc["flexible_s6_classes"]
    need(isinstance(flex_keys, list) and len(flex_keys) == 15
         and flex_keys == sorted(set(flex_keys)),
         "flexible S6 keys must be 15 sorted unique canonical strings")
    flex = {base.decode(k) for k in flex_keys}
    need(flex <= remaining and frozenset(flex) in solutions,
         "selected flexible S6 are not an optimal exact cover")
    chosen = forced | flex
    need(len(chosen) == 46
         and set().union(*(incidence[s6] for s6 in chosen)) == set(range(94))
         and sum(cost[s6] for s6 in chosen) == 2897,
         "invalid conditional S6 cover")

    # Reconstruct S7 children with independent 4x4 integer geometry.
    all_candidates = forced | remaining
    s7_sets = {}
    for s6 in sorted(all_candidates):
        m = independent.decode(base.key(s6), 6)
        need(independent.canonical(m) == m, "noncanonical S6")
        raw = independent.children(m)
        keys = {f"{independent.canonical(c):032x}" for c in raw}
        need(len(raw) == cost[s6] and len(keys) == len(raw),
             "independent S7 geometry disagrees with 3x3 cost")
        s7_sets[s6] = keys

    common = set().union(*(s7_sets[s6] for s6 in forced))
    distinct = []
    for flex_solution in solutions:
        union = set(common)
        for s6 in flex_solution:
            union.update(s7_sets[s6])
        distinct.append((len(union), flex_solution))
    best = min(value for value, _ in distinct)
    best_solutions = [s for value, s in distinct if value == best]
    need(best == 2662 and len(best_solutions) == 1
         and best_solutions[0] == frozenset(flex),
         "saved plan does not minimize distinct S7 among raw optima")

    old_selected = {base.decode(k) for k in old["selected_s6_classes"]}
    need(len(old_selected) == 46 and old_selected <= all_candidates,
         "old plan not in dual-optimal candidate family")
    old_s7 = set().union(*(s7_sets[s6] for s6 in old_selected))
    new_s7 = set(common)
    for s6 in flex:
        new_s7.update(s7_sets[s6])
    need(len(old_s7) == 2737 and len(new_s7) == 2662
         and (doc["selected_s6_count"], doc["raw_s7_edges"],
              doc["previous_distinct_s7"], doc["new_distinct_s7"],
              doc["shared_s7_reuses"], doc["unique_best_s7_cover_count"])
         == (46, 2897, 2737, 2662, 235, 1),
         "S7-sharing counts changed")

    # Frozen evidence is a comparison only. Do not promote old solver
    # labels to independently terminal-verified verdicts.
    old_loss = independent.inventory(
        independent.BASE / "all_s7_loss_2232.txt", 2232)
    old_win = independent.inventory(
        independent.BASE / "all_s7_win_17.txt", 17)
    lift = json.loads(independent.frozen(independent.LIFT))
    need(lift["schema"] == "n11-fixed14-direct37-s7-lift-v1"
         and (lift["win7"], lift["loss7"], lift["unknown7"],
              lift["winLossConflicts"]) == (13, 1, 0, 0),
         "fixed14 polarity changed")
    loss7 = old_loss | {r["s7"] for r in lift["rows"]
                        if r["verdict"] == "WIN"}
    win7 = old_win | {r["s7"] for r in lift["rows"]
                      if r["verdict"] == "LOSS"}
    need(not (loss7 & win7), "WIN7/LOSS7 conflict")
    loss_hits, win_hits = len(new_s7 & loss7), len(new_s7 & win7)
    need((loss_hits, win_hits) == (6, 0)
         and (doc["frozen_loss7_hits"], doc["known_win7_hits"]) == (6, 0),
         "new plan conflicts with frozen S7 evidence")

    return {
        "schema": "n11-central49-conditional46-distinct-s7-optimal-audit-v1",
        "s4_outcome": "UNKNOWN",
        "s6_outcomes": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
        "tight_candidates": len(forced | remaining) + (
            doc["tight_s6_candidates"] - len(forced | remaining)),
        "forced_s6": len(forced),
        "residual_candidates": len(remaining),
        "exact_raw_optimal_46_covers": len(solutions),
        "distinct_s7_per_cover": dict(sorted(Counter(
            n for n, _ in distinct).items())),
        "raw_s7_edges": sum(cost[s6] for s6 in chosen),
        "old_distinct_s7": len(old_s7),
        "new_distinct_s7": len(new_s7),
        "saved_s7_obligations": len(old_s7) - len(new_s7),
        "shared_s7_obligations": 2897 - len(new_s7),
        "solver_trusted_loss7_overlap": loss_hits,
        "known_win7_overlap": win_hits,
        "conditional_only": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    old = json.loads(OLD.read_text(encoding="utf-8"))
    data = base.reconstruct()
    base.verify(old, data)
    reduction = tight_reduction(data, old)
    solutions = enumerate_optima(data, reduction)
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    result = verify(doc, old, data, reduction, solutions)
    if args.negative:
        for field, bad in (
            ("new_distinct_s7", 2663),
            ("known_win7_hits", 1),
            ("flexible_s6_classes", doc["flexible_s6_classes"][:14]
             + [doc["flexible_s6_classes"][0]]),
        ):
            modified = copy.deepcopy(doc)
            modified[field] = bad
            try:
                verify(modified, old, data, reduction, solutions)
            except (ValueError, KeyError, TypeError):
                continue
            raise AssertionError(f"tampered {field} accepted")
        result["negative_tests"] = 3
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
