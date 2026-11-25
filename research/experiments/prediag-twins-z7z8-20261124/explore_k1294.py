#!/usr/bin/env python3
"""explore_k1294 (pre-declaration discovery census; K1290 kit syntax).

Discovery battery for the z7/z8 pre-diagonal twin layers (thickness 8)
and the plane-8/9 single-token uniformity lemmas, run BEFORE the
single-owner declaration:

  X1  z7 band (R, delta) table, m<=12, g<=25, all k<=0 in box: values
      depend only on (R, delta); low-R rows constant by parity (expected
      exception layer 2*[R odd] for R < L(7) = 8).
  X2  z7 beds (R, j) table, m<=12, j in [-30..0].
  X3  z4 band (R, delta) table (same box; expected layer for
      R < L(8) = 8, main f0(delta-8)).
  X4  z8 beds (same box as X2).
  X5  L-BU7G discovery: v(w,8,t) vs plane-7 law for w<=30
      (layer 2*[t odd] t<8, main g1(t-6)).
  X6  L-BU8G discovery: v(w,9,t) vs plane-8 law for w<=30
      (layer 2*[t odd] t<8, main f0(t-8)).
  X7  sharpened C-PSF first probe: z0..z10 planes, small box,
      layer = 2*[R odd] for R < 2*ceil(w/2), main = T_w(delta-2*floor(w/2)).
      (z9/z10 are NEW observation planes beyond the K1290 X7 z<=8 probe.)
  X8  typed-children self-check: build z7/z8 pair/bed children ONLY from
      the claim tables (this package's z7/z8 claims + K1290 z5/z6 claims,
      which the C children reference) + the K0832 closed form through the
      L-BU7G/L-BU8G laws; mex == claim == engine on a discovery box
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


# published claims reused (K1290: z5/z6; needed as C-child inputs)
def z5_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 6 else g1(R - 2 * m - 4)


def z5_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 6 else g1(j - 4)


def z6_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 6 else f0(R - 2 * m - 6)


def z6_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 6 else f0(j - 6)


# the candidate claims of this package (T-PDT7/T-BDT7/T-PDT8/T-BDT8)
def z7_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 8 else g1(R - 2 * m - 6)


def z7_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 8 else g1(j - 6)


def z8_pair_claim(R, m, g):
    return 2 * (R % 2) if R < 8 else f0(R - 2 * m - 8)


def z8_bed_claim(R, m, j):
    return 2 * (R % 2) if R < 8 else f0(j - 8)


# candidate L-BU7G/L-BU8G laws (from the K0832 closed form; X5/X6 check)
def lbu7g(t):
    return 2 * (t % 2) if t < 8 else g1(t - 6)


def lbu8g(t):
    return 2 * (t % 2) if t < 8 else f0(t - 8)


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
    # X1/X3: z7/z8 band discovery tables
    for z in (7, 8):
        tab = band_table(z, 12, 25, -60)
        show('X%d z%d band m<=12 g<=25 k>=-60' % (1 if z == 7 else 3, z), tab, 13, 9)
    # X2/X4: z7/z8 bed discovery tables
    for z in (7, 8):
        tab = bed_table(z, 12, -30)
        show('X%d z%d beds m<=12 j in [-30..0]' % (2 if z == 7 else 4, z), tab, 13, 9)

    # X5/X6: L-BU7G / L-BU8G discovery
    bad7 = bad8 = 0
    n = 0
    for w in range(2, 31):
        for t in range(0, w + 1):
            va = H(t, (w,), 8)
            vc = v(w, 8, t)
            vb = H(t, (w,), 9)
            vd = v(w, 9, t)
            n += 4
            if not (va == vc == lbu7g(t)):
                bad7 += 1
                print('  L-BU7G dev', w, t, va, vc, lbu7g(t))
            if not (vb == vd == lbu8g(t)):
                bad8 += 1
                print('  L-BU8G dev', w, t, vb, vd, lbu8g(t))
        H.cache_clear()
    print('== X5/X6 L-BU7G/L-BU8G: checks %d, bad %d / %d ==' % (n, bad7, bad8))
    # w=1 edges recorded for the bed typed proofs
    print('  w=1: v(1,8,t) t=0..1 = %d,%d ; v(1,9,t) = %d,%d'
          % (v(1, 8, 0), v(1, 8, 1), v(1, 9, 0), v(1, 9, 1)))

    # X7: sharpened C-PSF first probe on z0..z10
    def cpsf(w, R, d):
        L = 2 * ((w + 1) // 2)
        shift = 2 * (w // 2)
        if R < L:
            return 2 * (R % 2)
        return g1(d - shift) if w % 2 else f0(d - shift)

    bad = {}
    cnt = {}
    for z in range(0, 11):
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

    def typed_z7_pair(R, m, g):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z7_pair_claim(R - 1, m - 1, g + 1))
        else:
            kids.append(lbu7g(R - 1))       # token g+1 @ plane 8 (t<=w)
        if g >= 2:
            kids.append(z7_pair_claim(R - 1, m, g - 1))
        else:
            kids.append(z7_bed_claim(R - 1, m, R - 2 * m - 1))
        kids.append(1 ^ z6_pair_claim(R - 1, m, g))   # C -> z6 (K1290)
        return mexs(kids)

    def typed_z7_bed(R, m, j):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z7_pair_claim(R - 1, m - 1, 1))
        else:
            kids.append(lbu7g(R - 1))       # token 1 @ plane 8, t<=1
        kids.append(1 ^ z6_bed_claim(R - 1, m, j - 1))
        return mexs(kids)

    def typed_z8_pair(R, m, g):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z8_pair_claim(R - 1, m - 1, g + 1))
        else:
            kids.append(lbu8g(R - 1))       # token g+1 @ plane 9
        if g >= 2:
            kids.append(z8_pair_claim(R - 1, m, g - 1))
        else:
            kids.append(z8_bed_claim(R - 1, m, R - 2 * m - 1))
        kids.append(1 ^ z7_pair_claim(R - 1, m, g))   # C -> z7 (packet)
        return mexs(kids)

    def typed_z8_bed(R, m, j):
        if R == 0:
            return 0
        kids = []
        if m >= 2:
            kids.append(z8_pair_claim(R - 1, m - 1, 1))
        else:
            kids.append(lbu8g(R - 1))
        kids.append(1 ^ z7_bed_claim(R - 1, m, j - 1))
        return mexs(kids)

    stats = defaultdict(int)
    for z, tpair, tbed, pc, bc in [
            (7, typed_z7_pair, typed_z7_bed, z7_pair_claim, z7_bed_claim),
            (8, typed_z8_pair, typed_z8_bed, z8_pair_claim, z8_bed_claim)]:
        for m in range(1, 11):
            for g in range(1, 15):
                for k in range(max(-14, -2 * m - g), 1):
                    R = 2 * m + g + k
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
