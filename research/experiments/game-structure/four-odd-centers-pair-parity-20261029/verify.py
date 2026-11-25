#!/usr/bin/env python3
"""Two independent exact Node Kayles solvers; four odd-center classification."""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, permutations, product
from random import Random

EDGES = tuple(combinations(range(4), 2))

def canonical(counts):
    images = []
    for p in permutations(range(4)):
        d = {tuple(sorted((p[i], p[j]))): n
             for (i, j), n in zip(EDGES, counts)}
        images.append(tuple(d[e] for e in EDGES))
    return min(images)

def named(leaves, counts):
    adj = [15 ^ (1 << i) for i in range(4)]
    def add(neighbors):
        v = len(adj)
        adj.append(0)
        for i in neighbors:
            adj[i] |= 1 << v
            adj[v] |= 1 << i
    for i, n in enumerate(leaves):
        for _ in range(n):
            add((i,))
    for (i, j), n in zip(EDGES, counts):
        for _ in range(n):
            add((i, j))
    closed = tuple(a | (1 << i) for i, a in enumerate(adj))
    @lru_cache(None)
    def direct(mask):
        rem, options = mask, set()
        while rem:
            bit = rem & -rem
            rem -= bit
            i = bit.bit_length() - 1
            options.add(direct(mask & ~closed[i]))
        mex = 0
        while mex in options:
            mex += 1
        return mex
    return direct((1 << len(closed)) - 1), direct.cache_info().currsize

@lru_cache(None)
def quotient_g(k, state):
    if k == 0:
        return state[0] & 1
    options = set()
    for i in range(k):
        options.add(sum(n for s, n in enumerate(state) if not(s >> i & 1)) & 1)
    for support, n in enumerate(state):
        if not n:
            continue
        remaining = [i for i in range(k) if not(support >> i & 1)]
        nxt = [0] * (1 << len(remaining))
        for typ, count in enumerate(state):
            mapped = sum(1 << j for j, i in enumerate(remaining) if typ >> i & 1)
            nxt[mapped] += count
        nxt[0] -= 1
        options.add(quotient_g(len(remaining), tuple(nxt)))
    mex = 0
    while mex in options:
        mex += 1
    return mex

def quotient(leaves, counts):
    state = [0] * 16
    for i, n in enumerate(leaves):
        state[1 << i] += n
    for (i, j), n in zip(EDGES, counts):
        state[(1 << i) | (1 << j)] += n
    return quotient_g(4, tuple(state))

def main():
    hist, orbits = Counter(), defaultdict(set)
    max_states = 0
    cases = list(product(range(3), repeat=6))
    for c in cases:
        a, states = named((1,)*4, c)
        b = quotient((1,)*4, c)
        assert a == b, (c, a, b)
        assert b == quotient((1,)*4, tuple(n & 1 for n in c)), c
        hist[a] += 1
        orbits[canonical(c)].add(a)
        max_states = max(max_states, states)
    assert len(orbits) == 66 and all(len(s) == 1 for s in orbits.values())
    assert hist == Counter({0:108, 1:81, 2:240, 3:300}), hist

    classes = defaultdict(list)
    for c in product(range(2), repeat=6):
        classes[canonical(c)].append(c)
    expected = {
        "000000": (1,0), "000001": (6,3),
        "000011": (12,2), "001100": (3,1),
        "000111": (4,1), "001011": (4,0),
        "001101": (12,3), "001111": (12,2),
        "011110": (3,0), "011111": (6,3),
        "111111": (1,1)
    }
    assert len(classes) == 11
    for rep, labelled in classes.items():
        assert (len(labelled), quotient((1,)*4, rep)) == expected[''.join(map(str, rep))]

    rng = Random(20261029)
    for _ in range(60):
        while True:
            leaves = tuple(rng.choice((1,3,5)) for _ in range(4))
            c = tuple(rng.randrange(6) for _ in range(6))
            if 4 + sum(leaves) + sum(c) <= 17:
                break
        a, states = named(leaves, c)
        b = quotient(leaves, c)
        reduced = quotient((1,)*4, tuple(n & 1 for n in c))
        assert a == b == reduced, (leaves, c, a, b, reduced)
        max_states = max(max_states, states)
    print("PASS: 729/729 bases, 66/66 ternary orbits, 11/11 simple classes")
    print("PASS: even-positive -> zero for every base; 60/60 nonuniform samples")
    print("Grundy histogram:", dict(sorted(hist.items())))
    print("Max named states:", max_states, "quotient states:", quotient_g.cache_info().currsize)
    for rep, labelled in sorted(classes.items(), key=lambda kv:(sum(kv[0]),kv[0])):
        print(''.join(map(str,rep)),len(labelled),quotient((1,)*4,rep))

if __name__ == "__main__":
    main()
