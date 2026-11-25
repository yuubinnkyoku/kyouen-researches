#!/usr/bin/env python3
"""Exact necessary-congruence certificate: 25 double-hit rows in 190 rows imply gcd <= 2."""
from collections import Counter

W, K = 190, 25


def masks(g, p):
    """All local masks for the longest residue class modulo g, in two ways."""
    ys = list(range(0, W, g))
    squares = {z * z % p for z in range(p)}
    direct = set()
    inverse = set()
    for c in range(p):
        for n in range(p):
            m = sum(1 << i for i, y in enumerate(ys)
                    if (n - (2*y+c)**2) % p in squares)
            if m.bit_count() >= K:
                direct.add(m)
        # Instead of testing quadratic residues of the difference, enumerate
        # possible n values as (2y+c)^2+z^2 for each y.
        inv = [0] * p
        for i, y in enumerate(ys):
            base = (2*y+c)**2
            for sq in squares:
                inv[(base+sq) % p] |= 1 << i
        inverse.update(m for m in inv if m.bit_count() >= K)
    assert direct == inverse, (g, p, 'local methods disagree')
    return direct


def verify():
    assert 24 * 8 > W-1
    p = 19
    squares = {z*z % p for z in range(p)}
    max_residues = max(sum((n-(2*y+c)**2) % p in squares for y in range(p))
                       for c in range(p) for n in range(p))
    assert max_residues == 11
    for g in (5, 6, 7):
        ys = list(range(0, W, g))
        max_repeat = max(Counter(y % p for y in ys).values())
        assert max_repeat == 2
        assert max_residues * max_repeat < K
        print(f'g={g}: {len(ys)} candidate rows; mod19 <= {max_residues}*{max_repeat}=22 <25')
    for g, mods in ((4, (11, 19)), (3, (11, 19, 23))):
        ys = list(range(0, W, g))
        states = {(1 << len(ys)) - 1}
        for p in mods:
            local = masks(g, p)
            states = {a & b for a in states for b in local
                      if (a & b).bit_count() >= K}
            print(f'g={g}, p={p}: local={len(local)}, intersections={len(states)}')
            if not states:
                break
        assert not states
    print('PASS: 25 double-hit rows in 0..189 imply row-difference gcd in {1,2}')
    print('COROLLARY (assuming T(189)<=24): 25 rows in 0..189 imply gcd=1')


if __name__ == '__main__':
    verify()
