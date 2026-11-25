#!/usr/bin/env python3
"""Independent finite enumeration for coplanar-four on 2x3x4."""
import itertools
from functools import lru_cache
from collections import Counter
P = list(itertools.product(range(2), range(3), range(4)))
N = len(P)
edges = set()
for a,b,c in itertools.combinations(range(N),3):
    u = [P[b][j]-P[a][j] for j in range(3)]
    v = [P[c][j]-P[a][j] for j in range(3)]
    n = (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
    base = (1<<a)|(1<<b)|(1<<c)
    for d in range(N):
        if base>>d&1: continue
        if n==(0,0,0) or sum(n[j]*(P[d][j]-P[a][j]) for j in range(3))==0:
            edges.add(base|(1<<d))
assert len(edges)==2126
by = [[] for _ in range(N)]
for e in edges:
    for i in range(N):
        if e>>i&1: by[i].append(e^(1<<i))
def moves(s):
    for i in range(N):
        if not(s>>i&1) and not any(s&f==f for f in by[i]):
            yield s|(1<<i)
@lru_cache(None)
def grundy(s):
    children={grundy(t) for t in moves(s)}
    x=0
    while x in children: x+=1
    return x
assert grundy(0)==0
assert all(grundy(1<<i)==1 for i in range(N))
assert grundy.cache_info().currsize==31529
seen={0}; stack=[0]; hist=Counter();layers=Counter();term=Counter()
while stack:
    s=stack.pop();hist[grundy(s)]+=1;layers[s.bit_count()]+=1
    nxt=list(moves(s))
    if not nxt:term[s.bit_count()]+=1
    for t in nxt:
        if t not in seen:seen.add(t);stack.append(t)
assert len(seen)==31529
assert layers=={0:1,1:24,2:276,3:2024,4:8500,5:15056,6:5648}
assert hist=={0:12093,1:15844,2:3560,3:32}
assert term=={3:40,5:1184,6:5648}
print("PASS",len(edges),len(seen),dict(layers),dict(hist),dict(term))
