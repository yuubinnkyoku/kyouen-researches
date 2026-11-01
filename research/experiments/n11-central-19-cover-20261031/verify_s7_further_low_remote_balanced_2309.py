#!/usr/bin/env python3
"""Independently audit a 439-cross-worker S7 routing plan, conditional only.

Reconstruct all S6 and S7 geometry via the earlier 4x4 Bareiss checker.
Never promote the geometry-only worklist to a game verdict.
"""
import argparse
import copy
import json
from pathlib import Path

import verify_s7_low_remote_balanced_2309 as previous

HERE = Path(__file__).resolve().parent
PLAN = HERE / "conditional_s6_cover_46_further_low_remote_balanced_s7_ownership_2309.json"
POLICY = previous.POLICY


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def verify(doc, old, old_stats, s7_sets, source_keys):
    need(doc["schema"] ==
         "n11-central49-conditional46-further-low-remote-balanced-s7-ownership-v1"
         and doc["source_plan"] == previous.PLAN.name
         and doc["source_certificate"] == previous.baseline.previous.CERT.name
         and doc["owner_policy"] == POLICY
         and doc["evidence_level"] ==
         "GEOMETRY_ONLY_CONDITIONAL_PROOF_SCHEDULING_NOT_VERDICTS"
         and doc["outcomes"] == {
             "s6": "UNKNOWN", "s4": "UNKNOWN",
             "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"},
         "identity, source or UNKNOWN evidence boundary changed")
    need(doc["previous_low_remote"] == {
             "worker_owned_s7": old_stats["worker_owned_s7"],
             "cross_worker_s7_dependencies":
                 old_stats["cross_worker_s7_dependencies"]} ==
         {"worker_owned_s7": [578, 577, 577, 577],
          "cross_worker_s7_dependencies": 446},
         "previous verified routing changed")
    result, owners, pairs = previous.allocation(doc, s7_sets)
    expected = {
        "worker_s6_counts": [12, 12, 11, 11],
        "worker_raw_loads": [758, 721, 750, 715],
        "worker_exclusive_s7": [410, 552, 333, 575],
        "worker_owned_s7": [578, 577, 577, 577],
        "cross_worker_s7_dependencies": 439,
        "within_worker_shared_s7": 196,
        "distinct_s7": 2309,
    }
    need(result == expected == doc["further_low_remote"],
         "routing statistics differ from independently rebuilt geometry")
    need(pairs == {
             "0-1": 58, "0-2": 170, "0-3": 51,
             "1-2": 77, "1-3": 21, "2-3": 62}
         and set(owners) == source_keys
         and max(result["worker_owned_s7"]) == 578
         and all(715 <= x <= 760 for x in result["worker_raw_loads"])
         and result["cross_worker_s7_dependencies"] + 7 ==
             old_stats["cross_worker_s7_dependencies"]
         and result["within_worker_shared_s7"] ==
             old_stats["within_worker_shared_s7"] + 7,
         "balance, S7 coverage, or improvement invalid")
    return {
        "schema": "n11-central49-further-low-remote-s7-audit-v1",
        "conditional_only": True,
        "empty_board_outcome": "UNKNOWN",
        "s6_outcomes": "UNKNOWN",
        "s6_witnesses": 46,
        "raw_s7_edges": 2944,
        "distinct_s7": 2309,
        "previous_remote_dependencies": 446,
        "new_remote_dependencies": 439,
        "avoided_remote_dependencies": 7,
        "max_owned_s7": 578,
        "new": result,
        "shared_s7_pair_counts": pairs,
        "optimality_claim": "Only the max owned S7 count is globally optimal. Remote dependencies are not proved minimal.",
    }, owners


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    parser.add_argument("--worklist", type=int, choices=range(4))
    args = parser.parse_args()
    witnesses = previous.baseline.previous.source_witnesses()
    s7_sets = previous.baseline.previous.frontier(witnesses)
    locality = json.loads(previous.baseline.OLD.read_text(encoding="utf-8"))
    previous.baseline.previous.verify(locality, witnesses, s7_sets)
    balanced = json.loads(previous.BASELINE.read_text(encoding="utf-8"))
    source_stats, source_owners = previous.baseline.verify(
        balanced, locality, s7_sets)
    old = json.loads(previous.PLAN.read_text(encoding="utf-8"))
    old_result, old_owners = previous.verify(
        old, source_stats, s7_sets, set(source_owners))
    doc = json.loads(PLAN.read_text(encoding="utf-8"))
    result, owners = verify(doc, old, old_result, s7_sets, set(old_owners))
    if args.negative:
        for mutation in ("worker", "quota", "policy", "verdict",
                         "summary", "baseline", "source", "coverage"):
            bad = copy.deepcopy(doc)
            if mutation == "worker":
                bad["worker_index_by_sorted_s6"][0] = 0
            elif mutation == "quota":
                bad["shared_s7_pair_quotas"]["0-2"][0] += 1
            elif mutation == "policy":
                bad["owner_policy"] = "unverified"
            elif mutation == "verdict":
                bad["outcomes"]["s6"] = "LOSS"
            elif mutation == "summary":
                bad["further_low_remote"]["cross_worker_s7_dependencies"] -= 1
            elif mutation == "baseline":
                bad["previous_low_remote"]["cross_worker_s7_dependencies"] -= 1
            elif mutation == "source":
                bad["source_certificate"] = "unverified.json"
            else:
                bad["shared_s7_pair_quotas"]["1-3"] = [21, 0]
            try:
                verify(bad, old, old_result, s7_sets, set(old_owners))
            except (ValueError, KeyError, TypeError):
                continue
            raise AssertionError("tampered plan accepted: " + mutation)
        result["negative_tests"] = 8
    if args.worklist is None:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, worker in sorted(owners.items()):
            if worker == args.worklist:
                print(key)


if __name__ == "__main__":
    main()
