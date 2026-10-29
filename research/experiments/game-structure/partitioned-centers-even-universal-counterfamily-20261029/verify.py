#!/usr/bin/env python3
"""Independent named-vertex Node Kayles audit for a partitioned-clique family."""
from functools import lru_cache


def named_grundy(a, b, universal, private_counts=None, group_counts=(1, 1), universal_count=2):
    """Build every named vertex and recurse by deleting closed neighborhoods."""
    n = a + b
    if private_counts is None:
        private_counts = [1] * n
    supports = []
    for i, count in enumerate(private_counts):
        supports.extend([1 << i] * count)
    supports.extend([(1 << a) - 1] * group_counts[0])
    supports.extend([((1 << b) - 1) << a] * group_counts[1])
    if universal:
        supports.extend([(1 << n) - 1] * universal_count)

    adj = [0] * (n + len(supports))
    for c in range(n):
        adj[c] = ((1 << n) - 1) ^ (1 << c)
    for j, support in enumerate(supports, n):
        for c in range(n):
            if support & (1 << c):
                adj[j] |= 1 << c
                adj[c] |= 1 << j
    closed = [adj[i] | (1 << i) for i in range(len(adj))]

    @lru_cache(None)
    def grundy(remaining):
        options = set()
        todo = remaining
        while todo:
            low = todo & -todo
            todo -= low
            vertex = low.bit_length() - 1
            options.add(grundy(remaining & ~closed[vertex]))
        g = 0
        while g in options:
            g += 1
        return g

    full = (1 << len(adj)) - 1
    value = grundy(full)
    root_options = sorted({grundy(full & ~closed[i]) for i in range(len(adj))})
    return value, root_options, grundy.cache_info().currsize


def p(a, b):
    return (a + b + (a > 0) + (b > 0)) & 1


@lru_cache(None)
def quotient(a, b, universal):
    """Separate two-count recurrence, with isolated vertices factored by xor."""
    if not a and not b:
        return 0
    parity = p(a, b)
    options = {parity}
    if a:
        options.add(quotient(a - 1, b, universal) ^ parity ^ p(a - 1, b) ^ 1)
        options.add(quotient(0, b, universal) ^ parity ^ p(0, b) ^ 1)
    if b:
        options.add(quotient(a, b - 1, universal) ^ parity ^ p(a, b - 1) ^ 1)
        options.add(quotient(a, 0, universal) ^ parity ^ p(a, 0) ^ 1)
    if universal:
        options.add(parity ^ 1)
    g = 0
    while g in options:
        g += 1
    return g


def main():
    checked = 0
    for n in range(2, 13):
        for a in range(1, n):
            b = n - a
            for universal in (False, True):
                g, moves, states = named_grundy(a, b, universal)
                expected = (2 + (n & 1)) if universal else (1 - (n & 1))
                assert g == expected, (a, b, universal, g, expected)
                assert g == quotient(a, b, universal), (a, b, universal, g)
                checked += 1
                if (a, b) == (2, 3):
                    assert moves == ([0, 1, 2] if universal else [1, 2])
    print('PASS named-vertex and quotient checks:', checked, 'root positions')

    extended = 0
    # Multiplicity tests exercise the parity-compression extension directly.
    for a, b in [(2, 2), (2, 3), (3, 2), (3, 3)]:
        n = a + b
        private_counts = [1 + 2 * (i & 1) for i in range(n)]
        group_counts = (3, 3) if n <= 5 else (1, 1)
        universal_count = 4 if n <= 5 else 2
        for universal in (False, True):
            g, _, _ = named_grundy(
                a, b, universal, private_counts=private_counts,
                group_counts=group_counts, universal_count=universal_count,
            )
            expected = (2 + (n & 1)) if universal else (1 - (n & 1))
            assert g == expected, (a, b, universal, g, expected)
            extended += 1
    print('PASS varied odd multiplicities and positive even universal count:', extended)
    print('PASS total:', checked + extended)


if __name__ == '__main__':
    main()
