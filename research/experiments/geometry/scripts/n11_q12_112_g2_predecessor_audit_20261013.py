#!/usr/bin/env python3
"""Independent exact census of 111-stone predecessors of g=2 112-stone positions.

Board: 11x11, q=12, normal-play. Sets are represented by OMITTED points.
All arithmetic is integral. Runtime ~30 seconds on a typical workstation.
"""
from collections import Counter
from itertools import combinations
from math import gcd

P = [(i % 11, i // 11) for i in range(121)]
R = [x*x + y*y for x, y in P]
circles = {}
for i in range(121):
    x, y = P[i]
    for j in range(i+1, 121):
        u, v = P[j]
        dx, dy, dr = u-x, v-y, R[j]-R[i]
        for k in range(j+1, 121):
            w, z = P[k]
            ex, ey, er = w-x, z-y, R[k]-R[i]
            det = dx*ey - ex*dy
            if not det:
                continue
            a, b = -dr*ey + er*dy, -dx*er + ex*dr
            c = -R[i]*det - a*x - b*y
            g = gcd(gcd(gcd(abs(det), abs(a)), abs(b)), abs(c))
            if det < 0:
                g = -g
            key = (a//g, b//g, c//g, det//g)
            circles[key] = circles.get(key, 0) | (1<<i) | (1<<j) | (1<<k)
C = sorted(set(s for s in circles.values() if s.bit_count() == 12))
assert len(C) == 21
inc = [sum(1<<i for i,c in enumerate(C) if c>>p&1) for p in range(121)]
byedge = [[p for p in range(121) if inc[p]>>i&1] for i in range(21)]
assert max(v.bit_count() for v in inc) == 3
full = (1<<21)-1
m7, m8 = set(), set()

def dfs(covered, chosen, private):
    k = chosen.bit_count()
    if covered == full:
        if k == 7: m7.add(chosen)
        if k == 8: m8.add(chosen)
        return
    if k == 8 or 21-covered.bit_count() > 3*(8-k):
        return
    missing = full ^ covered
    edge = (missing & -missing).bit_length()-1
    for p in byedge[edge]:
        bit, hit = 1<<p, inc[p]
        if chosen & bit: continue
        if (hit & missing).bit_count()+3*(7-k) < missing.bit_count(): continue
        if any(not (v & ~hit) for v in private): continue
        dfs(covered|hit, chosen|bit,
            [v & ~hit for v in private]+[hit & missing])

dfs(0, 0, [])
assert (len(m7),len(m8)) == (52,54072)
g2 = {a|b for a in m7 for b in m8 if (a&b).bit_count()==6}
assert len(g2)==10632
candidates = {d|(1<<p) for d in g2 for p in range(121) if not(d>>p&1)}
assert len(candidates)==1120456

bad_pred = Counter()
bad_degree = Counter()
bad_states = {}
g3 = 0
for d in candidates:
    bits = [1<<p for p in range(121) if d>>p&1]
    has7, has8 = 0, 0
    for a in m7:
        if a&d == a:
            has7 |= d^a
    for i,j in combinations(range(10),2):
        if d^bits[i]^bits[j] in m8:
            has8 |= bits[i]|bits[j]
    invalid = 0
    for c in C:
        x = d&c
        if x.bit_count()==1:
            invalid |= x
    valid = d & ~invalid
    # Child Grundy g=0,1,2, respectively. The g=2 child is guaranteed.
    n0 = (valid & ~has8).bit_count()
    n1 = (valid & has8 & ~has7).bit_count()
    n2 = (valid & has8 & has7).bit_count()
    assert n2>0
    if n0 and n1:
        g3 += 1
    else:
        degree = 0
        for bit in bits:
            if d^bit in g2:
                bad_pred[d^bit] += 1
                degree += 1
        bad_degree[degree] += 1
        bad_states[d] = ((bool(n0),bool(n1),bool(n2)),degree)
assert g3==1118500
assert Counter(bad_pred[d] for d in g2)=={0:6804,1:3284,2:400,3:144}
assert bad_degree=={2:1440,3:476,4:16,6:24}

def orbit(d):
    out = set()
    for op in range(8):
        t, z = d, 0
        while t:
            bit=t&-t; t-=bit
            p=bit.bit_length()-1; x,y=p%11,p//11
            if op&1: x=10-x
            if op&2: y=10-y
            if op&4: x,y=y,x
            z |= 1<<(11*y+x)
        out.add(z)
    return out

bad_orbits = Counter()
pending = set(bad_states)
while pending:
    d = next(iter(pending))
    o = orbit(d)
    assert o<=pending
    pending -= o
    bad_orbits[bad_states[d],len(o)] += 1
g2_orbits = Counter()
pending = set(g2)
while pending:
    d = next(iter(pending))
    o = orbit(d)
    assert o<=pending
    pending -= o
    g2_orbits[bad_pred[d],len(o)] += 1

print("circles",len(C),"minimal7",len(m7),"minimal8",len(m8))
print("g2_112",len(g2),"111_candidates",len(candidates),"g3_111",g3)
print("g2_bad_predecessors",sorted(Counter(bad_pred[d] for d in g2).items()))
print("bad_111_g2_child_count",sorted(bad_degree.items()))
print("bad_111_orbits",sorted(bad_orbits.items()))
print("g2_orbits_by_bad_predecessors",sorted(g2_orbits.items()))
print("bad_incidence",sum(bad_pred.values()),"good_incidence",len(g2)*112-sum(bad_pred.values()))
assert sum(bad_pred.values())==4516
assert sum(v*sz for (_,sz),v in g2_orbits.items())==10632
assert sum(v*sz for (_,sz),v in bad_orbits.items())==1956
