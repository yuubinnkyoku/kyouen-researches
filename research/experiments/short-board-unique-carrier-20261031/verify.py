#!/usr/bin/env python3
"""Exact integer-lattice audit for short-board unique-carrier rigidity.

No external dependencies. Run: python verify.py
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import comb, factorial


def incircle_or_collinear(quad):
    (x0, y0), *other = quad
    (a, b, c), (d, e, f), (g, h, i) = [
        (x - x0, y - y0, (x - x0) ** 2 + (y - y0) ** 2)
        for x, y in other
    ]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g) == 0


def forbidden(points):
    return all(incircle_or_collinear(quad) for quad in combinations(points, 4))


def all_forbidden(points, q):
    return {frozenset(c) for c in combinations(points, q) if forbidden(c)}


def audit_board(points, q, check_game):
    n = len(points)
    forbidden_sets = all_forbidden(points, q)
    count = len(forbidden_sets)
    candidates = [0] + [comb(m, q) for m in range(q, n + 1)]
    assert count in candidates, (points, q, count)
    if count:
        carrier = set().union(*forbidden_sets)
        m = len(carrier)
        assert count == comb(m, q)
        assert forbidden_sets == {
            frozenset(c) for c in combinations(carrier, q)
        }
        L = n - m + q - 1
    else:
        carrier = set()
        L = n
    if not check_game:
        return count

    bad_masks = [
        sum(1 << points.index(p) for p in f) for f in forbidden_sets
    ]
    full = (1 << n) - 1

    @lru_cache(None)
    def game(s):
        if any(s & b == b for b in bad_masks):
            return None
        children = [
            game(s | (1 << i))
            for i in range(n) if not s & (1 << i)
        ]
        children = [child for child in children if child is not None]
        if not children:
            return (0, 1, frozenset((s,)), 1)

        def mex(xs):
            v = 0
            while v in xs:
                v += 1
            return v

        return (
            mex({child[0] for child in children}),
            mex({child[1] for child in children}),
            frozenset().union(*(child[2] for child in children)),
            sum(child[3] for child in children),
        )

    for s in range(full + 1):
        result = game(s)
        if result is None:
            continue
        used = s.bit_count()
        expected_g = (L - used) % 2
        assert result[:2] == (expected_g, 1 - expected_g), (
            points, q, s, result
        )
        if count:
            a = sum(
                bool(s & (1 << i))
                for i, p in enumerate(points) if p in carrier
            )
            expected_terminals = comb(m - a, q - 1 - a)
        else:
            expected_terminals = 1
        assert len(result[2]) == expected_terminals
        assert result[3] == expected_terminals * factorial(L - used)
    return count


def main():
    grid = tuple((x, y) for x in range(4) for y in range(4))
    for q, n in ((4, 5), (5, 7), (6, 9), (7, 11)):
        counts = Counter()
        for board in combinations(grid, n):
            count = audit_board(board, q, check_game=False)
            if counts[count] < 12:
                assert audit_board(board, q, check_game=True) == count
            counts[count] += 1
        assert sum(counts.values()) == comb(16, n)
        checked = sum(min(12, v) for v in counts.values())
        print(
            f'q={q} N={n} exhaustive={comb(16,n)} '
            f'f_histogram={dict(sorted(counts.items()))} '
            f'full_game_checked={checked}'
        )

    boundary4 = (
        (1, -2), (1, 2), (-2, -1), (-2, 1), (0, -1), (3, -2)
    )
    assert len(all_forbidden(boundary4, 4)) == 2

    boundary5 = (
        (1, -2), (1, 2), (-2, -1), (-2, 1),
        (-1, -2), (3, -2), (3, 2), (4, -1)
    )
    forb = all_forbidden(boundary5, 5)
    assert len(forb) == 2
    assert len(set.intersection(*map(set, forb))) == 2
    max_safe_sizes = set()
    for s in combinations(boundary5, 6):
        ss = set(s)
        if any(f <= ss for f in forb):
            continue
        if all(
            any(f <= ss | {p} for f in forb)
            for p in boundary5 if p not in ss
        ):
            max_safe_sizes.add(6)
    for s in combinations(boundary5, 7):
        ss = set(s)
        if not any(f <= ss for f in forb):
            max_safe_sizes.add(7)
    assert max_safe_sizes == {6, 7}
    print(
        'boundary q=4 N=6 forbidden=2; '
        'q=5 N=8 forbidden=2, intersection=2, '
        'maximal_safe_sizes=[6,7]'
    )


if __name__ == '__main__':
    main()
