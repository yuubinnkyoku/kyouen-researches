#!/usr/bin/env python3
"""General-q witness verifier via pure determinant zero tests (third system).

Independent of append_criterion.py (Fraction circle coefficients (D,E,F))
and of surgery_gen.js (canonical integer curve keys A,B,C,D).  This verifier
never forms a curve equation: every membership test is a determinant
vanishing test on point matrices only.

Facts used (standard, integer-exact):
  - 3 points a,b,c are collinear iff det[[x_i,y_i,1]] = 0 (3x3 integer det).
  - 4 points are collinear or concyclic iff
    det[[x_i,y_i,x_i^2+y_i^2,1]] = 0 (4x4 integer det, Leibniz).
  - For a fixed non-collinear triple (a,b,c), a stone s lies on the unique
    circle through a,b,c iff det4(a,b,c,s)=0; for a fixed pair (a,b) a stone
    s lies on line(a,b) iff det3(a,b,s)=0.

Witness conditions on the w x m board (columns 0..m-1, rows 0..w-1), points
are integer lattice cells, q >= 4:
  safety : no line and no circle contains >= q stones.
           Every line with >= q stones contains a stone pair (counted through
           det3); every circle with >= q stones that are not all collinear
           contains a non-collinear stone triple (counted through det4).
           (If >= q stones are all collinear the pair pass already finds the
           line, so the circle pass may skip collinear triples safely.)
  maximality at width m : every empty cell c is blocked: some stone s with
           det3(c,s,t)==0 for >= q-1 stones t, i.e. the line (c,s) holds
           >= q-1 stones, or some stone pair (s1,s2), non-collinear with c,
           has the circle (c,s1,s2) holding >= q-1 stones (det4 counts).
  row deficiency : every row <= q-1 stones, some row <= q-2 stones.

Usage: det_q_verify.py w m q < stones.json  ; exit 1 on failure.
Deterministic, stdlib only.  Chosen as the third verification system for the
six-row band surgery lane (adapted from det_witness_verify.py q=4 of the
five-row-q4-witness-band-40plus-20261121 lane, generalized to any q with
pair/triple enumeration instead of 4-subset enumeration).
"""
import json, sys
from itertools import combinations


def det3(a, b, c):
    return (a[0] * (b[1] - c[1]) - b[0] * (a[1] - c[1]) + c[0] * (a[1] - b[1]))


def det4(a, b, c, d):
    rows = [(x, y, x * x + y * y) for x, y in (a, b, c, d)]
    m = [list(r) + [1] for r in rows]
    return (m[0][0] * (m[1][1] * (m[2][2] * m[3][3] - m[2][3] * m[3][2])
                       - m[1][2] * (m[2][1] * m[3][3] - m[2][3] * m[3][1])
                       + m[1][3] * (m[2][1] * m[3][2] - m[2][2] * m[3][1]))
          - m[0][1] * (m[1][0] * (m[2][2] * m[3][3] - m[2][3] * m[3][2])
                       - m[1][2] * (m[2][0] * m[3][3] - m[2][3] * m[3][0])
                       + m[1][3] * (m[2][0] * m[3][2] - m[2][2] * m[3][0]))
          + m[0][2] * (m[1][0] * (m[2][1] * m[3][3] - m[2][3] * m[3][1])
                       - m[1][1] * (m[2][0] * m[3][3] - m[2][3] * m[3][0])
                       + m[1][3] * (m[2][0] * m[3][1] - m[2][1] * m[3][0]))
          - m[0][3] * (m[1][0] * (m[2][1] * m[3][2] - m[2][2] * m[3][1])
                       - m[1][1] * (m[2][0] * m[3][2] - m[2][2] * m[3][0])
                       + m[1][2] * (m[2][0] * m[3][1] - m[2][1] * m[3][0])))


def main():
    w, m, q = map(int, sys.argv[1:4])
    S = [tuple(p) for p in json.load(sys.stdin)]
    n = len(S)
    assert len(set(S)) == n and all(0 <= x < m and 0 <= y < w for x, y in S)
    rows = [0] * w
    for x, y in S:
        rows[y] += 1
    # row caps
    assert all(r <= q - 1 for r in rows), ("FAIL rowcap", rows)
    assert any(r <= q - 2 for r in rows), ("FAIL nodef", rows)
    # safety via det membership counts
    maxline = 0
    for a, b in combinations(S, 2):
        # true stone count on the line through a,b: a, b and all collinear
        # others (the 2026-11-21 pre-publication audit found the draft wrote
        # 1 + others == k-1, which misses a line holding exactly q stones;
        # fixed to 2 + others == k before any publication; see README).
        cnt = 2 + sum(1 for s in S if s != a and s != b and det3(a, b, s) == 0)
        if cnt > maxline:
            maxline = cnt
    if maxline >= q:
        print("FAIL safe line", maxline); sys.exit(1)
    maxcirc = 0
    for a, b, c in combinations(S, 3):
        if det3(a, b, c) == 0:
            continue  # collinear triple: cannot define a circle the safe way
        cnt = 3 + sum(1 for s in S if s not in (a, b, c) and det4(a, b, c, s) == 0)
        if cnt > maxcirc:
            maxcirc = cnt
    if maxcirc >= q:
        print("FAIL safe circle", maxcirc); sys.exit(1)
    # maximality: every empty cell blocked by det3/det4 counts
    empty = [(x, y) for y in range(w) for x in range(m) if (x, y) not in S]
    uncovered = []
    for c in empty:
        blocked = False
        # line through c and stone s (det3 membership count among S)
        for s in S:
            cnt = sum(1 for t in S if det3(c, s, t) == 0)
            if cnt >= q - 1:
                blocked = True
                break
        if not blocked:
            # circle through c, s1, s2 (det4 membership count among S)
            for s1, s2 in combinations(S, 2):
                if det3(c, s1, s2) == 0:
                    continue
                cnt = 2 + sum(1 for t in S if t not in (s1, s2) and det4(c, s1, s2, t) == 0)
                if cnt >= q - 1:
                    blocked = True
                    break
        if not blocked:
            uncovered.append(list(c))
    if uncovered:
        print("FAIL maximal", uncovered[:20], "count", len(uncovered)); sys.exit(1)
    print(json.dumps({"w": w, "m": m, "q": q, "n": n, "rows": rows,
                      "maxline": maxline, "maxcirc": maxcirc,
                      "safe": True, "maximal_at_m": True,
                      "empty_cells": len(empty), "det_system": "det3/det4 zeros"}))


if __name__ == "__main__":
    main()
