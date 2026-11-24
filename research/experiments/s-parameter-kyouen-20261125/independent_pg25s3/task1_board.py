#!/usr/bin/env python3
"""Task 1: verify that the board file describes PG(2,5).

Checks (all from scratch, standard library only):
  * header says 31 points, 31 lines
  * every line has exactly 6 distinct in-range points
  * every point 0..30 occurs in at least one line
  * every unordered pair of points lies on exactly one line
  * every unordered pair of lines meets in exactly one point (dual property)
  * every point lies on exactly 6 lines
  * no duplicate lines
"""
import json
import os
import sys
from collections import Counter
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.normpath(os.path.join(
    HERE, "..", "..", "projective-blocking-kyouen-20261125", "output", "board_pg2q5.txt"))
OUT = os.path.join(HERE, "out_task1.json")


def load_board(path):
    with open(path, "r", encoding="utf-8") as f:
        toks = f.read().split()
    it = iter(toks)
    n = int(next(it))
    b = int(next(it))
    lines = []
    for _ in range(b):
        k = int(next(it))
        pts = [int(next(it)) for _ in range(k)]
        lines.append(pts)
    # ensure the file has no trailing garbage
    trailing = list(it)
    if trailing:
        raise ValueError("trailing tokens in board file: %r" % (trailing,))
    return n, b, lines


def main():
    n, b, lines = load_board(BOARD)
    res = {
        "board_file": BOARD,
        "n": n,
        "b": b,
        "checks": {},
        "ok": True,
    }
    fails = []

    def chk(name, cond, detail=""):
        res["checks"][name] = {"pass": bool(cond), "detail": detail}
        if not cond:
            fails.append(name)

    chk("n_is_31", n == 31, "n=%d" % n)
    chk("b_is_31", b == 31, "b=%d" % b)

    # line sizes / ranges / duplicates
    sizes = Counter(len(L) for L in lines)
    chk("all_line_sizes_6", set(sizes) == {6}, "size histogram=%s" % dict(sizes))

    inrange = all(0 <= p < n for L in lines for p in L)
    chk("all_points_in_range", inrange)

    distinct_lines = len({tuple(sorted(L)) for L in lines})
    chk("no_duplicate_lines", distinct_lines == b, "distinct=%d/%d" % (distinct_lines, b))

    # each line must itself have distinct points
    dup_in_line = [i for i, L in enumerate(lines) if len(set(L)) != len(L)]
    chk("no_repeated_point_in_line", not dup_in_line, "bad lines=%s" % dup_in_line[:10])

    # every point occurs
    point_incidence = [0] * n
    for L in lines:
        for p in L:
            point_incidence[p] += 1
    all_points_used = all(c > 0 for c in point_incidence)
    chk("all_points_used", all_points_used,
        "min incidence=%d" % min(point_incidence) if point_incidence else "")
    chk("every_point_on_6_lines", all(c == 6 for c in point_incidence),
        "incidence histogram=%s" % dict(Counter(point_incidence)))

    # pair on exactly one line
    pair_counts = Counter()
    for L in lines:
        for a, bb in combinations(sorted(L), 2):
            pair_counts[(a, bb)] += 1
    npairs = n * (n - 1) // 2
    chk("all_pairs_covered", len(pair_counts) == npairs,
        "covered pairs=%d/%d" % (len(pair_counts), npairs))
    chk("every_pair_on_exactly_one_line",
        all(v == 1 for v in pair_counts.values()),
        "pair-multiplicity histogram=%s" % dict(Counter(pair_counts.values())))
    bad_pairs = [(k, v) for k, v in pair_counts.items() if v != 1]
    res["bad_pairs_sample"] = bad_pairs[:10]

    # line-line intersections
    line_masks = [sum(1 << p for p in L) for L in lines]
    inter = Counter()
    for i, j in combinations(range(b), 2):
        inter[(i, j)] = bin(line_masks[i] & line_masks[j]).count("1")
    chk("every_line_pair_meets_in_one_point",
        all(v == 1 for v in inter.values()),
        "intersection-size histogram=%s" % dict(Counter(inter.values())))

    # line size + v + pair-unique => 2-(31,6,1) design; order q = 5 plane.
    # order consistency: r = (v-1)/(k-1) = 30/5 = 6, lambda*(v-1) = k-1 -> 5 = 5.
    chk("design_parameters_2_31_6_1",
        n == 31 and set(sizes) == {6} and all(v == 1 for v in pair_counts.values()))

    res["ok"] = not fails
    res["failed_checks"] = fails
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(json.dumps({k: res[k] for k in ("n", "b", "ok", "failed_checks")}, indent=2))
    for name, c in res["checks"].items():
        print(("PASS" if c["pass"] else "FAIL"), name, "-", c["detail"])
    sys.exit(0 if res["ok"] else 1)


if __name__ == "__main__":
    main()
