#!/usr/bin/env python3
"""Frozen pre-declaration exploration for the BOUNDARY-BAND package (K1311).

Reproduces exactly the exploration steps that led from the K1308 Z-DIAG pair
vertex and the K0832 triple transient band conjectures to the universal
boundary-row hypothesis:

  X1  triple boundary row k = z+1: full value distribution by (z, j),
      j := x - y - w - z -- uniformity in j (no y/w splitting) discovered,
      the value-2 cells lie exactly on the line j = 2.
  X2  n = 4..7 boundary rows k = z+n-2: census against the single-coordinate
      claim D(E, k), E := x1 - (x2 + ... + xn) -- 0 mismatches.
  X3  n = 1 (L-SDB, engine vs published K0832 closed form), n = 2 (Z-DIAG
      boundary re-anchor incl. beds), all-ones families n = 2..8.
  X4  far stress (z 7..14, seeded), tail rows k >= z+n-1 (published regime).
  X5  typed option-value algebra on the boundary rows (mex region tables).

engine_block.py (sha pinned in the kit) provides the published K1138
recursive engines and the K0832 single-token closed form.
"""
import sys
from collections import defaultdict
from functools import lru_cache
from itertools import combinations_with_replacement
import random
sys.path.insert(0, '.')
from engine_block import H_canonical, H_ordered, single_token

def D(g, p):
    if g <= p:
        return 1 if g % 2 == 1 else 0
    if g == p + 1:
        return 2
    return 1 if g % 2 == 0 else 0

def E_of(X):
    Y = sorted(X, reverse=True)
    return Y[0] - (sum(Y) - Y[0])

print("=== X1: triple boundary row k=z+1, value distribution by (z,j) ===")
tot1 = 0; uni1 = 0
for z in range(0, 7):
    tab = defaultdict(lambda: defaultdict(int))
    for S in range(3, 17):
        for x in range(1, S):
            for y in range(1, min(x, S - x) + 1):
                w = S - x - y
                if 1 <= w <= y:
                    v = H_canonical(S + z + 1, (x, y, w), z)
                    j = x - y - w - z
                    tab[j][v] += 1
                    tot1 += 1
    for j in sorted(tab):
        sig = dict(tab[j])
        if len(sig) == 1:
            uni1 += sig[list(sig)[0]]
        print(f" z={z} j={j}: {sig}")
    H_canonical.cache_clear()
print(f"X1 summary: {tot1} cells, {uni1} lie in (z,j) columns with a single value")
print("X1 note: value 2 appears on the column j=2 only, for every z; phases below/above")
print("         match [(j+z) odd] (j<=1) / [(j+z) even] (j>=3) = D(j+z, z+1) = D(E, k)")

print()
print("=== X2: n=4..7 boundary rows k=z+n-2 vs claim D(E,k) ===")
for n in (4, 5, 6, 7):
    bad = 0; tot = 0
    Smax = {4: 16, 5: 15, 6: 14, 7: 13}[n]
    for z in range(0, 7):
        k = z + n - 2
        for X in combinations_with_replacement(range(1, 9), n):
            S = sum(X)
            if S > Smax:
                continue
            v = H_canonical(S + k, X, z)
            tot += 1
            if v != D(E_of(X), k):
                bad += 1
        H_canonical.cache_clear()
    print(f" n={n}: {tot - bad}/{tot} cells agree with D(E, k)")

print()
print("=== X3: n=1 L-SDB (closed form vs engine), n=2 Z-DIAG anchor, all-ones ===")
bad = 0; tot = 0; bad_cf = 0
for z in range(1, 11):
    for x in range(1, 17):
        v = H_canonical(x + z - 1, (x,), z)
        tot += 1
        if v != D(x, z - 1):
            bad += 1
        if single_token(x, z, x + z - 1) != v:
            bad_cf += 1
print(f" n=1 L-SDB: {tot - bad}/{tot} match D(x, z-1); closed-form mismatches: {bad_cf}")
bad = 0; tot = 0
for z in range(0, 9):
    for a in range(1, 8):
        for g in range(0, 17):
            S = 2 * a + g
            if S > 24:
                continue
            v = H_canonical(S + z, (a + g, a), z)
            tot += 1
            if v != D(g, z):
                bad += 1
    H_canonical.cache_clear()
print(f" n=2 Z-DIAG boundary (pairs + beds g=0): {tot - bad}/{tot} match D(g, z)")
bad = 0; tot = 0
for n in range(2, 9):
    for z in range(0, 9):
        k = z + n - 2
        v = H_canonical(n + k, tuple([1] * n), z)
        tot += 1
        if v != D(2 - n, k):
            bad += 1
print(f" all-ones n=2..8: {tot - bad}/{tot} match D(2-n, z+n-2)")

print()
print("=== X4: far stress (seeded) and published tail rows k>=z+n-1 ===")
random.seed(1311)
bad = 0; tot = 0
for n in (3, 4):
    for z in range(7, 15):
        k = z + n - 2
        for _ in range(60):
            X = tuple(sorted((random.randint(1, 12) for _ in range(n)), reverse=True))
            v = H_canonical(sum(X) + k, X, z)
            tot += 1
            if v != D(E_of(X), k):
                bad += 1
        H_canonical.cache_clear()
print(f" far stress triples/quads z=7..14: {tot - bad}/{tot}")
bad = 0; tot = 0
for n in (2, 3, 4):
    for z in range(0, 5):
        for kk in (z + n - 1, z + n):
            for X in combinations_with_replacement(range(1, 7), n):
                S = sum(X)
                if S > 14:
                    continue
                v = H_canonical(S + kk, X, z)
                tot += 1
                if v != S % 2:
                    bad += 1
        H_canonical.cache_clear()
print(f" tail rows k=z+n-1,z+n (published K0832 regime corollary): {tot - bad}/{tot}")

print()
print("=== X5: typed option-value algebra on boundary rows (k>=1 cells) ===")
def typed_options(X, z, k):
    n = len(X)
    Y = sorted(X, reverse=True)
    E = E_of(Y)
    opts = set()
    x1 = Y[0]
    uniq_top = (n >= 2 and x1 > Y[1]) or n == 1
    if uniq_top and x1 >= 2:
        opts.add(D(E - 1, k))
    for v in set(Y[1:]):
        if v >= 2:
            opts.add(D(E + 1, k))
    if 1 in X:
        opts.add(D(E + 1, k))
    if z >= 1:
        opts.add(1 ^ D(E, k - 1))
    return opts
bad = 0; tot = 0
for n in (2, 3, 4):
    for z in range(0, 6):
        k = z + n - 2
        if k < 1:
            continue
        for X in combinations_with_replacement(range(1, 6), n):
            if sum(X) > 14:
                continue
            E = E_of(X)
            c = D(E, k)
            opts = typed_options(X, z, k)
            m = 0
            while m in opts:
                m += 1
            tot += 1
            if not (m == c == H_canonical(sum(X) + k, X, z)):
                bad += 1
                if bad <= 5:
                    print(f"  TYPED BAD n={n} z={z} X={X} E={E} k={k} opts={sorted(opts)} mex={m} claim={c}")
        H_canonical.cache_clear()
print(f" typed mex == claim == engine: {tot - bad}/{tot} cells (n=2..4, z<=5, heaps<=5)")
print()
print("FROZEN pre-declaration exploration complete. All sections summarized above.")
