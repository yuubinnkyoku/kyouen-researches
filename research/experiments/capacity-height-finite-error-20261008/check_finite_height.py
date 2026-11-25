#!/usr/bin/env python3
"""Independent backward/forward exact checks for finite-height correction."""
from collections import defaultdict, Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement

def children(x,h,r):
    result=[]
    for i,v in enumerate(x):
        y=list(x)
        y[i]+=1
        y.sort(reverse=True)
        if sum(y[:h]) <= r:
            result.append((v,tuple(y)))
    return result

def backward(x,h,r):
    @lru_cache(None)
    def solve(z):
        moves=children(z,h,r)
        if not moves: return ({z[h-1]:F(1)}, {z[h-1]:F(0)})
        k=len(moves)
        mean=F(sum(v for v,y in moves),k)
        p=defaultdict(F); d=defaultdict(F)
        for v,y in moves:
            py,dy=solve(y)
            for t, pp in py.items():
                p[t]+=pp/k
                d[t]+=dy[t]/k + pp*(mean-v)/k
        return dict(p),dict(d)
    return solve(x)

def forward(x,h,r,m=None):
    mass={x:(F(1),F(0))}
    probs=defaultdict(F); deriv=defaultdict(F)
    while mass:
        nxt=defaultdict(lambda:(F(0),F(0)))
        for z,(weight,slope) in mass.items():
            moves=children(z,h,r)
            if not moves:
                probs[z[h-1]]+=weight; deriv[z[h-1]]+=slope
                continue
            k=len(moves)
            mean=F(sum(v for v,y in moves),k)
            total=sum((m-v for v,y in moves)) if m is not None else None
            for v,y in moves:
                q=F(1,k) if m is None else F(m-v,total)
                a=F(mean-v,k) if m is None else F(0)
                pw,dw=nxt[y]
                nxt[y]=(pw+weight*q,dw+slope*q+weight*a)
        mass=dict(nxt)
    return dict(probs),dict(deriv)

def check():
    tested=0
    finite_checks=0
    thresholds=0
    strict_d=0
    for w in range(3,6):
        for h in range(2,w):
            n=w-h
            for r in range(1,6):
                for asc in combinations_with_replacement(range(r+1),w):
                    x=tuple(asc[::-1])
                    if sum(x[:h])>r: continue
                    pb,db=backward(x,h,r)
                    pf,df=forward(x,h,r)
                    assert pb==pf, (w,h,r,x,pb,pf)
                    assert db==df, (w,h,r,x,db,df)
                    assert sum(pb.values())==1 and sum(db.values())==0
                    assert all(v>0 for v in pb.values())
                    if any(v for v in db.values()): strict_d+=1
                    thresholds+=len(pb)
                    tested+=1
                    L=r+n*(r//h)-sum(x)
                    for m in [r+1,r+2,2*r+1,5*r+1]:
                        pm,_=forward(x,h,r,m)
                        assert set(pm)==set(pb)
                        tv=sum((abs(pm[t]-pb[t]) for t in pb),F(0))/2
                        bound=F(L*r,4*(m-r))
                        assert tv<=bound, (w,h,r,x,m,tv,bound)
                        finite_checks+=1
    x=(0,0,0); pb,db=backward(x,2,3)
    assert pb=={0:F(1,9),1:F(8,9)},pb
    assert db=={0:F(-2,9),1:F(2,9)},db
    print("PASS positions",tested,"terminal entries",thresholds,
          "finite-height comparisons",finite_checks,"nonzero first-order",strict_d)
    print("EXAMPLE limit",pb,"first-order coefficient",db)
if __name__=="__main__":check()
