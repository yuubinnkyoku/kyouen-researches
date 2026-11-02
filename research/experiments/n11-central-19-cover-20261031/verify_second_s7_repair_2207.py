#!/usr/bin/env python3
"""Independent 4x4 geometry audit of the 46-S6 repair after second WIN7.

The 2097-S7 conditional LOSS cover has two certified WIN6 witnesses.
Remove both, hold the other 44 fixed, enumerate all two-for-two replacements
among the 3868 possible S6 classes excluding all terminal-proved WIN6.
This certifies a *conditional* geometric plan, not any S6 LOSS verdict.
"""
import copy
import itertools
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_s7_shared_frontier_46 as geom4
import verify_terminal_s6_55_repair_2097 as previous
import verify_terminal_s7_second_seven_win6 as second

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "conditional_s6_cover_46_after_second_s7_repair_2207.json"
REMOVED = [
    "00000000000000203808000000000020",
    "00000000000000203808000000002000",
]
ADDED = [
    "00000000000000821082002000000000",
    "00000000020000801002002080000000",
]
EXPECTED_MISSING = [5, 16, 50, 58]
EXPECTED_BEST = (2207, 2995, *ADDED)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def audit():
    incidence, costs, prior, old_win6, first_seven, known_win7 = previous.reconstruct()
    old_selected = ((prior - {base.decode(previous.ROOT),
                              base.decode(previous.OTHER)})
                    | {base.decode(k) for k in previous.ADDED})
    need(len(old_selected) == 46, "historical 2097 cover changed")
    terminal = second.audit()
    second_seven = {base.decode(row["canonical_s6"]) for row in terminal["parents"]}
    removed = old_selected & second_seven
    need(sorted(base.key(k) for k in removed) == REMOVED,
         "second terminal S7 did not refute exactly two selected S6")
    fixed = old_selected - removed
    need(len(fixed) == 44, "wrong fixed S6 count")
    known_win6 = old_win6 | first_seven | second_seven
    need(not (fixed & known_win6), "fixed S6 already known WIN")
    covered = set().union(*(incidence[k] for k in fixed))
    missing = set(range(94)) - covered
    need(sorted(missing) == EXPECTED_MISSING, "missing S5 obligations changed")
    candidates = sorted(k for k in incidence
                        if k not in fixed and k not in known_win6
                        and incidence[k] & missing)
    memo = {}

    def kids(k):
        if k not in memo:
            raw = geom4.children(k)
            classes = {base.key(geom4.canonical(child)) for child in raw}
            need(len(raw) == len(classes) == costs[k],
                 "4x4 and historical S7 geometry disagree")
            memo[k] = classes
        return memo[k]

    options = []
    for a, b in itertools.combinations(candidates, 2):
        if not missing <= incidence[a] | incidence[b]:
            continue
        chosen = fixed | {a, b}
        need(len(chosen) == 46
             and set().union(*(incidence[k] for k in chosen)) == set(range(94))
             and not (chosen & known_win6),
             "candidate does not give a safe 46-witness cover")
        raw_edges = 0
        union = set()
        for k in sorted(chosen):
            children = kids(k)
            raw_edges += len(children)
            union.update(children)
        need(not (union & (known_win7 | {base.key(geom4.canonical(second.S7))})),
             "candidate contains certified WIN7 child")
        options.append((len(union), raw_edges, base.key(a), base.key(b)))
    need(len(options) == 3, "two-for-two repair candidate count changed")
    best = min(options)
    need(best == EXPECTED_BEST, "2207-S7 fixed44 minimum changed")
    return {
        "schema": "n11-central49-second-terminal-s7-fixed44-repair-v1",
        "source": previous.MANIFEST.name,
        "terminal_s7": base.key(geom4.canonical(second.S7)),
        "terminal_raw_sha256": second.source.SHA,
        "removed": REMOVED,
        "added": ADDED,
        "eligible_two_for_two_pairs": len(options),
        "fixed_s6": 44,
        "selected_s6": 46,
        "s5_covered": 94,
        "raw_s7_edges": best[1],
        "distinct_s7": best[0],
        "known_win6_conflicts": 0,
        "known_win7_conflicts": 0,
        "evidence_level": "GEOMETRY_ONLY_CONDITIONAL_S6_LOSS_WITNESS_COVER_NOT_VERDICTS",
        "outcomes": {
            "selected_s6": "UNKNOWN",
            "s4": "UNKNOWN",
            "two_stone_root": "UNKNOWN",
            "empty_board": "UNKNOWN",
        },
    }


def main():
    result = audit()
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    need(doc == result, "2207-S7 repair manifest changed")
    tests = 0
    for field, bad in (
        ("distinct_s7", 2206),
        ("eligible_two_for_two_pairs", 2),
        ("known_win6_conflicts", 1),
        ("outcomes", {**doc["outcomes"], "empty_board": "WIN"}),
    ):
        altered = copy.deepcopy(doc)
        altered[field] = bad
        try:
            need(altered == result, "tampering rejected")
        except ValueError:
            tests += 1
        else:
            raise AssertionError("forged repair accepted")
    result["negative_tests"] = tests
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
