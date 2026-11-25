#!/usr/bin/env python3
"""Exact random-legal-move terminal laws for exchangeable forbidden hypergraphs."""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from random import Random
from math import comb


def quotient_law(sizes, profiles, start=None):
    sizes=tuple(sizes)
    d=len(sizes)
    profiles={tuple(p) for p in profiles}
    start=tuple([0]*d if start is None else start)
    assert all(0<=a<=k for a,k in zip(start,sizes))
    def safe(a):
        return all(any(a[i]<p[i] for i in range(d)) for p in profiles)
    assert safe(start)
    # Forward propagation on the count-vector DAG; unlike the direct verifier,
    # this never recursively enumerates labelled subsets.
    mass={start:Fraction(1)}
    terminal={}
    states=sorted(product(*(range(start[i],sizes[i]+1) for i in range(d))),key=sum)
    for a in states:
        if a not in mass:continue
        nxt=[]
        for i in range(d):
            if a[i]==sizes[i]:continue
            b=list(a);b[i]+=1;b=tuple(b)
            if safe(b):nxt.append((b,sizes[i]-a[i]))
        if not nxt:
            terminal[a]=mass[a]
            continue
        w=sum(c for _,c in nxt)
        for b,c in nxt:
            mass[b]=mass.get(b,Fraction(0))+mass[a]*Fraction(c,w)
    return terminal



def direct_law(sizes, profiles, start=None):
    """Independent labelled subset recursion: no count-vector transitions."""
    n=sum(sizes)
    starts=[sum(sizes[:i]) for i in range(len(sizes))]
    if start is None:start=[0]*len(sizes)
    initial=0
    for i,a in enumerate(start):
        initial|=((1<<a)-1)<<starts[i]
    edges=[]
    for p in profiles:
        choices=[list(combinations(range(starts[i],starts[i]+sizes[i]),p[i])) for i in range(len(sizes))]
        for chosen in product(*choices):
            mask=0
            for c in chosen:
                for x in c:mask|=1<<x
            edges.append(mask)
    edges=set(edges)
    def safe(mask):return all((mask&e)!=e for e in edges)
    assert safe(initial)
    @lru_cache(None)
    def dp(mask):
        children=[]
        for v in range(n):
            if not (mask>>v)&1 and safe(mask|(1<<v)):
                children.append(mask|(1<<v))
        if not children:
            a=tuple((mask>>starts[i]&((1<<sizes[i])-1)).bit_count() for i in range(len(sizes)))
            return {a:Fraction(1)}
        ans={}
        for child in children:
            for a,p in dp(child).items():
                ans[a]=ans.get(a,Fraction(0))+p/len(children)
        return ans
    return dp(initial)


def test():
    rng=Random(20261020)
    count=0
    # Every forbidden hypergraph with <=3 vertices, represented by singleton classes.
    for n in range(1,5):
        nonempty=[tuple(int(i in edge) for i in range(n)) for k in range(1,n+1) for edge in combinations(range(n),k)]
        for mask in range(1<<len(nonempty)):
            P=[e for j,e in enumerate(nonempty) if (mask>>j)&1]
            a=quotient_law((1,)*n,P)
            b=direct_law((1,)*n,P)
            assert a==b,(n,mask,a,b)
            count+=1
    # Random profiles with nontrivial class sizes; total <=8 labelled vertices.
    for _ in range(400):
        d=rng.randrange(1,5)
        sizes=[rng.randrange(1,4) for _ in range(d)]
        if sum(sizes)>8:continue
        all_profiles=list(product(*(range(k+1) for k in sizes)))
        all_profiles.remove((0,)*d)
        P=rng.sample(all_profiles,rng.randrange(min(len(all_profiles),9)+1))
        a=quotient_law(sizes,P)
        b=direct_law(sizes,P)
        assert a==b,(sizes,P,a,b)
        count+=1
    sizes=(3,4,5,6)
    P=((1,1,0,0),(0,1,1,0),(0,0,1,1))
    law=quotient_law(sizes,P)
    assert law==direct_law(sizes,P)  # Independent full 18-vertex labelled audit.
    print('cases',count,'plus independent 18-vertex full-state audit')
    print('18-vertex terminal count vectors / exact probabilities:')
    for a,p in sorted(law.items()):print(a,'stones',sum(a),'probability',str(p),'decimal',float(p))
    print('expected terminal stones',sum(Fraction(sum(a))*p for a,p in law.items()))
    print('probability sum',sum(law.values()))
    assert sum(law.values())==1
    assert {sum(a) for a in law}=={8,9,10}

if __name__=='__main__':test()
