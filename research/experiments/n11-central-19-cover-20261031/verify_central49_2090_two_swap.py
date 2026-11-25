#!/usr/bin/env python3
"""Independently verify the exact 2091 -> 2090 conditional S6 exchange.

The entire source 2091 plan and five terminal strategies are replayed.
All added six-stone children are checked using separate exact 4x4 Bareiss
and 3x3 difference determinants. No six-stone LOSS is assumed.
"""
import copy
import json
from pathlib import Path

import focus_s7_worker_2091 as focus
import verify_central49_2091_three_swap as predecessor
import verify_central49_2094_three_swap_descent as geometry

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_post_seven_win6_2090_two_swap.json"
SCHEMA = "n11-central49-2091-to-2090-two-swap-v1"
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}
FIELDS = {
    "schema", "source_certificate", "removed", "added",
    "selected_s6_count", "s5_covered", "raw_s7_edges",
    "distinct_s7_classes", "terminal_backed_loss7_hits_from_k0644",
    "known_win6_conflicts", "known_win7_conflicts",
    "evidence_level", "outcomes",
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def audit(doc):
    need(type(doc) is dict and set(doc) == FIELDS
         and doc.get("schema") == SCHEMA
         and doc.get("source_certificate") == predecessor.CERT.name
         and doc.get("outcomes") == UNKNOWN
         and doc.get("evidence_level") ==
         "GEOMETRY_ONLY_CONDITIONAL_COVER_WITH_TERMINAL_REPLAYED_S7_HITS",
         "wrong source or unverified verdict promotion")
    removed, added = doc["removed"], doc["added"]
    need(type(removed) is list and type(added) is list
         and len(removed) == len(added) == 2
         and removed == sorted(set(removed))
         and added == sorted(set(added))
         and all(type(k) is str and len(k) == 32
                 and all(c in "0123456789abcdef" for c in k)
                 for k in removed + added),
         "bad exact two-witness encoding")

    # Full terminal replay, independent source certificate, and 4x4 geometry.
    source_frontiers, counts, secured_before = focus.geometry()
    _, s5, incidence, costs, win6, win7, loss7, _ = geometry.context()
    need(len(source_frontiers) == 46 and len(counts) == 2091
         and sum(counts.values()) == 2984 and len(secured_before) == 6,
         "2091 predecessor changed")
    frontiers = dict(source_frontiers)  # Never mutate cached predecessor.
    before = set(frontiers)
    rm, ad = {int(k, 16) for k in removed}, {int(k, 16) for k in added}
    need(rm <= before and not (ad & before)
         and ad <= set(incidence) and not (ad & win6),
         "wrong predecessor membership or known WIN6 selected")
    selected = (before - rm) | ad
    need(len(selected) == 46
         and set().union(*(incidence[s] for s in selected)) == set(range(94)),
         "94 five-stone classes not covered")
    for s in rm:
        del frontiers[s]
    for s in ad:
        children = geometry.four_frontier(s)
        need(len(children) == costs[s],
             "4x4/3x3 child count disagreement")
        frontiers[s] = children
    need(set(frontiers) == selected and set(source_frontiers) == before,
         "frontier mutation or selected set disagreement")
    union = set().union(*frontiers.values())
    raw = sum(map(len, frontiers.values()))
    secured = union & loss7
    conflicts6 = len(selected & win6)
    conflicts7 = len(union & win7)
    actual = (len(selected), len(s5), raw, len(union), len(secured),
              conflicts6, conflicts7)
    claimed = tuple(doc[k] for k in (
        "selected_s6_count", "s5_covered", "raw_s7_edges",
        "distinct_s7_classes", "terminal_backed_loss7_hits_from_k0644",
        "known_win6_conflicts", "known_win7_conflicts"))
    need(actual == claimed == (46, 94, 2983, 2090, 6, 0, 0),
         "independent 2090 geometry or known-WIN exclusion failed")
    return {
        "schema": "n11-central49-2090-independent-two-swap-audit-v1",
        "source_distinct_s7": 2091,
        "final_distinct_s7": len(union),
        "saved_distinct_s7": 2091 - len(union),
        "raw_s7_edges": raw,
        "selected_s6": len(selected),
        "covered_s5": len(s5),
        "terminal_certified_loss7": len(secured),
        "terminal_hits_lost": len(secured_before - secured),
        "terminal_hits_gained": len(secured - secured_before),
        "unsecured_by_k0644": len(union - secured),
        "known_win6_conflicts": conflicts6,
        "known_win7_conflicts": conflicts7,
        "conditional_only": True,
        "outcomes": UNKNOWN,
    }


def negative_tests(doc):
    for mode in ("source", "verdict", "member", "added", "count", "raw", "secured", "collision"):
        bad = copy.deepcopy(doc)
        if mode == "source":
            bad["source_certificate"] = "obsolete_2094.json"
        elif mode == "verdict":
            bad["outcomes"]["s6"] = "LOSS"
        elif mode == "member":
            bad["removed"][0] = bad["added"][0]
        elif mode == "added":
            bad["added"][0] = bad["removed"][0]
        elif mode == "count":
            bad["distinct_s7_classes"] += 1
        elif mode == "raw":
            bad["raw_s7_edges"] -= 1
        elif mode == "secured":
            bad["terminal_backed_loss7_hits_from_k0644"] += 1
        else:
            bad["known_win7_conflicts"] += 1
        try:
            audit(bad)
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError("tampered certificate accepted: " + mode)
    return 8


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    result = audit(doc)
    if args.negative:
        result["negative_tests"] = negative_tests(doc)
    print(json.dumps(result, ensure_ascii=False))
