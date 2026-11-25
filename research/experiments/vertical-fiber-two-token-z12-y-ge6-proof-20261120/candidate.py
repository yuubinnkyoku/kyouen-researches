#!/usr/bin/env python3
"""Closed forms and direct engines for the two-token residual game z=12, y>=6.

The theorem candidate is value12(x,y,R), with S=x+y and d=x-y.
The child anchors are K1043 (z=12,y=5) and K1055 (z=11,y>=6).
"""
from functools import lru_cache
import math
import sys

sys.setrecursionlimit(300000)


def _odd(R, lo, hi):
    return R % 2 == 1 and lo <= R <= hi


def _even(R, lo, hi):
    return R % 2 == 0 and lo <= R <= hi


def value12_T(x, y, R):
    d = x - y
    Y = 2 * y
    S = x + y
    if d == 0 and y == 6:
        return _odd(R, 1, 17)
    if _odd(R, 1, 11):
        return True
    if d in (2, 6, 10):
        return R == Y + {2: 7, 6: 9, 10: 11}[d]
    if d == 13:
        return _odd(R, Y + 13, S + 12)
    if d >= 14:
        return R == Y + 13
    return False


def value12_P(x, y, R):
    d = x - y
    Y = 2 * y
    S = x + y
    if d == 0:
        return y >= 7 and _odd(R, 13, Y + 5)
    if d % 2 == 0:
        if d <= 10:
            cap = Y + 5 + 2 * math.ceil((d - 2) / 4)
            return _odd(R, 13, cap)
        if d == 12:
            return _odd(R, 13, Y + 11)
        if d >= 14:
            return (_odd(R, 13, Y + 11)
                    or _even(R, Y + 14, S + 12))
    else:
        if d <= 11:
            if _odd(R, 13, S + 12):
                return True
            if d == 1:
                return _even(R, Y + 8, S + 11)
            cap = Y + 4 + 2 * math.ceil((d - 1) / 4)
            special = d % 4 == 3 and R == cap + 2
            return special or _even(R, cap + 4, S + 11)
        if d >= 13:
            return (_odd(R, 13, Y + 11)
                    or _even(R, Y + 14, S + 11))
    return False


def value12(x, y, R):
    """Full candidate for z=12, x>=y>=6, all R>=0."""
    if R == 0:
        return 0
    S = x + y
    if R >= S + 13:
        return S % 2
    if value12_T(x, y, R):
        return 2
    if value12_P(x, y, R):
        return 1
    return 0


def k1055_z11(x, y, R):
    """Transcription of K1055: z=11, x>=y>=6."""
    d = x - y
    Y = 2 * y
    S = x + y
    if R == 0:
        return 0
    if R >= S + 12:
        return S % 2
    if _odd(R, 1, 11):
        return 2
    if d == 3 and R == Y + 7:
        return 2
    if d == 7 and R == Y + 9:
        return 2
    if d == 11 and R == Y + 11:
        return 2
    if d == 12 and _odd(R, Y + 11, S + 11):
        return 2
    if d >= 13 and R == Y + 11:
        return 2
    if d % 2 == 0 and d <= 10:
        p = _even(R, 12, Y + 4 + 2 * math.ceil(d / 4))
    elif d == 12:
        p = _even(R, 12, Y + 10)
    elif d % 2 == 0 and d >= 14:
        p = (_even(R, 12, Y + 10)
             or _odd(R, Y + 13, S + 11))
    elif d % 2 == 1 and d <= 11:
        p = (_even(R, 12, S + 11)
             or _odd(R, Y + 7 + 2 * ((d + 1) // 4), S + 10))
    else:
        p = (_even(R, 12, Y + 10)
             or _odd(R, Y + 13, S + 10))
    return 1 if p else 0


def k1043_z12_y5(x, R):
    """Transcription of K1043: z=12, y=5, x>=6."""
    if R == 0:
        return 0
    if R >= x + 18:
        return (x + 5) % 2
    odd = lambda lo, hi: _odd(R, lo, hi)
    T = False
    if x == 6:
        T = odd(1, 11)
    elif x == 7:
        T = odd(1, 17)
    elif 8 <= x <= 10:
        T = odd(1, 11)
    elif x == 11:
        T = odd(1, 11) or R == 19
    elif 12 <= x <= 14:
        T = odd(1, 11)
    elif x == 15:
        T = odd(1, 11) or R == 21
    elif x in (16, 17):
        T = odd(1, 11)
    elif x == 18:
        T = odd(1, 11) or odd(23, 35)
    else:
        T = odd(1, 11) or R == 23
    if T:
        return 2

    base = {
        8: (13, 15, 17),
        9: (13, 15, 17),
        10: (13, 15, 17, 19),
        11: (13, 15, 17),
        12: (13, 15, 17, 19),
        13: (13, 15, 17, 19),
        14: (13, 15, 17, 19, 21),
        15: (13, 15, 17, 19),
        16: (13, 15, 17, 19, 21),
        17: (13, 15, 17, 19, 21),
    }
    if x == 6 and R >= 12:
        return 1
    if x in base and R in base[x]:
        return 1
    if x in (8, 10, 12, 14, 16):
        lo = {8: 18, 10: 20, 12: 20, 14: 22, 16: 22}[x]
        if R >= lo:
            return 1
    if x >= 18 and R in (13, 15, 17, 19, 21):
        return 1
    if x >= 18 and _even(R, 24, x + 17):
        return 1
    return 0


def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


@lru_cache(None)
def H_ordered(R, X, z):
    """Direct mex recurrence preserving token order and duplicate moves."""
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            child = X[:i] + (v - 1,) + X[i + 1:]
            opts.add(H_ordered(R - 1, child, z))
        else:
            child = X[:i] + X[i + 1:]
            opts.add(H_ordered(R - 1, child, z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)


@lru_cache(None)
def H_canonical(R, X, z):
    """Independent direct mex recurrence on descending multiset states."""
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:],
                                 reverse=True))
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


def clear_engines():
    H_ordered.cache_clear()
    H_canonical.cache_clear()


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
