#!/usr/bin/env python3
"""Probe raw engine rows for the y=18 two-token family H(R;(x,18);z). Deterministic.

Mirrors the published y=11/y=12/y=13/y=14/y=15/y=16/y=17 fit probes
(vertical-fiber-two-token-y11-..-20261120 / -y12- / -y13- / -y14- /
-y15-/ -y16- / -y17-/ K1143-fam / K1152 / K1231-fam / K1233-fam / K1235-fam /
K1237-fam / K1240-fam): same engine (canonical descending-multiset recursion),
same RLE row format.
Y=18, box z=0..30, x=18..z+35, R<=x+z+38, merge marker x<=z-19.
The R cap x+z+38 = 2y+2 continues the y=14/y=15/y=16/y=17 published convention
(declared in research/log/2026-11-23-y18-two-token-skeleton-single-owner-note.md):
it exposes the band lower end 2y+2=38, the steady T pins z+36/z+37, and the
z-odd I-band last row th=2y+1=37 in-box. NOTE: for y=18 the merge region
x<=z-19 requires z>=38, so the box z=0..30 contains ZERO merge rows -- this
is pre-declared in the note; the merge regression is carried fully by
spot_y18.py out-of-box. NOTE (pre-declared): the lowest z-odd pin row d=-14
(x=z-14>=18 needs z>=32) and the lowest z-even pin row d=-16 (z>=34) are both
geometrically unreachable in-box and are raw-verified by the spot deep rows
(33,19)/(36,20).
Declared single-owner: research/log/2026-11-23-y18-two-token-skeleton-single-owner-note.md
(commit 738ab049).
"""
import sys
import time
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
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
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
    t0 = time.time()
    with open('probe_rows.txt', 'w') as f:
        for z in range(0, Z + 1):
            for x in range(18, z + 36):
                hi = x + z + 38
                vals = []
                for R in range(1, hi + 1):
                    vals.append(H_canonical(R, (x, 18), z))
                pts += hi
                segs = []
                cur = vals[0]
                cnt = 1
                for v in vals[1:]:
                    if v == cur:
                        cnt += 1
                    else:
                        segs.append((cur, cnt))
                        cur = v
                        cnt = 1
                segs.append((cur, cnt))
                s = ' '.join(f"{v}x{c}" for v, c in segs)
                f.write(f"z={z} x={x} d={x - z} merge={'1' if x <= z - 19 else '0'} :: {s}\n")
                n += 1
    dt = time.time() - t0
    print("rows:", n)
    print("points:", pts)
    print("seconds: %.1f" % dt)
    print("cache:", H_canonical.cache_info())

if __name__ == '__main__':
    main()
