#!/usr/bin/env python3
"""Exact independent checks of weighted random-greedy factorization for hereditary games.

A forbidden hyperedge is a frozenset of vertices; legal occupied sets contain
no complete hyperedge. Vertices are processed in an exponential race (or,
equivalently, picked among currently legal vertices with fixed positive weights).
"""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from random import Random


def legal(mask, edges):
    return all((mask & e) != e for e in edges)


def direct_distribution(n, weights, edges, effective_weight=None):
    @lru_cache(None)
    def dp(mask):
        moves = [i for i in range(n) if not mask >> i & 1 and legal(mask | (1 << i), edges)]
        if not moves:
            return {mask: Fraction(1)}
        rates = {i: weights[i] if effective_weight is None else effective_weight(mask, i)
                 for i in moves}
        total = sum(rates.values())
        ans = defaultdict(Fraction)
        for i in moves:
            for final, p in dp(mask | (1 << i)).items():
                ans[final] += Fraction(rates[i], total) * p
        return dict(ans)
    return dp(0)


def permutation_distribution(n, weights, edges):
    ans = defaultdict(Fraction)
    for perm in permutations(range(n)):
        rem = sum(weights)
        p = Fraction(1)
        mask = 0
        for i in perm:
            p *= Fraction(weights[i], rem)
            rem -= weights[i]
            if legal(mask | (1 << i), edges):
                mask |= 1 << i
        ans[mask] += p
    return dict(ans)


def factor_distribution(n, weights, edges, parts):
    ans = {0: Fraction(1)}
    for part in parts:
        index = {v: i for i, v in enumerate(part)}
        local_edges = []
        for e in edges:
            support = [v for v in range(n) if e >> v & 1]
            if set(support) <= set(part):
                local_edges.append(sum(1 << index[v] for v in support))
            elif set(support) & set(part):
                raise ValueError('a forbidden edge spans components')
        local = direct_distribution(len(part), [weights[v] for v in part], local_edges)
        nxt = defaultdict(Fraction)
        for global_mask, q in ans.items():
            for local_mask, p in local.items():
                added = sum(1 << v for j, v in enumerate(part) if local_mask >> j & 1)
                nxt[global_mask | added] += q * p
        ans = dict(nxt)
    return ans


def size_polynomial(dist):
    out = defaultdict(Fraction)
    for mask, p in dist.items():
        out[mask.bit_count()] += p
    return dict(sorted(out.items()))


def main():
    rng = Random(20261020)
    cases = 0
    # Fully arbitrary forbidden hypergraphs inside the two components.
    for n in range(2, 8):
        for _ in range(55):
            cut = rng.randrange(1, n)
            parts = [list(range(cut)), list(range(cut, n))]
            weights = [rng.randrange(1, 8) for _ in range(n)]
            edges = []
            for part in parts:
                for mask in range(1, 1 << len(part)):
                    if mask.bit_count() >= 2 and rng.randrange(3) == 0:
                        edges.append(sum(1 << v for j, v in enumerate(part) if mask >> j & 1))
            a = direct_distribution(n, weights, edges)
            b = factor_distribution(n, weights, edges, parts)
            c = permutation_distribution(n, weights, edges)
            assert a == b == c, (n, weights, edges, a, b, c)
            # Arbitrary state-dependent positive factor per component preserves
            # local relative weights and therefore terminal independence.
            def dynamic_weight(mask, v):
                comp = 0 if v < cut else 1
                factor = 1 + ((3 * mask.bit_count() + 5 * comp + mask % 7) % 9)
                return weights[v] * factor
            dynamic = direct_distribution(n, weights, edges, dynamic_weight)
            assert dynamic == b, (n, weights, edges, dynamic, b)
            assert sum(a.values()) == 1
            global_bias = sum(((-1) ** (m.bit_count())) * p for m, p in a.items())
            local_bias_product = Fraction(1)
            for part in parts:
                idx = {v: j for j, v in enumerate(part)}
                loc_edges = [sum(1 << idx[v] for v in part if e >> v & 1)
                             for e in edges if e & sum(1 << v for v in part)]
                loc = direct_distribution(len(part), [weights[v] for v in part], loc_edges)
                local_bias_product *= sum(((-1) ** (m.bit_count())) * p for m, p in loc.items())
            assert global_bias == local_bias_product
            cases += 1
    # Two disjoint P3 components, unequal positive vertex weights.
    n = 6
    edges = [0b000011, 0b000110, 0b011000, 0b110000]
    weights = [1, 3, 2, 1, 4, 5]
    actual = size_polynomial(direct_distribution(n, weights, edges))
    expected = {2: Fraction(1, 5), 3: Fraction(1, 2), 4: Fraction(3, 10)}
    assert actual == expected, (actual, expected)
    print('PASS: direct recursion / component product / weighted permutations / state-dependent component rates')
    print('Random decomposable hypergraphs:', cases)
    print('P3 + P3 exact terminal-size law:', actual)
    print('Expected terminal size:', sum(t * p for t, p in actual.items()))

if __name__ == '__main__':
    main()
