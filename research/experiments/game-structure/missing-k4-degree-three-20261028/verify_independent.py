#!/usr/bin/env python3
"""Independent Python quotient check and named-vertex audit of all 25 exceptions."""
from functools import lru_cache
from itertools import combinations
from collections import Counter

K = 5
EDGES = tuple(combinations(range(K), 2))
MISSING = {(a, b) for a in range(4) for b in range(a + 1, 4)}
PRESENT = tuple(e for e in EDGES if e not in MISSING)


def formula(t, pairs):
    u = (sum(t) + sum(pairs.values())) % 2
    z = [(t[i] + sum(c for e, c in pairs.items() if i in e)) % 2
         for i in range(K)]
    return (1 ^ u ^ z[0]) if len(set(z)) == 1 else 2 + u


def quotient(t, pairs):
    types = [(1 << i, c) for i, c in enumerate(t) if c]
    types += [((1 << a) | (1 << b), c)
              for (a, b), c in pairs.items() if c]
    parity = [sum(c & 1 for sig, c in types if sig & x) % 2
              for x in range(1 << K)]

    @lru_cache(None)
    def g(x):
        if not x:
            return 0
        children = set()
        for i in range(K):
            if x & (1 << i):
                children.add(sum(c for sig, c in types
                                 if sig & x and not sig & (1 << i)) % 2)
        for sig, c in types:
            if sig & x:
                y = x & ~sig
                children.add(g(y) ^ parity[x] ^ parity[y] ^ 1)
        return next(v for v in range(32) if v not in children)
    return g((1 << K) - 1)


def named(t, pairs):
    k = len(t)
    edges = tuple(combinations(range(k), 2))
    n = k + sum(t) + sum(pairs.values())
    adj = [0] * n
    for i, j in edges:
        adj[i] |= 1 << j
        adj[j] |= 1 << i
    v = k
    for i, c in enumerate(t):
        for _ in range(c):
            adj[i] |= 1 << v
            adj[v] = 1 << i
            v += 1
    for (a, b), c in pairs.items():
        for _ in range(c):
            adj[a] |= 1 << v
            adj[b] |= 1 << v
            adj[v] = (1 << a) | (1 << b)
            v += 1
    assert v == n

    @lru_cache(None)
    def g(x):
        if x == 0:
            return 0
        children = set()
        y = x
        while y:
            bit = y & -y
            i = bit.bit_length() - 1
            y -= bit
            children.add(g(x & ~(bit | adj[i])))
        return next(v for v in range(32) if v not in children)
    return g((1 << n) - 1)


def main():
    actual = Counter()
    failures = Counter()
    named_checks = 0
    for code in range(3**K):
        x = code
        t = []
        for _ in range(K):
            t.append(x % 3)
            x //= 3
        for bits in range(1 << len(PRESENT)):
            pairs = {e: 1 + ((bits >> j) & 1)
                     for j, e in enumerate(PRESENT)}
            g = quotient(t, pairs)
            want = formula(t, pairs)
            actual[g] += 1
            if g != want:
                failures[(g, want)] += 1
                assert named(t, pairs) == g
                named_checks += 1
                assert sum(v > 0 for v in t[:4]) <= 1
    print("star representatives:", sum(actual.values()))
    print("star Grundy distribution:", dict(sorted(actual.items())))
    print("star formula exceptions:", sum(failures.values()),
          dict(sorted(failures.items())))
    print("all exceptions named-vertex verified:", named_checks)
    assert sum(actual.values()) == 3**5 * 2**4 == 3888
    assert sum(failures.values()) == named_checks == 25
    assert failures == Counter({(2, 3): 5, (3, 2): 8,
                                (4, 2): 4, (4, 3): 8})
    # Independent named-vertex check of all 64 binary leaf assignments at k=6,
    # with exactly one copy of each of the nine present pair types.
    edges6 = tuple(combinations(range(6), 2))
    pairs6 = {e: 1 for e in edges6 if not (e[0] < 4 and e[1] < 4)}
    for bits in range(64):
        leaves6 = [(bits >> i) & 1 for i in range(6)]
        u = (sum(leaves6) + sum(pairs6.values())) & 1
        z = [(leaves6[i] + sum(c for e, c in pairs6.items() if i in e)) & 1
             for i in range(6)]
        want = (1 ^ u ^ z[0]) if len(set(z)) == 1 else 2 + u
        assert named(leaves6, pairs6) == want
    print("k6 named-vertex binary-leaf cases:", 64)


if __name__ == "__main__":
    main()
