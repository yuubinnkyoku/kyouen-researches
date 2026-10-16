#!/usr/bin/env python3
"""Exact finite-board audit of prime-adic row restrictions (not a universal proof)."""
from collections import Counter
from itertools import combinations
from math import gcd


def circle_key(a, b, c):
    (x, y), (u, v), (s, t) = a, b, c
    dx, dy, ex, ey = u-x, v-y, s-x, t-y
    den = dx*ey-ex*dy
    if den == 0:
        return None
    z1 = u*u+v*v-x*x-y*y
    z2 = s*s+t*t-x*x-y*y
    A = -(z1*ey-z2*dy)
    B = -(dx*z2-ex*z1)
    C = -(den*(x*x+y*y)+A*x+B*y)
    div = gcd(gcd(abs(den), abs(A)), gcd(abs(B), abs(C)))
    sign = 1 if den > 0 else -1
    return tuple(sign*z//div for z in (den, A, B, C))


def check_case(h, d, w, m, p, k):
    assert k >= 1 and h % p**k == 0 and d % p != 0
    points = [(h*j, d*i) for i in range(w) for j in range(m)]
    circles = set()
    for a, b, c in combinations(points, 3):
        key = circle_key(a, b, c)
        if key is not None:
            circles.add(key)
    max_pts = 0
    max_double_rows = 0
    q = p**(2*k)
    tbound = max((w+p-1)//p, 2*(w//q)+min(2, w%q))
    for A, B, C, D in circles:
        hits = [(x, y) for x, y in points if A*(x*x+y*y)+B*x+C*y+D == 0]
        max_pts = max(max_pts, len(hits))
        counts = Counter(y//d for x, y in hits)
        if max(counts.values()) < 2:
            continue
        rows = sorted(counts)
        max_double_rows = max(max_double_rows, len(rows))
        residues = {i % p for i in rows}
        if len(residues) != 1:
            assert len(residues) == 2, (h, d, w, m, rows, residues)
            assert len({i % q for i in rows}) <= 2, (h, d, w, m, rows, q)
        assert len(rows) <= tbound, (h, d, w, m, rows, tbound)
        assert len(hits) <= 2*tbound, (h, d, w, m, hits, tbound)
    assert max_pts <= max(w, 2*tbound), (h, d, w, m, max_pts, tbound)
    if w in (3, 4):
        assert max_pts == 4, (h, d, w, m, max_pts)
    print(f'h={h:2} d={d} p={p} k={k} w={w:2} m={m} '
          f'circles={len(circles):6} max_points={max_pts} '
          f'max_occupied_double_rows={max_double_rows} t_bound={tbound}')
    return len(circles)


def main():
    cases = [
        (3, 1, 3, 6, 3, 1), (3, 1, 4, 6, 3, 1),
        (3, 1, 5, 7, 3, 1), (3, 1, 6, 7, 3, 1),
        (3, 1, 7, 7, 3, 1), (3, 1, 10, 6, 3, 1),
        (5, 1, 3, 6, 5, 1), (5, 1, 4, 6, 5, 1),
        (5, 1, 10, 6, 5, 1), (7, 2, 12, 5, 7, 1),
        (9, 1, 3, 6, 3, 2), (9, 1, 4, 6, 3, 2),
        (9, 1, 10, 6, 3, 2), (25, 2, 11, 5, 5, 2),
    ]
    n = sum(check_case(*args) for args in cases)
    print(f'PASS: {len(cases)} finite boards, {n} exact distinct circles')


if __name__ == '__main__':
    main()
