#!/usr/bin/env python3
"""Exact 4x74 q=8 first nonlocal 19-stone correction."""
from collections import Counter
from itertools import combinations
from math import comb, isqrt

def B(n,k):
    return comb(n,k) if 0<=k<=n else 0

def circles(m):
    out={}
    for a in range(1,m):
        for b in range(1,m):
            if (a-b)%2: continue
            csq=2*b*b-a*a-8
            if csq<=0: continue
            c=isqrt(csq)
            if c*c!=csq or c>=m or (c-b)%2: continue
            dsq=2*c*c-b*b-8
            if dsq<=0: continue
            d=isqrt(dsq)
            if d*d!=dsq or d>=m or (d-c)%2: continue
            ds=(a,b,c,d)
            D=max(ds)
            for s in range(D,2*(m-1)-D+1):
                if (s-a)%2: continue
                points=frozenset((y,(s+sign*t)//2)
                                 for y,t in enumerate(ds) for sign in (-1,1))
                assert len(points)==8
                out[points]=ds
    return out

def safe19(m,circles):
    N,k=4*m,19
    C=list(circles)
    n=len(C)
    row=sum(B(m,a)*B(3*m,k-a) for a in range(8,m+1))
    rr=sum(B(m,a)*B(m,b)*B(2*m,k-a-b)
           for a in range(8,m+1) for b in range(8,m+1))
    rc=sum(B(m-2,a)*B(3*m-6,k-8-a) for a in range(6,m-1))
    cc=rcc=ccc=0
    overlap=Counter()
    for A,D in combinations(C,2):
        U=A|D
        u=len(U)
        overlap[16-u]+=1
        cc+=B(N-u,k-u)
        for y in range(4):
            t=sum(p[0]==y for p in U)
            rest_row=m-t
            rest_other=N-u-rest_row
            rcc+=sum(B(rest_row,a)*B(rest_other,k-u-a)
                     for a in range(max(0,8-t),min(rest_row,k-u)+1))
    for A,D,E in combinations(C,3):
        u=len(A|D|E)
        ccc+=B(N-u,k-u)
    return (B(N,k)-4*row-n*B(N-8,k-8)+6*rr+4*n*rc+cc-rcc-ccc,
            overlap,rcc,ccc)

def main():
    for m,target in [(8,325136492),(9,7969734820),(10,119338627316)]:
        C=circles(m)
        assert len(C)==m-3 and safe19(m,C)[0]==target
    C=circles(74)
    pats=Counter(C.values())
    assert pats=={(1,3,3,1):71,(35,51,63,73):1,(73,63,51,35):1}
    local=[s for s,ds in C.items() if ds==(1,3,3,1)]
    new=[s for s,ds in C.items() if ds!=(1,3,3,1)]
    cross=Counter(len(A&D) for A in new for D in local)
    assert cross=={0:118,1:24} and not new[0]&new[1]
    equations=[lambda x,y:x*x+y*y-73*x-345*y+1026,
               lambda x,y:x*x+y*y-73*x+339*y]
    hits={frozenset((y,x) for y in range(4) for x in range(74)
                    if f(x,y)==0) for f in equations}
    assert hits==set(new)
    baseline,_,br,bc=safe19(74,local)
    exact,pairs,rcc,ccc=safe19(74,C)
    assert bc==ccc==0 and pairs=={0:2466,1:24,2:138}
    assert rcc-br==72*B(70,4)
    R=sum(B(72,a)*B(216,11-a) for a in range(6,73))
    delta=-2*B(288,11)+8*R+119*B(280,3)+24*B(281,4)-72*B(70,4)
    assert delta==exact-baseline==-40801181949886698480
    assert baseline==295248500428508218666508077236
    assert exact==295248500387707036716621378756
    print('circles:',dict(pats))
    print('new/local overlaps:',dict(cross))
    print('local-only safe19:',baseline)
    print('nonlocal correction:',delta)
    print('exact safe19:',exact)
    print('all checks OK')

if __name__=='__main__':
    main()
