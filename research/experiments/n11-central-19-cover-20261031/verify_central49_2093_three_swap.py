#!/usr/bin/env python3
"""Independently verify a 2094 -> 2093 exact three-S6 witness exchange.

The complete five terminal strategies are replayed before six certified
LOSS7 children are credited. The three new S6 frontiers are recomputed
with 4x4 Bareiss geometry and cross-checked against exact 3x3 determinants.
No conditional witness is promoted to a WIN/LOSS verdict.
"""
import copy
import json
from pathlib import Path

import focus_s7_worker_2094 as focus
import verify_central49_2094_three_swap_descent as previous

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_post_seven_win6_2093_three_swap.json"
SCHEMA = "n11-central49-2094-to-2093-three-swap-v1"
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
         and doc.get("source_certificate") == previous.CERT.name
         and doc.get("outcomes") == UNKNOWN
         and doc.get("evidence_level") ==
         "GEOMETRY_ONLY_CONDITIONAL_COVER_WITH_TERMINAL_REPLAYED_S7_HITS",
         "wrong source, scope or evidence level")
    removed, added = doc["removed"], doc["added"]
    need(type(removed) is list and type(added) is list
         and len(removed) == len(added) == 3
         and removed == sorted(set(removed))
         and added == sorted(set(added))
         and all(type(k) is str and len(k) == 32
                 and all(c in "0123456789abcdef" for c in k)
                 for k in removed + added),
         "bad exact three-witness exchange encoding")

    # This reconstructs the full 2094 proof, including independent 4x4
    # geometry, the 2154 predecessor, and five complete terminal strategies.
    frontiers, multiplicity, secured_before = focus.geometry()
    _, s5, incidence, costs, win6, win7, loss7, _ = previous.context()
    selected = set(frontiers)
    rm, ad = {int(k, 16) for k in removed}, {int(k, 16) for k in added}
    need(len(selected) == 46 and len(multiplicity) == 2094
         and len(secured_before) == 6
         and rm <= selected and not (ad & selected)
         and ad <= set(incidence) and not (ad & win6),
         "wrong source membership or certified WIN6 selected")

    selected = (selected - rm) | ad
    need(len(selected) == 46 and
         set().union(*(incidence[s] for s in selected)) == set(range(94)),
         "replacement fails to cover all 94 five-stone classes")
    for s in rm:
        del frontiers[s]
    for s in ad:
        ch = previous.four_frontier(s)
        need(len(ch) == costs[s], "independent S6-to-S7 cost disagreement")
        frontiers[s] = ch
    need(set(frontiers) == selected, "frontier/selection mismatch")
    union = set().union(*frontiers.values())
    raw = sum(map(len, frontiers.values()))
    secured = union & loss7
    win6_conflicts = len(selected & win6)
    win7_conflicts = len(union & win7)
    actual = (len(selected), len(s5), raw, len(union), len(secured),
              win6_conflicts, win7_conflicts)
    claimed = tuple(doc[k] for k in (
        "selected_s6_count", "s5_covered", "raw_s7_edges",
        "distinct_s7_classes", "terminal_backed_loss7_hits_from_k0644",
        "known_win6_conflicts", "known_win7_conflicts"))
    need(actual == claimed == (46, 94, 2986, 2093, 6, 0, 0),
         "independent geometry or terminal-secured count changed")
    return {
        "schema": "n11-central49-2093-independent-three-swap-audit-v1",
        "source_distinct_s7": 2094,
        "final_distinct_s7": len(union),
        "saved_distinct_s7": 2094 - len(union),
        "raw_s7_edges": raw,
        "selected_s6": len(selected),
        "covered_s5": len(s5),
        "terminal_certified_loss7": len(secured),
        "unsecured_by_k0644": len(union - secured),
        "known_win6_conflicts": win6_conflicts,
        "known_win7_conflicts": win7_conflicts,
        "conditional_only": True,
        "outcomes": UNKNOWN,
    }


def negative_tests(doc):
    for mode in ("source", "verdict", "member", "added", "raw", "secured"):
        bad = copy.deepcopy(doc)
        if mode == "source":
            bad["source_certificate"] = "obsolete_1985.json"
        elif mode == "verdict":
            bad["outcomes"]["s6"] = "LOSS"
        elif mode == "member":
            bad["removed"][0] = bad["added"][0]
        elif mode == "added":
            bad["added"][0] = bad["removed"][0]
        elif mode == "raw":
            bad["raw_s7_edges"] -= 1
        else:
            bad["terminal_backed_loss7_hits_from_k0644"] += 1
        try:
            audit(bad)
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError("tampered certificate accepted: " + mode)
    return 6


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    result = audit(doc)
    if args.negative:
        result["negative_tests"] = negative_tests(doc)
    print(json.dumps(result, ensure_ascii=False, indent=2))
