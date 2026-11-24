#!/usr/bin/env python3
"""K1283 predeclaration exploration: z1 plane (delta-2 rows) census battery."""
from engine_block import H_canonical, H_ordered
from functools import lru_cache
from itertools import combinations_with_replacement
import json, sys

def clear(): H_canonical.cache_clear(); H_ordered.cache_clear()
def g(R, X, z=1):
    r = H_canonical(R, tuple(sorted(X, reverse=True)), z); clear(); return r

def shapes(m, hi, amax):
    for k in range(2, amax + 1):
        for c in combinations_with_replacement(range(m, hi + 1), k):
            if c[0] == m and max(c) > m:
                yield tuple(reversed(c))

out = {}

# E1: H2 census z1 delta-2 mixed, m=1..7
bad = 0; cnt = 0; hist = {}
for m in range(1, 8):
    R = 2*m+2
    if m == 1:
        gen = []
        for q in range(1, 4):
            for k in range(1, 4):
                for c in combinations_with_replacement(range(2, 10), k):
                    gen.append(tuple(sorted([1]*q + list(c), reverse=True)))
    else:
        gen = shapes(m, m+6, 5)
    for X in gen:
        h = g(R, X, 1); cnt += 1
        exp = min(sum(X), R) % 2
        hist[h] = hist.get(h, 0) + 1
        if h != exp: bad += 1
out['E1_h2_census'] = [cnt, bad, hist]

# E2: allm z1 delta-2: a>=2 -> 0 (m=1..8); a=1 single -> v
from engine_block import single_token
v = single_token
bad2 = 0; cnt2 = 0
for m in range(1, 9):
    R = 2*m+2
    for a in range(1, 9):
        h = g(R, tuple([m]*a), 1); cnt2 += 1
        exp = v(m, 1, R) if a == 1 else 0
        if h != exp: bad2 += 1
out['E2_allm'] = [cnt2, bad2]

# E3: z1 frontier classification m=2..7: mixed->2, (mm)->0, allm a>=3 -> 2
bad3 = 0; cnt3 = 0
for m in range(2, 8):
    R = 2*m+1
    for X in shapes(m, m+6, 5):
        h = g(R, X, 1); cnt3 += 1
        if h != 2: bad3 += 1
    h = g(R, tuple([m]*2), 1); cnt3 += 1
    if h != 0: bad3 += 1
    for a in range(3, 7):
        h = g(R, tuple([m]*a), 1); cnt3 += 1
        if h != 2: bad3 += 1
out['E3_frontier'] = [cnt3, bad3]

# E4: z1 band+diag collapse m=2..7, R in [m+2,2m], sum>=R regime
bad4 = 0; cnt4 = 0
for m in range(2, 8):
    for R in range(m+2, 2*m+1):
        for X in shapes(m, R+2, 4):
            if sum(X) < R: continue
            h = g(R, X, 1); cnt4 += 1
            if h != v(sum(X), 1, R): bad4 += 1
        for a in range(2, 6):
            X = tuple([m]*a)
            if sum(X) < R: continue
            h = g(R, X, 1); cnt4 += 1
            if h != v(sum(X), 1, R): bad4 += 1
    # diag R=2m
    R = 2*m
    for X in shapes(m, R+2, 4):
        if sum(X) < R: continue
        h = g(R, X, 1); cnt4 += 1
        if h != v(sum(X), 1, R): bad4 += 1
    for a in range(2, 6):
        X = tuple([m]*a)
        if sum(X) < R: continue
        h = g(R, X, 1); cnt4 += 1
        if h != v(sum(X), 1, R): bad4 += 1
out['E4_band_diag'] = [cnt4, bad4]

# E5: L-Z1F: arm-1 shapes at row j z1 delta-3 (budget 2j+3): value >= 1; C-child identity
bad5 = 0; cnt5 = 0
for j in range(1, 7):
    R = 2*j+3
    if j == 1:
        gen = []
        for k in range(1, 4):
            for c in combinations_with_replacement(range(2, 9), k):
                gen.append(tuple(sorted([1]+list(c), reverse=True)))
    else:
        gen = [X for X in shapes1(j, j+6, 5)] if False else []
        for X in shapes(j, j+6, 5):
            if X.count(j) == 1: gen.append(X)
    for X in gen:
        h = g(R, X, 1); cnt5 += 1
        if h < 1: bad5 += 1
        z0 = g(R-1, X, 0)  # C-child base must be 1 (T-H1)
        if z0 != 1: bad5 += 1; print("CANCHOR FAIL", j, X)
out['E5_lzf'] = [cnt5, bad5]

# E6: L-S: (j, j+2) @ z1 delta-3: value >= 2; stair child (j,j+1)@z1-d2 = 1
bad6 = 0; cnt6 = 0
for j in range(1, 7):
    R = 2*j+3
    h = g(R, (j, j+2), 1); cnt6 += 1
    if h < 2: bad6 += 1; print("LS FAIL", j, h)
    sc = g(R-1, (j, j+1), 1); cnt6 += 1
    if sc != 1: bad6 += 1; print("STAIR FAIL", j, sc)
out['E6_ls'] = [cnt6, bad6]

# E7: T-N0z1: z1 delta-3 mixed never 0, m=1..6; hist
bad7 = 0; cnt7 = 0; hist7 = {}
for m in range(1, 7):
    R = 2*m+3
    if m == 1:
        gen = []
        for q in range(1, 3):
            for k in range(1, 3):
                for c in combinations_with_replacement(range(2, 8), k):
                    gen.append(tuple(sorted([1]*q + list(c), reverse=True)))
    else:
        gen = shapes(m, m+5, 4)
    for X in gen:
        h = g(R, X, 1); cnt7 += 1
        hist7[h] = hist7.get(h, 0) + 1
        if h == 0: bad7 += 1
out['E7_n0z1'] = [cnt7, bad7, hist7]

# E8: T-IIz1: class E z1 delta-3 (m>=2): value >= 2
bad8 = 0; cnt8 = 0
for m in range(2, 7):
    R = 2*m+3
    for X in shapes(m, m+6, 5):
        if X.count(m) < 2: continue
        mult1 = X.count(m+1); hasD = max(X) >= m+2
        if (not hasD) and mult1 == 1: continue  # arm-2
        h = g(R, X, 1); cnt8 += 1
        if h < 2: bad8 += 1; print("IIz1 FAIL", m, X, h)
out['E8_iiz1'] = [cnt8, bad8]

# E9: G3z2: budget-3 z2 classification (multi -> 1; singles: 1->1, 2->2, >=3->1)
bad9 = 0; cnt9 = 0
for k in range(2, 6):
    for c in combinations_with_replacement(range(1, 12), k):
        h = g(3, tuple(reversed(c)), 2); cnt9 += 1
        if h != 1: bad9 += 1; print("G3 FAIL multi", c, h)
for x in range(1, 16):
    h = g(3, (x,), 2); cnt9 += 1
    exp = 2 if x == 2 else 1
    if h != exp: bad9 += 1; print("G3 FAIL single", x, h)
out['E9_g3z2'] = [cnt9, bad9]

# E10: row-1 z1 sanity + anchors
checks = [
    (g(4, (1,2), 1) == 1, 'H2(1) special'),
    (g(4, (1,3), 1) == 0, 'H2(1) generic'),
    (g(4, (1,1,2), 1) == 0, 'H2(1) (1,1,2)'),
    (g(3, (1,1), 1) == 0, 'F4 (1,1)'),
    (g(5, (2,3), 1) == 2, 'K1278 T_B witness'),
    (v(5,1,5) == 0, 'T_B single'),
    (g(5, (2,3), 0) == 2, 'K1278 T_A3 witness z0'),
    (g(5, (1,3), 1) >= 2, 'L-S(1)'),
    (g(2,(1,),2) == 1 and v(1,2,2)==1, 'v(1,2,2)'),
    (g(2,(2,),2) == 0 and v(2,2,2)==0, 'v(2,2,2)'),
    (g(3,(2,),2) == 2 and v(2,2,3)==2, 'v(2,2,3)'),
    (g(3,(3,),2) == 1 and v(3,2,3)==1, 'v(3,2,3)'),
]
bad10 = 0
for ok, name in checks:
    if not ok: bad10 += 1; print("ANCHOR FAIL:", name)
out['E10_anchors'] = [len(checks), bad10]

print(json.dumps(out, indent=1))
