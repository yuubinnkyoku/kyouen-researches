#!/usr/bin/env python3
"""Exact 11x11 q12 113-stone backbone: states.bin, reps.bin, graph.bin.
Deletion masks are little-endian 16-byte integers; reps are uint32.
Graph rows are uint32 degree followed by (uint32 neighbor, uint8 weight);
one weight unit is two single-stone moves.
"""
import struct
from collections import defaultdict
from itertools import combinations

N, P = 11, 121

def circles():
    found = set()
    for cx in range(21):
        for cy in range(21):
            radii = defaultdict(int)
            for p in range(P):
                x, y = p % N, p // N
                radii[(2*x-cx)**2 + (2*y-cy)**2] |= 1 << p
            found.update(m for m in radii.values() if m.bit_count() >= 12)
    assert len(found) == 21 and all(m.bit_count() == 12 for m in found)
    return sorted(found)

def minimal_deletions(curves):
    incidence = [sum(1 << i for i, c in enumerate(curves) if c >> p & 1)
                 for p in range(P)]
    byedge = [[p for p in range(P) if incidence[p] >> i & 1]
              for i in range(len(curves))]
    full = (1 << len(curves)) - 1
    seven, eight = set(), set()
    def dfs(covered, deleted, private):
        k = deleted.bit_count()
        if covered == full:
            if k == 7: seven.add(deleted)
            if k == 8: eight.add(deleted)
            return
        if k == 8 or (full ^ covered).bit_count() > 3*(8-k):
            return
        i = ((full ^ covered) & -(full ^ covered)).bit_length() - 1
        for p in byedge[i]:
            bit, hit = 1 << p, incidence[p]
            if deleted & bit or any((v & ~hit) == 0 for v in private):
                continue
            dfs(covered | hit, deleted | bit,
                [v & ~hit for v in private] + [hit & ~covered])
    dfs(0, 0, [])
    assert (len(seven), len(eight)) == (52, 54072)
    return seven, eight

def bits(d):
    return [p for p in range(P) if d >> p & 1]

def main():
    seven, eight = minimal_deletions(circles())
    states = sorted(eight | {d | (1 << p) for d in seven
                             for p in range(P) if not (d >> p & 1)})
    assert len(states) == 60000
    with open('states.bin', 'wb') as f:
        for d in states: f.write(d.to_bytes(16, 'little'))
    idx = {d:i for i,d in enumerate(states)}
    maps = []
    for rot in range(4):
        for reflect in (0,1):
            trans = []
            for p in range(P):
                x,y = p%N,p//N
                if reflect: x = 10-x
                for k in range(rot): x,y = 10-y,x
                trans.append(y*N+x)
            maps.append(trans)
    reps, visited = [], set()
    for i,d in enumerate(states):
        if i in visited: continue
        orb = set()
        for t in maps:
            e = 0
            for p in bits(d): e |= 1 << t[p]
            orb.add(idx[e])
        visited.update(orb)
        reps.append(i)
    assert len(reps) == 7574 and len(visited) == 60000
    with open('reps.bin', 'wb') as f:
        for i in reps: f.write(struct.pack('<I', i))
    by_six = defaultdict(list)
    for i,d in enumerate(states):
        for p,q in combinations(bits(d),2):
            by_six[d ^ (1 << p) ^ (1 << q)].append(i)
    assert len(by_six) == 769564
    adj = [{} for _ in states]
    for group in by_six.values():
        for a,b in combinations(group,2):
            weight = 1 if (states[a]&states[b]).bit_count()==7 else 2
            adj[a][b] = min(weight,adj[a].get(b,3))
            adj[b][a] = min(weight,adj[b].get(a,3))
    assert sum(map(len,adj))//2 == 3596092
    with open('graph.bin','wb') as f:
        for a in adj:
            f.write(struct.pack('<I',len(a)))
            for b,w in a.items(): f.write(struct.pack('<IB',b,w))
    print('states',len(states),'D4 orbits',len(reps),'edges',sum(map(len,adj))//2)

if __name__ == '__main__':
    main()
