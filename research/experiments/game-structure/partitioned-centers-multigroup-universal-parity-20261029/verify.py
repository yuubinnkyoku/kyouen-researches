#!/usr/bin/env python3
"""Independent named-vertex Node Kayles and count-state recursion checks."""
from functools import lru_cache
from itertools import product


def mex(values):
    seen = set(values)
    x = 0
    while x in seen:
        x += 1
    return x


def named_grundy(counts, universal=0, private_mult=1, group_mult=1):
    assert all(x > 0 for x in counts)
    assert universal >= 0
    n = sum(counts)
    adj = [0] * n

    def add(neighbors):
        v = len(adj)
        adj.append(0)
        for w in neighbors:
            adj[v] |= 1 << w
            adj[w] |= 1 << v

    for i in range(n):
        adj[i] |= ((1 << n) - 1) ^ (1 << i)
        for _ in range(private_mult):
            add([i])
    offset = 0
    for sz in counts:
        for _ in range(group_mult):
            add(range(offset, offset + sz))
        offset += sz
    for _ in range(universal):
        add(range(n))
    closed = [adj[v] | (1 << v) for v in range(len(adj))]

    @lru_cache(None)
    def rec(mask):
        options = []
        pending = mask
        while pending:
            bit = pending & -pending
            v = bit.bit_length() - 1
            pending ^= bit
            options.append(rec(mask & ~closed[v]))
        return mex(options)

    return rec((1 << len(adj)) - 1)


@lru_cache(None)
def quotient(universal, counts):
    n = sum(counts)
    if n == 0:
        return 0

    def parity(c):
        return ((sum(c) + sum(x > 0 for x in c) + (universal & 1)) & 1) if any(c) else 0

    p = parity(counts)
    options = [p ^ (universal & 1)]  # any center: private + group + universal
    for j, x in enumerate(counts):
        if x == 0:
            continue
        one = list(counts)
        one[j] -= 1
        one = tuple(one)
        options.append(quotient(universal, one) ^ p ^ parity(one) ^ 1)
        whole = list(counts)
        whole[j] = 0
        whole = tuple(whole)
        options.append(quotient(universal, whole) ^ p ^ parity(whole) ^ 1)
    if universal:
        options.append(p ^ 1)
    return mex(options)


def expected(counts, universal):
    active = sum(x > 0 for x in counts)
    n = sum(counts)
    if active == 0:
        return 0
    p = (n + active) & 1
    if active == 1:
        return (1 - p) if universal & 1 else (2 + p)
    return (2 + p) if universal > 0 and universal % 2 == 0 else (1 - p)


def compositions(n):
    for bits in range(1 << (n - 1)):
        result = []
        last = 0
        for j in range(n - 1):
            if bits >> j & 1:
                result.append(j + 1 - last)
                last = j + 1
        result.append(n - last)
        yield tuple(result)


def main():
    named = 0
    quot = 0
    for n in range(1, 10):
        for counts in compositions(n):
            for u in (0, 1, 2):
                predicted = expected(counts, u)
                q = quotient(u, counts)
                assert q == predicted, (counts, u, q, predicted)
                quot += 1
                if n <= 7 or (n == 8 and u != 1):
                    direct = named_grundy(counts, u)
                    assert direct == predicted, (counts, u, direct, predicted)
                    named += 1
    # Exercise the boundary and the induction with zero-count groups.
    for k in range(1, 7):
        for counts in product(range(4), repeat=k):
            if sum(counts) > 9:
                continue
            for u in (0, 1, 2):
                assert quotient(u, counts) == expected(counts, u), (counts, u)
                quot += 1
    # Distinct named vertices and higher odd/even multiplicities, not the quotient.
    varied = 0
    for counts in ((1, 1), (2, 1), (1, 1, 1), (2, 1, 2)):
        for private_mult, group_mult, universal in ((3, 1, 2), (1, 3, 4), (1, 1, 3)):
            actual = named_grundy(counts, universal, private_mult, group_mult)
            assert actual == expected(counts, universal), (counts, private_mult, group_mult, universal, actual)
            varied += 1
    print(f"PASS named_vertex_roots={named}, varied_multiplicity={varied}, quotient_states={quot}")


if __name__ == "__main__":
    main()
