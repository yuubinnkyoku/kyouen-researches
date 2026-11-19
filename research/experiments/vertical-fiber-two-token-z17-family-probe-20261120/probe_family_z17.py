#!/usr/bin/env python3
"""Finite structure probe for the z=17, y>=6 two-token uniform family.

This is a PROBE: raw recursion photographs of H(R;(x,y);17) for a finite
window (y=6..9, x up to XP, R up to x+RHAIR), compared against the
family structure transplanted from K1065 (z=15, odd z family) and
K1077 (z=16, even z family), with the y=5 base slice K1080.

No universal claims are made by this script; it only records where the
predicted band structure holds / breaks inside the computed window and
extracts transient cells.

Predicted odd-z family structure (working hypothesis in the
single-owner declaration note):
  S = x+y, d = x-y, Y = 2y
  T (value 2): base ladder O[1,17]; lattice rows d in {1,5,9,13}
     with ladder extended to r = Y+(d+17)//2; sweep row d=18
     with band O[Y+17, S+17]; steady rows d>=19: O[1,17] u {Y+17}
  P (value 1): base points {18,20,...,Y+16} (exactly y points)
     for rows d>=d1; intermediate band odd O[Y+19,...] as in the slices
  tail: R >= S+18 -> S mod 2
  low-R reduction: H(R;(x,y);17) == H(R;(S,);17) for R <= thr
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)

def mex(values):
    m = 0; values = set(values)
    while m in values: m += 1
    return m

@lru_cache(None)
def H(R, X, z):
    # X: tokens sorted descending tuple
    if R == 0: return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H(R - 1, X[:i] + (v - 1,) + X[i+1:], z))
        else:
            opts.add(H(R - 1, X[:i] + X[i+1:], z + 1))
    if z: opts.add(1 ^ H(R - 1, X, z - 1))
    return mex(opts)

def photo(x, y, z=17, rh=45):
    """row photograph: list of (start, end_inclusive, value) run-lengths"""
    Rmax = x + rh
    vals = [H(R, (max(x, y), min(x, y)), z) for R in range(Rmax + 1)]
    runs = []
    cur = vals[0]; start = 0
    for R in range(1, len(vals)):
        if vals[R] != cur:
            runs.append((start, R - 1, cur)); cur = vals[R]; start = R
    runs.append((start, len(vals) - 1, cur))
    return runs

def fmt(runs):
    return ' '.join(f'[{a},{b}]={v}' for a, b, v in runs)

def odd(a, b):  # inclusive
    if b < a or b % 2 == 0: b -= 1
    if a % 2 == 0: a += 1
    return set(range(a, b + 1, 2)) if a <= b else set()

def preds(x, y, z=17):
    S = x + y; d = x - y; Y = 2 * y
    T = odd(1, 17)
    src = 'ladder'
    if d % 4 == 1 and d <= 13:
        T |= odd(18, Y + (d + z) // 2)
        src = 'lattice'
    if d == 18:
        T |= odd(Y + 17, S + 17)
        src = 'sweep'
    if d >= 19:
        T |= {Y + 17}
        src = 'steady'
    return T, src

def main():
    z = 17
    XMAX = 45
    RHAIR = 45
    deviations = []
    for y in (6, 7, 8):
        print(f'===== y={y} =====')
        for x in range(y, XMAX + 1):
            runs = photo(x, y, z, RHAIR)
            line = f'x={x} d={x-y} S={x+y}: ' + fmt(runs)
            print(line)
    # summary per family rows for y=6..9: first deviations from predicted T in R<=x+42 window
    print('\n===== T-structure agreement check (finite window) =====')
    for y in (6, 7, 8, 9):
        for x in range(y, XMAX + 1):
            Tp, src = preds(x, y, z)
            Rmax = x + 42
            Traw = {R for R in range(1, Rmax + 1) if H(R, (max(x, y), min(x, y)), z) == 2}
            if Traw != (Tp & set(range(1, Rmax + 1))):
                bad = sorted((Traw - Tp) & set(range(1, Rmax + 1)))[:6]
                missing = sorted((Tp - Traw))[:6]
                deviations.append((x, y, src, bad, missing, len(Traw), len((Tp & set(range(1, Rmax + 1))))))
    print(f'T deviations: {len(deviations)} rows')
    for dv in deviations[:40]:
        print(f'  x={dv[0]} y={dv[1]} ({dv[2]}): extra={dv[3]} missing={dv[4]} |Traw|={dv[5]} |Tpred|={dv[6]}')
    cache = H.cache_info()
    print(f'cache: {cache}')

if __name__ == '__main__':
    main()
