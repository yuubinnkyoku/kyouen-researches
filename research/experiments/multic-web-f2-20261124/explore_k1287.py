#!/usr/bin/env python3
"""explore_k1287: wide census explorer for the multi-c web F2 package.

Pre-declaration exploration machine: it re-checks the five declared web
value-law tables (W/D/E/Ap/A, planes z in {0,1,2}) and the frontier
families (Am / SLB2 / SLB3 / L) on boxes that are WIDER than the audit
machine verify_k1287.py (W: d 1..8, c 2..7, m 1..12; D: d 2..8, c 2..7,
m 1..10; E: d 3..8, c 2..7, m 1..9; Ap: d 2..8, c 3..7, m 1..9;
A: s 0..6, m 1..12; Am: m 1..8, h 1..5, s 0..5; SLB2/3: x 2..12, c 1..8;
L: zp in {0,1}, d 1..8, s 1..5).

All claims here are CENSUS OBSERVATIONS on the stated finite boxes (the
audit machine re-checks the reproducible core box and the algebraic child
identities; universal status is discussed in the declaration note). The
laws checked are exactly the tables coded in verify_k1287.py (no tamper
paths there). Note the honest history: the E-family law used to be read
as "odd d -> 2 on z0/z2"; the wide census refuted exactly that (bad=96
on old lawcheck runs, all at odd d>=5) and produced the final table
EL(z,d): d even -> 1; d=3 -> (z1 -> 0, z0/z2 -> 2); odd d>=5 -> 0.

Usage: python3 explore_k1287.py z0|z1|z2|frontier
Stdout is deterministic given the argument (no timestamps on stdout).
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(200000)

@lru_cache(maxsize=2_000_000)
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

def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

def S(xs):
    return tuple(sorted(xs, reverse=True))

def XW(m, d, c):   return S([m] + [m + d] * c)
def XD(m, d, c):   return S([m, m + d - 1] + [m + d] * (c - 1))
def XE(m, d, c):   return S([m, m + d - 2] + [m + d] * (c - 1))
def XAp(m, d, c):  return S([m] + [m + d - 1] * 2 + [m + d] * (c - 2))
def XA(m, s):      return S([m, m] + [m + 1] * s)
def XAm(m, h, s):  return S([m, m] + [m + h] * s)

# ---- value-law tables (identical to verify_k1287.py, no tamper paths)
def WL(z, d, c, m):
    if z == 1:
        return 1 if d % 2 == 0 else 0
    if d == 1:
        if z == 2 and m == 1:
            return 2
        if c == 2:
            return 0
        return 2
    return 1 if d % 2 == 0 else 0

def DL(z, d, c, m):
    if z == 1:
        return 1 if d % 2 == 1 else 0
    if d == 2:
        if z == 2 and m == 1 and c == 2:
            return 0
        return 2
    return 1 if d % 2 == 1 else 0

def EL(z, d, c, m):
    if d % 2 == 0:
        return 1
    if d == 3:
        return 0 if z == 1 else 2
    return 0

def ApL(z, d, c, m):
    return 1 if d % 2 == 0 else 0

def AL(z, m, s):
    if z == 0:
        return 1 if s == 1 else 0
    if z == 2:
        if m == 1:
            return 0
        return 1 if s == 1 else 0
    if s == 0:
        return 0
    if m == 1:
        return 2
    if s == 1:
        return 1
    return 2

def AmL(z, m, h, s):
    if z == 0:
        return 0
    if z == 1:
        return 2 if s >= 1 else 0
    return 1 if (m == 1 and h == 2 and s == 1) else 0

def SLB2L(x, c):
    if x == 2:
        return 0 if c == 1 else (2 if c == 2 else 1)
    if c == 1:
        return 1 if x % 2 == 1 else 0
    return 1 if x % 2 == 0 else 0

def SLB3L(x, c):
    if x == 2:
        return 0 if c <= 2 else 1
    if c == 1:
        return 1 if x % 2 == 1 else 0
    return 1 if x % 2 == 0 else 0

def LL(zp, d, s):
    if d == 1 and zp == 0:
        return 2
    if d == 1 and zp == 1:
        return 1 if s == 1 else 0
    return 1 if d % 2 == 0 else 0

STAGE = sys.argv[1] if len(sys.argv) > 1 else 'z0'

def plane_family(z):
    t0 = time.time()
    res = {'stage': STAGE, 'z': z}
    n = bad = 0
    # W wide
    for d in range(1, 9):
        for c in range(2, 8):
            for m in range(1, 13):
                v = H(2 * m + d + 2 + z, XW(m, d, c), z)
                n += 1
                if v != WL(z, d, c, m):
                    bad += 1
                    print('W MISMATCH z=%d d=%d c=%d m=%d v=%d law=%d'
                          % (z, d, c, m, v, WL(z, d, c, m)))
    nw, bw = n, bad
    n = bad = 0
    for d in range(2, 9):
        for c in range(2, 8):
            for m in range(1, 11):
                v = H(2 * m + d + 1 + z, XD(m, d, c), z)
                n += 1
                if v != DL(z, d, c, m):
                    bad += 1
                    print('D MISMATCH z=%d d=%d c=%d m=%d v=%d law=%d'
                          % (z, d, c, m, v, DL(z, d, c, m)))
    nd, bd = n, bad
    n = bad = 0
    for d in range(3, 9):
        for c in range(2, 8):
            for m in range(1, 10):
                v = H(2 * m + d + z, XE(m, d, c), z)
                n += 1
                if v != EL(z, d, c, m):
                    bad += 1
                    print('E MISMATCH z=%d d=%d c=%d m=%d v=%d law=%d'
                          % (z, d, c, m, v, EL(z, d, c, m)))
    ne, be = n, bad
    n = bad = 0
    for d in range(2, 9):
        for c in range(3, 8):
            for m in range(1, 10):
                v = H(2 * m + d + z, XAp(m, d, c), z)
                n += 1
                if v != ApL(z, d, c, m):
                    bad += 1
                    print('Ap MISMATCH z=%d d=%d c=%d m=%d v=%d law=%d'
                          % (z, d, c, m, v, ApL(z, d, c, m)))
    nap, bap = n, bad
    n = bad = 0
    for s in range(0, 7):
        for m in range(1, 13):
            v = H(2 * m + 2 + z, XA(m, s), z)
            n += 1
            if v != AL(z, m, s):
                bad += 1
                print('A MISMATCH z=%d m=%d s=%d v=%d law=%d'
                      % (z, m, s, v, AL(z, m, s)))
    print('FAMILY_SUMMARY z=%d W: n=%d bad=%d | D: n=%d bad=%d | '
          'E: n=%d bad=%d | Ap: n=%d bad=%d | A: n=%d bad=%d'
          % (z, nw, bw, nd, bd, ne, be, nap, bap, n, bad))
    # exception spot rows (deterministic raw tables)
    print('SPOT W(z=%d,m=1,d=1,all c):' % z,
          [H(4 + 3 + z, XW(1, 1, c), z) for c in range(2, 8)])
    print('SPOT W(z=%d,m=1,d=2,all c):' % z,
          [H(6 + z, XW(1, 2, c), z) for c in range(2, 8)])
    print('SPOT D(z=%d,m=1,d=2,all c):' % z,
          [H(5 + z, XD(1, 2, c), z) for c in range(2, 8)])
    print('SPOT E(z=%d,d=3,c=2,m 1..9):' % z,
          [H(2 * m + 3 + z, XE(m, 3, 2), z) for m in range(1, 10)])
    print('SPOT A(z=%d,s 0..6,m=1):' % z,
          [H(4 + z, XA(1, s), z) for s in range(0, 7)])

import time

def frontier():
    n = bad = 0
    for z in (0, 1, 2):
        for h in range(1, 6):
            for s in range(0, 6):
                for m in range(1, 9):
                    v = H(2 * m + 2 + z, XAm(m, h, s), z)
                    if h == 1:
                        continue  # A family duplicAte; counted in planes
                    n += 1
                    if v != AmL(z, m, h, s):
                        bad += 1
                        print('Am MISMATCH z=%d m=%d h=%d s=%d v=%d law=%d'
                              % (z, m, h, s, v, AmL(z, m, h, s)))
    print('FRONTIER Am (h 2..5): n=%d bad=%d' % (n, bad))
    n = bad = 0
    for x in range(2, 13):
        for c in range(1, 9):
            v = H(x + 3, S([x] * c), 2)
            n += 1
            if v != SLB2L(x, c):
                bad += 1
                print('SLB2 MISMATCH x=%d c=%d v=%d law=%d' % (x, c, v, SLB2L(x, c)))
    print('FRONTIER SLB2: n=%d bad=%d' % (n, bad))
    n = bad = 0
    for x in range(2, 13):
        for c in range(1, 9):
            v = H(x + 4, S([x] * c), 3)
            n += 1
            if v != SLB3L(x, c):
                bad += 1
                print('SLB3 MISMATCH x=%d c=%d v=%d law=%d' % (x, c, v, SLB3L(x, c)))
    print('FRONTIER SLB3: n=%d bad=%d' % (n, bad))
    n = bad = 0
    for zp in (0, 1):
        for d in range(1, 9):
            for s in range(1, 6):
                v = H(d + 2 + zp, S([d] + [d + 1] * s), zp + 1)
                n += 1
                if v != LL(zp, d, s):
                    bad += 1
                    print('L MISMATCH zp=%d d=%d s=%d v=%d law=%d'
                          % (zp, d, s, v, LL(zp, d, s)))
    print('FRONTIER L: n=%d bad=%d' % (n, bad))
    # raw tables
    for z in (0, 1, 2):
        print('RAW Am z=%d (h x s -> m rows 1..8):' % z)
        for h in (2, 3):
            for s in (0, 1, 2, 3):
                print('  h=%d s=%d:' % (h, s),
                      [H(2 * m + 2 + z, XAm(m, h, s), z) for m in range(1, 9)])
    print('RAW SLB2 x rows (c 1..8):')
    for x in (2, 3, 4, 5):
        print('  x=%d:' % x, [H(x + 3, S([x] * c), 2) for c in range(1, 9)])
    print('RAW SLB3 x rows (c 1..8):')
    for x in (2, 3, 4, 5):
        print('  x=%d:' % x, [H(x + 4, S([x] * c), 3) for c in range(1, 9)])
    for zp in (0, 1):
        print('RAW L zp=%d (d -> s 1..5):' % zp)
        for d in (1, 2, 3, 4):
            print('  d=%d:' % d,
                  [H(d + 2 + zp, S([d] + [d + 1] * s), zp + 1) for s in range(1, 6)])

if STAGE in ('z0', 'z1', 'z2'):
    plane_family(int(STAGE[1]))
elif STAGE == 'frontier':
    frontier()
else:
    raise SystemExit('unknown stage: %s' % STAGE)
