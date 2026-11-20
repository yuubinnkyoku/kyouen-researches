#!/usr/bin/env python3
"""Out-of-box spot verification of cand10: deeper R, larger z/d, x=y edge,
plus regressions vs the published K0832 single-token merge form and the
tail law (d>=12: for x odd, R >= x+z+11 -> value 1). Deterministic.

Checks raw double-recursion values against cand10 outside the probe box
(z>30, R>x+z+26, d>27, x edge). Expected: bad 0.
"""
import sys
from functools import lru_cache
sys.setrecursionlimit(2_000_000)

def mex(v):
    s = set(v); m = 0
    while m in s: m += 1
    return m

@lru_cache(None)
def H(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H(R - 1, X, z - 1))
    return mex(opts)

from cand10 import cand10, single_token_val

n = bad = 0
bad_rows = []

def check(z, x, rlo, rhi, label):
    global n, bad
    b = 0
    for R in range(rlo, rhi + 1):
        n += 1
        c = cand10(z, x, R)
        raw = H(R, (x, 10), z)
        if c == -99 or c != raw:
            b += 1; bad += 1
            if len(bad_rows) < 60:
                bad_rows.append((label, z, x, R, raw, c))
    return b

# deep rows across parities and d classes (incl. previously-clipped rows)
for (z, x) in [(15, 18), (20, 11), (25, 30), (4, 13), (7, 11), (29, 16), (30, 38), (13, 25)]:
    b = check(z, x, 1, 130, "deep")
    print(f"deep z={z} x={x}: bad={b}", flush=True)

# large z (31..40), sweep across near-diagonal interval rows, pins, sweep d=11, steady d>=12
for z in range(31, 41):
    for d in (-10, -8, -6, -4, -2, 0, 1, 2, 4, 5, 8, 10, 11, 13, 20, 34):
        x = z + d
        if x < 10:
            continue
        check(z, x, 1, x + z + 30, "bigz")
    print(f"bigz z={z} done, cumulative bad={bad}", flush=True)

# x = y = 10 edge (minimal x)
for z in range(10, 41):
    check(z, 10, 1, z + 60, "x=10")
    check(z, 10, max(1, z - 20), z + 130, "x=10")
print("x=10 done", flush=True)

# far d (beyond probe d<=27)
for z in (5, 12, 19, 26, 33, 40):
    for d in (30, 41, 52):
        x = z + d
        check(z, x, 1, x + z + 30, "bigd")
print("bigd done", flush=True)

# regression 1: merge region x <= z-11 must equal the published K0832 single-token form
mm = 0
for z in (13, 20, 27, 34, 41, 48, 60, 75):
    for x in range(10, z - 10):
        for R in range(1, x + z + 30):
            c = cand10(z, x, R)
            s = single_token_val(x + 10, R)
            if c != s:
                mm += 1
print("merge-regression mismatches (cand10 vs K0832 single_token):", mm, flush=True)

# regression 2: tail law on raw: d>=12 rows, R >= x+z+11 -> value (x+10)%2
tb = 0
tail_n = 0
for (z, x) in [(15, 29), (20, 35), (31, 45), (40, 52), (33, 47), (26, 40)]:
    for R in range(x + z + 11, x + z + 26):
        raw = H(R, (x, 10), z)
        want = (x + 10) % 2
        tail_n += 1
        if raw != want:
            tb += 1
            if tb <= 20:
                print("TAIL-BAD", z, x, R, raw, want, flush=True)
print("tail raw mismatches:", tb, "of", tail_n, flush=True)

print(f"TOTAL checked={n} bad={bad}")
for b in bad_rows[:60]:
    print(b)
