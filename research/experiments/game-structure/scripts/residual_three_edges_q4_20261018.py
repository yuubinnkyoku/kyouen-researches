#!/usr/bin/env python3
"""Independent count-state audit for at most three minimal residual forbidden sets of size <=4."""
from __future__ import annotations
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import permutations, product
import json

CAP=4

def cases(k):
    # An incidence type t records membership in each of the k forbidden sets.
    for c in product(range(CAP+1), repeat=(1<<k)-1):
        sizes=[sum(c[t-1] for t in range(1,1<<k) if (t>>j)&1) for j in range(k)]
        if not all(1<=s<=CAP for s in sizes):continue
        # Keep only minimal (pairwise inclusion-incomparable) forbidden sets.
        if any(not any(c[t-1] and (t>>i&1) and not(t>>j&1) for t in range(1,1<<k))
               for i in range(k) for j in range(k) if i!=j):continue
        yield c

def permuted(c,perm):
    k=len(perm)
    out=[0]*((1<<k)-1)
    for t in range(1,1<<k):
        target=sum(((t>>j)&1)<<perm[j] for j in range(k))
        out[target-1]=c[t-1]
    return tuple(out)

def grundy(c,k):
    @lru_cache(None)
    def g(r):
        # r is the number of remaining vertices in each incidence class.
        assert all(sum(r[t-1] for t in range(1,1<<k) if (t>>j)&1)>0 for j in range(k))
        values=set()
        for j in range(len(r)):
            if not r[j]:continue
            nxt=list(r);nxt[j]-=1
            if any(not sum(nxt[t-1] for t in range(1,1<<k) if (t>>i)&1) for i in range(k)):
                continue
            values.add(g(tuple(nxt)))
        mex=0
        while mex in values:mex+=1
        return mex
    # Enumerate all safe residual count vectors to establish the global bound.
    for r in product(*(range(v+1) for v in c)):
        if all(sum(r[t-1] for t in range(1,1<<k) if (t>>i)&1)>0 for i in range(k)):
            g(r)
    all_values=[g(r) for r in product(*(range(v+1) for v in c))
        if all(sum(r[t-1] for t in range(1,1<<k) if (t>>i)&1)>0 for i in range(k))]
    return g(c),max(all_values)

def run():
    report={"scope":"all minimal forbidden-set families with 1<=k<=3 and edge size<=4, up to vertex relabeling", "per_k":{}}
    for k in (1,2,3):
        tally=Counter();maxes=Counter();roots=Counter();unique=set(); by_n=Counter();example={};uniform=set();uniform_labeled=0
        for c in cases(k):
            root,m=grundy(c,k)
            tally['families']+=1
            by_n[sum(c)]+=1
            roots[root]+=1
            maxes[m]+=1
            unique.add(min(permuted(c,p) for p in permutations(range(k))))
            if k==3 and all(sum(c[t-1] for t in range(1,1<<k) if (t>>j)&1)==4 for j in range(k)):
                uniform_labeled+=1
                uniform.add(min(permuted(c,p) for p in permutations(range(k))))
            if m not in example:example[m]=c
        report['per_k'][str(k)]={"labeled_incidence_types":tally['families'], "unlabeled_edge_types":len(unique),"root_nimber_counts":dict(sorted(roots.items())),"max_nimber_counts":dict(sorted(maxes.items())),"types_by_union_size":dict(sorted(by_n.items())),"max_nimber":max(maxes),"examples_for_maximum":list(example[max(maxes)])}
        if k==3:report["per_k"][str(k)]["exactly_four_per_edge"]={"labeled_incidence_types":uniform_labeled,"unlabeled_edge_types":len(uniform)}
    assert [report["per_k"][str(k)]["labeled_incidence_types"] for k in (1,2,3)]==[4,30,641]
    assert max(v["max_nimber"] for v in report["per_k"].values())==3
    assert report["per_k"]["3"]["exactly_four_per_edge"]=={"labeled_incidence_types":68,"unlabeled_edge_types":25}
    for c,k,expected in [((0,1,1,1,1,1,2),3,4),((0,1,1,2,1,1,2),3,5)]:
        assert grundy(c,k)[0]==expected
    return report

if __name__=='__main__':
    result=run()
    print(json.dumps(result,indent=2,ensure_ascii=False))
