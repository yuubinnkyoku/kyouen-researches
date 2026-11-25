#!/usr/bin/env python3
"""Exact clique-subset recurrence and closed-form tests for complete pair incidence.

Run from the repository root, or directly as a standalone Python 3 script.
No third-party dependencies.
"""
from __future__ import annotations

from itertools import combinations, product
from random import Random


def closed_form(k: int, pairs: tuple[int, ...], leaves: tuple[int, ...]) -> int:
    assert k >= 3 and len(pairs) == k * (k - 1) // 2 and len(leaves) == k
    assert all(r > 0 for r in pairs) and all(t >= 0 for t in leaves)
    z = [t % 2 for t in leaves]
    u = sum(leaves) % 2
    for (i, j), r in zip(combinations(range(k), 2), pairs):
        p = r % 2
        z[i] ^= p
        z[j] ^= p
        u ^= p
    if all(x == z[0] for x in z):
        return 1 - (u ^ z[0])
    return 2 + u


def exact_subsets(k: int, pairs: tuple[int, ...], leaves: tuple[int, ...]) -> int:
    """Exact Node Kayles mex, using original independent-vertex signatures.

    For a live clique subset A, all independent vertices whose original
    neighborhood meets A remain present; those no longer meeting A are
    isolated and accounted for by XOR parity on each transition.
    """
    assert len(pairs) == k * (k - 1) // 2
    signatures = [(1 << i, t) for i, t in enumerate(leaves) if t]
    signatures += [((1 << i) | (1 << j), r)
                   for (i, j), r in zip(combinations(range(k), 2), pairs) if r]
    full = (1 << k) - 1
    active_parity = [sum(n % 2 for s, n in signatures if s & a) % 2
                     for a in range(full + 1)]
    dp = [0] * (full + 1)
    for a in range(1, full + 1):
        options = set()
        for i in range(k):
            if a & (1 << i):
                # Choose a clique vertex: all clique vertices disappear.
                options.add(sum(n % 2 for s, n in signatures
                                if (s & a) and not (s & (1 << i))) % 2)
        for b in {s & a for s, _ in signatures if s & a}:
            a2 = a & ~b
            # Choose an independent vertex of active neighborhood b.
            # It disappears, while all other newly isolated vertices survive.
            isolated = active_parity[a] ^ active_parity[a2] ^ 1
            options.add(dp[a2] ^ isolated)
        value = 0
        while value in options:
            value += 1
        dp[a] = value
    return dp[full]


def main() -> None:
    for k in (3, 4):
        n_pairs = k * (k - 1) // 2
        histogram = [0, 0, 0, 0]
        for pairs in product((1, 2), repeat=n_pairs):
            for leaves in product((0, 1, 2), repeat=k):
                exact = exact_subsets(k, pairs, leaves)
                predicted = closed_form(k, pairs, leaves)
                assert exact == predicted, (k, pairs, leaves, exact, predicted)
                histogram[exact] += 1
        print(f'base k={k}: {sum(histogram)} complete parity/leaf-category cases; '
              f'g=0,1,2,3 counts={histogram}')
    rng = Random(20261028)
    for k, count in ((5, 400), (6, 400), (7, 400), (8, 200)):
        n_pairs = k * (k - 1) // 2
        for _ in range(count):
            pairs = tuple(rng.choice((1, 2, 3, 4, 5, 6)) for _ in range(n_pairs))
            leaves = tuple(rng.randrange(7) for _ in range(k))
            exact = exact_subsets(k, pairs, leaves)
            predicted = closed_form(k, pairs, leaves)
            assert exact == predicted, (k, pairs, leaves, exact, predicted)
        print(f'larger k={k}: {count} deterministic random checks OK')
    print('PASS: formula, complete finite bases, and independent recurrence agree')


if __name__ == '__main__':
    main()
