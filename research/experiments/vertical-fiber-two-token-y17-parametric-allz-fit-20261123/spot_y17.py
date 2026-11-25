#!/usr/bin/env python3
"""Out-of-box spot verification of cand17 against the raw double-recursion engine.

Scope (mirrors the published y=11..y=16 fit audits, adapted to the
pre-registered y=17 pin/skew/diagonal classes; ALL selected rows satisfy the
family domain x>=17 by construction with a mechanical assert -- the y=14 spot
audit's out-of-domain lesson is applied here):
  deep rows R<=130 for a pin/diag/skew/base/sweep/steady/merge selection of
    (z,x): all 9 z-odd pin rows d in {-15,-11,-7,-3,1,5,9,13,17} and all 8
    z-even pin rows d in {-13,-9,-5,-1,3,7,11,15} (row-count law check:
    first 9-pin-row family), plus diagonal (z-odd/z-even), non-pin I rows,
    base rows (incl. the d=17 saturation row and the d=16 z-even I row),
    sweep rows d=18 (both parities), steady rows (base/I type both
    parities), and the merge boundary rows x=z-18 (z=35/z=36);
  bigz z=31..40 x d in a 27-value selection, R<=x+z+36;
  x=y=17 edge z=17..42, R<=z+130;
  far d in {34,45,56} for z in {5,12,19,26,33,40}, R<=x+z+36;
  tail raw check on d>=18 rows: R in [x+z+18, x+z+31] equals (x+17) mod 2;
  merge regression vs K0832 single-token closed form on out-of-box merge rows
    z in {35,42,49,56,66,79}, x=17..z-18, R<=x+z+35.
NOTE (pre-declared in the note): the probe box z=0..30 contains ZERO merge
rows for y=17 (x<=z-18 needs z>=35); the merge evidence is entirely here.
Deterministic; prints aggregate points/bad and the tail/merge check results.
"""
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from cand17 import cand17, single_token_val

# This host has a ~3 GB budget, so the memo table is capped (deterministic LRU
# eviction; evicted values are recomputed, not approximated -> identical
# outputs). Same convention as the published y=14/y=15 fit spot audits.
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
            v = H_canonical(R, (x, 17), z)
            c = cand17(z, x, R)
            pts += 1
            if v != c:
                bad += 1
                if len(first) < 20:
                    first.append((z, x, R, v, c))
    return pts, bad, first

def main():
    t0 = time.time()
    pts = bad = 0
    # deep rows R<=130 (diagonal/all-pin/skew/base/sweep/steady/merge representatives)
    deep = [(35, 18), (36, 19),   # z-odd / z-even diagonal d=-17
            (33, 18), (29, 18), (25, 18), (21, 18), (17, 18), (13, 18), (9, 18), (5, 18), (15, 32),
                                    # all 9 z-odd pin rows d=-15,-11,-7,-3,1,5,9,13,17
            (30, 17), (26, 17), (22, 17), (18, 17), (24, 27), (20, 27), (16, 27), (30, 45),
                                    # all 8 z-even pin rows d=-13,-9,-5,-1,3,7,11,15
            (35, 22), (27, 20),   # z-odd non-pin I rows d=-13 / d=-7
            (33, 17), (19, 19), (15, 31),   # z-odd base rows d=-16 / d=0 / d=16
            (34, 18), (24, 18),   # z-even I rows d=-16 / d=-6
            (30, 46),            # z-even I row d=16 (max even-d I row)
            (32, 17), (30, 47),   # z-even base rows d=-15 / d=17 (saturation)
            (15, 33), (16, 34),   # sweep rows d=18 (z odd / z even)
            (18, 18),            # z-even I row d=0
            (5, 26), (5, 27), (28, 49), (28, 50), (29, 48),   # steady rows base/I both parities
            (35, 17), (36, 18)]   # merge boundary rows x=z-18 (z odd / z even)
    for (z, x) in deep:
        assert x >= 17, ("deep row below domain", z, x)
    p, b, f = sweep(((z, x, 130) for (z, x) in deep))
    pts += p; bad += b
    print("block deep done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # bigz
    ds = [-14, -13, -12, -11, -10, -9, -8, -7, -5, -4, -3, -1,
          1, 3, 5, 7, 9, 11, 13, 14, 15, 16, 17, 18, 19, 21, 37]
    pts_bigz = 0
    for z in range(31, 41):
        for d in ds:
            x = z + d
            assert x >= 17, ("bigz row below domain", z, d)
    p, b, f2 = sweep(((z, z + d, (z + d) + z + 36) for z in range(31, 41) for d in ds))
    pts += p; bad += b
    print("block bigz done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # x=y=17 edge
    p, b, f3 = sweep(((z, 17, z + 130) for z in range(17, 43)))
    pts += p; bad += b
    print("block edge done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # far d
    p, b, f4 = sweep(((z, z + d, (z + d) + z + 36)
                      for z in (5, 12, 19, 26, 33, 40) for d in (34, 45, 56)))
    pts += p; bad += b
    H_canonical.cache_clear()
    print("block far done: pts", pts, "bad", bad, flush=True)
    firsts = (f + f2 + f3 + f4)[:20]
    # tail raw check on sweep/steady rows d>=18 (both x parities)
    tail_pts = tail_bad = 0
    for (z, x) in [(17, 35), (18, 36), (23, 42), (22, 41), (35, 56), (40, 61)]:
        assert x - z >= 18, ("tail row below d=18", z, x)
        for R in range(x + z + 18, x + z + 32):
            v = H_canonical(R, (x, 17), z)
            exp = (x + 17) % 2
            want = 1 if exp == 1 else 0
            tail_pts += 1
            if v != want:
                tail_bad += 1
    H_canonical.cache_clear()
    # merge regression: cand17 vs K0832 single-token on out-of-box merge rows
    mg_pts = mg_bad = 0
    for z in (35, 42, 49, 56, 66, 79):
        for x in range(17, z - 18):
            for R in range(1, x + z + 36):
                mg_pts += 1
                if cand17(z, x, R) != single_token_val(x + 17, R):
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
