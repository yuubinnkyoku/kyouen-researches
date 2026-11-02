#!/usr/bin/env python3
"""Independent audits for the path graph-star terminal run formula.

No third-party dependencies. Run:
python research/experiments/path-run-coefficients-20261103/verify.py
"""
from collections import Counter
from math import comb


def closed(n, r):
    """Counts center-containing maximal positions by excess k over s=N-(n-1)."""
    assert n >= 2 and r >= 1
    out = Counter()
    for k in range((n + 1) // 2):
        for left in (0, 1):
            for right in (0, 1):
                for doubled in range(k + 1):
                    kept = n - left - right - k - doubled
                    edges = kept - k - 1
                    if kept >= k + 1:
                        out[k] += (comb(k, doubled) * comb(kept - 1, k)
                                   * r ** edges)
    return out


def enumerate_deleted(n, r):
    """Independent enumeration of deleted vertex subsets, checking domination."""
    out = Counter()
    for mask in range(1 << n):
        deleted = [bool(mask & (1 << i)) for i in range(n)]
        if any(deleted[i] and not (
            (i > 0 and not deleted[i - 1]) or
            (i + 1 < n and not deleted[i + 1])
        ) for i in range(n)):
            continue
        retained_edges = sum(not deleted[i] and not deleted[i + 1]
                             for i in range(n - 1))
        excess = n - 1 - sum(deleted) - retained_edges
        assert excess >= 0
        out[excess] += r ** retained_edges
    return out


def recurrence(n, r):
    """K0609's independent three-term transfer recurrence, normalized to excess."""
    S = {
        2: Counter({3: r + 2}),
        3: Counter({4: (r + 1) ** 2, 5: 1}),
        4: Counter({5: r * (r + 1) ** 2, 6: 2 * r + 3}),
    }
    for t in range(5, n + 1):
        p = Counter()
        for shift, factor, prev in ((1, r, t - 1), (3, 1, t - 2),
                                    (4, 1, t - 3)):
            for degree, coefficient in S[prev].items():
                p[degree + shift] += factor * coefficient
        S[t] = p
    return Counter({degree - (n + 1): coefficient
                    for degree, coefficient in S[n].items()})


def hyperedge_enumeration(n, r):
    """Directly enumerate maximal safe subsets of the abstract q-point hypergraph."""
    N = 1 + n + r * (n - 1)
    assert N <= 19
    hyperedges = []
    for edge in range(n - 1):
        points = [0, 1 + edge, 2 + edge]
        points += list(range(1 + n + r * edge, 1 + n + r * (edge + 1)))
        assert len(points) == r + 3
        hyperedges.append(sum(1 << p for p in points))
    full = (1 << N) - 1
    out = Counter()
    for mask in range(1 << N):
        if any(mask & h == h for h in hyperedges):
            continue
        missing = full ^ mask
        maximal = True
        while missing:
            bit = missing & -missing
            missing ^= bit
            if not any((mask | bit) & h == h for h in hyperedges):
                maximal = False
                break
        if maximal:
            out[mask.bit_count()] += 1
    return out


def main():
    checks = 0
    for n in range(2, 17):
        for r in (1, 2, 3, 5, 17):
            got = closed(n, r)
            assert got == enumerate_deleted(n, r) == recurrence(n, r), (n, r)
            assert set(got) == set(range((n + 1) // 2)), (n, r)
            if n % 2:
                assert got[(n - 1) // 2] == 1, (n, r)
            elif n >= 4:
                assert got[n // 2 - 1] == n // 2 * (r + 1) + 1, (n, r)
            checks += 1
    large_checks = 0
    for n in (20, 21, 40, 51, 100, 101, 200):
        for r in (1, 2, 1000003):
            assert closed(n, r) == recurrence(n, r), (n, r)
            large_checks += 1
    hyper_checks = 0
    for n, r in ((2, 1), (2, 2), (2, 3), (3, 1), (3, 2),
                 (3, 3), (4, 1), (4, 2), (4, 3), (5, 1),
                 (5, 2), (6, 1)):
        N = 1 + n + r * (n - 1)
        assert N <= 19
        s = N - (n - 1)
        expected = Counter({s + k: v for k, v in closed(n, r).items()})
        expected[N - 1] += 1
        assert expected == hyperedge_enumeration(n, r), (n, r)
        hyper_checks += 1
    print(f"OK: {checks} triple comparisons, {large_checks} long recurrences, "
          f"{hyper_checks} independent maximal-hypergraph enumerations; mismatches=0")


if __name__ == '__main__':
    main()
