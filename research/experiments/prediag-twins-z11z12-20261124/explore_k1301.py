#!/usr/bin/env python3
"""explore_k1301 (pre-declaration discovery census; K1290/K1294/K1299 kit syntax).

Discovery battery for the z11/z12 pre-diagonal twin layers (thickness 12)
and the plane-12/13 single-token uniformity lemmas, run BEFORE the
single-owner declaration:

  X1  z11 band (R, delta) table, m<=12, g<=25, all k<=0 in box: values
      depend only on (R, delta); low-R rows constant by parity (expected
      exception layer 2*[R odd] for R < L(11) = 2*ceil(11/2) = 12).
  X2  z11 beds (R, j) table, m<=12, j in [-30..0].
  X3  z12 band (R, delta) table (same box; expected layer for
      R < L(12) = 12, main f0(delta-12)).
  X4  z12 beds (same box as X2).
  X5  L-BU11G discovery: v(w,12,t) vs plane-11 law for w<=30
      (layer 2*[t odd] t<12, main g1(t-10)).
  X6  L-BU12G discovery: v(w,13,t) vs plane-12 law for w<=30
      (layer 2*[t odd] t<12, main f0(t-12)).
  X7  sharpened C-PSF first probe: z0..z14 planes, small box,
      layer = 2*[R odd] for R < 2*ceil(w/2), main = T_w(delta-2*floor(w/2)).
      (z13/z14 are NEW observation planes beyond the K1299 X7 z<=12
      band probe / Y8 dedup z<=14; here with band/bed tables.)
  X8  typed-children self-check: build z11/z12 pair/bed children ONLY from
      the claim tables (this package's z11/z12 claims + K1299 z9/z10
      published claims, which the C children reference) + the K0832 closed
      form through the L-BU11G/L-BU12G laws; mex == claim == engine on a
      discovery box (validates the hand-proof syntax before the
      declaration).

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


# published claims reused (K1299: z9/z10; needed as C-child inputs)
def z9_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 10 else g1(R - 2 * m - 8)


def z9_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 10 else g1(j - 8)


def z10_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 10 else f0(R - 2 * m - 10)


def z10_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 10 else f0(j - 10)


# the candidate claims of this package (T-PDT11/T-BDT11/T-PDT12/T-BDT12)
def z11_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 12 else g1(R - 2 * m - 10)


def z11_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 12 else g1(j - 10)


def z12_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 12 else f0(R - 2 * m - 12)


def z12_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 12 else f0(j - 12)


# candidate L-BU11G/L-BU12G laws (from the K0832 closed form; X5/X6 check)
def lbu11g(t):
    return 2 * (t % 2) if t < 12 else g1(t - 10)


def lbu12g(t):
    return 2 * (t % 2) if t < 12 else f0(t - 12)


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
    # X1/X3: z11/z12 band discovery tables
    for z in (11, 12):
        tab = band_table(z, 12, 25, -60)
        show('X%d z%d band m<=12 g<=25 k>=-60' % (1 if z == 11 else 3, z), tab, 17, 9)
    # X2/X4: z11/z12 bed discovery tables
    for z in (11, 12):
        tab = bed_table(z, 12, -30)
        show('X%d z%d beds m<=12 j in [-30..0]' % (2 if z == 11 else 4, z), tab, 17, 9)

    # X5/X6: L-BU11G / L-BU12G discovery
    bad11 = bad12 = 0
    n = 0
    for w in range(2, 31):
        for t in range(0, w + 1):
            va = H(t, (w,), 12)
            vc = v(w, 12, t)
            vb = H(t, (w,), 13)
            vd = v(w, 13, t)
            n += 4
            if not (va == vc == lbu11g(t)):
                bad11 += 1
                print('  L-BU11G dev', w, t, va, vc, lbu11g(t))
            if not (vb == vd == lbu12g(t)):
                bad12 += 1
                print('  L-BU12G dev', w, t, vb, vd, lbu12g(t))
        H.cache_clear()
    print('== X5/X6 L-BU11G/L-BU12G: checks %d, bad %d / %d ==' % (n, bad11, bad12))
    # w=1 edges recorded for the bed typed proofs
    print('  w=1: v(1,12,t) t=0..1 = %d,%d ; v(1,13,t) = %d,%d'
          % (v(1, 12, 0), v(1, 12, 1), v(1, 13, 0), v(1, 13, 1)))

    # X7: sharpened C-PSF first probe on z0..z14
    def cpsf(w, R, d):
        L = 2 * ((w + 1) // 2)
        shift = 2 * (w // 2)
        if R < L:
            return 2 * (R % 2)
        return g1(d - shift) if w % 2 else f0(d - shift)

    bad = {}
    cnt = {}
    for z in range(0, 15):
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

    def typed_z11_pair(R, m, g):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z11_pair_claim(R - 1, m - 1, g + 1))
        else:
            kids.append(lbu11g(R - 1))       # token g+1 @ plane 12 (t<=w)
        if g >= 2:
            kids.append(z11_pair_claim(R - 1, m, g - 1))
        else:
            kids.append(z11_bed_claim(R - 1, m, R - 2 * m - 1))
        kids.append(1 ^ z10_pair_claim(R - 1, m, g))   # C -> z10 (K1299)
        return mexs(kids)

    def typed_z11_bed(R, m, j):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z11_pair_claim(R - 1, m - 1, 1))
        else:
            kids.append(lbu11g(R - 1))       # token 1 @ plane 12, t<=1
        kids.append(1 ^ z10_bed_claim(R - 1, m, j - 1))
        return mexs(kids)

    def typed_z12_pair(R, m, g):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z12_pair_claim(R - 1, m - 1, g + 1))
        else:
            kids.append(lbu12g(R - 1))      # token g+1 @ plane 13
        if g >= 2:
            kids.append(z12_pair_claim(R - 1, m, g - 1))
        else:
            kids.append(z12_bed_claim(R - 1, m, R - 2 * m - 1))
        kids.append(1 ^ z11_pair_claim(R - 1, m, g))   # C -> z11 (packet)
        return mexs(kids)

    def typed_z12_bed(R, m, j):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z12_pair_claim(R - 1, m - 1, 1))
        else:
            kids.append(lbu12g(R - 1))
        kids.append(1 ^ z11_bed_claim(R - 1, m, j - 1))
        return mexs(kids)

    stats = defaultdict(int)
    for z, tpair, tbed, pc, bc in [
            (11, typed_z11_pair, typed_z11_bed, z11_pair_claim, z11_bed_claim),
            (12, typed_z12_pair, typed_z12_bed, z12_pair_claim, z12_bed_claim)]:
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
