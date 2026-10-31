#!/usr/bin/env python3
"""Independent exact checks for the m-by-n circle-incidence construction."""
from collections import Counter
from itertools import combinations
from math import comb

# Point order: O, rows, columns, and row-major private points.
WITNESS = [
    (0, 0), (8, -4), (2, -6), (-4, 4), (6, -2), (-2, 2),
    (-8, 24), (-6, -18), (8, 32), (2, -8), (-1, -2), (-14, -14),
]


def edges(m, n):
    return [tuple((0, 1 + i, 1 + m + j, 1 + m + n + i * n + j))
            for i in range(m) for j in range(n)]


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def is_forbidden_quad(quad):
    # A lifted determinant vanishes exactly for four concyclic or collinear points.
    x, y = quad[0]
    z = x*x + y*y
    rows = [(u-x, v-y, u*u + v*v-z) for u, v in quad[1:]]
    return det3(*rows) == 0


def formula(m, n):
    N = (m+1)*(n+1)
    out = Counter({N-1: 1})
    out[N-m] += 1
    out[N-n] += 1
    for a in range(m):
        for b in range(n):
            k = a + b + (m-a)*(n-b)
            out[N-k] += comb(m, a)*comb(n, b)
    return out


def enumerate_maximal(m, n):
    N = (m+1)*(n+1)
    edge_masks = [sum(1 << i for i in edge) for edge in edges(m, n)]
    out = Counter()
    safe_count = 0
    for mask in range(1 << N):
        if any(mask & e == e for e in edge_masks):
            continue
        safe_count += 1
        if all(any(((mask | (1 << i)) & e) == e for e in edge_masks)
               for i in range(N) if not mask & (1 << i)):
            out[mask.bit_count()] += 1
    return out, safe_count


def main():
    # Exact geometric audit, independent of the abstract incidence model.
    actual = {idx for idx in combinations(range(12), 4)
              if is_forbidden_quad([WITNESS[i] for i in idx])}
    expected = {tuple(sorted(edge)) for edge in edges(2, 3)}
    assert len(actual) == 6 and actual == expected, (actual, expected)
    print('geometry: 495 four-point subsets, exactly six intended forbidden sets')

    for m, n in ((2, 2), (2, 3), (2, 4), (3, 3)):
        brute, safe = enumerate_maximal(m, n)
        predicted = formula(m, n)
        assert brute == predicted, (m, n, brute, predicted)
        print(f'{m}x{n}: {safe} safe positions; maximal polynomial {dict(sorted(brute.items()))}')
        if (m, n) == (2, 3):
            assert safe == 3117
            assert brute == Counter({6:1, 7:3, 8:17, 9:1, 10:1, 11:1})
    print('all checks passed')


if __name__ == '__main__':
    main()
