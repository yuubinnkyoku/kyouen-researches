#!/usr/bin/env python3
"""Independently audit nine conditional 2-for-2 S6 replacements (2309 -> 1984 S7).

Reconstruct the prior 46-S6 certificate chain, recompute all newly selected
S6->S7 edges with separate 4x4 Bareiss integer geometry, and check known
WIN6/WIN7 conflicts. No worker reports or solver verdicts are promoted.
"""
import argparse
import copy
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_conditional_s6_distinct_s7_2309 as previous
import verify_s7_shared_frontier_46 as independent

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_distinct_s7_1984.json"
EXPECTED = [(2945, 2265), (2948, 2217), (2957, 2176),
            (2968, 2135), (2980, 2094), (2994, 2055),
            (2998, 2003), (2985, 1990), (2979, 1984)]
# A separately audited terminal-backed original-first WIN7, in addition to
# the 17 historical inventory and one original-first WIN7 in the fixed14 lift.
EXTRA_WIN7 = "00000000000100001000000042401008"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def source():
    data, selected = previous.predecessor()
    old = json.loads(previous.CERT.read_text(encoding="utf-8"))
    previous.verify(old, data, set(selected))
    removed = {base.decode(k) for k in old["removed_s6_classes"]}
    added = {base.decode(k) for k in old["added_s6_classes"]}
    need(removed <= selected and not (added & selected),
         "prior S6 replacement invalid")
    selected = (set(selected) - removed) | added
    need(len(selected) == 46 and
         set().union(*(data[2][s] for s in selected)) == set(range(94)),
         "prior 2309-S7 cover invalid")
    return data, selected


def known_comparisons():
    old_win7 = independent.inventory(
        independent.BASE / "all_s7_win_17.txt", 17)
    old_loss7 = independent.inventory(
        independent.BASE / "all_s7_loss_2232.txt", 2232)
    lift = json.loads(independent.frozen(independent.LIFT))
    need(lift["schema"] == "n11-fixed14-direct37-s7-lift-v1" and
         (lift["win7"], lift["loss7"], lift["unknown7"],
          lift["winLossConflicts"]) == (13, 1, 0, 0),
         "frozen S7 comparison evidence changed")
    win7 = old_win7 | {r["s7"] for r in lift["rows"]
                       if r["verdict"] == "LOSS"} | {EXTRA_WIN7}
    loss7 = old_loss7 | {r["s7"] for r in lift["rows"]
                         if r["verdict"] == "WIN"}
    need(len(win7) == 19 and not (win7 & loss7),
         "known original-first WIN7/LOSS7 conflict")
    win6 = set()
    for key in win7:
        mask = independent.decode(key, 7)
        need(independent.canonical(mask) == mask, "noncanonical WIN7 key")
        for p in independent.points(mask):
            win6.add(independent.canonical(mask ^ (1 << p)))
    need(len(win6) == 117, "known WIN6 reverse incidence changed")
    # Historical and terminal-backed outcomes are comparison evidence here,
    # not newly terminal-replayed certificates.
    return win6, win7, loss7


def verify(doc, data, selected, comparison, memo=None):
    s4, s5, incidence, cost, *_ = data
    win6, win7, loss7 = comparison
    need(doc["schema"] ==
         "n11-central49-conditional46-nine-two-swap-distinct-s7-1984-v1"
         and doc["source_certificate"] == previous.CERT.name
         and doc["priority_s4_key"] == base.key(s4)
         and doc["evidence_level"] ==
             "GEOMETRY_ONLY_CONDITIONAL_PROOF_PLAN_NOT_VERDICTS"
         and doc["outcomes"] == {
             "s6": "UNKNOWN", "s4": "UNKNOWN",
             "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"},
         "source identity, evidence level or UNKNOWN boundary changed")
    need(len(s5) == 94 and len(selected) == 46 and
         (doc["previous_s6_witnesses"], doc["previous_s5_covered"],
          doc["previous_raw_s7_edges"],
          doc["previous_distinct_s7_classes"]) == (46, 94, 2944, 2309),
         "prior certificate summary changed")
    need(isinstance(doc["steps"], list) and len(doc["steps"]) == 9,
         "expected nine constructive swaps")
    memo = {} if memo is None else memo

    def frontier(witnesses):
        union = set()
        edges = 0
        for s6 in sorted(witnesses):
            if s6 not in memo:
                mask = independent.decode(base.key(s6), 6)
                need(independent.canonical(mask) == mask,
                     "noncanonical selected S6")
                children = independent.children(mask)
                keys = {f"{independent.canonical(c):032x}" for c in children}
                need(len(keys) == len(children) == cost[s6],
                     "4x4 geometry disagrees with S6 child count")
                memo[s6] = keys
            edges += len(memo[s6])
            union.update(memo[s6])
        return edges, union

    edges, union = frontier(selected)
    need((edges, len(union)) == (2944, 2309),
         "prior S7 geometry not independently reconstructed")
    step_results = []
    current = set(selected)
    for i, step in enumerate(doc["steps"]):
        removed = step["removed_s6_classes"]
        added = step["added_s6_classes"]
        need(isinstance(removed, list) and isinstance(added, list)
             and len(removed) == len(added) == 2
             and removed == sorted(set(removed))
             and added == sorted(set(added)), "malformed 2-for-2 swap")
        rm = {base.decode(k) for k in removed}
        ad = {base.decode(k) for k in added}
        need(rm <= current and not (ad & current) and ad <= set(incidence),
             "invalid S6 removal/addition")
        current = (current - rm) | ad
        need(len(current) == 46 and
             set().union(*(incidence[s] for s in current)) == set(range(94)),
             "S5 cover incomplete after swap")
        edges, union = frontier(current)
        need((edges, len(union)) == EXPECTED[i] ==
             (step["raw_s7_edges"], step["distinct_s7_classes"]),
             "independent S7 count differs at swap step")
        step_results.append({"step": i + 1, "raw_s7_edges": edges,
                             "distinct_s7_classes": len(union)})

    win6_conflicts = len(current & win6)
    win7_conflicts = len(union & win7)
    need((doc["final_s6_witnesses"], doc["final_s5_covered"],
          doc["final_raw_s7_edges"], doc["final_distinct_s7_classes"],
          doc["distinct_s7_saved"], doc["shared_s7_reuses"],
          doc["known_win6_conflicts"], doc["known_win7_conflicts"]) ==
         (46, 94, edges, len(union), 2309 - len(union),
          edges - len(union), win6_conflicts, win7_conflicts) ==
         (46, 94, 2979, 1984, 325, 995, 0, 0),
         "final cover, comparison conflicts, or reduction changed")
    return {
        "schema": "n11-central49-conditional46-s7-1984-audit-v1",
        "conditional_only": True,
        "empty_board_outcome": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "s4_outcome": "UNKNOWN",
        "s6_outcomes": "UNKNOWN",
        "s5_covered": 94,
        "selected_s6": 46,
        "previous_distinct_s7": 2309,
        "final_distinct_s7": len(union),
        "distinct_s7_saved": 2309 - len(union),
        "raw_s7_edges": edges,
        "shared_s7_reuses": edges - len(union),
        "known_original_first_win6_conflicts": win6_conflicts,
        "known_original_first_win7_conflicts": win7_conflicts,
        "historical_original_first_loss7_hits": len(union & loss7),
        "steps": step_results,
        "routing_status": "PRIOR_2309_WORKER_ROUTING_INVALID_FOR_NEW_WITNESSES",
        "optimality_claim": "none; nine constructive two-for-two swaps only",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    data, selected = source()
    comparisons = known_comparisons()
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    memo = {}
    result = verify(doc, data, selected, comparisons, memo)
    if args.negative:
        for mutation in ("step_count", "step_edges", "duplicate_removed",
                         "invalid_added", "source", "verdict", "final_count",
                         "fake_win6"):
            bad = copy.deepcopy(doc)
            if mutation == "step_count":
                bad["steps"][3]["distinct_s7_classes"] -= 1
            elif mutation == "step_edges":
                bad["steps"][5]["raw_s7_edges"] += 1
            elif mutation == "duplicate_removed":
                bad["steps"][0]["removed_s6_classes"][1] = (
                    bad["steps"][0]["removed_s6_classes"][0])
            elif mutation == "invalid_added":
                bad["steps"][0]["added_s6_classes"][0] = "f" * 32
            elif mutation == "source":
                bad["source_certificate"] = "unverified.json"
            elif mutation == "verdict":
                bad["outcomes"]["s6"] = "LOSS"
            elif mutation == "final_count":
                bad["final_distinct_s7_classes"] -= 1
            else:
                bad["known_win6_conflicts"] = 1
            try:
                verify(bad, data, selected, comparisons, memo)
            except (ValueError, KeyError, TypeError):
                continue
            raise AssertionError("tampered plan accepted: " + mutation)
        result["negative_tests"] = 8
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
