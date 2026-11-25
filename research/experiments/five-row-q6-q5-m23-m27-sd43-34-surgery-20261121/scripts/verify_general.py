#!/usr/bin/env python3
"""Census-free exact verifier for the kyouen (fixed-width w, q-point) game.

Checks that a stone set contains NO winning configuration among its stones,
i.e., verifies a "witness" (a configuration that avoids all kyouen triples of
among-stone count >= q). Independent reimplementation (Fraction arithmetic,
no shared code with the JS toolchain).

A winning set is q stones on a common circle within the rectangle [0,w)x[0,h).
We enumerate candidate circles through triples of stones (two-radius lemma:
any circle carrying >=3 stones of a candidate set passes through >= 3 triples).
So the witness condition is: every circle through any 3 stones of the set
carries at most q-1 stones of the set, and every horizontal/vertical line
(in 4-point line mode; lines are not circles but separate objects in this
variant only if the census includes them - we check circles AND lines when
the census does) carries at most q-1.

This verifier matches the census-4 convention used by surgery4.js: a "curve"
is a maximal set of grid points lying on a common Euclidean circle, together
with (in line mode) rows/columns treated as curves of infinite radius. The
published surgery4 mainline uses circle census `buildCensus4` including lines?
See summary: verifyConfig in sat.js is the ground truth; this script mirrors
its semantics: curves = circles through >= 2 points? To stay exact we check
ALL circles through every triple of stones (count >= q on it -> fail), and
ALL lines through pairs of stones (count >= q collinear -> fail) when lines
are winning sets as well (for q >= 4, 4 collinear points => circle through?
NO: collinear points are not concyclic on a proper circle). sat.js counts
lines as curves with infinite radius. So we do the same: any line (any
direction) through >= 2 stones carrying >= q stones => fail.

Usage: verify_general.py <w> <q> <seed.json>
Exit 0 + "PASS" if valid witness, 1 + "FAIL" otherwise.
"""
import json, sys
from fractions import Fraction

def load(st, w):
    xs = [p[0] for p in st]; ys = [p[1] for p in st]
    x0, y0 = min(xs), min(ys)
    return sorted([(x - x0, y - y0) for x, y in st]), max(xs) - x0 + 1, max(ys) - y0 + 1

def circle_center(a, b, c):
    """Center of circumscribed circle of 3 non-collinear points, Fractions."""
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if d == 0:
        return None, None  # collinear
    ux = Fraction(
        ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay)
         + (cx * cx + cy * cy) * (ay - by)), d)
    uy = Fraction(
        ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx)
         + (cx * cx + cy * cy) * (bx - ax)), d)
    return ux, uy

def count_on_circle(st, ux, uy, r2):
    pts = []
    for (x, y) in st:
        dx, dy = x - ux, y - uy
        if dx * dx + dy * dy == r2:
            pts.append((x, y))
    return len(pts)

def line_key(p0, p1):
    """Canonical line through 2 integer points: (a,b,c) for ax+by=c, gcd=1."""
    x0, y0 = p0; x1, y1 = p1
    a, b = y0 - y1, x1 - x0
    if a == 0 and b == 0:
        return None
    c = a * x0 + b * y0
    g = 0
    for v in (a, b, c):
        g = g or v
    import math
    g = math.gcd(math.gcd(abs(a), abs(b)), abs(c))
    if g == 0:
        g = 1
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return a, b, c

def main():
    w = int(sys.argv[1]); q = int(sys.argv[2])
    _d = json.load(open(sys.argv[3]))
    stones = [tuple(p) for p in (_d if isinstance(_d, list) else _d["stones"])]
    st, W, H = load(stones, w)
    n = len(st)
    # circles through triples
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                ux, uy = circle_center(st[i], st[j], st[k])
                if ux is None:
                    continue
                r2 = (st[i][0] - ux) ** 2 + (st[i][1] - uy) ** 2
                if count_on_circle(st, ux, uy, r2) >= q:
                    print("FAIL circle")
                    sys.exit(1)
    # lines through pairs (any direction), if >= q collinear stones -> fail
    seen = set()
    for i in range(n):
        for j in range(i + 1, n):
            L = line_key(st[i], st[j])
            if L is None or L in seen:
                continue
            seen.add(L)
            a, b, c = L
            cnt = sum(1 for (x, y) in st if a * x + b * y == c)
            if cnt >= q:
                print("FAIL line")
                sys.exit(1)
    print("PASS")
    sys.exit(0)

main()
