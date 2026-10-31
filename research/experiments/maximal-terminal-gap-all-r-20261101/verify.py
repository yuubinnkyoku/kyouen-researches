#!/usr/bin/env python3
"""Independent finite checks for the r-edge maximum-gap theorem (K0596)."""
from collections import Counter
from functools import lru_cache
from itertools import combinations

POINTS = (
    (0, 0), (0, 1), (9, 1), (4, 5), (3, 3), (5, 0),
    (10, 5), (2, 5), (8, 0), (8, 1), (1, 3), (3, 4),
)
EXPECTED = {frozenset((0, 1, 2*i+2, 2*i+3)) for i in range(5)}


def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


def forbidden_quad(indices):
    a, b, c, d = (POINTS[i] for i in indices)
    def row(p):
        return (p[0]-a[0], p[1]-a[1],
                p[0]*p[0]+p[1]*p[1]-a[0]*a[0]-a[1]*a[1])
    return det3(row(b), row(c), row(d)) == 0


def spectrum_by_transversals(supports, r):
    """Brute-force inclusion-minimal transversals, independent of formula."""
    full = (1 << r) - 1
    n = len(supports)
    unions = [0] * (1 << n)
    spectrum = set()
    for subset in range(1, 1 << n):
        bit = subset & -subset
        unions[subset] = unions[subset ^ bit] | supports[bit.bit_length()-1]
        if unions[subset] != full:
            continue
        rest = subset
        while rest:
            bit = rest & -rest
            if unions[subset ^ bit] == full:
                break
            rest ^= bit
        else:
            spectrum.add(subset.bit_count())
    return spectrum


def verify_abstract():
    total = 0
    examples = 0
    for r in (3, 4):
        types = tuple(range(1, 1 << r))
        for support_bits in range(1 << len(types)):
            supports = tuple(m for i, m in enumerate(types)
                             if support_bits & (1 << i))
            actual = spectrum_by_transversals(supports, r)
            full = (1 << r) - 1
            predicted = (full in supports
                         and all(1 << i in supports for i in range(r))
                         and all(m.bit_count() in (1, r) for m in supports))
            assert (actual == {1, r}) == predicted, (r, supports, actual)
            total += 1
            examples += predicted
    return total, examples


def verify_integer_witness():
    assert len(POINTS) == len(set(POINTS)) == 12
    assert all(0 <= x <= 10 and 0 <= y <= 10 for x, y in POINTS)
    edges = {frozenset(ids) for ids in combinations(range(12), 4)
             if forbidden_quad(ids)}
    assert edges == EXPECTED, edges
    edge_masks = tuple(sum(1 << i for i in edge) for edge in edges)
    maximal = Counter()
    safe = set()
    for mask in range(1 << 12):
        if any(mask & edge == edge for edge in edge_masks):
            continue
        safe.add(mask)
        if all(any(((mask | (1 << i)) & edge) == edge for edge in edge_masks)
               for i in range(12) if not mask & (1 << i)):
            maximal[mask.bit_count()] += 1
    assert len(safe) == 3315
    assert maximal == Counter({7: 32, 11: 2}), maximal

    @lru_cache(None)
    def values(mask):
        children = [values(mask | (1 << i)) for i in range(12)
                    if not mask & (1 << i) and mask | (1 << i) in safe]
        def mex(seq):
            used = set(seq)
            j = 0
            while j in used:
                j += 1
            return j
        return (mex(c[0] for c in children),
                mex(c[1] for c in children) if children else 1)

    assert values(0) == (1, 0)
    assert values.cache_info().currsize == 3315
    return len(edges), len(safe), dict(maximal), values(0)


if __name__ == '__main__':
    print('abstract_support_families, extremal_families:', verify_abstract())
    print('integer_grid_witness (edges, safe, terminal, root):',
          verify_integer_witness())
    print('ALL CHECKS PASSED')
