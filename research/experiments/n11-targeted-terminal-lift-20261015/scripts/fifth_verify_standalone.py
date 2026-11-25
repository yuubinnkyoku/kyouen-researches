#!/usr/bin/env python3
"""Independent, cache-free terminal verifier for standard 11x11 S7 WIN.

Fixed-first-player semantics: odd S7/S9 are AND, even S8/S10 are OR.
Requires only Python 3.10+; the certificate is the sole input.
"""
import sys
if not __debug__:
    raise SystemExit('Assertions must be enabled: do not run with python -O')
from functools import lru_cache
from itertools import combinations

N = 11

def points(mask):
    return [p for p in range(121) if mask >> p & 1]

def det4(a, b, c, d):
    def lift(p):
        x, y = p % N, p // N
        return x, y, x*x + y*y
    z = lift(d)
    u, v, w = ([i-j for i,j in zip(lift(p),z)] for p in (a,b,c))
    return (u[0]*(v[1]*w[2]-v[2]*w[1])
            -u[1]*(v[0]*w[2]-v[2]*w[0])
            +u[2]*(v[0]*w[1]-v[1]*w[0]))

def safe(mask):
    return all(det4(*t) != 0 for t in combinations(points(mask), 4))

def legal(mask):
    occupied = points(mask)
    triples = list(combinations(occupied, 3))
    return [p for p in range(121) if not mask >> p & 1
            and all(det4(*t,p) != 0 for t in triples)]

def canonical(mask):
    ans = mask
    for t in range(1, 8):
        transformed = 0
        for p in points(mask):
            x, y = p % N, p // N
            X,Y = ((x,y),(10-y,x),(10-x,10-y),(y,10-x),
                   (10-x,y),(10-y,10-x),(x,10-y),(y,x))[t]
            transformed |= 1 << (Y*N+X)
        ans = min(ans, transformed)
    return ans

def children(mask):
    return {canonical(mask | (1 << p)) for p in legal(mask)}

def terminal_s10(mask):
    assert mask.bit_count() == 10 and canonical(mask) == mask and safe(mask)
    base, moves = points(mask), legal(mask)
    n = len(moves)
    assert n <= 63, 'terminal bitset needs at most 63 legal moves'
    bad2, bad3, forbidden = set(), set(), []
    for i,j in combinations(range(n), 2):
        if any(det4(a,b,moves[i],moves[j]) == 0 for a,b in combinations(base,2)):
            bit = (1<<i)|(1<<j)
            bad2.add(bit); forbidden.append(bit)
    for i,j,k in combinations(range(n), 3):
        if any(((1<<a)|(1<<b)) in bad2 for a,b in combinations((i,j,k),2)):
            continue
        if any(det4(a,moves[i],moves[j],moves[k]) == 0 for a in base):
            bit = (1<<i)|(1<<j)|(1<<k)
            bad3.add(bit); forbidden.append(bit)
    for ids in combinations(range(n), 4):
        if any(((1<<a)|(1<<b)) in bad2 for a,b in combinations(ids,2)):
            continue
        if any(sum(1<<a for a in tri) in bad3 for tri in combinations(ids,3)):
            continue
        if det4(*(moves[i] for i in ids)) == 0:
            forbidden.append(sum(1<<i for i in ids))
    constraints = [[] for _ in range(n)]
    for b in forbidden:
        for i in range(n):
            if b >> i & 1:
                constraints[i].append(b ^ (1<<i))
    @lru_cache(None)
    def wins(state):
        for i in range(n):
            bit = 1<<i
            if state & bit or any(state & b == b for b in constraints[i]):
                continue
            if not wins(state | bit):
                return True
        return False
    verdict = not wins(0)  # True means S10 is fixed-first LOSS
    return verdict, wins.cache_info().currsize, n

def verify(filename):
    lines = open(filename, encoding='utf-8').read().splitlines()
    assert lines[:2] == ['# n11-S7-WIN-terminal-v1','BOARD 11']
    assert lines[-1] == 'END'
    tag,roothex,n = lines[2].split()
    assert tag == 'ROOT' and len(roothex) == 32
    root = int(roothex,16)
    assert root.bit_count() == 7 and canonical(root) == root and safe(root)
    edges = {}
    for line in lines[3:-1]:
        tag,a,b = line.split()
        assert tag == 'EDGE' and len(a) == len(b) == 32
        a,b = int(a,16),int(b,16)
        assert a not in edges
        edges[a] = b
    assert len(edges) == int(n) and set(edges) == children(root)
    terminal = {}
    count = 0
    for s8,s9 in edges.items():
        assert s8.bit_count() == 8 and safe(s8) and canonical(s8) == s8
        assert s9.bit_count() == 9 and safe(s9) and canonical(s9) == s9
        assert s9 in children(s8)
        descendants = children(s9)
        assert descendants
        count += len(descendants)
        for s10 in descendants:
            if s10 not in terminal:
                is_loss,states,moves = terminal_s10(s10)
                assert not is_loss, f'LOSS child: {s10:032x}'
                terminal[s10] = (states,moves)
    parents = {canonical(root ^ (1<<p)) for p in points(root)}
    for p in parents:
        assert root in children(p)
    print('PASS root',roothex,'S8',len(edges),'S9-S10 edges',count,
          'unique S10',len(terminal),'states',sum(v[0] for v in terminal.values()),
          'S6 WIN parents',len(parents))
    return terminal

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: python3 fifth_verify_standalone.py fifth-s7-win-terminal.cert')
    verify(sys.argv[1])
