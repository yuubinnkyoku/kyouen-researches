#!/usr/bin/env python3
"""Out-of-box spot verification of cand16 against the raw double-recursion engine.

Scope (mirrors the published y=11..y=15 fit spot audits, adapted to the
pre-registered y=16 pin/skew/diagonal/saturation classes; every selected row
carries a MACHINE ASSERT x>=16 -- the y=14 fit's (19,13) below-domain lesson
is enforced structurally here):
  deep rows R<=130 for a 24-row pin/diag/skew/base/I/saturation/sweep/steady/
    merge-boundary selection of (z,x), all x>=16 (asserted);
  bigz z=33..42 x d in a 24-value selection, R<=x+z+34;
  x=y=16 edge z=16..41, R<=z+130;
  far d in {33,44,55} for z in {5,12,19,26,33,40}, R<=x+z+34;
  tail raw check on d>=16 rows: R in [x+z+17, x+z+30] equals (x+16) mod 2;
  merge regression vs K0832 single-token closed form on out-of-box merge rows
    z in {33,40,47,54,64,77}, x=16..z-17, R<=x+z+33.
Deterministic; prints aggregate points/bad and the tail/merge check results.
"""
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from cand16 import cand16, single_token_val

# The y=11..y=15 spot audits ran uncapped on hosts with more RAM; this host
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
        assert x >= 16, "below-domain row selected: z=%d x=%d" % (z, x)
        for R in range(1, hi + 1):
            v = H_canonical(R, (x, 16), z)
            c = cand16(z, x, R)
            pts += 1
            if v != c:
                bad += 1
                if len(first) < 20:
                    first.append((z, x, R, v, c))
    return pts, bad, first

def main():
    t0 = time.time()
    pts = bad = 0
    # deep rows R<=130 (diagonal/pin/skew/base/I/saturation/sweep/steady/merge reps)
    deep = [(33, 17), (34, 18),   # z-odd / z-even diagonal d=-16
            (27, 17), (23, 21),   # z-odd skew I rows d=-10 / d=-2 (d==2 mod 4)
            (23, 16),             # z-odd base row d=-7
            (25, 31),             # z-odd skew I row d=+6 (d==2 mod 4)
            (17, 19), (23, 17),   # z-odd pin rows d=+2 / d=-6
            (29, 17), (13, 21),   # z-odd pin rows d=-12 / d=+8
            (15, 31),             # z-odd last pin row d=+16 (=y, I[33) type)
            (18, 16), (30, 16),   # z-even pin rows d=-2 / d=-14
            (12, 18), (16, 30),   # z-even pin rows d=+6 / d=+14
            (32, 17), (14, 29),   # z-even I rows d=-15 / d=+15 (edge I rows)
            (14, 30),             # z-even base row d=+16 (saturated k=Y=16)
            (15, 32), (16, 33),   # sweep rows d=17 (z odd / z even)
            (5, 23), (28, 48),    # steady rows d=18 / d=20
            (33, 16), (34, 17)]   # merge boundary rows x=z-17
    p, b, f = sweep(((z, x, 130) for (z, x) in deep))
    pts += p; bad += b
    print("block deep done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # bigz
    ds = [-16, -15, -14, -13, -12, -11, -9, -7, -6, -5, -3, -2, -1, 0, 2, 4, 6, 8, 10, 14, 16, 17, 22, 36]
    p, b, f2 = sweep(((z, z + d, (z + d) + z + 34) for z in range(33, 43) for d in ds))
    pts += p; bad += b
    print("block bigz done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # x=y=16 edge
    p, b, f3 = sweep(((z, 16, z + 130) for z in range(16, 42)))
    pts += p; bad += b
    print("block edge done: pts", pts, "bad", bad, "cache", H_canonical.cache_info(), flush=True)
    H_canonical.cache_clear()
    # far d
    p, b, f4 = sweep(((z, z + d, (z + d) + z + 34)
                      for z in (5, 12, 19, 26, 33, 40) for d in (33, 44, 55)))
    pts += p; bad += b
    H_canonical.cache_clear()
    print("block far done: pts", pts, "bad", bad, flush=True)
    firsts = (f + f2 + f3 + f4)[:20]
    # tail raw check on sweep/steady rows d>=16
    tail_pts = tail_bad = 0
    for (z, x) in [(15, 32), (20, 37), (31, 48), (26, 43), (33, 50), (40, 56)]:
        for R in range(x + z + 17, x + z + 31):
            v = H_canonical(R, (x, 16), z)
            exp = (x + 16) % 2
            want = 1 if exp == 1 else 0
            tail_pts += 1
            if v != want:
                tail_bad += 1
    # merge regression: cand16 vs K0832 single-token on out-of-box merge rows
    mg_pts = mg_bad = 0
    for z in (33, 40, 47, 54, 64, 77):
        for x in range(16, z - 17):
            for R in range(1, x + z + 34):
                mg_pts += 1
                if cand16(z, x, R) != single_token_val(x + 16, R):
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
