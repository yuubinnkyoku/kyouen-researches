#!/usr/bin/env python3
"""Exact modular audit for tangent-row circle bounds, no external dependencies."""
from collections import Counter
from itertools import combinations
from math import gcd

SQUARE16 = {x*x % 16 for x in range(16)}
SQUARE9 = {x*x % 9 for x in range(9)}

# Independent residue methods: direct row-mask and allowed-parameter intersection.
def tangent_mask(w, k, t):
    return frozenset(i for i in range(w) if i != k and
                     ((i-k)*(t-(i-k))) % 16 in SQUARE16)

def tangent_max(w):
    return max(len(tangent_mask(w, k, t))
               for k in range(w) for t in range(16))

def tangent_max_independent(w):
    # Loop over all rows first, then intersect sets of admissible t residues.
    possible = [set(range(16)) for _ in range(w)]
    max_count = 0
    for k in range(w):
        by_t = Counter()
        for i in range(w):
            if i == k:
                continue
            allowed = {t for t in range(16)
                       if ((i-k)*(t-(i-k))) % 16 in SQUARE16}
            for t in allowed:
                by_t[t] += 1
        max_count = max(max_count, max(by_t.values(), default=0))
    return max_count

T_SMALL = {5:4, 6:4, 7:5, 8:6, 9:6, 10:6, 11:7, 12:8, 13:8, 14:8}

def T(w):
    return T_SMALL[w] if w <= 14 else (w+1)//2

for w in range(5, 145):
    u = tangent_max(w)
    assert u == tangent_max_independent(w)
    if w >= 15:
        expected = T(w) - (1 if w % 8 in (0,1,5,7) else 0)
        assert u == expected, (w,u,expected)
    if w <= 17:
        print(f'w={w:2d} T={T(w):2d} tangent_mod16_max={u:2d} '
              f'circle_point_upper={2*T(w) if u < T(w) else 2*T(w)+2:2d}')

# Independently confirm the mod9 six-row cap on double rows.
assert max(sum((n-(c+2*i)**2) % 9 in SQUARE9 for i in range(6))
           for c in range(9) for n in range(9)) == 4

# Independent determinant-based finite grid audit. Does not prove the unbounded theorem.
def circle_key(p, q, r):
    x1,y1=p; x2,y2=q; x3,y3=r
    a=2*((x2-x1)*(y3-y1)-(y2-y1)*(x3-x1))
    if not a:
        return None
    u=x2*x2+y2*y2-x1*x1-y1*y1
    v=x3*x3+y3*y3-x1*x1-y1*y1
    b=-2*(u*(y3-y1)-v*(y2-y1))
    c=-2*((x2-x1)*v-(x3-x1)*u)
    d=-(a*(x1*x1+y1*y1)+b*x1+c*y1)
    z=gcd(gcd(abs(a),abs(b)),gcd(abs(c),abs(d)))
    a,b,c,d=(t//z for t in (a,b,c,d))
    if a<0:
        a,b,c,d=-a,-b,-c,-d
    return (a,b,c,d)

for w,m in [(5,12),(6,15),(7,11),(8,10),(9,9),(10,9)]:
    pts=[(x,y) for y in range(w) for x in range(m)]
    keys={circle_key(p,q,r) for p,q,r in combinations(pts,3)}
    keys.discard(None)
    maximum=0
    for a,b,c,d in keys:
        count=sum(a*(x*x+y*y)+b*x+c*y+d==0 for x,y in pts)
        maximum=max(maximum,count)
    limit=2*T(w) if tangent_max(w)<T(w) else 2*T(w)+2
    assert maximum<=limit,(w,m,maximum,limit)
    print(f'grid={w}x{m}: {len(keys)} exact circles, maximum={maximum}, theorem bound={limit}')
print('PASS: modular universal lemma and independent finite grid audits')
