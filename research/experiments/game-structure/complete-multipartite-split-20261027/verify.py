#!/usr/bin/env python3
"""Two independent exact recurrences for multipartite graphs and a split witness."""
from functools import lru_cache
from itertools import product

SIGNATURES = ((0, 2, 4, 5), (0, 1, 2), (4,), (0, 3), (0, 1, 5), (0, 3, 4))


def split_edges():
    return (tuple((i, j) for i in range(6) for j in range(i + 1, 6))
            + tuple((c, 6 + i) for i, sig in enumerate(SIGNATURES) for c in sig))


def closed_neighborhoods(n, edges):
    closed = [1 << v for v in range(n)]
    for a, b in edges:
        assert 0 <= a < b < n
        closed[a] |= 1 << b
        closed[b] |= 1 << a
    return closed


def remaining(n, edges):
    closed = closed_neighborhoods(n, edges)

    @lru_cache(None)
    def rec(mask):
        if not mask:
            return 0
        vals = {rec(mask & ~closed[v]) for v in range(n) if mask & (1 << v)}
        return next(x for x in range(n + 1) if x not in vals)

    full = (1 << n) - 1
    return rec(full), tuple(rec(full & ~closed[v]) for v in range(n)), rec.cache_info().currsize


def occupied(n, edges):
    closed = closed_neighborhoods(n, edges)

    @lru_cache(None)
    def rec(chosen):
        vals = {rec(chosen | (1 << v)) for v in range(n) if not (chosen & closed[v])}
        return next(x for x in range(n + 1) if x not in vals)

    return rec(0), tuple(rec(1 << v) for v in range(n)), rec.cache_info().currsize


def multipartite(sizes):
    parts = []
    n = 0
    for size in sizes:
        parts.append(tuple(range(n, n + size)))
        n += size
    edges = tuple((a, b) for i, pi in enumerate(parts)
                  for pj in parts[i + 1:] for a in pi for b in pj)
    return n, edges


def formula(sizes):
    if not sizes:
        return 0
    children = {(size - 1) % 2 for size in sizes}
    return next(x for x in range(3) if x not in children)


def main():
    edges = split_edges()
    assert len(edges) == 31
    a = remaining(12, edges)
    b = occupied(12, edges)
    assert a[:2] == b[:2]
    assert a[0] == 4
    assert a[1] == (1, 0, 0, 0, 1, 0, 0, 3, 2, 3, 3, 0)
    print("split witness: vertices=12 edges=31 g=4 children=", a[1],
          "states=", (a[2], b[2]))
    count = 0
    for k in range(5):
        for sizes in product(range(1, 5), repeat=k):
            n, edges = multipartite(sizes)
            if n > 12:
                continue
            expected = formula(sizes)
            x = remaining(n, edges)[0]
            y = occupied(n, edges)[0]
            assert x == y == expected, (sizes, x, y, expected)
            count += 1
    assert count == 306
    print("complete multipartite: 306 exact checks, zero mismatches")


if __name__ == "__main__":
    main()
