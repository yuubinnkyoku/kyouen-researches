#!/usr/bin/env python3
"""Independent pointwise audit of the five-edge terminal-spectrum theorem.

Run: python3 research/experiments/five-edge-terminal-spectrum-20261101/verify.py
Uses only the Python standard library and exact integer arithmetic.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import comb
import random

R = 5
FULL = (1 << R) - 1
SINGLE = tuple(1 << i for i in range(R))
SHARED = tuple(t for t in range(1, FULL + 1) if t not in SINGLE)


def predicted_sizes(types):
    present = set(types)
    by_degree = {d: [t for t in present if t.bit_count() == d] for d in range(1, 6)}
    d2, d3, d4, d5 = (by_degree[d] for d in (2, 3, 4, 5))
    has3 = bool(d3) or any((a & b) == 0 for a, b in combinations(d2, 2))
    has2 = bool(d4) or any((a | b) == FULL for a in d3 for b in d2) or any(
        (a | b) == FULL for a, b in combinations(d3, 2)
    )
    return {5} | ({4} if d2 else set()) | ({3} if has3 else set()) | (
        {2} if has2 else set()
    ) | ({1} if d5 else set())


def _other_union(chosen, excluded):
    union = 0
    for t in chosen:
        if t != excluded:
            union |= t
    return union


def signature_polynomial(types):
    """Weighted formula using one selected point per nonempty incidence type."""
    counts = Counter(types)
    supports = sorted(t for t in counts if t)
    n = len(types)
    result = Counter()
    for k in range(1, min(R, len(supports)) + 1):
        for chosen in combinations(supports, k):
            union = 0
            for t in chosen:
                union |= t
            if union != FULL:
                continue
            if not all(t & ~_other_union(chosen, t) for t in chosen):
                continue
            weight = 1
            for t in chosen:
                weight *= counts[t]
            result[n - k] += weight
    return result


def pointwise_polynomial(types):
    """No signature quotient: inspect every labeled subset and every addition."""
    n = len(types)
    edges = [sum(1 << v for v, t in enumerate(types) if t & (1 << i)) for i in range(R)]
    safe = bytearray(1 << n)
    for mask in range(1 << n):
        safe[mask] = not any(mask & e == e for e in edges)
    polynomial = Counter()
    safe_count = 0
    for mask in range(1 << n):
        if not safe[mask]:
            continue
        safe_count += 1
        if all(not safe[mask | (1 << v)] for v in range(n) if not mask & (1 << v)):
            polynomial[mask.bit_count()] += 1
    return polynomial, safe_count


def collinear_or_cocircular(p):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    ax, ay = x1 - x0, y1 - y0
    bx, by = x2 - x0, y2 - y0
    cx, cy = x3 - x0, y3 - y0
    if ax * by == ay * bx and ax * cy == ay * cx:
        return True
    az = ax * (x1 + x0) + ay * (y1 + y0)
    bz = bx * (x2 + x0) + by * (y2 + y0)
    cz = cx * (x3 + x0) + cy * (y3 + y0)
    det = ax * (by * cz - bz * cy) - ay * (bx * cz - bz * cx) + az * (bx * cy - by * cx)
    return det == 0


POINTS = [
    (3, 5), (8, 0), (7, 3), (0, 4), (2, 10), (2, 9), (4, 5),
    (8, 1), (9, 0), (9, 7), (3, 2), (0, 5), (0, 1), (3, 1),
]
EXPECTED_EDGES = {
    (0, 1, 2, 3), (0, 1, 4, 5), (0, 1, 6, 7),
    (0, 8, 9, 10), (0, 11, 12, 13),
}


def geometry_audit():
    edges = {q for q in combinations(range(len(POINTS)), 4)
             if collinear_or_cocircular([POINTS[i] for i in q])}
    assert edges == EXPECTED_EDGES, (edges - EXPECTED_EDGES, EXPECTED_EDGES - edges)
    types = [sum(1 << i for i, e in enumerate(sorted(edges)) if v in e)
             for v in range(len(POINTS))]
    direct, safe_count = pointwise_polynomial(types)
    assert direct == Counter({9: 72, 11: 9, 13: 1}), direct
    assert signature_polynomial(types) == direct
    assert predicted_sizes(types) == {1, 3, 5}

    n = len(POINTS)
    edge_masks = [sum(1 << i for i in e) for e in edges]
    safe = bytearray(1 << n)
    for mask in range(1 << n):
        safe[mask] = not any(mask & e == e for e in edge_masks)

    @lru_cache(None)
    def values(mask):
        children = [values(mask | (1 << v)) for v in range(n)
                    if not mask & (1 << v) and safe[mask | (1 << v)]]
        if not children:
            return (0, 1)
        def mex(nums):
            found = set(nums)
            return next(i for i in range(len(found) + 1) if i not in found)
        return mex(a for a, _ in children), mex(b for _, b in children)

    assert values(0) == (1, 0)
    for mask in range(1 << n):
        if safe[mask]:
            assert values(mask) == ((13 - mask.bit_count()) % 2, (12 - mask.bit_count()) % 2)
    print(f'geometry: {comb(n,4)} exact quadruples; {safe_count} safe states; '
          f'P(u)=72u^9+9u^11+u^13; (g,h)=(1,0)')


def main():
    families = 0
    states = 0
    for count in range(5):
        for shared in combinations(SHARED, count):
            types = SINGLE + shared
            direct, safe = pointwise_polynomial(types)
            assert direct == signature_polynomial(types), (types, direct)
            assert {len(types) - length for length in direct} == predicted_sizes(types), (types, direct)
            families += 1
            states += safe
    realized = set()
    for selector in range(16):
        types = list(SINGLE) + [(1 << d) - 1 for d in range(2, 6) if selector & (1 << (d - 2))]
        types += [0] * (9 - len(types))
        direct, _ = pointwise_polynomial(types)
        sizes = {9 - length for length in direct}
        assert sizes == ({5} | {6 - d for d in range(2, 6) if selector & (1 << (d - 2))})
        realized.add(tuple(sorted(sizes)))
    assert len(realized) == 16
    rng = random.Random(20261101)
    weighted = 0
    weighted_states = 0
    for _ in range(600):
        extra = rng.sample(SHARED, rng.randrange(5))
        signatures = list(SINGLE) + extra
        counts = [rng.randrange(1, 4) for _ in signatures]
        if sum(counts) > 13:
            continue
        types = [t for t, c in zip(signatures, counts) for _ in range(c)]
        direct, safe = pointwise_polynomial(types)
        assert direct == signature_polynomial(types), (types, direct)
        assert {len(types) - length for length in direct} == predicted_sizes(types)
        weighted += 1
        weighted_states += safe
    print(f'abstract: all {len(realized)} terminal spectra realized on N=9; '
          f'{families} complete incidence-support families (up to 4 shared types), '
          f'{states} safe states; {weighted} multiplicity checks, '
          f'{weighted_states} additional safe states; mismatches=0')
    geometry_audit()
    print('PASS')


if __name__ == '__main__':
    main()
