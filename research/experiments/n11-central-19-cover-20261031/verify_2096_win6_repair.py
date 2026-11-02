#!/usr/bin/env python3
"""Independently verify the 2090->2096 conditional cover repair.

The 2090 geometry is historical (its LOSS plan was refuted by a WIN6).
The repair must remove that proven WIN6, cover all 94 S5, avoid all 146
currently inventoried WIN6 and known WIN7, preserve six terminal LOSS7,
and match exact 4x4 integer geometry for both new witnesses.
"""
import copy
from functools import lru_cache
import json
from pathlib import Path

import audit_2090_known_win6_refutation as refutation
import repair_2090_win6_two_swap as search
import focus_s7_worker_2090 as source
import verify_central49_2094_three_swap_descent as geom
import verify_focus_s6_win_strategy as known_win

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_2096_exclude_missed_win6.json"
SCHEMA = "n11-central49-2090-to-2096-exclude-certified-win6-v1"
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}
FIELDS = {
    "schema", "source_certificate", "refuted_certified_win6",
    "removed", "added", "selected_s6_count", "s5_covered",
    "raw_s7_edges", "distinct_s7_classes",
    "terminal_backed_loss7_hits", "known_win6_exclusions",
    "known_win6_conflicts", "known_win7_conflicts",
    "evidence_level", "outcomes",
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


@lru_cache(maxsize=1)
def independent():
    refuted = refutation.audit()
    need(refuted["conditional_2090_loss_cover_valid"] is False,
         "source refutation was not independently reproduced")
    searched = search.audit()
    best = searched["best_preserving"]
    need(best is not None and searched["valid_preserving_all_six"] > 0,
         "no preserving repair exists")
    frontiers, _, old_secured = source.geometry()
    _, s5, incidence, costs, win6, win7, loss7, _ = geom.context()
    removed = {int(k, 16) for k in best["removed"]}
    added = {int(k, 16) for k in best["added"]}
    selected = (set(frontiers) - removed) | added
    excluded6 = win6 | {known_win.ROOT}
    need(known_win.ROOT in removed and not (selected & excluded6)
         and len(excluded6) == 146, "certified WIN6 exclusion failed")
    need(len(selected) == 46
         and set().union(*(incidence[s] for s in selected)) ==
         set(range(len(s5))), "94-S5 cover failed")
    final = dict(frontiers)
    for s in removed:
        del final[s]
    for s in added:
        children = geom.four_frontier(s)
        need(len(children) == costs[s], "new witness child count changed")
        final[s] = children
    union = set().union(*final.values())
    raw = sum(map(len, final.values()))
    secured = union & loss7
    need(secured == old_secured and not (union & win7)
         and (raw, len(union), len(secured)) == (2989, 2096, 6),
         "independent repaired frontier or terminal preservation failed")
    need((best["raw_s7_edges"], best["distinct_s7_classes"],
          best["terminal_proved_loss7"], best["not_proved_s7"]) ==
         (2989, 2096, 6, 2090),
         "exhaustive two-swap search disagrees with independent geometry")
    return {
        "schema": SCHEMA,
        "source_certificate": source.proof.CERT.name,
        "refuted_certified_win6": f"{known_win.ROOT:032x}",
        "removed": best["removed"],
        "added": best["added"],
        "selected_s6_count": len(selected),
        "s5_covered": len(s5),
        "raw_s7_edges": raw,
        "distinct_s7_classes": len(union),
        "terminal_backed_loss7_hits": len(secured),
        "known_win6_exclusions": len(excluded6),
        "known_win6_conflicts": len(selected & excluded6),
        "known_win7_conflicts": len(union & win7),
        "evidence_level": "GEOMETRY_ONLY_CONDITIONAL_COVER_WITH_TERMINAL_WIN6_EXCLUDED",
        "outcomes": UNKNOWN,
    }


def audit(doc):
    need(type(doc) is dict and set(doc) == FIELDS
         and doc.get("schema") == SCHEMA
         and doc.get("outcomes") == UNKNOWN,
         "invalid manifest schema or promoted verdict")
    expected = independent()
    need(doc == expected, "frozen repair differs from independent search and 4x4 geometry")
    return {
        "schema": "n11-central49-2096-independent-repair-verification-v1",
        "selected_s6": 46,
        "s5_covered": 94,
        "raw_s7_edges": 2989,
        "distinct_s7": 2096,
        "terminal_proved_loss7": 6,
        "not_proved_s7": 2090,
        "excluded_known_win6": 146,
        "known_win6_conflicts": 0,
        "known_win7_conflicts": 0,
        "removed": doc["removed"],
        "added": doc["added"],
        "s6_outcome": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
    }


def negative_tests(doc):
    for mode in ("source", "refuted", "removed", "added",
                 "raw", "secured", "verdict", "win6"):
        bad = copy.deepcopy(doc)
        if mode == "source":
            bad["source_certificate"] = "obsolete.json"
        elif mode == "refuted":
            bad["refuted_certified_win6"] = "0" * 32
        elif mode == "removed":
            bad["removed"][0] = bad["added"][0]
        elif mode == "added":
            bad["added"][0] = bad["removed"][0]
        elif mode == "raw":
            bad["raw_s7_edges"] -= 1
        elif mode == "secured":
            bad["terminal_backed_loss7_hits"] -= 1
        elif mode == "verdict":
            bad["outcomes"]["s6"] = "LOSS"
        else:
            bad["known_win6_conflicts"] += 1
        try:
            audit(bad)
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError("altered 2096 repair accepted: " + mode)
    return 8


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--negative", action="store_true")
    args = p.parse_args()
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    result = audit(doc)
    if args.negative:
        result["negative_tests"] = negative_tests(doc)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
