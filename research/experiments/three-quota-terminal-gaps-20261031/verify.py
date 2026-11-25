#!/usr/bin/env python3
"""Pointwise audit of sunflower quotas and an integer-plane q=4 example."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from math import comb, prod

POINTS = ((0,0),(2,0),(6,-6),(-4,-6),(6,-4),(2,-6),(4,-2),(-2,-4),(3,3),(-1,1),(0,4))
CARRIERS = (frozenset((0,1,2,3,4)),frozenset((0,1,5,6,7)),frozenset((0,1,8,9,10)))

def det4(rows):
    def sign(p):
        return -1 if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2 else 1
    return sum(sign(p)*prod(rows[i][p[i]] for i in range(4)) for p in permutations(range(4)))

def geometry():
    bad = set()
    for ids in combinations(range(11),4):
        rows = [(x*x+y*y,x,y,1) for x,y in (POINTS[i] for i in ids)]
        if det4(rows)==0: bad.add(frozenset(ids))
    expected = set()
    for group in CARRIERS:
        expected.update(frozenset(c) for c in combinations(group,4))
    assert bad==expected and len(bad)==15, (bad-expected,expected-bad)
    return tuple(sum(1<<i for i in b) for b in bad)

def formula(c, xs, ps, z):
    out=Counter()
    for j in range(min(c,*ps)+1):
        out[z+sum(ps)-(len(ps)-1)*j] += comb(c,j)*prod(comb(x,p-j) for x,p in zip(xs,ps))
    return out

def brute(c, xs, ps, z):
    n=c+sum(xs)+z
    masks=[]
    pos=c
    for x in xs:
        masks.append(((1<<c)-1)|(((1<<x)-1)<<pos))
        pos+=x
    out=Counter()
    for s in range(1<<n):
        if any((s&m).bit_count()>p for m,p in zip(masks,ps)): continue
        if all(any(((s|(1<<i))&m).bit_count()>p for m,p in zip(masks,ps))
               for i in range(n) if not (s>>i)&1):
            out[s.bit_count()]+=1
    return out

def abstract_audit():
    count=0
    for r in (2,3,4):
        for ps in product((1,2),repeat=r):
            for extra in product((0,1),repeat=r):
                xs=tuple(p+e for p,e in zip(ps,extra))
                for c in range(3):
                    for z in range(2):
                        assert brute(c,xs,ps,z)==formula(c,xs,ps,z), (c,xs,ps,z)
                        count+=1
    assert count==2016
    return count

def planar_audit():
    bad=geometry()
    safe=[s for s in range(1<<11) if all((s&b)!=b for b in bad)]
    counts=Counter()
    for s in safe:
        if all(any(((s|(1<<i))&b)==b for b in bad)
               for i in range(11) if not (s>>i)&1):
            counts[s.bit_count()]+=1
    assert counts==Counter({5:27,7:54,9:1})==formula(2,(3,3,3),(3,3,3),0)
    @lru_cache(None)
    def solve(s):
        children=[solve(s|(1<<i)) for i in range(11)
                  if not (s>>i)&1 and all(((s|(1<<i))&b)!=b for b in bad)]
        if not children: return (0,1)
        def mex(v):
            k=0
            while k in v: k+=1
            return k
        return mex({a for a,b in children}),mex({b for a,b in children})
    for s in safe:
        assert solve(s)==((9-s.bit_count())%2,(8-s.bit_count())%2),s
    assert solve(0)==(1,0)
    assert all(solve(1<<i)==(0,1) for i in range(11))
    assert len(safe)==1262 and sum(counts.values())==82
    return len(bad),len(safe),sum(counts.values())

if __name__=="__main__":
    a=abstract_audit()
    b,s,t=planar_audit()
    print(f"PASS abstract={a} cases; planar forbidden4={b}; safe={s}; maximal={t}; g(empty)=1, h(empty)=0")
