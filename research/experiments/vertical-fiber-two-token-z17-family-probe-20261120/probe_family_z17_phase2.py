#!/usr/bin/env python3
"""Phase-2 probe for the z=17, y>=6 two-token uniform family.

Extracts machine-readable row features from raw recursion for a finite
window, spot-checks the y-parameterized skeleton at deep y, and measures
the low-R reduction threshold (height-only collapse to a single token).
Finite probe only; no universal claims.
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(200000)

def mex(values):
    m = 0; values = set(values)
    while m in values: m += 1
    return m

@lru_cache(None)
def H(R, X, z):
    if R == 0: return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H(R - 1, X[:i] + (v - 1,) + X[i+1:], z))
        else:
            opts.add(H(R - 1, X[:i] + X[i+1:], z + 1))
    if z: opts.add(1 ^ H(R - 1, X, z - 1))
    return mex(opts)

def row(x, y, z=17, Rmax=None):
    if Rmax is None: Rmax = x + 45
    return [H(R, (x if x >= y else y, y if x >= y else x), z) for R in range(Rmax + 1)]

def features(x, y, z=17, Rmax=None):
    vals = row(x, y, z, Rmax)
    T = [R for R, v in enumerate(vals) if v == 2]
    P = [R for R, v in enumerate(vals) if v == 1]
    # ladder top
    top = None
    for R in range(1, min(17, len(vals) - 1) + 1):
        if vals[R] == 2: top = R
        if R + 2 < len(vals) and vals[R + 2] != 2 and vals[R] == 2:
            break
    # first value-2 beyond 17 (generic feature)
    adv = [r for r in T if r > 17]
    # base-point run: value-1 at even R starting at 18, contiguous evens
    base_end = None
    r = 18
    while r < len(vals) and vals[r] == 1:
        base_end = r; r += 2
    # saturation start: all R >= s have value 1 (limited window evidence)
    s = None
    for cand in range(18, len(vals)):
        if all(vals[R] == 1 for R in range(cand, len(vals))):
            s = cand; break
    # tail: constant beyond tb (last run)
    tail_val, tb = None, None
    v = vals[-1]
    R = len(vals) - 1
    while R > 0 and vals[R - 1] == v: R -= 1
    if R <= len(vals) - 8:
        tail_val, tb = v, R
    return dict(x=x, y=y, S=x + y, d=x - y, top=top, adv=adv,
                base_end=base_end, sat=s, tail=tail_val, tail_from=tb,
                T=T, P=P, Rmax=len(vals) - 1)

def main():
    z = 17
    print('== feature table (y=6..12, all x=y..min(y+40,60)) ==')
    for y in range(6, 13):
        for x in range(y, min(y + 40, 61) + 1):
            f = features(x, y, z)
            print(f"y={y} x={x} d={f['d']} S={f['S']} top={f['top']} adv={f['adv']} "
                  f"base_end={f['base_end']} sat={f['sat']} tail={f['tail']}@{f['tail_from']}")
    print('\n== skeleton check at deep y (T-point / pin / sweep / steady) ==')
    for y in (13, 20, 40, 61, 100):
        # lattice row d=9: expect single advance point 2y+13
        x = y + 9; vals = row(x, y, z, min(x + 42, 2 * y + 40))
        r = 2 * y + 13
        ok = 17 < r < len(vals) and vals[r] == 2 and all(
            vals[q] == 0 for q in range(19, r, 2)) if r < len(vals) else False
        print(f'y={y} lattice d=9 x={x}: point@{r}={vals[r] if r < len(vals) else "?"} '
              f"gap-clean={ok} window={len(vals)-1}")
        # pin row d=17: expect single point 2y+17
        x = y + 17; vals = row(x, y, z, min(x + 42, 2 * y + 44))
        r = 2 * y + 17
        print(f'y={y} pin d=17 x={x}: point@{r}={vals[r] if r < len(vals) else "?"} '
              f'ladder_end17={vals[17]}')
        # sweep row d=18: band O[2y+17, S+17]
        x = y + 18; S = x + y; vals = row(x, y, z, S + 30)
        tband = [R for R in range(1, len(vals)) if vals[R] == 2 and R > 17]
        expect = list(range(2 * y + 17, S + 18, 2))
        pred = (tband == expect)
        print(f'y={y} sweep d=18 x={x} S={S}: bandok={(tband == expect)} '
              f'first={tband[:2]} last={tband[-1] if tband else None} wantlast={S+17 if S%2 else S+16}')
        # steady row d=19: T = O[1,17] u {2y+17}; P base evens 2y+16, band odd Y+19..S+17, tail S+18 -> S mod 2
        x = y + 19; S = x + y; vals = row(x, y, z, S + 24)
        Tset = {R for R in range(1, len(vals)) if vals[R] == 2}
        Texp = set(range(1, 18, 2)) | ({2 * y + 17} if 2 * y + 17 < len(vals) else set())
        Pset = {R for R in range(1, len(vals)) if vals[R] == 1}
        Pexp = set(range(18, 2 * y + 17, 2))
        Pexp |= {R for R in range(2 * y + 19, min(S + 18, len(vals)), 2)}
        if S % 2 == 1: Pexp |= {R for R in range(S + 18, len(vals))}
        mism = (Tset != (Texp & Tset)) or (Pset != (Pexp & Pset))
        print(f'y={y} steady d=19 x={x} S={S}: mismatch={mism} '
              f'tail={vals[-1]} wanttail={S % 2}')
    print('\n== low-R reduction threshold (two tokens vs single token S) ==')
    for y in range(6, 13):
        worst = None
        for x in range(y, min(y + 30, 55) + 1):
            S = x + y
            Rmax = x + 45
            thr = None
            prev = True
            for R in range(0, Rmax + 1):
                a = H(R, (max(x, y), min(x, y)), z)
                b = H(R, (S,), z)
                if a != b:
                    thr = R; break
            if thr is None: thr = 10 ** 9
            if worst is None or thr < worst[0]:
                worst = (thr, x, y)
            if thr < 40: print(f'  FIRST-BREAK y={y} x={x} S={x+y} at R={thr}')
        print(f'y={y}: uniform threshold (min break over rows) = {worst[0]} at x={worst[1]}')
    print('\ncache:', H.cache_info())

if __name__ == '__main__':
    main()
