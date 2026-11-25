#!/usr/bin/env python3
"""Exact five-center Node Kayles by support-count recursion.

Five clique vertices have one private leaf each. The ten pair-support
multiplicities range over 0,1,2 in the complete finite verification.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, permutations, product

K = 5
EDGES = tuple(combinations(range(K), 2))
PERMS = tuple(permutations(range(K)))


def canon(counts):
    return min(tuple(counts[EDGES.index(tuple(sorted((p[i], p[j]))))]
                     for i, j in EDGES) for p in PERMS)


@lru_cache(None)
def grundy(k, counts):
    """counts[s]: independent vertices with clique support s."""
    if not k:
        return counts[0] & 1
    options = set()
    for i in range(k):
        options.add(sum(n for s, n in enumerate(counts)
                        if not (s >> i & 1)) & 1)
    for support, n in enumerate(counts):
        if not n:
            continue
        remaining = [i for i in range(k) if not (support >> i & 1)]
        nxt = [0] * (1 << len(remaining))
        for old_support, count in enumerate(counts):
            new_support = sum(1 << j for j, i in enumerate(remaining)
                              if old_support >> i & 1)
            nxt[new_support] += count
        nxt[0] -= 1
        # Proven independent-twin parity compression (K0336).
        nxt[0] &= 1
        for j in range(1, len(nxt)):
            if nxt[j] > 2:
                nxt[j] = 1 if nxt[j] & 1 else 2
        options.add(grundy(len(remaining), tuple(nxt)))
    value = 0
    while value in options:
        value += 1
    return value


def value(pair_counts):
    counts = [0] * (1 << K)
    for i in range(K):
        counts[1 << i] = 1
    for (i, j), n in zip(EDGES, pair_counts):
        counts[(1 << i) | (1 << j)] = n
    return grundy(K, tuple(counts))


def main():
    histogram = Counter()
    simple_classes = defaultdict(list)
    for c in product(range(3), repeat=len(EDGES)):
        a = value(c)
        b = value(tuple(v & 1 for v in c))
        assert a == b, (c, a, b)
        histogram[a] += 1
        if all(v < 2 for v in c):
            simple_classes[canon(c)].append(c)
    assert histogram == Counter({0: 1744, 1: 2225, 2: 27780, 3: 27300}), histogram
    assert len(simple_classes) == 34
    assert sum(map(len, simple_classes.values())) == 1024
    simple_hist = Counter()
    for rep, cases in simple_classes.items():
        simple_hist[value(rep)] += len(cases)
    assert simple_hist == Counter({0: 32, 1: 32, 2: 480, 3: 480}), simple_hist
    print('PASS 59049/59049 ternary bases; even-positive pair types = zero')
    print('PASS 34/34 simple isomorphism classes; 1024/1024 labelled graphs')
    print('Ternary histogram:', dict(sorted(histogram.items())))
    print('Simple histogram:', dict(sorted(simple_hist.items())))
    print('Quotient cache states:', grundy.cache_info().currsize)
    print('representative | labelled count | Grundy')
    for rep, cases in sorted(simple_classes.items(),
                             key=lambda item: (sum(item[0]), item[0])):
        print(''.join(map(str, rep)), len(cases), value(rep))


if __name__ == '__main__':
    main()
