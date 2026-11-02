#!/usr/bin/env python3
"""Lift five terminal-certified original-first LOSS7 roots through their
winning first moves to every seven-stone parent of the resulting LOSS8.

The solver's 3x3 geometry is not trusted. Fixed terminal strategies are
independently replayed using 4x4 Bareiss, and every parent->eight move is
rechecked by 4x4 geometry. This is NOT a six-stone or two-stone verdict.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path

import verify_five_terminal_loss7 as terminal
import verify_central49_post_seven_win6_repair_2301 as current

G = current.geometry
HERE = Path(__file__).resolve().parent

# New current-cover hits beyond the four roots recorded in K0642.
NEW_CURRENT_HITS = {
    "0000000000000020380a000000000040":
        "00000000000000203808000000000040",
    "00000000000002043800800000000010":
        "00000000000000203808000000000040",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def selected_s6():
    # First audit the entire current 2301 plan, not an old invalid worklist.
    manifest = json.loads(current.CERT.read_text(encoding="utf-8"))
    checked = current.verify(manifest)
    need(checked["distinct_s7"] == 2301 and
         checked["k0637_terminal_loss7_secured_classes"] == 4,
         "current 2301 plan was not independently validated")
    source = json.loads(current.repaired.CERT.read_text(encoding="utf-8"))
    selected = {current.base.decode(k) for k in source["selected_s6_classes"]}
    need(len(selected) == 46, "bad source selected S6 count")
    for row in current.historical.load_rows():
        removed = {current.base.decode(k) for k in row[:2]}
        added = {current.base.decode(k) for k in row[2:4]}
        need(len(removed) == len(added) == 2 and removed <= selected
             and not (added & selected), "historical swap changed")
        selected = (selected - removed) | added
    removed = {current.base.decode(k) for k in current.REMOVED}
    added = {current.base.decode(k) for k in current.ADDED}
    need(len(removed) == len(added) == 7 and removed <= selected
         and not (added & selected), "post-seven-WIN6 repair changed")
    selected = (selected - removed) | added
    need(len(selected) == 46, "current S6 count changed")
    return selected


def checked_parent_transition(parent, eight):
    need(parent.bit_count() == 7 and eight.bit_count() == 8
         and (parent & eight) == parent
         and (eight ^ parent).bit_count() == 1,
         "not a seven-to-eight single move")
    need(eight in G.children(parent),
         "seven-to-eight transition is not legal by independent 4x4 geometry")


def audit(folder):
    # SHA-256 pinned five fixed strategies, all branches and terminal leaves.
    verified = terminal.audit(folder)
    need(verified["total_reachable_states"] == 13293
         and verified["total_terminal_states"] == 1901,
         "fixed terminal certificate audit changed")
    roots = set(terminal.EXPECTED)
    need(len(roots) == 5, "five-root inventory changed")
    provenance = {}
    eight_roots = []
    for root in sorted(roots):
        data = (folder / ("n11_s7_" + root + ".cert")).read_bytes()
        strategy = terminal.parse(data, root)
        board = int(root, 16)
        first_move = strategy[board]
        need(not (board & (1 << first_move)),
             "winning first move is already occupied")
        eight = board | (1 << first_move)
        need(eight.bit_count() == 8 and eight in G.children(board),
             "certified first move is not legal by independent geometry")
        need(all(not G.forbidden(*quad)
                 for quad in combinations(G.points(eight), 4)),
             "resulting eight-stone board is not safe")
        eight_roots.append(f"{eight:032x}")
        for removed in G.points(eight):
            parent = eight ^ (1 << removed)
            checked_parent_transition(parent, eight)
            key = f"{G.canonical(parent):032x}"
            provenance.setdefault(key, []).append({
                "certified_loss7_root": root,
                "winning_first_move": first_move,
                "removed_point_from_loss8": removed,
            })

    need(len(provenance) == 23 and roots <= set(provenance),
         "seven-parent LOSS7 closure count or source changed")
    need(len(set(eight_roots)) == 4,
         "unexpected number of distinct eight-stone LOSS roots")
    selected = selected_s6()
    hits = {}
    for key in sorted(provenance):
        seven = int(key, 16)
        selected_parents = sorted({
            f"{G.canonical(seven ^ (1 << p)):032x}"
            for p in G.points(seven)
            if G.canonical(seven ^ (1 << p)) in selected
        })
        for sixkey in selected_parents:
            six = int(sixkey, 16)
            need(seven in {G.canonical(c) for c in G.children(six)},
                 "current six-stone witness cannot legally reach LOSS7")
        if selected_parents:
            hits[key] = selected_parents

    old_hits = {k for k in hits if k in roots}
    new_hits = {k for k in hits if k not in roots}
    need(len(hits) == 6 and len(old_hits) == 4 and len(new_hits) == 2
         and sum(map(len, hits.values())) == 6,
         "current 2301 cover intersection changed")
    need({k: hits[k][0] for k in new_hits} == NEW_CURRENT_HITS,
         "new current-cover LOSS7 classes changed")
    need(len({s for parents in hits.values() for s in parents}) == 3,
         "secured witness count changed")
    return {
        "schema": "n11-central49-five-terminal-loss7-eight-parent-lift-v1",
        "source_terminal_loss7_roots": len(roots),
        "distinct_certified_loss8_children": len(set(eight_roots)),
        "all_7_parent_edges_checked": sum(map(len, provenance.values())),
        "distinct_certified_loss7_by_parent_lift": len(provenance),
        "new_loss7_classes_from_lift": len(provenance) - len(roots),
        "current_conditional_s7_classes": 2301,
        "current_secured_loss7_classes": len(hits),
        "previously_secured_by_k0637": len(old_hits),
        "new_current_secured_loss7_classes": len(new_hits),
        "current_secured_s6_to_s7_edges": sum(map(len, hits.values())),
        "current_secured_s6_witnesses": len(
            {s for parents in hits.values() for s in parents}),
        "current_not_secured_by_this_lift": 2301 - len(hits),
        "new_current_hits": {k: hits[k] for k in sorted(new_hits)},
        "all_current_hits": hits,
        "new_current_provenance": {k: provenance[k] for k in sorted(new_hits)},
        "s6_outcome": "UNKNOWN",
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
        "evidence_limit": "Terminal-certified LOSS7 strategy first moves imply LOSS8; any safe seven-stone parent has a winning move to that LOSS8. No S6 LOSS is proved.",
    }


def negative_tests():
    root = int(next(iter(terminal.EXPECTED)), 16)
    p = next(i for i in range(121) if not (root >> i) & 1)
    eight = root | (1 << p)
    tests = [
        (root, root),               # no added point
        (root, eight | (1 << (p + 1))),  # more than one added point
    ]
    rejected = 0
    for parent, child in tests:
        try:
            checked_parent_transition(parent, child)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("malformed parent transition accepted")
    need(rejected == 2, "negative fixtures did not execute")
    return rejected


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("certificate_directory", type=Path)
    ap.add_argument("--negative", action="store_true")
    args = ap.parse_args()
    result = audit(args.certificate_directory)
    if args.negative:
        result["negative_tests"] = negative_tests()
    print(json.dumps(result, ensure_ascii=False, indent=2))
