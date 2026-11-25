#!/usr/bin/env python3
"""Independently check the sharp 471-row, gcd=2 integer-circle witness."""
from math import gcd, isqrt
from functools import reduce

N = 55250
hits = []
for y in range(-235, 236):
    x2 = N - y*y
    if x2 <= 0:
        continue
    x = isqrt(x2)
    if x > 0 and x*x == x2:
        assert x*x+y*y == N and (-x)*(-x)+y*y == N
        hits.append((y,x))
ys = [y for y,x in hits]
assert len(hits) == 32
assert ys[0] == -235 and ys[-1] == 235
assert reduce(gcd,(y-ys[0] for y in ys[1:]),0) == 2
assert len(set(ys)) == 32
assert all(y % 2 and x % 2 for y,x in hits)
print('PASS N=55250, 32 double-hit rows, width=471, row-difference gcd=2')
print('rows:', ','.join(map(str,ys)))
