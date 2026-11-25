#!/usr/bin/env python3
"""Out-of-box spot verification of cand23 against the raw double-recursion engine.

Scope (mirrors the published y=11..y=22 fit audits, adapted to the
pre-registered y=23 pin/skew/diagonal classes; ALL selected rows satisfy the
family domain x>=23 by construction with a mechanical assert):
  deep rows R<=130 for a pin/diag/skew/base/sweep/steady/merge selection of
    (z,x): all 12 z-odd pin rows d in {-21,-17,-13,-9,-5,-1,3,7,11,15,19,23}
    at x=24 (d=-21, d=-17, d=-13 and d=-9 are the box-unreachable lowest
    z-odd pins, first observed here at (45,24), (41,24), (37,24) and (33,24)
    -- the FIRST family with FOUR out-of-box pin rows on a single parity,
    pre-declared) and all 11 z-even pin rows d in
    {-19,-15,-11,-7,-3,1,5,9,13,17,21} at x=23 (d=-19, d=-15 and d=-11
    box-unreachable, first observed here at (42,23), (38,23) and (34,23));
    the top z-odd pin row d=23 is simultaneously the k=Y=23 saturating final
    I row (three-row k=Y census {z-odd base d=22, z-odd I d=23, z-even base
    top d=23}, machine-observed k=23=Y on all three rows); plus both
    diagonals, z-odd skew (non-pin I) rows, base rows (incl. the d=22 z-odd
    saturation row and the d=23 z-even base top saturation row at k=Y=23),
    z-even I rows, sweep rows d=24 (both parities), steady rows (base/I type
    both parities), and the merge boundary rows x=z-24 (z=47/z=48);
  bigz z=31..40 x d in the y=21 28-value selection shifted by +2,
    R<=x+z+48;
  x=y=23 edge z=23..47, R<=z+130;
  far d in {46,57,68} for z in {5,12,19,26,33,40}, R<=x+z+48;
  tail raw check on d>=24 rows: R in [x+z+24, x+z+37) equals (x+23) mod 2;
  merge regression vs K0832 single-token closed form on out-of-box merge rows
    z in {47,54,61,68,78,91}, x=23..z-25, R<=x+z+47 (2y+1).
NOTE (pre-declared in the note): the probe box z=0..30 contains ZERO merge
rows for y=23 (x<=z-24 needs z>=47); the merge evidence is entirely here.
Declared spot totals (machine-precomputed in the note): deep 46 rows /
5,980 pts, bigz 280 rows / 36,190 pts, edge 25 rows / 4,125 pts, far 18
rows / 2,700 pts, tail raw 78 pts, merge regression 117 rows / 19,005
comparisons; total compared points of the fit (probe + spot + tail raw +
merge): 194,899.
CACHING CAVEAT (honest, this family): the bigz block of y=23 exceeds the
300-second sandbox command cap in a single process (the first attempt was
killed by the cap; the y=22 battery's largest block was bigz 168s). The
reference bigz coverage is therefore executed as a UNION OF z SUB-RANGES via
spot_chunk_rerun_y23.py 'bigz:a-b' -- the sweep is a pure function of
(R, tokens, z) and cache state does not affect values, so the union of the
sub-range sweeps equals the full-range sweep point-for-point; the deep/edge/
far/tailmerge blocks run as byte-exact whole-block slices exactly as in the
y=21/y=22 fit audits.
Deterministic; prints aggregate points/bad and the tail/merge check results.
"""
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from cand23 import cand23, single_token_val

# Same cap as the published y=14..y=22 fit spot audits
# (deterministic LRU eviction; evicted values are recomputed -> identical outputs).
CACHE_CAP = 1_500_000

# bigz z-range (module-level so spot_chunk_rerun_y23.py can bind sub-ranges
# per chunk run; the reference full main() uses the full range)
BIGZ_ZS = range(31, 41)

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
            v = H_canonical(R, (x, 23), z)
            c = cand23(z, x, R)
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
    deep = [(47, 24), (46, 23),   # z-odd / z-even diagonal d=-23
            (45, 24), (41, 24), (37, 24), (33, 24), (29, 24), (25, 24), (21, 24), (17, 24), (13, 24), (9, 24), (5, 24), (1, 24),
                                    # all 12 z-odd pin rows d=-21,-17,-13,-9,-5,-1,3,7,11,15,19,23 (x=24)
                                    # (d=-21 / d=-17 / d=-13 / d=-9 box-unreachable; the top pin d=23 is also
                                    #  the k=Y=23 saturating z-odd final I row, th=47)
            (42, 23), (38, 23), (34, 23), (30, 23), (26, 23), (22, 23), (18, 23), (14, 23), (10, 23), (6, 23), (2, 23),
                                    # all 11 z-even pin rows d=-19,-15,-11,-7,-3,1,5,9,13,17,21 (x=23)
                                    # (d=-19 / d=-15 / d=-11 box-unreachable)
            (43, 24), (31, 24),   # z-odd skew (non-pin I) rows d=-19 / d=-7
            (43, 23), (23, 23), (21, 43),   # z-odd base rows d=-20 / d=0 / d=22 (saturation k=Y=23)
            (44, 24), (30, 24), (22, 24), (2, 24),   # z-even I rows d=-20 / d=-6 / d=2 (mid-band) / d=22 (max even-d I row)
            (44, 23), (16, 35), (4, 27),   # z-even base rows d=-21 / d=19 / d=23 (top saturation k=Y=23)
            (15, 39), (16, 40),   # sweep rows d=24 (z odd / z even)
            (5, 30), (5, 31), (28, 53), (28, 54), (29, 54),   # steady rows base/I both parities
            (47, 23), (48, 24)]   # merge boundary rows x=z-24 (z odd / z even)
    n_deep = len(deep)
    assert n_deep == 46, n_deep
    seen = set()
    for (z, x) in deep:
        assert x >= 23, ("deep row below domain", z, x)
        assert (z, x) not in seen, ("deep row duplicate", z, x)
        seen.add((z, x))
    p, b, f = sweep(((z, x, 130) for (z, x) in deep))
    pts += p
    bad += b
    print("block deep done:", n_deep, "rows, pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # bigz (d <= -9 is excluded: z=31 gives x=z+d < 23; the low-pin/diagonal
    # regime d in [-23,-9] is fully covered by the deep rows instead -- the
    # pre-flight domain assert below rejects any below-domain row)
    ds = [-8, -7, -6, -5, -4, -3, -2, -1, 0, 1,
          3, 5, 7, 9, 11, 13, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 43]
    assert len(ds) == 28, len(ds)
    for z in BIGZ_ZS:
        for d in ds:
            x = z + d
            assert x >= 23, ("bigz row below domain", z, d)
    p, b, f2 = sweep(((z, z + d, (z + d) + z + 48) for z in BIGZ_ZS for d in ds))
    pts += p
    bad += b
    print("block bigz done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # x=y=23 edge
    p, b, f3 = sweep(((z, 23, z + 130) for z in range(23, 48)))
    pts += p
    bad += b
    print("block edge done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # far d
    for z in (5, 12, 19, 26, 33, 40):
        for d in (46, 57, 68):
            assert z + d >= 23, ("far row below domain", z, d)
    p, b, f4 = sweep(((z, z + d, (z + d) + z + 48)
                      for z in (5, 12, 19, 26, 33, 40) for d in (46, 57, 68)))
    pts += p
    bad += b
    H_canonical.cache_clear()
    print("block far done: pts", pts, "bad", bad, flush=True)
    firsts = (f + f2 + f3 + f4)[:20]
    # tail raw check on sweep/steady rows d>=24 (both x parities)
    tail_pts = tail_bad = 0
    for (z, x) in [(21, 46), (20, 45), (25, 51), (24, 50), (39, 65), (42, 68)]:
        assert x - z >= 24, ("tail row below d=24", z, x)
        for R in range(x + z + 24, x + z + 37):
            v = H_canonical(R, (x, 23), z)
            exp = (x + 23) % 2
            want = 1 if exp == 1 else 0
            tail_pts += 1
            if v != want:
                tail_bad += 1
    H_canonical.cache_clear()
    # merge regression: cand23 vs K0832 single-token on out-of-box merge rows
    mg_pts = mg_bad = 0
    mg_rows = 0
    for z in (47, 54, 61, 68, 78, 91):
        for x in range(23, z - 24):
            mg_rows += 1
            assert x <= z - 24, ("merge row not a merge row", z, x)
            for R in range(1, x + z + 48):
                mg_pts += 1
                if cand23(z, x, R) != single_token_val(x + 23, R):
                    mg_bad += 1
    dt = time.time() - t0
    print("spot points:", pts, "bad:", bad, "seconds: %.1f" % dt)
    for t in firsts:
        print("BAD", t)
    print("tail raw check points:", tail_pts, "bad:", tail_bad)
    print("merge regression rows:", mg_rows, "points:", mg_pts, "bad:", mg_bad)
    print("cache:", H_canonical.cache_info())

if __name__ == '__main__':
    main()
