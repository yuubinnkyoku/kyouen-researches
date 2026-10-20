#!/usr/bin/env python3
"""Exhaustive Venn-count DP for at most 3 rank<=4 minimal forbidden edges.

A vertex is in class p if its membership mask across the 3 edges is p.
Class 0 (free vertices) is handled by xor with their count modulo 2.
"""
from functools import lru_cache
import sys
from collections import Counter
import json

@lru_cache(None)
def g(counts):
    edge_sizes=[sum(counts[p-1] for p in range(1,8) if p & (1<<k)) for k in range(3)]
    children=set()
    for p in range(1,8):
        if not counts[p-1] or any(edge_sizes[k]==1 for k in range(3) if p & (1<<k)):
            continue
        nxt=list(counts)
        nxt[p-1]-=1
        children.add(g(tuple(nxt)))
    x=0
    while x in children: x+=1
    return x

def valid(c):
    edges=[sum(c[p-1] for p in range(1,8) if p & (1<<k)) for k in range(3)]
    if any(not (2<=z<=4) for z in edges): return False
    for i in range(3):
        for j in range(3):
            if i!=j and sum(c[p-1] for p in range(1,8) if p & (1<<i) and not p & (1<<j))==0:
                return False
    return True

hist=Counter(); size_hist=Counter(); rank_hist={2:Counter(),3:Counter(),4:Counter()}; witnesses={}; total=0
for code in range(5**7):
    t=code
    digits=[]
    for _ in range(7):
        digits.append(t%5)
        t//=5
    c=tuple(digits)
    if not valid(c): continue
    total+=1
    z=g(c)
    if "--cases" in sys.argv:
        print(f"{code},{z}")
    hist[z]+=1
    size_hist[(sum(c),z)]+=1
    edges=[sum(c[p-1] for p in range(1,8) if p & (1<<k)) for k in range(3)]
    rank=max(edges)
    for r in range(rank,5): rank_hist[r][z]+=1
    if z not in witnesses or sum(c)<sum(witnesses[z]):witnesses[z]=c
out={"rank4_minimal_three_edges_venn_classes":total,"grundy_hist":dict(sorted(hist.items())),"rank_leq_hist":{r:dict(sorted(v.items())) for r,v in rank_hist.items()},"min_size_witnesses":{z:{"counts":v,"union_size":sum(v)} for z,v in witnesses.items()},"by_union_size":{f"{n},{z}":v for (n,z),v in sorted(size_hist.items())},"cached_states":g.cache_info().currsize}
assert total==562 and hist==Counter({0:228,1:231,2:49,3:54})
if "--cases" not in sys.argv:
    print(json.dumps(out,indent=2,ensure_ascii=False))
