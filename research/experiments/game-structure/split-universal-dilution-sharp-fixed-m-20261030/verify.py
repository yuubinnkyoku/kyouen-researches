#!/usr/bin/env python3
"""Exact independent checks for the universal-clique dilution theorem."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product, permutations
from math import factorial


def game(adjacency, center_mask=0):
    n = len(adjacency)
    allmask = (1 << n) - 1

    @lru_cache(None)
    def rec(mask):
        if not mask:
            return ({0: Fraction(1)}, Fraction(1), 0, 1)
        vs = [v for v in range(n) if mask >> v & 1]
        d = Counter()
        p = Fraction(0)
        options = set()
        sequences = 0
        for v in vs:
            child = mask & ~(adjacency[v] | (1 << v))
            dd, pp, gg, ss = rec(child)
            for length, weight in dd.items():
                d[length + 1] += weight / len(vs)
            if not (center_mask >> v & 1):
                p += pp / len(vs)
            options.add(gg)
            sequences += ss
        g = 0
        while g in options:
            g += 1
        return (dict(d), p, g, sequences)

    return rec(allmask)


def split(m, assignment, c):
    """m independent vertices, k singleton centers, c universal centers."""
    k = len(assignment)
    n = m + k + c
    a = [0] * n
    for idx, j in enumerate(assignment):
        v = m + idx
        a[v] |= 1 << j
        a[j] |= 1 << v
    for v in range(m, n):
        for w in range(m, n):
            if v != w:
                a[v] |= 1 << w
    for v in range(m + k, n):
        for j in range(m):
            a[v] |= 1 << j
            a[j] |= 1 << v
    return a, ((1 << (k + c)) - 1) << m


def universal_extension(a, c):
    n = len(a)
    return [x | (((1 << c) - 1) << n) for x in a] + [((1 << (n + c)) - 1) ^ (1 << v) for v in range(n, n + c)]


def check_general():
    checks = 0
    for n in range(1, 5):
        edges = [(i, j) for i in range(n) for j in range(i)]
        for bits in range(1 << len(edges)):
            a = [0] * n
            for e, (i, j) in enumerate(edges):
                if bits >> e & 1:
                    a[i] |= 1 << j
                    a[j] |= 1 << i
            base = game(a)
            for c in range(1, 4):
                ext = game(universal_extension(a, c))
                factor = Fraction(n, n + c)
                expected = Counter({length: p * factor for length, p in base[0].items()})
                expected[1] += Fraction(c, n + c)
                assert ext[0] == dict(expected), (n, bits, c, ext[0], expected)
                assert ext[3] == base[3] + c, (n, bits, c)
                checks += 1
    return checks


def check_split():
    count = 0
    cases = 0
    for m in range(1, 5):
        for k in range(0, 6):
            for assignment in product(range(m), repeat=k):
                t = [assignment.count(j) for j in range(m)]
                for c in range(0, 4):
                    a, centers = split(m, assignment, c)
                    d, p, g, sequences = game(a, centers)
                    expected_p = Fraction(m + k, m + k + c)
                    for x in t:
                        expected_p /= (x + 1)
                    assert p == expected_p, (m, k, assignment, c, p, expected_p)
                    expected_d = Counter({m: Fraction(m + k, m + k + c)})
                    if c:
                        expected_d[1] += Fraction(c, m + k + c)
                    assert d == dict(expected_d), (m, k, assignment, c, d, expected_d)
                    expected_g = m % 2 if c == 0 else (1 if m % 2 else 2)
                    assert g == expected_g, (m, k, assignment, c, g, expected_g)
                    assert sequences == (k + 1) * factorial(m) + c, (m, k, assignment, c, sequences)
                    a0, r0 = divmod(k, m)
                    lower = Fraction(m + k, m + k + c) / ((a0 + 1) ** (m - r0) * (a0 + 2) ** r0)
                    upper = Fraction(m + k, (m + k + c) * (k + 1))
                    assert lower <= p <= upper
                    assert (p == lower) == (max(t) - min(t) <= 1)
                    assert (p == upper) == (sum(x > 0 for x in t) <= 1)
                    count += 1
                cases += 1
    return count, cases


def check_priority():
    count = 0
    for m in range(1, 4):
        for k in range(0, 4):
            for c in range(0, 3):
                if m + k + c > 7:
                    continue
                for assignment in product(range(m), repeat=k):
                    a, centers = split(m, assignment, c)
                    n = len(a)
                    no_center = 0
                    dist = Counter()
                    for perm in permutations(range(n)):
                        mask = (1 << n) - 1
                        chosen = []
                        for v in perm:
                            if mask >> v & 1:
                                chosen.append(v)
                                mask &= ~(a[v] | (1 << v))
                        no_center += all(not (centers >> v & 1) for v in chosen)
                        dist[len(chosen)] += 1
                    d, p, _, _ = game(a, centers)
                    assert p == Fraction(no_center, factorial(n))
                    assert d == {x: Fraction(v, factorial(n)) for x, v in dist.items()}
                    count += 1
    return count


if __name__ == '__main__':
    print('general graphs / universal extension:', check_general())
    print('split configurations and assignments:', check_split())
    print('direct random-priority permutations:', check_priority())
    print('all checks passed')
