#!/usr/bin/env python3
"""Independent exact-Fraction verifier for a (w x m, q) witness candidate.

Fresh implementation (no repo code): safety = no integer line or circle
carrying >= q stones of S; maximality = every empty board cell lies on some
line or circle carrying >= q-1 stones of S. Lines: Ax+By+C=0 integer
primitive through stone pairs. Circles: exact circumcenter of stone triples.
"""
import json, sys
from fractions import Fraction
from math import gcd


def primitive_line(a, b):
    A, B = b[1] - a[1], a[0] - b[0]
    C = -(A * a[0] + B * a[1])
    if A < 0 or (A == 0 and B < 0):
        A, B, C = -A, -B, -C
    g = gcd(gcd(abs(A), abs(B)), abs(C)) or 1
    return (A // g, B // g, C // g)


def circumcenter(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if d == 0:
        return None
    a2, b2, c2 = ax * ax + ay * ay, bx * bx + by * by, cx * cx + cy * cy
    return (Fraction(a2 * (by - cy) + b2 * (cy - ay) + c2 * (ay - by), d),
            Fraction(a2 * (cx - bx) + b2 * (ax - cx) + c2 * (bx - ax), d))


def verify(w, m, q, stones):
    S = set(stones)
    board = [(x, y) for x in range(m) for y in range(w)]
    assert len(S) == len(stones) and all(p in set(board) for p in S)
    curves = {}
    n = len(stones)
    for i in range(n):
        for j in range(i + 1, n):
            curves.setdefault(("L",) + primitive_line(stones[i], stones[j]), set())
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                a, b, c = stones[i], stones[j], stones[k]
                if (b[0] - a[0]) * (c[1] - a[1]) == (b[1] - a[1]) * (c[0] - a[0]):
                    continue
                u = circumcenter(a, b, c)
                r2 = (Fraction(a[0]) - u[0]) ** 2 + (Fraction(a[1]) - u[1]) ** 2
                curves.setdefault(("C", u[0], u[1], r2), set())
    tab = []
    for key in curves:
        st_on = set()
        full = []
        for (x, y) in board:
            if key[0] == "L":
                on = key[1] * x + key[2] * y + key[3] == 0
            else:
                _, ux, uy, r2 = key
                on = (Fraction(x) - ux) ** 2 + (Fraction(y) - uy) ** 2 == r2
            if on:
                full.append((x, y))
                if (x, y) in S:
                    st_on.add((x, y))
        if len(st_on) >= 3:
            tab.append((key, st_on, frozenset(full)))
    maxc = max(len(st) for _, st, _ in tab)
    assert maxc <= q - 1, f"UNSAFE: curve with {maxc} stones"
    unblocked = []
    for e in board:
        if e in S:
            continue
        blocked = any(e in full and len(st) >= q - 1 for _, st, full in tab)
        if not blocked:
            unblocked.append(e)
    rows = [sum(1 for x in range(m) if (x, y) in S) for y in range(w)]
    return {"safe": True, "max_curve_stones": maxc, "rows": rows,
            "size": len(S), "maximal": not unblocked,
            "unblocked": [list(e) for e in unblocked]}


def main():
    w, m, q = map(int, sys.argv[1:4])
    raw = json.load(open(sys.argv[4]))
    if isinstance(raw, dict):
        raw = raw["stones"]
    stones = [tuple(p) for p in raw]
    res = verify(w, m, q, stones)
    print(json.dumps(res, indent=1))
    sys.exit(0 if res["maximal"] else 1)


if __name__ == "__main__":
    main()
