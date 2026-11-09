#!/usr/bin/env python3
"""Independent full-layer misere audit for the 2x3x4 coplanar-four game."""
from itertools import product, combinations
from collections import Counter
from functools import lru_cache

P = list(product(range(2), range(3), range(4)))
N = len(P)
def det(a,b,c,d):
    u=[b[i]-a[i] for i in range(3)]
    v=[c[i]-a[i] for i in range(3)]
    w=[d[i]-a[i] for i in range(3)]
    return (u[0]*(v[1]*w[2]-v[2]*w[1])
            -u[1]*(v[0]*w[2]-v[2]*w[0])
            +u[2]*(v[0]*w[1]-v[1]*w[0]))
edges=[sum(1<<i for i in ids) for ids in combinations(range(N),4)
       if det(*(P[i] for i in ids))==0]
assert len(edges)==2126
blockers=[[] for _ in range(N)]
for edge in edges:
    for i in range(N):
        if edge & (1<<i): blockers[i].append(edge^(1<<i))
def successors(mask):
    return [mask|(1<<i) for i in range(N)
            if not mask & (1<<i)
            and not any(mask & b == b for b in blockers[i])]
@lru_cache(None)
def winning(mask):
    nxt=successors(mask)
    return not nxt or any(not winning(t) for t in nxt)
seen={0}
todo=[0]
layers=Counter()
terminals=Counter()
while todo:
    mask=todo.pop()
    nxt=successors(mask)
    layers[(mask.bit_count(),winning(mask))]+=1
    if not nxt: terminals[mask.bit_count()]+=1
    for t in nxt:
        if t not in seen:
            seen.add(t)
            todo.append(t)
expected=[(0,1),(24,0),(0,276),(1952,72),(8,8492),(13872,1184),(0,5648)]
for k,(p,q) in enumerate(expected):
    assert (layers[k,False],layers[k,True])==(p,q),(k,layers)
assert len(seen)==31529
assert terminals=={3:40,5:1184,6:5648}
assert winning(0)
assert all(not winning(1<<i) for i in range(N))
print("PASS: full layer outcomes, terminal histogram, all first moves")
