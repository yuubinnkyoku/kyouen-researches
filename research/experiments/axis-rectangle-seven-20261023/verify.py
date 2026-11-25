#!/usr/bin/env python3
"""7-row axis-aligned rectangle-free capacity: exact small DP and certificates."""
from itertools import combinations
import json

LINES=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
EDGES=list(combinations(range(7),2))
assert sorted(tuple(sorted(e)) for line in LINES for e in combinations(line,2))==EDGES

def bound(w,m):
    e=w*(w-1)//2; f=m*(m-1)//2
    return min(m+e,m+(e+m)//2,w+f,w+(f+w)//2)

def value(m):
    if m<=4:return 7+m*(m-1)//2
    if m<=6:return 3*m
    if m<=21:return m+(m+21)//2
    return m+21

def witness(m):
    if m<=4:
        rows=list(combinations(range(m),2))+[(0,)]*(7-m*(m-1)//2)
        return [tuple(i for i,row in enumerate(rows) if j in row) for j in range(m)]
    if m<=6:return LINES[:m]
    if m<=21:
        r=(21-m)//2
        tri=LINES[:r]
        used={tuple(sorted(e)) for line in tri for e in combinations(line,2)}
        return tri+[e for e in EDGES if e not in used][:m-r]
    return EDGES+[(0,)]*(m-21)

def exact(m):
    pairs=list(combinations(range(m),2))
    options=[]
    for b in range(1<<m):
        e=sum(1<<k for k,(i,j) in enumerate(pairs) if (b>>i&1) and (b>>j&1))
        options.append((e,b.bit_count()))
    dp={0:0}
    for _ in range(7):
        nxt={}
        for mask,score in dp.items():
            for e,s in options:
                if mask&e:continue
                k=mask|e
                if score+s>nxt.get(k,-1):nxt[k]=score+s
        dp=nxt
    return max(dp.values()),len(dp)

def main():
    checks={}
    for m in range(1,41):
        cols=witness(m)
        assert len(cols)==m
        used=set()
        for col in cols:
            assert len(set(col))==len(col)
            assert all(0<=x<7 for x in col)
            for edge in combinations(sorted(col),2):
                assert edge not in used
                used.add(edge)
        assert sum(map(len,cols))==value(m)==bound(7,m)
        if m<=6:
            optimum,states=exact(m)
            assert optimum==value(m)
            checks[m]={'optimum':optimum,'states':states}
    print(json.dumps({'values':[value(m) for m in range(1,41)],'exact_dp':checks},indent=2))

if __name__=='__main__':main()
