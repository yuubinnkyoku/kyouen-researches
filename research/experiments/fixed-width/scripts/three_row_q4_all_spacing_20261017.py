#!/usr/bin/env python3
"""Exact symbolic certificate and independent 9-point game audit for 3x3 q=4.

No external packages. The 4-point circle determinant is expanded as a polynomial
in positive integers a,b,d; division and sign checks are exact integer algebra.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from fractions import Fraction

ZERO = {}

def poly(n=0, mon=(0,0,0)):
    return {mon: Fraction(n)} if n else {}

def add(p, q):
    r=p.copy()
    for k,v in q.items():
        r[k]=r.get(k,0)+v
        if not r[k]: del r[k]
    return r

def neg(p):return {k:-v for k,v in p.items()}
def sub(p,q):return add(p,neg(q))
def mul(p,q):
    r={}
    for k,v in p.items():
        for h,w in q.items():
            t=tuple(x+y for x,y in zip(k,h))
            r[t]=r.get(t,0)+v*w
    return {k:v for k,v in r.items() if v}

def divexact(p,q):
    """Single-divisor lexicographic polynomial division; return quotient or None."""
    rem=p.copy(); out={}
    lead=max(q); lc=q[lead]
    while rem:
        m=max(rem)
        if any(x<y for x,y in zip(m,lead)):
            return None
        t=tuple(x-y for x,y in zip(m,lead))
        term=poly(rem[m]/lc,t)
        out=add(out,term)
        rem=sub(rem,mul(term,q))
    return out

def definite(p):
    return bool(p) and (all(v>0 for v in p.values()) or all(v<0 for v in p.values()))

A=poly(1,(1,0,0)); B=poly(1,(0,1,0)); D=poly(1,(0,0,1))
AB=mul(A,B); d2=mul(D,D); apb=add(A,B)
conditions=[sub(AB,d2),sub(AB,mul(poly(2),d2)),
            sub(mul(A,apb),d2),sub(mul(A,apb),mul(poly(2),d2)),
            sub(mul(B,apb),d2),sub(mul(B,apb),mul(poly(2),d2))]
points=[(x,mul(poly(y),D)) for x in (ZERO,A,apb) for y in range(3)]

def symbolic_circle_det(c):
    rows=[]
    for i in c:
        x,y=points[i]
        rows.append([add(mul(x,x),mul(y,y)),x,y])
    r=[[sub(rows[k][t],rows[0][t]) for t in range(3)] for k in range(1,4)]
    (a,b,c),(d,e,f),(g,h,i)=r
    return add(sub(mul(a,sub(mul(e,i),mul(f,h))),mul(b,sub(mul(d,i),mul(f,g)))),
               mul(c,sub(mul(d,h),mul(e,g))))

def symbolic_edges():
    base=[]; by_condition=[[] for _ in range(6)]; strictly_positive=0
    for c in combinations(range(9),4):
        p=symbolic_circle_det(c); mask=sum(1<<i for i in c)
        if not p:base.append(mask);continue
        if definite(p):strictly_positive+=1;continue
        matches=[j for j,q in enumerate(conditions) if (quot:=divexact(p,q)) is not None and definite(quot)]
        assert len(matches)==1, (c,p,matches)
        by_condition[matches[0]].append(mask)
    assert len(base)==9 and list(map(len,by_condition))==[1,8,4,2,4,2]
    assert strictly_positive==96, strictly_positive
    return base,by_condition

def numerical_edges(a,b,d):
    p=[(x,y*d) for x in (0,a,a+b) for y in range(3)]
    edges=[]
    for c in combinations(range(9),4):
        r=[[p[i][0]**2+p[i][1]**2,p[i][0],p[i][1]] for i in c]
        r=[[r[k][t]-r[0][t] for t in range(3)] for k in range(1,4)]
        (x,y,z),(u,v,w),(h,i,j)=r
        det=x*(v*j-w*i)-y*(u*j-w*h)+z*(u*i-v*h)
        if det==0:edges.append(sum(1<<i for i in c))
    return sorted(edges)

def independent_bottom_up(edges):
    """Separate non-recursive dynamic program over all 512 subsets."""
    safe=[all(mask&e!=e for e in edges) for mask in range(512)]
    values={}
    for count in range(9,-1,-1):
        for mask in range(512):
            if not safe[mask] or mask.bit_count()!=count:
                continue
            options=set()
            for i in range(9):
                if not(mask>>i&1) and safe[mask|1<<i]:
                    options.add(values[mask|1<<i])
            nimber=0
            while nimber in options:
                nimber+=1
            values[mask]=nimber
    return values

def signature(a,b,d):
    return sum(int(test)<<j for j,test in enumerate((a*b==d*d,a*b==2*d*d,
        a*(a+b)==d*d,a*(a+b)==2*d*d,b*(a+b)==d*d,b*(a+b)==2*d*d)))

def symbolic_forbidden(sig,base,by):
    return sorted(base+[e for j,edges in enumerate(by) if sig>>j&1 for e in edges])

def solve(edges):
    @lru_cache(None)
    def g(mask):
        opts=set()
        for i in range(9):
            bit=1<<i
            if mask&bit:continue
            nxt=mask|bit
            if all(nxt&e!=e for e in edges):opts.add(g(nxt))
        n=0
        while n in opts:n+=1
        return n
    safe=[m for m in range(512) if all(m&e!=e for e in edges)]
    hist=Counter(g(m) for m in safe)
    maximal=Counter(m.bit_count() for m in safe if all(any(((m|1<<i)&e)==e for e in edges)
                for i in range(9) if not(m>>i&1)))
    return g(0),tuple(g(1<<i) for i in range(9)),len(safe),hist,maximal,{m:g(m) for m in safe}

# In each case the six-bit signature is ordered as in 'conditions'.
# Pairwise simultaneous equations can only be realized for (a,b,d)=(t,t,t),
# giving bits 0,3,5. The six singleton signatures are all realizable.
representatives={0:(1,1,2),1:(1,4,2),2:(1,2,1),4:(1,3,2),
                 8:(1,7,2),16:(3,1,2),32:(1,8,6),41:(1,1,1)}

def main():
    base,by=symbolic_edges()
    print('Exact polynomial certificate: 126 four-subsets = 9 unconditional circles'
          ' + 21 conditional circles + 96 never circles')
    print('Conditional circle counts by six conditions:',list(map(len,by)))
    assert len(representatives)==8
    for sig,(a,b,d) in sorted(representatives.items()):
        assert signature(a,b,d)==sig
        predicted=symbolic_forbidden(sig,base,by)
        actual=numerical_edges(a,b,d)
        assert predicted==actual
        root,children,n,hist,maximal,values=solve(predicted)
        assert root==1 and children==(0,)*9,(sig,root,children)
        # Independent direct determinant geometry -> full 9-bit Grundy.
        assert independent_bottom_up(actual)==values
        print(f'sig={sig:06b} rep={(a,b,d)} circles4={len(actual)} '
              f'safe={n} root={root} first={children} '
              f'hist={dict(sorted(hist.items()))} terminal={dict(sorted(maximal.items()))}')
    counts=Counter()
    for a in range(1,17):
        for b in range(1,17):
            for d in range(1,17):
                sig=signature(a,b,d)
                assert sig in representatives,(a,b,d,sig)
                assert numerical_edges(a,b,d)==symbolic_forbidden(sig,base,by),(a,b,d)
                counts[sig]+=1
    print('Independent determinant sweep 1<=a,b,d<=16:',dict(sorted(counts.items())))
    print('PASS: all realizable 3x3 q=4 boards are first-player wins; all nine first moves win.')

if __name__=='__main__':main()
