#!/usr/bin/env python3
"""Independent direct pairwise intersection verifier, q=4,5, small square grids."""
from collections import Counter, defaultdict
from itertools import combinations
from math import comb
import json
from fractions import Fraction
from math import gcd


def forbidden(points, ids):
    a, b, c, d = (points[i] for i in ids[:4])
    x1, y1 = b[0]-a[0], b[1]-a[1]
    x2, y2 = c[0]-a[0], c[1]-a[1]
    x3, y3 = d[0]-a[0], d[1]-a[1]
    z1, z2, z3 = x1*x1+y1*y1, x2*x2+y2*y2, x3*x3+y3*y3
    return z1*(x2*y3-y2*x3)+z2*(x3*y1-y3*x1)+z3*(x1*y2-y1*x2) == 0


def support_curve(points, e):
    p0, p1, p2 = (points[i] for i in e[:3])
    dx1,dy1=p1[0]-p0[0],p1[1]-p0[1]
    dx2,dy2=p2[0]-p0[0],p2[1]-p0[1]
    det=dx1*dy2-dy1*dx2
    if det == 0:
        aa,bb=dy1,-dx1
        cc=-(aa*p0[0]+bb*p0[1])
        g=gcd(gcd(abs(aa),abs(bb)),abs(cc))
        aa,bb,cc=aa//g,bb//g,cc//g
        if (aa,bb,cc)<(0,0,0):aa,bb,cc=-aa,-bb,-cc
        return ('line',aa,bb,cc)
    rhs1=p1[0]**2+p1[1]**2-p0[0]**2-p0[1]**2
    rhs2=p2[0]**2+p2[1]**2-p0[0]**2-p0[1]**2
    ux=Fraction(rhs1*dy2-dy1*rhs2,2*det)
    uy=Fraction(dx1*rhs2-rhs1*dx2,2*det)
    radius=(Fraction(p0[0])-ux)**2+(Fraction(p0[1])-uy)**2
    return ('circle',ux,uy,radius)


def on_curve(point, key):
    x,y=point
    if key[0]=='line':
        return key[1]*x+key[2]*y+key[3]==0
    _,ux,uy,r2=key
    return (x-ux)**2+(y-uy)**2==r2


def run(n, q):
    pts = [(x,y) for y in range(n) for x in range(n)]
    # For q>=4, each q-tuple is forbidden iff all four-subsets have zero determinant.
    edges = [t for t in combinations(range(n*n), q)
             if all(forbidden(pts, u) for u in combinations(t, 4))]
    masks = [sum(1 << i for i in e) for e in edges]
    hist = [0]*q
    for i, a in enumerate(masks):
        for b in masks[i+1:]:
            hist[(a & b).bit_count()] += 1
    incidence = [Counter() for _ in range(q)]
    for e in edges:
        for t in range(q):
            for s in combinations(e,t):
                incidence[t][s] += 1
    moments = [sum(comb(d,2) for d in counts.values()) for counts in incidence]
    recovered = [sum((-1)**(t-j)*comb(t,j)*moments[t] for t in range(j,q)) for j in range(q)]
    assert recovered == hist, (n,q,hist,recovered)
    curves={support_curve(pts,e) for e in edges}
    sizes=[sum(on_curve(p,c) for p in pts) for c in curves]
    # Distinct circles/lines meeting in >=3 points are impossible.
    # Hence the j>=3 intersection histogram is curve-local.
    for j in range(3,q):
        predicted=sum(comb(k,q)*comb(q,j)*comb(k-q,q-j)//2
                      for k in sizes if k>=q)
        assert predicted==hist[j], (n,q,j,predicted,hist[j])
    return {'n':n,'q':q,'forbidden':len(edges),'moments':moments,'histogram':hist}


if __name__ == '__main__':
    result=[run(n,q) for n,q in [(3,4),(4,4),(5,4),(4,5),(5,5)]]
    print(json.dumps(result,ensure_ascii=False,indent=2))
