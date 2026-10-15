#!/usr/bin/env python3
"""Finite residue certificates for an unbounded four-row mod-9 theorem.

The unbounded theorem is proved by checking all 16 residue pairs.
The exact-chord search is an additional finite sanity check only.
"""
from itertools import product
from math import isqrt

R = {x*x % 9 for x in range(9)}
assert R == {0, 1, 4, 7}

for h in (1, 2, 4, 5, 7, 8):
    solutions = []
    for a, b in product(sorted(R), repeat=2):
        c = (2*b-a-8*h*h) % 9
        d = (3*b-2*a-24*h*h) % 9
        if c in R and d in R:
            solutions.append((a, b, c, d))
    assert solutions == [(h*h % 9, 0, 0, h*h % 9)]
    print("chord residues", h, solutions)

# Independent variables: N=B²+C²-4D, d_i²=N-(C+2i)².
pairs = []
for C, N in product(range(9), repeat=2):
    residues = tuple((N-(C+2*i)**2) % 9 for i in range(4))
    if all(v in R for v in residues):
        pairs.append((C, N, residues))
assert pairs == [(6, 1, (1, 0, 0, 1))]
print("center residues", pairs)

for h in range(1, 6):
    count = 0
    for a in range(1, 351):
        for b in range(1, 351):
            c2 = 2*b*b-a*a-8*h*h
            d2 = 3*b*b-2*a*a-24*h*h
            if min(c2, d2) <= 0:
                continue
            c, d = isqrt(c2), isqrt(d2)
            if c*c != c2 or d*d != d2 or max(c, d) > 350:
                continue
            count += 1
            if h % 3:
                assert b % 3 == c % 3 == 0
                assert a*a % 9 == d*d % 9 == h*h % 9
    print("finite exact chords", h, count)

h, ds = 3, (7, 11, 11, 7)
assert ds[0]**2-2*ds[1]**2+ds[2]**2 == -8*h*h
assert ds[1]**2-2*ds[2]**2+ds[3]**2 == -8*h*h
assert ds[1] % 3
print("h divisible by 3 counterexample:", ds)
print("ALL CHECKS PASSED")
