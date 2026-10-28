#!/usr/bin/env python3
"""Independent explicit Node Kayles and subset-mex checks for K5 missing pairs."""
from functools import lru_cache
from itertools import product
from random import Random


def full_graph(k, pair_counts, leaves):
    adj = [0] * k
    for i in range(k):
        for j in range(i + 1, k):
            adj[i] |= 1 << j
            adj[j] |= 1 << i

    def add(neighbors):
        v = len(adj)
        adj.append(0)
        for j in neighbors:
            adj[v] |= 1 << j
            adj[j] |= 1 << v

    for (i, j), count in sorted(pair_counts.items()):
        for _ in range(count):
            add((i, j))
    for i, count in enumerate(leaves):
        for _ in range(count):
            add((i,))

    @lru_cache(None)
    def g(mask):
        options = set()
        for v in range(len(adj)):
            if mask >> v & 1:
                options.add(g(mask & ~(adj[v] | (1 << v))))
        x = 0
        while x in options:
            x += 1
        return x

    all_mask = (1 << len(adj)) - 1
    children = [g(all_mask & ~(adj[v] | (1 << v))) for v in range(len(adj))]
    return len(adj), g(all_mask), children


def quotient_by_remaining_clique(k, pairs, leaves):
    """Directly count newly isolated groups, unlike the C++ parity-difference recurrence."""
    groups = [(sum(1 << x for x in edge), n) for edge, n in pairs.items() if n]
    groups.extend((1 << i, n) for i, n in enumerate(leaves) if n)
    dp = [0] * (1 << k)
    for active in range(1, 1 << k):
        options = set()
        for i in range(k):
            if active & (1 << i):
                isolated = sum(n for group, n in groups
                               if group & active and not group & (1 << i))
                options.add(isolated & 1)
        for group, n in groups:
            if not group & active:
                continue
            remain = active & ~group
            isolated = sum(n for other, n in groups
                           if other & active and not other & remain)
            options.add(dp[remain] ^ ((isolated - 1) & 1))
        mex = 0
        while mex in options:
            mex += 1
        dp[active] = mex
    return dp[-1]


def prediction(k, pairs, leaves):
    u = (sum(pairs.values()) + sum(leaves)) % 2
    z = [(leaves[i] + sum(n for edge, n in pairs.items() if i in edge)) % 2
         for i in range(k)]
    return (1 ^ u ^ z[0]) if len(set(z)) == 1 else (2 + u)


def pairs_from_mask(k, mask):
    edges = [(i, j) for i in range(k) for j in range(i + 1, k)
             if i >= 5 or j >= 5]
    return {edge: 1 + ((mask >> index) & 1)
            for index, edge in enumerate(edges)}


def main():
    for leaves, expected, children in [
        ((0, 0, 0, 0, 1, 0), 3, {0, 1, 2}),
        ((0, 0, 0, 1, 1, 0), 5, {0, 1, 2, 3, 4}),
    ]:
        pairs = pairs_from_mask(6, 15)
        assert quotient_by_remaining_clique(6, pairs, leaves) == expected
        n, actual, options = full_graph(6, pairs, leaves)
        assert actual == expected and set(options) == children
        print('named witness', n, 'g=', actual, 'child values=', options)

    tested = 0
    for mask in range(32):
        pairs = pairs_from_mask(6, mask)
        for first_five in product((1, 2), repeat=5):
            for extra in range(3):
                leaves = first_five + (extra,)
                actual = quotient_by_remaining_clique(6, pairs, leaves)
                assert actual == prediction(6, pairs, leaves)
                tested += 1
    assert tested == 3072
    print('independent k=6 protected base:', tested, 'exact cases')

    rng = Random(20261028)
    for _ in range(300):
        k = 7
        pairs = pairs_from_mask(k, rng.randrange(1 << 11))
        leaves = tuple(rng.randrange(3) for _ in range(k))
        assert quotient_by_remaining_clique(k, pairs, leaves) == prediction(k, pairs, leaves)
    print('independent k=7 random cases: 300')


if __name__ == '__main__':
    main()
