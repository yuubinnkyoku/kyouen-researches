#!/usr/bin/env python3
"""Out-of-box spot verification of cand18 against the raw double-recursion engine.

Scope (mirrors the published y=11..y=17 fit audits, adapted to the
pre-registered y=18 pin/skew/diagonal classes; ALL selected rows satisfy the
family domain x>=18 by construction with a mechanical assert -- the y=14 spot
audit's out-of-domain lesson is applied here):
  deep rows R<=130 for a pin/diag/skew/base/sweep/steady/merge selection of
    (z,x): all 9 z-odd pin rows d in {-14,-10,-6,-2,2,6,10,14,18} at x=19
    (d=-14 is the box-unreachable lowest z-odd pin, first observed here at
    (33,19)) and all 9 z-even pin rows d in {-16,-12,-8,-4,0,4,8,12,16} at
    x=20 (d=-16 box-unreachable lowest z-even pin, first observed here at
    (36,20)), plus diagonals (z-odd/z-even), z-odd skew/non-pin I rows,
    z-even I rows, base rows (incl. the d=18 saturation row on z-even at
    k=Y=18), sweep rows d=19 (both parities), steady rows (base/I type both
    parities), and the merge boundary rows x=z-19 (z=39/z=38);
  bigz z=31..40 x d in a 28-value selection, R<=x+z+38;
  x=y=18 edge z=18..43, R<=z+130;
  far d in {36,47,58} for z in {5,12,19,26,33,40}, R<=x+z+38;
  tail raw check on d>=19 rows: R in [x+z+19, x+z+33) equals (x+18) mod 2;
  merge regression vs K0832 single-token closed form on out-of-box merge rows
    z in {38,45,52,59,69,82}, x=18..z-20, R<=x+z+37.
NOTE (pre-declared in the note): the probe box z=0..30 contains ZERO merge
rows for y=18 (x<=z-19 needs z>=38); the merge evidence is entirely here.
Deterministic; prints aggregate points/bad and the tail/merge check results.
"""
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from cand18 import cand18, single_token_val

# This host has a multi-GB budget, but the memo table is capped to the
# published convention (deterministic LRU eviction; evicted values are
# recomputed, not approximated -> identical outputs). Same cap as the
# published y=14/y=15/y=16/y=17 fit spot audits.
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
            v = H_canonical(R, (x, 18), z)
            c = cand18(z, x, R)
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
    deep = [(37, 19), (36, 18),   # z-odd / z-even diagonal d=-18
            (33, 19), (29, 19), (25, 19), (21, 19), (17, 19), (13, 19), (9, 19), (5, 19), (1, 19),
                                    # all 9 z-odd pin rows d=-14,-10,-6,-2,2,6,10,14,18 (x=19)
            (36, 20), (32, 20), (28, 20), (24, 20), (20, 20), (16, 20), (12, 20), (8, 20), (4, 20),
                                    # all 9 z-even pin rows d=-16,-12,-8,-4,0,4,8,12,16 (x=20)
            (35, 19), (27, 19),   # z-odd skew (non-pin I) rows d=-16 / d=-8
            (35, 18), (19, 20), (15, 32),   # z-odd base rows d=-17 / d=1 / d=17
            (19, 19),            # z-odd I row d=0 (mid-band skew row)
            (36, 19), (25, 20), (16, 33),   # z-even I rows d=-17 / d=-5 / d=17
            (34, 20),            # z-even base row d=-14
            (18, 36),            # z-even base row d=18 (saturation, k reaches Y=18)
            (17, 36), (18, 37),   # sweep rows d=19 (z odd / z even)
            (5, 27), (5, 28), (28, 51), (28, 52), (29, 50),   # steady rows base/I both parities
            (39, 20), (38, 19)]   # merge boundary rows x=z-19 (z odd / z even)
    for (z, x) in deep:
        assert x >= 18, ("deep row below domain", z, x)
    p, b, f = sweep(((z, x, 130) for (z, x) in deep))
    pts += p
    bad += b
    print("block deep done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # bigz (d <= -13 is excluded: z=31 gives x=z+d < 18; the low-pin/diagonal
    # regime d in {-18..-14} is fully covered by the deep rows instead -- the
    # pre-flight domain assert below caught the first draft's d=-16 entry at
    # z=31 (x=15 < 18) exactly as designed, honest record)
    ds = [-13, -12, -11, -10, -9, -7, -6, -5, -3,
          -1, 1, 3, 5, 7, 9, 11, 13, 15, 16, 17, 19, 20, 21, 23, 39]
    for z in range(31, 41):
        for d in ds:
            x = z + d
            assert x >= 18, ("bigz row below domain", z, d)
    p, b, f2 = sweep(((z, z + d, (z + d) + z + 38) for z in range(31, 41) for d in ds))
    pts += p
    bad += b
    print("block bigz done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # x=y=18 edge
    p, b, f3 = sweep(((z, 18, z + 130) for z in range(18, 44)))
    pts += p
    bad += b
    print("block edge done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # far d
    for z in (5, 12, 19, 26, 33, 40):
        for d in (36, 47, 58):
            assert z + d >= 18, ("far row below domain", z, d)
    p, b, f4 = sweep(((z, z + d, (z + d) + z + 38)
                      for z in (5, 12, 19, 26, 33, 40) for d in (36, 47, 58)))
    pts += p
    bad += b
    H_canonical.cache_clear()
    print("block far done: pts", pts, "bad", bad, flush=True)
    firsts = (f + f2 + f3 + f4)[:20]
    # tail raw check on sweep/steady rows d>=19 (both x parities)
    tail_pts = tail_bad = 0
    for (z, x) in [(19, 38), (20, 39), (24, 44), (25, 45), (37, 58), (42, 63)]:
        assert x - z >= 19, ("tail row below d=19", z, x)
        for R in range(x + z + 19, x + z + 33):
            v = H_canonical(R, (x, 18), z)
            exp = (x + 18) % 2
            want = 1 if exp == 1 else 0
            tail_pts += 1
            if v != want:
                tail_bad += 1
    H_canonical.cache_clear()
    # merge regression: cand18 vs K0832 single-token on out-of-box merge rows
    mg_pts = mg_bad = 0
    for z in (38, 45, 52, 59, 69, 82):
        for x in range(18, z - 19):
            for R in range(1, x + z + 38):
                mg_pts += 1
                if cand18(z, x, R) != single_token_val(x + 18, R):
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
