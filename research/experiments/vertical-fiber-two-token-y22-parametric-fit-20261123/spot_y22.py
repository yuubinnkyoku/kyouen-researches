#!/usr/bin/env python3
"""Out-of-box spot verification of cand22 against the raw double-recursion engine.

Scope (mirrors the published y=11..y=21 fit audits, adapted to the
pre-registered y=22 pin/skew/diagonal classes; ALL selected rows satisfy the
family domain x>=22 by construction with a mechanical assert):
  deep rows R<=130 for a pin/diag/skew/base/sweep/steady/merge selection of
    (z,x): all 11 z-odd pin rows d in {-18,-14,-10,-6,-2,2,6,10,14,18,22} at
    x=23 (d=-18, d=-14 and d=-10 are the box-unreachable lowest z-odd pins,
    first observed here at (41,23), (37,23) and (33,23) -- the FIRST family
    with THREE out-of-box pin rows on EACH parity, pre-declared) and all
    11 z-even pin rows d in {-20,-16,-12,-8,-4,0,4,8,12,16,20} at x=22
    (d=-20, d=-16 and d=-12 box-unreachable, first observed here at
    (42,22), (38,22) and (34,22)); for y=22 BOTH parities reach 11 pin rows
    simultaneously for the first time in the series. The top z-odd pin row
    d=22 is simultaneously the k=Y=22 saturating z-odd final I row (th=45),
    and the z-odd skew saturation row d=20 (k=Y=22, th=44) is also included:
    y=22 has the FOUR-row k=Y census {z-odd I d=20, z-odd I d=22, z-odd base
    d=21, z-even base top d=22}; plus both diagonals, z-odd skew (non-pin I)
    rows, base rows (incl. the d=21 z-odd saturation row and the d=22 z-even
    base top saturation row at k=Y=22), z-even I rows, sweep rows d=23 (both
    parities), steady rows (base/I type both parities), and the merge
    boundary rows x=z-23 (z=45/z=46);
  bigz z=31..40 x d in the y=20 24-value selection shifted by +2,
    R<=x+z+46;
  x=y=22 edge z=22..46, R<=z+130;
  far d in {44,55,66} for z in {5,12,19,26,33,40}, R<=x+z+46;
  tail raw check on d>=24 rows: R in [x+z+23, x+z+36) equals (x+22) mod 2;
  merge regression vs K0832 single-token closed form on out-of-box merge rows
    z in {46,53,60,67,77,90}, x=22..z-24, R<=x+z+45 (2y+1).
NOTE (pre-declared in the note): the probe box z=0..30 contains ZERO merge
rows for y=22 (x<=z-23 needs z>=46); the merge evidence is entirely here.
Declared spot totals (machine-precomputed in the note): deep 46 rows /
5,980 pts, bigz 240 rows / 30,240 pts, edge 25 rows / 4,100 pts, far 18
rows / 2,628 pts, tail raw 78 pts, merge regression 19,449 comparisons /
123 rows; total compared points of the fit (probe + spot + tail raw +
merge) 182,042.
Deterministic; prints aggregate points/bad and the tail/merge check results.
"""
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from cand22 import cand22, single_token_val

# Same cap as the published y=14/y=15/y=16/y=17/y=18/y=19/y=20/y=21 fit spot audits
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
            v = H_canonical(R, (x, 22), z)
            c = cand22(z, x, R)
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
    # 46 rows (pre-declared deep geometry: 46 rows / 5,980 points).
    deep = [(45, 23), (44, 22),   # z-odd / z-even diagonal d=-22
            (41, 23), (37, 23), (33, 23), (29, 23), (25, 23), (21, 23), (17, 23), (13, 23), (9, 23), (5, 23), (1, 23),
                                    # all 11 z-odd pin rows d=-18,-14,-10,-6,-2,2,6,10,14,18,22 (x=23)
                                    # (d=-18 / d=-14 / d=-10 box-unreachable; the top pin d=22 is also
                                    #  the k=Y=22 saturating z-odd final I row, th=45)
            (42, 22), (38, 22), (34, 22), (30, 22), (26, 22), (22, 22), (18, 22), (14, 22), (10, 22), (6, 22), (2, 22),
                                    # all 11 z-even pin rows d=-20,-16,-12,-8,-4,0,4,8,12,16,20 (x=22)
                                    # (d=-20 / d=-16 / d=-12 box-unreachable; FIRST family with 11 pins
                                    #  on BOTH parities simultaneously)
            (43, 23), (31, 23),   # z-odd skew (non-pin I) rows d=-20 / d=-8
            (21, 41),             # z-odd skew SATURATION row d=20 (k=Y=22, th=44)
            (43, 22), (23, 23), (15, 36),   # z-odd base rows d=-21 / d=0 / d=21 (saturation k=Y=22)
            (44, 23), (30, 23), (22, 23), (2, 23),   # z-even I rows d=-21 / d=-7 / d=1 (mid-band) / d=21 (max odd-d I row)
            (44, 24), (16, 34), (4, 26),   # z-even base rows d=-20 / d=18 / d=22 (top saturation k=Y=22)
            (15, 38), (16, 39),   # sweep rows d=23 (z odd / z even)
            (5, 29), (5, 30), (28, 52), (28, 53), (29, 53),   # steady rows base/I both parities
            (45, 22), (46, 23)]   # merge boundary rows x=z-23 (z odd / z even)
    n_deep = len(deep)
    seen = set()
    for (z, x) in deep:
        assert x >= 22, ("deep row below domain", z, x)
        assert (z, x) not in seen, ("deep row duplicate", z, x)
        seen.add((z, x))
    p, b, f = sweep(((z, x, 130) for (z, x) in deep))
    pts += p
    bad += b
    print("block deep done:", n_deep, "rows, pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # bigz (d <= -10 is excluded: z=31 gives x=z+d < 22; the low-pin/diagonal
    # regime d in [-22,-10] is fully covered by the deep rows instead -- the
    # pre-flight domain assert below rejects any below-domain row)
    ds = [-9, -8, -7, -6, -5, -4, -3, -1,
          1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 20, 21, 23, 25, 27, 43]
    assert len(ds) == 24, len(ds)
    for z in range(31, 41):
        for d in ds:
            x = z + d
            assert x >= 22, ("bigz row below domain", z, d)
    p, b, f2 = sweep(((z, z + d, (z + d) + z + 46) for z in range(31, 41) for d in ds))
    pts += p
    bad += b
    print("block bigz done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # x=y=22 edge
    p, b, f3 = sweep(((z, 22, z + 130) for z in range(22, 47)))
    pts += p
    bad += b
    print("block edge done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # far d
    for z in (5, 12, 19, 26, 33, 40):
        for d in (44, 55, 66):
            assert z + d >= 22, ("far row below domain", z, d)
    p, b, f4 = sweep(((z, z + d, (z + d) + z + 46)
                      for z in (5, 12, 19, 26, 33, 40) for d in (44, 55, 66)))
    pts += p
    bad += b
    H_canonical.cache_clear()
    print("block far done: pts", pts, "bad", bad, flush=True)
    firsts = (f + f2 + f3 + f4)[:20]
    # tail raw check on sweep/steady rows d>=24 (both x parities)
    tail_pts = tail_bad = 0
    for (z, x) in [(21, 45), (20, 44), (25, 50), (24, 49), (39, 64), (42, 67)]:
        assert x - z >= 24, ("tail row below d=24", z, x)
        for R in range(x + z + 23, x + z + 36):
            v = H_canonical(R, (x, 22), z)
            exp = (x + 22) % 2
            want = 1 if exp == 1 else 0
            tail_pts += 1
            if v != want:
                tail_bad += 1
    H_canonical.cache_clear()
    # merge regression: cand22 vs K0832 single-token on out-of-box merge rows
    mg_pts = mg_bad = 0
    for z in (46, 53, 60, 67, 77, 90):
        for x in range(22, z - 23):
            for R in range(1, x + z + 46):
                mg_pts += 1
                if cand22(z, x, R) != single_token_val(x + 22, R):
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
