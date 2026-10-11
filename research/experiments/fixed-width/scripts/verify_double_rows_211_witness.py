#!/usr/bin/env python3
"""Integer-only independent lower witness check for first T(w)=25 at w=211."""
from math import isqrt

def double_rows(w, C, D):
    result = []
    for y in range(w):
        disc = 1 - 4 * (y*y + C*y + D)
        if disc <= 0:
            continue
        r = isqrt(disc)
        if r*r != disc or r % 2 == 0:
            continue
        xs = ((-1-r)//2, (-1+r)//2)
        assert xs[0] != xs[1]
        for x in xs:
            assert x*x + y*y + x + C*y + D == 0
        result.append(y)
    return result

EXPECTED = [0,1,3,4,10,15,22,25,45,49,60,70,87,91,102,115,120,133,144,148,165,175,186,190,210]
assert double_rows(211,-235,-6) == EXPECTED
assert double_rows(210,-235,-6) == EXPECTED[:-1]
assert len(double_rows(210,-105,-6)) == 24
print('PASS witness T(211)>=25; T(210)>=24')
