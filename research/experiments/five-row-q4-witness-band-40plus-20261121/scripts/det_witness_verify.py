#!/usr/bin/env python3
"""Third independent verifier: maximality via 4x4 determinant degeneracy.

Independent of append_criterion.py (line/circle census with Fraction circle
coefficients) and of surgery.js (BigInt A*x+B*y+C+D*(x^2+y^2)==0 checks).

Method: a set T of 4 distinct cells violates (w,q=4) iff the points are
collinear or concyclic, i.e. iff the degenerate-concyclic condition holds:
    det [[x_i, y_i, x_i^2+y_i^2, 1]]_{i=1..4} == 0.
S safe iff no 4-subset of S is degenerate. S maximal at width m iff S safe
and every empty cell c of the w x m board has some 4-subset of S+{c}
degenerate. Pure integer arithmetic (Leibniz expansion).
Usage: det_witness_verify.py w m < stones.json ; exit 1 on failure.
"""
import json, sys
from itertools import combinations


def det4(rows):
    a = rows
    return (a[0][0] * (a[1][1] * (a[2][2] * a[3][3] - a[2][3] * a[3][2])
                     - a[1][2] * (a[2][1] * a[3][3] - a[2][3] * a[3][1])
                     + a[1][3] * (a[2][1] * a[3][2] - a[2][2] * a[3][1]))
          - a[0][1] * (a[1][0] * (a[2][2] * a[3][3] - a[2][3] * a[3][2])
                     - a[1][2] * (a[2][0] * a[3][3] - a[2][3] * a[3][0])
                     + a[1][3] * (a[2][0] * a[3][2] - a[2][2] * a[3][0]))
          + a[0][2] * (a[1][0] * (a[2][1] * a[3][3] - a[2][3] * a[3][1])
                     - a[1][1] * (a[2][0] * a[3][3] - a[2][3] * a[3][0])
                     + a[1][3] * (a[2][0] * a[3][1] - a[2][1] * a[3][0]))
          - a[0][3] * (a[1][0] * (a[2][1] * a[3][2] - a[2][2] * a[3][1])
                     - a[1][1] * (a[2][0] * a[3][2] - a[2][2] * a[3][0])
                     + a[1][2] * (a[2][0] * a[3][1] - a[2][1] * a[3][0])))


def deg(T):
    rows = [(x, y, x * x + y * y, 1) for x, y in T]
    return det4(rows) == 0


def main():
    w, m = map(int, sys.argv[1:3])
    S = [tuple(p) for p in json.load(sys.stdin)]
    n = len(S)
    assert len(set(S)) == n and all(0 <= x < m and 0 <= y < w for x, y in S)
    # safety: no degenerate 4-subset
    for T in combinations(S, 4):
        if deg(T):
            print("FAIL safe", T); sys.exit(1)
    # maximality: every empty cell blocked by some degenerate 4-subset with c
    empty = [(x, y) for y in range(w) for x in range(m) if (x, y) not in S]
    uncovered = []
    for c in empty:
        if not any(deg(list(T3) + [c]) for T3 in combinations(S, 3)):
            uncovered.append(list(c))
    if uncovered:
        print("FAIL maximal", uncovered); sys.exit(1)
    print(json.dumps({"w": w, "m": m, "n": n, "safe": True, "maximal_at_m": True,
                      "empty_cells": len(empty)}))


if __name__ == "__main__":
    main()
