#!/usr/bin/env python3
"""Exact q=6 high-pattern count, via two independent intersection-poset methods."""
from collections import Counter, defaultdict
from itertools import combinations
from math import comb

Q = 6
ALL = (1 << (1 << Q)) - 1
CUTOFF = 32


def obstacles():
    """The complete list of >32-pattern affine-extension obstructions."""
    result = []
    for support_size in (3, 5):
        for support in combinations(range(Q), support_size):
            for minus in combinations(support, (support_size - 1) // 2):
                weights = [0] * Q
                for i in support:
                    weights[i] = -1 if i in minus else 1
                mask = 0
                for pattern in range(1 << Q):
                    value = sum(weights[i] * ((pattern >> i) & 1) for i in range(Q))
                    if value in (0, 1):
                        mask |= 1 << pattern
                result.append(mask)
    assert len(result) == len(set(result)) == 120
    assert Counter(m.bit_count() for m in result) == {48: 60, 40: 60}
    return result


def incremental_inclusion_exclusion(masks):
    """For k>32, maintain c(M) in sum_M c(M)*binom(|M|,k)."""
    coefficients = {ALL: 1}
    for obstacle in masks:
        updated = coefficients.copy()
        for mask, coefficient in coefficients.items():
            meet = mask & obstacle
            if meet.bit_count() > CUTOFF:
                updated[meet] = updated.get(meet, 0) - coefficient
        coefficients = {m: c for m, c in updated.items() if c}
    return coefficients


def poset_mobius(masks):
    """Independent method: enumerate the intersection closure, then invert zeta."""
    closure = {ALL}
    for obstacle in masks:
        closure |= {m & obstacle for m in tuple(closure)
                    if (m & obstacle).bit_count() > CUTOFF}
    ordered = sorted(closure, key=lambda m: m.bit_count(), reverse=True)
    coefficients = {ALL: 1}
    for mask in ordered[1:]:
        coefficients[mask] = -sum(c for sup, c in coefficients.items()
                                  if sup & mask == mask)
    return {m: c for m, c in coefficients.items() if c}


def main():
    masks = obstacles()
    first = incremental_inclusion_exclusion(masks)
    second = poset_mobius(masks)
    assert first == second
    totals = defaultdict(int)
    counts = Counter()
    for mask, coefficient in first.items():
        totals[mask.bit_count()] += coefficient
        counts[mask.bit_count()] += 1
    expected = {64: 1, 48: -60, 40: 390, 36: 900, 34: 255}
    assert dict(totals) == expected
    assert dict(counts) == {64: 1, 48: 60, 40: 510, 36: 1980, 34: 255}
    print('intersection states:', len(first))
    print('sizes, states, signed coefficients:')
    for size in sorted(totals, reverse=True):
        print(size, counts[size], totals[size])
    print('g[6,k] for k>32:')
    for k in (33, 34, 35, 36, 40, 48, 49, 64):
        value = sum(c * comb(size, k) for size, c in totals.items() if size >= k)
        assert 0 <= value <= comb(64, k)
        print(k, value)
    for obstacle in masks:
        selected = [i for i in range(64) if (obstacle >> i) & 1][:33]
        selected_mask = sum(1 << i for i in selected)
        assert sum(c for m, c in first.items() if m & selected_mask == selected_mask) == 0
    print('independent methods and obstruction witnesses: OK')


if __name__ == '__main__':
    main()
