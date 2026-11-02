#!/usr/bin/env python3
"""Independent 4x4 geometry audit of the 2301-S7 conditional repair.

Seven terminal-backed original-first WIN6 witnesses in the superseded 1980
plan are removed, and seven new UNKNOWN S6 witnesses cover all 94 S5 parents.
This proves only geometric feasibility and the S7 obligation count.
"""
import argparse
import copy
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_s6_cover_exclude_certified_win6 as repaired
import verify_repaired_s6_1980 as historical
import verify_conditional_s6_distinct_s7_1984 as comparisons
import verify_s7_shared_frontier_46 as geometry
import verify_shared_s7_seven_win6 as shared
import verify_terminal_s7_seven_win6 as first
import verify_terminal_s7_second_seven_win6 as second
import verify_focus_s6_win_refutation as focus

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_post_seven_win6_repair_2301.json"
REMOVED = tuple(sorted(historical.CURRENT_CERTIFIED_WIN6))
ADDED = (
    "00000000000000003808100001000000",
    "0000000000000000380c200000000000",
    "00000000000000203800100000002000",
    "00000000000000203800800000080000",
    "00000000000000203804200000000000",
    "00000000000000803082002000000000",
    "00000000000000803082008000000000",
)
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}
FOCUS_PARENT_KEYS = {
    "0000000000000000380a100000000000",
    "0000000000000020180a100000000000",
    "0000000000000020280a100000000000",
    "0000000000000020300a100000000000",
    "00000000000000203802100000000000",
    "00000000000000203808100000000000",
    "0000000000000020380a000000000000",
}

# These five S7 roots have terminal-backed original-first LOSS proofs in K0637.
# This verifier audits only their geometric overlap with the CURRENT cover;
# it does not re-run the K0637 terminal strategies.
K0637_TERMINAL_LOSS7 = (
    "00000000000000203808000000000120",
    "0000000000000020380a000000004000",
    "00000000000000a03808100000000000",
    "00000000000002043800800000040000",
    "00000000000200801082008100000000",
)
K0637_OUTSIDE_CURRENT_COVER = "00000000000000a03808100000000000"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def comparison_inventories():
    old_win6, old_win7, _ = comparisons.known_comparisons()
    terminal_win7 = {
        "00000000000000603808200000000000",
        json.loads((HERE / "terminal_s7_seven_s6_parents.json").read_text())["shared_s7"],
        json.loads((HERE / "terminal_s7_second_seven_s6_parents.json").read_text())["shared_s7"],
        focus.ROOT,
    }
    need(len(terminal_win7) == 4 and focus.ROOT ==
         "0000000000000020380a100000000000",
         "terminal WIN7 roots changed")
    win7 = set(old_win7) | terminal_win7
    need(len(win7) == 23, "terminal WIN7 comparison count changed")
    old_terminal_parents = set(shared.EXPECTED) | set(first.EXPECTED_KEYS) | set(second.EXPECTED_KEYS)
    need(len(old_terminal_parents) == 21, "previous terminal WIN6 parents changed")
    focus_root = int(focus.ROOT, 16)
    focus_parents = set()
    for p in geometry.points(focus_root):
        parent = focus_root ^ (1 << p)
        need(focus_root in geometry.children(parent),
             "a six-stone parent cannot legally return to K0638 WIN7")
        focus_parents.add(f"{geometry.canonical(parent):032x}")
    need(focus_parents == FOCUS_PARENT_KEYS and not
         (focus_parents & ({f"{m:032x}" for m in old_win6} | old_terminal_parents)),
         "K0638 WIN7 parent keys or non-overlap changed")
    win6 = {f"{m:032x}" for m in old_win6} | old_terminal_parents | focus_parents
    need(len(win6) == 145 and set(REMOVED) <= win6,
         "terminal-backed WIN6 inventory changed")
    return old_win6, old_win7, win6, win7, focus_parents


def verify(doc):
    data = base.reconstruct()
    old_win6, old_win7, win6, win7, focus_parents = comparison_inventories()
    source = json.loads(repaired.CERT.read_text(encoding="utf-8"))
    repaired.verify(source, data, {f"{m:032x}" for m in old_win6})
    initial = {base.decode(k) for k in source["selected_s6_classes"]}
    rows = historical.load_rows()
    memo = {}
    history = historical.audit(
        rows, data, initial, set(old_win6) | {int(repaired.REFUTED, 16)},
        set(old_win7), memo)
    need(history["current_certified_win6_conflicts"] == 7 and
         history["plan_status"] == "SUPERSEDED_BY_CERTIFIED_WIN6",
         "source must be a known invalid historical cover")
    selected = set(initial)
    for row in rows:
        removed = {base.decode(k) for k in row[:2]}
        added = {base.decode(k) for k in row[2:4]}
        need(removed <= selected and not (added & selected),
             "historical chain changed")
        selected = (selected - removed) | added
    need(len(selected) == 46 and
         {f"{m:032x}" for m in selected} & win6 == set(REMOVED),
         "historical selected WIN6 conflicts differ from seven")
    kept = selected - {base.decode(k) for k in REMOVED}
    added = {base.decode(k) for k in ADDED}
    need(len(kept) == 39 and len(added) == 7 and not (added & selected),
         "not a direct seven-for-seven replacement")
    final = kept | added
    incidence, cost = data[2], data[3]
    need(len(final) == 46 and all(m in incidence for m in final)
         and set().union(*(incidence[m] for m in final)) == set(range(94)),
         "final 46 witnesses fail to cover all 94 S5 classes")
    need(not ({f"{m:032x}" for m in final} & win6),
         "known WIN6 selected as a LOSS witness")

    def children(m):
        if m not in memo:
            need(geometry.canonical(m) == m and m.bit_count() == 6,
                 "noncanonical six-stone witness")
            raw = geometry.children(m)
            canonical = {f"{geometry.canonical(c):032x}" for c in raw}
            need(len(raw) == len(canonical) == cost[m],
                 "independent 4x4 S6-to-S7 geometry differs from 3x3")
            memo[m] = canonical
        return memo[m]

    raw = sum(len(children(m)) for m in final)
    frontier = set().union(*(children(m) for m in final))
    need((raw, len(frontier)) == (2992, 2301),
         "repaired seven-stone obligation count changed")
    need(not (frontier & win7), "known WIN7 in proposed LOSS7 obligation")

    # K0637 proved five original-first LOSS7 roots by fixed terminal strategies.
    # Reuse only exact D4-canonical matches, not solver-trusted cache labels.
    loss7 = set(K0637_TERMINAL_LOSS7)
    need(len(loss7) == 5 and not (loss7 & win7),
         "K0637 terminal LOSS7 inventory conflicts with WIN7")
    for key in loss7:
        root = int(key, 16)
        need(root.bit_count() == 7 and geometry.canonical(root) == root,
             "noncanonical K0637 terminal LOSS7 key")
    secured = frontier & loss7
    secured_by_witness = {
        f"{m:032x}": sorted(children(m) & loss7)
        for m in sorted(final) if children(m) & loss7
    }
    secured_edges = sum(len(v) for v in secured_by_witness.values())
    need(len(secured) == 4 and secured_edges == 4
         and len(secured_by_witness) == 2
         and loss7 - frontier == {K0637_OUTSIDE_CURRENT_COVER},
         "K0637 independently proved LOSS7 overlap changed")

    expected = {
        "schema": "n11-central49-conditional46-post-seven-win6-repair-v1",
        "source_certificate": historical.CERT.name,
        "removed_certified_win6": list(REMOVED),
        "added_s6_classes": list(ADDED),
        "s6_witnesses": 46,
        "s5_covered": 94,
        "raw_s7_edges": 2992,
        "distinct_s7_classes": 2301,
        "known_win6_comparison_classes": 145,
        "known_win7_comparison_classes": 23,
        "known_win6_conflicts": 0,
        "known_win7_conflicts": 0,
        "evidence_level": "GEOMETRY_ONLY_CONDITIONAL_REPAIR_NOT_VERDICTS",
        "outcomes": UNKNOWN,
        "caveat": "Constructive direct 7-for-7 replacement of the historical 1980 S7 witness set, excluding all 7 currently identified terminal-backed WIN6. The 2301 S7 classes are proof obligations, not proven LOSS7; no optimality or root outcome is claimed.",
    }
    need(doc == expected, "conditional repair manifest changed")
    return {
        "schema": "n11-central49-post-seven-win6-2301-independent-audit-v1",
        "source_historical_plan": "SUPERSEDED_BY_CERTIFIED_WIN6",
        "removed_win6": list(REMOVED),
        "new_win6_from_K0638_parent_lift": sorted(focus_parents),
        "comparison_win6": len(win6),
        "comparison_win7": len(win7),
        "selected_s6": 46,
        "covered_s5": 94,
        "raw_s7_edges": raw,
        "distinct_s7": len(frontier),
        "known_win6_conflicts": 0,
        "known_win7_conflicts": 0,
        "k0637_terminal_loss7_secured_classes": len(secured),
        "k0637_terminal_loss7_secured_edges": secured_edges,
        "k0637_terminal_loss7_secured_witnesses": len(secured_by_witness),
        "k0637_terminal_loss7_not_in_cover": sorted(loss7 - frontier),
        "k0637_terminal_loss7_hits_by_s6": secured_by_witness,
        "s7_not_secured_by_k0637": len(frontier - secured),
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
    result = verify(doc)
    if args.negative:
        for kind in ("refuted_witness", "wrong_cost", "verdict", "provenance"):
            bad = copy.deepcopy(doc)
            if kind == "refuted_witness":
                bad["added_s6_classes"][0] = REMOVED[0]
            elif kind == "wrong_cost":
                bad["distinct_s7_classes"] -= 1
            elif kind == "verdict":
                bad["outcomes"]["s6"] = "LOSS"
            else:
                bad["source_certificate"] = "unverified.txt"
            try:
                need(bad == doc, "tampered certificate")
            except ValueError:
                continue
            raise AssertionError("tampering accepted: " + kind)
        result["negative_tests"] = 4
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
