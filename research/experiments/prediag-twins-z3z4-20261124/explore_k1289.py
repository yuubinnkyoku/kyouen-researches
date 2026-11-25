#!/usr/bin/env python3
"""explore_k1289 (pre-declaration discovery census; K1288 kit syntax).

Discovery battery for the z3/z4 pre-diagonal twin layers and the plane-4/5
single-token uniformity lemmas, run BEFORE the single-owner declaration:

  X1  z3 band (R, delta) table, m<=12, g<=25, all k<=0 in box: values
      depend only on (R, delta); low-R rows constant by parity.
  X2  z3 beds (R, j) table, m<=12, j in [-30..0].
  X3  z4 band (R, delta) table (same box as X1).
  X4  z4 beds (same box as X2).
  X5  L-BU3G discovery: v(w,4,t) vs plane-3 law for w<=30.
  X6  L-BU4G discovery: v(w,5,t) vs plane-4 law for w<=30.
  X7  sharpened C-PSF first probe: z0..z6 planes, small box,
      layer = 2*[R odd] for R < 2*ceil(w/2), main = T_w(delta-2*floor(w/2)).

Emphasis: discovery census only, NO universal claims in this script.
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


def plane3_law(t):
    return 2 * (t % 2) if t <= 3 else g1(t - 2)


def plane4_law(t):
    return 2 * (t % 2) if t < 4 else f0(t - 4)


def plane5_law(t):
    return 2 * (t % 2) if t < 6 else g1(t - 4)


def plane6_law(t):
    return 2 * (t % 2) if t < 6 else f0(t - 6)


def main():
    # X1/X3: z3/z4 band discovery tables
    for z in (3, 4):
        tab = band_table(z, 12, 25, -60)
        show('X%d z%d band m<=12 g<=25 k>=-60' % (1 if z == 3 else 3, z), tab, 9, 7)
    # X2/X4: z3/z4 bed discovery tables
    for z in (3, 4):
        tab = bed_table(z, 12, -30)
        show('X%d z%d beds m<=12 j in [-30..0]' % (2 if z == 3 else 4, z), tab, 9, 7)

    # X5/X6: L-BU3G / L-BU4G discovery
    bad3 = bad4 = 0
    n = 0
    for w in range(2, 31):
        for t in range(0, w + 1):
            va = H(t, (w,), 4)
            vc = v(w, 4, t)
            vb = H(t, (w,), 5)
            vd = v(w, 5, t)
            n += 4
            if w == 1:
                continue
            if not (va == vc == plane3_law(t)):
                bad3 += 1
                print('  L-BU3G dev', w, t, va, vc, plane3_law(t))
            if not (vb == vd == plane4_law(t)):
                bad4 += 1
                print('  L-BU4G dev', w, t, vb, vd, plane4_law(t))
        H.cache_clear()
    print('== X5/X6 L-BU3G/L-BU4G: checks %d, bad %d / %d ==' % (n, bad3, bad4))
    # w=1 edges recorded for the bed typed proofs
    print('  w=1: v(1,4,t) t=0..1 = %d,%d ; v(1,5,t) = %d,%d'
          % (v(1, 4, 0), v(1, 4, 1), v(1, 5, 0), v(1, 5, 1)))

    # X7: sharpened C-PSF first probe on z0..z6
    def cpsf(w, R, d):
        L = 2 * ((w + 1) // 2)
        shift = 2 * (w // 2)
        if R < L:
            return 2 * (R % 2)
        return g1(d - shift) if w % 2 else f0(d - shift)

    bad = {}
    cnt = {}
    for z in range(0, 7):
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


main()
