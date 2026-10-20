#!/usr/bin/env python3
"""Exact integer audit of pair-sum multiset nonuniqueness at powers of two."""
from collections import Counter
from itertools import combinations
from math import comb
import json


def sums(xs):
    return Counter(a+b for a,b in combinations(xs,2))


def next_pair(a,b):
    assert len(a)==len(b) and sums(a)==sums(b)
    # Both sets start at zero; a large gap ensures two disjoint blocks.
    shift = max(a+b) + 11
    x = sorted(a + [z+shift for z in b])
    y = sorted(b + [z+shift for z in a])
    delta = min(x+y)
    return [z-delta for z in x], [z-delta for z in y]


def newton_audit(xs):
    n = len(xs)
    power = [n]+[sum(x**k for x in xs) for k in range(1,n+1)]
    hist = sums(xs)
    q = [None]+[sum(mult*(s**k) for s,mult in hist.items()) for k in range(1,n+1)]
    for k in range(1,n+1):
        assert 2*q[k] == (2*n-2**k)*power[k] + sum(comb(k,j)*power[j]*power[k-j] for j in range(1,k))


def main():
    a,b = [0,3],[1,2]
    records=[]
    for n in (2,4,8,16,32):
        assert len(a)==len(b)==n and a!=b and len(set(a))==len(a) and len(set(b))==len(b)
        assert sums(a)==sums(b)
        newton_audit(a)
        newton_audit(b)
        records.append({'n':n,'A':a,'B':b,'pair_sums':sum(sums(a).values()),'equal':True})
        a,b=next_pair(a,b)
    # The n=4 base can also be explained by complementing pairs of four points.
    c=[0,1,4,7]
    total=sum(c)
    d=sorted(total//2-x for x in c)
    assert c!=d and sums(c)==sums(d)
    records.append({'n':4,'A':c,'B':d,'method':'four-point complement'})
    # A finite audit, not the proof of uniqueness.
    checked={}
    for n in (3,5,6):
        seen={}
        for xs in combinations(range(11),n):
            sig=tuple(sorted(sums(xs).items()))
            assert sig not in seen, (n,xs,seen.get(sig))
            seen[sig]=xs
        checked[n]=len(seen)
    result={'witnesses':records,'finite_unique_checks':checked,'scope':'witnesses exact; uniqueness for all n not power of 2 follows from Newton identity'}
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
