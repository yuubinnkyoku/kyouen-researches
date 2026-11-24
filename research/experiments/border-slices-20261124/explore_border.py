#!/usr/bin/env python3
"""explore_border: pre-declaration census of the border region (k<=0) for
pair slices and the allm beds (reproduction record of the K1286
exploration; the declaration note cites these as E1-E6).

All queries are restricted to VALID positions (budget R >= 0); cells with
R < 0 are printed as '.' and excluded from law/m-independence tests.

  E1  border pair-slice census z in {0,1,2}, k in [-8..0], m 1..8,
      g 1..18: per-(z,k) m-independence over valid cells + m=1 row.
  E2  z0 delta-collapse candidate: value == f0(g+k) per valid cell
      (m<=12, g<=21, k in [-26..0]) + mismatch count.
  E3  allm bed census (m,m)@(2m+j), z in {0,1,2}, j in [-8..2], m 1..14
      + per-(z,j) m-constancy.
  E4  z1 slice-law candidate table Z1(k,g), k in {-1,0,1}, and z2 law
      table Z2(k,g), k in {0,1,2}: match counts over m<=14, g<=21.
  E5  F2 spread web census: F_d(m,c) / G_d(m,c), d in {1,2,3},
      m 1..8, c 1..6 (multi-token positions, observation only).
  E6  nucleation census z1-k(-2), z2-k(-1), z2-k(-2): m 1..10, g 1..16,
      explicit m-split report.
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


def z1k(k, g):
    if k == 1:
        if g == 1: return 1
        if g == 2: return 2
        return IND(g % 2 == 0)
    if k == 0:
        if g == 1: return 2
        return IND(g % 2 == 1)
    if k == -1:
        if g == 1: return 1
        if g == 2: return 2
        return IND(g % 2 == 0)
    raise ValueError((k, g))


def z2k(k, g):
    if k in (0, 2):
        if g == 1: return 1
        if g == 2: return 0
        if g == 3: return 2
        return IND(g % 2 == 0)
    if k == 1:
        return IND(g % 2 == 1)
    raise ValueError((k, g))


def cell(z, k, m, g):
    R = 2 * m + g + k
    if R < 0:
        return None
    return H(R, (m, m + g), z)


def srow(vals):
    return '[' + ', '.join('.' if v is None else str(v) for v in vals) + ']'


print("E1: border pair-slice census, k in [-8..0], m 1..8, g 1..18 (valid cells)")
for z in (0, 1, 2):
    for k in range(-8, 1):
        rows = {m: [cell(z, k, m, g) for g in range(1, 19)] for m in range(1, 9)}
        indep = True
        for m in range(2, 9):
            for g in range(1, 19):
                a, b = rows[1][g - 1], rows[m][g - 1]
                if a is not None and b is not None and a != b:
                    indep = False
        print("z=%d k=%d INDEP=%s m1=%s" % (z, k, indep, srow(rows[1])))

print()
print("E2: z0 delta-collapse candidate value==f0(g+k), m 1..12, g 1..21, k [-26..0]")
n = bad = 0
badex = []
for m in range(1, 13):
    for g in range(1, 22):
        for k in range(max(-26, -2 * m - g), 1):
            v = cell(0, k, m, g)
            e = f0(g + k)
            n += 1
            if v != e:
                bad += 1
                if len(badex) < 8: badex.append((m, g, k, v, e))
print("valid cells=%d mismatches=%d %s" % (n, bad, badex))

print()
print("E3: allm bed census (m,m)@(2m+j), z x j in [-8..2], m 1..14")
for z in (0, 1, 2):
    for j in range(-8, 3):
        vals = []
        for m in range(1, 15):
            R = 2 * m + j
            vals.append('.' if R < 0 else H(R, (m, m), z))
        uniq = sorted(set(vals) - {'.'})
        const = len(uniq) <= 1
        print("z=%d j=%d const=%s vals=%s" % (z, j, const, srow(vals)))

print()
print("E4: z1 law table Z1 (k -1..1) / z2 law table Z2 (k 0..2), m 1..14, g 1..21")
for (z, ks, fn, tag) in [(1, (-1, 0, 1), z1k, 'Z1'), (2, (0, 1, 2), z2k, 'Z2')]:
    n = bad = 0
    for k in ks:
        for m in range(1, 15):
            for g in range(1, 22):
                v = cell(z, k, m, g)
                e = fn(k, g)
                n += 1
                if v != e:
                    bad += 1
                    if bad < 5: print("  MISMATCH", tag, m, g, k, v, e)
    print("%s: cells=%d mismatches=%d" % (tag, n, bad))

print()
print("E5: F2 spread web census (observation only), d 1..3, m 1..8, c 1..6")
def Fexp(d, c):
    if d == 1: return 1 if c == 1 else 0
    if d == 2: return 0 if c == 1 else 1
    return 1 if c == 1 else 0


def Gexp(d, c):
    if d == 1:
        return 1 if c == 1 else (0 if c == 2 else 2)
    if d == 2: return 0 if c == 1 else 1
    return 1 if c == 1 else 0


for d in (1, 2, 3):
    rowsF, rowsG = [], []
    for c in range(1, 7):
        rowsF.append([H(2 * m + d + 3, tuple(sorted([m] + [m + d] * c, reverse=True)), 1) for m in range(1, 9)])
        rowsG.append([H(2 * m + d + 2, tuple(sorted([m] + [m + d] * c, reverse=True)), 0) for m in range(1, 9)])
    print("d=%d F rows(c=1..6, m=1..8):" % d)
    for c in range(1, 7):
        e = Fexp(d, c)
        ok = '' if rowsF[c - 1] == [e] * 8 else ' MISMATCH'
        print("  c=%d -> %s (exp %d)%s" % (c, rowsF[c - 1], e, ok))
    print("d=%d G rows(c=1..6, m=1..8):" % d)
    for c in range(1, 7):
        e = Gexp(d, c)
        ok = '' if rowsG[c - 1] == [e] * 8 else ' MISMATCH'
        print("  c=%d -> %s (exp %d)%s" % (c, rowsG[c - 1], e, ok))

print()
print("E6: nucleation census z1-k(-2), z2-k(-1), z2-k(-2), m 1..10, g 1..16")
for (z, k, tag) in [(1, -2, 'z1km2'), (2, -1, 'z2km1'), (2, -2, 'z2km2')]:
    print("%s rows by m (g=1..16):" % tag)
    for m in range(1, 11):
        vals = [cell(z, k, m, g) for g in range(1, 17)]
        print("  m=%d %s" % (m, srow(vals)))
print("done")
