#!/usr/bin/env python3
"""Independent all-safe mex audit for the 2x9 threshold board."""
from itertools import combinations
from functools import lru_cache
import json

m = 9
points = [(x,y) for y in range(2) for x in range(m)]


def det3(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            -a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))


def forbidden(ids):
    x0,y0 = points[ids[0]]

    def row(i):
        x,y = points[i]
        return (x*x-x0*x0,x-x0,y-y0)

    return det3(*(row(i) for i in ids[1:])) == 0


blocked = [[] for _ in points]
bad = 0
for ids in combinations(range(len(points)),4):
    if forbidden(ids):
        bad += 1
        for p in ids:
            blocked[p].append(sum(1<<i for i in ids if i!=p))


def moves(mask):
    for p in range(len(points)):
        if mask>>p&1:
            continue
        if any(mask&t == t for t in blocked[p]):
            continue
        yield mask | 1<<p


@lru_cache(None)
def grundy(mask):
    children = {grundy(t) for t in moves(mask)}
    g = 0
    while g in children:
        g += 1
    return g


seen = set()


def check(mask):
    if mask in seen:
        return
    seen.add(mask)
    assert grundy(mask) == (6-mask.bit_count())%2, mask
    for t in moves(mask):
        check(t)


check(0)
print(json.dumps({'board':'2x9','forbidden_quadruples':bad,
                  'safe_states':len(seen),'empty_grundy':grundy(0),
                  'all_safe_parity':True}))
