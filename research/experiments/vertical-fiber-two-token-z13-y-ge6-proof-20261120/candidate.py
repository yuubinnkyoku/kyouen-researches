#!/usr/bin/env python3
"""Candidate uniform closed form for the two-token residual game
z=13, all x>=y>=6, all R>=0.

T (value 2), P (value 1), band region 1<=R<=S+13 (S=x+y, Y=2y, d=x-y),
tail R>=S+14 -> S mod 2 (K0832 general tail).

Classes (z=13, odd z):
  T: ladder O[1,13];
     lattice d+z≡2 (mod 4), d<=13: point R=Y+(d+z)/2 (d=1,5,9,13);
     sweep d=14 (=z+1): O[Y+13, S+13];
     pin d>=15: R=Y+13.
     Degenerate base cells: (y,d)=(6,0): ladder stops at O[1,11];
     (y,d)=(6,1): contiguous O[1,19]=O[1,Y+7].
  P: even d<=12: E[14, Y+4+2*ceil((d+2)/4)];
     d=14: E[14, Y+12];
     even d>=16: E[14, Y+12] ∪ O[Y+15, S+13];
     odd d<=13: E[14, S+13] ∪ O[Y+7+2*ceil(d/4), S+12];
     odd d>=15: E[14, Y+12] ∪ O[Y+15, S+12].
     Degenerate base cell (y,d)=(6,0): no P at all.
Child anchors (published): K1045 (z=13,y=5, x>=6) for the y=6 B child,
K1056 z=12 uniform for the C child.
"""
import math
import sys
from functools import lru_cache

sys.setrecursionlimit(500000)


def _odd(R, lo, hi):
    return R % 2 == 1 and lo <= R <= hi


def _even(R, lo, hi):
    return R % 2 == 0 and lo <= R <= hi


def v13_T(x, y, R):
    d = x - y
    S = x + y
    Y = 2 * y
    if y == 6 and d == 0:
        return _odd(R, 1, 11)
    if y == 6 and d == 1:
        return _odd(R, 1, 19)
    if _odd(R, 1, 13):
        return True
    if d % 2 == 1 and 1 <= d <= 13 and (d + 13) % 4 == 2:
        return R == Y + (d + 13) // 2
    if d == 14 and _odd(R, Y + 13, S + 13):
        return True
    if d >= 15 and R == Y + 13:
        return True
    return False


def v13_P(x, y, R):
    d = x - y
    S = x + y
    Y = 2 * y
    if y == 6 and d == 0:
        return False
    if d % 2 == 0:
        if d <= 12:
            return _even(R, 14, Y + 4 + 2 * ((d + 2 + 3) // 4))
        if d == 14:
            return _even(R, 14, Y + 12)
        return (_even(R, 14, Y + 12)
                or _odd(R, Y + 15, S + 13))
    if d <= 13:
        return (_even(R, 14, S + 13)
                or _odd(R, Y + 7 + 2 * ((d + 3) // 4), S + 12))
    return (_even(R, 14, Y + 12)
            or _odd(R, Y + 15, S + 12))


def v13(x, y, R):
    if R == 0:
        return 0
    S = x + y
    if R >= S + 14:
        return S % 2
    if v13_T(x, y, R):
        return 2
    if v13_P(x, y, R):
        return 1
    return 0


# ------- K1056 (z=12, x>=y>=6) uniform formula transcription -------

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


# ------- K1045 (z=13, y=5, x>=5) transcription (from its verifier) ---

def k1045_T(x, r):
    if x == 5:
        return _odd(r, 1, 9)
    if x in (6, 7):
        return _odd(r, 1, 11)
    if x == 8:
        return _odd(r, 1, 17)
    if x == 9:
        return _odd(r, 1, 13)
    if x == 10:
        return _odd(r, 1, 13) or r == 19
    if x in (11, 12, 13, 15, 16, 17):
        return _odd(r, 1, 13)
    if x == 14:
        return _odd(r, 1, 13) or r == 21
    if x == 18:
        return _odd(r, 1, 13) or r == 23
    if x == 19:
        return _odd(r, 1, 13) or _odd(r, 23, 37)
    return _odd(r, 1, 13) or r == 23


def k1045_P(x, r):
    if x == 5:
        return False
    if x == 6:
        return r >= 12
    if x == 7:
        return False
    if x == 8:
        return r in (14, 16, 18) or r >= 19
    if x == 9:
        return r in (14, 16, 18)
    if x == 10:
        return r in (14, 16, 18, 20) or r >= 21
    if x == 11:
        return r in (14, 16, 18)
    if x == 12:
        return r in (14, 16, 18, 20) or r >= 21
    if x == 13:
        return r in (14, 16, 18, 20)
    if x == 14:
        return r in (14, 16, 18, 20, 22) or r >= 23
    if x == 15:
        return r in (14, 16, 18, 20)
    if x == 16:
        return r in (14, 16, 18, 20, 22) or r >= 23
    if x == 17:
        return r in (14, 16, 18, 20, 22)
    if x == 18:
        return r in (14, 16, 18, 20, 22) or r >= 24
    if x == 19:
        return r in (14, 16, 18, 20, 22)
    if x % 2 == 0:
        return (r in (14, 16, 18, 20, 22)
                or (r % 2 == 1 and 25 <= r <= x + 17)
                or r >= x + 19)
    return r in (14, 16, 18, 20, 22) or (r % 2 == 1 and 25 <= r <= x + 18)


def k1045(x, r):
    if r == 0:
        return 0
    if k1045_T(x, r):
        return 2
    return 1 if k1045_P(x, r) else 0


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


if __name__ == "__main__":
    bad = tot = 0
    for y in [6, 7, 8, 9, 10, 11, 12]:
        for d in range(0, 16):
            x = y + d
            for R in range(0, x + y + 15):
                tot += 1
                a = H_ord(R, (x, y), 13)
                b = H_can(R, (x, y), 13)
                if a != b:
                    print("ENGINE MISMATCH", y, d, R, a, b)
                    bad += 1
                if a != v13(x, y, R):
                    bad += 1
                    if bad < 40:
                        print(f"MISMATCH z13 y={y} d={d} x={x} R={R}: engine {a} cand {v13(x,y,R)}")
            clear()
    for y in [15, 20, 25, 40]:
        for d in range(0, 12):
            x = y + d
            for R in range(0, x + y + 15):
                tot += 1
                a = H_ord(R, (x, y), 13)
                if a != v13(x, y, R):
                    bad += 1
                    if bad < 60:
                        print(f"MISMATCH z13 y={y} d={d} R={R}: engine {a} cand {v13(x,y,R)}")
            clear()
    print(f"z13 candidate engine checks: total={tot} bad={bad}")
    # C anchor: z=12 uniform transcription vs engine
    bad2 = tot2 = 0
    for y in [6, 7, 8, 9, 10, 12, 15]:
        for d in range(0, 14):
            x = y + d
            for r in range(0, x + y + 14):
                tot2 += 1
                a = H_ord(r, (x, y), 12)
                if a != value12(x, y, r):
                    bad2 += 1
                    if bad2 < 20:
                        print(f"MISMATCH z12 y={y} d={d} r={r}: engine {a} cand {value12(x,y,r)}")
            clear()
    print(f"z12 K1056 transcription checks: total={tot2} bad={bad2}")
    # B anchor: K1045 transcription vs engine
    bad3 = tot3 = 0
    for x in range(5, 31):
        for r in range(0, x + 24):
            tot3 += 1
            a = H_ord(r, (x, 5), 13)
            if a != k1045(x, r):
                bad3 += 1
                if bad3 < 20:
                    print(f"MISMATCH k1045 x={x} r={r}: engine {a} cand {k1045(x,r)}")
        clear()
    print(f"k1045 transcription checks: total={tot3} bad={bad3}")
