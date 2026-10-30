#!/usr/bin/env python3
"""Exact two-method audit of Node Kayles on split graphs with <=3 clique vertices."""
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement, product
from random import Random


@lru_cache(None)
def signature_grundy(k, counts):
    """Direct move recurrence on neighborhood-signature multiplicities."""
    assert len(counts) == 1 << k
    if k == 0:
        return counts[0] % 2
    options = set()
    for center in range(k):
        options.add(sum(n for mask, n in enumerate(counts)
                        if not mask & (1 << center)) % 2)
    for mask, multiplicity in enumerate(counts):
        if not multiplicity:
            continue
        remaining = [i for i in range(k) if not mask & (1 << i)]
        reduced = [0] * (1 << len(remaining))
        for old, number in enumerate(counts):
            new = sum(1 << j for j, i in enumerate(remaining)
                      if old & (1 << i))
            reduced[new] += number - (old == mask)
        options.add(signature_grundy(len(remaining), tuple(reduced)))
    value = 0
    while value in options:
        value += 1
    return value


def graph_grundy(k, counts):
    """Independent named-vertex closed-neighborhood deletion, no signatures."""
    adjacency = [(1 << k) - 1 ^ (1 << i) for i in range(k)]
    for mask, number in enumerate(counts):
        for _ in range(number):
            vertex = len(adjacency)
            adjacency.append(mask)
            for center in range(k):
                if mask & (1 << center):
                    adjacency[center] |= 1 << vertex

    @lru_cache(None)
    def recurse(alive):
        children = set()
        remaining = alive
        while remaining:
            bit = remaining & -remaining
            vertex = bit.bit_length() - 1
            children.add(recurse(alive & ~(bit | adjacency[vertex])))
            remaining -= bit
        value = 0
        while value in children:
            value += 1
        return value

    value = recurse((1 << len(adjacency)) - 1)
    return value, recurse.cache_info().currsize


def main():
    histograms = {}
    states = 0
    checked = 0
    for k in range(4):
        histogram = Counter()
        for signature in product(range(3), repeat=(1 << k) - 1):
            counts = (0,) + signature
            via_signatures = signature_grundy(k, counts)
            via_vertices, visited = graph_grundy(k, counts)
            assert via_signatures == via_vertices, (k, counts, via_signatures, via_vertices)
            assert via_vertices <= 3, (k, counts, via_vertices)
            histogram[via_vertices] += 1
            states += visited
            checked += 1
        histograms[k] = dict(sorted(histogram.items()))

    # Independent named-vertex regression for arbitrary multiplicities > 2.
    rng = Random(20261030)
    random_checked = 0
    for _ in range(1200):
        counts = (0,) + tuple(rng.randint(0, 4) for _ in range(7))
        if sum(counts) > 14:
            continue
        reduced = (0,) + tuple(0 if n == 0 else 1 if n % 2 else 2
                               for n in counts[1:])
        expected = signature_grundy(3, reduced)
        actual, _ = graph_grundy(3, counts)
        assert expected == actual, (counts, expected, actual)
        random_checked += 1

    # Three different pairs of shared leaves: no private or triple-shared leaves.
    triangle = {}
    for a, b, c in combinations_with_replacement(range(3), 3):
        counts = [0] * 8
        counts[3], counts[5], counts[6] = a, b, c
        triangle[f'{a}{b}{c}'] = signature_grundy(3, tuple(counts))

    # Adding isolated vertices toggles the low bit (Sprague-Grundy xor).
    for k in range(4):
        counts = (1,) + (0,) * ((1 << k) - 1)
        assert signature_grundy(k, counts) == (signature_grundy(k, (0,) * (1 << k)) ^ 1)

    print('representatives=', checked)
    print('histograms=', histograms)
    print('named_vertex_states_sum=', states)
    print('arbitrary_multiplicity_checks=', random_checked)
    print('triangle_sorted_ternary=', triangle)
    print('all checks passed')


if __name__ == '__main__':
    main()
