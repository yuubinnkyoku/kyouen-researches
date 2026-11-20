#!/usr/bin/env python3
"""Out-of-box spot verification of cand9: deeper R, larger z/d, x=y edge. 25,376 points, bad 0."""
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
            child = tuple(sorted(X[:i] + (v - 1,) + X[i+1:], reverse=True))
            opts.add(H(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i+1:], reverse=True))
            opts.add(H(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i+1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H(R - 1, X, z - 1))
    return mex(opts)

from cand9 import cand9

n = bad = 0
bad_rows = []

def check(z, x, rlo, rhi, label):
    global n, bad
    b = 0
    for R in range(rlo, rhi + 1):
        n += 1
        c = cand9(z, x, R)
        raw = H(R, (x, 9), z)
        if c == -99 or c != raw:
            b += 1; bad += 1
            if len(bad_rows) < 50: bad_rows.append((label, z, x, R, raw, c))
    return b

for (z, x) in [(15,18),(20,11),(25,30),(4,13),(7,9),(29,16),(30,38)]:
    b = check(z, x, 1, 130, "deep")
    print(f"deep z={z} x={x}: bad={b}")

for z in range(31, 41):
    for d in (-9, -7, -5, -3, -1, 0, 1, 5, 9, 10, 11, 13, 20, 34):
        x = z + d
        if x < 9: continue
        check(z, x, 1, x + z + 30, "bigz")
print("bigz done")

for z in range(9, 41):
    check(z, 9, 1, z + 60, "x=9")
    check(z, 9, max(1, z - 20), z + 130, "x=9")
print("x=9 done")

for z in (5, 12, 19, 26, 33, 40):
    for d in (30, 41, 52):
        x = z + d
        check(z, x, 1, x + z + 30, "bigd")
print("bigd done")

print(f"TOTAL checked={n} bad={bad}")
for b in bad_rows[:50]:
    print(b)
