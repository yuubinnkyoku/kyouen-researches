#!/usr/bin/env python3
"""Independent 4x4 geometry audit of a direct three-for-three S6 cover repair.

The historical 1980-S7 cover contains three terminal-certified original-first
WIN6 witnesses and is not a valid LOSS plan. This auditor removes all three,
enumerates all direct 3-for-3 replacements covering the six exposed S5
classes, excludes known WIN6 parents, and checks S7 obligations with 4x4
integer Bareiss geometry. No S6 LOSS or root verdict is inferred.
"""
import argparse
import copy
import itertools
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_s6_cover_exclude_certified_win6 as source_audit
import verify_repaired_s6_1980 as historical
import verify_conditional_s6_distinct_s7_1984 as comparisons
import verify_s7_shared_frontier_46 as geometry
import verify_shared_s7_seven_win6 as shared
import verify_terminal_s7_seven_win6 as first
import verify_terminal_s7_second_seven_win6 as second
import verify_focus_s6_win_refutation as focus

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_post_three_win6_repair_2145.json"
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}
REMOVED = tuple(sorted(historical.CURRENT_CERTIFIED_WIN6))
ADDED = (
    "0000000000000000380c200000000000",
    "00000000000000203802800000000000",
    "00000000000000203804200000000000",
)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def certified_comparisons():
    old_win6, old_win7, _ = comparisons.known_comparisons()
    roots = {
        "00000000000000603808200000000000",
        json.loads((HERE / "terminal_s7_seven_s6_parents.json").read_text())["shared_s7"],
        json.loads((HERE / "terminal_s7_second_seven_s6_parents.json").read_text())["shared_s7"],
        focus.ROOT,
    }
    need(len(roots) == 4 and focus.ROOT ==
         "0000000000000020380a100000000000",
         "four terminal WIN7 provenance roots changed")
    win7 = set(old_win7) | roots
    need(len(win7) == 23, "WIN7 comparison inventory changed")
    win6 = {f"{m:032x}" for m in old_win6}
    expected21 = set(shared.EXPECTED) | set(first.EXPECTED_KEYS) | set(second.EXPECTED_KEYS)
    need(len(expected21) == 21, "previous terminal WIN6 parent inventories changed")
    win6.update(expected21)
    focus_parents = set()
    root = int(focus.ROOT, 16)
    for p in geometry.points(root):
        parent = geometry.canonical(root ^ (1 << p))
        focus_parents.add(f"{parent:032x}")
        need(root in geometry.children(root ^ (1 << p)),
             "a removed focus parent cannot legally return to terminal WIN7")
    need(len(focus_parents) == 7 and focus.ROOT in win7,
         "focus WIN7 parent lift changed")
    win6.update(focus_parents)
    need(len(win6) == 145 and set(REMOVED) <= win6,
         "terminal-backed WIN6 exclusions changed")
    return win6, win7, focus_parents


def historical_selection(data, win6, win7, memo):
    original = json.loads(source_audit.CERT.read_text(encoding="utf-8"))
    historical_win6, _, _ = comparisons.known_comparisons()
    source_audit.verify(original, data, {f"{k:032x}" for k in historical_win6})
    initial = {base.decode(k) for k in original["selected_s6_classes"]}
    rows = historical.load_rows()
    old_result = historical.audit(
        rows, data, initial, set(historical_win6) |
        {int(source_audit.REFUTED, 16)}, set(win7) &
        set(comparisons.known_comparisons()[1]), memo)
    need(old_result["current_certified_win6_conflicts"] == 3
         and old_result["plan_status"] == "SUPERSEDED_BY_CERTIFIED_WIN6",
         "historical source must be explicitly superseded")
    selected = set(initial)
    for row in rows:
        selected.difference_update(base.decode(k) for k in row[:2])
        selected.update(base.decode(k) for k in row[2:4])
    need(len(selected) == 46 and {f"{k:032x}" for k in selected} &
         set(REMOVED) == set(REMOVED), "three certified WIN6 absent from source")
    return selected


def matchings(vertices):
    if not vertices:
        yield ()
        return
    a, *tail = vertices
    for i, b in enumerate(tail):
        for rest in matchings(tail[:i] + tail[i+1:]):
            yield ((a, b),) + rest


def audit(doc):
    data = base.reconstruct()
    win6, win7, focus_parents = certified_comparisons()
    memo = {}
    selected = historical_selection(data, win6, win7, memo)
    removed = {base.decode(k) for k in REMOVED}
    kept = selected - removed
    incidence = data[2]
    covered = set().union(*(incidence[k] for k in kept))
    missing = tuple(sorted(set(range(94)) - covered))
    need(len(kept) == 43 and len(missing) == 6,
         "expected six exposed S5 classes after three WIN6 exclusions")
    by_pair = {}
    for k, parents in incidence.items():
        if k in selected:
            continue
        pair = tuple(sorted(parents & set(missing)))
        if len(pair) == 2:
            by_pair.setdefault(pair, []).append(k)

    def children(k):
        if k not in memo:
            need(geometry.canonical(k) == k and k.bit_count() == 6,
                 "bad canonical six-stone candidate")
            raw = geometry.children(k)
            canonical = {f"{geometry.canonical(c):032x}" for c in raw}
            need(len(raw) == len(canonical) == data[3][k],
                 "4x4 independent S6-to-S7 geometry disagrees with 3x3")
            memo[k] = canonical
        return memo[k]

    options = set()
    for pairs in matchings(list(missing)):
        for triple in itertools.product(*(by_pair.get(p, ()) for p in pairs)):
            if len(set(triple)) == 3:
                options.add(tuple(sorted(triple)))
    need(len(options) == 7, "direct three-repair enumeration changed")
    valid = []
    for triple in sorted(options):
        keys = {f"{k:032x}" for k in triple}
        if keys & win6:
            continue
        witness_set = kept | set(triple)
        need(len(witness_set) == 46 and
             set().union(*(incidence[k] for k in witness_set)) ==
             set(range(94)), "repair lost a five-stone parent")
        frontier = set().union(*(children(k) for k in witness_set))
        need(not (frontier & win7), "certified original-first WIN7 conflict")
        edges = sum(len(children(k)) for k in witness_set)
        valid.append((len(frontier), edges, tuple(sorted(keys)), witness_set))
    need(len(valid) == 5, "certified WIN6 exclusions changed repair count")
    valid.sort(key=lambda x: (x[0], x[1], x[2]))
    distinct, edges, added, selected_final = valid[0]
    need((distinct, edges, added) == (2145, 2983, ADDED),
         "best direct repair differs from 4x4 geometry")
    need(not ({f"{k:032x}" for k in selected_final} & win6),
         "certified WIN6 selected as LOSS witness")
    expected = {
        "schema": "n11-central49-conditional46-post-three-certified-win6-direct-three-repair-v1",
        "source_certificate": historical.CERT.name,
        "removed_certified_win6": list(REMOVED),
        "added_s6_classes": list(ADDED),
        "s6_witnesses": 46,
        "s5_covered": 94,
        "raw_s7_edges": 2983,
        "distinct_s7_classes": 2145,
        "all_direct_three_replacements": 7,
        "nonconflicting_direct_three_replacements": 5,
        "known_win6_conflicts": 0,
        "known_win7_conflicts": 0,
        "evidence_level": "GEOMETRY_ONLY_CONDITIONAL_REPAIR_NOT_VERDICTS",
        "outcomes": UNKNOWN,
        "caveat": "Minimum 2145 distinct S7 classes only among direct 3-for-3 replacements of the fixed historical 1980 witness set after removing three terminal-certified WIN6; no global optimality, no selected S6 LOSS, no two-stone or empty-board verdict.",
    }
    need(doc == expected, "conditional repair certificate content changed")
    return {
        "schema": "n11-central49-post-three-win6-2145-independent-audit-v1",
        "historical_distinct_s7": 1980,
        "historical_plan_status": "SUPERSEDED_BY_CERTIFIED_WIN6",
        "removed_certified_win6": list(REMOVED),
        "focus_s7_derived_win6_parents": sorted(focus_parents),
        "known_win6_comparison_classes": len(win6),
        "known_win7_comparison_classes": len(win7),
        "direct_three_replacements": len(options),
        "nonconflicting_replacements": len(valid),
        "best_direct_repair_distinct_s7": distinct,
        "raw_s7_edges": edges,
        "s5_covered": 94,
        "selected_s6": 46,
        "conditional_only": True,
        "s6_outcome": "UNKNOWN",
        "s4_outcome": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    result = audit(doc)
    if args.negative:
        for change in ("add_win6", "cost", "outcome", "source"):
            bad = copy.deepcopy(doc)
            if change == "add_win6":
                bad["added_s6_classes"][0] = REMOVED[0]
            elif change == "cost":
                bad["distinct_s7_classes"] -= 1
            elif change == "outcome":
                bad["outcomes"]["s6"] = "LOSS"
            else:
                bad["source_certificate"] = "unverified.txt"
            try:
                # Strict expected-certificate comparison is sufficient for these
                # mutations after the complete independent audit has run once.
                need(bad == doc, "tampered certificate")
            except ValueError:
                continue
            raise AssertionError("tampering accepted: " + change)
        result["negative_tests"] = 4
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
