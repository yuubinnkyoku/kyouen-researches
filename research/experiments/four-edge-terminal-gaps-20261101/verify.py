#!/usr/bin/env python3
"""Independent exhaustive checks for the four-edge terminal-gap theorem (K0595)."""
from collections import Counter
from functools import lru_cache
from itertools import combinations

FULL = 0b1111
SINGLETONS = (1, 2, 4, 8)
OPTIONAL = tuple(t for t in range(1, 16) if t not in SINGLETONS)


def union(types):
    result = 0
    for t in types:
        result |= t
    return result


def minimal_transversal_sizes(types):
    """Enumerate transversals directly, without using the incidence theorem."""
    sizes = set()
    for size in range(1, 5):
        for chosen in combinations(types, size):
            if union(chosen) != FULL:
                continue
            if all(union(chosen[:i] + chosen[i + 1:]) != FULL
                   for i in range(size)):
                sizes.add(size)
    return sizes


def predicted_sizes(types):
    degrees = {t.bit_count() for t in types}
    complementary_pair = any(t.bit_count() == 2 and (FULL ^ t) in types
                             for t in types)
    result = {4}
    if 4 in degrees:
        result.add(1)
    if 3 in degrees or complementary_pair:
        result.add(2)
    if 2 in degrees:
        result.add(3)
    return result


def check_abstract():
    counts = Counter()
    for flags in range(1 << len(OPTIONAL)):
        types = SINGLETONS + tuple(t for i, t in enumerate(OPTIONAL)
                                   if (flags >> i) & 1)
        actual = minimal_transversal_sizes(types)
        predicted = predicted_sizes(types)
        assert actual == predicted, (types, actual, predicted)
        counts[tuple(sorted(actual))] += 1
    assert sum(counts.values()) == 2048
    assert counts[(1, 4)] == 1
    assert counts[(2, 4)] == 15
    return counts


def lifted_det4(points):
    """Exact determinant: zero iff four planar points are cocircular or collinear."""
    rows = [(x * x + y * y, x, y) for x, y in points]
    a, b, c = [tuple(rows[i][j] - rows[0][j] for j in range(3))
               for i in range(1, 4)]
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def forbidden_edges(points):
    return tuple(ids for ids in combinations(range(len(points)), 4)
                 if lifted_det4([points[i] for i in ids]) == 0)


def maximal_counts(edge_masks, n):
    def safe(mask):
        return all(mask & edge != edge for edge in edge_masks)
    counts = Counter()
    safe_count = 0
    for mask in range(1 << n):
        if not safe(mask):
            continue
        safe_count += 1
        if all(not safe(mask | (1 << i)) for i in range(n)
               if not (mask >> i) & 1):
            counts[mask.bit_count()] += 1
    return counts, safe_count


def check_integer_examples():
    examples = [
        ("two common points", [
            (2, 5), (8, 5), (5, 2), (5, 8), (0, 10), (10, 10),
            (4, 7), (8, 3), (0, 9), (1, 6),
        ], {6: 16, 9: 2}, 849, (2, 2)),
        ("four triple points", [
            (4, 3), (5, 6), (10, 9), (10, 6),
            (9, 10), (1, 6), (4, 4), (4, 2),
        ], {4: 1, 6: 10}, 209, (0, 1)),
    ]
    for name, points, expected, expected_safe, expected_gh in examples:
        assert len(points) == len(set(points))
        assert all(0 <= x <= 10 and 0 <= y <= 10 for x, y in points)
        edges = forbidden_edges(points)
        assert len(edges) == 4, (name, edges)
        masks = tuple(sum(1 << i for i in edge) for edge in edges)
        counts, safe_count = maximal_counts(masks, len(points))
        assert counts == expected, (name, counts)
        assert safe_count == expected_safe, (name, safe_count)

        @lru_cache(None)
        def solve(mask, misere):
            values = {solve(mask | (1 << i), misere)
                      for i in range(len(points))
                      if not (mask >> i) & 1
                      and all((mask | (1 << i)) & e != e for e in masks)}
            if misere and not values:
                return 1
            return next(k for k in range(len(values) + 1) if k not in values)

        assert (solve(0, False), solve(0, True)) == expected_gh
        print(f"{name}: N={len(points)}, edges={len(edges)}, "
              f"safe={safe_count}, maximal={dict(sorted(counts.items()))}, "
              f"(g,h)={expected_gh}")
        print("  forbidden index quadruples:", edges)


def check_abstract_extremal_families():
    for q in (4, 5, 6):
        a = [FULL] * 2 + [1 << i for i in range(4) for _ in range(q - 2)]
        b = [FULL ^ (1 << i) for i in range(4)] + [
            1 << i for i in range(4) for _ in range(q - 3)
        ]
        for types, expected in (
            (a, {4 * q - 10: (q - 2) ** 4, 4 * q - 7: 2}),
            (b, {4 * q - 12: (q - 3) ** 4, 4 * q - 10: 4 * q - 6}),
        ):
            masks = [sum(1 << j for j, t in enumerate(types) if (t >> i) & 1)
                     for i in range(4)]
            counts, _ = maximal_counts(masks, len(types))
            assert counts == expected, (q, len(types), counts, expected)
    print("Abstract extremal counting formulas checked for q=4,5,6")


if __name__ == "__main__":
    counts = check_abstract()
    print("Exhaustive incidence-support families:", sum(counts.values()))
    print("Spectra and counts:", sorted(counts.items()))
    check_integer_examples()
    check_abstract_extremal_families()
    print("All checks passed")
