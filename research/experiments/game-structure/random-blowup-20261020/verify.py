#!/usr/bin/env python3
"""Exact independent audits of random greedy play on independent-set blowups."""
from collections import defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from random import Random


def class_law(sizes, edges, weights):
    d = len(sizes)
    offsets = [sum(sizes[:i]) for i in range(d)]
    rate = [sum(weights[offsets[i]:offsets[i] + sizes[i]]) for i in range(d)]
    closed = [1 << i for i in range(d)]
    for i, j in edges:
        closed[i] |= 1 << j
        closed[j] |= 1 << i
    @lru_cache(None)
    def go(mask):
        if mask == 0:
            return {0: Q(1)}
        total = sum(rate[i] for i in range(d) if mask >> i & 1)
        ans = defaultdict(Q)
        for i in range(d):
            if mask >> i & 1:
                for chosen, p in go(mask & ~closed[i]).items():
                    ans[chosen | (1 << i)] += Q(rate[i], total) * p
        return dict(ans)
    return {tuple(sizes[i] if chosen >> i & 1 else 0 for i in range(d)): p
            for chosen, p in go((1 << d) - 1).items()}


def labelled_law(sizes, edges, weights):
    d = len(sizes)
    n = sum(sizes)
    offsets = [sum(sizes[:i]) for i in range(d)]
    group = [i for i, k in enumerate(sizes) for _ in range(k)]
    conflict = [0] * n
    for v in range(n):
        for u in range(n):
            if (group[v], group[u]) in edges or (group[u], group[v]) in edges:
                conflict[v] |= 1 << u
    @lru_cache(None)
    def go(occupied):
        moves = [v for v in range(n) if not (occupied >> v & 1)
                 and not (occupied & conflict[v])]
        if not moves:
            vec = tuple(((occupied >> offsets[i]) & ((1 << sizes[i]) - 1)).bit_count()
                        for i in range(d))
            return {vec: Q(1)}
        total = sum(weights[v] for v in moves)
        ans = defaultdict(Q)
        for v in moves:
            for vec, p in go(occupied | (1 << v)).items():
                ans[vec] += Q(weights[v], total) * p
        return dict(ans)
    return go(0)


def run():
    rng = Random(20261020)
    count = 0
    for _ in range(300):
        d = rng.randint(1, 5)
        sizes = tuple(rng.randint(1, 3) for _ in range(d))
        if sum(sizes) > 9:
            continue
        weights = tuple(rng.randint(1, 5) for _ in range(sum(sizes)))
        edges = [(i, j) for i in range(d) for j in range(i + 1, d)
                 if rng.randrange(2)]
        a = class_law(sizes, edges, weights)
        b = labelled_law(sizes, edges, weights)
        assert a == b, (sizes, edges, weights, a, b)
        count += 1
    sizes = (3, 4, 5, 6)
    edges = [(0, 1), (1, 2), (2, 3)]
    per_vertex = (1,) * 3 + (2,) * 4 + (3,) * 5 + (4,) * 6
    law = class_law(sizes, edges, per_vertex)
    assert law == labelled_law(sizes, edges, per_vertex)
    hetero = (1, 1, 1) + (1, 1, 2, 4) + (1, 2, 3, 4, 5) + (1, 1, 2, 4, 8, 8)
    assert law == class_law(sizes, edges, hetero) == labelled_law(sizes, edges, hetero)
    assert law == {(3, 0, 5, 0): Q(21, 65), (3, 0, 0, 6): Q(24, 143),
                   (0, 4, 0, 6): Q(28, 55)}
    assert sum(law.values()) == 1
    print('independent labelled-state checks:', count, '+ 18-point exact check')
    print('18-point weighted law:', {str(k): str(v) for k, v in sorted(law.items())})
    print('expected terminal size:', sum(sum(k) * p for k, p in law.items()))

if __name__ == '__main__':
    run()
