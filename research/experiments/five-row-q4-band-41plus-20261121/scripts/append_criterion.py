#!/usr/bin/env python3
"""Free-column append criterion checker (independent pure-Python Fraction implementation).

Lemma (K0853). Let S be a finite stone set with rows in 0..w-1, q >= 2.
(1) Safety is width-independent: S safe (no line/circle holds >= q stones)
    implies the same set is safe on any board width m' > max_x(S).
(2) Call an empty cell c *blocked* iff some line or circle through c holds
    >= q-1 stones of S (== exactly q-1 when S is safe). Blocking depends only
    on (S, c), not on the board width. Hence, with S maximal at width m0,
    S stays safe+maximal at every width m0 <= m' <= R(S), where R(S) is the
    free-append reach: the first column > max_x(S) containing an unblocked
    cell (R = infinity if none). For m' > R(S) the set is not maximal.
Row deficiency is invariant, so a row-deficient maximal witness at m0 is a
row-deficient maximal witness at every width in [m0, R(S)].

Method note: a blocking line through c must contain a stone, so it is the
line (c, s) for some s in S. A blocking circle through c with >= q-1 stones
contains 3 non-collinear stones of S, so it is the circle of some stone
triple. Both candidate families are enumerated exactly; counting is exact
Fraction arithmetic (no floating point).

Usage: append_criterion.py w scan_limit q < stones.json
  stones.json: [[x,y], ...]
Output: one JSON line with safety census, old-column coverage, free-append
  reach, and the first unblocked cell (the m'+1 frontier stop).
"""
import json, sys, math
from fractions import Fraction


def canon_line(a, b):
    A, B, C = b[1] - a[1], a[0] - b[0], b[0] * a[1] - b[1] * a[0]
    g = math.gcd(math.gcd(abs(A), abs(B)), abs(C)) or 1
    return (A // g, B // g, C // g)


def circle_coeffs(p, r, s):
    """Circle through 3 non-collinear points as (D, E, F), x^2+y^2+Dx+Ey+F=0.

    Linear system (subtract the first equation to eliminate F):
      D*(x2-x1) + E*(y2-y1) = -(f2 - f1)
      D*(x3-x1) + E*(y3-y1) = -(f3 - f1)
    NOTE: the right-hand side has NO /2. The /2 of the perpendicular-bisector
    midpoint form cancels against the center a=-D/2, b=-E/2. An earlier draft
    of this checker used -(f2-f1)/2 and was wrong (caught by cross-checking
    verify_witness.py on cell (40,0) of the (6,4) m=46 witness).
    """
    x1, y1 = p; x2, y2 = r; x3, y3 = s
    a11, a12 = x2 - x1, y2 - y1
    a21, a22 = x3 - x1, y3 - y1
    det = a11 * a22 - a12 * a21
    if det == 0:
        return None
    f = lambda x, y: x * x + y * y
    b1 = Fraction(-(f(x2, y2) - f(x1, y1)))
    b2 = Fraction(-(f(x3, y3) - f(x1, y1)))
    D = (b1 * a22 - b2 * a12) / det
    E = (a11 * b2 - a21 * b1) / det
    F = -D * x1 - E * y1 - Fraction(f(x1, y1))
    return (D, E, F)


def main():
    w, limit, q = map(int, sys.argv[1:4])
    S = [tuple(p) for p in json.load(sys.stdin)]
    n = len(S)
    assert len(set(S)) == n
    assert all(0 <= y < w for x, y in S)
    maxx = max(x for x, y in S)

    # --- safety census (width-independent) ---
    lines = set()
    for i in range(n):
        for j in range(i + 1, n):
            lines.add(canon_line(S[i], S[j]))
    circles = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                co = circle_coeffs(S[i], S[j], S[k])
                if co is not None:
                    circles.add(co)

    def line_cnt(key):
        return sum(1 for p in S if key[0] * p[0] + key[1] * p[1] + key[2] == 0)

    def circ_cnt(co):
        D, E, F = co
        return sum(1 for p in S if p[0] * p[0] + p[1] * p[1] + D * p[0] + E * p[1] + F == 0)

    maxline = max((line_cnt(k) for k in lines), default=0)
    maxcirc = max((circ_cnt(c) for c in circles), default=0)
    safe = maxline < q and maxcirc < q

    def blocked(c):
        if safe:
            thr = q - 1  # == exact count under safety
        else:
            thr = q - 1
        for s in S:
            key = canon_line(c, s)
            if line_cnt(key) >= thr:
                return True
        for co in circles:
            D, E, F = co
            x, y = c
            if x * x + y * y + D * x + E * y + F == 0 and circ_cnt(co) >= thr:
                return True
        return False

    # --- old-column coverage (columns 0..maxx) ---
    old_uncovered = []
    for x in range(0, maxx + 1):
        for y in range(w):
            c = (x, y)
            if c in S:
                continue
            if not blocked(c):
                old_uncovered.append(list(c))

    # --- free-append reach: first column > maxx with an unblocked cell ---
    reach = maxx
    first_unblocked = None
    col = maxx + 1
    while col < limit:
        ok = True
        for y in range(w):
            if not blocked((col, y)):
                ok = False
                first_unblocked = [col, y]
                break
        if not ok:
            reach = col
            break
        reach = col + 1
        col += 1

    rows = [0] * w
    for x, y in S:
        rows[y] += 1
    out = {
        "n": n, "w": w, "q": q, "rows": rows, "min_row": min(rows),
        "safe": safe, "maxline": maxline, "maxcirc": maxcirc,
        "maxx": maxx,
        "old_uncovered_count": len(old_uncovered),
        "free_append_reach": reach,
        "first_unblocked": first_unblocked,
        "witness_widths": [maxx + 1, reach] if (safe and not old_uncovered) else [],
        "scan_limit": limit,
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
