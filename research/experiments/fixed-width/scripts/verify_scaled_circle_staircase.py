#!/usr/bin/env python3
"""Exact integer audit of the N=55250 circle and its inert-prime dilations."""
import json
from math import gcd, isqrt
from functools import reduce

N = 55250

def base_rows():
    # Method A: enumerate all odd Gaussian second coordinates.
    bvals = [b for b in range(-isqrt(N), isqrt(N)+1)
             if b % 2 and (t := N-b*b)>0 and isqrt(t)**2 == t]
    assert len(bvals) == 32
    assert bvals == sorted(bvals)
    return [(b+235)//2 for b in bvals]

def direct_rows(g, height):
    # Method B: directly solve the scaled quadratic discriminant for each row.
    result=[]
    for y in range(height):
        delta = 55250*g*g-(2*y-235*g)**2
        if delta <= 0: continue
        s = isqrt(delta)
        if s*s != delta or (s-g)%2: continue
        x1=(-g-s)//2
        x2=(-g+s)//2
        assert x1 != x2
        for x in (x1,x2):
            assert x*x+y*y+g*x-235*g*y-6*g*g==0
        result.append(y)
    return result

base=base_rows()
assert direct_rows(1,236)==base
assert base[0]==0 and base[-1]==235
records=[]
for k in range(25,33):
    w,i=min(((base[j+k-1]-base[j]+1,j) for j in range(len(base)-k+1)))
    records.append(dict(k=k, w=w, y_min=base[i], y_max=base[i+k-1], count=sum(0<=y<w for y in base)))
    assert base[i]==0 and base[i+k-1]==w-1
assert [(r['k'],r['w']) for r in records]==[(25,211),(26,214),(27,221),(28,226),(29,232),(30,233),(31,235),(32,236)]
for g in [1,2,3,4,7,8,11,16]:
    rows=direct_rows(g,210*g+1)
    expected=[g*y for y in base if y<=210]
    assert rows==expected, (g,rows,expected)
    assert len(rows)==25
    assert reduce(gcd,(y-rows[0] for y in rows[1:]))==g
print(json.dumps({'N':N,'base_rows':base,'staircase':records,'dilation_g_tested':[1,2,3,4,7,8,11,16], 'full_circle_rows':len(base),'status':'PASS'},ensure_ascii=False,indent=2))
