#!/usr/bin/env python3
"""Out-of-box spot verification of cand15 against the raw double-recursion engine.

Scope (mirrors the published y=11/y=12/y=13/y=14 fit audits, adapted to the
pre-registered y=15 pin/skew/diagonal classes; ALL selected rows satisfy the
family domain x>=15 -- the y=14 spot audit's out-of-domain lesson is applied
by construction here):
  deep rows R<=130 for a pin/diag/skew/base/sweep/steady/merge selection of
    (z,x): all 8 z-odd pin rows d in {-13,-9,-5,-1,3,7,11,15} and all 7
    z-even pin rows d in {-11,-7,-3,1,5,9,13} (row-count law check), plus
    diagonal (z-odd/z-even), non-pin I rows, base rows (incl. the d=15
    saturation row and the d=14 z-even I row), sweep rows d=16 (both
    parities), steady rows (base/I type both parities), and the merge
    boundary rows x=z-16 (z=31/z=32);
  bigz z=31..40 x d in a 27-value selection, R<=x+z+32;
  x=y=15 edge z=15..40, R<=z+130;
  far d in {32,43,54} for z in {5,12,19,26,33,40}, R<=x+z+32;
  tail raw check on d>=16 rows: R in [x+z+16, x+z+29] equals (x+15) mod 2;
  merge regression vs K0832 single-token closed form on out-of-box merge rows
    z in {31,38,45,52,62,75}, x=15..z-16, R<=x+z+31.
NOTE (pre-declared in the note): the probe box z=0..30 contains ZERO merge
rows for y=15 (x<=z-16 needs z>=31); the merge evidence is entirely here.
Deterministic; prints aggregate points/bad and the tail/merge check results.
"""
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from cand15 import cand15, single_token_val

# This host has a ~3 GB budget, so the memo table is capped (deterministic LRU
# eviction; evicted values are recomputed, not approximated -> identical
# outputs). Same convention as the published y=14 fit spot audit.
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
            v = H_canonical(R, (x, 15), z)
            c = cand15(z, x, R)
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
    deep = [(31, 16), (30, 15),   # z-odd / z-even diagonal d=-15
            (29, 16), (25, 16), (21, 16), (19, 18), (17, 20), (19, 26), (23, 34), (15, 30),
                                    # all 8 z-odd pin rows d=-13,-9,-5,-1,3,7,11,15
            (26, 15), (24, 17), (20, 17), (18, 19), (18, 23), (22, 31), (26, 39),
                                    # all 7 z-even pin rows d=-11,-7,-3,1,5,9,13
            (29, 18), (27, 20),   # z-odd non-pin I rows d=-11 / d=-7
            (31, 17), (19, 19), (15, 29),   # z-odd base rows d=-14 / d=0 / d=14
            (30, 16), (22, 16),   # z-even I rows d=-14 / d=-6
            (30, 44),            # z-even I row d=14 (max even-d I row)
            (28, 15), (30, 45),   # z-even base rows d=-13 / d=15 (saturation)
            (15, 31), (16, 32),   # sweep rows d=16 (z odd / z even)
            (18, 18),            # z-even I row d=0
            (5, 22), (5, 23), (28, 47), (28, 48), (29, 48),   # steady rows base/I both parities
            (31, 15), (32, 16)]   # merge boundary rows x=z-16 (z odd / z even)
    for (z, x) in deep:
        assert x >= 15, ("deep row below domain", z, x)
    p, b, f = sweep(((z, x, 130) for (z, x) in deep))
    pts += p; bad += b
    print("block deep done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # bigz
    ds = [-16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -5, -4, -3, -1,
          1, 3, 5, 7, 9, 11, 12, 13, 14, 15, 16, 21, 35]
    p, b, f2 = sweep(((z, z + d, (z + d) + z + 32) for z in range(31, 41) for d in ds))
    pts += p; bad += b
    print("block bigz done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # x=y=15 edge
    p, b, f3 = sweep(((z, 15, z + 130) for z in range(15, 41)))
    pts += p; bad += b
    print("block edge done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # far d
    p, b, f4 = sweep(((z, z + d, (z + d) + z + 32)
                      for z in (5, 12, 19, 26, 33, 40) for d in (32, 43, 54)))
    pts += p; bad += b
    H_canonical.cache_clear()
    print("block far done: pts", pts, "bad", bad, flush=True)
    firsts = (f + f2 + f3 + f4)[:20]
    # tail raw check on sweep/steady rows d>=16 (both x parities)
    tail_pts = tail_bad = 0
    for (z, x) in [(15, 31), (16, 32), (21, 37), (20, 36), (31, 47), (40, 56)]:
        for R in range(x + z + 16, x + z + 30):
            v = H_canonical(R, (x, 15), z)
            exp = (x + 15) % 2
            want = 1 if exp == 1 else 0
            tail_pts += 1
            if v != want:
                tail_bad += 1
    H_canonical.cache_clear()
    # merge regression: cand15 vs K0832 single-token on out-of-box merge rows
    mg_pts = mg_bad = 0
    for z in (31, 38, 45, 52, 62, 75):
        for x in range(15, z - 16):
            for R in range(1, x + z + 32):
                mg_pts += 1
                if cand15(z, x, R) != single_token_val(x + 15, R):
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
