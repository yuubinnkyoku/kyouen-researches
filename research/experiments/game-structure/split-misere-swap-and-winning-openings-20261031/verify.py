#!/usr/bin/env python3
"""Independent named-vertex audit for misere Node Kayles on split graphs."""
from functools import lru_cache
from itertools import product
from random import Random


def audit(k, signatures, full_audit=False):
    m = len(signatures)
    n = k + m
    closed = [1 << i for i in range(n)]
    for i in range(k):
        closed[i] |= (1 << k) - 1
    for j, s in enumerate(signatures):
        assert 0 <= s < 1 << k
        for i in range(k):
            if s >> i & 1:
                closed[i] |= 1 << (k + j)
                closed[k + j] |= 1 << i

    seen_masks = set()

    @lru_cache(None)
    def value(mask, terminal):
        seen_masks.add(mask)
        if not mask:
            return terminal
        seen = {value(mask & ~closed[i], terminal)
                for i in range(n) if mask >> i & 1}
        v = 0
        while v in seen:
            v += 1
        return v

    root = (1 << n) - 1
    normal = value(root, 0)
    misere = value(root, 1)
    assert misere == {0: 1, 1: 0}.get(normal, normal), (k, signatures, normal, misere)
    degrees = [sum(s >> i & 1 for s in signatures) for i in range(k)]
    predicted = set()
    for i in range(k):
        if (degrees[i] - m) % 2:
            predicted.add(i)
    full = (1 << k) - 1
    for j, s in enumerate(signatures):
        t = full ^ s
        if m % 2 == 0:
            if all((degrees[i] & 1) == 1 for i in range(k) if t >> i & 1):
                predicted.add(k + j)
        else:
            if t and all((degrees[i] & 1) == 0 for i in range(k) if t >> i & 1) \
                    and not any((s | other) == full for z, other in enumerate(signatures) if z != j):
                predicted.add(k + j)
    actual = {i for i in range(n) if value(root & ~closed[i], 1) == 0}
    assert actual == predicted, (k, signatures, normal, misere, actual, predicted)
    if full_audit:
        for mask in tuple(seen_masks):
            g = value(mask, 0)
            h = value(mask, 1)
            assert h == {0: 1, 1: 0}.get(g, g), (k, signatures, mask, g, h)
    return normal, misere, len(actual)


def main():
    count = 0
    by_normal = {}
    for k in range(5):
        for m in range(5):
            for sigs in product(range(1 << k), repeat=m):
                g, h, _ = audit(k, sigs)
                count += 1
                by_normal[g] = by_normal.get(g, 0) + 1
        print('complete', k, count, flush=True)
    rng = Random(20261031)
    for k in range(1, 10):
        for m in range(5, 12):
            for _ in range(8):
                audit(k, tuple(rng.randrange(1 << k) for _ in range(m)))
                count += 1
    assert audit(7, (3, 3, 5, 5, 9, 9, 33, 48, 80), full_audit=True)[:2] == (5, 5)
    assert audit(7, (3, 3, 4, 4, 5, 9, 9, 16, 33, 33, 64, 64, 68, 80, 84), full_audit=True)[:2] == (8, 8)
    count += 2

    # Out-of-class counterexample: two disjoint P3 stars, g=h=0.
    edges = [(0, 4), (0, 5), (1, 2), (1, 3)]
    adj = [1 << i for i in range(6)]
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    @lru_cache(None)
    def general(mask, terminal):
        if not mask:
            return terminal
        options = {general(mask & ~adj[i], terminal)
                   for i in range(6) if mask >> i & 1}
        r = 0
        while r in options:
            r += 1
        return r

    assert (general(63, 0), general(63, 1)) == (0, 0)
    print('OK', count, 'split root graphs; normal distribution complete', by_normal)
    print('Non-split boundary: 2P3 has (g,h)=(0,0)')


if __name__ == '__main__':
    main()
