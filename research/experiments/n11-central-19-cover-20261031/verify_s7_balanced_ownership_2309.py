#!/usr/bin/env python3
"""Independently audit balanced, unique S7 ownership for 46 conditional S6 roots.

This does NOT solve S6 positions. It reuses the existing 4x4-integer-geometry
certificate-chain auditor, then assigns each distinct canonical S7 obligation
to exactly one worker. Remote S6 dependencies require verified shared results.
"""
import argparse
from collections import defaultdict
import copy
import json
from pathlib import Path

import verify_s6_worker_partition_2309 as previous

HERE = Path(__file__).resolve().parent
PLAN = HERE / "conditional_s6_cover_46_balanced_s7_ownership_2309.json"
OLD = HERE / "conditional_s6_cover_46_s7_locality_workers_2309.json"
POLICY = (
    "canonical_s7_sorted__least_current_owned_load_among_s6_workers__"
    "tie_lowest_worker_id"
)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def allocation(assignment, s7_sets):
    need(len(assignment) == len(s7_sets) == 46
         and all(type(w) is int and 0 <= w < 4 for w in assignment),
         "invalid S6 worker allocation")
    raw, distinct, cross = previous.statistics(assignment, s7_sets)
    counts = [assignment.count(w) for w in range(4)]
    owners = defaultdict(set)
    for worker, s7s in zip(assignment, s7_sets):
        for s7 in s7s:
            owners[s7].add(worker)
    need(len(owners) == 2309 and sum(map(len, s7_sets)) == 2944,
         "source S7 frontier changed")
    exclusive = [0] * 4
    remote = []
    owner_by_s7 = {}
    for s7, workers in owners.items():
        need(1 <= len(workers) <= 2, "unexpected S7 worker multiplicity")
        if len(workers) == 1:
            worker = next(iter(workers))
            exclusive[worker] += 1
            owner_by_s7[s7] = worker
        else:
            remote.append((s7, sorted(workers)))
    owned = exclusive.copy()
    # Every shared S7 is computed by one of its S6 workers. The other
    # worker must obtain the verified result through a conflict-checked cache.
    for s7, eligible in sorted(remote):
        worker = min(eligible, key=lambda w: (owned[w], w))
        need(s7 not in owner_by_s7, "duplicate S7 owner")
        owner_by_s7[s7] = worker
        owned[worker] += 1
    within = 2944 - 2309 - cross
    need(len(remote) == cross and sum(owned) == len(owner_by_s7) == 2309
         and sum(exclusive) + cross == 2309
         and within + cross == 2944 - 2309,
         "S7 ownership or overlap conservation failed")
    return {
        "worker_s6_counts": counts,
        "worker_raw_loads": raw,
        "worker_exclusive_s7": exclusive,
        "worker_owned_s7": owned,
        "cross_worker_s7_dependencies": cross,
        "within_worker_shared_s7": within,
        "distinct_s7": len(owner_by_s7),
    }, owner_by_s7


def verify(plan, old, s7_sets):
    need(plan["schema"] == "n11-central49-conditional46-balanced-s7-ownership-v1"
         and plan["source_partition"] == OLD.name
         and plan["source_certificate"] == previous.CERT.name
         and plan["owner_policy"] == POLICY
         and plan["evidence_level"] ==
         "GEOMETRY_ONLY_CONDITIONAL_PROOF_SCHEDULING_NOT_VERDICTS"
         and plan["outcomes"] == {
             "s6": "UNKNOWN", "s4": "UNKNOWN",
             "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"},
         "plan identity, ownership policy, or evidence boundary changed")
    old_stats, old_owners = allocation(old["worker_index_by_sorted_s6"], s7_sets)
    new_stats, new_owners = allocation(plan["worker_index_by_sorted_s6"], s7_sets)
    old_summary = {
        k: old_stats[k] for k in (
            "worker_raw_loads", "worker_exclusive_s7",
            "worker_owned_s7", "cross_worker_s7_dependencies")
    }
    need(plan["baseline_locality"] == old_summary
         and old_summary == {
             "worker_raw_loads": [726, 736, 745, 737],
             "worker_exclusive_s7": [517, 735, 330, 327],
             "worker_owned_s7": [525, 735, 524, 525],
             "cross_worker_s7_dependencies": 400},
         "old ownership baseline changed")
    need(plan["balanced_ownership"] == new_stats
         and new_stats == {
             "worker_s6_counts": [12, 12, 11, 11],
             "worker_raw_loads": [748, 759, 715, 722],
             "worker_exclusive_s7": [460, 445, 462, 460],
             "worker_owned_s7": [578, 577, 577, 577],
             "cross_worker_s7_dependencies": 482,
             "within_worker_shared_s7": 153,
             "distinct_s7": 2309},
         "balanced S7 owner counts changed")
    need(all(715 <= x <= 760 for x in new_stats["worker_raw_loads"])
         and max(new_stats["worker_owned_s7"]) == 578
         and max(new_stats["worker_owned_s7"]) <
             max(old_stats["worker_owned_s7"])
         and set(new_owners) == set(old_owners),
         "balance, coverage, or claimed improvement invalid")
    return {
        "schema": "n11-central49-balanced-s7-ownership-audit-v1",
        "conditional_only": True,
        "empty_board_outcome": "UNKNOWN",
        "s6_outcomes": "UNKNOWN",
        "s6_witnesses": 46,
        "distinct_s7": len(new_owners),
        "baseline_max_owned_s7": max(old_stats["worker_owned_s7"]),
        "balanced_max_owned_s7": max(new_stats["worker_owned_s7"]),
        "baseline_cross_worker_dependencies": old_stats[
            "cross_worker_s7_dependencies"],
        "balanced_cross_worker_dependencies": new_stats[
            "cross_worker_s7_dependencies"],
        "baseline": old_stats,
        "balanced": new_stats,
        "caveat": "A static routing plan only; no S6 verdict or runtime speedup.",
    }, new_owners


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    parser.add_argument("--worklist", type=int, choices=range(4),
                        help="print verified canonical S7 keys owned by one worker")
    args = parser.parse_args()
    witnesses = previous.source_witnesses()
    s7_sets = previous.frontier(witnesses)
    old = json.loads(OLD.read_text(encoding="utf-8"))
    previous.verify(old, witnesses, s7_sets)
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    result, owner_by_s7 = verify(plan, old, s7_sets)
    if args.negative:
        tests = 0
        for mutation in ("bad_worker", "bad_policy", "bad_verdict",
                         "bad_balance", "bad_baseline"):
            bad = copy.deepcopy(plan)
            if mutation == "bad_worker":
                bad["worker_index_by_sorted_s6"][0] = 0
            elif mutation == "bad_policy":
                bad["owner_policy"] = "hash_mod_four"
            elif mutation == "bad_verdict":
                bad["outcomes"]["s6"] = "LOSS"
            elif mutation == "bad_balance":
                bad["balanced_ownership"]["worker_owned_s7"][0] += 1
            else:
                bad["baseline_locality"]["cross_worker_s7_dependencies"] -= 1
            try:
                verify(bad, old, s7_sets)
            except (ValueError, KeyError, TypeError):
                tests += 1
            else:
                raise AssertionError("tampered S7 routing accepted: " + mutation)
        result["negative_tests"] = tests
    if args.worklist is None:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for s7, worker in sorted(owner_by_s7.items()):
            if worker == args.worklist:
                print(s7)


if __name__ == "__main__":
    main()
