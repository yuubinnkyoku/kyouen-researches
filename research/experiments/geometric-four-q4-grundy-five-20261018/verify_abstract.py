#!/usr/bin/env python3
"""Exact exhaustive classification of four distinct forbidden 4-sets.

Each point is represented by a nonzero 4-bit incidence mask.  Points of the
same incidence type are indistinguishable; enumerating their multiplicities
exhausts all hypergraphs up to vertex permutation (edges remain labelled).
The Grundy solver deliberately uses a separate, uncompressed bit-mask DP.
"""
from collections import Counter
from functools import lru_cache
from itertools import permutations
import json


def incidence_vectors():
    caps = [4, 4, 4, 4]
    counts = [0] * 15

    def rec(i, total):
        if i == 15:
            if all(v == 0 for v in caps):
                yield tuple(counts), total
            return
        t = i + 1
        max_count = min(caps[j] for j in range(4) if (t >> j) & 1)
        for k in range(max_count + 1):
            counts[i] = k
            for j in range(4):
                if (t >> j) & 1:
                    caps[j] -= k
            yield from rec(i + 1, total + k)
            for j in range(4):
                if (t >> j) & 1:
                    caps[j] += k
        counts[i] = 0

    yield from rec(0, 0)


def masks_from_counts(counts):
    edges = [0] * 4
    n = 0
    for t, c in enumerate(counts, 1):
        for _ in range(c):
            for j in range(4):
                if (t >> j) & 1:
                    edges[j] |= 1 << n
            n += 1
    return edges, n


def canonical(counts):
    best = None
    for perm in permutations(range(4)):
        new = [0] * 15
        for t, c in enumerate(counts, 1):
            nt = sum(1 << perm[j] for j in range(4) if (t >> j) & 1)
            new[nt - 1] = c
        tup = tuple(new)
        if best is None or tup < best:
            best = tup
    return best


def solve_bitmask(edges, n):
    @lru_cache(None)
    def g(s):
        outcomes = set()
        for j in range(n):
            bit = 1 << j
            if s & bit:
                continue
            new = s | bit
            if all((new & edge) != edge for edge in edges):
                outcomes.add(g(new))
        k = 0
        while k in outcomes:
            k += 1
        return k

    root = g(0)
    largest = max(g(s) for s in range(1 << n)
                  if all((s & edge) != edge for edge in edges))
    return root, largest


def main():
    hist = {}
    all_hist = {}
    witness = {}
    isoclasses = {}
    for counts, n in incidence_vectors():
        edges, check_n = masks_from_counts(counts)
        assert check_n == n and all(e.bit_count() == 4 for e in edges)
        root, mx = solve_bitmask(edges, n)
        all_hist.setdefault(n, {'patterns': 0, 'root': Counter(), 'all_states_max': Counter()})
        all_hist[n]['patterns'] += 1
        all_hist[n]['root'][root] += 1
        all_hist[n]['all_states_max'][mx] += 1
        if len(set(edges)) < 4:
            continue
        hist.setdefault(n, {'patterns': 0, 'root': Counter(), 'all_states_max': Counter()})
        hist[n]['patterns'] += 1
        hist[n]['root'][root] += 1
        hist[n]['all_states_max'][mx] += 1
        if root >= 4:
            key = (n, root)
            iso = canonical(counts)
            isoclasses.setdefault(key, set()).add(iso)
            witness.setdefault(key, {'n': n, 'root': root,
                                      'incidence_counts': list(counts),
                                      'edges': [[j for j in range(n) if e >> j & 1]
                                                for e in edges]})
    out = {'all_with_repetitions': {str(n): {'patterns': v['patterns'],
                               'root': dict(sorted(v['root'].items())),
                               'all_states_max': dict(sorted(v['all_states_max'].items()))}
                      for n, v in sorted(all_hist.items())},
           'counts': {str(n): {'patterns': v['patterns'],
                               'root': dict(sorted(v['root'].items())),
                               'all_states_max': dict(sorted(v['all_states_max'].items()))}
                      for n, v in sorted(hist.items())},
           'witnesses': {f'n{n}_g{g}': w for (n, g), w in sorted(witness.items())},
           'isomorphism_classes_root_ge4':
               {f'n{n}_g{g}': len(s) for (n, g), s in sorted(isoclasses.items())}}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
