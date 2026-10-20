#!/usr/bin/env python3
"""Independent direct-subset audit for the sunflower forbidden-hypergraph SG formula.

Run: python sunflower_grundy_20261018.py [--max-points N] [--output FILE]
Uses only the Python standard library. Each explicit board is fully enumerated.
"""
import argparse
import json
from functools import lru_cache
from itertools import product
from math import prod


def formula(c, petals, z):
    """Grundy value from remaining core, petals, and unconstrained points."""
    k = len(petals)
    assert k >= 1 and (c > 0 or all(u > 0 for u in petals))
    n = c + sum(petals)
    if k & 1:
        h = (n - 1) & 1
    else:
        m = min(petals)
        if m < c:
            h = (n - 1) & 1
        elif m == c:
            h = 2 + (sum(petals) & 1)
        else:
            h = n & 1
    return h ^ (z & 1)


def direct_game(core, petals, isolated):
    """Bitmask-based direct legal-subset recursion, without count compression."""
    bits = []
    offset = 0
    for p in [core, *petals, isolated]:
        mask = ((1 << p) - 1) << offset
        bits.append(mask)
        offset += p
    core_mask, *petal_masks, isolated_mask = bits
    edges = tuple(core_mask | p for p in petal_masks)
    full = (1 << sum([core, *petals, isolated])) - 1

    @lru_cache(maxsize=None)
    def g(s):
        opts = set()
        for bit in range(full.bit_length()):
            b = 1 << bit
            if s & b:
                continue
            t = s | b
            if not any(t & e == e for e in edges):
                opts.add(g(t))
        h = 0
        while h in opts:
            h += 1
        return h

    safe = 0
    max_g = 0
    maximal = {}
    for s in range(full + 1):
        if any(s & e == e for e in edges):
            continue
        safe += 1
        c = core - (s & core_mask).bit_count()
        us = tuple(p - (s & mask).bit_count() for p, mask in zip(petals, petal_masks))
        z = isolated - (s & isolated_mask).bit_count()
        actual = g(s)
        expected = formula(c, us, z)
        max_g = max(max_g, actual)
        if actual != expected:
            raise AssertionError((core, petals, isolated, s, actual, expected))
        # A terminal state has no safe addition.
        if not any(not s & (1 << j) and not any((s | (1 << j)) & e == e for e in edges)
                   for j in range(full.bit_length())):
            maximal[full.bit_length() - s.bit_count()] = maximal.get(full.bit_length() - s.bit_count(), 0) + 1
    expected_maximal = {1: core, len(petals): prod(petals)}
    if len(petals) == 1:
        expected_maximal = {1: core + petals[0]}
    if maximal != expected_maximal:
        raise AssertionError((core, petals, isolated, maximal, expected_maximal))
    expected_safe = (1 << isolated) * (((1 << core) - 1) * (1 << sum(petals))
                                        + prod((1 << p) - 1 for p in petals))
    if safe != expected_safe:
        raise AssertionError((core, petals, isolated, safe, expected_safe))
    return safe, max_g


def run(max_points):
    counts = {'max_points': max_points, 'boards': 0, 'safe_states': 0,
              'by_petals': {}, 'max_nimber_seen': 0}
    for k in range(1, max_points):
        boards = 0
        for core in range(1, max_points - k + 1):
            for z in range(0, min(3, max_points - core - k) + 1):
                remaining = max_points - core - z
                for petals in product(range(1, remaining - k + 2), repeat=k):
                    if sum(petals) > remaining:
                        continue
                    # Identical petals up to relabeling: enumerate only nondecreasing sizes.
                    if tuple(sorted(petals)) != petals:
                        continue
                    safe, max_g = direct_game(core, petals, z)
                    boards += 1
                    counts['boards'] += 1
                    counts['safe_states'] += safe
                    counts['max_nimber_seen'] = max(counts['max_nimber_seen'], max_g)
        if boards:
            counts['by_petals'][str(k)] = boards
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-points', type=int, default=12)
    parser.add_argument('--output')
    args = parser.parse_args()
    result = run(args.max_points)
    result['check'] = 'all safe subsets, direct mex vs closed formula; terminal and safe counts'
    payload = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(payload)
    print(payload, end='')


if __name__ == '__main__':
    main()
