#!/usr/bin/env python3
"""Audit 4-worker S6 allocation with exact S7 sharing and source provenance.

No WIN/LOSS claims. This is a geometry-only allocation of conditional proof
obligations. Rebuilds the 46 witnesses from the previous certificate chain.
"""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_conditional_s6_distinct_s7_2309 as source
import verify_s7_shared_frontier_46 as geometry

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_distinct_s7_2309.json"
PLAN = HERE / "conditional_s6_cover_46_s7_locality_workers_2309.json"


def need(ok, why):
    if not ok:
        raise ValueError(why)


def source_witnesses():
    data, previous = source.predecessor()
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    source.verify(doc, data, previous)
    removed = {base.decode(k) for k in doc["removed_s6_classes"]}
    added = {base.decode(k) for k in doc["added_s6_classes"]}
    selected = (set(previous) - removed) | added
    need(len(selected) == 46 and removed <= previous
         and not (added & previous), "invalid source replacement")
    return sorted(selected)


def frontier(witnesses):
    per_witness = []
    for s6 in witnesses:
        m = geometry.decode(base.key(s6), 6)
        need(geometry.canonical(m) == m, "noncanonical S6")
        raw = geometry.children(m)  # 4x4 Bareiss, independent of 3x3 search
        unique = {base.key(geometry.canonical(child)) for child in raw}
        need(len(unique) == len(raw), "within-witness S7 collision")
        per_witness.append(unique)
    return per_witness


def statistics(assignment, sets):
    raw = [0] * 4
    per_worker = [set() for _ in range(4)]
    for worker, s7 in zip(assignment, sets):
        raw[worker] += len(s7)
        per_worker[worker].update(s7)
    distinct = [len(s) for s in per_worker]
    union = set().union(*per_worker)
    return raw, distinct, sum(distinct) - len(union)


def verify(plan, witnesses, sets):
    need(plan["schema"] == "n11-central49-conditional46-s7-locality-workers-v1"
         and plan["source_certificate"] == CERT.name
         and plan["evidence_level"] == "GEOMETRY_ONLY_NO_S6_VERDICTS"
         and plan["outcomes"] == {"s6": "UNKNOWN", "s4": "UNKNOWN",
                                    "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"},
         "identity or evidence boundary changed")
    assignment = plan["worker_index_by_sorted_s6"]
    need(isinstance(assignment, list) and len(assignment) == len(witnesses) == 46
         and all(type(x) is int and 0 <= x < 4 for x in assignment),
         "invalid worker assignment")
    union = set().union(*sets)
    total = sum(map(len, sets))
    multiplicity = Counter(s7 for ss in sets for s7 in ss)
    need((total, len(union)) == (2944, 2309)
         and Counter(multiplicity.values()) == {1: 1674, 2: 635},
         "source frontier or multiplicity changed")
    baseline = [i % 4 for i in range(46)]
    baseline_raw, baseline_distinct, baseline_cut = statistics(baseline, sets)
    raw, distinct, cut = statistics(assignment, sets)
    counts = [assignment.count(i) for i in range(4)]
    need((baseline_raw, baseline_cut) == ([770, 757, 698, 719], 494),
         "baseline round-robin geometry changed")
    need((counts, raw, distinct, cut) ==
         ([12, 12, 11, 11], [726, 736, 745, 737],
          [706, 735, 636, 632], 400), "saved allocation changed")
    need(all(715 <= x <= 760 for x in raw)
         and sum(raw) == 2944 and sum(distinct) == 2709
         and cut == sum(distinct) - 2309
         and baseline_cut - cut == 94, "worker balance or reuse invalid")
    need(plan["baseline_round_robin"] == {
             "worker_raw_loads": baseline_raw,
             "cross_worker_s7_duplicates": baseline_cut}
         and plan["locality_partition"] == {
             "worker_s6_counts": counts,
             "worker_raw_loads": raw,
             "worker_distinct_s7": distinct,
             "cross_worker_s7_duplicates": cut},
         "saved summary does not match recomputed geometry")
    return {"schema": "n11-central49-s6-worker-locality-audit-v1",
            "conditional_only": True, "s6_outcomes": "UNKNOWN",
            "empty_board_outcome": "UNKNOWN",
            "witnesses": len(witnesses), "raw_s7_edges": total,
            "distinct_s7": len(union),
            "multiplicity_histogram": dict(Counter(multiplicity.values())),
            "worker_counts": counts, "worker_raw_loads": raw,
            "worker_distinct_s7": distinct,
            "baseline_raw_loads": baseline_raw,
            "baseline_cross_worker_duplicates": baseline_cut,
            "new_cross_worker_duplicates": cut,
            "avoided_cross_worker_duplicates": baseline_cut - cut,
            "optimality_claim": "none; measured feasible partition only"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    witnesses = source_witnesses()
    sets = frontier(witnesses)
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    result = verify(plan, witnesses, sets)
    if args.negative:
        tests = 0
        for mutation in ("wrong_worker", "short", "bad_evidence", "false_verdict", "false_summary"):
            bad = copy.deepcopy(plan)
            if mutation == "wrong_worker":
                bad["worker_index_by_sorted_s6"][0] = 3
            elif mutation == "short":
                bad["worker_index_by_sorted_s6"].pop()
            elif mutation == "bad_evidence":
                bad["evidence_level"] = "PROVED"
            elif mutation == "false_verdict":
                bad["outcomes"]["s6"] = "LOSS"
            else:
                bad["locality_partition"]["cross_worker_s7_duplicates"] = 399
            try:
                verify(bad, witnesses, sets)
            except (ValueError, KeyError, TypeError):
                tests += 1
            else:
                raise AssertionError("tampered allocation accepted: " + mutation)
        result["negative_tests"] = tests
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
