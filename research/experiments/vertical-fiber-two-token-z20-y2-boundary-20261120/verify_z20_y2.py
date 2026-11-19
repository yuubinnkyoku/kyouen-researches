#!/usr/bin/env python3
"""Independent audit for the z=20, y=2 two-token residual-game slice.

Theorem (census-derived, anchored on published child theorems):
  * value-2 positions T(x):  x=2: {1,3}; x in (3,4): O[1,5];
    x in (5,6): O[1,7]; x in (7,8): O[1,9]; x in (9,10): O[1,11];
    x in (11,12): O[1,13]; x in (13,14): O[1,15]; x in (15,16): O[1,17];
    x=17: O[1,19];
    x=18 (x+y=z row, d=16, d+z=36 == 0 mod 4): O[1,21] contiguous
      top 21 = z+1 = 2y+(d+z)/2 - 1 (even-z x+y=z lattice top);
    x in (19,21,22): O[1,19];
    x=20 (x=z row, d=18, d+z=38 == 2 mod 4): O[1,19] u {23}
      (even-z lattice pin 23 = 2y+(d+z)/2 = 2y+z-1, on the x=z row);
    x=23 (sweep row x=z+y+1): O[1,19] u O[25,45]
      (sweep band O[2y+z+1, x+y+z], bottom = standing pin);
    x>=24: O[1,19] u {25} (even-z standing pin 25 = 2y+z+1).
  * value-1 positions P(x): x even <=18: empty; x odd <=17: I[x+3,inf);
    x=19: {21} u I[23,inf); x=20: {21}; x=21: {21} u I[23,inf);
    x=22: {21,23};
    x odd >=23: {21,23} u E[26,x+21] u I[x+23,inf);
    x even >=24: {21,23} u E[26,x+22].
Value-1 base points {21,23} = {z+1,z+3} (y=2 family). For even z the
sweep band and standing pin sit at 2y+z+1 and the lone in-band lattice
pin 2y+z-1 lies on the x=z row; for odd z both collapse to 2y+z on the
x=z+2 row (K1044/K1052).
  * tail: R >= x+23 => H = (x+2) mod 2. Height-only: R <= 22 =>
    H = single_token(x+2, 20, R) (one notch above z+1).
Children: A = H(R-1;(x-1,2);20) (x-outer induction, same-slice row x-1),
B = H(R-1;(x,1);20) = K1023 published universal parametric slice,
C = 1 xor H(R-1;(x,2);19) = 1 xor K1052 published universal slice.
At x=2 the two token-decrement moves coincide in the (2,2) child
multiset (1,2);20; the B child value is used for both.
The universal argument is x-induction with the complete A/B/C signature
band table below (static rows x=2..24; closed forms for odd x>=25 /
even x>=26 covering R=1..x+22) plus the K0832 general tail (R>=x+23)
and height-only (R<=22) reductions. The two direct mex engines and
finite grids audit transcription; they are not a substitute for the
all-x proof.
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


# ---- engine-independent closed forms (published children + candidate) ----
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


def cand(z, x, R):
    """Published K1023 y=1 parametric all-z closed form (verbatim)."""
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
        else:
            T = (R == z + 3 or (R % 2 == 1 and R <= z - 1))
        if x % 2 == 1 and x <= z - 1:
            P = False
        elif x % 2 == 0 and x <= z - 2:
            P = (R >= x + 2)
        elif x == z:
            P = (R >= z + 1)
        elif x == z + 1:
            P = (R == z + 1)
        elif x % 2 == 0:
            P = (R == z + 1 or (R % 2 == 0 and z + 4 <= R <= S - 1) or R >= S + 1)
        else:
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
        else:
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
        elif x % 2 == 1:
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S))
        else:
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S) or R >= S + 1)
    assert not (T and P), (z, x, R)
    return 2 if T else (1 if P else 0)


def z20_y1(x, r):
    return cand(20, x, r)


def z19_y2_T(x, r):
    """Published K1052 z=19, y=2 (verbatim)."""
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
    if x in (13, 14):
        return 1 <= r <= 15 and r % 2 == 1
    if x in (15, 16):
        return 1 <= r <= 17 and r % 2 == 1
    if x == 17:
        return 1 <= r <= 21 and r % 2 == 1
    if x == 21:
        return (1 <= r <= 19 and r % 2 == 1) or r == 23
    if x == 22:
        return r % 2 == 1 and (1 <= r <= 19 or 23 <= r <= 43)
    if x >= 23:
        return (1 <= r <= 19 and r % 2 == 1) or r == 23
    return 1 <= r <= 19 and r % 2 == 1


def z19_y2_P(x, r):
    if x % 2 == 0 and x <= 16:
        return False
    if x % 2 == 1 and x <= 15:
        return r >= x + 3
    if x == 17:
        return r >= 20 and r != 21
    if x == 18:
        return r == 20
    if x == 19:
        return r in (20, 22) or r >= 23
    if x == 20:
        return r in (20, 22)
    if x == 21:
        return r in (20, 22) or r >= 24
    if x == 22:
        return r in (20, 22)
    if x % 2 == 1:
        return (r in (20, 22)
                or (r % 2 == 1 and 25 <= r <= x + 21)
                or r >= x + 22)
    return r in (20, 22) or (r % 2 == 1 and 25 <= r <= x + 21)


def z19_y2(x, R):
    if R == 0:
        return 0
    if z19_y2_T(x, R):
        return 2
    return 1 if z19_y2_P(x, R) else 0


def candidate_T(x, r):
    """Derived theorem candidate: z=20, y=2."""
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
    if x in (13, 14):
        return 1 <= r <= 15 and r % 2 == 1
    if x in (15, 16):
        return 1 <= r <= 17 and r % 2 == 1
    if x == 17:
        return 1 <= r <= 19 and r % 2 == 1
    if x == 18:
        return 1 <= r <= 21 and r % 2 == 1
    if x == 20:
        return (1 <= r <= 19 and r % 2 == 1) or r == 23
    if x == 23:
        return r % 2 == 1 and (1 <= r <= 19 or 25 <= r <= 45)
    if x >= 24:
        return (1 <= r <= 19 and r % 2 == 1) or r == 25
    return 1 <= r <= 19 and r % 2 == 1


def candidate_P(x, r):
    if x % 2 == 0 and x <= 18:
        return False
    if x % 2 == 1 and x <= 17:
        return r >= x + 3
    if x == 19:
        return r == 21 or r >= 23
    if x == 20:
        return r == 21
    if x == 21:
        return r == 21 or r >= 23
    if x == 22:
        return r in (21, 23)
    if x % 2 == 1:
        return (r in (21, 23)
                or (r % 2 == 0 and 26 <= r <= x + 21)
                or r >= x + 23)
    return r in (21, 23) or (r % 2 == 0 and 26 <= r <= x + 22)


def candidate(x, R):
    assert not (candidate_T(x, R) and candidate_P(x, R)), (x, R)
    if R == 0:
        return 0
    if candidate_T(x, R):
        return 2
    return 1 if candidate_P(x, R) else 0


# Complete A/B/C signature bands: (R parity, lower, upper, signature).
# Static rows x=2..24 (machine-baked from the published child closed
# forms); closed forms for odd x>=25 / even x>=26. Each row covers
# R=1..x+22 disjointly; R>=x+23 is the K0832 general tail.
STATIC_TABLE = _STATIC_TABLE = {
                2: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "1"), (0, 6, 6, "1"), (1, 7, 7, "1"), (0, 8, 8, "1"), (1, 9, 9, "1"), (0, 10, 10, "1"), (1, 11, 11, "1"), (0, 12, 12, "1"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1")],
        3: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "03"), (1, 7, 7, "0"), (0, 8, 8, "0"), (1, 9, 9, "0"), (0, 10, 10, "0"), (1, 11, 11, "0"), (0, 12, 12, "0"), (1, 13, 13, "0"), (0, 14, 14, "0"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0")],
        4: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "1"), (0, 8, 8, "1"), (1, 9, 9, "1"), (0, 10, 10, "1"), (1, 11, 11, "1"), (0, 12, 12, "1"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1")],
        5: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "03"), (1, 9, 9, "0"), (0, 10, 10, "0"), (1, 11, 11, "0"), (0, 12, 12, "0"), (1, 13, 13, "0"), (0, 14, 14, "0"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0")],
        6: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "1"), (0, 10, 10, "1"), (1, 11, 11, "1"), (0, 12, 12, "1"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1")],
        7: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "03"), (1, 11, 11, "0"), (0, 12, 12, "0"), (1, 13, 13, "0"), (0, 14, 14, "0"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0")],
        8: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "1"), (0, 12, 12, "1"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1"), (0, 30, 30, "1")],
        9: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "03"), (1, 13, 13, "0"), (0, 14, 14, "0"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0"), (0, 30, 30, "0"), (1, 31, 31, "0")],
        10: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1"), (0, 30, 30, "1"), (1, 31, 31, "1"), (0, 32, 32, "1")],
        11: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "03"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0"), (0, 30, 30, "0"), (1, 31, 31, "0"), (0, 32, 32, "0"), (1, 33, 33, "0")],
        12: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1"), (0, 30, 30, "1"), (1, 31, 31, "1"), (0, 32, 32, "1"), (1, 33, 33, "1"), (0, 34, 34, "1")],
        13: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "03"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0"), (0, 30, 30, "0"), (1, 31, 31, "0"), (0, 32, 32, "0"), (1, 33, 33, "0"), (0, 34, 34, "0"), (1, 35, 35, "0")],
        14: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1"), (0, 30, 30, "1"), (1, 31, 31, "1"), (0, 32, 32, "1"), (1, 33, 33, "1"), (0, 34, 34, "1"), (1, 35, 35, "1"), (0, 36, 36, "1")],
        15: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "01"), (0, 18, 18, "03"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0"), (0, 30, 30, "0"), (1, 31, 31, "0"), (0, 32, 32, "0"), (1, 33, 33, "0"), (0, 34, 34, "0"), (1, 35, 35, "0"), (0, 36, 36, "0"), (1, 37, 37, "0")],
        16: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "01"), (0, 18, 18, "23"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1"), (0, 30, 30, "1"), (1, 31, 31, "1"), (0, 32, 32, "1"), (1, 33, 33, "1"), (0, 34, 34, "1"), (1, 35, 35, "1"), (0, 36, 36, "1"), (1, 37, 37, "1"), (0, 38, 38, "1")],
        17: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "01"), (0, 18, 18, "23"), (1, 19, 19, "01"), (0, 20, 20, "03"), (1, 21, 21, "0"), (0, 22, 22, "03"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0"), (0, 30, 30, "0"), (1, 31, 31, "0"), (0, 32, 32, "0"), (1, 33, 33, "0"), (0, 34, 34, "0"), (1, 35, 35, "0"), (0, 36, 36, "0"), (1, 37, 37, "0"), (0, 38, 38, "0"), (1, 39, 39, "0")],
        18: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "01"), (0, 18, 18, "23"), (1, 19, 19, "01"), (0, 20, 20, "23"), (1, 21, 21, "01"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1"), (0, 30, 30, "1"), (1, 31, 31, "1"), (0, 32, 32, "1"), (1, 33, 33, "1"), (0, 34, 34, "1"), (1, 35, 35, "1"), (0, 36, 36, "1"), (1, 37, 37, "1"), (0, 38, 38, "1"), (1, 39, 39, "1"), (0, 40, 40, "1")],
        19: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "01"), (0, 18, 18, "23"), (1, 19, 19, "01"), (0, 20, 20, "23"), (1, 21, 21, "0"), (0, 22, 22, "12"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0"), (0, 30, 30, "0"), (1, 31, 31, "0"), (0, 32, 32, "0"), (1, 33, 33, "0"), (0, 34, 34, "0"), (1, 35, 35, "0"), (0, 36, 36, "0"), (1, 37, 37, "0"), (0, 38, 38, "0"), (1, 39, 39, "0"), (0, 40, 40, "0"), (1, 41, 41, "0")],
        20: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "01"), (0, 18, 18, "23"), (1, 19, 19, "01"), (0, 20, 20, "23"), (1, 21, 21, "0"), (0, 22, 22, "1"), (1, 23, 23, "01"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1"), (0, 30, 30, "1"), (1, 31, 31, "1"), (0, 32, 32, "1"), (1, 33, 33, "1"), (0, 34, 34, "1"), (1, 35, 35, "1"), (0, 36, 36, "1"), (1, 37, 37, "1"), (0, 38, 38, "1"), (1, 39, 39, "1"), (0, 40, 40, "1"), (1, 41, 41, "1"), (0, 42, 42, "1")],
        21: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "01"), (0, 18, 18, "23"), (1, 19, 19, "01"), (0, 20, 20, "23"), (1, 21, 21, "0"), (0, 22, 22, "1"), (1, 23, 23, "0"), (0, 24, 24, "023"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0"), (0, 30, 30, "0"), (1, 31, 31, "0"), (0, 32, 32, "0"), (1, 33, 33, "0"), (0, 34, 34, "0"), (1, 35, 35, "0"), (0, 36, 36, "0"), (1, 37, 37, "0"), (0, 38, 38, "0"), (1, 39, 39, "0"), (0, 40, 40, "0"), (1, 41, 41, "0"), (0, 42, 42, "0"), (1, 43, 43, "0")],
        22: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "01"), (0, 18, 18, "23"), (1, 19, 19, "01"), (0, 20, 20, "23"), (1, 21, 21, "0"), (0, 22, 22, "1"), (1, 23, 23, "0"), (0, 24, 24, "123"), (1, 25, 25, "1"), (0, 26, 26, "123"), (1, 27, 27, "1"), (0, 28, 28, "123"), (1, 29, 29, "1"), (0, 30, 30, "123"), (1, 31, 31, "1"), (0, 32, 32, "123"), (1, 33, 33, "1"), (0, 34, 34, "123"), (1, 35, 35, "1"), (0, 36, 36, "123"), (1, 37, 37, "1"), (0, 38, 38, "123"), (1, 39, 39, "1"), (0, 40, 40, "123"), (1, 41, 41, "1"), (0, 42, 42, "123"), (1, 43, 43, "1"), (0, 44, 44, "123")],
        23: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "01"), (0, 18, 18, "23"), (1, 19, 19, "01"), (0, 20, 20, "23"), (1, 21, 21, "0"), (0, 22, 22, "1"), (1, 23, 23, "0"), (0, 24, 24, "123"), (1, 25, 25, "01"), (0, 26, 26, "0"), (1, 27, 27, "01"), (0, 28, 28, "0"), (1, 29, 29, "01"), (0, 30, 30, "0"), (1, 31, 31, "01"), (0, 32, 32, "0"), (1, 33, 33, "01"), (0, 34, 34, "0"), (1, 35, 35, "01"), (0, 36, 36, "0"), (1, 37, 37, "01"), (0, 38, 38, "0"), (1, 39, 39, "01"), (0, 40, 40, "0"), (1, 41, 41, "01"), (0, 42, 42, "0"), (1, 43, 43, "01"), (0, 44, 44, "0"), (1, 45, 45, "01")],
        24: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"), (1, 17, 17, "01"), (0, 18, 18, "23"), (1, 19, 19, "01"), (0, 20, 20, "23"), (1, 21, 21, "0"), (0, 22, 22, "1"), (1, 23, 23, "0"), (0, 24, 24, "123"), (1, 25, 25, "01"), (0, 26, 26, "02"), (1, 27, 27, "1"), (0, 28, 28, "02"), (1, 29, 29, "1"), (0, 30, 30, "02"), (1, 31, 31, "1"), (0, 32, 32, "02"), (1, 33, 33, "1"), (0, 34, 34, "02"), (1, 35, 35, "1"), (0, 36, 36, "02"), (1, 37, 37, "1"), (0, 38, 38, "02"), (1, 39, 39, "1"), (0, 40, 40, "02"), (1, 41, 41, "1"), (0, 42, 42, "02"), (1, 43, 43, "1"), (0, 44, 44, "02"), (1, 45, 45, "1"), (0, 46, 46, "02")],
    
    }

STATIC = {int(k): v for k, v in STATIC_TABLE.items()}


def closed_bands(x):
    head = [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"),
            (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"),
            (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"),
            (1, 13, 13, "01"), (0, 14, 14, "23"), (1, 15, 15, "01"), (0, 16, 16, "23"),
            (1, 17, 17, "01"), (0, 18, 18, "23"), (1, 19, 19, "01"), (0, 20, 20, "23"),
            (1, 21, 21, "0"), (0, 22, 22, "1"), (1, 23, 23, "0"),
            (0, 24, 24, "123"), (1, 25, 25, "01"), (0, 26, 26, "02")]
    if x % 2 == 1:
        return head + [(1, 27, x + 22, "1"), (0, 28, x + 21, "0")]
    return head + [(1, 27, x + 21, "1"), (0, 28, x + 22, "0")]


def bands_for(x):
    if x in STATIC:
        return STATIC[x]
    if x >= 25:
        return closed_bands(x)
    raise ValueError(x)


def band_signatures(x, R):
    return [sig for parity, lo, hi, sig in bands_for(x)
            if R % 2 == parity and lo <= R and R <= hi]


def abc_options(x, R):
    r = R - 1
    opts = set()
    if x == 2:
        # The two token-decrement moves coincide in (2,2);20 -> (1,2);20.
        opts.add(z20_y1(2, r))
    else:
        opts.add(candidate(x - 1, r))
        opts.add(z20_y1(x, r))
    opts.add(1 ^ z19_y2(x, r))
    return opts


def child_signature(x, R):
    return "".join(str(v) for v in sorted(abc_options(x, R)))


def audit_once():
    failures = []
    counts = {}

    # Two independent direct mex recurrences vs the closed form.
    direct = 0
    for x in range(2, 61):
        for R in range(0, x + 41):
            expected = candidate(x, R)
            a = H_ordered(R, (x, 2), 20)
            b = H_canonical(R, (x, 2), 20)
            direct += 2
            if a != expected or b != expected or a != b:
                failures.append(("direct", x, R, a, b, expected))
    counts["ordered_and_canonical_direct_vs_formula"] = direct

    # Published B/C child anchors, checked by both direct engines.
    anchors = 0
    for x in range(2, 61):
        for R in range(0, x + 41):
            for engine in (H_ordered, H_canonical):
                b = engine(R, (x, 1), 20)
                c = engine(R, (x, 2), 19)
                anchors += 2
                if b != z20_y1(x, R):
                    failures.append(("B-anchor", x, R, b, z20_y1(x, R)))
                if c != z19_y2(x, R):
                    failures.append(("C-anchor", x, R, c, z19_y2(x, R)))
    counts["B_C_child_anchor_direct_checks"] = anchors

    # Complete A/B/C signature-band table: exact coverage of R=1..x+21,
    # signature identity, mex, and Theorem T parity bounds.
    signature_checks = parity_checks = 0
    for x in range(2, 1501):
        for R in range(1, x + 23):
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

    # K0832 height-only reduction for R <= 22 (one notch above z+1).
    low = 0
    for x in range(2, 1001):
        for R in range(0, 23):
            low += 1
            if candidate(x, R) != single_token(x + 2, 20, R):
                failures.append(("height-only", x, R, candidate(x, R),
                                 single_token(x + 2, 20, R)))
    counts["height_only_reduction_R_le_22"] = low

    # General high-R tail: S=x+2, z=20, threshold S+z+1=x+23.
    tail = 0
    for x in range(2, 10001):
        for offset in range(4):
            R = x + 23 + offset
            tail += 1
            expected = (x + 2) % 2
            if candidate(x, R) != expected:
                failures.append(("tail", x, R, candidate(x, R), expected))
    counts["general_tail"] = tail

    # Theorem T on a wider formula grid.
    theorem_grid = 0
    for x in range(2, 1501):
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
    rng = random.Random(20261122)
    scatter = 0
    for _ in range(25000):
        x = rng.randint(2, 1500)
        R = rng.randint(0, x + 110)
        scatter += 1
        actual = 0 if R == 0 else mex(abc_options(x, R))
        expected = candidate(x, R)
        if actual != expected:
            failures.append(("scatter", x, R, actual, expected))
    counts["fixed_seed_ABC_scatter"] = scatter

    return {
        "all_pass": not failures,
        "theorem": "z=20 y=2 two-token residual Grundy slice",
        "classification": "universal proof by x-induction and complete A/B/C signature bands",
        "finite_audit_role": "independent ordered/canonical recursion, child anchors, band coverage/signature/mex, low-R reduction, tail, parity, and fixed-seed scatter checks only",
        "scope": {
            "target": "H(R;(x,2);19), x>=2, R>=0",
            "anchor_R": "0 <= R <= x+40",
            "anchor_x": [2, 60],
            "direct_R": "0 <= R <= x+40",
            "direct_x": [2, 60],
            "low_R": "0 <= R <= 22",
            "low_x": [2, 1000],
            "scatter_points": 25000,
            "scatter_seed": 20261122,
            "signature_R": "1 <= R <= x+22",
            "signature_x": [2, 1500],
            "tail_R": "x+23 <= R <= x+26",
            "tail_x": [2, 10000],
            "theorem_grid_R": "0 <= R <= x+30",
            "theorem_grid_x": [2, 1500],
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
