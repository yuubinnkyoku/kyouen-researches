#!/usr/bin/env python3
"""Exact integer-square-root audit of the 32-row witness, all widths 301..310."""
from math import isqrt

def rows_for_width(w):
    ans=[]
    for y in range(w):
        delta=1-4*(y*y-235*y-6)
        if delta <= 0: continue
        r=isqrt(delta)
        if r*r != delta or r%2 != 1: continue
        x1=(-1-r)//2
        x2=(-1+r)//2
        assert x1 != x2
        assert x1*x1+y*y+x1-235*y-6 == 0
        assert x2*x2+y*y+x2-235*y-6 == 0
        ans.append(y)
    return ans

expected=[0,1,3,4,10,15,22,25,45,49,60,70,87,91,102,115,
          120,133,144,148,165,175,186,190,210,213,220,225,231,232,234,235]
for w in range(301,311):
    rows=rows_for_width(w)
    assert rows==expected, (w,rows)
print('PASS 301..310: exactly 32 double-hit rows on x^2+y^2+x-235y-6=0')
