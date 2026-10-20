#!/usr/bin/env python3
"""225-state orbit quotient for two intersecting forbidden 6-sets."""
from functools import lru_cache
from collections import Counter
from itertools import product
from math import comb
import json

CAP=(2,4,4,2)  # common, exclusive left, exclusive right, free

def safe(t):
    a,b,c,d=t
    return not (a==2 and (b==4 or c==4))

@lru_cache(None)
def grundy(t):
    assert safe(t)
    successors=set()
    for i in range(4):
        if t[i]<CAP[i]:
            child=tuple(t[j]+(j==i) for j in range(4))
            if safe(child):successors.add(grundy(child))
    g=0
    while g in successors:g+=1
    return g

def report():
    hist=Counter(); maximal=Counter(); count=0
    for t in product(*(range(n+1) for n in CAP)):
        if not safe(t):continue
        weight=1
        for n,k in zip(CAP,t):weight*=comb(n,k)
        hist[grundy(t)]+=weight;count+=weight
        if not any(t[i]<CAP[i] and safe(tuple(t[j]+(j==i) for j in range(4))) for i in range(4)):
            maximal[sum(t)]+=weight
    assert count==3972
    assert dict(hist)=={0:1378,1:1378,2:608,3:608}
    assert dict(maximal)=={10:16,11:2}
    assert grundy((0,0,0,0))==0
    return {'safe_states':sum(safe(t) for t in product(*(range(n+1) for n in CAP))),
            'safe_labeled_subsets':count,'root':grundy((0,0,0,0)),
            'histogram':dict(sorted(hist.items())),'maximal':dict(sorted(maximal.items()))}

if __name__=='__main__':print(json.dumps(report(),indent=2))
