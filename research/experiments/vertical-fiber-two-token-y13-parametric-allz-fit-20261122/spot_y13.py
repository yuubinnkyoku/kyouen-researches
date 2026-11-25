#!/usr/bin/env python3
"""Out-of-box spot verification of cand13 against the raw double-recursion engine.

Scope (mirrors the published y=11/y=12 fit audits):
  deep rows R<=130 for a pin/diag/sweep/steady/merge selection of (z,x);
  bigz z=31..40 x d in a 22-value selection, R<=x+z+30;
  x=y=13 edge z=13..40, R<=z+130;
  far d in {30,41,52} for z in {5,12,19,26,33,40}, R<=x+z+30;
  tail raw check on d>=14 rows: R in [x+z+14, x+z+27] equals (x+13) mod 2;
  merge regression vs K0832 single-token closed form on out-of-box merge rows
    z in {31,38,45,52,62,75}, x=13..z-14, R<=x+z+29.
Deterministic; prints aggregate points/bad and the tail/merge check results.
"""
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from cand13 import cand13, single_token_val

def mex(values):
    s = set(values)
    m = 0
    while m in s:
        m += 1
    return m

@lru_cache(None)
def H_canonical(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def sweep(points):
    pts = bad = 0
    first = []
    for (z, x, hi) in points:
        for R in range(1, hi + 1):
            v = H_canonical(R, (x, 13), z)
            c = cand13(z, x, R)
            pts += 1
            if v != c:
                bad += 1
                if len(first) < 20:
                    first.append((z, x, R, v, c))
    return pts, bad, first

def main():
    t0 = time.time()
    pts = bad = 0
    # deep rows R<=130 (diagonal/pin/sweep/steady/merge/frontier representatives)
    deep = [(27, 14), (28, 15),   # z-odd / z-even diagonal d=-13
            (23, 14), (21, 14),   # z-odd skew I row d=-9 / base row d=-7
            (17, 18), (21, 18),   # z-odd pin rows d=+1 / d=-3
            (18, 13), (12, 15),   # z-even pin rows d=-5 / d=+3
            (15, 28),             # z-odd last pin row d=13
            (15, 29), (16, 30),   # sweep rows d=14 (z odd / z even)
            (5, 20), (28, 48),    # steady rows d=15 / d=20
            (29, 13), (30, 16)]   # merge boundary rows
    p, b, f = sweep(((z, x, 130) for (z, x) in deep))
    pts += p; bad += b
    # bigz
    ds = [-13, -12, -11, -9, -7, -5, -3, -1, 0, 1, 3, 5, 7, 9, 11, 12, 13, 14, 15, 20, 28, 34]
    p, b, f2 = sweep(((z, z + d, (z + d) + z + 30) for z in range(31, 41) for d in ds))
    pts += p; bad += b
    # x=y=13 edge
    p, b, f3 = sweep(((z, 13, z + 130) for z in range(13, 41)))
    pts += p; bad += b
    # far d
    p, b, f4 = sweep(((z, z + d, (z + d) + z + 30)
                      for z in (5, 12, 19, 26, 33, 40) for d in (30, 41, 52)))
    pts += p; bad += b
    firsts = (f + f2 + f3 + f4)[:20]
    # tail raw check on sweep/steady rows d>=14
    tail_pts = tail_bad = 0
    for (z, x) in [(15, 29), (20, 35), (31, 46), (26, 41), (33, 48), (40, 54)]:
        for R in range(x + z + 14, x + z + 28):
            v = H_canonical(R, (x, 13), z)
            exp = (x + 13) % 2
            want = 1 if exp == 1 else 0
            tail_pts += 1
            if v != want:
                tail_bad += 1
    # merge regression: cand13 vs K0832 single-token on out-of-box merge rows
    mg_pts = mg_bad = 0
    for z in (31, 38, 45, 52, 62, 75):
        for x in range(13, z - 13):
            for R in range(1, x + z + 30):
                mg_pts += 1
                if cand13(z, x, R) != single_token_val(x + 13, R):
                    mg_bad += 1
    dt = time.time() - t0
    print("spot points:", pts, "bad:", bad, "seconds: %.1f" % dt)
    for t in firsts:
        print("BAD", t)
    print("tail raw check points:", tail_pts, "bad:", tail_bad)
    print("merge regression points:", mg_pts, "bad:", mg_bad)
    print("cache:", H_canonical.cache_info())

if __name__ == '__main__':
    main()
