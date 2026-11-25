#!/usr/bin/env python3
"""Out-of-box spot verification of cand19 against the raw double-recursion engine.

Scope (mirrors the published y=11..y=18 fit audits, adapted to the
pre-registered y=19 pin/skew/diagonal classes; ALL selected rows satisfy the
family domain x>=19 by construction with a mechanical assert):
  deep rows R<=130 for a pin/diag/skew/base/sweep/steady/merge selection of
    (z,x): all 10 z-odd pin rows d in {-17,-13,-9,-5,-1,3,7,11,15,19} at x=20
    (d=-17 and d=-13 are the box-unreachable lowest z-odd pins, first observed
    here at (37,20) and (33,20) -- the FIRST family with TWO out-of-box pin
    rows on a single parity, pre-declared) and all 9 z-even pin rows
    d in {-15,-11,-7,-3,1,5,9,13,17} at x=19 (d=-15 box-unreachable, first
    observed here at (34,19)), plus both diagonals, z-odd skew (non-pin I)
    rows, z-even I rows, base rows (incl. the d=18 z-odd saturation row at
    k=Y=19), sweep rows d=20 (both parities), steady rows (base/I type both
    parities), and the merge boundary rows x=z-20 (z=41/z=40);
  bigz z=31..40 x d in a 28-value selection, R<=x+z+40;
  x=y=19 edge z=19..43, R<=z+130;
  far d in {38,49,60} for z in {5,12,19,26,33,40}, R<=x+z+40;
  tail raw check on d>=20 rows: R in [x+z+20, x+z+33) equals (x+19) mod 2;
  merge regression vs K0832 single-token closed form on out-of-box merge rows
    z in {39,46,53,60,70,83}, x=19..z-21, R<=x+z+39 (2y+1).
NOTE (pre-declared in the note): the probe box z=0..30 contains ZERO merge
rows for y=19 (x<=z-20 needs z>=39); the merge evidence is entirely here.
Deterministic; prints aggregate points/bad and the tail/merge check results.
"""
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from cand19 import cand19, single_token_val

# Same cap as the published y=14/y=15/y=16/y=17/y=18 fit spot audits
# (deterministic LRU eviction; evicted values are recomputed -> identical outputs).
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
            v = H_canonical(R, (x, 19), z)
            c = cand19(z, x, R)
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
    deep = [(39, 20), (38, 19),   # z-odd / z-even diagonal d=-19
            (37, 20), (33, 20), (29, 20), (25, 20), (21, 20), (17, 20), (13, 20), (9, 20), (5, 20), (1, 20),
                                    # all 10 z-odd pin rows d=-17,-13,-9,-5,-1,3,7,11,15,19 (x=20)
            (34, 19), (30, 19), (26, 19), (22, 19), (18, 19), (14, 19), (10, 19), (6, 19), (2, 19),
                                    # all 9 z-even pin rows d=-15,-11,-7,-3,1,5,9,13,17 (x=19)
            (35, 20), (27, 20),   # z-odd skew (non-pin I) rows d=-15 / d=-7
            (37, 19), (19, 19), (15, 33),   # z-odd base rows d=-18 / d=0 / d=18 (saturation k=Y=19)
            (38, 20), (26, 20),   # z-even I rows d=-18 / d=-6
            (16, 34),            # z-even I row d=18 (max even-d I row)
            (20, 20),            # z-even I row d=0 (mid-band)
            (36, 19), (16, 33),   # z-even base rows d=-17 / d=17
            (15, 35), (16, 36),   # sweep rows d=20 (z odd / z even)
            (5, 26), (5, 27), (28, 49), (28, 50), (29, 50),   # steady rows base/I both parities
            (41, 21), (40, 20)]   # merge boundary rows x=z-20 (z odd / z even)
    for (z, x) in deep:
        assert x >= 19, ("deep row below domain", z, x)
    p, b, f = sweep(((z, x, 130) for (z, x) in deep))
    pts += p
    bad += b
    print("block deep done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # bigz (d <= -13 is excluded: z=31 gives x=z+d < 19; the low-pin/diagonal
    # regime d in [-19,-13] is fully covered by the deep rows instead -- the
    # pre-flight domain assert below rejects any below-domain row)
    ds = [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -1,
          1, 3, 5, 7, 9, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 39]
    for z in range(31, 41):
        for d in ds:
            x = z + d
            assert x >= 19, ("bigz row below domain", z, d)
    p, b, f2 = sweep(((z, z + d, (z + d) + z + 40) for z in range(31, 41) for d in ds))
    pts += p
    bad += b
    print("block bigz done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # x=y=19 edge
    p, b, f3 = sweep(((z, 19, z + 130) for z in range(19, 44)))
    pts += p
    bad += b
    print("block edge done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # far d
    for z in (5, 12, 19, 26, 33, 40):
        for d in (38, 49, 60):
            assert z + d >= 19, ("far row below domain", z, d)
    p, b, f4 = sweep(((z, z + d, (z + d) + z + 40)
                      for z in (5, 12, 19, 26, 33, 40) for d in (38, 49, 60)))
    pts += p
    bad += b
    H_canonical.cache_clear()
    print("block far done: pts", pts, "bad", bad, flush=True)
    firsts = (f + f2 + f3 + f4)[:20]
    # tail raw check on sweep/steady rows d>=20 (both x parities)
    tail_pts = tail_bad = 0
    for (z, x) in [(17, 37), (18, 38), (23, 44), (22, 43), (35, 58), (40, 61)]:
        assert x - z >= 20, ("tail row below d=20", z, x)
        for R in range(x + z + 20, x + z + 33):
            v = H_canonical(R, (x, 19), z)
            exp = (x + 19) % 2
            want = 1 if exp == 1 else 0
            tail_pts += 1
            if v != want:
                tail_bad += 1
    H_canonical.cache_clear()
    # merge regression: cand19 vs K0832 single-token on out-of-box merge rows
    mg_pts = mg_bad = 0
    for z in (39, 46, 53, 60, 70, 83):
        for x in range(19, z - 20):
            for R in range(1, x + z + 40):
                mg_pts += 1
                if cand19(z, x, R) != single_token_val(x + 19, R):
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
