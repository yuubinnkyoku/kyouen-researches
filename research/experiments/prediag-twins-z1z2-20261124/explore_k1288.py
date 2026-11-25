#!/usr/bin/env python3
"""explore_k1288: pre-declaration census of the z1/z2 PRE-DIAGONAL band
(slices k<=-2 for z1, k<=-1 for z2) and the corresponding beds (z1 beds
j<=-2, z2 beds j<=-1). Successor of explore_border (K1286 E1-E6); this
covers the regions K1286 left open as O1/O2/O4.

All queries restricted to VALID positions (budget R >= 0); invalid cells
printed '.'.

  X1  z1 pre-diag slices k in [-9..-2], m 1..10, g 1..16: per-(k) rows
      by m, m-uniformity report (m>=2 uniform? m=1 row?), cross-k row
      comparison (is the row table k-uniform for k<=-2?).
  X2  z1 beds (m,m)@(2m+j), j in [-12..-2], m 1..14: per-(j) values by m,
      m-split report.
  X3  z2 pre-diag slices k in [-9..-1], m 1..10, g 1..16.
  X4  z2 beds j in [-12..-1], m 1..14.
"""
from engine_block import H_canonical as H


def IND(b):
    return 1 if b else 0


def f0(d):
    if d == 1:
        return 2
    if d <= 0:
        return IND(d % 2 == 1)
    return IND(d % 2 == 0)


def cell(z, k, m, g):
    R = 2 * m + g + k
    if R < 0:
        return None
    return H(R, (m, m + g), z)


def bed(z, m, j):
    R = 2 * m + j
    if R < 0:
        return None
    return H(R, (m, m), z)


def srow(vals):
    return '[' + ', '.join('.' if v is None else str(v) for v in vals) + ']'


print("X1: z1 pre-diag slices k in [-9..-2], m 1..10, g 1..16")
for k in range(-9, -1):
    print("z1 k=%d:" % k)
    for m in range(1, 11):
        vals = [cell(1, k, m, g) for g in range(1, 17)]
        print("  m=%d %s" % (m, srow(vals)))
    rows = {m: [cell(1, k, m, g) for g in range(1, 17)] for m in range(1, 11)}
    # m>=2 uniformity over valid cells
    uni = True
    for m in range(3, 11):
        for g in range(1, 17):
            a, b = rows[2][g - 1], rows[m][g - 1]
            if a is not None and b is not None and a != b:
                uni = False
    # m=1 vs m=2 diffs
    d12 = [(g, rows[1][g - 1], rows[2][g - 1]) for g in range(1, 17)
           if rows[1][g - 1] is not None and rows[2][g - 1] is not None
           and rows[1][g - 1] != rows[2][g - 1]]
    print("  m>=2 uniform: %s ; m1-vs-m2 diffs (g,v1,v2): %s" % (uni, d12))
    print()

print("X1b: cross-k comparison of z1 common rows (m>=2 representative row m=5):")
for k in range(-9, -1):
    vals = [cell(1, k, 5, g) for g in range(1, 17)]
    print("  k=%d %s" % (k, srow(vals)))
print()

print("X2: z1 beds (m,m)@(2m+j), j in [-12..-2], m 1..14")
for j in range(-12, -1):
    vals = [bed(1, m, j) for m in range(1, 15)]
    print("z1 j=%d %s" % (j, srow(vals)))
print()

print("X3: z2 pre-diag slices k in [-9..-1], m 1..10, g 1..16")
for k in range(-9, 0):
    print("z2 k=%d:" % k)
    for m in range(1, 11):
        vals = [cell(2, k, m, g) for g in range(1, 17)]
        print("  m=%d %s" % (m, srow(vals)))
    rows = {m: [cell(2, k, m, g) for g in range(1, 17)] for m in range(1, 11)}
    uni = all(
        rows[m][g - 1] in (None, rows[1][g - 1])
        for m in range(2, 11) for g in range(1, 17)
        if rows[1][g - 1] is not None or rows[m][g - 1] is not None
    ) and all(rows[m][g-1] is not None or True for m in range(1, 11) for g in range(1, 17))
    # simpler: m-uniform means all valid values equal per g
    flat = True
    for g in range(1, 17):
        vs = {rows[m][g - 1] for m in range(1, 11) if rows[m][g - 1] is not None}
        if len(vs) > 1:
            flat = False
    d12 = [(g, rows[1][g - 1], rows[2][g - 1]) for g in range(1, 17)
           if rows[1][g - 1] is not None and rows[2][g - 1] is not None
           and rows[1][g - 1] != rows[2][g - 1]]
    print("  all-m uniform: %s ; m1-vs-m2 diffs: %s" % (flat, d12))
    print()

print("X4: z2 beds j in [-12..-1], m 1..14")
for j in range(-12, 0):
    vals = [bed(2, m, j) for m in range(1, 15)]
    print("z2 j=%d %s" % (j, srow(vals)))
print("done")
