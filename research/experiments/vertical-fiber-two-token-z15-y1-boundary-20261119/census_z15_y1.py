#!/usr/bin/env python3
"""Census for the z=15, y=1 two-token residual-game slice.

H(R;(x,1);15) is computed with two independent direct recursions
(order-preserving and descending-canonical) plus child anchors:
  A = H(R-1;(x-1,1);15)   (x >= 2; both removal moves coincide at x=1)
  B = single_token(x, 16, R-1)   (K0832 universal closed form)
  C = 1 ^ K1018(R-1; x)   (published z=14, y=1 slice)
Outputs T/P row tables and A/B/C signature bands per row.
"""
from __future__ import annotations
import sys
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

@lru_cache(None)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(None)
def H_canonical(R, X, z):
    X = tuple(sorted(X))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            opts.add(H_canonical(R - 1, tuple(sorted(X[:i] + (v - 1,) + X[i + 1:])), z))
        else:
            opts.add(H_canonical(R - 1, X[:i] + X[i + 1:], z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def q_odd(k):
    return k if k % 2 else k - 1

def single_token(x, z, R):
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))

# K1018, z=14, y=1 (published; formulas copied verbatim from verify_z14_y1.py).
def T14(x, r):
    if x == 1: return r == 1
    if x == 13: return 1 <= r <= 15 and r % 2 == 1
    if x <= 12:
        top = x + 1 if x % 2 == 0 else x
        return 1 <= r <= top and r % 2 == 1
    if x == 14 or x == 15: return 1 <= r <= 13 and r % 2 == 1
    if x == 16:
        return (1 <= r <= 13 or 17 <= r <= 31) and r % 2 == 1
    return r in (1,3,5,7,9,11,13,17)
def P14(x, r):
    if x % 2 == 1:
        if x <= 13: return False
        if x == 15: return r == 15
        # x odd, >= 17
        return r == 15 or (r % 2 == 0 and 18 <= r <= x + 15)
    if x <= 12: return r >= x + 2
    if x == 14: return r >= 15
    # x even, >= 16
    return r == 15 or (r % 2 == 0 and 18 <= r <= x + 14) or r >= x + 16
def h14_y1(x, r):
    if r == 0: return 0
    if T14(x, r): return 2
    if P14(x, r): return 1
    return 0

def runs(flag, Rmax):
    out = []
    start = None
    for r in range(Rmax + 1):
        if flag(r) and start is None:
            start = r
        elif not flag(r) and start is not None:
            out.append((start, r - 1))
            start = None
    if start is not None:
        out.append((start, Rmax))
    return out

def main():
    XMAX = 26
    PAD = 48
    # child-anchor cross-check
    bad = 0
    for x in range(1, 41):
        for r in range(0, x + PAD):
            if H_ordered(r, (x, 1), 14) != h14_y1(x, r):
                bad += 1
    print("K1018 child anchor mismatches:", bad)
    for x in range(1, 61):
        for r in range(0, 90):
            if H_ordered(r, (x,), 16) != single_token(x, 16, r):
                bad += 1
    print("single-token z=16 anchor mismatches:", bad)

    print("\n=== T/P row tables (z=15, y=1) ===")
    for x in range(1, XMAX + 1):
        Rmax = x + PAD
        T = [R for R in range(Rmax + 1) if H_ordered(R, (x, 1), 15) == 2]
        P = [R for R in range(Rmax + 1) if H_ordered(R, (x, 1), 15) == 1]
        # canonical cross-check
        for R in range(Rmax + 1):
            assert H_canonical(R, (x, 1), 15) == H_ordered(R, (x, 1), 15), (x, R)
        T_run = runs(lambda r: H_ordered(r, (x, 1), 15) == 2, Rmax)
        P_run = runs(lambda r: H_ordered(r, (x, 1), 15) == 1, Rmax)
        print(f"x={x:2d} T2={T_run}")
        print(f"      P1={P_run}")

    print("\n=== A/B/C signature bands (z=15, y=1) ===")
    for x in range(1, XMAX + 1):
        Rmax = x + PAD
        bands = []
        prev = None
        for R in range(1, Rmax + 1):
            r = R - 1
            opts = set()
            if x >= 2:
                opts.add(H_ordered(r, (x - 1, 1), 15))
            opts.add(single_token(x, 16, r))
            opts.add(1 ^ h14_y1(x, r))
            sig = "".join(map(str, sorted(opts)))
            if sig != prev:
                bands.append((R, R, sig))
                prev = sig
            else:
                bands[-1] = (bands[-1][0], R, sig)
        desc = ", ".join(f"{a}-{b}:{s}" if a != b else f"{a}:{s}" for a, b, s in bands)
        print(f"x={x:2d} {desc}")

    # tail probe
    print("\n=== tail probe ===")
    for x in range(1, 22):
        for off in range(4):
            R = x + 17 + off
            print(f"x={x:2d} R={R:3d} H={H_ordered(R, (x,1), 15)} tail=({x+1})%2={{{(x+1)%2}}}", end="  ")
        print()

if __name__ == "__main__":
    main()
