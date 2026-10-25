#!/usr/bin/env python3
"""Independent set-based cross-check (no bit masks) of the third coefficient.

Checks q=4,5,6 by explicitly constructing the allowed binary tuples for
every signed support-3 and support-5 equation.
"""
from itertools import combinations, product
from math import comb


def allowed_sets(q, support_size):
    universe = list(product((0, 1), repeat=q))
    out = []
    for support in combinations(range(q), support_size):
        for negative in combinations(support, (support_size - 1) // 2):
            negative = set(negative)
            positive = set(support) - negative
            out.append(
                frozenset(
                    v for v in universe
                    if sum(v[i] for i in positive) - sum(v[i] for i in negative)
                    in (0, 1)
                )
            )
    return out


for q, expected in [(4, 30), (5, 140), (6, 390)]:
    triples = allowed_sets(q, 3)
    quintuples = allowed_sets(q, 5) if q >= 5 else []
    large_pair_count = sum(
        len(left & right) == 5 * 2 ** (q - 3)
        for i, left in enumerate(triples)
        for right in triples[i + 1:]
    )
    assert large_pair_count == 30 * comb(q, 4)
    assert len(quintuples) == 10 * comb(q, 5)
    assert large_pair_count - len(quintuples) == expected
    print(f"q={q}: {large_pair_count} 5/8 pairs, "
          f"{len(quintuples)} support-5 obstacles, coefficient {expected}")
