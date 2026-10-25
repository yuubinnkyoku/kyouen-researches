#!/usr/bin/env python3
"""Finite exhaustive certificates for the universal third exponential term.

Each mask is a subset of {0,1}^n. The checks imply the corresponding
arbitrary-q bounds because the tested families use at most 4, 6, 8, 9,
or 10 coordinates, respectively.
"""
from itertools import combinations
from math import comb


def obstacles(n, support_size):
    result = []
    for support in combinations(range(n), support_size):
        for negatives in combinations(support, (support_size - 1) // 2):
            neg = set(negatives)
            pos = [i for i in support if i not in neg]
            mask = 0
            for v in range(1 << n):
                value = sum((v >> i) & 1 for i in pos) - sum(
                    (v >> i) & 1 for i in neg
                )
                if value in (0, 1):
                    mask |= 1 << v
            result.append(mask)
    return result


def essential(mask, n, coordinate):
    return any(
        bool(mask & (1 << v))
        != bool(mask & (1 << (v ^ (1 << coordinate))))
        for v in range(1 << n)
    )


def run():
    a4 = obstacles(4, 3)
    assert len(a4) == 12
    high4 = [
        x & y
        for i, x in enumerate(a4)
        for y in a4[i + 1 :]
        if (x & y).bit_count() == 10
    ]
    assert len(high4) == len(set(high4)) == 30
    assert all(
        all(essential(mask, 4, j) for j in range(4)) for mask in high4
    )
    print("4 coordinates: 30 distinct, fully supported 5/8 pair intersections")

    a6 = obstacles(6, 3)
    sizes6 = [
        (x & y).bit_count()
        for i, x in enumerate(a6)
        for y in a6[i + 1 :]
    ]
    assert max(sizes6) == 40
    assert sizes6.count(40) == 30 * comb(6, 4) == 450
    print("6 coordinates: all 1770 A3 pairs; maximum 40/64")

    a9 = obstacles(9, 3)
    max_triple = max(
        (a9[i] & a9[j] & a9[k]).bit_count()
        for i in range(len(a9))
        for j in range(i + 1, len(a9))
        for k in range(j + 1, len(a9))
    )
    assert max_triple == 288  # 9/16 of 512
    print("9 coordinates: all 2635500 A3 triples; maximum 9/16")

    a8, b8 = obstacles(8, 3), obstacles(8, 5)
    max_mixed = max((x & y).bit_count() for x in a8 for y in b8)
    assert max_mixed == 144  # 9/16 of 256
    print("8 coordinates: all 94080 A3-B5 pairs; maximum 9/16")

    b10 = obstacles(10, 5)
    max_five_pair = max(
        (x & y).bit_count()
        for i, x in enumerate(b10)
        for y in b10[i + 1 :]
    )
    assert len(b10) == len(set(b10)) == 10 * comb(10, 5) == 2520
    assert max_five_pair == 512  # 1/2 of 1024
    print("10 coordinates: all 3173940 B5 pairs; maximum 1/2")

    # Independent published q=4,5,6 coefficients (K0559, K0561, K0565).
    for q, expected in [(4, 30), (5, 140), (6, 390)]:
        assert 30 * comb(q, 4) - 10 * comb(q, 5) == expected
    print("third coefficients q=4,5,6: 30, 140, 390")


if __name__ == "__main__":
    run()
