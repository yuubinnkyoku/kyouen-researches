#!/usr/bin/env python3
"""Out-of-box spot verification of cand21 against the raw double-recursion engine.

Scope (mirrors the published y=11..y=20 fit audits, adapted to the
pre-registered y=21 pin/skew/diagonal classes; ALL selected rows satisfy the
family domain x>=21 by construction with a mechanical assert):
  deep rows R<=130 for a pin/diag/skew/base/sweep/steady/merge selection of
    (z,x): all 11 z-odd pin rows d in {-19,-15,-11,-7,-3,1,5,9,13,17,21} at
    x=22 (d=-19, d=-15 and d=-11 are the box-unreachable lowest z-odd pins,
    first observed here at (41,22), (37,22) and (33,22) -- the FIRST family
    with THREE out-of-box pin rows on a single parity, pre-declared) and all
    10 z-even pin rows d in {-17,-13,-9,-5,-1,3,7,11,15,19} at x=21 (d=-17
    and d=-13 box-unreachable, first observed here at (38,21) and (34,21));
    the top z-odd pin row d=21 is simultaneously the k=Y=21 saturating final
    I row (three-row k=Y census {z-odd base d=20, z-odd I d=21, z-even base
    top d=21}); plus both diagonals, z-odd skew (non-pin I) rows, base rows
    (incl. the d=20 z-odd saturation row and the d=21 z-even base top
    saturation row at k=Y=21), z-even I rows, sweep rows d=22 (both
    parities), steady rows (base/I type both parities), and the merge
    boundary rows x=z-22 (z=43/z=44);
  bigz z=31..40 x d in the y=19 28-value selection shifted by +2,
    R<=x+z+44;
  x=y=21 edge z=21..45, R<=z+130;
  far d in {42,53,64} for z in {5,12,19,26,33,40}, R<=x+z+44;
  tail raw check on d>=23 rows: R in [x+z+22, x+z+35) equals (x+21) mod 2;
  merge regression vs K0832 single-token closed form on out-of-box merge rows
    z in {43,50,57,64,74,87}, x=21..z-23, R<=x+z+43 (2y+1).
NOTE (pre-declared in the note): the probe box z=0..30 contains ZERO merge
rows for y=21 (x<=z-22 needs z>=43); the merge evidence is entirely here.
Declared spot totals (machine-precomputed in the note): deep 44 rows /
5,720 pts, bigz 280 rows / m pts, edge 25 rows / 4,075 pts, far 18 rows /
f pts, tail raw 78 pts, merge regression M comparisons; total compared
points of the fit (probe + spot + tail raw + merge): computed in the note.
Deterministic; prints aggregate points/bad and the tail/merge check results.
"""
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from cand21 import cand21, single_token_val

# Same cap as the published y=14/y=15/y=16/y=17/y=18/y=19/y=20 fit spot audits
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
            v = H_canonical(R, (x, 21), z)
            c = cand21(z, x, R)
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
    # 44 rows (pre-declared deep geometry: 44 rows / 5,720 points).
    deep = [(43, 22), (42, 21),   # z-odd / z-even diagonal d=-21
            (41, 22), (37, 22), (33, 22), (29, 22), (25, 22), (21, 22), (17, 22), (13, 22), (9, 22), (5, 22), (1, 22),
                                    # all 11 z-odd pin rows d=-19,-15,-11,-7,-3,1,5,9,13,17,21 (x=22)
                                    # (d=-19 / d=-15 / d=-11 box-unreachable; the top pin d=21 is also
                                    #  the k=Y=21 saturating z-odd final I row, th=43)
            (38, 21), (34, 21), (30, 21), (26, 21), (22, 21), (18, 21), (14, 21), (10, 21), (6, 21), (2, 21),
                                    # all 10 z-even pin rows d=-17,-13,-9,-5,-1,3,7,11,15,19 (x=21)
                                    # (d=-17 / d=-13 box-unreachable)
            (39, 22), (27, 22),   # z-odd skew (non-pin I) rows d=-17 / d=-5
            (41, 21), (21, 21), (15, 35),   # z-odd base rows d=-20 / d=0 / d=20 (saturation k=Y=21)
            (42, 22), (28, 22), (22, 22), (2, 22),   # z-even I rows d=-20 / d=-6 / d=0 (mid-band) / d=20 (max even-d I row)
            (40, 21), (16, 33), (4, 25),   # z-even base rows d=-19 / d=17 / d=21 (top saturation k=Y=21)
            (15, 37), (16, 38),   # sweep rows d=22 (z odd / z even)
            (5, 28), (5, 29), (28, 51), (28, 52), (29, 52),   # steady rows base/I both parities
            (43, 21), (44, 22)]   # merge boundary rows x=z-22 (z odd / z even)
    n_deep = len(deep)
    seen = set()
    for (z, x) in deep:
        assert x >= 21, ("deep row below domain", z, x)
        assert (z, x) not in seen, ("deep row duplicate", z, x)
        seen.add((z, x))
    p, b, f = sweep(((z, x, 130) for (z, x) in deep))
    pts += p
    bad += b
    print("block deep done:", n_deep, "rows, pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # bigz (d <= -11 is excluded: z=31 gives x=z+d < 21; the low-pin/diagonal
    # regime d in [-21,-11] is fully covered by the deep rows instead -- the
    # pre-flight domain assert below rejects any below-domain row)
    ds = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1,
          1, 3, 5, 7, 9, 11, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 41]
    assert len(ds) == 28, len(ds)
    for z in range(31, 41):
        for d in ds:
            x = z + d
            assert x >= 21, ("bigz row below domain", z, d)
    p, b, f2 = sweep(((z, z + d, (z + d) + z + 44) for z in range(31, 41) for d in ds))
    pts += p
    bad += b
    print("block bigz done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # x=y=21 edge
    p, b, f3 = sweep(((z, 21, z + 130) for z in range(21, 46)))
    pts += p
    bad += b
    print("block edge done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # far d
    for z in (5, 12, 19, 26, 33, 40):
        for d in (42, 53, 64):
            assert z + d >= 21, ("far row below domain", z, d)
    p, b, f4 = sweep(((z, z + d, (z + d) + z + 44)
                      for z in (5, 12, 19, 26, 33, 40) for d in (42, 53, 64)))
    pts += p
    bad += b
    H_canonical.cache_clear()
    print("block far done: pts", pts, "bad", bad, flush=True)
    firsts = (f + f2 + f3 + f4)[:20]
    # tail raw check on sweep/steady rows d>=23 (both x parities)
    tail_pts = tail_bad = 0
    for (z, x) in [(21, 44), (20, 43), (25, 49), (24, 48), (39, 64), (42, 67)]:
        assert x - z >= 23, ("tail row below d=23", z, x)
        for R in range(x + z + 22, x + z + 35):
            v = H_canonical(R, (x, 21), z)
            exp = (x + 21) % 2
            want = 1 if exp == 1 else 0
            tail_pts += 1
            if v != want:
                tail_bad += 1
    H_canonical.cache_clear()
    # merge regression: cand21 vs K0832 single-token on out-of-box merge rows
    mg_pts = mg_bad = 0
    for z in (43, 50, 57, 64, 74, 87):
        for x in range(21, z - 22):
            for R in range(1, x + z + 44):
                mg_pts += 1
                if cand21(z, x, R) != single_token_val(x + 21, R):
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
