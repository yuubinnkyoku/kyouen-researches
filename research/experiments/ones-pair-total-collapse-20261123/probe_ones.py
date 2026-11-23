#!/usr/bin/env python3
"""Pre-declaration exploration grid test for the {1,1} total-collapse claim.
Engines + closed form transcribed verbatim from published K1264 verifier
(verify_min_token_staircase.py, SHA-256 108fdd65...)."""
import sys
from functools import lru_cache
sys.setrecursionlimit(1_000_000)

def mex(values):
    values = set(values); m = 0
    while m in values: m += 1
    return m

@lru_cache(maxsize=6_000_000)
def H_ordered(R, X, z):
    if R == 0: return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(maxsize=6_000_000)
def H_canonical(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0: return 0
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
        while i + 1 < len(X) and X[i + 1] == v: i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def q_odd(k):
    return k if k % 2 else k - 1

def single_token(x, z, R):
    if R == 0 or x <= 0: return 0
    if z == 0: return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1: return 2
        if R % 2 == 0 and R <= x - 1: return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m: return 2 if R % 2 else 0
        if m < R < x + z: return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m: return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))

def vC(x, z, R): return H_canonical(R, (x,), z)
def vO(x, z, R): return H_ordered(R, (x,), z)

# Lemma V1 characteristic function of v(1,z,n)
def char1(z, n):
    if n == 0: return 0
    if n == 1: return 2 if z >= 1 else 1
    return 1

bad = pts = 0
# Lemma V1 grid: z 0..40, n 0..min(z+14, 54)
for z in range(0, 41):
    for n in range(0, min(z + 15, 55)):
        c = char1(z, n)
        pts += 3
        if vC(1, z, n) != c: bad += 1
        if vO(1, z, n) != c: bad += 1
        if single_token(1, z, n) != c: bad += 1
print(f"LemmaV1 grid: pts={pts} bad={bad}")

# {1,1} theorem grid: z 0..24, all R 0..min(z+14, 38)
bad2 = pts2 = 0
first_break = None
for z in range(0, 25):
    for R in range(0, min(z + 15, 39)):
        s = single_token(2, z, R)
        go = H_ordered(R, (1, 1), z)
        gc = H_canonical(R, (1, 1), z)
        pts2 += 3
        if go != s or gc != s or go != gc:
            bad2 += 1
            if first_break is None: first_break = (z, R, go, gc, s)
print(f"{chr(123)}1,1{chr(125)} theorem grid: pts={pts2} bad={bad2} first_break={first_break}")

# {1}^t census t=1..6: first break vs single_token(t,z,R), z<=12, R<=z+8
for t in range(1, 7):
    fb = None; b = 0; cnt = 0
    for z in range(0, 13):
        for R in range(0, z + 9):
            s = single_token(t, z, R)
            gc = H_canonical(R, (1,) * t, z)
            cnt += 1
            if gc != s:
                b += 1
                if fb is None: fb = (z, R, gc, s)
    print(f"{{1}}^{t}: pts={cnt} breaks={b} first={fb}")
