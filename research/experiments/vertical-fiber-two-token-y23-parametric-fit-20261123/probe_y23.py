"""Probe raw engine rows for the y=23 two-token family H(R;(x,23);z). Deterministic.

Mirrors the published y=11..y=22 fit probes (same canonical
descending-multiset engine, same RLE row format).
Y=23, box z=0..30, x=23..z+45, R<=x+z+48, merge marker x<=z-24.
The R cap x+z+48 = 2y+2 continues the published convention
(declared in research/log/2026-11-23-y23-two-token-skeleton-single-owner-note.md,
published BEFORE this probe run):
it exposes the band lower end 2y+2=48, the steady T pins z+46/z+47, and the
z-odd I-band last row th=2y+1=47 in-box. NOTE: for y=23 the merge region
x<=z-24 requires z>=47, so the box z=0..30 contains ZERO merge rows -- the
9th consecutive family with this property; the merge regression is carried
fully by spot_y23.py out-of-box. NOTE (pre-declared): the lowest z-odd pin
rows d=-21, d=-17, d=-13 and d=-9 (need z>=45 / z>=41 / z>=37 / z>=33) and
the lowest z-even pin rows d=-19, d=-15 and d=-11 (need z>=42 / z>=38 /
z>=34) are all geometrically unreachable in-box -- the FIRST family with
FOUR out-of-box pin rows on EACH parity (7 total, series-first by either
counting) -- and are raw-verified by the spot deep rows
(45,24) / (41,24) / (37,24) / (33,24) / (42,23) / (38,23) / (34,23).
Declared box geometry (machine-computed and pre-declared in the note):
1,178 rows, 126,821 points.
Declared single-owner: research/log/2026-11-23-y23-two-token-skeleton-single-owner-note.md
(publish-then-execute; the note commit sha is recorded in the fit log).
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
            for x in range(23, z + 46):
                hi = x + z + 48
                vals = []
                for R in range(1, hi + 1):
                    vals.append(H_canonical(R, (x, 23), z))
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
                f.write(f"z={z} x={x} d={x - z} merge={'1' if x <= z - 24 else '0'} :: {s}\n")
                n += 1
    dt = time.time() - t0
    print("rows:", n)
    print("points:", pts)
    print("seconds: %.1f" % dt)
    print("cache:", H_canonical.cache_info())

if __name__ == '__main__':
    main()
