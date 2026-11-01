#!/usr/bin/env python3
"""Audit a lower-communication, optimally balanced 4-worker S7 ownership plan.

This is a geometry-only scheduling certificate, not an S6 game proof.
All 2,944 legal S6->S7 edges are independently rebuilt by the existing
4x4-integer-geometry certificate-chain verifier before routing is checked.
"""
import argparse
from collections import defaultdict
import copy
import json
from pathlib import Path

import verify_s7_balanced_ownership_2309 as baseline

HERE = Path(__file__).resolve().parent
PLAN = HERE / "conditional_s6_cover_46_low_remote_balanced_s7_ownership_2309.json"
BASELINE = HERE / "conditional_s6_cover_46_balanced_s7_ownership_2309.json"
POLICY = (
    "canonical_s7_sorted_per_worker_pair__"
    "frozen_quota_to_lower_worker_then_higher_worker"
)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def allocation(plan, s7_sets):
    assignment = plan["worker_index_by_sorted_s6"]
    need(isinstance(assignment, list) and len(assignment) == len(s7_sets) == 46
         and all(type(w) is int and 0 <= w < 4 for w in assignment),
         "invalid worker assignment")
    raw = [0] * 4
    counts = [0] * 4
    workers_by_s7 = defaultdict(set)
    for worker, keys in zip(assignment, s7_sets):
        counts[worker] += 1
        raw[worker] += len(keys)
        for key in keys:
            workers_by_s7[key].add(worker)
    need(len(workers_by_s7) == 2309 and sum(raw) == 2944,
         "source S7 frontier changed")
    exclusive = [0] * 4
    owner_by_s7 = {}
    shared = defaultdict(list)
    for key, workers in workers_by_s7.items():
        need(1 <= len(workers) <= 2, "unexpected worker multiplicity")
        if len(workers) == 1:
            worker = next(iter(workers))
            exclusive[worker] += 1
            owner_by_s7[key] = worker
        else:
            shared[tuple(sorted(workers))].append(key)

    quotas = plan["shared_s7_pair_quotas"]
    need(isinstance(quotas, dict)
         and set(quotas) == {f"{a}-{b}" for a, b in shared},
         "pair quotas must cover exactly the remote dependencies")
    pair_counts = {}
    for (a, b), keys in sorted(shared.items()):
        label = f"{a}-{b}"
        q = quotas[label]
        need(isinstance(q, list) and len(q) == 2
             and all(type(n) is int and n >= 0 for n in q)
             and sum(q) == len(keys), "invalid shared S7 pair quota")
        pair_counts[label] = len(keys)
        keys = sorted(keys)
        for key in keys[:q[0]]:
            need(key not in owner_by_s7, "duplicate S7 owner")
            owner_by_s7[key] = a
        for key in keys[q[0]:]:
            need(key not in owner_by_s7, "duplicate S7 owner")
            owner_by_s7[key] = b

    owned = [0] * 4
    for worker in owner_by_s7.values():
        owned[worker] += 1
    cross = sum(pair_counts.values())
    within = 2944 - len(owner_by_s7) - cross
    need(len(owner_by_s7) == 2309 and sum(owned) == 2309
         and sum(exclusive) + cross == 2309
         and within + cross == 635, "S7 ownership conservation failed")
    return {
        "worker_s6_counts": counts,
        "worker_raw_loads": raw,
        "worker_exclusive_s7": exclusive,
        "worker_owned_s7": owned,
        "cross_worker_s7_dependencies": cross,
        "within_worker_shared_s7": within,
        "distinct_s7": len(owner_by_s7),
    }, owner_by_s7, pair_counts


def verify(plan, source, s7_sets, source_keys):
    need(plan["schema"] ==
         "n11-central49-conditional46-low-remote-balanced-s7-ownership-v1"
         and plan["source_plan"] == BASELINE.name
         and plan["source_certificate"] == baseline.previous.CERT.name
         and plan["owner_policy"] == POLICY
         and plan["evidence_level"] ==
         "GEOMETRY_ONLY_CONDITIONAL_PROOF_SCHEDULING_NOT_VERDICTS"
         and plan["outcomes"] == {
             "s6": "UNKNOWN", "s4": "UNKNOWN",
             "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"},
         "source identity, routing policy or evidence boundary changed")
    expected_baseline = {
        "worker_owned_s7": source["balanced"]["worker_owned_s7"],
        "cross_worker_s7_dependencies":
            source["balanced"]["cross_worker_s7_dependencies"],
    }
    need(plan["baseline_balanced"] == expected_baseline
         and expected_baseline == {
             "worker_owned_s7": [578, 577, 577, 577],
             "cross_worker_s7_dependencies": 482},
         "source balanced ownership changed")
    result, owners, pairs = allocation(plan, s7_sets)
    expected = {
        "worker_s6_counts": [12, 12, 11, 11],
        "worker_raw_loads": [758, 722, 743, 721],
        "worker_exclusive_s7": [409, 553, 326, 575],
        "worker_owned_s7": [578, 577, 577, 577],
        "cross_worker_s7_dependencies": 446,
        "within_worker_shared_s7": 189,
        "distinct_s7": 2309,
    }
    need(result == plan["low_remote_balanced"] == expected,
         "saved routing statistics disagree with independent geometry")
    need(pairs == {
             "0-1": 57, "0-2": 174, "0-3": 52,
             "1-2": 75, "1-3": 24, "2-3": 64}
         and set(owners) == source_keys
         and all(715 <= x <= 760 for x in result["worker_raw_loads"])
         and max(result["worker_owned_s7"]) == 578
         and result["cross_worker_s7_dependencies"] <
             expected_baseline["cross_worker_s7_dependencies"],
         "remote-dependency improvement or exact balance failed")
    return {
        "schema": "n11-central49-low-remote-balanced-s7-audit-v1",
        "conditional_only": True,
        "empty_board_outcome": "UNKNOWN",
        "s6_outcomes": "UNKNOWN",
        "s6_witnesses": 46,
        "raw_s7_edges": 2944,
        "distinct_s7": 2309,
        "baseline_cross_worker_dependencies": 482,
        "new_cross_worker_dependencies": 446,
        "avoided_remote_dependencies": 36,
        "baseline_max_owned_s7": 578,
        "new_max_owned_s7": 578,
        "new": result,
        "shared_s7_pair_counts": pairs,
        "optimality_claim": "Only the max owner count 578 is globally minimal for 2309 tasks over four workers; communication is not proven optimal.",
    }, owners


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    parser.add_argument("--worklist", type=int, choices=range(4),
                        help="print the exact canonical S7 keys owned by worker")
    args = parser.parse_args()
    witnesses = baseline.previous.source_witnesses()
    s7_sets = baseline.previous.frontier(witnesses)
    locality = json.loads(baseline.OLD.read_text(encoding="utf-8"))
    baseline.previous.verify(locality, witnesses, s7_sets)
    source = json.loads(BASELINE.read_text(encoding="utf-8"))
    source_stats, source_owners = baseline.verify(source, locality, s7_sets)
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    result, owners = verify(plan, source_stats, s7_sets, set(source_owners))
    if args.negative:
        tests = 0
        for mutation in ("worker", "quota", "policy", "verdict",
                         "summary", "baseline", "source"):
            bad = copy.deepcopy(plan)
            if mutation == "worker":
                bad["worker_index_by_sorted_s6"][0] = 0
            elif mutation == "quota":
                bad["shared_s7_pair_quotas"]["0-2"][0] += 1
            elif mutation == "policy":
                bad["owner_policy"] = "unverified_hash_routing"
            elif mutation == "verdict":
                bad["outcomes"]["s6"] = "LOSS"
            elif mutation == "summary":
                bad["low_remote_balanced"]["worker_owned_s7"][0] += 1
            elif mutation == "baseline":
                bad["baseline_balanced"]["cross_worker_s7_dependencies"] -= 1
            else:
                bad["source_certificate"] = "unverified.json"
            try:
                verify(bad, source_stats, s7_sets, set(source_owners))
            except (ValueError, KeyError, TypeError):
                tests += 1
            else:
                raise AssertionError("tampered S7 plan accepted: " + mutation)
        result["negative_tests"] = tests
    if args.worklist is None:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for key, worker in sorted(owners.items()):
            if worker == args.worklist:
                print(key)


if __name__ == "__main__":
    main()
