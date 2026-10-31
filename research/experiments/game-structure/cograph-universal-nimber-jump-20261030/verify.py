#!/usr/bin/env python3
"""Independent exact Node Kayles verifier: universal-vertex nimber jumps.

Uses labeled adjacency masks and closed-neighborhood deletion, not the
cotree option-set recurrence used in the mathematical proof.
"""
from functools import lru_cache


def disjoint(a, b):
    n = len(a)
    return a + tuple(x << n for x in b)


def join(a, b):
    n, m = len(a), len(b)
    return (tuple(x | (((1 << m) - 1) << n) for x in a)
            + tuple((x << n) | ((1 << n) - 1) for x in b))


def construct(p):
    a, b = (0,), ()
    for _ in range(p):
        b = join(b, disjoint(a, a))
        a = join(b, (0,))
    return a, b


def options_and_grundy(graph):
    n = len(graph)
    assert all(not (row & (1 << i)) for i, row in enumerate(graph))
    assert all(bool(graph[i] & (1 << j)) == bool(graph[j] & (1 << i))
               for i in range(n) for j in range(i))

    @lru_cache(None)
    def grundy(mask):
        options = set()
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            v = bit.bit_length() - 1
            options.add(grundy(mask & ~(graph[v] | bit)))
        mex = 0
        while mex in options:
            mex += 1
        return mex

    full = (1 << n) - 1
    option_set = {grundy(full & ~(graph[v] | (1 << v))) for v in range(n)}
    return option_set, grundy(full), grundy.cache_info().currsize


def verify_family(max_p=4):
    for p in range(max_p + 1):
        a, b = construct(p)
        assert len(a) == 3**p and len(b) == 3**p - 1
        for label, graph, expected in (
            ('B', b, set(range(1, 2**p))),
            ('A', a, set(range(2**p))),
        ):
            options, value, states = options_and_grundy(graph)
            assert options == expected, (p, label, options, expected)
            assert value == (0 if label == 'B' else 2**p)
            print(f'p={p} {label}: vertices={len(graph)}, g={value}, '
                  f'option_count={len(options)}, memo_states={states}')


def verify_universal_small_graphs():
    total = 0
    for n in range(6):
        edges = [(i, j) for i in range(n) for j in range(i)]
        for mask in range(1 << len(edges)):
            rows = [0] * n
            for k, (i, j) in enumerate(edges):
                if mask & (1 << k):
                    rows[i] |= 1 << j
                    rows[j] |= 1 << i
            graph = tuple(rows)
            options, g, _ = options_and_grundy(graph)
            new_options, new_g, _ = options_and_grundy(join(graph, (0,)))
            assert new_options == options | {0}
            expected = g if g > 0 else next(
                x for x in range(1, n + 3) if x not in options)
            assert new_g == expected, (n, mask, g, new_g, expected)
            total += 1
    print(f'universal addition: {total} labeled graphs, no mismatches')


if __name__ == '__main__':
    verify_family()
    verify_universal_small_graphs()
    print('PASS')
