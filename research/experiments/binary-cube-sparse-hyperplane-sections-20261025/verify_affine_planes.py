#!/usr/bin/env python3
"""Exact independent audit of 3-vertex affine planes in binary cubes.

Enumerates every unordered triple for dimensions 2..6 and computes its
affine-plane intersection by integer Cramer's rule. No floating point,
minority-coordinate criterion, or inclusion-exclusion is used for membership.
"""
from itertools import combinations
from math import comb


def plane_vertex_count(triple: tuple[int, int, int], dimension: int) -> int:
    u, v, w = triple
    a = [((v >> k) & 1) - ((u >> k) & 1) for k in range(dimension)]
    b = [((w >> k) & 1) - ((u >> k) & 1) for k in range(dimension)]
    pivots = next(
        (i, j, a[i] * b[j] - a[j] * b[i])
        for i in range(dimension)
        for j in range(i + 1, dimension)
        if a[i] * b[j] != a[j] * b[i]
    )
    i, j, det = pivots
    count = 0
    for z in range(1 << dimension):
        c = [((z >> k) & 1) - ((u >> k) & 1) for k in range(dimension)]
        alpha = c[i] * b[j] - c[j] * b[i]
        beta = a[i] * c[j] - a[j] * c[i]
        if all(
            det * c[k] == alpha * a[k] + beta * b[k]
            for k in range(dimension)
        ):
            count += 1
    return count


def stirling_three(n: int) -> int:
    return (3**n - 3 * 2**n + 3) // 6


def main() -> None:
    for d in range(2, 7):
        counts = {3: 0, 4: 0}
        for triple in combinations(range(1 << d), 3):
            size = plane_vertex_count(triple, d)
            assert size in (3, 4), (d, triple, size)
            counts[size] += 1
        predicted_three = (8**d - 3 * 6**d + 3 * 4**d - 2**d) // 6
        predicted_four = 4 * 2 ** (d - 2) * stirling_three(d + 1)
        assert counts[3] == predicted_three, (d, counts, predicted_three)
        assert counts[4] == predicted_four, (d, counts, predicted_four)
        assert sum(counts.values()) == comb(1 << d, 3)
        print(
            f"d={d}: triples={comb(1 << d, 3)}, "
            f"affine-plane-3={counts[3]}, affine-plane-4={counts[4]} PASS"
        )


if __name__ == "__main__":
    main()
