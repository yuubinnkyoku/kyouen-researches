#!/usr/bin/env python3
"""Candidate uniform closed form for the two-token residual game
z=11, all x>=y>=6, all R>=0.  Derived from the raw census (derive.py).

T (value 2), P (value 1), tail R>=S+12 -> S mod 2, S=x+y, d=x-y.

Also: z10_uniform = transcription of the published K1002 uniform formula
(z=10, x>=y>=6) used as the C child anchor.
"""
import sys
sys.setrecursionlimit(300000)
from functools import lru_cache

# ---------------- candidate for z=11, x>=y>=6 ----------------

def v11_T(x, y, R):
    d = x - y
    S = x + y
    if R % 2 == 1 and 1 <= R <= 11:
        return True
    if d == 3 and R == 2 * y + 7:
        return True
    if d == 7 and R == 2 * y + 9:
        return True
    if d == 11 and R == 2 * y + 11:
        return True
    if d == 12 and R % 2 == 1 and 2 * y + 11 <= R <= S + 11:
        return True
    if d >= 13 and R == 2 * y + 11:
        return True
    return False

def v11_P(x, y, R):
    """value 1 membership, valid in the band region 1<=R<=S+11.
    (Tail 1 rows: beyond the caps the tail supplies value 1 anyway.)"""
    d = x - y
    S = x + y
    ce = -(-d // 4)  # ceil(d/4)
    if d % 2 == 0 and 0 <= d <= 10:
        return R % 2 == 0 and 12 <= R <= 2 * y + 4 + 2 * ce
    if d == 12:
        return R % 2 == 0 and 12 <= R <= 2 * y + 10
    if d % 2 == 0 and d >= 14:
        return ((R % 2 == 0 and 12 <= R <= 2 * y + 10)
                or (R % 2 == 1 and 2 * y + 13 <= R <= S + 11))
    if d % 2 == 1 and 1 <= d <= 11:
        return ((R % 2 == 0 and 12 <= R <= S + 11)
                or (R % 2 == 1 and 2 * y + 7 + 2 * ((d + 1) // 4) <= R <= S + 10))
    if d % 2 == 1 and d >= 13:
        return ((R % 2 == 0 and 12 <= R <= 2 * y + 10)
                or (R % 2 == 1 and 2 * y + 13 <= R <= S + 10))
    raise ValueError(d)

def v11(x, y, R):
    if R == 0:
        return 0
    S = x + y
    if R >= S + 12:
        return S % 2
    if v11_T(x, y, R):
        return 2
    if v11_P(x, y, R):
        return 1
    return 0

# ------- K1002 (z=10, x>=y>=6) uniform formula transcription -------

def z10_T(x, y, R):
    d = x - y
    S = x + y
    if R % 2 == 1 and 1 <= R <= 9:
        return True
    if d in (0, 4, 8) and R == 2 * y + 5 + d // 2:
        return True
    if d == 11 and R % 2 == 1 and 2 * y + 11 <= R <= S + 10:
        return True
    if d >= 12 and R == 2 * y + 11:
        return True
    return False

def z10_P(x, y, R):
    d = x - y
    S = x + y
    ce = -(-d // 4)
    if d % 2 == 0 and 0 <= d <= 10:
        return R % 2 == 1 and 11 <= R <= 2 * y + 3 + 2 * ce
    if d % 2 == 0 and d >= 12:
        return ((R % 2 == 1 and 11 <= R <= 2 * y + 9)
                or (R % 2 == 0 and 2 * y + 12 <= R <= S + 10))
    if d % 2 == 1 and 1 <= d <= 9:
        return ((R % 2 == 1 and 11 <= R <= S + 10)
                or (R % 2 == 0 and 2 * y + 6 + 2 * ((d + 1) // 4) <= R <= S + 9))
    if d % 2 == 1 and d >= 11:
        return ((R % 2 == 1 and 11 <= R <= 2 * y + 9)
                or (R % 2 == 0 and 2 * y + 12 <= R <= S + 9))
    raise ValueError(d)

def z10_uniform(x, y, R):
    if R == 0:
        return 0
    S = x + y
    if R >= S + 11:
        return S % 2
    if z10_T(x, y, R):
        return 2
    if z10_P(x, y, R):
        return 1
    return 0

# ---------------- direct engines (published style) ----------------

def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

@lru_cache(None)
def H_ord(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ord(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ord(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ord(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(None)
def H_can(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_can(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_can(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_can(R - 1, X, z - 1))
    return mex(opts)

def clear():
    H_ord.cache_clear()
    H_can.cache_clear()

if __name__ == "__main__":
    # broad engine check of the candidate
    bad = 0
    total = 0
    for y in [6, 7, 8, 9, 10, 11, 12]:
        for d in range(0, 16):
            x = y + d
            for R in range(0, x + y + 13):
                total += 1
                a = H_ord(R, (x, y), 11)
                if a != v11(x, y, R):
                    bad += 1
                    if bad < 20:
                        print(f"MISMATCH z11 y={y} d={d} x={x} R={R}: engine {a} cand {v11(x,y,R)}")
            clear()
    for y in [15, 20, 25]:
        for d in range(0, 10):
            x = y + d
            for R in range(0, x + y + 13):
                total += 1
                a = H_ord(R, (x, y), 11)
                if a != v11(x, y, R):
                    bad += 1
                    if bad < 30:
                        print(f"MISMATCH z11 y={y} d={d} R={R}: engine {a} cand {v11(x,y,R)}")
            clear()
    print(f"z11 candidate checks: total={total} bad={bad}")
    # C-anchor transcription check: z=10 uniform vs engine, y>=6
    bad2 = 0
    tot2 = 0
    for y in [6, 7, 8, 9, 10, 12, 15]:
        for d in range(0, 13):
            x = y + d
            for r in range(0, x + y + 12):
                tot2 += 1
                a = H_ord(r, (x, y), 10)
                if a != z10_uniform(x, y, r):
                    bad2 += 1
                    if bad2 < 20:
                        print(f"MISMATCH z10 y={y} d={d} r={r}: engine {a} cand {z10_uniform(x,y,r)}")
            clear()
    print(f"z10 K1002 transcription checks: total={tot2} bad={bad2}")
