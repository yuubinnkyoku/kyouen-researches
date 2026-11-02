#!/usr/bin/env python3
"""Independently refute the 2097-S7 conditional LOSS plan by a second WIN7.

A single selected S6 with a terminal-proved WIN7 child is not a LOSS witness.
This audit finds two such selected S6 parents. It does NOT repair the cover.
"""
import copy
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_s7_shared_frontier_46 as geom4
import verify_terminal_s6_55_repair_2097 as old
import verify_terminal_s7_second_seven_win6 as second

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "conditional_s6_cover_2097_refuted_by_second_s7.json"
EXPECTED = [
    "00000000000000203808000000000020",
    "00000000000000203808000000002000",
]


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def audit():
    incidence, _, prior, old_win6, first_seven, _ = old.reconstruct()
    selected = ((prior - {base.decode(old.ROOT), base.decode(old.OTHER)})
                | {base.decode(k) for k in old.ADDED})
    need(len(selected) == 46
         and set().union(*(incidence[k] for k in selected)) == set(range(94)),
         "historical 2097 geometric cover changed")
    result = second.audit()
    new_win6 = {base.decode(r["canonical_s6"]) for r in result["parents"]}
    need(len(new_win6) == 7 and not (new_win6 & first_seven),
         "second terminal S7 parents overlap first seven")
    conflicts = sorted(base.key(k) for k in selected & new_win6)
    need(conflicts == EXPECTED, "two selected WIN6 conflicts changed")
    s7 = base.key(geom4.canonical(second.S7))
    for k in selected & new_win6:
        children = {base.key(geom4.canonical(c)) for c in geom4.children(k)}
        need(s7 in children, "selected S6 lacks the terminal-proved WIN7")
    return {
        "schema": "n11-central49-2097-conditional-cover-refuted-v1",
        "source": old.MANIFEST.name,
        "terminal_s7": s7,
        "terminal_sha256": second.source.SHA,
        "refuted_selected_s6": conflicts,
        "refuted_selected_s6_count": 2,
        "historical_s6_selected": 46,
        "historical_s5_covered": 94,
        "historical_distinct_s7": 2097,
        "conditional_loss_cover_valid": False,
        "replan_required": True,
        "new_s6_loss_proofs": 0,
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
    }


def check(doc, result):
    need(doc == result, "refutation manifest altered")


def main():
    result = audit()
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check(doc, result)
    negative = 0
    for field, value in (
        ("refuted_selected_s6_count", 1),
        ("conditional_loss_cover_valid", True),
        ("replan_required", False),
        ("empty_board", "WIN"),
    ):
        bad = copy.deepcopy(doc)
        bad[field] = value
        try:
            check(bad, result)
        except ValueError:
            negative += 1
        else:
            raise AssertionError("tampered refutation accepted")
    result["negative_tests"] = negative
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
