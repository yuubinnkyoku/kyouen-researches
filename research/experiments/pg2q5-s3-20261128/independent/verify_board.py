#!/usr/bin/env python3
"""Independent structural verification of board_pg2q5.txt.

Checks that the incidence structure is a projective plane of order 5:
  * 31 points, 31 lines, every line has exactly 6 distinct points
  * every point lies on exactly 6 lines
  * every unordered pair of distinct points lies on exactly one line
  * every two distinct lines meet in exactly one point
  * all lines are distinct

Writes a JSON summary to out/board_check.json.
"""
import itertools
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.abspath(os.path.join(
    HERE, "..", "..", "projective-blocking-kyouen-20261125",
    "output", "board_pg2q5.txt"))


def parse_board(path):
    with open(path, encoding="utf-8") as f:
        tokens = f.read().split()
    it = iter(tokens)
    n = int(next(it))
    b = int(next(it))
    lines = []
    for _ in range(b):
        ln = int(next(it))
        pts = [int(next(it)) for _ in range(ln)]
        lines.append(pts)
    rest = list(it)
    return n, b, lines, rest


def main():
    n, b, lines, rest = parse_board(BOARD)
    res = {"board_path": BOARD, "n_header": n, "b_header": b,
           "trailing_tokens": rest}
    errors = []

    if rest:
        errors.append(f"trailing tokens after last line: {rest[:10]}")
    if n != 31 or b != 31:
        errors.append(f"header says {n} points, {b} lines; expected 31,31")
    if len(lines) != b:
        errors.append(f"parsed {len(lines)} lines, header says {b}")

    lens = Counter(len(L) for L in lines)
    res["line_length_histogram"] = dict(lens)
    if set(lens) != {6}:
        errors.append(f"not all lines have 6 points: {dict(lens)}")

    flat = [p for L in lines for p in L]
    bad = [p for p in flat if not (0 <= p < n)]
    if bad:
        errors.append(f"point indices out of range: {bad[:10]}")
    if set(flat) != set(range(n)):
        missing = sorted(set(range(n)) - set(flat))
        errors.append(f"points not on any line: {missing}")
    # every line must have distinct points
    for i, L in enumerate(lines):
        if len(set(L)) != len(L):
            errors.append(f"line {i} repeats a point: {L}")

    line_sets = [frozenset(L) for L in lines]
    res["distinct_lines"] = len(set(line_sets))
    if len(set(line_sets)) != b:
        errors.append(f"only {len(set(line_sets))} distinct lines of {b}")

    # point degrees
    deg = [0] * n
    for L in lines:
        for p in L:
            deg[p] += 1
    res["point_degree_histogram"] = dict(Counter(deg))
    if set(deg) != {6}:
        errors.append(f"point degrees not all 6: {dict(Counter(deg))}")

    # pair coverage: every unordered pair exactly once
    pair_count = Counter()
    for L in line_sets:
        for p, q in itertools.combinations(sorted(L), 2):
            pair_count[(p, q)] += 1
    total_pairs = n * (n - 1) // 2
    res["distinct_pairs_covered"] = len(pair_count)
    res["total_pairs_expected"] = total_pairs
    if len(pair_count) != total_pairs:
        errors.append(
            f"pair coverage {len(pair_count)} of {total_pairs}")
    over = [(k, v) for k, v in pair_count.items() if v != 1]
    res["pairs_with_wrong_multiplicity"] = len(over)
    if over:
        errors.append(f"{len(over)} pairs covered != once; examples {over[:5]}")

    # line intersections
    inter_hist = Counter()
    for i, j in itertools.combinations(range(b), 2):
        inter_hist[len(line_sets[i] & line_sets[j])] += 1
    res["line_intersection_histogram"] = dict(inter_hist)
    if set(inter_hist) != {1}:
        errors.append(f"line intersections not all 1: {dict(inter_hist)}")

    # consistency of design parameters
    res["incidences"] = sum(len(L) for L in lines)
    res["v_minus_1_over_k_minus_1"] = (n - 1) // (6 - 1)
    res["expected_lines"] = n * (n - 1) // (6 * 5)
    res["is_projective_plane_order_5"] = (not errors)
    res["errors"] = errors

    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "board_check.json"), "w",
              encoding="utf-8") as f:
        json.dump(res, f, indent=1, sort_keys=True)

    print(json.dumps(res, indent=1, sort_keys=True))
    if errors:
        print("\nBOARD CHECK: FAIL")
        return 1
    print("\nBOARD CHECK: PASS (2-(31,6,1) design = PG(2,5), unique for q=5)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
