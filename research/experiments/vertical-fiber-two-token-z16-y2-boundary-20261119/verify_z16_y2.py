#!/usr/bin/env python3
"""Independent audit for the z=16, y=2 two-token residual-game slice.

Theorem (candidate, census-derived, anchored on published child theorems):
  * value-2 positions T(x):  x=2: {1,3}; x in (3,4): O[1,5];
    x in (5,6): O[1,7]; x in (7,8): O[1,9]; x in (9,10): O[1,11];
    x in (11,12): O[1,13]; x in (13,15,17,18): O[1,15];
    x=14 (h=z row, x=z-y, d=12, d+z=28 == 0 mod 4; even-z lattice
    family, isolated top 17 = q_odd(2y+(d+z)/2) = q_odd(18));
    x=16 (d=14, d+z=30 == 2 mod 4 lattice row): O[1,15] u {19};
    x=19 (sweep row x=z+y+1): O[1,15] u O[21,37] = O[1,z] u O[pin,x+y+z];
    x>=20: O[1,15] u {21} (even-z ladder O[1,z] u pin=2y+z+1=21).
  * value-1 positions P(x): x even <=14: empty; x in (3,5,7,9,11,13):
    I[x+3,inf); x in (15,17): {17,19} u I[20,inf); x=16: {17};
    x=18: {17,19};
    x odd >=19: {17,19} u E[22,x+19] u I[x+20,inf);
    x even >=20: {17,19} u E[22,x+18] finite.
  * tail: R >= x+19 => H = (x+2) mod 2. Height-only: R <= 17 =>
    H = single_token(x+2, 16, R).
Children: A = H(R-1;(x-1,2);16) (x-outer induction, same-slice row x-1),
B = H(R-1;(x,1);16) = K1023 published universal parametric slice,
C = 1 xor H(R-1;(x,2);15) = 1 xor K1032 published universal slice.
At x=2 the two token-decrement moves coincide in the (2,1);16 child.
The universal argument is x-induction with the complete A/B/C signature
band table below (static rows x=2..20, closed forms for x>=21 covering
R=1..x+17) plus the K0832 general tail (R>=x+19) and height-only
(R<=17) reductions. The two direct mex engines and finite grids audit
transcription; they are not a substitute for the all-x proof.
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from functools import lru_cache
from pathlib import Path

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


def q_odd(k):
    return k if k % 2 else k - 1


def single_token(x, z, R):
    """K0832 single-token closed form."""
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


# Published child K1023: y=1 parametric, all z (verbatim cand, z=16).
def cand(z, x, R):
    if R == 0:
        return 0
    if x < 1:
        return 0
    S = x + 1 + z
    if z % 2 == 0:
        if x % 2 == 0 and 2 <= x <= z - 2:
            T = (R % 2 == 1 and R <= x + 1)
        elif x % 2 == 1 and x <= z - 3:
            T = (R % 2 == 1 and R <= x)
        elif x == z - 1:
            T = (R % 2 == 1 and R <= z + 1)
        elif x in (z, z + 1):
            T = (R % 2 == 1 and R <= z - 1)
        elif x == z + 2:
            T = (R % 2 == 1 and (R <= z - 1 or z + 3 <= R <= 2 * z + 3))
        else:  # x >= z + 3
            T = (R == z + 3 or (R % 2 == 1 and R <= z - 1))
        if x % 2 == 1 and x <= z - 1:
            P = False
        elif x % 2 == 0 and x <= z - 2:
            P = (R >= x + 2)
        elif x == z:
            P = (R >= z + 1)
        elif x == z + 1:
            P = (R == z + 1)
        elif x % 2 == 0:  # >= z + 2
            P = (R == z + 1 or (R % 2 == 0 and z + 4 <= R <= S - 1) or R >= S + 1)
        else:  # x odd >= z + 3
            P = (R == z + 1 or (R % 2 == 0 and z + 4 <= R <= S))
    else:
        if x % 2 == 0 and x <= z - 1:
            T = (R % 2 == 1 and R <= x + 1)
        elif x % 2 == 1 and x <= z:
            T = (R % 2 == 1 and R <= x)
        elif x == z + 1:
            T = (R % 2 == 1 and R <= z + 2)
        elif x == z + 2:
            T = (R % 2 == 1 and R <= 2 * z + 3)
        else:  # x >= z + 3
            T = (R == z + 2 or (R % 2 == 1 and R <= z))
        if x % 2 == 1 and x <= z - 2:
            P = False
        elif x % 2 == 0 and x <= z - 1:
            P = (R >= x + 2)
        elif x == z:
            P = (R == z + 1)
        elif x == z + 1:
            P = (R == z + 1 or R >= z + 3)
        elif x == z + 2:
            P = (R == z + 1)
        elif x % 2 == 1:  # odd x >= z + 3
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S))
        else:  # even x >= z + 4
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S) or R >= S + 1)
    return 2 if T else (1 if P else 0)


def z16_y1(x, r):
    return cand(16, x, r)


# Published child K1032: z=15, y=2 (verbatim closed form).
def z15_y2_T(x, r):
    if x == 2:
        return r in (1, 3)
    if x in (3, 4):
        return r in (1, 3, 5)
    if x in (5, 6):
        return r in (1, 3, 5, 7)
    if x in (7, 8):
        return r in (1, 3, 5, 7, 9)
    if x in (9, 10):
        return r in (1, 3, 5, 7, 9, 11)
    if x in (11, 12):
        return r in (1, 3, 5, 7, 9, 11, 13)
    if x == 13:
        return 1 <= r <= 17 and r % 2 == 1
    if x in (14, 15, 16):
        return 1 <= r <= 15 and r % 2 == 1
    if x == 17:
        return (1 <= r <= 15 and r % 2 == 1) or r == 19
    if x == 18:
        return r % 2 == 1 and (1 <= r <= 15 or 19 <= r <= 35)
    return r in (1, 3, 5, 7, 9, 11, 13, 15, 19)


def z15_y2_P(x, r):
    if x % 2 == 0 and x <= 12:
        return False
    if x in (3, 5, 7, 9, 11):
        return r >= x + 3
    if x in (13, 15):
        return r == 16 or r >= 18
    if x == 14:
        return r == 16
    if x == 16:
        return r in (16, 18)
    if x == 17:
        return r in (16, 18) or r >= 20
    if x == 18:
        return r in (16, 18)
    if x % 2 == 1:
        return (r in (16, 18)
                or (r % 2 == 1 and 21 <= r <= x + 16)
                or r >= x + 18)
    return r in (16, 18) or (r % 2 == 1 and 21 <= r <= x + 17)


def z15_y2(x, R):
    if R == 0:
        return 0
    if z15_y2_T(x, R):
        return 2
    return 1 if z15_y2_P(x, R) else 0


# Candidate theorem: z=16, y=2.
def candidate_T(x, r):
    if x == 2:
        return r in (1, 3)
    if x in (3, 4):
        return 1 <= r <= 5 and r % 2 == 1
    if x in (5, 6):
        return 1 <= r <= 7 and r % 2 == 1
    if x in (7, 8):
        return 1 <= r <= 9 and r % 2 == 1
    if x in (9, 10):
        return 1 <= r <= 11 and r % 2 == 1
    if x in (11, 12):
        return 1 <= r <= 13 and r % 2 == 1
    if x == 14:
        return 1 <= r <= 17 and r % 2 == 1
    if x == 16:
        return (1 <= r <= 15 and r % 2 == 1) or r == 19
    if x == 19:
        return r % 2 == 1 and (1 <= r <= 15 or 21 <= r <= 37)
    if x >= 20:
        return r in (1, 3, 5, 7, 9, 11, 13, 15, 21)
    return 1 <= r <= 15 and r % 2 == 1


def candidate_P(x, r):
    if x % 2 == 0 and x <= 14:
        return False
    if x % 2 == 1 and x <= 13:
        return r >= x + 3
    if x in (15, 17):
        return r in (17, 19) or r >= 20
    if x == 16:
        return r == 17
    if x == 18:
        return r in (17, 19)
    if x % 2 == 1:
        return r in (17, 19) or (r % 2 == 0 and 22 <= r <= x + 19) or r >= x + 20
    return r in (17, 19) or (r % 2 == 0 and 22 <= r <= x + 18)


def candidate(x, R):
    if R == 0:
        return 0
    if candidate_T(x, R):
        return 2
    return 1 if candidate_P(x, R) else 0


# Complete A/B/C signature bands: (R parity, lower, upper, signature).
# Static rows x=2..20 (machine-baked from the published child closed
# forms); closed forms for x>=21. Each row covers R=1..x+17 disjointly;
# R>=x+19 is the K0832 general tail.
def bands_for(x):
    table = {
        2: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "1"), (0, 6, 6, "1"), (1, 7, 7, "1"), (0, 8, 8, "1"), (1, 9, 9, "1"), (0, 10, 10, "1"), (1, 11, 11, "1"), (0, 12, 12, "1"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1")],
        3: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "03"), (1, 7, 7, "0"), (0, 8, 8, "0"), (1, 9, 9, "0"), (0, 10, 10, "0"), (1, 11, 11, "0"), (0, 12, 12, "0"), (1, 13, 13, "0"), (0, 14, 14, "0"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0")],
        4: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "1"), (0, 8, 8, "1"), (1, 9, 9, "1"), (0, 10, 10, "1"), (1, 11, 11, "1"), (0, 12, 12, "1"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1")],
        5: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "03"), (1, 9, 9, "0"), (0, 10, 10, "0"), (1, 11, 11, "0"), (0, 12, 12, "0"), (1, 13, 13, "0"), (0, 14, 14, "0"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0")],
        6: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "1"), (0, 10, 10, "1"), (1, 11, 11, "1"), (0, 12, 12, "1"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1")],
        7: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "03"), (1, 11, 11, "0"), (0, 12, 12, "0"), (1, 13, 13, "0"), (0, 14, 14, "0"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0")],
        8: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "1"), (0, 12, 12, "1"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1")],
        9: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "03"), (1, 13, 13, "0"), (0, 14, 14, "0"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0")],
        10: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1")],
        11: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "03"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0")],
        12: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1")],
        13: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "03"), (1, 17, 17, "0"), (0, 18, 18, "03"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0"), (0, 30, 30, "0")],
        14: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "01"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1"), (0, 30, 30, "1"), (1, 31, 31, "1")],
        15: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "0"), (0, 18, 18, "12"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0"), (0, 30, 30, "0"), (1, 31, 31, "0"), (0, 32, 32, "0")],
        16: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "0"), (0, 18, 18, "1"), (1, 19, 19, "01"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1"), (0, 30, 30, "1"), (1, 31, 31, "1"), (0, 32, 32, "1"), (1, 33, 33, "1")],
        17: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "0"), (0, 18, 18, "1"), (1, 19, 19, "0"), (0, 20, 20, "023"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0"), (0, 30, 30, "0"), (1, 31, 31, "0"), (0, 32, 32, "0"), (1, 33, 33, "0"), (0, 34, 34, "0")],
        18: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "0"), (0, 18, 18, "1"), (1, 19, 19, "0"), (0, 20, 20, "123"), (1, 21, 21, "1"), (0, 22, 22, "123"), (1, 23, 23, "1"), (0, 24, 24, "123"), (1, 25, 25, "1"), (0, 26, 26, "123"), (1, 27, 27, "1"), (0, 28, 28, "123"), (1, 29, 29, "1"), (0, 30, 30, "123"), (1, 31, 31, "1"), (0, 32, 32, "123"), (1, 33, 33, "1"), (0, 34, 34, "123"), (1, 35, 35, "1")],
        19: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "0"), (0, 18, 18, "1"), (1, 19, 19, "0"), (0, 20, 20, "123"), (1, 21, 21, "01"), (0, 22, 22, "0"), (1, 23, 23, "01"), (0, 24, 24, "0"), (1, 25, 25, "01"), (0, 26, 26, "0"), (1, 27, 27, "01"), (0, 28, 28, "0"), (1, 29, 29, "01"), (0, 30, 30, "0"), (1, 31, 31, "01"), (0, 32, 32, "0"), (1, 33, 33, "01"), (0, 34, 34, "0"), (1, 35, 35, "01"), (0, 36, 36, "0")],
        20: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "0"), (0, 18, 18, "1"), (1, 19, 19, "0"), (0, 20, 20, "123"), (1, 21, 21, "01"), (0, 22, 22, "02"), (1, 23, 23, "1"), (0, 24, 24, "02"), (1, 25, 25, "1"), (0, 26, 26, "02"), (1, 27, 27, "1"), (0, 28, 28, "02"), (1, 29, 29, "1"), (0, 30, 30, "02"), (1, 31, 31, "1"), (0, 32, 32, "02"), (1, 33, 33, "1"), (0, 34, 34, "02"), (1, 35, 35, "1"), (0, 36, 36, "02"), (1, 37, 37, "1")],
    }
    if x in table:
        return table[x]
    if x >= 21 and x % 2 == 1:
        return [(1, 1, 15, "01"), (0, 2, 16, "23"), (1, 17, 17, "0"),
                (0, 18, 18, "1"), (1, 19, 19, "0"), (0, 20, 20, "123"),
                (1, 21, 21, "01"), (0, 22, 22, "02"),
                (1, 23, x + 16, "1"), (0, 24, x + 17, "0")]
    if x >= 22 and x % 2 == 0:
        return [(1, 1, 15, "01"), (0, 2, 16, "23"), (1, 17, 17, "0"),
                (0, 18, 18, "1"), (1, 19, 19, "0"), (0, 20, 20, "123"),
                (1, 21, 21, "01"), (0, 22, 22, "02"),
                (1, 23, x + 17, "1"), (0, 24, x + 16, "0")]
    raise ValueError(x)


def band_signatures(x, R):
    return [sig for parity, lo, hi, sig in bands_for(x)
            if R % 2 == parity and lo <= R and (hi is None or R <= hi)]


def abc_options(x, R):
    r = R - 1
    opts = set()
    if x == 2:
        # The two token-decrement moves coincide in (2,1);16.
        opts.add(z16_y1(2, r))
    else:
        opts.add(candidate(x - 1, r))
        opts.add(z16_y1(x, r))
    opts.add(1 ^ z15_y2(x, r))
    return opts


def child_signature(x, R):
    return "".join(str(v) for v in sorted(abc_options(x, R)))


def audit_once():
    failures = []
    counts = {}

    # Two independent direct mex recurrences vs the closed form.
    direct = 0
    for x in range(2, 81):
        for R in range(0, x + 41):
            expected = candidate(x, R)
            a = H_ordered(R, (x, 2), 16)
            b = H_canonical(R, (x, 2), 16)
            direct += 2
            if a != expected or b != expected or a != b:
                failures.append(("direct", x, R, a, b, expected))
    counts["ordered_and_canonical_direct_vs_formula"] = direct

    # Published B/C child anchors, checked by both direct engines.
    anchors = 0
    for x in range(2, 81):
        for R in range(0, x + 41):
            for engine in (H_ordered, H_canonical):
                b = engine(R, (x, 1), 16)
                c = engine(R, (x, 2), 15)
                anchors += 2
                if b != z16_y1(x, R):
                    failures.append(("B-anchor", x, R, b, z16_y1(x, R)))
                if c != z15_y2(x, R):
                    failures.append(("C-anchor", x, R, c, z15_y2(x, R)))
    counts["B_C_child_anchor_direct_checks"] = anchors

    # Complete A/B/C signature-band table: exact coverage of R=1..x+17,
    # signature identity, mex, and Theorem T parity bounds.
    signature_checks = parity_checks = 0
    for x in range(2, 3001):
        for R in range(1, x + 18):
            hits = band_signatures(x, R)
            if len(hits) != 1:
                failures.append(("band-coverage", x, R, hits))
                continue
            actual = child_signature(x, R)
            if hits[0] != actual:
                failures.append(("band-signature", x, R, hits[0], actual))
                continue
            value = mex({int(ch) for ch in hits[0]})
            expected = candidate(x, R)
            signature_checks += 1
            if value != expected:
                failures.append(("band-mex", x, R, hits[0], value, expected))
            values = {int(ch) for ch in hits[0]}
            if R % 2:
                if not values.issubset({0, 1}) or value > 2:
                    failures.append(("Theorem-T-odd", x, R, hits[0], value))
            elif value > 1:
                failures.append(("Theorem-T-even", x, R, hits[0], value))
            parity_checks += 1
    counts["A_B_C_signature_coverage_identity_mex_and_Theorem_T"] = signature_checks
    counts["Theorem_T_parity_bound"] = parity_checks

    # K0832 height-only reduction for R <= z+1 = 17.
    low = 0
    for x in range(2, 1001):
        for R in range(0, 18):
            low += 1
            if candidate(x, R) != single_token(x + 2, 16, R):
                failures.append(("height-only", x, R, candidate(x, R),
                                 single_token(x + 2, 16, R)))
    counts["height_only_reduction_R_le_17"] = low

    # General high-R tail: S=x+2, z=16, threshold S+z+1=x+19.
    tail = 0
    for x in range(2, 10001):
        for offset in range(4):
            R = x + 19 + offset
            tail += 1
            expected = (x + 2) % 2
            if candidate(x, R) != expected:
                failures.append(("tail", x, R, candidate(x, R), expected))
    counts["general_tail"] = tail

    # Theorem T on a wider formula grid.
    theorem_grid = 0
    for x in range(2, 3001):
        for R in range(0, x + 31):
            theorem_grid += 1
            value = candidate(x, R)
            if value not in (0, 1, 2):
                failures.append(("range", x, R, value))
            if R % 2 == 0 and value > 1:
                failures.append(("Theorem-T-even-grid", x, R, value))
            if value == 2 and R % 2 == 0:
                failures.append(("even-value-two", x, R))
    counts["Theorem_T_formula_grid"] = theorem_grid

    # Fixed-seed independent A/B/C mex scatter.
    rng = random.Random(20261119)
    scatter = 0
    for _ in range(25000):
        x = rng.randint(2, 3000)
        R = rng.randint(0, x + 110)
        scatter += 1
        actual = 0 if R == 0 else mex(abc_options(x, R))
        expected = candidate(x, R)
        if actual != expected:
            failures.append(("scatter", x, R, actual, expected))
    counts["fixed_seed_ABC_scatter"] = scatter

    return {
        "all_pass": not failures,
        "theorem": "z=16 y=2 two-token residual Grundy slice",
        "classification": "universal proof by x-induction and complete A/B/C signature bands",
        "finite_audit_role": "independent ordered/canonical recursion, child anchors, band coverage/signature/mex, low-R reduction, tail, parity, and fixed-seed scatter checks only",
        "scope": {
            "target": "H(R;(x,2);16), x>=2, R>=0",
            "anchor_R": "0 <= R <= x+40",
            "anchor_x": [2, 80],
            "direct_R": "0 <= R <= x+40",
            "direct_x": [2, 80],
            "low_R": "0 <= R <= 17",
            "low_x": [2, 1000],
            "scatter_points": 25000,
            "scatter_seed": 20261119,
            "signature_R": "1 <= R <= x+17",
            "signature_x": [2, 3000],
            "tail_R": "x+19 <= R <= x+22",
            "tail_x": [2, 10000],
            "theorem_grid_R": "0 <= R <= x+30",
            "theorem_grid_x": [2, 3000],
        },
        "counts": counts,
        "total_checks": sum(counts.values()),
        "failure_count": len(failures),
        "first_failures": failures[:20],
    }


def run():
    first = audit_once()
    second = audit_once()
    first_bytes = json.dumps(first, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":")).encode()
    second_bytes = json.dumps(second, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":")).encode()
    same = first_bytes == second_bytes
    result = {
        **first,
        "repeat_runs": 2,
        "repeat_byte_identical": same,
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sha256_without_hash_field": hashlib.sha256(first_bytes).hexdigest(),
    }
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True,
                         indent=2) + "\n"
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "audit.json").write_text(payload, encoding="utf-8")
    print(payload, end="")
    if not result["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
