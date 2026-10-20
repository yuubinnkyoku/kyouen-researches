#!/usr/bin/env python3
"""Independent branch-and-bound enumeration of 5x5 eleven-point minimizers."""
from itertools import combinations
from verify_geometry import forbidden
P=[(x,y) for x in range(5) for y in range(5)]
by_last=[[] for _ in P]
for e in combinations(range(25),4):
    if forbidden([P[i] for i in e]):
        by_last[e[-1]].append(sum(1<<i for i in e[:-1]))
minimizers=[]

def dfs(start,n,mask,edges):
    if n==11:
        if edges==5:minimizers.append(mask)
        return
    for i in range(start,25-(11-n)+1):
        add=sum((mask&t)==t for t in by_last[i])
        if edges+add<=5:
            dfs(i+1,n+1,mask|(1<<i),edges+add)
dfs(0,0,0,0)
assert len(minimizers)==8

def transform(x,y,k):
    if k>=4:
        x=4-x
        k-=4
    for _ in range(k):
        x,y=y,4-x
    return x,y

def move(mask,k):
    out=0
    for i,(x,y) in enumerate(P):
        if mask>>i&1:
            a,b=transform(x,y,k)
            out|=1<<(a*5+b)
    return out
orbit={move(minimizers[0],k) for k in range(8)}
assert orbit==set(minimizers)
print('5x5: exactly 8 eleven-point minimizers with 5 forbidden quadruples; one D4 orbit')
