#!/usr/bin/env python3
"""Independent geometry audit of the conditional 46-S6 / 2,347-S7 plan.

Recheck the entire preceding certificate chain, the 94-S5 cover and all
selected S6->S7 legal children with 4x4 Bareiss integer determinants and D4.
This is a constructive conditional proof plan, NOT an outcome certificate.
"""
import argparse
import copy
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_conditional_s6_distinct_s7_2386 as previous
import verify_conditional_s6_distinct_s7_2553 as geometry
import verify_s7_shared_frontier_46 as independent

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_distinct_s7_2347.json"
SOURCE = HERE / "conditional_s6_cover_46_distinct_s7_2386.json"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def predecessor():
    data, selected = previous.predecessor()
    prior = json.loads(SOURCE.read_text(encoding="utf-8"))
    previous.verify(prior, data, set(selected))
    removed = {base.decode(k) for k in prior["removed_s6_classes"]}
    added = {base.decode(k) for k in prior["added_s6_classes"]}
    need(removed <= selected and not (added & selected),
         "invalid preceding two-for-two replacement")
    selected = (selected - removed) | added
    need(len(selected) == 46, "preceding S6 count changed")
    return data, selected


def verify(doc, data, selected):
    s4, s5, incidence, cost, *_ = data
    need(doc["schema"] ==
         "n11-central49-conditional46-distinct-s7-two-for-two-2347-v1"
         and doc["source_certificate"] == SOURCE.name
         and doc["priority_s4_key"] == base.key(s4)
         and doc["evidence_level"] ==
             "GEOMETRY_ONLY_CONDITIONAL_PROOF_PLAN_NOT_VERDICTS"
         and doc["outcomes"] == {
             "s4": "UNKNOWN", "s6": "UNKNOWN",
             "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"
         }, "identity, evidence level, or verdict changed")
    need(len(s5) == 94 and len(selected) == 46
         and set().union(*(incidence[k] for k in selected)) ==
             set(range(94)), "predecessor S5 cover changed")
    old_edges, old_s7 = geometry.s7_frontier(selected, cost)
    need((old_edges, len(old_s7)) ==
         (doc["previous_raw_s7_edges"],
          doc["previous_distinct_s7_classes"]) == (2929, 2386),
         "predecessor S7 geometry changed")

    removed = doc["removed_s6_classes"]
    added = doc["added_s6_classes"]
    need(isinstance(removed, list) and isinstance(added, list)
         and len(removed) == len(added) == 2
         and removed == sorted(set(removed))
         and added == sorted(set(added)), "invalid replacement lists")
    rm = {base.decode(k) for k in removed}
    ad = {base.decode(k) for k in added}
    need(rm <= selected and not (ad & selected)
         and ad <= set(incidence)
         and all(independent.canonical(k) == k for k in ad),
         "replacement is invalid or noncanonical")
    selected = (selected - rm) | ad
    need(len(selected) == 46
         and set().union(*(incidence[k] for k in selected)) ==
             set(range(94)), "replacement does not cover all 94 S5 parents")
    new_edges, new_s7 = geometry.s7_frontier(selected, cost)
    need((doc["s5_covered"], doc["s6_witnesses"],
          doc["final_raw_s7_edges"], doc["final_distinct_s7_classes"],
          doc["distinct_s7_saved"], doc["shared_s7_reuses"]) ==
         (94, 46, new_edges, len(new_s7),
          len(old_s7) - len(new_s7), new_edges - len(new_s7)) ==
         (94, 46, 2934, 2347, 39, 587),
         "new S7 geometry or reduction disagrees")

    old_win = independent.inventory(
        independent.BASE / "all_s7_win_17.txt", 17)
    old_loss = independent.inventory(
        independent.BASE / "all_s7_loss_2232.txt", 2232)
    lift = json.loads(independent.frozen(independent.LIFT))
    need(lift["schema"] == "n11-fixed14-direct37-s7-lift-v1"
         and (lift["win7"], lift["loss7"], lift["unknown7"],
              lift["winLossConflicts"]) == (13, 1, 0, 0),
         "frozen terminal evidence changed")
    # Historical S7 files are original-first; fixed14 is side-to-move.
    # At odd S7, fixed14 side-to-move WIN means original-first LOSS.
    known_loss = old_loss | {
        row["s7"] for row in lift["rows"] if row["verdict"] == "WIN"
    }
    known_win = old_win | {
        row["s7"] for row in lift["rows"] if row["verdict"] == "LOSS"
    }
    need(not (known_loss & known_win), "frozen WIN/LOSS conflict")
    loss_hits = len(new_s7 & known_loss)
    win_hits = len(new_s7 & known_win)
    need(win_hits == doc["known_win7_hits"] == 0,
          "frozen S7 WIN evidence conflicts with conditional S6 LOSS")

    return {
        "schema": "n11-central49-conditional46-s7-2347-audit-v1",
        "conditional_only": True,
        "s4_outcome": "UNKNOWN", "s6_outcomes": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
        "s5_covered": len(s5), "selected_s6": len(selected),
        "previous_distinct_s7": len(old_s7),
        "final_distinct_s7": len(new_s7),
        "distinct_s7_saved": len(old_s7) - len(new_s7),
        "raw_s7_edges": new_edges,
        "shared_s7_reuses": new_edges - len(new_s7),
        "historical_original_first_loss7_hits": loss_hits,
        "known_original_first_win7_hits": win_hits,
        "optimality_claim": "none; constructive two-for-two improvement",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    data, selected = predecessor()
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    result = verify(doc, data, selected)
    if args.negative:
        for field, value in (
            ("final_distinct_s7_classes", 2346),
            ("known_win7_hits", 1),
            ("s4", "LOSS"),
            ("duplicate_removed", doc["removed_s6_classes"][0]),
            ("invalid_added", "ffffffffffffffffffffffffffffffff"),
        ):
            altered = copy.deepcopy(doc)
            if field == "s4":
                altered["outcomes"]["s4"] = value
            elif field == "duplicate_removed":
                altered["removed_s6_classes"][1] = value
            elif field == "invalid_added":
                altered["added_s6_classes"][1] = value
            else:
                altered[field] = value
            try:
                verify(altered, data, set(selected))
            except (ValueError, KeyError, TypeError):
                continue
            raise AssertionError("tampered certificate accepted: " + field)
        result["negative_tests"] = 5
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
