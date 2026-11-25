#!/usr/bin/env python3
"""Exact all-safe census using layerwise normalized segment directions.
Independent implementation: independent.cpp uses integer 3x3 determinants.
"""
from collections import Counter, defaultdict
from itertools import combinations
from math import gcd

EXPECTED = {
    (1, 1): ([1, 2, 1, 0, 0, 0, 0], [0]*7, (0, 1)),
    (1, 2): ([1, 4, 6, 4, 0, 0, 0], [0]*7, (1, 0)),
    (1, 3): ([1, 6, 15, 20, 0, 0, 0], [0]*7, (1, 0)),
    (1, 4): ([1, 8, 28, 56, 0, 0, 0], [0]*7, (1, 0)),
    (2, 2): ([1, 8, 28, 56, 58, 8, 0], [1, 8, 16, 0, 0, 0, 0], (0, 0)),
    (2, 3): ([1, 12, 66, 220, 386, 172, 0], [0]*7, (1, 0)),
    (2, 4): ([1, 16, 120, 560, 1364, 1008, 0], [0]*7, (1, 0)),
    (3, 3): ([1, 18, 153, 816, 2436, 2664, 368], [0, 10, 25, 16, 0, 0, 0], (1, 0)),
    (3, 4): ([1, 24, 276, 2024, 8500, 15056, 5648], [0, 0, 8, 12, 0, 0, 0], (0, 1)),
    (3, 5): ([1, 30, 435, 4060, 21840, 52680, 31800], [0]*7, (0, 1)),
    (3, 6): ([1, 36, 630, 7140, 46854, 143652, 123200], [0]*7, (0, 1)),
    (4, 4): ([1, 32, 496, 4960, 29172, 80736, 64696], [0]*7, (0, 1)),
    (4, 5): ([1, 40, 780, 9880, 74496, 278760, 343080], [0]*7, (0, 1)),
}

def direction(a, b):
    dy, dz = b[0]-a[0], b[1]-a[1]
    d = gcd(abs(dy), abs(dz))
    dy, dz = dy//d, dz//d
    return (dy, dz) if dy > 0 or (dy == 0 and dz > 0) else (-dy, -dz)

def audit(k, m):
    n = k*m
    points = [(i//m, i%m) for i in range(n)]
    options = defaultdict(list)
    for size in range(4):
        for indices in combinations(range(n), size):
            dirs = [direction(points[a], points[b]) for a, b in combinations(indices, 2)]
            # A collinear triple is safe alone but cannot coexist with the other layer.
            shape = None if size == 3 and len(set(dirs)) != 3 else frozenset(dirs)
            options[size].append((sum(1 << i for i in indices), shape))

    layers = [[] for _ in range(7)]
    for a in range(4):
        for b in range(4):
            if a+b > 6:
                continue
            for aa, da in options[a]:
                for bb, db in options[b]:
                    if (da is None and b) or (db is None and a):
                        continue
                    if da is not None and db is not None and not da.isdisjoint(db):
                        continue
                    layers[a+b].append(aa | (bb << n))
    all_safe = set().union(*layers)
    assert len(all_safe) == sum(map(len, layers))

    values = {}
    failures = Counter()
    terminal = Counter()
    witnesses = {}
    for size in range(6, -1, -1):
        for s in layers[size]:
            children = [values[s | (1 << i)] for i in range(2*n)
                        if not (s >> i & 1) and (s | (1 << i)) in all_safe]
            if not children:
                terminal[size] += 1
            gs = {g for g, _ in children}
            hs = {h for _, h in children}
            g = 0
            while g in gs:
                g += 1
            h = 1 if not children else 0
            while h in hs:
                h += 1
            values[s] = (g, h)
            if h != (1-g if g < 2 else g):
                failures[size] += 1
                witnesses.setdefault(size, (s, g, h))
    return ([len(layer) for layer in layers],
            [failures[i] for i in range(7)], values[0],
            [terminal[i] for i in range(7)], witnesses)

def main():
    for board, expected in EXPECTED.items():
        counts, failures, root, terminal, witnesses = audit(*board)
        assert (counts, failures, root) == expected, (board, counts, failures, root)
        print(f'{board}: safe={counts} failures={failures} root={root} terminal={terminal}')
        if witnesses:
            print('  witnesses:', witnesses)
    print('All thirteen finite boards agree with the independent determinant census.')

if __name__ == '__main__':
    main()
