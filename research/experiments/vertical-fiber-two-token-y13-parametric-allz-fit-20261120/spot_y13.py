#!/usr/bin/env python3
"""Out-of-box spot verification for cand13 (y=13 two-token family fit).

The probe box is z=0..30, x=13..z+29, R<=x+z+26. This script re-checks the
closed form on rows OUTSIDE that box, by category:
  1. ext-z deep:     z=31..40, x=z-20 (deep zone d<=-12 beyond fitted z).
  2. ext-z trans:    z=31..40, x=z-11 (d=-11 transition layer at new z).
  3. ext-z generic: z=31..40, x=z-5 and x=z+3 (generic A/B/C/D rows).
  4. large d:       z=3,12,13,14,15,16,30 with x up to z+60 (d outside box).
  5. ext-R:         chosen z,x with R extended past the box cap.
  6. deep-merge regression: cand13 deep formula equals single_token(x+11)
     as a function (identity check over a grid, no engine needed).

Engine: same canonical descending-multiset recursion as probe_y13.py.
Prints per-category mismatch counts; expected all zero. A nonzero category
means the law does not extend beyond the fitted box in that direction
(record it, do not silently widen the claim).
"""
import sys
from functools import lru_cache
from cand13 import cand13, single_token_val

sys.setrecursionlimit(2_000_000)

def mex(values):
    s = set(values)
    m = 0
    while m in s:
        m += 1
    return m

@lru_cache(None)
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
            child = tuple(sorted(X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def check_row(z, x, rhi, cat, agg):
    bad = 0
    firsts = []
    for R in range(1, rhi + 1):
        exp = H_canonical(R, (x, 13), z)
        got = cand13(z, x, R)
        if exp != got:
            bad += 1
            if len(firsts) < 5:
                firsts.append((z, x, R, exp, got))
    agg[cat] = agg.get(cat, [0, 0])
    agg[cat][0] += bad
    agg[cat][1] += rhi
    if bad:
        print(f"  [{cat}] z={z} x={x} mismatches={bad} first={firsts[0]}")

def main():
    agg = {}
    RCAP = 120
    # 1-3: extended z rows
    for z in range(31, 41):
        for dx, cat in ((-20, "ext-z-deep"), (-11, "ext-z-d-11"),
                        (-5, "ext-z-gen"), (3, "ext-z-gen")):
            x = z + dx
            if x < 13:
                continue
            check_row(z, x, min(x + z + 26, RCAP), cat, agg)
    # 4/5: large d and extended R inside fitted z, beyond fitted x-range
    for z in (3, 12, 13, 14, 15, 16, 20, 30):
        for x in (z + 35, z + 60) if z <= 16 else (z + 60,):
            check_row(z, x, min(x + z + 26, RCAP), "large-d-ext-R", agg)
    # deep rows at fitted z with very deep x (past z-29 floor is impossible: x>=13)
    for z in (25, 30):
        check_row(z, 13, 13 + z + 26, "edge-x13-deep", agg)
    # 6: deep-merge regression grid (identity vs single_token, no engine)
    bad6 = n6 = 0
    for z in range(0, 41):
        for x in range(13, z - 11):        # deep zone only: d = x-z <= -12
            for R in range(1, x + z + 26):
                n6 += 1
                if cand13(z, x, R) != single_token_val(x + 11, R):
                    bad6 += 1
    agg["deep-merge-regression"] = [bad6, n6]
    print("category summaries:")
    for k, (b, n) in sorted(agg.items()):
        print(f"  {k}: mismatches={b} (points~{n})")
    total = sum(v[0] for v in agg.values())
    print(f"TOTAL SPOT MISMATCHES: {total}")

if __name__ == '__main__':
    main()
