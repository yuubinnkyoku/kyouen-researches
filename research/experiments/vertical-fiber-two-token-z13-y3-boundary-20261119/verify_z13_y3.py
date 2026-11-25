#!/usr/bin/env python3
"""Independent verifier for the z=13, y=3 two-token residual Grundy slice.

Universal classification of H(R;(x,3);13) for all x>=3, R>=0 (values 0/1/2).
Children: A = same slice x-1 row (outer x-induction), B = K1025 (z=13,y=2),
C = 1 xor K1021 (z=12,y=3). At x=3 the two token-decrement moves coincide in
the multiset (2,3);13 handled by the published K1025 row x'=3.

Checks (all finite audits only; universality rests on the x-induction and the
complete A/B/C signature-band table):
  1. two independent direct mex recurrences vs the closed form,
  2. published B/C child anchors against both recurrences,
  3. complete signature-band coverage / identity / mex / Theorem T parity,
  4. K0832 height-only reduction for R<=z+1=14,
  5. general tail R>=x+17 with value (x+3) mod 2,
  6. Theorem T formula grid,
  7. fixed-seed A/B/C mex scatter.

Deterministic: two in-process runs must be byte-identical; writes
output/audit.json. Standard library only.
"""
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


# Published child K1025: z=13, y=2 (verbatim closed form).
def z13_y2_T(x, r):
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
    if x == 11:
        return r in (1, 3, 5, 7, 9, 11, 13, 15)
    if x in (12, 13, 14):
        return r in (1, 3, 5, 7, 9, 11, 13)
    if x == 15:
        return r in (1, 3, 5, 7, 9, 11, 13, 17)
    if x == 16:
        return (r in (1, 3, 5, 7, 9, 11, 13)
                or (17 <= r <= 31 and r % 2 == 1))
    return r in (1, 3, 5, 7, 9, 11, 13, 17)


def z13_y2_P(x, r):
    if x % 2 == 0 and x <= 10:
        return False
    if x in (3, 5, 7, 9):
        return r >= x + 3
    if x in (11, 13):
        return r == 14 or r >= 16
    if x == 12:
        return r == 14
    if x == 14:
        return r in (14, 16)
    if x == 15:
        return r in (14, 16) or r >= 18
    if x == 16:
        return r in (14, 16)
    if x % 2 == 1:
        return (r in (14, 16)
                or (r % 2 == 1 and 19 <= r <= x + 15)
                or r >= x + 16)
    return r in (14, 16) or (r % 2 == 1 and 19 <= r <= x + 15)


def z13_y2(x, R):
    if R == 0:
        return 0
    if z13_y2_T(x, R):
        return 2
    return 1 if z13_y2_P(x, R) else 0


# Published child K1021: z=12, y=3 (verbatim closed form).
def z12_y3_T(x, r):
    if x == 3:
        return r in (1, 3, 5)
    if x in (4, 5):
        return r in (1, 3, 5, 7)
    if x in (6, 7):
        return r in (1, 3, 5, 7, 9)
    if x == 8:
        return r in (1, 3, 5, 7, 9, 11)
    if x == 9:
        return r in (1, 3, 5, 7, 9, 11, 13, 15)
    if x in (10, 11, 12, 14, 15):
        return r in (1, 3, 5, 7, 9, 11)
    if x == 13:
        return r in (1, 3, 5, 7, 9, 11) or r == 17
    if x == 16:
        return (r in (1, 3, 5, 7, 9, 11)
                or (19 <= r <= 31 and r % 2 == 1))
    return r in (1, 3, 5, 7, 9, 11, 19)


def z12_y3_P(x, r):
    if x % 2 == 1 and x <= 9:
        return False
    if x == 4:
        return r >= 8
    if x == 6:
        return r >= 10
    if x == 8:
        return r >= 12
    if x == 10:
        return r in (13, 15) or r >= 16
    if x == 11:
        return r in (13, 15)
    if x == 12:
        return r in (13, 15) or r >= 17
    if x == 13:
        return r in (13, 15)
    if x == 14:
        return r in (13, 15) or r >= 17
    if x == 15:
        return r in (13, 15, 17)
    if x == 16:
        return (r in (13, 15, 17)
                or (r % 2 == 0 and 20 <= r <= 32)
                or r >= 33)
    if x % 2 == 1:
        return r in (13, 15, 17) or (r % 2 == 0 and 20 <= r <= x + 15)
    return (r in (13, 15, 17)
            or (r % 2 == 0 and 20 <= r <= x + 16)
            or r >= x + 17)


def z12_y3(x, R):
    if R == 0:
        return 0
    if z12_y3_T(x, R):
        return 2
    return 1 if z12_y3_P(x, R) else 0


# Candidate closed form for this slice (z=13, y=3).
def candidate_T(x, r):
    if x == 3:
        return r in (1, 3, 5)
    if x in (4, 5):
        return r in (1, 3, 5, 7)
    if x in (6, 7):
        return r in (1, 3, 5, 7, 9)
    if x in (8, 9):
        return r in (1, 3, 5, 7, 9, 11)
    if x == 10:
        return r in (1, 3, 5, 7, 9, 11, 13, 15)
    if x == 12:
        return r in (1, 3, 5, 7, 9, 11, 13) or r == 17
    if x in (11, 13, 14, 15):
        return r in (1, 3, 5, 7, 9, 11, 13)
    if x == 16:
        return r in (1, 3, 5, 7, 9, 11, 13) or r == 19
    if x == 17:
        return (r in (1, 3, 5, 7, 9, 11, 13)
                or (19 <= r <= 33 and r % 2 == 1))
    return r in (1, 3, 5, 7, 9, 11, 13) or r == 19


def candidate_P(x, r):
    if x % 2 == 1:
        if x <= 9:
            return False
        if x in (11, 13):
            return r in (14, 16)
        if x in (15, 17):
            return r in (14, 16, 18)
        return r in (14, 16, 18) or (r % 2 == 1 and 21 <= r <= x + 16)
    if x <= 8:
        return r >= x + 4
    if x == 10:
        return r == 14 or r >= 16
    if x in (12, 14):
        return r in (14, 16) or r >= 18
    if x == 16:
        return r in (14, 16, 18) or r >= 20
    return (r in (14, 16, 18)
            or (r % 2 == 1 and 21 <= r <= x + 15)
            or r >= x + 17)


def candidate(x, R):
    if R == 0:
        return 0
    if candidate_T(x, R):
        return 2
    return 1 if candidate_P(x, R) else 0


def bands_for(x):
    table = {
        3: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "1"), (0, 8, 8, "1"), (1, 9, 9, "1"), (0, 10, 10, "1"), (1, 11, 11, "1"), (0, 12, 12, "1"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1")],
        4: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "03"), (1, 9, 9, "0"), (0, 10, 10, "0"), (1, 11, 11, "0"), (0, 12, 12, "0"), (1, 13, 13, "0"), (0, 14, 14, "0"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0")],
        5: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "1"), (0, 10, 10, "1"), (1, 11, 11, "1"), (0, 12, 12, "1"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1")],
        6: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "03"), (1, 11, 11, "0"), (0, 12, 12, "0"), (1, 13, 13, "0"), (0, 14, 14, "0"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0")],
        7: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "1"), (0, 12, 12, "1"), (1, 13, 13, "1"), (0, 14, 14, "1"), (1, 15, 15, "1"), (0, 16, 16, "1"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1")],
        8: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "03"), (1, 13, 13, "0"), (0, 14, 14, "0"), (1, 15, 15, "0"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0")],
        9: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "1"), (0, 14, 14, "13"), (1, 15, 15, "1"), (0, 16, 16, "13"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1")],
        10: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "0"), (1, 15, 15, "01"), (0, 16, 16, "0"), (1, 17, 17, "0"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0")],
        11: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "02"), (1, 15, 15, "1"), (0, 16, 16, "02"), (1, 17, 17, "1"), (0, 18, 18, "1"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1")],
        12: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "02"), (1, 15, 15, "1"), (0, 16, 16, "0"), (1, 17, 17, "01"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0")],
        13: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "02"), (1, 15, 15, "1"), (0, 16, 16, "0"), (1, 17, 17, "1"), (0, 18, 18, "123"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1")],
        14: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "02"), (1, 15, 15, "1"), (0, 16, 16, "0"), (1, 17, 17, "1"), (0, 18, 18, "0"), (1, 19, 19, "0"), (0, 20, 20, "0"), (1, 21, 21, "0"), (0, 22, 22, "0"), (1, 23, 23, "0"), (0, 24, 24, "0"), (1, 25, 25, "0"), (0, 26, 26, "0"), (1, 27, 27, "0"), (0, 28, 28, "0"), (1, 29, 29, "0"), (0, 30, 30, "0")],
        15: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "02"), (1, 15, 15, "1"), (0, 16, 16, "0"), (1, 17, 17, "1"), (0, 18, 18, "02"), (1, 19, 19, "1"), (0, 20, 20, "1"), (1, 21, 21, "1"), (0, 22, 22, "1"), (1, 23, 23, "1"), (0, 24, 24, "1"), (1, 25, 25, "1"), (0, 26, 26, "1"), (1, 27, 27, "1"), (0, 28, 28, "1"), (1, 29, 29, "1"), (0, 30, 30, "1"), (1, 31, 31, "1")],
        16: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "02"), (1, 15, 15, "1"), (0, 16, 16, "0"), (1, 17, 17, "1"), (0, 18, 18, "02"), (1, 19, 19, "01"), (0, 20, 20, "023"), (1, 21, 21, "0"), (0, 22, 22, "023"), (1, 23, 23, "0"), (0, 24, 24, "023"), (1, 25, 25, "0"), (0, 26, 26, "023"), (1, 27, 27, "0"), (0, 28, 28, "023"), (1, 29, 29, "0"), (0, 30, 30, "023"), (1, 31, 31, "0"), (0, 32, 32, "023")],
        17: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "02"), (1, 15, 15, "1"), (0, 16, 16, "0"), (1, 17, 17, "1"), (0, 18, 18, "02"), (1, 19, 19, "01"), (0, 20, 20, "123"), (1, 21, 21, "01"), (0, 22, 22, "1"), (1, 23, 23, "01"), (0, 24, 24, "1"), (1, 25, 25, "01"), (0, 26, 26, "1"), (1, 27, 27, "01"), (0, 28, 28, "1"), (1, 29, 29, "01"), (0, 30, 30, "1"), (1, 31, 31, "01"), (0, 32, 32, "1"), (1, 33, 33, "01")],
        18: [(1, 1, 1, "01"), (0, 2, 2, "23"), (1, 3, 3, "01"), (0, 4, 4, "23"), (1, 5, 5, "01"), (0, 6, 6, "23"), (1, 7, 7, "01"), (0, 8, 8, "23"), (1, 9, 9, "01"), (0, 10, 10, "23"), (1, 11, 11, "01"), (0, 12, 12, "23"), (1, 13, 13, "01"), (0, 14, 14, "02"), (1, 15, 15, "1"), (0, 16, 16, "0"), (1, 17, 17, "1"), (0, 18, 18, "02"), (1, 19, 19, "01"), (0, 20, 20, "123"), (1, 21, 21, "0"), (0, 22, 22, "12"), (1, 23, 23, "0"), (0, 24, 24, "12"), (1, 25, 25, "0"), (0, 26, 26, "12"), (1, 27, 27, "0"), (0, 28, 28, "12"), (1, 29, 29, "0"), (0, 30, 30, "12"), (1, 31, 31, "0"), (0, 32, 32, "12"), (1, 33, 33, "0"), (0, 34, 34, "12")],
    }
    if x in table:
        return table[x]
    if x >= 19 and x % 2 == 1:
        return [(1, 1, 13, "01"), (1, 15, 15, "1"), (1, 17, 17, "1"),
                (1, 19, 19, "01"), (1, 21, x + 16, "0"),
                (0, 2, 12, "23"), (0, 14, 14, "02"), (0, 16, 16, "0"),
                (0, 18, 18, "02"), (0, 20, 20, "123"), (0, 22, x + 15, "1")]
    if x >= 20 and x % 2 == 0:
        return [(1, 1, 13, "01"), (1, 15, 15, "1"), (1, 17, 17, "1"),
                (1, 19, 19, "01"), (1, 21, x + 15, "0"),
                (0, 2, 12, "23"), (0, 14, 14, "02"), (0, 16, 16, "0"),
                (0, 18, 18, "02"), (0, 20, 20, "123"), (0, 22, x + 16, "1")]
    raise ValueError(x)


def band_signatures(x, R):
    return [sig for parity, lo, hi, sig in bands_for(x)
            if R % 2 == parity and lo <= R and (hi is None or R <= hi)]


def abc_options(x, R):
    r = R - 1
    opts = set()
    if x == 3:
        # The two token-decrement moves coincide in the multiset (2,3);13.
        opts.add(z13_y2(3, r))
    else:
        opts.add(candidate(x - 1, r))
        opts.add(z13_y2(x, r))
    opts.add(1 ^ z12_y3(x, r))
    return opts


def child_signature(x, R):
    return "".join(str(v) for v in sorted(abc_options(x, R)))


def audit_once():
    failures = []
    counts = {}

    # Two independent direct mex recurrences vs the closed form.
    direct = 0
    for x in range(3, 81):
        for R in range(0, x + 41):
            expected = candidate(x, R)
            a = H_ordered(R, (x, 3), 13)
            b = H_canonical(R, (x, 3), 13)
            direct += 2
            if a != expected or b != expected or a != b:
                failures.append(("direct", x, R, a, b, expected))
    counts["ordered_and_canonical_direct_vs_formula"] = direct

    # Published B/C child anchors, checked by both direct engines.
    anchors = 0
    for x in range(3, 81):
        for R in range(0, x + 41):
            for engine in (H_ordered, H_canonical):
                b = engine(R, (x, 2), 13)
                c = engine(R, (x, 3), 12)
                anchors += 2
                if b != z13_y2(x, R):
                    failures.append(("B-anchor", x, R, b, z13_y2(x, R)))
                if c != z12_y3(x, R):
                    failures.append(("C-anchor", x, R, c, z12_y3(x, R)))
    counts["B_C_child_anchor_direct_checks"] = anchors

    # Complete A/B/C signature-band table: exact coverage of R=1..x+16,
    # signature identity, mex, and Theorem T parity bounds.
    signature_checks = parity_checks = 0
    for x in range(3, 3001):
        for R in range(1, x + 17):
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

    # K0832 height-only reduction for R <= z+1 = 14.
    low = 0
    for x in range(3, 1001):
        for R in range(0, 15):
            low += 1
            if candidate(x, R) != single_token(x + 3, 13, R):
                failures.append(("height-only", x, R, candidate(x, R),
                                 single_token(x + 3, 13, R)))
    counts["height_only_reduction_R_le_14"] = low

    # General high-R tail: S=x+3, z=13, threshold S+z+1=x+17.
    tail = 0
    for x in range(3, 10001):
        for offset in range(4):
            R = x + 17 + offset
            tail += 1
            expected = (x + 3) % 2
            if candidate(x, R) != expected:
                failures.append(("tail", x, R, candidate(x, R), expected))
    counts["general_tail"] = tail

    # Theorem T on a wider formula grid.
    theorem_grid = 0
    for x in range(3, 3001):
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
    rng = random.Random(20261121)
    scatter = 0
    for _ in range(25000):
        x = rng.randint(3, 3000)
        R = rng.randint(0, x + 110)
        scatter += 1
        actual = 0 if R == 0 else mex(abc_options(x, R))
        expected = candidate(x, R)
        if actual != expected:
            failures.append(("scatter", x, R, actual, expected))
    counts["fixed_seed_ABC_scatter"] = scatter

    return {
        "all_pass": not failures,
        "theorem": "z=13 y=3 two-token residual Grundy slice",
        "classification": "universal proof by x-induction and complete A/B/C signature bands",
        "finite_audit_role": "independent ordered/canonical recursion, child anchors, band coverage/signature/mex, low-R reduction, tail, parity, and fixed-seed scatter checks only",
        "scope": {
            "target": "H(R;(x,3);13), x>=3, R>=0",
            "anchor_R": "0 <= R <= x+40",
            "anchor_x": [3, 80],
            "direct_R": "0 <= R <= x+40",
            "direct_x": [3, 80],
            "low_R": "0 <= R <= 14",
            "low_x": [3, 1000],
            "scatter_points": 25000,
            "scatter_seed": 20261121,
            "signature_R": "1 <= R <= x+16",
            "signature_x": [3, 3000],
            "tail_R": "x+17 <= R <= x+20",
            "tail_x": [3, 10000],
            "theorem_grid_R": "0 <= R <= x+30",
            "theorem_grid_x": [3, 3000],
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
    print("all_pass:", result["all_pass"])
    print("total checks:", result["total_checks"])
    print("repeat byte-identical:", result["repeat_byte_identical"])
    print("audit.json sha256 (without hash field):",
          result["sha256_without_hash_field"])


if __name__ == "__main__":
    run()
