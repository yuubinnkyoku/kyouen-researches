#!/usr/bin/env python3
"""Independent all-state verifier for 3D 5-point hyperplane/sphere game.

Uses a 4x4 difference determinant (24 permutations) and recursive mex;
the separate C++ implementation uses fraction-free 5x5 elimination.
"""
from __future__ import annotations
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
import hashlib
import json
import sys

shape = tuple(map(int, sys.argv[1:])) if len(sys.argv) > 1 else (3, 3, 3)
assert len(shape) == 3 and all(n >= 1 for n in shape) and shape[0]*shape[1]*shape[2] <= 27
points = list(product(*(range(n) for n in shape)))
size = len(points)
all_bits = (1 << size) - 1
perms = []
for perm in permutations(range(4)):
    inversions = sum(perm[i] > perm[j] for i in range(4) for j in range(i+1, 4))
    perms.append((perm, -1 if inversions & 1 else 1))

def lifted(p):
    return (sum(t*t for t in p), *p)

def det4(rows):
    return sum(sign*rows[0][p[0]]*rows[1][p[1]]*rows[2][p[2]]*rows[3][p[3]]
               for p,sign in perms)

lifts = [lifted(p) for p in points]
forbidden = []
completion = {}
for ids in combinations(range(size), 5):
    base = lifts[ids[0]]
    rows = [[lifts[i][j]-base[j] for j in range(4)] for i in ids[1:]]
    if det4(rows) != 0:
        continue
    edge = sum(1 << i for i in ids)
    forbidden.append(edge)
    for i in ids:
        four = edge ^ (1 << i)
        completion[four] = completion.get(four, 0) | (1 << i)

@lru_cache(None)
def legal(mask):
    bits = [i for i in range(size) if (mask >> i) & 1]
    blocked = 0
    for indices in combinations(bits, 4):
        blocked |= completion.get(sum(1 << i for i in indices), 0)
    return all_bits & ~(mask | blocked)

@lru_cache(None)
def grundy(mask):
    moves = legal(mask)
    options = 0
    while moves:
        bit = moves & -moves
        moves ^= bit
        options |= 1 << grundy(mask | bit)
    val = 0
    while (options >> val) & 1:
        val += 1
    return val

root = grundy(0)
states = set()
def visit(mask):
    if mask in states:
        return
    states.add(mask)
    moves = legal(mask)
    while moves:
        bit = moves & -moves
        moves ^= bit
        visit(mask | bit)
visit(0)
assert len(states) == grundy.cache_info().currsize == legal.cache_info().currsize
hist = {}
terminals = 0
for mask in states:
    hist.setdefault(mask.bit_count(), Counter())[grundy(mask)] += 1
    terminals += legal(mask) == 0
two_loss = sum(grundy((1 << a) | (1 << b)) == 0 for a,b in combinations(range(size), 2))
if shape == (3,3,3):
    assert root == 0 and len(states) == 205506 and len(forbidden) == 16026
    assert two_loss == 351
    lookup = {p:i for i,p in enumerate(points)}
    symmetry = []
    for axes in permutations(range(3)):
        for flips in product((0,1),repeat=3):
            symmetry.append([lookup[tuple(2-p[axes[j]] if flips[j] else p[axes[j]]
                                           for j in range(3))] for p in points])
    assert len({tuple(a) for a in symmetry}) == 48
    pair_orbits = {}
    for a,b in combinations(range(size),2):
        rep = min(tuple(sorted((perm[a],perm[b]))) for perm in symmetry)
        pair_orbits.setdefault(rep,[]).append((a,b))
    assert len(pair_orbits) == 20
    orbits = [{"representative":[points[a],points[b]],"size":len(items),
               "grundy":grundy((1 << a)|(1 << b))}
              for (a,b),items in sorted(pair_orbits.items())]
else:
    orbits = []
digest = hashlib.sha256()
for mask in sorted(states):
    digest.update(f"{mask},{grundy(mask)}\n".encode())
print(json.dumps({
    "shape":shape, "forbidden_five_sets":len(forbidden), "safe_states":len(states),
    "terminal_states":terminals, "root_grundy":root,
    "grundy_by_stones":{str(k):dict(sorted(c.items())) for k,c in sorted(hist.items())},
    "two_stone_losing":two_loss, "two_stone_total":size*(size-1)//2,
    "two_stone_symmetry_orbits":len(orbits), "two_stone_orbits":orbits,
    "sha256_state_nimber":digest.hexdigest()
},indent=2,ensure_ascii=False))
