#!/usr/bin/env python3
"""Audit the replacement 46-S6 geometric cover after a terminal-certified WIN6.

The certificate is only a conditional cover. The original-first WIN6 is
excluded; none of the remaining selected S6 is thereby proved LOSS.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_s7_shared_frontier_46 as geometry
import verify_conditional_s6_distinct_s7_1984 as old_comparison

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_exclude_certified_win6.json"
WIN_CERT = HERE / "focus_s6_win_strategy_1984.cert"
REFUTED = "00000000000000603800000000008000"
WIN_SHA = "390554902426c5876b9742edb4219cae13648e103d6310d4f94b9d690ea4e63e"
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def verify(doc, data, known_win6):
    s4, s5, incidence, cost, *_ = data
    need(doc.get("schema") ==
         "n11-central49-conditional46-repaired-exclude-certified-win6-v1"
         and doc.get("source_s4_key") == base.key(s4)
         and doc.get("excluded_certified_win6") == REFUTED
         and doc.get("win6_certificate") == WIN_CERT.name
         and doc.get("win6_sha256") == WIN_SHA
         and doc.get("evidence_level") ==
         "GEOMETRY_ONLY_CONDITIONAL_REPAIR_NOT_S6_LOSS"
         and doc.get("outcomes") == UNKNOWN,
         "certificate identity, provenance or UNKNOWN boundary changed")
    keys = doc.get("selected_s6_classes")
    need(type(keys) is list and len(keys) == 46
         and keys == sorted(set(keys)), "46 sorted unique S6 keys required")
    need(REFUTED not in keys and not (set(keys) & known_win6),
         "certified original-first WIN6 was selected as LOSS witness")
    selected = [base.decode(k) for k in keys]
    need(len(s5) == 94 and all(m in incidence for m in selected)
         and set().union(*(incidence[m] for m in selected)) == set(range(94)),
         "94-S5 geometric cover is incomplete")
    edges, frontier = 0, set()
    for key, mask in zip(keys, selected):
        need(geometry.canonical(mask) == mask, "noncanonical S6 key")
        children = geometry.children(mask)
        child_keys = {f"{geometry.canonical(c):032x}" for c in children}
        need(len(children) == len(child_keys) == cost[mask],
             "independent 4x4 S6-S7 geometry differs from 3x3")
        edges += len(children)
        frontier.update(child_keys)
    need((doc["s5_covered"], doc["selected_s6_count"],
          doc["raw_s7_edges"], doc["distinct_s7_classes"],
          doc["known_original_first_win6_conflicts"]) ==
         (94, 46, edges, len(frontier), len(set(keys) & known_win6)) ==
         (94, 46, 2900, 2711, 0),
         "repaired S6 cover or S7 obligation counts changed")
    return {
        "schema": "n11-central49-repaired-46-s6-cover-audit-v1",
        "s5_covered": 94,
        "s6_witnesses": 46,
        "excluded_certified_win6": REFUTED,
        "known_win6_conflicts": 0,
        "raw_s7_edges": edges,
        "distinct_s7_classes": len(frontier),
        "conditional_only": True,
        "s6_outcome": "UNKNOWN",
        "s4_outcome": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
        "optimality_claim": "46-S6 feasibility only; 2711 S7 is not proven minimal"
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    need(hashlib.sha256(WIN_CERT.read_bytes()).hexdigest() == WIN_SHA,
         "independently terminal-proved WIN6 certificate changed")
    old = json.loads((HERE / "conditional_s6_cover_46.json").read_text(encoding="utf-8"))
    data = base.reconstruct()
    base.verify(old, data)
    win6, _, _ = old_comparison.known_comparisons()
    need(len(win6) == 117, "historical WIN6 inventory changed")
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    result = verify(doc, data, {f"{k:032x}" for k in win6})
    if args.negative:
        for mutation in ("refuted", "duplicate", "count", "verdict", "source"):
            bad = copy.deepcopy(doc)
            if mutation == "refuted":
                bad["selected_s6_classes"][0] = REFUTED
                bad["selected_s6_classes"].sort()
            elif mutation == "duplicate":
                bad["selected_s6_classes"][1] = bad["selected_s6_classes"][0]
            elif mutation == "count":
                bad["distinct_s7_classes"] -= 1
            elif mutation == "verdict":
                bad["outcomes"]["s6"] = "LOSS"
            else:
                bad["win6_sha256"] = "0" * 64
            try:
                verify(bad, data, {f"{k:032x}" for k in win6})
            except (ValueError, KeyError, TypeError):
                continue
            raise AssertionError("tampered repaired cover accepted: " + mutation)
        result["negative_tests"] = 5
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
