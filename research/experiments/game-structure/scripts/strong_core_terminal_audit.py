#!/usr/bin/env python3
"""Independent brute-force audit of the strong-core maximal-extension formula.

Usage: python strong_core_terminal_audit.py
All subsets are encoded as integer bit masks; forbidden hyperedges are masks.
"""
from collections import Counter
from itertools import combinations
from random import Random


def core_spectrum(n, edges, core):
    full = (1 << n) - 1
    outside = full ^ core
    assert all((h & outside).bit_count() <= 1 for h in edges)
    hist = Counter()
    maximal_masks = set()
    a = core
    while True:
        if not any((h & a) == h for h in edges):
            b = 0
            for v in range(n):
                bit = 1 << v
                if outside & bit and not any((h & (a | bit)) == h for h in edges):
                    b |= bit
            terminal = a | b
            if all(any((h & (terminal | (1 << v))) == h for h in edges)
                   for v in range(n) if not (terminal >> v & 1)):
                assert not any((h & terminal) == h for h in edges)
                assert terminal not in maximal_masks
                maximal_masks.add(terminal)
                hist[terminal.bit_count()] += 1
        if a == 0:
            break
        a = (a - 1) & core
    return hist, maximal_masks


def brute_spectrum(n, edges):
    maximal = set()
    for mask in range(1 << n):
        if any((h & mask) == h for h in edges):
            continue
        if all(any((h & (mask | (1 << v))) == h for h in edges)
               for v in range(n) if not (mask >> v & 1)):
            maximal.add(mask)
    return Counter(x.bit_count() for x in maximal), maximal


def valid_cores(n, edges):
    for core in range(1 << n):
        if all((h & (((1 << n) - 1) ^ core)).bit_count() <= 1 for h in edges):
            yield core


def audit():
    checks = 0
    # Every hypergraph with n<=4, edges of cardinality >=2,
    # and every admissible core (not just a minimum core).
    for n in range(5):
        possible = [sum(1 << i for i in subset)
                    for k in range(2, n + 1)
                    for subset in combinations(range(n), k)]
        for fam in range(1 << len(possible)):
            edges = [h for j, h in enumerate(possible) if fam >> j & 1]
            expected = brute_spectrum(n, edges)
            for core in valid_cores(n, edges):
                assert core_spectrum(n, edges, core) == expected, (n, edges, core)
                checks += 1
    print('exhaustive_n_le_4_checks=', checks)
    # Independently sample nonuniform, nested, singleton and empty hyperedges.
    rng = Random(20261019)
    random_checks = 0
    for n in range(1, 10):
        for _ in range(600):
            planted_core = rng.randrange(1 << n)
            possible = [h for h in range(1, 1 << n)
                        if (h & (((1 << n) - 1) ^ planted_core)).bit_count() <= 1]
            edges = [h for h in possible if rng.random() < min(0.35, 8 / len(possible))]
            expected = brute_spectrum(n, edges)
            assert core_spectrum(n, edges, planted_core) == expected
            random_checks += 1
    print('random_planted_core_checks=', random_checks)
    # k independent edges have 2^k distinct maximal independent sets.
    for k in range(1, 9):
        n = 2 * k
        edges = [(1 << (2 * i)) | (1 << (2 * i + 1)) for i in range(k)]
        core = sum(1 << (2 * i) for i in range(k))
        spectrum, terminals = core_spectrum(n, edges, core)
        assert spectrum == Counter({k: 1 << k})
        assert len(terminals) == 1 << k
    print('matching_tightness_k_1_to_8= PASS')
    print('ALL CHECKS PASS')


if __name__ == '__main__':
    audit()
