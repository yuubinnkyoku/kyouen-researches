#!/usr/bin/env python3
"""Probe raw engine rows for the y=13 two-token family H(R;(x,13);z). Deterministic.

Mirrors the published y=10/y=11/y=12 fit probes (vertical-fiber-two-token-y1{0,1,2}-parametric-allz-fit-20261120):
same engine (canonical descending multiset recursion), same box shape
(z=0..30, x=13..z+29, R<=x+z+26), same RLE row format. Y=13, merge marker x<=z-14.
Declared single-owner: research/log/2026-11-20-y13-two-token-skeleton-single-owner-note.md (2026-11-20T22:16:00Z).
"""
import sys
from functools import lru_cache

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

def main():
    Z = 30
    n = 0
    pts = 0
    with open('probe_rows.txt', 'w') as f:
        for z in range(0, Z + 1):
            for x in range(13, z + 30):
                hi = x + z + 26
                vals = []
                for R in range(1, hi + 1):
                    vals.append(H_canonical(R, (x, 13), z))
                pts += hi
                segs = []
                cur = vals[0]
                cnt = 1
                for v in vals[1:]:
                    if v == cur:
                        cnt += 1
                    else:
                        segs.append(f"{cur}x{cnt}")
                        cur = v
                        cnt = 1
                segs.append(f"{cur}x{cnt}")
                f.write(f"z={z} x={x} d={x-z} merge={1 if x<=z-14 else 0} :: " + " ".join(segs) + "\n")
                n += 1
    print(f"rows: {n} points: {pts}")

if __name__ == '__main__':
    main()
