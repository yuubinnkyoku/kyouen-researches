#!/usr/bin/env python3
"""Exact relaxed enumeration of residual realizations of a fixed Grundy-5 set.

Integer lifted 4x4 determinant. We intentionally do NOT require occupied
4-tuples to be safe; the enumeration is a superset of valid game positions.
"""
from itertools import combinations
from functools import lru_cache

W = tuple(sorted(((0, 0), (0, 4), (1, 1), (1, 3), (3, 1),
                  (3, 2), (3, 4), (4, 1), (4, 5), (5, 0), (5, 2))))


def forbidden(points):
    (x, y), *rest = points
    a = [(u-x, v-y, u*u+v*v-x*x-y*y) for u, v in rest]
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])) == 0


def check_witness():
    edges = tuple(sum(1 << W.index(p) for p in t)
                  for t in combinations(W, 4) if forbidden(t))
    assert len(edges) == 4
    @lru_cache(None)
    def grundy(mask):
        child = set()
        for i in range(11):
            if mask >> i & 1:
                continue
            new = mask | (1 << i)
            if all(new & e != e for e in edges):
                child.add(grundy(new))
        k = 0
        while k in child:
            k += 1
        return k
    assert grundy(0) == 5
    assert grundy.cache_info().currsize == 1635
    print('witness: forbidden=4 safe=1635 g=5')


def audit(n):
    outside = tuple((x, y) for x in range(n) for y in range(n)
                    if (x, y) not in W)
    candidate = tuple(p for p in outside
                      if not any(forbidden((p, *t)) for t in combinations(W, 3)))
    z = len(candidate)
    pairs = set()
    for i, j in combinations(range(z), 2):
        if any(forbidden((candidate[i], candidate[j], *t))
               for t in combinations(W, 2)):
            pairs.add((i, j))
    triples = set()
    cover = {}
    for t in combinations(range(z), 3):
        pts = tuple(candidate[i] for i in t)
        if any(forbidden((*pts, w)) for w in W):
            triples.add(t)
        else:
            cover[t] = sum(1 << j for j, p in enumerate(outside)
                           if p not in pts and forbidden((*pts, p)))
    positions = {p: i for i, p in enumerate(outside)}
    count = max_s = max_blocked = 0
    full = (1 << len(outside)) - 1

    def walk(start, chosen, blocked, occupied):
        nonlocal count, max_s, max_blocked
        count += 1
        max_s = max(max_s, len(chosen))
        max_blocked = max(max_blocked, blocked.bit_count())
        assert (blocked | occupied) != full
        for i in range(start, z):
            if any((j, i) in pairs for j in chosen):
                continue
            if any((*ab, i) in triples for ab in combinations(chosen, 2)):
                continue
            b = blocked
            for ab in combinations(chosen, 2):
                b |= cover[(*ab, i)]
            walk(i + 1, (*chosen, i), b,
                 occupied | (1 << positions[candidate[i]]))

    walk(0, (), 0, 0)
    assert max_s + max_blocked < len(outside)
    return n, z, len(pairs), len(triples), count, max_s, max_blocked, len(outside)


if __name__ == '__main__':
    check_witness()
    expected = (
        (6, 0, 0, 0, 1, 0, 0, 25),
        (7, 1, 0, 0, 2, 1, 0, 38),
        (8, 2, 1, 0, 3, 1, 0, 53),
        (9, 9, 14, 15, 43, 3, 6, 70),
        (10, 18, 55, 84, 424, 5, 17, 89),
        (11, 27, 121, 233, 2234, 7, 33, 110),
        (12, 43, 254, 750, 58635, 10, 71, 133),
        (13, 60, 425, 1560, 1425787, 12, 126, 158),
    )
    for row in expected:
        got = audit(row[0])
        assert got == row, (got, row)
        print(got)
