#!/usr/bin/env python3
"""explore_k1303 (pre-declaration discovery; NOT published yet).

General-w candidate law to stress-test BEFORE declaring:

  CPSF-GEN(w): for pairs (m, m+g), band k = R-2m-g <= 0, delta = R-2m:
        H(R; (m,m+g); w) = 2*[R odd]      (R <  L(w) = 2*ceil(w/2))
                           T_w(delta - s(w))  (R >= L(w)), s(w)=2*floor(w/2)
  BED-GEN(w):  for beds (m,m), j = R-2m <= 0:
        H(R; (m,m); w)    = 2*[R odd]      (R <  L(w))
                           T_w(j - s(w))      (R >= L(w))
  T_w = g1 (w odd) / f0 (w even); L(0)=0, s(0)=0.
  L-BU-GEN(w): v(x, w+1, t) = 2*[t odd] (t < L(w)); T_w(t - s(w)) (t >= L(w)),
        for all x >= 1, 0 <= t <= x.

The typed self-check builds children ONLY from CPSF-GEN/BED-GEN tables and
the K0832 closed form (plane w-1 reads are CPSF-GEN(w-1) claims), i.e. it
machine-checks the general induction arithmetic pointwise.

Batteries:
  X1  band census planes w=0..16 (m<=12, g<=25, k in [max(-60,-2m-g),0])
  X2  bed census planes w=0..16 (m<=14, j in [-30..0])
  X3  typed general self-check planes w=0..16 (m<=10, g<=14, k>=-14,
      beds j>=-16): typed mex == claim == engine
  X4  seam/crossing rows R in {L-2..L+4} exhaustive (m<=26, g<=40)
      planes w=0..16
  X5  L-BU-GEN closed form vs cpsfgen(w,t,t) vs canonical engine,
      w<=30, x<=34 (covers the 3 closed-form regions)
  X6  NEW planes w=17..20 far-field probes (m<=12, g<=16, k>=-40)
  X7  dedup (R,delta) sweep z=0..20
  X8  cross-engine ordered vs canonical subsample
"""
import json, sys, time
from engine_block import H_canonical, H_ordered, single_token as v, vC, vO

def mexs(vals):
    s = set(vals)
    x = 0
    while x in s:
        x += 1
    return x

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

def Lw(w):
    return 2 * ((w + 1) // 2)

def sw(w):
    return 2 * (w // 2)

def Tw(w, d):
    return g1(d) if w % 2 else f0(d)

def cpsfG(w, R, d):
    if R < Lw(w):
        return 2 * (R % 2)
    return Tw(w, d - sw(w))

def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()

def pairX(z, k, m, g):
    R = 2 * m + g + k
    return H_canonical(R, tuple(sorted([m, m + g], reverse=True)), z)

def typed_pair(R, m, g, w):
    """mex of children valued ONLY by CPSF-GEN(w)/BED-GEN(w)/CPSF-GEN(w-1)/closed form."""
    if R == 0:
        return 0
    kids = []
    # lower token: fall (m>=2) / B-exit (m=1 -> token g+1 @ plane w+1, t<=g+1)
    if m >= 2:
        kids.append(cpsfG(w, R - 1, (R - 1) - 2 * (m - 1)))
    else:
        t = R - 1
        assert t <= g + 1, (w, m, g, R)
        kids.append(v(g + 1, w + 1, t))
    # upper token: compress (g>=2) / corner bed (g=1)
    kids.append(cpsfG(w, R - 1, (R - 1) - 2 * m))
    # C move: plane w-1 same pair, budget R-1
    if w >= 1:
        kids.append(1 ^ cpsfG(w - 1, R - 1, (R - 1) - 2 * m))
    return mexs(kids)

def typed_bed(R, m, j, w):
    if R == 0:
        return 0
    assert j == R - 2 * m and j <= 0
    kids = []
    if m >= 2:
        kids.append(cpsfG(w, R - 1, (R - 1) - 2 * (m - 1)))
    else:
        t = R - 1  # = j+1 <= 1
        assert t <= 1
        kids.append(v(1, w + 1, t))
    if w >= 1:
        kids.append(1 ^ cpsfG(w - 1, R - 1, j - 1))
    return mexs(kids)

def main():
    t0 = time.time()
    res = {}
    bad_total = 0

    # X1: band census planes 0..16
    X1 = {}
    for w in range(0, 17):
        n = 0; bad = []
        for m in range(1, 13):
            for g in range(1, 26):
                for k in range(max(-60, -2 * m - g), 1):
                    R = 2 * m + g + k
                    h = pairX(w, k, m, g)
                    exp = cpsfG(w, R, R - 2 * m)
                    n += 1
                    if h != exp and len(bad) < 8:
                        bad.append([m, g, k, R, h, exp])
            clear()
        X1[w] = {'points': n, 'bad': bad}
        bad_total += len(bad)
        clear()
    res['X1'] = X1

    # X2: bed census planes 0..16
    X2 = {}
    for w in range(0, 17):
        n = 0; bad = []
        for m in range(1, 15):
            for j in range(-30, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = H_canonical(R, (m, m), w)
                exp = cpsfG(w, R, j)
                n += 1
                if h != exp and len(bad) < 8:
                    bad.append([m, j, R, h, exp])
            clear()
        X2[w] = {'points': n, 'bad': bad}
        bad_total += len(bad)
    res['X2'] = X2

    # X3: typed general self-check planes 0..16
    X3 = {}
    for w in range(0, 17):
        n = 0; bad = []
        for m in range(1, 11):
            for g in range(1, 15):
                for k in range(max(-14, -2 * m - g), 1):
                    R = 2 * m + g + k
                    exp = cpsfG(w, R, R - 2 * m)
                    mx = typed_pair(R, m, g, w)
                    h = pairX(w, k, m, g)
                    n += 1
                    if not (mx == exp == h) and len(bad) < 8:
                        bad.append([m, g, k, R, exp, mx, h])
            for j in range(-16, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                exp = cpsfG(w, R, j)
                mx = typed_bed(R, m, j, w)
                h = H_canonical(R, (m, m), w)
                n += 1
                if not (mx == exp == h) and len(bad) < 8:
                    bad.append([m, j, R, exp, mx, h])
            clear()
        X3[w] = {'points': n, 'bad': bad}
        bad_total += len(bad)
        clear()
    res['X3'] = X3

    # X4: seam/crossing rows exhaustive planes 0..16
    X4 = {}
    for w in range(0, 17):
        L = Lw(w)
        n = 0; bad = []
        for R in range(max(0, L - 2), L + 5):
            for m in range(1, 27):
                for g in range(1, 41):
                    k = R - 2 * m - g
                    if k < -40 or k > 0:
                        continue
                    h = pairX(w, k, m, g)
                    exp = cpsfG(w, R, R - 2 * m)
                    n += 1
                    if h != exp and len(bad) < 8:
                        bad.append([R, m, g, k, h, exp])
                clear()
                for j in range(-30, 1):
                    Rb = 2 * m + j
                    if Rb < 0 or not (L - 2 <= Rb <= L + 4):
                        continue
                    h = H_canonical(Rb, (m, m), w)
                    exp = cpsfG(w, Rb, j)
                    n += 1
                    if h != exp and len(bad) < 8:
                        bad.append([Rb, m, j, h, exp])
                clear()
        X4[w] = {'points': n, 'bad': bad, 'L': L}
        bad_total += len(bad)
    res['X4'] = X4

    # X5: L-BU-GEN closed form vs cpsfG(w,t,t) vs engine, w<=30, x<=34
    X5 = {'points': 0, 'bad': []}
    for w in range(0, 31):
        for x in range(1, 35):
            for t in range(0, min(x, 36) + 1):
                cf = v(x, w + 1, t)
                want = cpsfG(w, t, t)
                hc = vC(x, w + 1, t)
                X5['points'] += 1
                if not (cf == want == hc) and len(X5['bad']) < 8:
                    X5['bad'].append([w, x, t, cf, want, hc])
            clear()
    bad_total += len(X5['bad'])
    res['X5'] = X5

    # X6: NEW planes w=17..20 far-field probes
    X6 = {}
    for w in range(17, 21):
        n = 0; bad = []
        for m in range(1, 13):
            for g in range(1, 17):
                for k in range(max(-40, -2 * m - g), 1):
                    R = 2 * m + g + k
                    if R < 0:
                        continue
                    h = pairX(w, k, m, g)
                    exp = cpsfG(w, R, R - 2 * m)
                    n += 1
                    if h != exp and len(bad) < 8:
                        bad.append([m, g, k, R, h, exp])
            for j in range(-24, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = H_canonical(R, (m, m), w)
                exp = cpsfG(w, R, j)
                n += 1
                if h != exp and len(bad) < 8:
                    bad.append([m, j, R, h, exp])
            clear()
        X6[w] = {'points': n, 'bad': bad}
        bad_total += len(bad)
    res['X6'] = X6

    # X7: dedup (R,delta) sweep z=0..20
    X7 = {}
    for z in range(0, 21):
        tab = {}
        for m in range(1, 11):
            for g in range(1, 21):
                for k in range(max(-50, -2 * m - g), 1):
                    R = 2 * m + g + k
                    if R < 0:
                        continue
                    d = R - 2 * m
                    h = pairX(z, k, m, g)
                    tab.setdefault((R, d), set()).add(h)
            clear()
        mixed = sum(1 for s in tab.values() if len(s) > 1)
        bb = 0
        for (R, dd), vals in tab.items():
            c = cpsfG(z, R, dd)
            for x in vals:
                if x != c:
                    bb += 1
        X7[z] = {'cells': len(tab), 'mixed': mixed, 'cpsf_bad': bb}
        bad_total += bb
        clear()
    res['X7'] = X7

    # X8: cross-engine subsample
    X8 = {'points': 0, 'bad': []}
    for z in (0, 5, 11, 13, 16, 19):
        for m in range(1, 8):
            for g in range(1, 11):
                for k in range(max(-8, -2 * m - g), 1):
                    R = 2 * m + g + k
                    X = tuple(sorted([m, m + g], reverse=True))
                    hc = H_canonical(R, X, z)
                    ho = H_ordered(R, X, z)
                    X8['points'] += 1
                    if hc != ho and len(X8['bad']) < 8:
                        X8['bad'].append([z, m, g, k, hc, ho])
                clear()
    bad_total += len(X8['bad'])
    res['X8'] = X8

    res['bad_total'] = bad_total
    res['elapsed_s'] = round(time.time() - t0, 1)
    print(json.dumps(res, indent=1, sort_keys=True))

main()
