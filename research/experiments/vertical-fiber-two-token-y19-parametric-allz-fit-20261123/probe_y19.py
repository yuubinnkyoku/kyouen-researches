"""Probe raw engine rows for the y=19 two-token family H(R;(x,19);z). Deterministic.

Mirrors the published y=11/y=12/y=13/y=14/y=15/y=16/y=17/y=18 fit probes
(vertical-fiber-two-token-y11-..-20261120 / -y12- / -y13- / -y14- /
-y15-/ -y16- / -y17- / -y18- / K1143-fam / K1152 / K1231-fam / K1233-fam /
K1235-fam / K1237-fam / K1240-fam / K1242-fam): same engine (canonical
descending-multiset recursion), same RLE row format.
Y=19, box z=0..30, x=19..z+37, R<=x+z+40, merge marker x<=z-20.
The R cap x+z+40 = 2y+2 continues the published convention
(declared in research/log/2026-11-23-y19-two-token-skeleton-single-owner-note.md,
commit c15b1c3f, published BEFORE the probe run):
it exposes the band lower end 2y+2=40, the steady T pins z+38/z+39, and the
z-odd I-band last row th=2y+1=39 in-box. NOTE: for y=19 the merge region
x<=z-20 requires z>=39, so the box z=0..30 contains ZERO merge rows -- this
is pre-declared in the note; the merge regression is carried fully by
spot_y19.py out-of-box. NOTE (pre-declared): the lowest z-odd pin rows d=-17
and d=-13 (x=19 needs z>=37 / z>=33) and the lowest z-even pin row d=-15
(needs z>=34) are all geometrically unreachable in-box -- the FIRST family
with TWO out-of-box pin rows on a single parity -- and are raw-verified by
the spot deep rows (37,20) / (33,20) / (34,19).
Declared box geometry (machine-computed and pre-declared in the note):
1,054 rows, 99,107 points.
Declared single-owner: research/log/2026-11-23-y19-two-token-skeleton-single-owner-note.md
(commit c15b1c3f).
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
            for x in range(19, z + 38):
                hi = x + z + 40
                vals = []
                for R in range(1, hi + 1):
                    vals.append(H_canonical(R, (x, 19), z))
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
                f.write(f"z={z} x={x} d={x - z} merge={'1' if x <= z - 20 else '0'} :: {s}\n")
                n += 1
    dt = time.time() - t0
    print("rows:", n)
    print("points:", pts)
    print("seconds: %.1f" % dt)
    print("cache:", H_canonical.cache_info())

if __name__ == '__main__':
    main()
