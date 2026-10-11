#!/usr/bin/env python3
"""Independent integer-arithmetic checks for C4 symmetry congruences."""
from collections import Counter
from itertools import combinations
from math import comb
import json


def det3(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def concyclic(a,b,c,d):
    # Integer incircle determinant, translated to a.
    bx,by=b[0]-a[0],b[1]-a[1]
    cx,cy=c[0]-a[0],c[1]-a[1]
    dx,dy=d[0]-a[0],d[1]-a[1]
    return ((bx*bx+by*by)*(cx*dy-cy*dx)
            -(cx*cx+cy*cy)*(bx*dy-by*dx)
            +(dx*dx+dy*dy)*(bx*cy-by*cx))==0


def classify(points):
    if all(det3(points[0],points[1],p)==0 for p in points[2:]):
        return 'line'
    a=points[0]
    for b,c in combinations(points[1:],2):
        if det3(a,b,c):
            break
    return 'circle' if all(concyclic(a,b,c,p) for p in points) else None


def rotate(p): return (-p[1],p[0])


def prediction(points,q):
    P=set(points)
    assert all(rotate(p) in P for p in P)
    delta=int((0,0) in P)
    # Canonical antipodal representatives.
    pairs=[p for p in P if p!=(0,0) and p<(-p[0],-p[1])]
    a=Counter(p[0]*p[0]+p[1]*p[1] for p in pairs)
    # Canonical direction: divide by gcd, modulo sign.
    from math import gcd
    b=Counter()
    for x,y in pairs:
        g=gcd(abs(x),abs(y))
        dx,dy=x//g,y//g
        if (dx,dy)>(-dx,-dy): dx,dy=-dx,-dy
        b[(dx,dy)]+=1
    seen=set()
    c=Counter()
    for p in P:
        if p==(0,0) or p in seen: continue
        orb=set(); z=p
        for _ in range(4): orb.add(z);z=rotate(z)
        seen.update(orb)
        c[p[0]*p[0]+p[1]*p[1]]+=1
    def C(n,k): return comb(n,k) if 0<=k<=n else 0
    if q%2==0:
        cm4=sum(C(v,q//2) for v in a.values())%4
        hm4=sum(C(v,q//2) for v in b.values())%4
    else:
        cm4=0
        hm4=delta*sum(C(v,(q-1)//2) for v in b.values())%4
    cm2=sum(C(v,q//4) for v in c.values())%2 if q%4==0 else 0
    return {'circle_mod4':cm4,'line_mod4':hm4,'circle_mod2':cm2,'line_mod2':0}


def audit(points, qs):
    P=sorted(points)
    ans={}
    for q in qs:
        actual=Counter(classify(t) for t in combinations(P,q))
        pred=prediction(P,q)
        assert actual['circle']%4==pred['circle_mod4'],(P,q,actual,pred)
        assert actual['line']%4==pred['line_mod4'],(P,q,actual,pred)
        assert actual['circle']%2==pred['circle_mod2'],(P,q,actual,pred)
        assert actual['line']%2==pred['line_mod2'],(P,q,actual,pred)
        ans[q]={'circle':actual['circle'],'line':actual['line'],'predicted':pred}
    return ans


def main():
    cases=0
    examples={}
    # All 16 C4 orbit subsets of a 5x5 centered square (5 noncentral orbits)
    full={(x,y) for x in range(-2,3) for y in range(-2,3)}
    orbit=[];used=set()
    for p in sorted(full):
        if p in used or p==(0,0):continue
        o=set();z=p
        for _ in range(4):o.add(z);z=rotate(z)
        used.update(o);orbit.append(o)
    assert len(orbit)==6
    # Full 5x5, all q=4..8.
    examples['5x5']=audit(full,range(4,9));cases+=5
    # All 2^6 orbit selections with center optionally, only sizes <= 13 for cheap exhaustive q.
    for mask in range(1<<6):
        base=set().union(*(orbit[i] for i in range(6) if mask>>i&1))
        if len(base)>12:continue
        for center in (False,True):
            pts=base|({(0,0)} if center else set())
            for q in range(4,min(len(pts),9)+1):
                audit(pts,[q]);cases+=1
    # More asymmetric rotation-symmetric sets; C4 action but not reflection-invariant.
    seeds=[(1,2),(2,3),(1,4),(3,5)]
    for mask in range(1,1<<len(seeds)):
        pts=set()
        for i,p in enumerate(seeds):
            if mask>>i&1:
                z=p
                for _ in range(4):pts.add(z);z=rotate(z)
        if len(pts)>12:continue
        for center in (False,True):
            t=pts|({(0,0)} if center else set())
            for q in range(4,min(len(t),9)+1):
                audit(t,[q]);cases+=1
    result={'checked_q_instances':cases,'full_5x5':examples['5x5'],'method':'all q-subsets, direct integer determinant and collinearity; independent orbit formula'}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
