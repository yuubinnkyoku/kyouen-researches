#!/usr/bin/env python3
"""Independently audit a 46-S6 conditional cover with 2,417 distinct S7 children.

The input is a two-for-two substitution from the independently audited
2,491-class cover. Rebuild all 94 S5 parents and 3,868 S6 candidates using
3x3 integer geometry; independently rebuild all selected S6->S7 edges with
4x4 Bareiss determinants and D4. This is NOT a game-outcome certificate.
"""
import argparse
import copy
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_conditional_s6_distinct_s7_2491 as previous
import verify_s7_shared_frontier_46 as independent

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_distinct_s7_2417.json"
SOURCE = HERE / "conditional_s6_cover_46_distinct_s7_2491.json"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def predecessor():
    data, initial = previous.predecessor()
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    previous.verify(source, data, set(initial))
    selected = set(initial)
    for swap in source["swaps"]:
        removed = base.decode(swap["removed_s6_class"])
        added = base.decode(swap["added_s6_class"])
        need(removed in selected and added not in selected,
             "invalid predecessor replacement")
        selected = (selected - {removed}) | {added}
    need(len(selected) == 46, "predecessor S6 count changed")
    return data, selected


def verify(doc, data, selected):
    s4, s5, incidence, cost, *_ = data
    need(doc["schema"] ==
         "n11-central49-conditional46-distinct-s7-two-for-two-2417-v1"
         and doc["source_certificate"] == SOURCE.name
         and doc["priority_s4_key"] == base.key(s4)
         and doc["evidence_level"] ==
             "GEOMETRY_ONLY_CONDITIONAL_PROOF_PLAN_NOT_VERDICTS"
         and doc["outcomes"] == {
             "s4": "UNKNOWN", "s6": "UNKNOWN",
             "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN",
         }, "invalid identity, evidence level, or outcome")

    need(len(s5) == 94 and len(selected) == 46
         and set().union(*(incidence[k] for k in selected)) ==
             set(range(94)), "predecessor S5 coverage changed")
    edges, old_s7 = previous.previous.s7_frontier(selected, cost)
    need((edges, len(old_s7)) ==
         (doc["previous_raw_s7_edges"],
          doc["previous_distinct_s7_classes"]) == (2913, 2491),
         "predecessor S7 geometry changed")

    removed = doc["removed_s6_classes"]
    added = doc["added_s6_classes"]
    need(isinstance(removed, list) and isinstance(added, list)
         and len(removed) == len(added) == 2
         and removed == sorted(set(removed))
         and added == sorted(set(added)), "bad two-for-two replacement")
    rm = {base.decode(k) for k in removed}
    ad = {base.decode(k) for k in added}
    need(rm <= selected and not (ad & selected)
         and ad <= set(incidence)
         and all(independent.canonical(k) == k for k in ad),
         "replacement keys invalid or noncanonical")
    selected = (selected - rm) | ad
    need(len(selected) == 46
         and set().union(*(incidence[k] for k in selected)) ==
             set(range(94)), "replacement loses an S5 parent")
    edges, new_s7 = previous.previous.s7_frontier(selected, cost)
    need((doc["s5_covered"], doc["s6_witnesses"],
          doc["final_raw_s7_edges"], doc["final_distinct_s7_classes"],
          doc["distinct_s7_saved"], doc["shared_s7_reuses"]) ==
         (94, 46, edges, len(new_s7),
          len(old_s7) - len(new_s7), edges - len(new_s7)) ==
         (94, 46, 2919, 2417, 74, 502),
         "new S7 geometry or recorded reduction disagrees")

    old_win = independent.inventory(
        independent.BASE / "all_s7_win_17.txt", 17)
    old_loss = independent.inventory(
        independent.BASE / "all_s7_loss_2232.txt", 2232)
    lift = json.loads(independent.frozen(independent.LIFT))
    need(lift["schema"] == "n11-fixed14-direct37-s7-lift-v1"
         and (lift["win7"], lift["loss7"], lift["unknown7"],
              lift["winLossConflicts"]) == (13, 1, 0, 0),
         "frozen terminal comparison evidence changed")
    # Historical inventory is original-first; the terminal lift is
    # side-to-move. At odd S7 these labels have opposite polarities.
    known_original_first_win = old_win | {
        row["s7"] for row in lift["rows"] if row["verdict"] == "LOSS"
    }
    known_original_first_loss = old_loss | {
        row["s7"] for row in lift["rows"] if row["verdict"] == "WIN"
    }
    need(not (known_original_first_win & known_original_first_loss),
         "conflicting frozen comparison evidence")
    win_hits = len(new_s7 & known_original_first_win)
    need(win_hits == 0, "historical WIN7 conflicts with S6 LOSS hypothesis")
    loss_hits = len(new_s7 & known_original_first_loss)

    return {
        "schema": "n11-central49-conditional46-s7-2417-audit-v1",
        "conditional_only": True,
        "s4_outcome": "UNKNOWN", "s6_outcomes": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
        "s5_covered": 94, "selected_s6": len(selected),
        "previous_distinct_s7": len(old_s7),
        "final_distinct_s7": len(new_s7),
        "distinct_s7_saved": len(old_s7) - len(new_s7),
        "raw_s7_edges": edges,
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
            ("final_distinct_s7_classes", 2416),
            ("distinct_s7_saved", 75),
            ("s4", "LOSS"),
            ("added_duplicate", doc["added_s6_classes"][0]),
        ):
            altered = copy.deepcopy(doc)
            if field == "s4":
                altered["outcomes"]["s4"] = value
            elif field == "added_duplicate":
                altered["added_s6_classes"][1] = value
            else:
                altered[field] = value
            try:
                verify(altered, data, set(selected))
            except (ValueError, KeyError, TypeError):
                continue
            raise AssertionError("tampered certificate accepted: " + field)
        result["negative_tests"] = 4
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
