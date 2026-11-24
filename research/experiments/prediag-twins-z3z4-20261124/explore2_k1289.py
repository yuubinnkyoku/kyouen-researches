#!/usr/bin/env python3
"""explore2_k1289 (pre-declaration wide verification census; OBS for z5/z6).

  Y1  z3/z4 band wide census vs claims (m<=14, g<=25, k in
      [max(-30,-2m-g),0]): claim z3 = 2*[R odd] (R<=3) / g1(delta-2);
      z4 = 2*[R odd] (R<4) / f0(delta-4).
  Y2  z3/z4 beds wide census vs claims (m<=18, j in [-36..0]).
  Y3  z5/z6 band census vs sharpened C-PSF prediction (m<=10, g<=20,
      k in [max(-50,-2m-g),0])  [OBS, NO universal claim].
  Y4  z5/z6 beds census vs sharpened C-PSF prediction (m<=10,
      j in [-24..0])  [OBS].
  Y5  z5/z6 far-row tables at m=12 (k in [-12..-1], g in [1..18]) vs
      main-law prediction  [OBS].
  Y6  cross-engine canonical vs ordered subsample z3..z6.
  Y7  L-BU3G/L-BU4G wider sweep (w<=40) + closed-form crosscheck z in 4..6
      + L-BU5G/L-BU6G discovery probes (v(w,6,t) plane-5 law,
      v(w,7,t) plane-6 law)  [OBS for w=6,7 planes].
  Y8  sharpened C-PSF identity sweep on the dedup (R,delta) tables of the
      z0..z6 planes (the 320-cell box) + T-TWIN algebra identity d sweep.

Discovery/OBS census only, NO universal claims in this script.
"""
import sys
from collections import defaultdict
from engine_block import (H_canonical as HC, H_ordered as HO,
                          single_token as v)

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


def z3_pair(R, m, g):
    return 2 * (R % 2) if R <= 3 else g1(R - 2 * m - 2)


def z3_bed(R, m, j):
    return 2 * (R % 2) if R <= 3 else g1(j - 2)


def z4_pair(R, m, g):
    return 2 * (R % 2) if R < 4 else f0(R - 2 * m - 4)


def z4_bed(R, m, j):
    return 2 * (R % 2) if R < 4 else f0(j - 4)


def cpsf(w, R, d):
    L = 2 * ((w + 1) // 2)
    shift = 2 * (w // 2)
    if R < L:
        return 2 * (R % 2)
    return g1(d - shift) if w % 2 else f0(d - shift)


def pairX(z, k, m, g):
    R = 2 * m + g + k
    return HC(R, tuple(sorted((m + g, m), reverse=True)), z)


def main():
    tot = defaultdict(int)
    bad = defaultdict(int)

    # Y1: z3/z4 band wide
    for (z, fn, tag) in [(3, z3_pair, 'Y1z3'), (4, z4_pair, 'Y1z4')]:
        for m in range(1, 15):
            for g in range(1, 26):
                for k in range(max(-30, -2 * m - g), 1):
                    R = 2 * m + g + k
                    h = pairX(z, k, m, g)
                    e = fn(R, m, g)
                    tot[tag] += 1
                    if h != e:
                        bad[tag] += 1
                        if bad[tag] <= 5:
                            print('  %s dev m=%d g=%d k=%d R=%d h=%d e=%d'
                                  % (tag, m, g, k, R, h, e))
            HC.cache_clear()
        print('== %s: %d cells, bad %d ==' % (tag, tot[tag], bad[tag]))

    # Y2: z3/z4 beds wide
    for (z, fn, tag) in [(3, z3_bed, 'Y2z3'), (4, z4_bed, 'Y2z4')]:
        for m in range(1, 19):
            for j in range(-36, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = HC(R, (m, m), z)
                e = fn(R, m, j)
                tot[tag] += 1
                if h != e:
                    bad[tag] += 1
                    if bad[tag] <= 5:
                        print('  %s dev m=%d j=%d R=%d h=%d e=%d'
                              % (tag, m, j, R, h, e))
            HC.cache_clear()
        print('== %s: %d cells, bad %d ==' % (tag, tot[tag], bad[tag]))

    # Y3/Y4/Y5: z5/z6 OBS
    for (z, tag) in [(5, 'Y3z5'), (6, 'Y3z6')]:
        for m in range(1, 11):
            for g in range(1, 21):
                for k in range(max(-50, -2 * m - g), 1):
                    R = 2 * m + g + k
                    d = R - 2 * m
                    h = pairX(z, k, m, g)
                    e = cpsf(z, R, d)
                    tot[tag] += 1
                    if h != e:
                        bad[tag] += 1
                        if bad[tag] <= 5:
                            print('  %s dev m=%d g=%d k=%d h=%d e=%d'
                                  % (tag, m, g, k, h, e))
            HC.cache_clear()
        print('== %s (OBS): %d cells, bad %d ==' % (tag, tot[tag], bad[tag]))
    for (z, tag) in [(5, 'Y4z5'), (6, 'Y4z6')]:
        for m in range(1, 11):
            for j in range(-24, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = HC(R, (m, m), z)
                e = cpsf(z, R, j)
                tot[tag] += 1
                if h != e:
                    bad[tag] += 1
                    if bad[tag] <= 5:
                        print('  %s dev m=%d j=%d h=%d e=%d' % (tag, m, j, h, e))
            HC.cache_clear()
        print('== %s (OBS): %d cells, bad %d ==' % (tag, tot[tag], bad[tag]))
    for (z, fn, tag) in [(5, lambda d: g1(d - 4), 'Y5z5'),
                         (6, lambda d: f0(d - 6), 'Y5z6')]:
        for k in range(-12, 0):
            for g in range(1, 19):
                R = 24 + g + k
                if R < 0:
                    continue
                h = pairX(z, k, 12, g)
                e = fn(R - 24)
                tot[tag] += 1
                if h != e:
                    bad[tag] += 1
                    if bad[tag] <= 5:
                        print('  %s dev k=%d g=%d h=%d e=%d' % (tag, k, g, h, e))
            HC.cache_clear()
        print('== %s far-row m=12 (OBS): %d cells, bad %d =='
              % (tag, tot[tag], bad[tag]))

    # Y6: cross-engine z3..z6 subsample
    for z in (3, 4, 5, 6):
        t = b = 0
        for m in range(1, 7):
            for g in range(1, 10):
                for k in range(max(-8, -2 * m - g), 1):
                    R = 2 * m + g + k
                    X = tuple(sorted((m + g, m), reverse=True))
                    t += 1
                    if HC(R, X, z) != HO(R, X, z):
                        b += 1
            HC.cache_clear(); HO.cache_clear()
        print('== Y6 z=%d pairs cross-engine: %d cells, mismatch %d =='
              % (z, t, b))

    # Y7: L-BU3G/L-BU4G wider + L-BU5G/L-BU6G discovery + closed-form cross
    laws = {4: lambda t: 2 * (t % 2) if t <= 3 else g1(t - 2),
            5: lambda t: 2 * (t % 2) if t < 4 else f0(t - 4),
            6: lambda t: 2 * (t % 2) if t < 6 else g1(t - 4),
            7: lambda t: 2 * (t % 2) if t < 6 else f0(t - 6)}
    for z in (4, 5, 6, 7):
        b = n = 0
        for w in range(2, 41):
            for t in range(0, w + 1):
                hs = HC(t, (w,), z)
                cf = v(w, z, t) if (w, z, t) != (0,) else None
                n += 1
                law = laws[z](t)
                # planes z=6,7 are discovery probes (OBS); z=4,5 are the
                # L-BU3G/L-BU4G lemma checks
                if hs != law or (cf is not None and hs != cf):
                    b += 1
                    if b <= 5:
                        print('  Y7 dev z=%d w=%d t=%d h=%d law=%d cf=%s'
                              % (z, w, t, hs, law, cf))
            HC.cache_clear()
        print('== Y7 z=%d plane-token sweep: %d cells, bad %d%s =='
              % (z, n, b, ' (OBS)' if z in (6, 7) else ''))

    # Y8: T-TWIN algebra identity + sharpened C-PSF dedup sweep z0..z6
    b = 0
    for d in range(-260, 261):
        if d == 1:
            if g1(d) != 2 or f0(d) != 2:
                b += 1
        elif g1(d) != (1 ^ f0(d)):
            b += 1
    print('== Y8 T-TWIN identity d in [-260..260]: bad %d ==' % b)
    for z in range(0, 7):
        tab = defaultdict(set)
        for m in range(1, 11):
            for g in range(1, 21):
                for k in range(max(-50, -2 * m - g), 1):
                    R = 2 * m + g + k
                    if R < 0:
                        continue
                    tab[(R, R - 2 * m)].add(pairX(z, k, m, g))
            HC.cache_clear()
        mixed = sum(1 for s in tab.values() if len(s) > 1)
        bb = 0
        for (R, dd), vals in tab.items():
            c = cpsf(z, R, dd)
            for x in vals:
                if x != c:
                    bb += 1
        print('== Y8 z=%d dedup (R,delta) sweep: cells %d, mixed %d, cpsf bad %d =='
              % (z, len(tab), mixed, bb))


main()
