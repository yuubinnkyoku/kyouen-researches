#!/usr/bin/env python3
"""Row-line blocking proposition checker (independent pure-Python Fraction).

Proposition (K0854). Let S be a finite stone set on rows 0..w-1, q >= 2,
S safe (no line/circle holds >= q stones). Then every row holds at most
q-1 stones (the row's horizontal line would otherwise be a violation).
For any row y with exactly r_y = q-1 stones, the horizontal line y passes
through all r_y stones, hence through any empty cell (x, y) it is a curve
containing exactly q-1 stones: every empty cell of that row is *blocked*.
Consequently the free-append stopping cell of K0853 (the first unblocked
cell right of max_x) always lies in a row with at most q-2 stones — for a
single-deficiency witness (rows q-2, q-1 x (w-1)) it lies in the unique
deficient row.

Machine audit performed per witness:
  (a) row census: max(rows) <= q-1 (safety corollary);
  (b) every empty cell of every (q-1)-stone row, over all scanned columns
      0..limit-1, is blocked (direct enumeration, exact Fractions);
  (c) every unblocked cell in the scanned window (not only the first) lies
      in a deficient row (r_y <= q-2);
  (d) first unblocked cell reported with its row's stone count.

Usage: rowline_check.py w scan_limit q < stones.json   (stones: [[x,y],...])
Output: one JSON line. Exit code 0 iff all checks pass.
"""
import json, sys, math
from fractions import Fraction


def canon_line(a, b):
    A, B, C = b[1] - a[1], a[0] - b[0], b[0] * a[1] - b[1] * a[0]
    g = math.gcd(math.gcd(abs(A), abs(B)), abs(C)) or 1
    return (A // g, B // g, C // g)


def circle_coeffs(p, r, s):
    """Circle through 3 non-collinear points as (D, E, F), x^2+y^2+Dx+Ey+F=0."""
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

    rows = [0] * w
    for x, y in S:
        rows[y] += 1
    deficient = [y for y in range(w) if rows[y] <= q - 2]
    full = [y for y in range(w) if rows[y] == q - 1]

    # (a) safety corollary
    row_cap_ok = max(rows) <= q - 1

    # (b) every empty cell of every (q-1)-stone row is blocked over the scan
    full_row_violations = []
    for x in range(limit):
        for y in full:
            c = (x, y)
            if c in S:
                continue
            if not blocked(c):
                full_row_violations.append(list(c))

    # (c)+(d) all unblocked cells in the scanned window lie in deficient rows
    unblocked = []
    for x in range(limit):
        for y in range(w):
            c = (x, y)
            if c in S:
                continue
            if not blocked(c):
                unblocked.append([x, y])
    stray = [c for c in unblocked if c[1] not in deficient]
    first = unblocked[0] if unblocked else None
    first_in_deficient = (first is None) or (first[1] in deficient)

    ok = safe and row_cap_ok and not full_row_violations and not stray and first_in_deficient
    out = {
        "n": n, "w": w, "q": q, "rows": rows,
        "safe": safe, "maxline": maxline, "maxcirc": maxcirc,
        "row_cap_ok": row_cap_ok,
        "deficient_rows": deficient, "full_rows": full,
        "full_row_violations": full_row_violations,
        "unblocked_in_window": unblocked,
        "stray_unblocked_outside_deficient": stray,
        "first_unblocked": first,
        "first_unblocked_row_stones": rows[first[1]] if first else None,
        "pass": ok,
        "scan_limit": limit,
    }
    print(json.dumps(out))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
