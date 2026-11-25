#!/usr/bin/env python3
"""Independent exact checks for co-degree-one split graphs (standard library)."""
from fractions import Fraction
from functools import lru_cache
from itertools import product, permutations
from collections import defaultdict
from math import factorial


def model(m, assignment):
    """Center j misses independent vertex assignment[j]."""
    k = len(assignment)
    n = m + k
    adj = [0] * n
    for a in range(k):
        for b in range(a):
            adj[m + a] |= 1 << (m + b)
            adj[m + b] |= 1 << (m + a)
        for v in range(m):
            if v != assignment[a]:
                adj[m + a] |= 1 << v
                adj[v] |= 1 << (m + a)
    return tuple(adj)


def exact_recursive(m, assignment):
    adj = model(m, assignment)
    k = len(assignment)

    @lru_cache(None)
    def rec(mask):
        if not mask:
            return (Fraction(1), (1,), 0)
        available = [v for v in range(m + k) if mask >> v & 1]
        prob = Fraction(0)
        child_nimbers = []
        lengths = defaultdict(Fraction)
        for v in available:
            child = mask & ~(adj[v] | (1 << v))
            p, dist, g = rec(child)
            if v < m:
                prob += p / len(available)
            child_nimbers.append(g)
            for i, q in enumerate(dist):
                lengths[i + 1] += q * Fraction(1, len(available))
        g = 0
        while g in child_nimbers:
            g += 1
        return prob, tuple(lengths.get(i, Fraction(0)) for i in range(max(lengths) + 1)), g

    @lru_cache(None)
    def no_center(mask):
        if not mask:
            return Fraction(1)
        moves = [v for v in range(m + k) if mask >> v & 1]
        return sum((no_center(mask & ~(adj[v] | (1 << v))) if v < m else Fraction(0)) for v in moves) / len(moves)

    initial = (1 << (m + k)) - 1
    _, dist, g = rec(initial)
    return no_center(initial), dist, g


def formula(m, assignment):
    k = len(assignment)
    t = [assignment.count(j) for j in range(m)]
    p = Fraction(m - 1, m + k) * sum((Fraction(1, m - 1 + x) for x in t), Fraction(0))
    if m % 2 == 0:
        g = 0
    elif k == 0:
        g = 1
    elif min(t) == 0:
        g = 3
    else:
        g = 0
    length = [Fraction(0)] * (max(m, 2) + 1)
    if k:
        length[2] += 1 - p
    length[m] += p
    return p, tuple(length), g


def sharp_bounds(m, k):
    a, r = divmod(k, m)
    lo = Fraction(m - 1, m + k) * (
        Fraction(m - r, m - 1 + a) + Fraction(r, m + a)
    )
    hi = Fraction(m - 1, m + k - 1)
    return lo, hi


def exhaustive():
    checked = 0
    grouped = defaultdict(list)
    for m in range(2, 6):
        for k in range(0, 7):
            if m ** k > 9000:
                continue
            for assignment in product(range(m), repeat=k):
                expected = formula(m, assignment)
                got = exact_recursive(m, assignment)
                assert got == expected, (m, assignment, got, expected)
                p = got[0]
                lo, hi = sharp_bounds(m, k)
                assert lo <= p <= hi
                grouped[(m, k)].append(p)
                checked += 1
    for (m, k), vals in grouped.items():
        lo, hi = sharp_bounds(m, k)
        assert min(vals) == lo and max(vals) == hi, (m, k, min(vals), max(vals), lo, hi)
    return checked, len(grouped)


def permutation_check():
    checked = 0
    for m in range(2, 5):
        for k in range(0, 5):
            if m + k > 8:
                continue
            for assignment in product(range(m), repeat=k):
                if checked > 350:
                    return checked
                adj = model(m, assignment)
                count = 0
                lengths = defaultdict(int)
                total = factorial(m + k)
                for order in permutations(range(m + k)):
                    blocked = 0
                    selected = []
                    for v in order:
                        if not blocked >> v & 1:
                            selected.append(v)
                            blocked |= adj[v] | (1 << v)
                    if all(v < m for v in selected):
                        count += 1
                    lengths[len(selected)] += 1
                p, dist, _ = formula(m, assignment)
                assert Fraction(count, total) == p, (m, assignment)
                assert all(Fraction(lengths[i], total) == dist[i] for i in range(len(dist)))
                checked += 1
    return checked


if __name__ == '__main__':
    a, b = exhaustive()
    c = permutation_check()
    print(f'exact closed-neighborhood recursion: {a} labeled configurations, {b} (m,k) classes, zero mismatches')
    print(f'independent greedy-permutation enumeration: {c} configurations, zero mismatches')
    for m, k in ((3, 5), (4, 6), (5, 5)):
        print(f'm={m}, k={k}: sharp P_I interval = {sharp_bounds(m, k)}')
