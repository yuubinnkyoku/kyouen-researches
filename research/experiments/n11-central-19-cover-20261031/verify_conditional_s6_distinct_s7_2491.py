#!/usr/bin/env python3
"""Independent audit of two 1-for-1 S6 swaps reducing conditional S7 duties to 2491.

This checks the full predecessor certificate chain, all 94 S5 parents, every
legal S6->S7 move using separate 4x4 Bareiss geometry, D4 canonicalization,
and the polarity of frozen historical comparison evidence. This does NOT
establish any game verdict or prove global optimality of the cover.
"""
import argparse
import copy
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_conditional_s6_distinct_s7_2553 as previous
import verify_s7_shared_frontier_46 as geometry

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_distinct_s7_2491.json"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def predecessor():
    original = json.loads(previous.ORIGINAL.read_text(encoding="utf-8"))
    data = base.reconstruct()
    base.verify(original, data)
    prior = json.loads(previous.PRIOR.read_text(encoding="utf-8"))
    initial = previous.selected_from_prior(data, original, prior)
    source = json.loads(previous.CERT.read_text(encoding="utf-8"))
    previous.verify(source, data, initial)
    selected = set(initial)
    for swap in source["swaps"]:
        selected.difference_update(base.decode(k) for k in swap["removed_s6_classes"])
        selected.update(base.decode(k) for k in swap["added_s6_classes"])
    need(len(selected) == 46, "predecessor S6 selection changed")
    return data, selected


def verify(doc, data, selected):
    s4, s5, incidence, cost, *_ = data
    need(doc["schema"] == "n11-central49-conditional46-distinct-s7-two-single-swaps-v1"
         and doc["source_certificate"] == previous.CERT.name
         and doc["priority_s4_key"] == base.key(s4)
         and doc["evidence_level"] ==
             "GEOMETRY_ONLY_CONDITIONAL_PROOF_PLAN_NOT_VERDICTS"
         and doc["outcomes"] == {
             "s4": "UNKNOWN", "s6": "UNKNOWN",
             "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN",
         }, "identity, evidence boundary or outcome changed")
    need(len(doc["swaps"]) == 2 and len(selected) == 46
         and set().union(*(incidence[s] for s in selected)) == set(range(94)),
         "invalid predecessor or number of swaps")
    edges, s7 = previous.s7_frontier(selected, cost)
    need((edges, len(s7)) ==
         (doc["previous_raw_s7_edges"], doc["previous_distinct_s7_classes"])
         == (2905, 2553), "predecessor S7 frontier changed")

    steps = []
    for step in doc["swaps"]:
        rm_key, ad_key = step["removed_s6_class"], step["added_s6_class"]
        rm, ad = base.decode(rm_key), base.decode(ad_key)
        need(rm_key == base.key(rm) and ad_key == base.key(ad)
             and rm in selected and ad not in selected
             and ad in incidence and geometry.canonical(ad) == ad,
             "invalid replacement key or class")
        selected = (selected - {rm}) | {ad}
        need(len(selected) == 46
             and set().union(*(incidence[s] for s in selected)) == set(range(94)),
             "replacement breaks the 46-S6 cover of all 94 S5")
        edges, s7 = previous.s7_frontier(selected, cost)
        need((edges, len(s7)) ==
             (step["raw_s7_edges"], step["distinct_s7_classes"]),
             "independent S7 geometry disagrees with swap")
        steps.append({"removed": rm_key, "added": ad_key,
                      "raw_s7_edges": edges, "distinct_s7": len(s7)})

    need((doc["s5_covered"], doc["s6_witnesses"],
          doc["final_raw_s7_edges"], doc["final_distinct_s7_classes"])
         == (94, 46, 2913, 2491), "final proof obligation summary changed")

    old_loss = geometry.inventory(
        geometry.BASE / "all_s7_loss_2232.txt", 2232)
    old_win = geometry.inventory(
        geometry.BASE / "all_s7_win_17.txt", 17)
    lift = json.loads(geometry.frozen(geometry.LIFT))
    need(lift["schema"] == "n11-fixed14-direct37-s7-lift-v1"
         and (lift["win7"], lift["loss7"], lift["unknown7"],
              lift["winLossConflicts"]) == (13, 1, 0, 0),
         "terminal-backed comparison inventory changed")
    # Historical S7 labels refer to ORIGINAL FIRST player's result, not
    # side-to-move: at odd S7, the two polarities are opposite.
    known_original_first_loss = old_loss | {
        r["s7"] for r in lift["rows"] if r["verdict"] == "WIN"}
    known_original_first_win = old_win | {
        r["s7"] for r in lift["rows"] if r["verdict"] == "LOSS"}
    need(not (known_original_first_loss & known_original_first_win),
         "historical WIN/LOSS conflict")
    loss_hits = len(s7 & known_original_first_loss)
    win_hits = len(s7 & known_original_first_win)
    need((loss_hits, win_hits) ==
         (doc["historical_original_first_loss7_hits"],
          doc["known_win7_hits"]) == (7, 0),
         "historical S7 evidence intersection changed")

    return {
        "schema": "n11-central49-conditional46-s7-2491-audit-v1",
        "conditional_only": True,
        "s4_outcome": "UNKNOWN", "s6_outcomes": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
        "s5_covered": len(s5), "selected_s6": len(selected),
        "previous_distinct_s7": 2553, "final_distinct_s7": len(s7),
        "distinct_s7_saved": 2553 - len(s7),
        "raw_s7_edges": edges, "raw_edge_increase": edges - 2905,
        "historical_original_first_loss7_hits": loss_hits,
        "known_original_first_win7_hits": win_hits,
        "unclassified_against_compared_evidence": len(s7) - loss_hits - win_hits,
        "steps": steps, "optimality_claim": "none; constructive local improvement",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    data, selected = predecessor()
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    result = verify(doc, data, selected)
    if args.negative:
        for field, bad_value in (
            ("final_distinct_s7_classes", 2490),
            ("known_win7_hits", 1),
            ("s4", "LOSS"),
            ("first_removed", doc["swaps"][0]["added_s6_class"]),
        ):
            bad = copy.deepcopy(doc)
            if field == "s4":
                bad["outcomes"]["s4"] = bad_value
            elif field == "first_removed":
                bad["swaps"][0]["removed_s6_class"] = bad_value
            else:
                bad[field] = bad_value
            try:
                verify(bad, data, set(selected))
            except (ValueError, KeyError, TypeError):
                continue
            raise AssertionError("tampered certificate accepted: " + field)
        result["negative_tests"] = 4
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
