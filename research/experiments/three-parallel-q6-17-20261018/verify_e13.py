#!/usr/bin/env python3
"""Independent Python exact audits for the E=13 obstruction in q=6.

Symbolic coordinates are coefficient pairs (constant, coefficient of t),
so generic verification does not sample floating-point values.
"""
from itertools import combinations, product
from collections import Counter
from math import gcd
import json


def add(x,y): return (x[0]+y[0],x[1]+y[1])
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
def twice(x): return (2*x[0],2*x[1])


def family(k):
    gaps = [[(1,0),(0,1),(1,0),(1,0)],
            [(1,0),(0,1),(1,0),(0,1)],
            [(1,0),(0,1),(1,0),(1,1)]][k]
    out=[(0,0)]
    for g in gaps: out.append(add(out[-1],g))
    return tuple(out)


def psum(x):
    return Counter(add(x[i],x[j]) for i,j in combinations(range(5),2))

def E(x,y):
    a,b=psum(x),psum(y)
    return sum(n*b[s] for s,n in a.items())

def H(x): return sum(n*n for n in psum(x).values())


def generic_audit():
    report=[]
    for k in range(3):
        B=family(k); B2=tuple(twice(v) for v in B)
        S=tuple(psum(B))
        twiceS={twice(s) for s in S}
        seen=set(); hits=[]
        for a,b,c in product(S,repeat=3):
            x=sub(add(a,b),c)
            y=sub(add(a,c),b)
            z=sub(add(b,c),a)
            if len({x,y,z})!=3: continue
            for d in S:
                w=sub(twice(d),x)
                if w in (x,y,z): continue
                if sum(add(w,v) in twiceS for v in (x,y,z))<2:continue
                for e in S:
                    v=sub(twice(e),x)
                    if v in (x,y,z,w): continue
                    C=tuple(sorted((x,y,z,w,v)))
                    if C in seen: continue
                    seen.add(C)
                    if E(B2,C)>=13: hits.append((C,E(B2,C),H(C)))
        assert len(seen)==544,(k,len(seen))
        assert hits==[(tuple(sorted(B2)),14,14)],(k,hits)
        report.append({'family':k,'symbolic_candidates':len(seen),
                       'E_ge_13':[{'E':14,'H':14,'C_equals_B':True}]})
    return report


def num_family(k,p,q):
    ds=[[q,p,q,q],[q,p,q,p],[q,p,q,q+p]][k]
    B=[0]
    for d in ds:B.append(B[-1]+d)
    return tuple(B)

def pair_sums(x):return [x[i]+x[j] for i,j in combinations(range(5),2)]
def numH(x):return sum(v*v for v in Counter(pair_sums(x)).values())


def circle_pairs(B,C2):
    out=[]
    for i,j in combinations(range(5),2):
        for k,l in combinations(range(5),2):
            if 2*(B[i]+B[j])==C2[k]+C2[l]:
                out.append(((1<<i)|(1<<j),(1<<k)|(1<<l)))
    return out

def four_compatible(B,C2):
    cs=circle_pairs(B,C2)
    for q in combinations(cs,4):
        if all((x[0]&y[0]).bit_count()+(x[1]&y[1]).bit_count()==1
               for x,y in combinations(q,2)):
            return True
    return False


def rational_audit():
    seen=set();tested=hits=0;per_family=[]
    for k in range(3):
        local=0
        for p in range(1,37):
            for q in range(1,25):
                if gcd(p,q)!=1: continue
                B=num_family(k,p,q)
                if numH(B)!=14: continue
                prof=Counter(pair_sums(B)); S=tuple(prof)
                support={2*s for s in S}
                for a,b,c in product(S,repeat=3):
                    x,y,z=a+b-c,a+c-b,b+c-a
                    if len({x,y,z})!=3:continue
                    for d in S:
                        w=2*d-x
                        if w in (x,y,z):continue
                        first=(x,y,z,w)
                        if sum(first[i]+first[j] in support
                               for i,j in combinations(range(4),2))<5:continue
                        for e in S:
                            v=2*e-x
                            if v in first:continue
                            C=tuple(sorted((*first,v)));tested+=1
                            vals=pair_sums(C)
                            energy=sum(prof[s//2] for s in vals if s%2==0)
                            if energy!=13:continue
                            if sum(n*n for n in Counter(vals).values())!=14:continue
                            hits+=1;local+=1
                            key=(k,p,q,C)
                            if key not in seen:
                                assert not four_compatible(B,C),key
                                seen.add(key)
        per_family.append(local)
    assert per_family==[0,0,60],per_family
    assert tested==6173662,tested
    assert hits==60 and seen=={(2,1,1,(-2,2,4,6,8))},seen
    return {'rational_candidates_after_safe_pruning':tested,
            'matching_labeled_cases':hits,
            'unique_normalized_cases':len(seen),
            'family_hit_counts':per_family,
            'compatible_four_circle_sets':0}


def ap_audit():
    # C={0,1,2,3,4}; B has >=8 integral sums from C.
    C=(0,2,4,6,8)
    pC=Counter(pair_sums(C))
    candidates=0; hits=[]
    for pool in (range(-10,19,2),range(-9,18,2)):
        for B in combinations(pool,5):
            candidates+=1
            pB=Counter(pair_sums(B))
            en=sum(n*pC[s] for s,n in pB.items())
            if en==13:
                assert sum(n*n for n in pB.values())==14
                hits.append(B)
                assert not four_compatible(C,tuple(2*x for x in B))
    assert candidates==5005
    expected=[(-2,0,2,6,8),(-2,0,4,6,8),
              (0,2,4,8,10),(0,2,6,8,10),
              (-1,1,3,5,9),(-1,1,3,7,9),
              (-1,1,5,7,9),(-1,3,5,7,9)]
    assert hits==expected,hits
    return {'ap_partner_candidates':candidates,
            'energy13_partner_shapes':len(hits),
            'H12_H16_energy13_cases':0,
            'compatible_four_circle_sets':0}


if __name__=='__main__':
    result={'generic':generic_audit(),
            'rational':rational_audit(),
            'ap':ap_audit(),
            'status':'all exact assertions passed'}
    print(json.dumps(result,ensure_ascii=False,indent=2))
