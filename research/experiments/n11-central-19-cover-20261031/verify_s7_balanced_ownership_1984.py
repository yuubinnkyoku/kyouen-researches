#!/usr/bin/env python3
"""Independent 4x4-integer audit of unique 1984-S7 ownership by four workers.

The source is the nine-swap conditional certificate, not a solved game.
Each S7 has exactly one owner; S6 witnesses may need results from other
workers. No solver verdict is read, inferred, or promoted by this program.
"""
import argparse
from collections import Counter, defaultdict
import copy
import json
from pathlib import Path

import verify_conditional_s6_distinct_s7_1984 as source

HERE = Path(__file__).resolve().parent
PLAN = HERE / "conditional_s6_cover_46_balanced_s7_ownership_1984.json"
POLICY = (
    "canonical_s7_sorted_per_worker_pair__"
    "frozen_quota_to_lower_worker_then_higher_worker"
)
UNKNOWN = {
    "s6": "UNKNOWN", "s4": "UNKNOWN",
    "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN",
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def source_frontier():
    # The predecessor chain, all nine swaps, the 94-parent cover, and the
    # 4x4 Bareiss S6->S7 geometry are checked before any routing is trusted.
    data, selected = source.source()
    comparisons = source.known_comparisons()
    certificate = json.loads(source.CERT.read_text(encoding="utf-8"))
    memo = {}
    audit = source.verify(certificate, data, selected, comparisons, memo)
    need(audit["final_distinct_s7"] == 1984
         and audit["raw_s7_edges"] == 2979
         and audit["known_original_first_win6_conflicts"] == 0
         and audit["known_original_first_win7_conflicts"] == 0,
         "conditional source audit changed")
    current = set(selected)
    for step in certificate["steps"]:
        current.difference_update(
            source.base.decode(k) for k in step["removed_s6_classes"])
        current.update(
            source.base.decode(k) for k in step["added_s6_classes"])
    need(len(current) == 46 and all(s6 in memo for s6 in current),
         "final witness set does not match the audited certificate")
    sets = [memo[s6] for s6 in sorted(current)]
    need(sum(map(len, sets)) == 2979
         and len(set().union(*sets)) == 1984,
         "independent S7 source reconstruction failed")
    return sets


def partition(assignment, s7_sets):
    need(type(assignment) is list and len(assignment) == 46
         and all(type(w) is int and 0 <= w < 4 for w in assignment),
         "bad S6 worker assignment")
    counts, raw = [0] * 4, [0] * 4
    by_key = defaultdict(set)
    for i, (worker, keys) in enumerate(zip(assignment, s7_sets)):
        counts[worker] += 1
        raw[worker] += len(keys)
        for key in keys:
            by_key[key].add(worker)
    need(len(by_key) == 1984 and sum(raw) == 2979,
         "S7 frontier changed or keys lost")
    exclusive = [0] * 4
    pairs = defaultdict(list)
    for key, workers in by_key.items():
        need(1 <= len(workers) <= 2, "unexpected S7 worker multiplicity")
        if len(workers) == 1:
            exclusive[next(iter(workers))] += 1
        else:
            a, b = sorted(workers)
            pairs[f"{a}-{b}"].append(key)
    pair_counts = {p: len(keys) for p, keys in sorted(pairs.items())}
    cross = sum(pair_counts.values())
    return {
        "worker_s6_counts": counts,
        "worker_raw_loads": raw,
        "worker_exclusive_s7": exclusive,
        "cross_worker_s7_dependencies": cross,
        "within_worker_shared_s7": 2979 - 1984 - cross,
        "distinct_s7": 1984,
        "raw_s7_edges": 2979,
        "shared_s7_pair_counts": pair_counts,
    }, by_key, pairs


def verify(doc, s7_sets):
    need(doc["schema"] ==
         "n11-central49-conditional46-balanced-unique-s7-ownership-1984-v1"
         and doc["source_certificate"] == source.CERT.name
         and doc["owner_policy"] == POLICY
         and doc["evidence_level"] ==
             "GEOMETRY_ONLY_CONDITIONAL_PROOF_SCHEDULING_NOT_VERDICTS"
         and doc["outcomes"] == UNKNOWN,
         "routing identity, source or UNKNOWN evidence boundary changed")
    old, _, _ = partition([i % 4 for i in range(46)], s7_sets)
    old_expected = {
        "worker_s6_counts": [12, 12, 11, 11],
        "worker_raw_loads": [783, 771, 702, 723],
        "cross_worker_s7_dependencies": 769,
        "within_worker_shared_s7": 226,
    }
    need(doc["baseline_round_robin"] == old_expected
         and all(old[k] == v for k, v in old_expected.items()),
         "baseline comparison not reproducible")

    new, by_key, pairs = partition(doc["worker_index_by_sorted_s6"], s7_sets)
    quotas = doc["shared_s7_pair_quotas"]
    need(type(quotas) is dict and set(quotas) == set(pairs),
         "pair quotas do not match cross-worker S7 classes")
    owners = {}
    for key, workers in by_key.items():
        if len(workers) == 1:
            owners[key] = next(iter(workers))
    for pair, keys in sorted(pairs.items()):
        quota = quotas[pair]
        need(type(quota) is list and len(quota) == 2
             and all(type(n) is int and n >= 0 for n in quota)
             and sum(quota) == len(keys), "bad shared S7 quota")
        a, b = map(int, pair.split("-"))
        keys = sorted(keys)
        for key in keys[:quota[0]]:
            need(key not in owners, "duplicate S7 owner")
            owners[key] = a
        for key in keys[quota[0]:]:
            need(key not in owners, "duplicate S7 owner")
            owners[key] = b
    need(len(owners) == len(by_key) == 1984
         and all(worker in by_key[key] for key, worker in owners.items()),
         "missing, duplicated, or ineligible S7 owner")
    owned = [sum(worker == w for worker in owners.values()) for w in range(4)]
    new["worker_owned_s7"] = owned
    expected = {
        "worker_s6_counts": [12, 12, 11, 11],
        "worker_raw_loads": [787, 790, 701, 701],
        "worker_exclusive_s7": [212, 217, 374, 476],
        "worker_owned_s7": [496, 496, 496, 496],
        "cross_worker_s7_dependencies": 705,
        "within_worker_shared_s7": 290,
        "distinct_s7": 1984,
        "raw_s7_edges": 2979,
        "shared_s7_pair_counts": {
            "0-1": 239, "0-2": 126, "0-3": 87,
            "1-2": 127, "1-3": 82, "2-3": 44,
        },
    }
    need(new == expected == doc["balanced_locality"],
         "saved routing differs from independently reconstructed geometry")
    need(max(owned) == (1984 + 3) // 4
         and sum(owned) == 1984
         and old["cross_worker_s7_dependencies"] - new[
             "cross_worker_s7_dependencies"] == 64
         and new["within_worker_shared_s7"] -
             old["within_worker_shared_s7"] == 64,
         "balance lower bound or sharing improvement not achieved")
    need(Counter(map(len, (
        [i for i, keys in enumerate(s7_sets) if key in keys]
        for key in by_key))) == {1: 989, 2: 995},
         "S7 parent multiplicity changed")
    return {
        "schema": "n11-central49-1984-s7-ownership-audit-v1",
        "conditional_only": True,
        "s6_outcomes": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
        "s6_witnesses": 46,
        "raw_s7_edges": 2979,
        "distinct_s7": 1984,
        "baseline_cross_worker_dependencies": 769,
        "new_cross_worker_dependencies": 705,
        "avoided_cross_worker_dependencies": 64,
        "worker_owned_s7": owned,
        "minimum_possible_max_worker_owned_s7": 496,
        "optimality_claim": (
            "Only the maximum owned S7 count is proven optimal; "
            "cross-worker dependencies and runtime are not."
        ),
    }, owners


def negative_tests(doc, s7_sets):
    for mutation in (
        "worker", "quota_sum", "quota_owner", "policy", "verdict",
        "summary", "baseline", "source", "short_assignment", "bad_worker",
    ):
        bad = copy.deepcopy(doc)
        if mutation == "worker":
            bad["worker_index_by_sorted_s6"][0] = (
                bad["worker_index_by_sorted_s6"][0] + 1) % 4
        elif mutation == "quota_sum":
            bad["shared_s7_pair_quotas"]["0-1"][0] += 1
        elif mutation == "quota_owner":
            bad["shared_s7_pair_quotas"]["0-1"][0] += 1
            bad["shared_s7_pair_quotas"]["0-1"][1] -= 1
        elif mutation == "policy":
            bad["owner_policy"] = "unverified"
        elif mutation == "verdict":
            bad["outcomes"]["s6"] = "LOSS"
        elif mutation == "summary":
            bad["balanced_locality"]["cross_worker_s7_dependencies"] -= 1
        elif mutation == "baseline":
            bad["baseline_round_robin"]["cross_worker_s7_dependencies"] -= 1
        elif mutation == "source":
            bad["source_certificate"] = "unverified.json"
        elif mutation == "short_assignment":
            bad["worker_index_by_sorted_s6"].pop()
        else:
            bad["worker_index_by_sorted_s6"][0] = 4
        try:
            verify(bad, s7_sets)
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError("tampered plan accepted: " + mutation)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    parser.add_argument("--worklist", type=int, choices=range(4))
    args = parser.parse_args()
    sets = source_frontier()
    doc = json.loads(PLAN.read_text(encoding="utf-8"))
    result, owners = verify(doc, sets)
    if args.negative:
        negative_tests(doc, sets)
        result["negative_tests"] = 10
    if args.worklist is None:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for key, worker in sorted(owners.items()):
            if worker == args.worklist:
                print(key)


if __name__ == "__main__":
    main()
