#!/usr/bin/env python3
"""Independent checks of the even-pair-incidence Grundy formula."""
from functools import cache
from itertools import product
from random import Random

def mex(values):
    seen = set(values)
    return next(x for x in range(len(seen) + 1) if x not in seen)

def formula(leaves):
    k = len(leaves)
    b = sum(t & 1 for t in leaves)
    if k == 0:
        return 0
    if k == 1:
        return 1 if leaves[0] == 0 or b else 2
    if k == 2:
        return (2, 3, 0)[b]
    if b == 0:
        return 1
    if b == k:
        return k & 1
    return 3 if b & 1 else 2

def signatures(leaves, pairs):
    k = len(leaves)
    result = [1 << i for i, t in enumerate(leaves) for _ in range(t)]
    result += [(1 << i) | (1 << j)
               for i in range(k) for j in range(i + 1, k)
               for _ in range(pairs[i][j])]
    return result

def split_dp(leaves, pairs):
    # Enumerate all active-clique subsets, independently of the formula.
    k = len(leaves)
    types = signatures(leaves, pairs)
    parity = [sum(bool(s & x) for s in types) & 1 for x in range(1 << k)]
    values = [0] * (1 << k)
    for x in range(1, 1 << k):
        children = set()
        for i in range(k):
            if x >> i & 1:
                children.add(sum(not (s & (1 << i)) for s in types if s & x) & 1)
        for s in set(types):
            if s & x:
                y = x & ~s
                children.add(values[y] ^ parity[x] ^ parity[y] ^ 1)
        values[x] = mex(children)
    return values[-1]

def named_vertex_dp(leaves, pairs):
    # Separate solver: construct named vertices and remove closed neighborhoods.
    k = len(leaves)
    neighbors = [set(range(k)) - {i} for i in range(k)]
    for s in signatures(leaves, pairs):
        v = len(neighbors)
        neighbors.append(set())
        for i in range(k):
            if s >> i & 1:
                neighbors[v].add(i)
                neighbors[i].add(v)
    closed = [sum(1 << j for j in ns | {i}) for i, ns in enumerate(neighbors)]

    @cache
    def grundy(mask):
        seen = set()
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            v = bit.bit_length() - 1
            seen.add(grundy(mask & ~closed[v]))
        return mex(seen)

    return grundy((1 << len(neighbors)) - 1), grundy.cache_info().currsize

def uniform_pairs(k, r):
    return [[r if j > i else 0 for j in range(k)] for i in range(k)]

def main():
    exhaustive = 0
    for k in range(8):
        pairs = uniform_pairs(k, 2)
        for leaves in product(range(3), repeat=k):
            got = split_dp(leaves, pairs)
            want = formula(leaves)
            assert got == want, ('exhaustive', k, leaves, got, want)
            exhaustive += 1
    print('uniform pair multiplicity 2, all t_i=0/1/2, k<=7:', exhaustive, 'OK')

    rng = Random(20261028)
    sampled = 0
    for k in range(1, 9):
        for _ in range(120):
            leaves = tuple(rng.randrange(6) for _ in range(k))
            pairs = [[2 * rng.randint(1, 3) if j > i else 0
                      for j in range(k)] for i in range(k)]
            got = split_dp(leaves, pairs)
            want = formula(leaves)
            assert got == want, ('nonuniform', k, leaves, pairs, got, want)
            sampled += 1
    print('nonuniform positive even pair multiplicities:', sampled, 'OK')

    named = states = 0
    for k in range(5):
        for leaves in product(range(3), repeat=k):
            pairs = uniform_pairs(k, 2)
            n = k + sum(leaves) + k * (k - 1)
            if n > 17:
                continue
            got, visited = named_vertex_dp(leaves, pairs)
            want = formula(leaves)
            assert got == want, ('named', k, leaves, got, want)
            named += 1
            states += visited
    for k in range(2, 5):
        for _ in range(50):
            leaves = tuple(rng.randrange(3) for _ in range(k))
            pairs = [[2 * rng.randint(1, 2) if j > i else 0
                      for j in range(k)] for i in range(k)]
            n = k + sum(leaves) + sum(sum(row) for row in pairs)
            if n > 17:
                continue
            got, visited = named_vertex_dp(leaves, pairs)
            want = formula(leaves)
            assert got == want, ('named nonuniform', k, leaves, got, want)
            named += 1
            states += visited
    print('named-vertex closed-neighborhood recursion:', named, 'graphs,', states, 'memo states, OK')

if __name__ == '__main__':
    main()
