#!/usr/bin/env python3
"""explore_k1299 (pre-declaration discovery census; K1290/K1294 kit syntax).

Discovery battery for the z9/z10 pre-diagonal twin layers (thickness 10)
and the plane-10/11 single-token uniformity lemmas, run BEFORE the
single-owner declaration:

  X1  z9 band (R, delta) table, m<=12, g<=25, all k<=0 in box: values
      depend only on (R, delta); low-R rows constant by parity (expected
      exception layer 2*[R odd] for R < L(9) = 2*ceil(9/2) = 10).
  X2  z9 beds (R, j) table, m<=12, j in [-30..0].
  X3  z10 band (R, delta) table (same box; expected layer for
      R < L(10) = 10, main f0(delta-10)).
  X4  z10 beds (same box as X2).
  X5  L-BU9G discovery: v(w,10,t) vs plane-9 law for w<=30
      (layer 2*[t odd] t<10, main g1(t-8)).
  X6  L-BU10G discovery: v(w,11,t) vs plane-10 law for w<=30
      (layer 2*[t odd] t<10, main f0(t-10)).
  X7  sharpened C-PSF first probe: z0..z12 planes, small box,
      layer = 2*[R odd] for R < 2*ceil(w/2), main = T_w(delta-2*floor(w/2)).
      (z11/z12 are NEW observation planes beyond the K1294 X7 z<=12 dedup
      band probe; here with band/bed tables.)
  X8  typed-children self-check: build z9/z10 pair/bed children ONLY from
      the claim tables (this package's z9/z10 claims + K1294 z7/z8 claims,
      which the C children reference) + the K0832 closed form through the
      L-BU9G/L-BU10G laws; mex == claim == engine on a discovery box
      (validates the hand-proof syntax before the declaration).

Discovery census only, NO universal claims in this script.
"""
import sys
from collections import defaultdict
from engine_block import H_canonical as H, single_token as v

sys.setrecursionlimit(100000)


def IND(b):
    return 1 if b else 0


def f0(d):
    if d == 1:
        return 2
    if d <= 0:
        return IND(d % 2 == 1)
    return IND(d % 2 == 0)


def g1(d):
    if d == 1:
        return 2
    if d <= 0:
        return IND(d % 2 == 0)
    return IND(d % 2 == 1)


# published claims reused (K1294: z7/z8; needed as C-child inputs)
def z7_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 8 else g1(R - 2 * m - 6)


def z7_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 8 else g1(j - 6)


def z8_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 8 else f0(R - 2 * m - 8)


def z8_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 8 else f0(j - 8)


# the candidate claims of this package (T-PDT9/T-BDT9/T-PDT10/T-BDT10)
def z9_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 10 else g1(R - 2 * m - 8)


def z9_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 10 else g1(j - 8)


def z10_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 10 else f0(R - 2 * m - 10)


def z10_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 10 else f0(j - 10)


# candidate L-BU9G/L-BU10G laws (from the K0832 closed form; X5/X6 check)
def lbu9g(t):
    return 2 * (t % 2) if t < 10 else g1(t - 8)


def lbu10g(t):
    return 2 * (t % 2) if t < 10 else f0(t - 10)


def band_table(z, mmax, gmax, kmin):
    tab = defaultdict(set)
    for m in range(1, mmax + 1):
        for g in range(1, gmax + 1):
            for k in range(max(kmin, -2 * m - g), 1):
                R = 2 * m + g + k
                if R < 0:
                    continue
                d = R - 2 * m
                tab[(R, d)].add(H(R, tuple(sorted((m + g, m), reverse=True)), z))
        H.cache_clear()
    return tab


def bed_table(z, mmax, jmin):
    tab = defaultdict(set)
    for m in range(1, mmax + 1):
        for j in range(jmin, 1):
            R = 2 * m + j
            if R < 0:
                continue
            tab[(R, j)].add(H(R, (m, m), z))
        H.cache_clear()
    return tab


def show(tag, tab, rmax, dd):
    mixed = sum(1 for s in tab.values() if len(s) > 1)
    print('== %s: cells %d, mixed (R,delta) cells %d ==' % (tag, len(tab), mixed))
    for R in range(0, rmax + 1):
        keys = sorted(d for (r, d) in tab if r == R and d <= dd)
        row = ' '.join('%d:%d' % (d, sorted(tab[(R, d)])[0]) for d in keys)
        print('  R=%-2d %s' % (R, row[:340]))


def main():
    # X1/X3: z9/z10 band discovery tables
    for z in (9, 10):
        tab = band_table(z, 12, 25, -60)
        show('X%d z%d band m<=12 g<=25 k>=-60' % (1 if z == 9 else 3, z), tab, 15, 9)
    # X2/X4: z9/z10 bed discovery tables
    for z in (9, 10):
        tab = bed_table(z, 12, -30)
        show('X%d z%d beds m<=12 j in [-30..0]' % (2 if z == 9 else 4, z), tab, 15, 9)

    # X5/X6: L-BU9G / L-BU10G discovery
    bad9 = bad10 = 0
    n = 0
    for w in range(2, 31):
        for t in range(0, w + 1):
            va = H(t, (w,), 10)
            vc = v(w, 10, t)
            vb = H(t, (w,), 11)
            vd = v(w, 11, t)
            n += 4
            if not (va == vc == lbu9g(t)):
                bad9 += 1
                print('  L-BU9G dev', w, t, va, vc, lbu9g(t))
            if not (vb == vd == lbu10g(t)):
                bad10 += 1
                print('  L-BU10G dev', w, t, vb, vd, lbu10g(t))
        H.cache_clear()
    print('== X5/X6 L-BU9G/L-BU10G: checks %d, bad %d / %d ==' % (n, bad9, bad10))
    # w=1 edges recorded for the bed typed proofs
    print('  w=1: v(1,10,t) t=0..1 = %d,%d ; v(1,11,t) = %d,%d'
          % (v(1, 10, 0), v(1, 10, 1), v(1, 11, 0), v(1, 11, 1)))

    # X7: sharpened C-PSF first probe on z0..z12
    def cpsf(w, R, d):
        L = 2 * ((w + 1) // 2)
        shift = 2 * (w // 2)
        if R < L:
            return 2 * (R % 2)
        return g1(d - shift) if w % 2 else f0(d - shift)

    bad = {}
    cnt = {}
    for z in range(0, 13):
        tab = band_table(z, 10, 20, -50)
        mixed = sum(1 for s in tab.values() if len(s) > 1)
        b = 0
        for (R, d), vals in sorted(tab.items()):
            c = cpsf(z, R, d)
            for x in vals:
                if x != c:
                    b += 1
                    if b <= 5:
                        print('  cpsf dev z=%d (R=%d,d=%d): %s vs %d'
                              % (z, R, d, sorted(vals), c))
        bad[z] = b + 100 * mixed
        cnt[z] = len(tab)
    print('== X7 sharpened C-PSF probe (discovery only): bad %s over cells %s =='
          % (bad, cnt))

    # X8: typed-children self-check (children only from the claim tables
    # + closed form; validates the hand-proof mex syntax pre-declaration)
    def mexs(vals):
        s = set(vals)
        x = 0
        while x in s:
            x += 1
        return x

    def typed_z9_pair(R, m, g):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z9_pair_claim(R - 1, m - 1, g + 1))
        else:
            kids.append(lbu9g(R - 1))       # token g+1 @ plane 10 (t<=w)
        if g >= 2:
            kids.append(z9_pair_claim(R - 1, m, g - 1))
        else:
            kids.append(z9_bed_claim(R - 1, m, R - 2 * m - 1))
        kids.append(1 ^ z8_pair_claim(R - 1, m, g))   # C -> z8 (K1294)
        return mexs(kids)

    def typed_z9_bed(R, m, j):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z9_pair_claim(R - 1, m - 1, 1))
        else:
            kids.append(lbu9g(R - 1))       # token 1 @ plane 10, t<=1
        kids.append(1 ^ z8_bed_claim(R - 1, m, j - 1))
        return mexs(kids)

    def typed_z10_pair(R, m, g):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z10_pair_claim(R - 1, m - 1, g + 1))
        else:
            kids.append(lbu10g(R - 1))      # token g+1 @ plane 11
        if g >= 2:
            kids.append(z10_pair_claim(R - 1, m, g - 1))
        else:
            kids.append(z10_bed_claim(R - 1, m, R - 2 * m - 1))
        kids.append(1 ^ z9_pair_claim(R - 1, m, g))   # C -> z9 (packet)
        return mexs(kids)

    def typed_z10_bed(R, m, j):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z10_pair_claim(R - 1, m - 1, 1))
        else:
            kids.append(lbu10g(R - 1))
        kids.append(1 ^ z9_bed_claim(R - 1, m, j - 1))
        return mexs(kids)

    stats = defaultdict(int)
    for z, tpair, tbed, pc, bc in [
            (9, typed_z9_pair, typed_z9_bed, z9_pair_claim, z9_bed_claim),
            (10, typed_z10_pair, typed_z10_bed, z10_pair_claim, z10_bed_claim)]:
        for m in range(1, 11):
            for g in range(1, 15):
                for k in range(max(-14, -2 * m - g), 1):
                    R = 2 * m + g + k
                    if R < 0:
                        continue
                    exp = pc(R, m, g)
                    mx = tpair(R, m, g)
                    h = H(R, tuple(sorted((m + g, m), reverse=True)), z)
                    stats['slice'] += 1
                    if not (mx == exp == h):
                        stats['slice_bad'] += 1
                        if stats['slice_bad'] <= 8:
                            print('  X8 z%d dev m=%d g=%d k=%d R=%d exp=%d mx=%d h=%d'
                                  % (z, m, g, k, R, exp, mx, h))
            H.cache_clear()
            for j in range(-16, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                exp = bc(R, m, j)
                mx = tbed(R, m, j)
                h = H(R, (m, m), z)
                stats['bed'] += 1
                if not (mx == exp == h):
                    stats['bed_bad'] += 1
                    if stats['bed_bad'] <= 8:
                        print('  X8 z%d bed dev m=%d j=%d R=%d exp=%d mx=%d h=%d'
                              % (z, m, j, R, exp, mx, h))
            H.cache_clear()
    print('== X8 typed self-check: slices %d bad %d, beds %d bad %d =='
          % (stats['slice'], stats['slice_bad'], stats['bed'], stats['bed_bad']))


main()
