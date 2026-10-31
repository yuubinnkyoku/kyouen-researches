#!/usr/bin/env python3
"""Independent occupied-subset mex audit for the <=2 forbidden-set misere swap.

Run: python verify.py. Does not use a count-state recurrence to compute mex.
"""
from collections import Counter
from random import Random


def mex(values):
    values = set(values)
    k = 0
    while k in values:
        k += 1
    return k


def closed_normal(n, E, F, S):
    remaining = ((1 << n) - 1) ^ S
    c = ((E & F) & remaining).bit_count()
    u = ((E & ~F) & remaining).bit_count()
    v = ((F & ~E) & remaining).bit_count()
    z = ((~(E | F)) & remaining).bit_count()
    if c == 0:
        core = (u + v) % 2
    elif min(u, v) < c:
        core = (c - 1 + u + v) % 2
    elif min(u, v) == c:
        core = 2 + ((max(u, v) - c) % 2)
    else:
        core = (c + u + v) % 2
    return core ^ (z % 2)


def audit(n, E, F):
    full = (1 << n) - 1
    g = [-1] * (1 << n)
    h = [-1] * (1 << n)
    positions = 0
    low_child = 0
    for S in range(full, -1, -1):
        if (S & E) == E or (S & F) == F:
            continue
        options = []
        rest = full ^ S
        while rest:
            bit = rest & -rest
            rest -= bit
            child = S | bit
            if (child & E) != E and (child & F) != F:
                options.append(child)
        g[S] = mex(g[T] for T in options) if options else 0
        h[S] = mex(h[T] for T in options) if options else 1
        expected = 1 - g[S] if g[S] < 2 else g[S]
        assert h[S] == expected, (n, E, F, S, g[S], h[S])
        assert g[S] == closed_normal(n, E, F, S), (n, E, F, S, g[S])
        if options:
            assert any(g[T] <= 1 for T in options), (n, E, F, S)
            low_child += 1
        positions += 1
    return positions, low_child, max(g), max(h)


def main():
    rng = Random(20261031)
    totals = Counter()
    for n in range(1, 8):
        families = 0
        for E in range(1, 1 << n):
            for F in range(E, 1 << n):
                positions, low_child, _, _ = audit(n, E, F)
                families += 1
                totals['positions'] += positions
                totals['nonterminal'] += low_child
        totals['families'] += families
        print(f'exhaustive n={n}: {families} families')
    for n in range(8, 13):
        for _ in range(200):
            E = rng.randrange(1, 1 << n)
            F = rng.randrange(1, 1 << n)
            positions, low_child, _, _ = audit(n, E, F)
            totals['positions'] += positions
            totals['nonterminal'] += low_child
            totals['sample_families'] += 1
    print('AUDIT PASS', dict(totals))


if __name__ == '__main__':
    main()
