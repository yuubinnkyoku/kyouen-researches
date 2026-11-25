#!/usr/bin/env python3
"""Independent point-pair line enumeration for high-q collinear subsets in boxes."""
from collections import defaultdict
from itertools import combinations, product
from math import comb, gcd, prod


def closed_form(shape, q):
    nmax = max(shape)
    if not (q >= 2 and 2 * (q - 1) > nmax - 1):
        raise ValueError('requires q>=2 and 2(q-1)>max(n_i)-1')
    return sum(comb(k - 2, q - 2) *
               (prod(n + 2 * max(0, n - k + 1) for n in shape) - prod(shape))
               for k in range(q, nmax + 1)) // 2


def independent_lines(shape, q):
    pts = list(product(*(range(n) for n in shape)))
    groups = defaultdict(set)
    for i, j in combinations(range(len(pts)), 2):
        a, b = pts[i], pts[j]
        delta = tuple(y - x for x, y in zip(a, b))
        g = 0
        for z in delta:
            g = gcd(g, abs(z))
        v = tuple(z // g for z in delta)
        if next(z for z in v if z) < 0:
            v = tuple(-z for z in v)
        origin = a
        while all(0 <= x - step < n for x, step, n in zip(origin, v, shape)):
            origin = tuple(x - step for x, step in zip(origin, v))
        groups[(v, origin)].update((i, j))
    return sum(comb(len(points), q) for points in groups.values()
               if len(points) >= q)


def main():
    checked = 0
    by_dimension = {}
    for d, upper in ((1, 10), (2, 7), (3, 4), (4, 3)):
        count = 0
        for shape in product(range(1, upper + 1), repeat=d):
            if prod(shape) > 90:
                continue
            for q in range(2, max(shape) + 2):
                if 2 * (q - 1) <= max(shape) - 1:
                    continue
                got = closed_form(shape, q)
                expected = independent_lines(shape, q)
                assert got == expected, (shape, q, got, expected)
                count += 1
        checked += count
        by_dimension[d] = count
    print('Exhaustive independent pair-line comparisons:', checked)
    print('by dimension:', by_dimension)
    for shape, q in [((2,3,4),3), ((3,3,3),3), ((4,4,4),4),
                     ((5,5,5),4), ((2,4,7),5), ((7,7),6)]:
        print(f'shape={shape}, q={q}, H={closed_form(shape,q)}')


if __name__ == '__main__':
    main()
