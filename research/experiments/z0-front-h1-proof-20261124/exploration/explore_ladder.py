#!/usr/bin/env python3
"""Fast-lane exploration: z0/z1 beyond-front ladder (R = 2m+k, k>=1)
for mixed / allm shapes. Uses the published engine block verbatim."""
import sys
from functools import lru_cache
sys.setrecursionlimit(100000)

# engine (verbatim, same as engine_block.py)
def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

@lru_cache(maxsize=6_000_000)
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

def shapes(m, tmax, amax):
    """all multisets with min=m, tokens in [m, tmax], arity<=amax, |X|>=2"""
    out = []
    def rec(cur, lo):
        if len(cur) >= 2:
            out.append(tuple(sorted(cur)))
        if len(cur) >= amax:
            return
        for t in range(max(lo, m), tmax + 1):
            rec(cur + [t], t)
    rec([], m)
    return out

def allm_shapes(m, amax):
    return [tuple([m] * a) for a in range(2, amax + 1)]

def run(m, kmax, z, tmax, amax):
    rows = []
    for k in range(1, kmax + 1):
        R = 2 * m + k
        tbl = {}
        for X in shapes(m, tmax, amax):
            tbl[X] = H(R, X, z)
        rows.append(tbl)
    return rows

if __name__ == "__main__":
    for m in [2, 3, 4]:
        for z in [0, 1]:
            print(f"=== m={m} z={z} : H(2m+k; X; z), mixed shapes, tmax=m+5, amax=4, k=1..8 ===")
            rows = run(m, 8, z, m + 5, 4)
            hdr = ["shape".ljust(24)] + [f"k={k}".rjust(4) for k in range(1, 9)]
            print("".join(hdr))
            for X in sorted(rows[0].keys(), key=lambda t: (sum(t), t)):
                vals = "".join(f"{rows[k-1][X]}".rjust(4) for k in range(1, 9))
                print(f"{str(X).ljust(24)}{vals}")
            print()
