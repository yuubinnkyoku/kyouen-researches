#!/usr/bin/env python3
"""Exact 3-column x 4-row q=4 generic game; standard library only.

Two independent forbidden-set builders (midpoint/collinearity vs 4x4
lifted determinant), and two independent full safe-state Grundy recursions.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations

ROWS=range(4)
COLS=range(3)
N=12
FULL=(1<<N)-1

def index(x,y):return 4*x+y

def structural_edges():
    e=set()
    for x in COLS:
        e.add(sum(1<<index(x,y) for y in ROWS))
    for x,z in combinations(COLS,2):
        for pair in combinations(ROWS,2):
            for other in combinations(ROWS,2):
                if sum(pair)==sum(other):
                    e.add(sum(1<<index(x,y) for y in pair)+sum(1<<index(z,y) for y in other))
    return sorted(e)

def arithmetic_edges(a,b,d):
    """All 2+1+1 circles, from the three-column divided difference."""
    edges=set(structural_edges())
    for paired in COLS:
        others=[i for i in COLS if i!=paired]
        for u,v in combinations(ROWS,2):
            S=u+v
            for r in ROWS:
                for t in ROWS:
                    y=[None]*3
                    y[paired]=u*v
                    y[others[0]]=r*(S-r)
                    y[others[1]]=t*(S-t)
                    if d*d*(b*y[0]-(a+b)*y[1]+a*y[2])==a*b*(a+b):
                        edges.add((1<<index(paired,u))|(1<<index(paired,v))|
                                  (1<<index(others[0],r))|(1<<index(others[1],t)))
    return sorted(edges)

def det3(a):
    (a,b,c),(d,e,f),(g,h,i)=a
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)

def geometric_edges(a,b,d):
    pts=[(x,d*y) for x in (0,a,a+b) for y in ROWS]
    e=[]
    for inds in combinations(range(N),4):
        r=[[x*x+y*y,x,y] for j in inds for x,y in [pts[j]]]
        delta=[[r[i][j]-r[0][j] for j in range(3)] for i in (1,2,3)]
        if det3(delta)==0:
            e.append(sum(1<<i for i in inds))
    return sorted(e)

def solve_bottom_up(edges):
    safe=bytearray([1])*(FULL+1)
    for edge in edges:
        complement=FULL^edge
        s=complement
        while True:
            safe[edge|s]=0
            if s==0:break
            s=(s-1)&complement
    g=bytearray(FULL+1)
    for s in range(FULL,-1,-1):
        if not safe[s]:continue
        options=0
        for i in range(N):
            t=s|(1<<i)
            if t!=s and safe[t]:options|=1<<g[t]
        g[s]=next(j for j in range(N+1) if not (options>>j)&1)
    hist=Counter(g[s] for s in range(FULL+1) if safe[s])
    terminal=Counter(s.bit_count() for s in range(FULL+1) if safe[s] and
        all(not safe[s|1<<i] for i in range(N) if not (s>>i)&1))
    return safe,g,hist,terminal

def solve_recursive(edges):
    @lru_cache(None)
    def f(s):
        v={f(s|1<<i) for i in range(N) if not(s>>i&1) and
           all((s|1<<i)&e!=e for e in edges)}
        j=0
        while j in v:j+=1
        return j
    return f

def main():
    universal=structural_edges()
    assert len(universal)==27
    print('structural forbidden 4-sets:',len(universal))
    samples=0
    large=0
    for a in range(1,17):
      for b in range(1,17):
       for d in range(1,17):
        actual=geometric_edges(a,b,d)
        assert arithmetic_edges(a,b,d)==actual,(a,b,d)
        if a*b*(a+b)%(d*d):
            assert actual==universal,(a,b,d)
            samples+=1
        if a*b>6*d*d:
            assert actual==universal,(a,b,d)
            large+=1
    print('arithmetic vs determinant: 4096 parameter triples; nondivisible universal:',samples,'ab>6d^2 universal:',large)
    assert len(arithmetic_edges(2,3,1))>27
    safe,g,hist,terminal=solve_bottom_up(universal)
    print('safe states:',sum(safe),'root:',g[0], 'first:',[g[1<<i] for i in range(N)])
    print('Grundy histogram:',dict(sorted(hist.items())))
    print('maximal safe sizes:',dict(sorted(terminal.items())))
    print('maximum Grundy:',max(hist))
    f=solve_recursive(geometric_edges(1,1,2))
    assert all(f(s)==g[s] for s in range(FULL+1) if safe[s])
    print('independent recursive mex matches all safe states')
    assert g[0]==0 and all(g[1<<i]==4 for i in range(N))
    print('PASS')
if __name__=='__main__':main()
