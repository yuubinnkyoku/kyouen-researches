#!/usr/bin/env python3
"""explore_k1285: pre-declaration exploration for the K1285 pair-slices pack.

Reproduces the discovery censuses (deterministic):
  E1  pair k-slice family discovery tables (k = R - 2m - g coordinate)
  E2  J-family row-1 tables ((1, 1+g)@r, z0/z1) incl. diagonal law reading
  E3  pre-band single-layer laws (x^c)@(x+1,x+2) z0/z1
  E4  border triangle observations (z0-k0 / z1-k1 / z2-k1 / z2-k2)
  E5  multi-c web Attempt (F/G d=1 c-slices) and the z2-band blocker
  E6  slice law wide confirmation (the basis of the D8 battery)

This is a record of exploration, NOT an audit: the official machine is
verify_k1285.py (see the declaration note for the publish-then-execute
protocol).
"""
import sys
from functools import lru_cache


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


def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


print("E1 pair k-slice discovery: k = R - 2m - g, family (z, k); m=1..4, g=1..12")
for z in (0, 1, 2):
    for k in range(0, 5):
        print("  z=%d k=%d" % (z, k))
        for m in range(1, 5):
            row = [H(2 * m + g + k, (m, m + g), z) for g in range(1, 13)]
            print("    m=%d: %s" % (m, row))

print("E2 J-family row-1: (1, 1+g)@r, r=3..13, g=1..9, z0 then z1")
for z in (0, 1):
    for r in range(3, 14):
        print("  z=%d r=%d: %s" % (z, r,
              [H(r, (1, 1 + g), z) for g in range(1, 10)]))

print("E3 pre-band single-layer: (x^c)@(x+1) z0 [PC], (x^c)@(x+2) z1 [PB2]; x=2..8, c=1..5")
for x in range(2, 9):
    print("  x=%d PC(z0,x+1): %s  PB2(z1,x+2): %s" % (
        x,
        [H(x + 1, (x,) * c, 0) for c in range(1, 6)],
        [H(x + 2, (x,) * c, 1) for c in range(1, 6)]))

print("E4 border triangle: z0-k0 / z1-k1 / z2-k1 / z2-k2 pairs m=1..6, g=1..12")
for (z, k) in [(0, 0), (1, 1), (2, 1), (2, 2)]:
    for m in range(1, 7):
        print("  z=%d k=%d m=%d: %s" % (z, k, m,
              [H(2 * m + g + k, (m, m + g), z) for g in range(1, 13)]))

print("E5 multi-c web attempt: F(d=1,c,m)=(m,(m+1)^c)@2m+4 z1, G=(... )@2m+3 z0")
for m in range(1, 9):
    print("  F m=%d: c=1..6 %s" % (m,
          [H(2 * m + 4, tuple(sorted([m] + [m + 1] * c, reverse=True)), 1)
           for c in range(1, 7)]))
    print("  G m=%d: c=1..6 %s" % (m,
          [H(2 * m + 3, tuple(sorted([m] + [m + 1] * c, reverse=True)), 0)
           for c in range(1, 7)]))
print("  z2-pre-band single-layer (x^c)@(x+3) z2, x=2..8, c=1..5 (blocker census)")
for x in range(2, 9):
    print("  x=%d: %s" % (x, [H(x + 3, (x,) * c, 2) for c in range(1, 6)]))

print("E6 slice law confirmation grid (m<=8, g<=14, fams 7) - counts of mismatches vs [g odd]")
fams = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (2, 4)]
tot = 0; bad = 0
for (z, k) in fams:
    n = 0; b = 0
    for m in range(1, 9):
        for g in range(1, 15):
            n += 1
            if H(2 * m + g + k, (m, m + g), z) != (1 if g % 2 else 0):
                b += 1
    print("  z=%d k=%d n=%d bad=%d" % (z, k, n, b))
    tot += n; bad += b
print("  TOTAL n=%d bad=%d" % (tot, bad))
