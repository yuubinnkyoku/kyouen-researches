#!/usr/bin/env python3
"""Out-of-box spot verification of cand20 against the raw double-recursion engine.

Scope (mirrors the published y=11..y=19 fit audits, adapted to the
pre-registered y=20 pin/skew/diagonal classes; ALL selected rows satisfy the
family domain x>=20 by construction with a mechanical assert):
  deep rows R<=130 for a pin/diag/skew/base/sweep/steady/merge selection of
    (z,x): all 10 z-odd pin rows d in {-16,-12,-8,-4,0,4,8,12,16,20} at x=21
    (d=-16 and d=-12 are the box-unreachable lowest z-odd pins, first observed
    here at (37,21) and (33,21)) and all 10 z-even pin rows
    d in {-18,-14,-10,-6,-2,2,6,10,14,18} at x=20 (d=-18 and d=-14
    box-unreachable, first observed here at (38,20) and (34,20)) -- the FIRST
    family with TWO out-of-box pin rows on EACH parity (2+2), pre-declared,
    and the first family with 10 pin rows on both parities -- plus both
    diagonals, z-odd skew (non-pin I) rows (d=-18 / d=-6, plus d=18 -- the
    k=Y=20 skew saturation row th=40, completing the pre-declared four-row
    k=Y census {z-odd I d=18, z-odd I d=20 (= the top pin row at (1,21)),
    z-odd base d=19, z-even base d=20}; note d=0 is a PIN row for y=20,
    unlike y=18 where it carried the mid-band skew), z-odd base rows (the
    d=19 saturation row at k=Y=20), z-even I rows, z-even base rows (incl.
    the d=20 z-even base top saturation row), sweep rows d=21 (both
    parities), steady rows (base/I type both parities), and the merge
    boundary rows x=z-21 (z=43/z=42);
  bigz z=31..40 x d in a 24-value selection, R<=x+z+42;
  x=y=20 edge z=20..44, R<=z+130;
  far d in {40,51,62} for z in {5,12,19,26,33,40}, R<=x+z+42;
  tail raw check on d>=21 rows: R in [x+z+21, x+z+34) equals (x+20) mod 2;
  merge regression vs K0832 single-token closed form on out-of-box merge rows
    z in {42,49,56,63,73,86}, x=20..z-22, R<=x+z+41 (2y+1).
NOTE (pre-declared in the note): the probe box z=0..30 contains ZERO merge
rows for y=20 (x<=z-21 needs z>=42); the merge evidence is entirely here.
Declared spot totals (machine-precomputed in the note): deep 44 rows / 5,720
pts, bigz 240 rows / 28,800 pts, edge 25 rows / 4,050 pts, far 18 rows /
2,484 pts, tail raw 78 pts, merge regression 18,219 comparisons; total
compared points of the fit (probe + spot + tail raw + merge):
165,061.
Deterministic; prints aggregate points/bad and the tail/merge check results.
"""
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from cand20 import cand20, single_token_val

# Same cap as the published y=14/y=15/y=16/y=17/y=18/y=19 fit spot audits
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
            v = H_canonical(R, (x, 20), z)
            c = cand20(z, x, R)
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
    deep = [(41, 21), (40, 20),   # z-odd / z-even diagonal d=-20
            (37, 21), (33, 21), (29, 21), (25, 21), (21, 21), (17, 21), (13, 21), (9, 21), (5, 21), (1, 21),
                                    # all 10 z-odd pin rows d=-16,-12,-8,-4,0,4,8,12,16,20 (x=21)
                                    # (d=-16 / d=-12 box-unreachable; the top pin d=20 is also
                                    #  the k=Y=20 saturating z-odd I row, th=41)
            (38, 20), (34, 20), (30, 20), (26, 20), (22, 20), (18, 20), (14, 20), (10, 20), (6, 20), (2, 20),
                                    # all 10 z-even pin rows d=-18,-14,-10,-6,-2,2,6,10,14,18 (x=20)
                                    # (d=-18 / d=-14 box-unreachable)
            (39, 21), (27, 21),   # z-odd skew (non-pin I) rows d=-18 / d=-6
            (21, 39),   # z-odd I row d=18 (skew saturation: k(d)=floor((18+62)/4)=20=Y, th=40)
                        # -- the 4th row of the pre-declared k=Y saturation census
                        # {z-odd I d=18 / z-odd I d=20 (= top pin row, (1,21)) /
                        #   z-odd base d=19 / z-even base d=20}
            (41, 22), (19, 20), (15, 34),   # z-odd base rows d=-19 / d=1 / d=19 (saturation k=Y=20)
            (40, 21), (22, 21), (16, 33), (2, 21),   # z-even I rows d=-19 / d=-1 / d=17 / d=19
            (36, 20), (20, 24), (4, 24),   # z-even base rows d=-16 / d=4 / d=20 (saturation, k=Y=20)
            (19, 40), (18, 39),   # sweep rows d=21 (z odd / z even)
            (5, 27), (5, 28), (28, 50), (28, 51), (29, 52),   # steady rows base/I both parities
            (43, 22), (42, 21)]   # merge boundary rows x=z-21 (z odd / z even)
    n_deep = len(deep)
    seen = set()
    for (z, x) in deep:
        assert x >= 20, ("deep row below domain", z, x)
        assert (z, x) not in seen, ("deep row duplicate", z, x)
        seen.add((z, x))
    p, b, f = sweep(((z, x, 130) for (z, x) in deep))
    pts += p
    bad += b
    print("block deep done:", n_deep, "rows, pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # bigz (d <= -12 is excluded: z=31 gives x=z+d < 20; the low-pin/diagonal
    # regime d in [-20,-12] is fully covered by the deep rows instead -- the
    # pre-flight domain assert below rejects any below-domain row)
    ds = [-11, -10, -9, -8, -7, -6, -5, -3, -1,
          1, 3, 5, 7, 9, 11, 13, 15, 17, 18, 19, 21, 23, 25, 41]
    assert len(ds) == 24, len(ds)
    for z in range(31, 41):
        for d in ds:
            x = z + d
            assert x >= 20, ("bigz row below domain", z, d)
    p, b, f2 = sweep(((z, z + d, (z + d) + z + 42) for z in range(31, 41) for d in ds))
    pts += p
    bad += b
    print("block bigz done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # x=y=20 edge
    p, b, f3 = sweep(((z, 20, z + 130) for z in range(20, 45)))
    pts += p
    bad += b
    print("block edge done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # far d
    for z in (5, 12, 19, 26, 33, 40):
        for d in (40, 51, 62):
            assert z + d >= 20, ("far row below domain", z, d)
    p, b, f4 = sweep(((z, z + d, (z + d) + z + 42)
                      for z in (5, 12, 19, 26, 33, 40) for d in (40, 51, 62)))
    pts += p
    bad += b
    H_canonical.cache_clear()
    print("block far done: pts", pts, "bad", bad, flush=True)
    firsts = (f + f2 + f3 + f4)[:20]
    # tail raw check on sweep/steady rows d>=21 (both x parities)
    tail_pts = tail_bad = 0
    for (z, x) in [(21, 42), (20, 41), (25, 47), (24, 46), (39, 62), (42, 65)]:
        assert x - z >= 21, ("tail row below d=21", z, x)
        for R in range(x + z + 21, x + z + 34):
            v = H_canonical(R, (x, 20), z)
            exp = (x + 20) % 2
            want = 1 if exp == 1 else 0
            tail_pts += 1
            if v != want:
                tail_bad += 1
    H_canonical.cache_clear()
    # merge regression: cand20 vs K0832 single-token on out-of-box merge rows
    mg_pts = mg_bad = 0
    for z in (42, 49, 56, 63, 73, 86):
        for x in range(20, z - 21):
            for R in range(1, x + z + 42):
                mg_pts += 1
                if cand20(z, x, R) != single_token_val(x + 20, R):
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
