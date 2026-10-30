#!/usr/bin/env python3
"""Two independent mex recursions for a tree family violating normal/misere swap."""
from functools import lru_cache

BASE = ((0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7))


def make_tree(odd, t):
    n = 8 + odd + 2*t
    return n, BASE + tuple((0, i) for i in range(8, n))


def mex(values):
    seen = set(values)
    result = 0
    while result in seen:
        result += 1
    return result


def bitmask_mex(n, edges):
    closed = [1 << i for i in range(n)]
    for u, v in edges:
        closed[u] |= 1 << v
        closed[v] |= 1 << u

    @lru_cache(None)
    def value(mask):
        if not mask:
            return (0, 1)
        children = [value(mask & ~closed[i]) for i in range(n) if mask & (1 << i)]
        return mex(p[0] for p in children), mex(p[1] for p in children)

    full = (1 << n) - 1
    return value(full), tuple(value(full & ~closed[i]) for i in range(n)), value.cache_info().currsize


def vertex_set_mex(n, edges):
    neighbor = {i: {i} for i in range(n)}
    for u, v in edges:
        neighbor[u].add(v)
        neighbor[v].add(u)

    @lru_cache(None)
    def value(vertices):
        if not vertices:
            return (0, 1)
        child = [value(vertices.difference(neighbor[v])) for v in sorted(vertices)]
        return mex(x for x, y in child), mex(y for x, y in child)

    full = frozenset(range(n))
    return value(full), tuple(value(full.difference(neighbor[i])) for i in range(n)), value.cache_info().currsize


def main():
    checked = 0
    for odd in (0, 1):
        expected = (3, 0) if odd else (1, 4)
        for t in range(6):
            n, edges = make_tree(odd, t)
            assert len(edges) == n - 1
            first = bitmask_mex(n, edges)
            second = vertex_set_mex(n, edges)
            assert first[:2] == second[:2], (n, first, second)
            assert first[0] == expected, (n, first[0])
            assert first[0][1] != (1 - first[0][0] if first[0][0] < 2 else first[0][0])
            if t == 0:
                print(f"base n={n}, (g,h)={first[0]}, children={first[1]}")
            checked += 1
    print(f"PASS: {checked} distinct labeled trees, two independent recursions, no mismatches")


if __name__ == '__main__':
    main()
