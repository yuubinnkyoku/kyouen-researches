#!/usr/bin/env python3
"""Labelled-subset vs symmetric count-vector game audit (stdlib only)."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from math import comb, factorial, prod
from random import Random


def subsets(n, low=2):
    return tuple(x for x in range(1, 1 << n) if x.bit_count() >= low)


def exchangeable_classes(n, edges):
    f = frozenset(edges)
    parent = list(range(n))
    def root(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for u in range(n):
        for v in range(u + 1, n):
            bitu, bitv = 1 << u, 1 << v
            def swap(e):
                return e ^ (bitu | bitv) if bool(e & bitu) != bool(e & bitv) else e
            if all(swap(e) in f for e in f):
                parent[root(v)] = root(u)
    out = {}
    for v in range(n):
        out.setdefault(root(v), []).append(v)
    return tuple(tuple(c) for c in out.values())


def labelled(n, edges):
    @lru_cache(None)
    def safe(mask):
        return all(mask & e != e for e in edges)
    @lru_cache(None)
    def grundy(mask):
        children = {grundy(mask | (1 << v)) for v in range(n)
                    if not (mask >> v) & 1 and safe(mask | (1 << v))}
        g = 0
        while g in children:
            g += 1
        return g
    spectrum = Counter()
    for mask in range(1 << n):
        if not safe(mask):
            continue
        legal = [v for v in range(n) if not (mask >> v) & 1 and safe(mask | (1 << v))]
        if not legal:
            spectrum[mask.bit_count()] += 1
        grundy(mask)
    return safe, grundy, spectrum


def quotient(n, edges, classes):
    ks = tuple(map(len, classes))
    profiles = set()
    for e in edges:
        profiles.add(tuple(sum(bool(e & (1 << v)) for v in c) for c in classes))
    @lru_cache(None)
    def safe(a):
        return all(not all(ai >= pi for ai, pi in zip(a, p)) for p in profiles)
    @lru_cache(None)
    def grundy(a):
        children = set()
        for i in range(len(ks)):
            if a[i] == ks[i]:
                continue
            b = a[:i] + (a[i] + 1,) + a[i + 1:]
            if safe(b):
                children.add(grundy(b))
        g = 0
        while g in children:
            g += 1
        return g
    spectrum = Counter()
    for a in product(*(range(k + 1) for k in ks)):
        if not safe(a):
            continue
        has_move = False
        for i, k in enumerate(ks):
            if a[i] < k and safe(a[:i] + (a[i] + 1,) + a[i + 1:]):
                has_move = True
                break
        if not has_move:
            spectrum[sum(a)] += prod(comb(k, ai) for k, ai in zip(ks, a))
        grundy(a)
    return safe, grundy, spectrum


def verify(n, edges):
    classes = exchangeable_classes(n, edges)
    s0, g0, p0 = labelled(n, edges)
    s1, g1, p1 = quotient(n, edges, classes)
    assert p0 == p1, (n, edges, classes, p0, p1)
    assert sum(factorial(k) * v for k, v in p0.items()) == sum(factorial(k) * v for k, v in p1.items())
    for mask in range(1 << n):
        a = tuple(sum(bool(mask & (1 << v)) for v in c) for c in classes)
        assert s0(mask) == s1(a), (n, edges, classes, mask)
        if s0(mask):
            assert g0(mask) == g1(a), (n, edges, classes, mask, g0(mask), g1(a))
    return len(classes) < n


def planted(rng, ks):
    n = sum(ks)
    classes = []
    off = 0
    for k in ks:
        classes.append(list(range(off, off + k)))
        off += k
    all_profiles = [p for p in product(*(range(k + 1) for k in ks)) if 2 <= sum(p) <= 4]
    chosen = [p for p in all_profiles if rng.randrange(5) == 0]
    edges = set()
    for p in chosen:
        for blocks in product(*(combinations(c, t) for c, t in zip(classes, p))):
            mask = sum(1 << v for b in blocks for v in b)
            edges.add(mask)
    return n, tuple(edges)


def main():
    rng = Random(20261020)
    exhaustive = planted_count = random_count = reduced = 0
    for n in range(1, 5):
        candidates = subsets(n)
        for family in range(1 << len(candidates)):
            edges = tuple(e for i, e in enumerate(candidates) if family >> i & 1)
            reduced += verify(n, edges)
            exhaustive += 1
    for ks in [(3, 2), (4, 2), (3, 3), (3, 2, 2), (4, 3), (3, 3, 2), (4, 3, 2)]:
        for _ in range(45):
            n, edges = planted(rng, ks)
            reduced += verify(n, edges)
            planted_count += 1
    for _ in range(400):
        n = rng.randrange(2, 9)
        edges = tuple(e for e in subsets(n) if e.bit_count() <= 4 and rng.randrange(10) == 0)
        reduced += verify(n, edges)
        random_count += 1
    blocks = []
    offset = 0
    for k in (3, 4, 5, 6):
        blocks.append(range(offset, offset + k))
        offset += k
    edges = tuple((1 << u) | (1 << v)
                  for i in range(3) for u in blocks[i] for v in blocks[i + 1])
    _, brute_g, brute_p = labelled(18, edges)
    assert brute_g(0) == 0 and dict(brute_p) == {8: 1, 9: 1, 10: 1}
    print(f'PASS exhaustive={exhaustive} planted={planted_count} random={random_count} total={exhaustive+planted_count+random_count} nontrivial_quotients={reduced}')
    print('PASS independent 18-point P4 blow-up: grundy=0 spectrum={8:1,9:1,10:1}')


if __name__ == '__main__':
    main()
