#!/usr/bin/env python3
"""Exact all-dimension maximal integer-line histogram, with independent pair enumerator."""
from collections import Counter
from itertools import combinations, product
from math import gcd, comb, prod


def mobius_sieve(n):
    mu = [0] * (n + 1)
    if n >= 1:
        mu[1] = 1
    primes, composites = [], [False] * (n + 1)
    for i in range(2, n + 1):
        if not composites[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            j = i * p
            if j > n:
                break
            composites[j] = True
            if i % p == 0:
                mu[j] = 0
                break
            mu[j] = -mu[i]
    return mu


def fast_histogram(sizes):
    """E[k] = number of distinct maximal lattice lines containing exactly k points."""
    assert sizes and all(n >= 1 for n in sizes)
    nmax = max(sizes)
    if nmax <= 1:
        return {}
    mu = mobius_sieve(nmax - 1)
    F = [0] * nmax
    total = prod(sizes)
    for t in range(1, nmax):
        val = 1
        for n in sizes:
            a = (n - 1) // t
            val *= (2 * a + 1) * n - t * a * (a + 1)
        F[t] = val - total
    # P[k] = sum_{ell>=k} (ell-k+1) E[ell].
    P = [0] * (nmax + 3)
    for s in range(1, nmax):
        numerator = sum(mu[a] * F[s * a] for a in range(1, (nmax - 1) // s + 1))
        assert numerator % 2 == 0, (sizes, s, numerator)
        P[s + 1] = numerator // 2
    E = {k: P[k] - 2 * P[k + 1] + P[k + 2] for k in range(2, nmax + 1)}
    assert all(v >= 0 for v in E.values()), (sizes, E)
    return {k: v for k, v in E.items() if v}


def pair_enumerated_histogram(sizes):
    """Independent direct geometric method: canonical maximal lines from every pair."""
    pts = list(product(*(range(n) for n in sizes)))
    d = len(sizes)
    lines = {}
    for p, q in combinations(pts, 2):
        delta = tuple(q[i] - p[i] for i in range(d))
        g = 0
        for x in delta:
            g = gcd(g, abs(x))
        v = tuple(x // g for x in delta)
        if next(x for x in v if x) < 0:
            v = tuple(-x for x in v)
        start = p
        while all(0 <= start[i] - v[i] < sizes[i] for i in range(d)):
            start = tuple(start[i] - v[i] for i in range(d))
        key = (v, start)
        if key not in lines:
            count, cur = 0, start
            while all(0 <= cur[i] < sizes[i] for i in range(d)):
                count += 1
                cur = tuple(cur[i] + v[i] for i in range(d))
            lines[key] = count
    return dict(sorted(Counter(lines.values()).items()))


def direct_collinear_subsets(sizes, q):
    pts = list(product(*(range(n) for n in sizes)))
    d = len(sizes)
    count = 0
    for tup in combinations(pts, q):
        delta = [tup[1][i] - tup[0][i] for i in range(d)]
        if all(all(delta[i] * (p[j] - tup[0][j]) == delta[j] * (p[i] - tup[0][i])
                   for i in range(d) for j in range(i + 1, d)) for p in tup[2:]):
            count += 1
    return count


def run():
    boxes = set()
    for d, max_side in [(1, 10), (2, 7), (3, 4), (4, 3)]:
        boxes.update(product(range(1, max_side + 1), repeat=d))
    for i, sizes in enumerate(sorted(boxes, key=lambda a: (len(a), a)), 1):
        fast = fast_histogram(sizes)
        direct = pair_enumerated_histogram(sizes)
        assert fast == direct, (sizes, fast, direct)
    subset_cases = 0
    for sizes in sorted(boxes, key=lambda a: (len(a), a)):
        n = prod(sizes)
        if 3 <= n <= 12:
            hist = fast_histogram(sizes)
            for q in range(3, min(n, max(sizes)) + 1):
                got = sum(v * comb(k, q) for k, v in hist.items() if k >= q)
                want = direct_collinear_subsets(sizes, q)
                assert got == want, (sizes, q, got, want)
                subset_cases += 1
    for sizes in [(3, 3, 3), (2, 3, 4), (11, 11), (100, 100), (4, 4, 4)]:
        hist = fast_histogram(sizes)
        print(f"{sizes}: lines={sum(hist.values())}, histogram={hist if max(sizes)<=11 else 'omitted'}")
        if sizes == (11, 11):
            for q in (3, 4, 5, 6, 8):
                print(f"  collinear q={q}: {sum(v*comb(k,q) for k,v in hist.items() if k>=q)}")
    print(f"PASS: {len(boxes)} boxes; {subset_cases} direct q-subset checks")


if __name__ == '__main__':
    run()
