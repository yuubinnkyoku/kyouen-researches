#!/usr/bin/env python3
"""Exact independent audits for a one-missing-pair split Node Kayles family.

Run: python3 research/experiments/game-structure/one-missing-pair-uniform-leaves-20261028/verify.py
No external dependencies.
"""
from functools import lru_cache


def predicted(m: int, t: int) -> int:
    assert m >= 2 and t >= 0
    if m == 2:
        return 1 - t % 2
    return (3, 3 - t % 2, 2, 2 + t % 2)[m % 4]


def mex(values) -> int:
    s = set(values)
    n = 0
    while n in s:
        n += 1
    return n


def split_recurrence(m: int, t: int):
    """DP on surviving clique subsets; independent vertices are folded into signatures."""
    assert m >= 2 and t >= 0
    pairs = [(1 << i) | (1 << j) for i in range(m)
             for j in range(i + 1, m) if (i, j) != (0, 1)]
    total_pairs = len(pairs)

    @lru_cache(None)
    def active_parity(c):
        outside = m - c.bit_count()
        inactive_pairs = outside * (outside - 1) // 2 - int((c & 3) == 0)
        return (total_pairs - inactive_pairs + t * c.bit_count()) & 1

    @lru_cache(None)
    def solve(c):
        if c == 0:
            return 0
        a = active_parity(c)
        children = []
        for i in range(m):
            if c & (1 << i):
                # Selecting a clique vertex leaves only independent isolated vertices.
                children.append(a ^ ((m - 1 - int(i < 2) + t) & 1))
        for pair in pairs:
            if pair & c:
                d = c & ~pair
                # Newly isolated independent vertices, excluding the chosen one.
                children.append(solve(d) ^ a ^ active_parity(d) ^ 1)
        if t:
            for i in range(m):
                if c & (1 << i):
                    d = c & ~(1 << i)
                    children.append(solve(d) ^ a ^ active_parity(d) ^ 1)
        return mex(children)

    result = solve((1 << m) - 1)
    return result, solve.cache_info().currsize


def direct_named_vertices(m: int, t: int):
    """Independent named-vertex closed-neighborhood deletion, no clique compression."""
    assert m >= 2 and t >= 0
    edges = [(i, j) for i in range(m) for j in range(i + 1, m)]
    index = m
    for i in range(m):
        for j in range(i + 1, m):
            if (i, j) == (0, 1):
                continue
            edges.extend([(i, index), (j, index)])
            index += 1
    for i in range(m):
        for _ in range(t):
            edges.append((i, index))
            index += 1
    closed = [1 << i for i in range(index)]
    for i, j in edges:
        closed[i] |= 1 << j
        closed[j] |= 1 << i

    @lru_cache(None)
    def solve(c):
        if not c:
            return 0
        # Isolated vertices form an impartial disjoint sum of single moves.
        # Strip them in one step rather than exploring their 2^s subsets.
        active = c
        isolated_parity = 0
        todo = c
        while todo:
            bit = todo & -todo
            i = bit.bit_length() - 1
            todo ^= bit
            if closed[i] & c == bit:
                active ^= bit
                isolated_parity ^= 1
        if active != c:
            return solve(active) ^ isolated_parity
        children = []
        todo = c
        while todo:
            bit = todo & -todo
            i = bit.bit_length() - 1
            todo ^= bit
            children.append(solve(c & ~closed[i]))
        return mex(children)

    return solve((1 << index) - 1), solve.cache_info().currsize, index


def symbolic_children(m: int, t: int):
    """Mathematically exhaustive move orbits for m>=7, using the induction formula."""
    assert m >= 7 and t >= 0
    choose2 = lambda n: n * (n - 1) // 2
    special_clique = (choose2(m - 1) + (m - 1) * t) & 1
    regular_clique = special_clique ^ 1
    special_regular_pair = 2 + (((m - 2) * t + 1 + choose2(m - 2)) & 1)
    regular_regular_pair = predicted(m - 2, t + 2)
    children = [special_clique, regular_clique,
                special_regular_pair, regular_regular_pair]
    if t > 0:
        special_leaf = (2 + (((m - 1) * t + (m - 2) + choose2(m - 1)) & 1)) ^ ((t - 1) & 1)
        regular_leaf = predicted(m - 1, t + 1) ^ ((t - 1) & 1)
        children.extend([special_leaf, regular_leaf])
    return children


def main():
    # These three values represent every nonnegative leaf multiplicity:
    # zero, positive odd, and positive even (independent-twin parity lemma).
    count = 0
    named_states = 0
    for m in range(2, 7):
        for t in range(3):
            expected = predicted(m, t)
            a, _ = split_recurrence(m, t)
            assert a == expected, (m, t, expected, a)
            b, states, vertices = direct_named_vertices(m, t)
            assert a == b, (m, t, a, b)
            named_states += states
            print(f'base m={m} t={t}: g={a}, named_vertices={vertices}, named_states={states}')
            count += 1
    print(f'BASE_OK {count} cases; named-vertex states {named_states}')

    # Exact subset DP extends well beyond the finite base; it is not used as
    # evidence of the universal induction.
    checked = 0
    extra_named_count = 0
    for m in range(7, 15):
        for t in range(3):
            a, states = split_recurrence(m, t)
            assert a == predicted(m, t), (m, t, a)
            if m <= 12:
                b, named, vertices = direct_named_vertices(m, t)
                assert a == b, (m, t, a, b)
                named_states += named
                extra_named_count += 1
            checked += 1
        print(f'EXTRA_OK m={m}, {states} subset states (last t)')
    print(f'EXTRA_OK {checked} cases; extra named checks {extra_named_count}')
    print(f'NAMED_OK {count + extra_named_count} cases, {named_states} total states')

    # The child formulas depend only on m modulo 4, t modulo 2, and t=0
    # versus t>0. Hence the following 12 representatives prove the
    # induction step for all m>=7 and t>=0, not merely for finite m.
    table = {}
    for m in range(7, 11):
        for t in (0, 1, 2):
            ch = symbolic_children(m, t)
            independent = ch[2:]
            assert len(set(independent)) == 1, (m, t, ch)
            assert independent[0] in (2, 3), (m, t, ch)
            assert set(ch) == {0, 1, independent[0]}, (m, t, ch)
            assert mex(ch) == predicted(m, t), (m, t, ch)
            table[(m % 4, t)] = (independent[0], predicted(m, t))
    print('INDUCTION_OK (m mod 4, t representative): (non-clique child, mex)')
    for key in sorted(table):
        print(f'  {key}: {table[key]}')
    print('ALL_OK')


if __name__ == '__main__':
    main()
