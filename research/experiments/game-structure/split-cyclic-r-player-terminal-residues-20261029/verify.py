#!/usr/bin/env python3
"""Independent exhaustive audit of terminal lengths for cyclic multiplayer Node Kayles on split graphs.

Only Python 3 standard library. Run from any directory.
"""
from functools import lru_cache
from itertools import product


def build_graph(k: int, m: int, cross: int) -> list[int]:
    n = k + m
    adj = [0] * n
    for i in range(k):
        for j in range(i + 1, k):
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    for i in range(k):
        for j in range(m):
            if (cross >> (i * m + j)) & 1:
                adj[i] |= 1 << (k + j)
                adj[k + j] |= 1 << i
    return adj


def expected_lengths(k: int, m: int, cross: int) -> set[int]:
    if k == 0:
        return {m}
    d = [sum((cross >> (i * m + j)) & 1 for j in range(m)) for i in range(k)]
    sizes = {m + 1 - x for x in d}
    if all(x > 0 for x in d):
        sizes.add(m)
    return sizes


def maximal_independent_lengths(adj: list[int]) -> set[int]:
    n = len(adj)
    result = set()
    for mask in range(1 << n):
        independent = True
        covered = mask
        for i in range(n):
            if mask >> i & 1:
                if adj[i] & mask:
                    independent = False
                    break
                covered |= adj[i]
        if independent and covered == (1 << n) - 1:
            result.add(mask.bit_count())
    return result


def play_lengths(adj: list[int]) -> set[int]:
    """All complete move counts via actual closed-neighborhood deletion."""
    @lru_cache(None)
    def rec(remaining: int) -> frozenset[int]:
        if not remaining:
            return frozenset((0,))
        lengths = set()
        x = remaining
        while x:
            bit = x & -x
            i = bit.bit_length() - 1
            x ^= bit
            next_remaining = remaining & ~(adj[i] | bit)
            lengths.update(1 + v for v in rec(next_remaining))
        return frozenset(lengths)
    return set(rec((1 << len(adj)) - 1))


def predict_locked(k: int, m: int, cross: int, r: int) -> bool:
    if k == 0:
        return True
    d = [sum((cross >> (i * m + j)) & 1 for j in range(m)) for i in range(k)]
    return (all(x % r == 1 for x in d)
            or (0 in d and all(x % r == 0 for x in d)))


def main():
    # Includes all labelled k,m <=4, and asymmetric 3x5 / 5x3 interfaces.
    cases = 0
    locked_by_r = {r: 0 for r in range(2, 7)}
    max_distinct = 0
    max_size = 0
    for k, m in (list(product(range(5), repeat=2)) + [(3, 5), (5, 3)]):
        for cross in range(1 << (k * m)):
            adj = build_graph(k, m, cross)
            expected = expected_lengths(k, m, cross)
            direct = maximal_independent_lengths(adj)
            via_play = play_lengths(adj)
            if expected != direct or expected != via_play:
                raise AssertionError(('terminal mismatch', k, m, cross, expected, direct, via_play))
            for r in locked_by_r:
                actual = len({v % r for v in direct}) == 1
                predicted = predict_locked(k, m, cross, r)
                if actual != predicted:
                    raise AssertionError(('residue mismatch', k, m, cross, r, direct, actual, predicted))
                locked_by_r[r] += actual
            cases += 1
            max_distinct = max(max_distinct, len(direct))
            max_size = max(max_size, max(direct))
    print(f'PASS labelled_split_graphs={cases} two_independent_enumerators=PASS '
          f'r=2..6 locked_counts={locked_by_r} max_distinct_lengths={max_distinct} '
          f'max_terminal_size={max_size}')

    # A witness for r=3 with different exact lengths but identical last mover.
    k, m = 3, 6
    # Each centre has one private leaf, plus three twins adjacent to centres 0 and 1.
    cross = 0
    for i, j in [(0, 0), (1, 1), (2, 2), (0, 3), (1, 3),
                 (0, 4), (1, 4), (0, 5), (1, 5)]:
        cross |= 1 << (i * m + j)
    lengths = maximal_independent_lengths(build_graph(k, m, cross))
    assert lengths == {3, 6}, lengths
    assert {x % 3 for x in lengths} == {0}
    print('PASS r=3 witness terminal_lengths={3,6} last_mover=player_3')


if __name__ == '__main__':
    main()
