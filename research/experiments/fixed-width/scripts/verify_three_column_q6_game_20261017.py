#!/usr/bin/env python3
"""Independent q=6 forbidden-set and full-state Grundy audit for h=1,d=2,m=6."""
from itertools import combinations
from functools import lru_cache

h,d,m,q=1,2,6,6
pts=[(i*h,j*d) for i in range(3) for j in range(m)]
n=len(pts)

def cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def on_circle(inds):
    p=[pts[k] for k in inds]
    t=next(((a,b,c) for a,b,c in combinations(range(6),3) if cross(p[a],p[b],p[c])),None)
    if t is None: return False
    a,b,c=[p[k] for k in t]
    x1,y1=a; x2,y2=b; x3,y3=c
    D=cross(a,b,c)
    # Solve 2*(x2-x1)*cx+2*(y2-y1)*cy=z2-z1, etc.
    z=lambda v:v[0]**2+v[1]**2
    U=(z(b)-z(a))*(y3-y1)-(z(c)-z(a))*(y2-y1)
    V=(x2-x1)*(z(c)-z(a))-(x3-x1)*(z(b)-z(a))
    # 2D*cx=U, 2D*cy=V. Radius equality for all points.
    return all(D*(z(v)-z(a))==U*(v[0]-x1)+V*(v[1]-y1) for v in p)

forbidden=[]
for inds in combinations(range(n),q):
    pp=[pts[k] for k in inds]
    if all(cross(pp[0],pp[1],v)==0 for v in pp[2:]) or on_circle(inds):
        forbidden.append(sum(1<<i for i in inds))
expected={sum(1<<(i*m+j) for j in range(m)) for i in range(3)}
assert set(forbidden)==expected,(len(forbidden),forbidden)

@lru_cache(None)
def grundy(s):
    succ=[]
    for k in range(n):
        if s>>k&1: continue
        t=s|(1<<k)
        if any((t&f)==f for f in forbidden): continue
        succ.append(grundy(t))
    return next(v for v in range(n+1) if v not in succ)

states=0
for s in range(1<<n):
    if any((s&f)==f for f in forbidden):continue
    assert grundy(s)==(15-s.bit_count())%2,(s,grundy(s))
    states+=1
assert states==63**3,states
print('h=1,d=2,m=6,q=6: exactly 3 forbidden six-sets, all vertical')
print(f'full safe-state mex audit: {states} safe states, all match g=(15-|S|) mod 2')
