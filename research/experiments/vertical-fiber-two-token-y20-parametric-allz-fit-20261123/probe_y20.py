"""Probe raw engine rows for the y=20 two-token family H(R;(x,20);z). Deterministic.

Mirrors the published y=11/y=12/y=13/y=14/y=15/y=16/y=17/y=18/y=19 fit probes
(vertical-fiber-two-token-y11-..-20261120 / -y12- / -y13- / -y14- /
-y15-/ -y16- / -y17- / -y18- / -y19- / K1143-fam / K1152 / K1231-fam /
K1233-fam / K1235-fam / K1237-fam / K1240-fam / K1242-fam / K1243-fam):
same engine (canonical descending-multiset recursion), same RLE row format.
Y=20, box z=0..30, x=20..z+39, R<=x+z+42, merge marker x<=z-21.
The R cap x+z+42 = 2y+2 continues the published convention
(declared in research/log/2026-11-23-y20-two-token-skeleton-single-owner-note.md,
commit cc20473c, published BEFORE the probe run):
it exposes the band lower end 2y+2=42, the steady T pins z+40/z+41, and the
z-odd I-band last row th=2y+1=41 in-box. NOTE: for y=20 the merge region
x<=z-21 requires z>=42, so the box z=0..30 contains ZERO merge rows -- this
is pre-declared in the note; the merge regression is carried fully by
spot_y20.py out-of-box. NOTE (pre-declared): the lowest z-odd pin rows d=-16
and d=-12 (x=21 needs z>=37 / z>=33) and the lowest z-even pin rows d=-18
and d=-14 (x=20 needs z>=38 / z>=34) are all geometrically unreachable
in-box -- the FIRST family with TWO out-of-box pin rows on EACH parity
(2+2; y=17 had one, y=18 1+1, y=19 2+1) -- and are raw-verified by the
spot deep rows (37,21) / (33,21) / (38,20) / (34,20).
Declared box geometry (machine-computed and pre-declared in the note):
1,085 rows, 105,710 points.
Declared single-owner: research/log/2026-11-23-y20-two-token-skeleton-single-owner-note.md
(commit cc20473c).
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
            for x in range(20, z + 40):
                hi = x + z + 42
                vals = []
                for R in range(1, hi + 1):
                    vals.append(H_canonical(R, (x, 20), z))
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
                f.write(f"z={z} x={x} d={x - z} merge={'1' if x <= z - 21 else '0'} :: {s}\n")
                n += 1
    dt = time.time() - t0
    print("rows:", n)
    print("points:", pts)
    print("seconds: %.1f" % dt)
    print("cache:", H_canonical.cache_info())

if __name__ == '__main__':
    main()
