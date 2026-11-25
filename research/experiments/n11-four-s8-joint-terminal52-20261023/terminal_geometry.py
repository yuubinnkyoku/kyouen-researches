#!/usr/bin/env python3
"""Standalone terminal-only proof of one S8 LOSS on standard 11x11.

Standard 11x11, q=4, complete call, normal play, fixed original-first-player
WIN/LOSS.  All geometry uses exact integer determinants; no search cache is read.
"""
from functools import lru_cache
from itertools import combinations
N=11
def check(condition,message='invalid certificate'):
    if not condition: raise ValueError(message)
def points(m): return [i for i in range(121) if m>>i&1]
def circle(a,b,c,d):
    def vec(p):
        x,y=p%N,p//N
        return (x,y,x*x+y*y)
    z=vec(d)
    u=[x-y for x,y in zip(vec(a),z)]
    v=[x-y for x,y in zip(vec(b),z)]
    w=[x-y for x,y in zip(vec(c),z)]
    return (u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0]))==0
def safe(m): return all(not circle(*q) for q in combinations(points(m),4))
def legal(m):
    p=points(m); triples=list(combinations(p,3))
    return [x for x in range(121) if not (m>>x&1) and all(not circle(a,b,c,x) for a,b,c in triples)]
def canonical(m):
    best=None
    for t in range(8):
        v=0
        for p in points(m):
            x,y=p%11,p//11
            xx,yy=((x,y),(10-y,x),(10-x,10-y),(y,10-x),(10-x,y),(10-y,10-x),(x,10-y),(y,x))[t]
            v|=1<<(11*yy+xx)
        best=v if best is None else min(best,v)
    return best
def children(m): return {canonical(m|(1<<p)) for p in legal(m)}
def next_player_wins_at_s10(m):
    check(m.bit_count() in (10,11) and safe(m))
    base=points(m); moves=legal(m); n=len(moves)
    check(n<=31,f'terminal bitmask width exceeded: {n}')
    bad=set()
    for i,j in combinations(range(n),2):
        if any(circle(a,b,moves[i],moves[j]) for a,b in combinations(base,2)):
            bad.add((1<<i)|(1<<j))
    for i,j,k in combinations(range(n),3):
        e=(1<<i)|(1<<j)|(1<<k)
        if any(e&b==b for b in bad):continue
        if any(circle(a,moves[i],moves[j],moves[k]) for a in base):bad.add(e)
    for ids in combinations(range(n),4):
        e=sum(1<<i for i in ids)
        if any(e&b==b for b in bad):continue
        if circle(*(moves[i] for i in ids)):bad.add(e)
    ban_by=[[] for _ in range(n)]
    for e in bad:
        for i in range(n):
            if e>>i&1:ban_by[i].append(e^(1<<i))
    @lru_cache(None)
    def win(state):
        for i in range(n):
            bit=1<<i
            if state&bit or any(state&b==b for b in ban_by[i]):continue
            if not win(state|bit):return True
        return False
    return win(0),win.cache_info().currsize
