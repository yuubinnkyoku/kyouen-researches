#!/usr/bin/env python3
"""Independent exact named-vertex Node Kayles audit for disjoint odd-center/even-star cliques."""
from functools import lru_cache
from itertools import combinations_with_replacement


def predicted(ps, m):
    h = len(ps)
    assert h >= 1 and m >= 0 and all(p >= 0 for p in ps)
    if not (sum(ps) + m):
        return h % 2
    heavy = sum(p >= 3 for p in ps)
    if h % 2:
        return 2 if heavy > h // 2 else 3
    if heavy < h // 2:
        return 2
    return 4 if heavy == h // 2 else 3


def graph(ps, m, variant=0):
    h = len(ps)
    nclique = h + sum(ps) + m
    adj = [((1 << nclique) - 1) ^ (1 << i) for i in range(nclique)]

    def leaf(neighbors, count):
        for _ in range(count):
            j = len(adj)
            adj.append(0)
            for i in neighbors:
                adj[i] |= 1 << j
                adj[j] |= 1 << i

    for i in range(h):
        leaf([i], 1 if variant == 0 or i % 2 == 0 else 3)
    k = h
    for i, p in enumerate(ps):
        for j in range(p):
            leaf([i, k], 2 if variant == 0 or (i + j) % 2 == 0 else 4)
            k += 1
    for j in range(m):
        leaf([k], 2 if variant == 0 or j % 2 == 0 else 4)
        k += 1
    assert k == nclique
    return adj


def exact(adj):
    full = (1 << len(adj)) - 1
    closed = [a | (1 << i) for i, a in enumerate(adj)]

    @lru_cache(maxsize=None)
    def grundy(mask):
        children = set()
        left = mask
        while left:
            bit = left & -left
            i = bit.bit_length() - 1
            children.add(grundy(mask & ~closed[i]))
            left ^= bit
        g = 0
        while g in children:
            g += 1
        return g

    value = grundy(full)
    return value, grundy.cache_info().currsize


def main():
    tests = []
    # Every selected small parameter tuple, including the 2->3 branch transition.
    for h in range(1, 8):
        for ps in combinations_with_replacement(range(4), h):
            for m in range(2):
                if h + sum(ps) + m + h + 2 * (sum(ps) + m) > 23:
                    continue
                tests.append((ps, m, 0))
    # Odd center leaf counts 1/3 and even pair/aux multiplicities 2/4.
    for h in range(1, 5):
        for ps in combinations_with_replacement(range(4), h):
            for m in range(2):
                if h + sum(ps) + m + 2 * h + 3 * (sum(ps) + m) > 23:
                    continue
                tests.append((ps, m, 1))

    counts = {}
    max_states = (0, None)
    for ps, m, variant in tests:
        adj = graph(ps, m, variant)
        if len(adj) > 23:
            continue
        actual, states = exact(adj)
        expected = predicted(ps, m)
        assert actual == expected, (ps, m, variant, len(adj), actual, expected)
        counts[len(ps)] = counts.get(len(ps), 0) + 1
        if states > max_states[0]:
            max_states = (states, (ps, m, variant, len(adj)))
    print("PASS")
    print("tested by number of centers:", dict(sorted(counts.items())))
    print("total:", sum(counts.values()))
    print("maximum states:", max_states)

    for ps, m in [
        ((0, 0, 3), 0),
        ((0, 3, 3), 0),
        ((0, 0, 3, 3), 0),
        ((0, 2, 3), 0),
        ((2, 3), 1),
        ((0, 0, 2, 3), 0),
    ]:
        adj = graph(ps, m)
        actual, states = exact(adj)
        print("example", ps, m, "vertices", len(adj), "grundy", actual, "states", states)
        assert actual == predicted(ps, m)


if __name__ == "__main__":
    main()
