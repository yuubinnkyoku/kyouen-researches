#!/usr/bin/env python3
"""Finite independent checks of the universal linear vertex-cover Grundy bound.

The theorem is proved by induction, not by these finite checks.
"""
from functools import lru_cache
from itertools import combinations
from random import Random

G6 = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4),
      (3, 5), (4, 6), (7, 8), (7, 9)]


def adjacency(n, edges):
    a = [0] * n
    for u, v in edges:
        a[u] |= 1 << v
        a[v] |= 1 << u
    return a


def grundy_remaining(adj):
    n = len(adj)

    @lru_cache(None)
    def g(mask):
        children = {g(mask & ~(adj[v] | (1 << v)))
                    for v in range(n) if mask & (1 << v)}
        mex = 0
        while mex in children:
            mex += 1
        return mex

    return g((1 << n) - 1)


def grundy_occupied(adj):
    n = len(adj)

    @lru_cache(None)
    def g(chosen):
        children = {g(chosen | (1 << v)) for v in range(n)
                    if not (chosen & (1 << v)) and not (adj[v] & chosen)}
        mex = 0
        while mex in children:
            mex += 1
        return mex

    return g(0)


def alpha(adj):
    n = len(adj)
    independent = [False] * (1 << n)
    independent[0] = True
    best = 0
    for mask in range(1, 1 << n):
        bit = mask & -mask
        v = bit.bit_length() - 1
        rest = mask ^ bit
        independent[mask] = independent[rest] and not (adj[v] & rest)
        if independent[mask]:
            best = max(best, mask.bit_count())
    return best


def check(adj):
    n = len(adj)
    a = alpha(adj)
    tau = n - a
    g1 = grundy_remaining(adj)
    g2 = grundy_occupied(adj)
    assert g1 == g2, (adj, g1, g2)
    assert g1 <= a, (adj, g1, a)
    if tau >= 2:
        assert g1 <= 2 * tau - 1, (adj, g1, tau)
        if tau >= 3 and all(adj):
            assert g1 <= 2 * tau - 2, (adj, g1, tau)
    if g1 >= 4:
        assert n >= g1 + (g1 + 2) // 2, (adj, n, g1)
    return tau, g1


def main():
    totals = {}
    for n in range(7):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            adj = [0] * n
            for j, (u, v) in enumerate(pairs):
                if mask & (1 << j):
                    adj[u] |= 1 << v
                    adj[v] |= 1 << u
            tau, g = check(adj)
            totals[(n, tau)] = max(g, totals.get((n, tau), 0))
        print(f"all labelled graphs n={n}: {1 << len(pairs)} checked")

    rng = Random(20261027)
    for k in (3, 4, 5):
        for n in (9, 11, 13):
            for _ in range(200):
                adj = [0] * n
                for u in range(n):
                    for v in range(u + 1, n):
                        if (u < k or v < k) and rng.randrange(2):
                            adj[u] |= 1 << v
                            adj[v] |= 1 << u
                check(adj)
            print(f"random covered graphs k={k}, n={n}: 200 checked")

    for isolated in (False, True):
        n = 11 if isolated else 10
        adj = adjacency(n, G6)
        tau, g = check(adj)
        assert (tau, g) == (4, 7 if isolated else 6), (tau, g)
        print(f"sharp witness n={n}: tau={tau}, g={g}, isolated={isolated}")
    print("all tests passed")


if __name__ == '__main__':
    main()
