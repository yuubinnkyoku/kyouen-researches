#!/usr/bin/env python3
"""Lift one terminal-certified original-first WIN7 to all seven S6 parents.

A fixed original-first strategy for the shared seven-stone child was
independently checked by a 4x4 integer determinant. Every six-stone parent
can legally play its missing point and use the same child strategy, up to D4.
No historical solver verdict is used.
"""
import argparse
import hashlib
import json

import verify_s7_shared_frontier_46 as geometry
import verify_shared58_s6_win_strategy as source

EXPECTED = [
    "00000000000000083801800000000000",
    "00000000000000203808200000000000",
    "0000000000000020380c000000000000",
    "00000000000000403808200000000000",
    "00000000000000601808200000000000",
    "00000000000000602808200000000000",
    "00000000000000603008200000000000",
]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def transform(mask, row):
    return sum(1 << row[p] for p in source.points(mask))


def lift(base_strategy, raw_parent, point, canonical_parent):
    row = next((row for row in geometry.D4
                if transform(raw_parent, row) == canonical_parent), None)
    need(row is not None, "no D4 map to canonical parent")
    mapped_move = row[point]
    shared_child = source.ROOT | (1 << 70)
    need(raw_parent | (1 << point) == shared_child
         and transform(shared_child, row)
             == canonical_parent | (1 << mapped_move),
         "parent move does not reach certified shared S7")
    strategy = {canonical_parent: mapped_move}
    for mask, move in base_strategy.items():
        if mask == source.ROOT:
            continue
        transformed = transform(mask, row)
        need(transformed not in strategy, "strategy states collide")
        strategy[transformed] = row[move]
    need(len(strategy) == 10881, "incorrect lifted strategy size")
    return strategy, mapped_move


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    raw = source.CERT.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == source.EXPECTED_SHA256,
         "fixed terminal strategy hash changed")
    strategy = source.parse_certificate(raw.decode("utf-8"))
    source.replay(strategy)
    shared = source.ROOT | (1 << 70)
    need(geometry.canonical(shared) == shared
         and source.legal(source.ROOT) & (1 << 70),
         "shared seven-stone child not canonical or not legal")
    parent_rows = []
    for p in source.points(shared):
        raw_parent = shared ^ (1 << p)
        canonical_parent = geometry.canonical(raw_parent)
        lifted, first_move = lift(strategy, raw_parent, p, canonical_parent)
        proof = source.replay(lifted, canonical_parent, first_move)
        need(proof["strategy_nodes"] == 10881
             and proof["visited_states"] == 16980
             and proof["terminal_leaves"] == 2237,
             "independent terminal replay counts changed")
        parent_rows.append({
            "s6": f"{canonical_parent:032x}",
            "original_removed_point": p,
            "canonical_first_move": first_move,
            "terminal_leaves": proof["terminal_leaves"],
            "original_first_verdict": "WIN",
        })
    parent_rows.sort(key=lambda r: r["s6"])
    need([r["s6"] for r in parent_rows] == EXPECTED,
         "seven S6 parent classes changed or duplicate")
    need(source.ROOT_KEY in EXPECTED and source.DERIVED_ROOT_KEY in EXPECTED,
         "previously certified two WIN6 missing")
    if args.negative:
        # A forged first move is rejected by the same independent full-game
        # replay checker; no searcher-provided verdict is trusted.
        row = parent_rows[0]
        parent = int(row["s6"], 16)
        raw_parent = shared ^ (1 << row["original_removed_point"])
        lifted, move = lift(strategy, raw_parent,
                            row["original_removed_point"], parent)
        forged = dict(lifted)
        forged[parent] = (move + 1) % 121
        try:
            source.replay(forged, parent, move)
        except ValueError:
            pass
        else:
            raise AssertionError("forged WIN6 first move accepted")
    print(json.dumps({
        "schema": "n11-shared-terminal-win7-seven-s6-parents-v1",
        "terminal_source_sha256": source.EXPECTED_SHA256,
        "original_first_win6_classes": 7,
        "new_vs_previous_two": 5,
        "proof": "4x4-integer-determinant-full-terminal-strategy-replay",
        "parents": parent_rows,
        "negative_tests": 1 if args.negative else 0,
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
