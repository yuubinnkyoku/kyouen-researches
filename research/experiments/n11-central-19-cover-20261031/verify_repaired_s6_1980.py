#!/usr/bin/env python3
"""HISTORICAL audit of the superseded 1980-S7 conditional cover.

Seven selected S6 witnesses are now terminal-backed original-first WIN.
Default execution refuses to treat the historical plan as current. Explicit
--allow-superseded-plan reproduces geometry only, never an S6 LOSS verdict.
"""
import argparse
import collections
import copy
import hashlib
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_s6_cover_exclude_certified_win6 as repaired
import verify_conditional_s6_distinct_s7_1984 as comparisons
import verify_s7_shared_frontier_46 as independent

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "conditional_s6_cover_46_exclude_certified_win6.json"
CERT = HERE / "conditional_s6_cover_46_repaired_1980_swaps.txt"
HEADER = [
    "# n11-central49-repaired-46-s6-18-two-swap-v1",
    "# source=conditional_s6_cover_46_exclude_certified_win6.json",
    "# outcomes=s6:UNKNOWN,s4:UNKNOWN,two_stone_root:UNKNOWN,empty_board:UNKNOWN",
    "# conditional geometry only; none of these S6 are established LOSS",
    "# removed1 removed2 added1 added2 raw_s7_edges distinct_s7_classes",
]
EXPECTED_FINAL = (2972, 1980)
EXPECTED_STEPS = 18
# Seven historical selections conflict with terminal-backed WIN6:
# K0624 (two), K0627 (one), K0628 (two), K0638 (one directly,
# plus one more six-stone parent of the same proven WIN7).
CURRENT_CERTIFIED_WIN6 = (
    "00000000000000203808000000000020",
    "00000000000000203808000000002000",
    "00000000000000203808100000000000",
    "00000000000000203808200000000000",
    "0000000000000020380a000000000000",
    "0000000000000020380c000000000000",
    "00000000000200801002000081000000",
)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def load_rows():
    lines = CERT.read_text(encoding="utf-8").splitlines()
    need(lines[:len(HEADER)] == HEADER, "source, provenance or UNKNOWN boundary changed")
    rows = [line.split() for line in lines[len(HEADER):]]
    need(len(rows) == EXPECTED_STEPS and all(len(row) == 6 for row in rows),
         "expected 18 complete two-for-two swaps")
    return rows


def audit(rows, data, initial, win6, win7, memo):
    s4, s5, incidence, cost, *_ = data
    need(len(s5) == 94 and len(initial) == 46, "wrong starting S5/S6 cover")
    current = set(initial)
    need(set().union(*(incidence[s] for s in current)) == set(range(94)),
         "initial S5 cover incomplete")

    def frontier(witnesses):
        union = set()
        edges = 0
        for mask in sorted(witnesses):
            if mask not in memo:
                need(independent.canonical(mask) == mask, "noncanonical S6")
                children = independent.children(mask)  # independent 4x4 Bareiss
                keys = {f"{independent.canonical(c):032x}" for c in children}
                need(len(children) == len(keys) == cost[mask],
                     "independent S6->S7 geometry mismatch")
                memo[mask] = keys
            edges += len(memo[mask])
            union.update(memo[mask])
        need(not (union & win7), "known original-first WIN7 in LOSS7 obligation")
        return edges, union

    initial_edges, initial_union = frontier(current)
    need((initial_edges, len(initial_union)) == (2900, 2711),
         "repaired source S7 frontier changed")
    history = []
    for i, row in enumerate(rows):
        removed_keys, added_keys = row[:2], row[2:4]
        need(removed_keys == sorted(set(removed_keys))
             and added_keys == sorted(set(added_keys)),
             "swaps require sorted distinct pairs")
        removed = {base.decode(k) for k in removed_keys}
        added = {base.decode(k) for k in added_keys}
        need(removed <= current and not (added & current)
             and added <= set(incidence) and not (added & win6),
             "invalid replacement or certified WIN6 selected")
        current = (current - removed) | added
        need(len(current) == 46 and
             set().union(*(incidence[s] for s in current)) == set(range(94)),
             "94 S5 parents not covered")
        need(not (current & win6), "known original-first WIN6 in witness list")
        edges, union = frontier(current)
        need((edges, len(union)) == tuple(int(v) for v in row[4:]),
             f"4x4 independent frontier mismatch at step {i+1}")
        history.append(len(union))
    need((edges, len(union)) == EXPECTED_FINAL, "final S7 cost changed")
    certified_conflicts = sorted({f"{s:032x}" for s in current}
                                 & set(CURRENT_CERTIFIED_WIN6))
    need(certified_conflicts == sorted(CURRENT_CERTIFIED_WIN6),
         "historical plan no longer matches its seven terminal-backed WIN6 conflicts")
    return {
        "schema": "n11-central49-repaired-46-s6-1980-independent-audit-v1",
        "s5_covered": 94,
        "s6_witnesses": 46,
        "two_for_two_swaps": len(rows),
        "initial_distinct_s7": 2711,
        "final_distinct_s7": len(union),
        "distinct_s7_saved": 2711 - len(union),
        "raw_s7_edges": edges,
        "known_win6_conflicts": len(current & win6),
        "current_certified_win6_conflicts": len(certified_conflicts),
        "current_certified_win6_keys": certified_conflicts,
        "plan_status": "SUPERSEDED_BY_CERTIFIED_WIN6",
        "known_win7_conflicts": len(union & win7),
        "history": history,
        "conditional_only": True,
        "s6_outcome": "UNKNOWN",
        "s4_outcome": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
        "optimality_claim": "none; 18 constructive 2-for-2 swaps only"
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    parser.add_argument("--allow-superseded-plan", action="store_true",
                        help="historical geometry replay only; never dispatch work")
    args = parser.parse_args()
    need(args.allow_superseded_plan,
         "SUPERSEDED_BY_CERTIFIED_WIN6: seven selected S6 are proven WIN; "
         "historical replay requires --allow-superseded-plan")
    need(hashlib.sha256(repaired.WIN_CERT.read_bytes()).hexdigest()
         == repaired.WIN_SHA, "terminal-certified WIN6 artifact changed")
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    data = base.reconstruct()
    win6, win7, _ = comparisons.known_comparisons()
    known_win6 = set(win6) | {int(repaired.REFUTED, 16)}
    repaired.verify(source, data, {f"{k:032x}" for k in win6})
    initial = {base.decode(k) for k in source["selected_s6_classes"]}
    rows = load_rows()
    memo = {}
    result = audit(rows, data, initial, known_win6, win7, memo)
    if args.negative:
        for mutation in ("duplicate", "bad_count", "known_win6",
                         "wrong_order", "bad_added", "missing_step"):
            bad = copy.deepcopy(rows)
            if mutation == "duplicate":
                bad[0][1] = bad[0][0]
            elif mutation == "bad_count":
                bad[-1][5] = str(int(bad[-1][5]) - 1)
            elif mutation == "known_win6":
                bad[0][2] = repaired.REFUTED
            elif mutation == "wrong_order":
                bad[0], bad[1] = bad[1], bad[0]
            elif mutation == "bad_added":
                bad[0][2] = "f" * 32
            else:
                bad.pop()
            try:
                audit(bad, data, initial, known_win6, win7, memo)
            except (ValueError, KeyError, TypeError):
                continue
            raise AssertionError("tampered swap certificate accepted: " + mutation)
        result["negative_tests"] = 6
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
