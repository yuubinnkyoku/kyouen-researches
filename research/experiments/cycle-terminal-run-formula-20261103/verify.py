#!/usr/bin/env python3
"""Independent finite audit for cyclic graph-star terminal coefficients.

Method A: cyclic 0/1 deletion words and induced-edge counts.
Method B: exact run-composition binomial formula.
Method C: K0608's independent three-term polynomial recurrence.
"""
from collections import defaultdict
from math import comb


def direct(n, r):
    out = defaultdict(int)
    for x in range(1 << n):
        deleted = [(x >> i) & 1 for i in range(n)]
        if any(deleted[i] and deleted[(i - 1) % n] and deleted[(i + 1) % n]
               for i in range(n)):
            continue
        runs = sum(deleted[i] and not deleted[(i - 1) % n] for i in range(n))
        remaining_edges = sum(not deleted[i] and not deleted[(i + 1) % n] for i in range(n))
        out[runs] += r ** remaining_edges
    return dict(out)


def formula(n, r):
    out = {0: r ** n}
    for k in range(1, n // 2 + 1):
        numerator = 0
        for j in range(min(k, n - 2 * k) + 1):
            numerator += comb(k, j) * comb(n - k - j - 1, k - 1) * r ** (n - 2 * k - j)
        assert (n * numerator) % k == 0
        out[k] = n * numerator // k
    return out


def recurrence(n, r):
    # Q_n: exponent n+k; this method does not inspect cyclic deletion words.
    a = {1: {0: r}, 2: {0: r*r, 1: 2},
         3: {0: r**3, 1: 3*(r+1)}}
    for t in range(4, n + 1):
        z = defaultdict(int)
        for k, v in a[t-1].items(): z[k] += r*v
        for k, v in a[t-2].items(): z[k+1] += v
        for k, v in a[t-3].items(): z[k+1] += v
        a[t] = dict(z)
    return a[n]


def hypergraph_direct(n, r):
    """Enumerate all point subsets of abstract K0602 forbidden hyperedges."""
    edges = []
    for i in range(n):
        private_start = n + 1 + i * r
        mask = (1 << 0) | (1 << (1 + i)) | (1 << (1 + ((i+1) % n)))
        for j in range(r):
            mask |= 1 << (private_start + j)
        edges.append(mask)
    N = 1 + n + n*r
    out = defaultdict(int)
    for x in range(1 << N):
        if any((x & h) == h for h in edges):
            continue
        if any(not (x >> i & 1) and not any(((x | (1 << i)) & h) == h for h in edges)
               for i in range(N)):
            continue
        out[x.bit_count()] += 1
    return dict(out)


def predicted_full(n, r):
    s = 1 + n*r
    out = defaultdict(int)
    for k, v in formula(n, r).items():
        out[s+k] += v
    out[n+n*r] += 1  # center-absent unique terminal
    return dict(out)


def run():
    cases = 0
    for n in range(3, 17):
        for r in (1, 2, 3, 5, 17, 101):
            a, b, c = direct(n, r), formula(n, r), recurrence(n, r)
            assert a == b == c, (n, r, a, b, c)
            assert set(a) == set(range(n // 2 + 1))
            cases += 1
    hypergraph_cases = 0
    for n in (3, 4, 5):
        for r in (1, 2):
            assert hypergraph_direct(n, r) == predicted_full(n, r), (n, r)
            hypergraph_cases += 1
    for n in (20, 21, 40, 51, 100, 101, 200):
        for r in (1, 2, 1000003):
            assert formula(n, r) == recurrence(n, r), (n, r)
            cases += 1
    print(f"PASS: {cases} parameter cases; {hypergraph_cases} forbidden-hypergraph full-subset enumerations; all agree")


if __name__ == '__main__':
    run()
