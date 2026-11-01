#!/usr/bin/env python3
"""Independently audit a 46-S6 conditional cover with 2,553 distinct S7 children.

The two local substitutions are constructive upper bounds, not optimality
claims. Uses the separate 4x4 Bareiss determinant and D4 geometry to check
all S6 -> S7 edges, rather than trusting the saved child counts. Historical
S7 outcomes are comparison evidence only. No S6 verdict is inferred.
"""
import argparse
import copy
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_conditional_s6_shared_s7_optimal as previous
import verify_s7_shared_frontier_46 as independent

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_distinct_s7_2553.json"
PRIOR = HERE / "conditional_s6_cover_46_shared_s7_optimal.json"
ORIGINAL = HERE / "conditional_s6_cover_46.json"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def selected_from_prior(data, original, prior):
    reduction = previous.tight_reduction(data, original)
    solutions = previous.enumerate_optima(data, reduction)
    previous.verify(prior, original, data, reduction, solutions)
    forced = reduction[0]
    flex = {base.decode(k) for k in prior["flexible_s6_classes"]}
    return forced | flex


def s7_frontier(selected, cost):
    result = set()
    edges = 0
    for s6 in sorted(selected):
        # 4x4 Bareiss, separate from the 3x3 incidence reconstruction.
        mask = independent.decode(base.key(s6), 6)
        need(independent.canonical(mask) == mask, "noncanonical S6")
        raw = independent.children(mask)
        keys = {f"{independent.canonical(child):032x}" for child in raw}
        need(len(raw) == len(keys) == cost[s6],
             "independent S7 child geometry disagrees")
        edges += len(raw)
        result.update(keys)
    return edges, result


def verify(doc, data, initial):
    s4, s5, incidence, cost, *_ = data
    need(doc["schema"] ==
         "n11-central49-conditional46-distinct-s7-two-step-improvement-v1"
         and doc["source_certificate"] == PRIOR.name
         and doc["priority_s4_key"] == base.key(s4)
         and doc["evidence_level"] ==
         "GEOMETRY_ONLY_CONDITIONAL_PROOF_PLAN_NOT_VERDICTS"
         and doc["outcomes"] == {
             "s4": "UNKNOWN", "s6": "UNKNOWN",
             "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"
         }, "identity, scope, or outcome changed")
    need(len(doc["swaps"]) == 2 and len(initial) == 46,
         "unexpected number of swaps or initial S6")
    need(set().union(*(incidence[s] for s in initial)) == set(range(94)),
         "initial S5 coverage incomplete")
    edges, initial_s7 = s7_frontier(initial, cost)
    need((edges, len(initial_s7)) ==
         (doc["previous_raw_s7_edges"], doc["previous_distinct_s7_classes"])
         == (2897, 2662), "source plan changed")

    selected = set(initial)
    steps = []
    for index, swap in enumerate(doc["swaps"]):
        removed = swap["removed_s6_classes"]
        added = swap["added_s6_classes"]
        need(isinstance(removed, list) and isinstance(added, list)
             and len(removed) == len(added) == 2
             and removed == sorted(set(removed))
             and added == sorted(set(added)), "bad two-for-two swap")
        rm = {base.decode(k) for k in removed}
        ad = {base.decode(k) for k in added}
        need(rm <= selected and not (ad & selected)
             and ad <= set(incidence), "swap is not a valid replacement")
        selected = (selected - rm) | ad
        need(len(selected) == 46
             and set().union(*(incidence[s] for s in selected)) == set(range(94)),
             "a swap breaks the 46-S6 cover")
        edges, s7 = s7_frontier(selected, cost)
        need((edges, len(s7)) ==
             (swap["raw_s7_edges"], swap["distinct_s7_classes"]),
             "independent S7 count differs at swap step")
        steps.append({"step": index + 1, "raw_s7_edges": edges,
                      "distinct_s7_classes": len(s7)})

    need((doc["s5_covered"], doc["s6_witnesses"],
          doc["final_raw_s7_edges"], doc["final_distinct_s7_classes"])
         == (94, 46, 2905, 2553), "final coverage or cost changed")
    old_win = independent.inventory(
        independent.BASE / "all_s7_win_17.txt", 17)
    lift = json.loads(independent.frozen(independent.LIFT))
    need(lift["schema"] == "n11-fixed14-direct37-s7-lift-v1"
         and (lift["win7"], lift["loss7"], lift["unknown7"],
              lift["winLossConflicts"]) == (13, 1, 0, 0),
         "fixed14 polarity changed")
    # The lift file is side-to-move; at odd S7 its LOSS is original-first WIN.
    known_win = old_win | {row["s7"] for row in lift["rows"]
                           if row["verdict"] == "LOSS"}
    win_hits = len(s7 & known_win)
    need(win_hits == doc["known_win7_hits"] == 0,
         "known original-first WIN7 refutes a proposed S6 LOSS")
    old_loss = independent.inventory(
        independent.BASE / "all_s7_loss_2232.txt", 2232)
    known_loss = old_loss | {row["s7"] for row in lift["rows"]
                             if row["verdict"] == "WIN"}
    need(not (known_win & known_loss), "historical WIN7/LOSS7 conflict")
    return {
        "schema": "n11-central49-conditional46-s7-2553-audit-v1",
        "conditional_only": True,
        "s4_outcome": "UNKNOWN", "s6_outcomes": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
        "s5_covered": 94, "selected_s6": len(selected),
        "initial_distinct_s7": len(initial_s7),
        "final_distinct_s7": len(s7),
        "distinct_s7_saved": len(initial_s7) - len(s7),
        "raw_s7_edges": edges,
        "raw_s7_edge_increase": edges - 2897,
        "known_win7_hits": win_hits,
        "historical_solver_trusted_loss7_hits": len(s7 & known_loss),
        "steps": steps,
        "optimality_claim": "none; constructive improvement only"
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    original = json.loads(ORIGINAL.read_text(encoding="utf-8"))
    data = base.reconstruct()
    base.verify(original, data)
    prior = json.loads(PRIOR.read_text(encoding="utf-8"))
    initial = selected_from_prior(data, original, prior)
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    result = verify(doc, data, initial)
    if args.negative:
        for field, value in (("final_distinct_s7_classes", 2552),
                             ("known_win7_hits", 1),
                             ("s4", "LOSS")):
            bad = copy.deepcopy(doc)
            if field == "s4":
                bad["outcomes"]["s4"] = value
            else:
                bad[field] = value
            try:
                verify(bad, data, initial)
            except (ValueError, KeyError, TypeError):
                continue
            raise AssertionError(f"tampered {field} accepted")
        bad = copy.deepcopy(doc)
        bad["swaps"][0]["added_s6_classes"][0] = (
            bad["swaps"][0]["removed_s6_classes"][0])
        try:
            verify(bad, data, initial)
        except (ValueError, KeyError, TypeError):
            pass
        else:
            raise AssertionError("invalid replacement accepted")
        result["negative_tests"] = 4
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
