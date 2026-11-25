#!/usr/bin/env python3
"""Independent check: enumerate maximal independent vertex subsets, not move trees."""
from math import factorial
from random import Random


def predicted(k, m, edge):
    degrees = [
        sum((edge >> (i * m + j)) & 1 for j in range(m))
        for i in range(k)
    ]
    result = {}
    for d in degrees:
        t = m + 1 - d
        result[t] = result.get(t, 0) + factorial(t)
    if k == 0 or all(degrees):
        result[m] = result.get(m, 0) + factorial(m)
    return result


def independent_count(k, m, edge):
    n = k + m
    edges = [(i, j) for i in range(k) for j in range(i + 1, k)]
    edges += [
        (i, k + j)
        for i in range(k)
        for j in range(m)
        if (edge >> (i * m + j)) & 1
    ]
    neighbors = [0] * n
    for i, j in edges:
        neighbors[i] |= 1 << j
        neighbors[j] |= 1 << i

    result = {}
    for mask in range(1 << n):
        if any((mask >> i & 1) and (mask >> j & 1) for i, j in edges):
            continue
        # Maximality: every excluded vertex touches an included vertex.
        if any(
            not (mask >> i & 1) and not (neighbors[i] & mask)
            for i in range(n)
        ):
            continue
        length = mask.bit_count()
        result[length] = result.get(length, 0) + factorial(length)
    return result


def main():
    rng = Random(0xA3D9)
    tested = 0
    for k in range(4):
        for m in range(4):
            for edge in range(1 << (k * m)):
                assert predicted(k, m, edge) == independent_count(k, m, edge)
                tested += 1
    for k, m in ((4, 4), (5, 3), (3, 5)):
        for _ in range(250):
            edge = rng.randrange(1 << (k * m))
            assert predicted(k, m, edge) == independent_count(k, m, edge)
            tested += 1
    print(f"PASS independent maximal-independent-set enumeration: {tested} graphs")


if __name__ == "__main__":
    main()
