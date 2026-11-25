#!/usr/bin/env python3
"""Independent named-vertex and multiplicity-quotient Node Kayles checks."""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, product
from random import Random


def graph(leaves, pairs):
    h = len(leaves)
    adj = [((1 << h) - 1) ^ (1 << i) for i in range(h)]

    def add(neighbors):
        j = len(adj)
        adj.append(0)
        for i in neighbors:
            adj[i] |= 1 << j
            adj[j] |= 1 << i

    for i, count in enumerate(leaves):
        for _ in range(count):
            add((i,))
    for (i, j), count in pairs.items():
        for _ in range(count):
            add((i, j))
    return tuple(x | (1 << i) for i, x in enumerate(adj))


def named_value(closed):
    @lru_cache(None)
    def g(mask):
        rem, seen = mask, 0
        while rem:
            bit = rem & -rem
            rem -= bit
            i = bit.bit_length() - 1
            seen |= 1 << g(mask & ~closed[i])
        mex = 0
        while (seen >> mex) & 1:
            mex += 1
        return mex

    full = (1 << len(closed)) - 1
    result = g(full)
    child_set = frozenset(g(full & ~x) for x in closed)
    return result, child_set, g.cache_info().currsize


def quotient_value(leaves, pairs):
    """No named independent vertices: state counts neighbor masks."""
    h = len(leaves)
    counts = [0] * (1 << h)
    for i, n in enumerate(leaves):
        counts[1 << i] += n
    for (i, j), n in pairs.items():
        counts[(1 << i) | (1 << j)] += n

    @lru_cache(None)
    def g(k, state):
        if k == 0:
            return state[0] & 1
        options = set()
        full = (1 << k) - 1
        for i in range(k):
            # Choosing a clique vertex removes the entire clique.
            options.add(sum(n for typ, n in enumerate(state)
                            if not (typ & (1 << i))) & 1)
        for support, n in enumerate(state):
            if not n:
                continue
            if support == 0:
                nxt = list(state)
                nxt[0] -= 1
                options.add(g(k, tuple(nxt)))
                continue
            surviving = [i for i in range(k) if not (support >> i) & 1]
            nxt = [0] * (1 << len(surviving))
            for typ, count in enumerate(state):
                if count:
                    new_typ = sum(1 << pos for pos, i in enumerate(surviving)
                                  if (typ >> i) & 1)
                    nxt[new_typ] += count
            nxt[0] -= 1  # The selected independent point is now isolated.
            options.add(g(len(surviving), tuple(nxt)))
        mex = 0
        while mex in options:
            mex += 1
        return mex

    return g(h, tuple(counts))


def main():
    pairs3 = tuple(combinations(range(3), 2))
    histogram = Counter()
    child_sets = defaultdict(set)
    max_states = 0

    for counts in product(range(3), repeat=3):
        edges = dict(zip(pairs3, counts))
        value, children, states = named_value(graph((1, 1, 1), edges))
        independently = quotient_value((1, 1, 1), edges)
        e = sum(x & 1 for x in counts)
        assert value == independently == (1 + e) % 4, (counts, value)
        histogram[e] += 1
        child_sets[e].add(tuple(sorted(children)))
        max_states = max(max_states, states)

    assert histogram == Counter({0: 8, 1: 12, 2: 6, 3: 1})
    assert dict(child_sets) == {
        0: {(0,)}, 1: {(0, 1, 3)},
        2: {(0, 1, 2)}, 3: {(1,)}
    }

    pairs4 = tuple(combinations(range(4), 2))
    hist4 = Counter()
    two_edge_values = set()
    for counts in product(range(2), repeat=6):
        edges = dict(zip(pairs4, counts))
        value, _, states = named_value(graph((1, 1, 1, 1), edges))
        assert value == quotient_value((1, 1, 1, 1), edges)
        hist4[value] += 1
        if sum(counts) == 2:
            two_edge_values.add(value)
        max_states = max(max_states, states)
    assert hist4 == Counter({0: 8, 1: 8, 2: 24, 3: 24})
    assert two_edge_values == {1, 2}

    rng = Random(20261029)
    for _ in range(80):
        leaves = tuple(rng.choice((1, 3)) for _ in range(3))
        counts = tuple(rng.randrange(4) for _ in range(3))
        edges = dict(zip(pairs3, counts))
        value, _, states = named_value(graph(leaves, edges))
        assert value == quotient_value(leaves, edges)
        assert value == (1 + sum(x & 1 for x in counts)) % 4
        max_states = max(max_states, states)

    print("3-center canonical cases:", sum(histogram.values()), dict(histogram))
    print("3-center child nimbers:", dict(child_sets))
    print("4-center simple graphs:", sum(hist4.values()), dict(hist4))
    print("4-center two-edge values:", sorted(two_edge_values))
    print("nonuniform checks: 80; total: 171")
    print("maximum named states:", max_states)
    print("PASS")


if __name__ == "__main__":
    main()
