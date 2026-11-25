#!/usr/bin/env python3
from itertools import combinations
from math import comb

def nk(m,w,a,b,k): return max(0,m-k*a)*max(0,w-k*b)
def closed(m,w,a,b):
    return 2*(3*nk(m,w,a,b,2)+sum(nk(m,w,a,b,k) for k in range(4,max(m,w)+1)))
def zero(m,w): return m*comb(w,2) if w>=3 else 0
def geometric(m,w,a,b,z=False):
    pts=[(x,y) for x in range(m) for y in range(w)]
    pairs=set()
    for t in combinations(pts,3):
        p,q,r=t
        dx=q[0]-p[0];dy=q[1]-p[1]
        if dx*(r[1]-p[1])!=dy*(r[0]-p[0]):continue
        if (dx!=0 if z else b*b*dx*dx!=a*a*dy*dy):continue
        pairs.update(combinations(t,2))
    return len(pairs)
def det3(t):
    return t[0][0]*(t[1][1]*t[2][2]-t[1][2]*t[2][1])-t[0][1]*(t[1][0]*t[2][2]-t[1][2]*t[2][0])+t[0][2]*(t[1][0]*t[2][1]-t[1][1]*t[2][0])
def minors(m,w,a,b,z=False):
    pts=[(x,y) for x in range(m) for y in range(w)]
    pairs=set()
    for t in combinations(pts,3):
        A=[(x*x if z else b*b*x*x-a*a*y*y,x,y,1) for x,y in t]
        if all(det3([[row[j] for j in cols] for row in A])==0 for cols in combinations(range(4),3)):
            pairs.update(combinations(t,2))
    return len(pairs)
if __name__=='__main__':
    ab=[(1,1),(2,1),(1,2),(3,2),(2,3)]
    for m in range(1,9):
        for w in range(1,8):
            for a,b in ab:assert geometric(m,w,a,b)==closed(m,w,a,b),(m,w,a,b)
            assert geometric(m,w,0,1,True)==zero(m,w),(m,w)
    for m in range(1,7):
        for w in range(1,6):
            for a,b in ab[:3]:assert minors(m,w,a,b)==closed(m,w,a,b),(m,w,a,b)
            assert minors(m,w,0,1,True)==zero(m,w),(m,w)
    assert closed(237,4,1,1)==2820
    print("PASS: 280+56 geometric cases; 90+30 independent rank-minor cases")
