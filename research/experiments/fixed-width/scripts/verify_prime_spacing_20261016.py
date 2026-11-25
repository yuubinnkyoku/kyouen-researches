#!/usr/bin/env python3
"""Exact finite-board audit of the prime-spacing circle bound.

Every circle containing >=3 grid points is determined by a noncollinear triple.
All calculations use integers. This is a finite audit, not the universal proof.
"""
from itertools import combinations
from math import gcd


def circle_key(a, b, c):
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c
    dx2, dy2 = x2 - x1, y2 - y1
    dx3, dy3 = x3 - x1, y3 - y1
    den = dx2 * dy3 - dx3 * dy2
    if not den:
        return None
    z2 = x2 * x2 + y2 * y2 - x1 * x1 - y1 * y1
    z3 = x3 * x3 + y3 * y3 - x1 * x1 - y1 * y1
    # den*(x^2+y^2)+A*x+B*y+C=0
    aa = -(z2 * dy3 - z3 * dy2)
    bb = -(dx2 * z3 - dx3 * z2)
    cc = -(den * (x1 * x1 + y1 * y1) + aa * x1 + bb * y1)
    g = gcd(gcd(abs(den), abs(aa)), gcd(abs(bb), abs(cc)))
    s = 1 if den > 0 else -1
    return tuple(s * v // g for v in (den, aa, bb, cc))


def audit(h, d, w, m, p):
    points = [(h * j, d * i) for i in range(w) for j in range(m)]
    circles = {}
    for i, j, k in combinations(range(len(points)), 3):
        key = circle_key(points[i], points[j], points[k])
        if key is not None:
            circles[key] = circles.get(key, 0) | (1 << i) | (1 << j) | (1 << k)
    assert w >= 4
    bound = w
    best = max((mask.bit_count() for mask in circles.values()), default=2)
    assert best <= bound, (h, d, w, m, p, best, bound)
    # Independent geometric check: one class modulo p, or two classes modulo p^2.
    for mask in circles.values():
        rows = [i for i in range(w) if (mask >> (i * m) & ((1 << m) - 1))]
        if any((mask >> (i * m) & ((1 << m) - 1)).bit_count() >= 2 for i in rows):
            classes = {i % p for i in rows}
            assert len(classes) <= 2, (h, d, w, m, p, rows)
            if len(classes) == 2:
                assert len({i % (p*p) for i in rows}) <= 2, (h, d, w, m, p, rows)
    return len(circles), best, bound


def main():
    cases = [(3, 1, 3), (7, 1, 7), (14, 1, 7), (7, 2, 7), (5, 1, 5),
             (10, 1, 5), (5, 2, 5), (11, 1, 11), (22, 3, 11)]
    count = 0
    for h, d, p in cases:
        for w in (4, 5, 6, 7, 8, 9):
            if h == 22 and w > 7:
                continue
            n, best, bound = audit(h, d, w, 6, p)
            count += 1
            print(f'h={h} d={d} p={p} w={w} m=6 circles={n} max={best} bound={bound}')
    for h, d, w, m, p in ((3, 1, 12, 10, 3), (5, 1, 7, 16, 5), (7, 1, 9, 16, 7), (7, 3, 12, 14, 7)):
        n, best, bound = audit(h, d, w, m, p)
        count += 1
        print(f'h={h} d={d} p={p} w={w} m={m} circles={n} max={best} bound={bound}')
    print(f'PASS: {count} finite boards; exact triple enumeration and residue audit')


if __name__ == '__main__':
    main()
