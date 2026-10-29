#!/usr/bin/env python3
"""Independent exact checks for degree-one split-graph terminal statistics."""
from fractions import Fraction
from functools import lru_cache
from itertools import product, permutations
from math import factorial


def predicted(m, assignment):
    counts = [assignment.count(j) for j in range(m)]
    result = Fraction(1)
    for t in counts:
        result /= t + 1
    return result


def bounds(m, k):
    q, r = divmod(k, m)
    return Fraction(1, (q + 1) ** (m - r) * (q + 2) ** r), Fraction(1, k + 1)


def graph(m, assignment):
    k = len(assignment)
    n = m + k
    adj = [0] * n
    for i, j in enumerate(assignment):
        for h in range(k):
            if h != i:
                adj[i] |= 1 << h
        adj[i] |= 1 << (k + j)
        adj[k + j] |= 1 << i
    return adj


def direct_markov(m, assignment):
    """Named-vertex closed-neighborhood recursion, independent of the formula."""
    k = len(assignment)
    adj = graph(m, assignment)
    n = m + k

    @lru_cache(None)
    def rec(mask):
        if not mask:
            return Fraction(1)
        return sum(
            (rec(mask & ~(1 << v) & ~adj[v])
             for v in range(k, n) if mask & (1 << v)),
            Fraction(0),
        ) / mask.bit_count()

    return rec((1 << n) - 1)


def direct_permutations(m, assignment):
    """Enumerate all vertex priorities; accept a vertex iff it survives."""
    k = len(assignment)
    n = m + k
    adj = graph(m, assignment)
    successful = 0
    for ordering in permutations(range(n)):
        mask = (1 << n) - 1
        no_center = True
        for v in ordering:
            if mask & (1 << v):
                if v < k:
                    no_center = False
                mask &= ~(1 << v) & ~adj[v]
        successful += no_center
    return Fraction(successful, factorial(n))


def direct_game(m, assignment):
    """Check every reachable residual: SG parity, length, sequence count."""
    k = len(assignment)
    n = m + k
    adj = graph(m, assignment)

    @lru_cache(None)
    def rec(mask):
        if not mask:
            return 0, frozenset((0,)), 1
        children = [
            rec(mask & ~(1 << v) & ~adj[v])
            for v in range(n) if mask & (1 << v)
        ]
        child_sg = {g for g, _, _ in children}
        g = 0
        while g in child_sg:
            g += 1
        lengths = frozenset(1 + length for _, ls, _ in children for length in ls)
        sequences = sum(count for _, _, count in children)
        return g, lengths, sequences

    seen = set()

    def walk(mask):
        if mask in seen:
            return
        seen.add(mask)
        g, lengths, _ = rec(mask)
        remaining_independent = (mask >> k).bit_count()
        assert g == remaining_independent % 2
        assert lengths == frozenset((remaining_independent,))
        for v in range(n):
            if mask & (1 << v):
                walk(mask & ~(1 << v) & ~adj[v])

    full = (1 << n) - 1
    walk(full)
    assert rec(full)[2] == (k + 1) * factorial(m)
    return len(seen)


def main():
    checked_markov = checked_permutations = 0
    checked_game = reachable_states = 0
    checked_extrema = checked_classes = 0

    for m in range(1, 5):
        for k in range(7):
            for assignment in product(range(m), repeat=k):
                assert direct_markov(m, assignment) == predicted(m, assignment)
                checked_markov += 1
                if m + k <= 7:
                    assert direct_permutations(m, assignment) == predicted(m, assignment)
                    checked_permutations += 1
                if k <= 5:
                    reachable_states += direct_game(m, assignment)
                    checked_game += 1

    for m in range(1, 6):
        for k in range(8):
            values = [predicted(m, a) for a in product(range(m), repeat=k)]
            low, high = bounds(m, k)
            assert min(values) == low, (m, k, min(values), low)
            assert max(values) == high, (m, k, max(values), high)
            checked_extrema += len(values)
            checked_classes += 1

    assert (checked_markov, checked_permutations) == (6688, 276)
    assert (checked_game, reachable_states) == (1798, 42304)
    assert (checked_extrema, checked_classes) == (123044, 40)
    print("named-vertex Markov:", checked_markov)
    print("full priority permutations:", checked_permutations)
    print("complete game graphs / reachable residuals:", checked_game, reachable_states)
    print("extrema assignments / (m,k) classes:", checked_extrema, checked_classes)
    print("all exact checks passed")


if __name__ == "__main__":
    main()
