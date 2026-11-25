#!/usr/bin/env python3
"""Exact finite audits for the q6 18-candidate obstruction rigidity.

Proof for arbitrary reals is in proof.md. This is a finite independent audit.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb
import json


def profile(a):
    return Counter(x+y for x,y in combinations(a,2))


def h(p):
    return sum(v*v for v in p.values())


def e(p,q):
    return sum(v*q[s] for s,v in p.items())


def power_sum_recovery(a):
    n=len(a)
    q=[None]+[sum((x+y)**k for x,y in combinations(a,2)) for k in range(1,n+1)]
    p=[Fraction(n)]
    for k in range(1,n+1):
        lower=sum(comb(k,j)*p[j]*p[k-j] for j in range(1,k)) / 2
        p.append((q[k]-lower)/Fraction(n-2**(k-1)))
    assert p==[Fraction(sum(x**k for x in a)) for k in range(n+1)]


def main():
    sets=list(combinations(range(10),5))
    profiles=[profile(s) for s in sets]
    hist=Counter()
    for s in sets:power_sum_recovery(s)
    for i,pa in enumerate(profiles):
        ha=h(pa)
        for j,pb in enumerate(profiles):
            hb=h(pb)
            z=e(pa,pb)
            assert z != 15 and z <= 16
            if z==14:
                hist[(ha,hb)]+=1
                if ha==hb==14:
                    assert sets[i]==sets[j]
                elif ha==hb==16:
                    a,b=sets[i],sets[j]
                    assert len({a[k+1]-a[k] for k in range(4)})==1
                    assert len({b[k+1]-b[k] for k in range(4)})==1
                    assert a[1]-a[0]==b[1]-b[0]
                    assert 2*abs(a[0]-b[0])==a[1]-a[0]
                else:
                    assert {ha,hb}=={14,16}
                    assert sum(abs(pa[x]-pb[x]) for x in set(pa)|set(pb))==2
    result={'range':'all 5-subsets of {0,...,9}',
            'sets':len(sets),'ordered_pairs':len(sets)**2,
            'energy_14_classes':{f'{a},{b}':v for (a,b),v in sorted(hist.items())},
            'power_sum_recovery_checks':len(sets),
            'energy_15_cases':0,'assertions_passed':True}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
