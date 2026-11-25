#!/usr/bin/env python3
"""Independent point-level checks for all-r terminal-spectrum universality.

No third-party packages. Enumerates actual hitting sets, not signature covers.
"""
from itertools import combinations
from math import prod


def construct(r, q, desired, pad):
    """r q-uniform edges, each with private points; desired transversal sizes."""
    assert r >= 2 and q >= r
    assert set(desired) <= set(range(1, r))
    signatures = [frozenset(range(r - k + 1)) for k in sorted(desired)]
    private_counts = [q - sum(i in a for a in signatures) for i in range(r)]
    assert min(private_counts) >= 1
    signatures += [frozenset([i]) for i in range(r) for _ in range(private_counts[i])]
    if pad:
        signatures += [frozenset() for _ in range(r * q - len(signatures))]
        assert len(signatures) == r * q
    edges = [sum(1 << j for j, a in enumerate(signatures) if i in a) for i in range(r)]
    assert all(e.bit_count() == q for e in edges)
    return signatures, edges, private_counts


def construct_minimal(r, desired):
    signatures = [frozenset(range(r-k+1)) for k in sorted(desired)]
    signatures += [frozenset([i]) for i in range(r)]
    edges = [sum(1 << j for j, a in enumerate(signatures) if i in a) for i in range(r)]
    return signatures, edges, [1]*r


def predicted(r, desired, counts, N):
    ans = {N - r: prod(counts)}
    for k in desired:
        ans[N - k] = prod(counts[r - k + 1:])
    return ans


def direct_hitting_counts(edges, N):
    """Enumerate candidate hitting sets of cardinality <= number of edges."""
    r = len(edges)
    out = {}
    for k in range(1, r + 1):
        for inds in combinations(range(N), k):
            mask = sum(1 << i for i in inds)
            if any(not (mask & e) for e in edges):
                continue
            if any(all((mask ^ (1 << j)) & e for e in edges) for j in inds):
                continue
            out[N - k] = out.get(N - k, 0) + 1
    return out


def independent_safe_maximal(edges, N):
    """Enumerate all safe subsets; no hitting-set minimality test used."""
    out = {}
    allmask = (1 << N) - 1
    for occupied in range(1 << N):
        if any(occupied & e == e for e in edges):
            continue
        unoccupied = allmask ^ occupied
        if all(any((occupied | (1 << j)) & e == e for e in edges)
               for j in range(N) if unoccupied & (1 << j)):
            k = occupied.bit_count()
            out[k] = out.get(k, 0) + 1
    return out


def check(r, q, desired, pad, full=False, minimal=False):
    signatures, edges, counts = (construct_minimal(r, desired) if minimal
                                 else construct(r, q, desired, pad))
    N = len(signatures)
    want = predicted(r, desired, counts, N)
    got = direct_hitting_counts(edges, N)
    assert got == want, (r, q, desired, pad, got, want)
    if full:
        other = independent_safe_maximal(edges, N)
        assert other == want, (r, q, desired, pad, other, want)
    return N


def main():
    cases = 0
    subset_tests = 0
    for r in range(2, 8):
        q = r
        for bits in range(1 << (r - 1)):
            desired = tuple(k for k in range(1, r) if bits & (1 << (k - 1)))
            check(r, q, desired, pad=False, full=True, minimal=True)
            cases += 1
            subset_tests += 1 << (r + len(desired))
    for r in range(2, 6):
        q = r
        for bits in range(1 << (r - 1)):
            desired = tuple(k for k in range(1, r) if bits & (1 << (k - 1)))
            check(r, q, desired, pad=True, full=(r <= 4))
            cases += 1
            if r <= 4:
                subset_tests += 1 << (r * q)
    for r, q in ((3, 4), (4, 5), (5, 6)):
        for bits in (0, 1, (1 << (r-1)) - 1):
            desired = tuple(k for k in range(1, r) if bits & (1 << (k - 1)))
            check(r, q, desired, pad=False, full=False)
            cases += 1
    print(f"PASS: {cases} configurations; {subset_tests} subsets in independent full enumeration; all 2^(r-1) abstract spectra for r=2..7")


if __name__ == '__main__':
    main()
