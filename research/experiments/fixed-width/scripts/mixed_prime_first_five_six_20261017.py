#!/usr/bin/env python3
"""Independent finite audit for three columns x=0,4,13, rows y=6j.

Method 1: common-midpoint chord lengths (Diophantine equation).
Method 2: enumerate 3-column point triples, normalize exact circle equations.
No floating point or external packages.
"""
from collections import Counter
from functools import reduce
from math import gcd, isqrt

X = (0, 4, 13)
D = 6


def chord_solutions(max_diff):
    """All ordered nonnegative differences satisfying 9D0²-13D1²+4D2²=-52."""
    ans = []
    for t0 in range(max_diff + 1):
        for t1 in range(max_diff + 1):
            n = -52 - 9 * t0 * t0 + 13 * t1 * t1
            if n < 0 or n % 4:
                continue
            t2 = isqrt(n // 4)
            if t2 > max_diff or t2 * t2 != n // 4:
                continue
            if (t0 - t1) % 2 or (t1 - t2) % 2:
                continue
            if sum(t > 0 for t in (t0, t1, t2)) < 2:
                continue
            ans.append((t0, t1, t2))
    return ans


def five_span(t):
    """Minimum row-index span of five *distinct* points on this circle."""
    ds = sorted(t, reverse=True)
    if ds[2] == 0:
        return ds[0]  # the tangent point cannot be discarded
    return (ds[0] + ds[1]) // 2  # discard one end of longest chord


def det3(a, b, c):
    return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])


def circle_multiplicities(m):
    """Each 3-column circle has 1,2,4,8 transversal triples for 3,4,5,6 points."""
    counts = Counter()
    for j0 in range(m):
        x, y = X[0], D * j0
        r0 = x * x + y * y
        for j1 in range(m):
            u, v = X[1], D * j1
            r1 = u * u + v * v
            for j2 in range(m):
                w, z = X[2], D * j2
                r2 = w * w + z * z
                delta = det3((x, y, 1), (u, v, 1), (w, z, 1))
                if delta == 0:
                    continue
                aa = det3((-r0, y, 1), (-r1, v, 1), (-r2, z, 1))
                bb = det3((x, -r0, 1), (u, -r1, 1), (w, -r2, 1))
                cc = det3((x, y, -r0), (u, v, -r1), (w, z, -r2))
                div = reduce(gcd, (delta, aa, bb, cc))
                sgn = 1 if delta > 0 else -1
                key = tuple(sgn * t // div for t in (delta, aa, bb, cc))
                counts[key] += 1
    return counts


def audit():
    expected = {
        37: (0, 0, 50471, 2),
        38: (2, 0, 54674, 4),
        40: (6, 0, 63764, 4),
        41: (9, 1, 68658, 8),
    }
    for m, (five_count, six_count, circle_count, maximum) in expected.items():
        # All possible 5-point circles have max difference <= 2(m-1).
        ds = chord_solutions(2 * (m - 1))
        exists5 = any(five_span(t) <= m - 1 for t in ds)
        exists6 = any(all(t > 0 for t in s) and max(s) <= m - 1 for s in ds)
        circles = circle_multiplicities(m)
        n5 = sum(v >= 4 for v in circles.values())
        n6 = sum(v >= 8 for v in circles.values())
        assert (n5, n6, len(circles), max(circles.values())) == (five_count, six_count, circle_count, maximum)
        assert exists5 == (n5 > 0) and exists6 == (n6 > 0)
        print(f'm={m}: >=5-point circles={n5}, 6-point circles={n6}, distinct transversal circles={len(circles)}, max triple multiplicity={maximum}; methods agree')
        if m == 38:
            assert {k for k, v in circles.items() if v >= 4} == {
                (1, 995, -240, 0), (1, 995, -204, -3996)}
        if m == 41:
            assert {k for k, v in circles.items() if v >= 8} == {(1, 995, -240, 0)}
    witness = [(0, 0), (0, 240), (4, 18), (4, 222), (13, 84), (13, 156)]
    assert all(x*x+y*y+995*x-240*y == 0 for x, y in witness)
    print('EXACT: first five-point circle at 38 rows; first six-point circle at 41 rows.')
    print('Unique six-point circle in 41 rows: x²+y²+995x-240y=0.')


if __name__ == '__main__':
    audit()
