#!/usr/bin/env python3
"""Out-of-box spot verification of cand14 against the raw double-recursion engine.

Scope (mirrors the published y=11/y=12/y=13 fit audits, adapted to the
pre-registered y=14 pin/skew/diagonal classes):
  deep rows R<=130 for a pin/diag/skew/base/sweep/steady/merge selection of (z,x)
    (honesty record: the first probe of this script selected (19,13) as the
    z-odd d=-6 pin-row representative, which is BELOW the family domain x>=14
    (the state {13,14} is the y=13-family x=14 row and raw value 1 there is
    correct); cand14 makes no claim for x<14. The row was corrected to
    (21,15) BEFORE any publication; reruns below are with the corrected row);
  bigz z=31..40 x d in a 23-value selection, R<=x+z+30;
  x=y=14 edge z=14..40, R<=z+130;
  far d in {30,41,52} for z in {5,12,19,26,33,40}, R<=x+z+30;
  tail raw check on d>=15 rows: R in [x+z+15, x+z+28] equals (x+14) mod 2;
  merge regression vs K0832 single-token closed form on out-of-box merge rows
    z in {31,38,45,52,62,75}, x=14..z-15, R<=x+z+29.
Deterministic; prints aggregate points/bad and the tail/merge check results.
"""
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from cand14 import cand14, single_token_val

# The y=11/y=12/y=13 spot audits ran uncapped on hosts with more RAM; this host
# has a ~3 GB budget, so the memo table is capped (deterministic LRU eviction;
# evicted values are recomputed, not approximated -> identical outputs).
CACHE_CAP = 1_500_000

def mex(values):
    s = set(values)
    m = 0
    while m in s:
        m += 1
    return m

@lru_cache(CACHE_CAP)
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
            v = H_canonical(R, (x, 14), z)
            c = cand14(z, x, R)
            pts += 1
            if v != c:
                bad += 1
                if len(first) < 20:
                    first.append((z, x, R, v, c))
    return pts, bad, first

def main():
    t0 = time.time()
    pts = bad = 0
    # deep rows R<=130 (diagonal/pin/skew/base/sweep/steady/merge representatives)
    deep = [(29, 15), (28, 14),   # z-odd / z-even diagonal d=-14
            (23, 15), (23, 16),   # z-odd skew I row d=-8 / base row d=-7
            (17, 19), (21, 15),   # z-odd pin rows d=+2 / d=-6 (d==2 mod 4 class)
            (18, 14), (12, 16),   # z-even pin rows d=-4 / d=+4 (d==0 mod 4 class)
            (15, 29),              # z-odd last pin row d=14 (=y)
            (15, 30), (16, 31),    # sweep rows d=15 (z odd / z even)
            (5, 21), (28, 48),     # steady rows d=16 / d=20
            (31, 16), (30, 15)]    # merge boundary rows x=z-15
    p, b, f = sweep(((z, x, 130) for (z, x) in deep))
    pts += p; bad += b
    print("block deep done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # bigz
    ds = [-14, -13, -12, -11, -9, -8, -7, -5, -4, -3, -1, 0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 20, 34]
    p, b, f2 = sweep(((z, z + d, (z + d) + z + 30) for z in range(31, 41) for d in ds))
    pts += p; bad += b
    print("block bigz done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # x=y=14 edge
    p, b, f3 = sweep(((z, 14, z + 130) for z in range(14, 41)))
    pts += p; bad += b
    print("block edge done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # far d
    p, b, f4 = sweep(((z, z + d, (z + d) + z + 30)
                      for z in (5, 12, 19, 26, 33, 40) for d in (30, 41, 52)))
    pts += p; bad += b
    H_canonical.cache_clear()
    print("block far done: pts", pts, "bad", bad, flush=True)
    firsts = (f + f2 + f3 + f4)[:20]
    # tail raw check on sweep/steady rows d>=15
    tail_pts = tail_bad = 0
    for (z, x) in [(15, 30), (20, 35), (31, 46), (26, 41), (33, 48), (40, 54)]:
        for R in range(x + z + 15, x + z + 29):
            v = H_canonical(R, (x, 14), z)
            exp = (x + 14) % 2
            want = 1 if exp == 1 else 0
            tail_pts += 1
            if v != want:
                tail_bad += 1
    # merge regression: cand14 vs K0832 single-token on out-of-box merge rows
    mg_pts = mg_bad = 0
    for z in (31, 38, 45, 52, 62, 75):
        for x in range(14, z - 15):
            for R in range(1, x + z + 30):
                mg_pts += 1
                if cand14(z, x, R) != single_token_val(x + 14, R):
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
