#!/usr/bin/env python3
"""explore2_k1303: pre-declaration discovery part 2 (wide + symbolic).

  Y1  symbolic mex-table meta-check of the hand proof's two MAIN tables:
      odd w : mex{g1(d+1), g1(d-1), 1^f0(d-1) (3 at d=2)} == g1(d)
      even w: mex{f0(d+1), f0(d-1), 1^g1(d+1) (3 at d=0)} == f0(d)
      over d in [-3000..3000] (60,001 cells x 2)
  Y2  L-BU-GEN wide: closed form == cpsfG(w,t,t) == canonical engine,
      w<=36, x<=48 (all t<=x)
  Y3  core/nucleation far cells: delta-s(w) in {0,1,2,3} at m<=48 on
      planes w in {3,9,13,16} vs engine (bed cols j-s(w) in {0,1,2})
  Y4  layer-row option-set constancy: for odd w in {3..21}, rows R=w and
      R=w+1: engine C-child reads 1^f0(delta-w) constants (m<=20)
"""
import json, time
from engine_block import H_canonical, single_token as v, vC

def mexs(vals):
    s = set(vals); x = 0
    while x in s: x += 1
    return x

def IND(b): return 1 if b else 0

def f0(d):
    if d == 1: return 2
    if d <= 0: return IND(d % 2 == 1)
    return IND(d % 2 == 0)

def g1(d):
    if d == 1: return 2
    if d <= 0: return IND(d % 2 == 0)
    return IND(d % 2 == 1)

def Lw(w): return 2 * ((w + 1) // 2)
def sw(w): return 2 * (w // 2)
def Tw(w, d): return g1(d) if w % 2 else f0(d)
def cpsfG(w, R, d):
    if R < Lw(w): return 2 * (R % 2)
    return Tw(w, d - sw(w))

def clear():
    H_canonical.cache_clear()

def main():
    t0 = time.time()
    res = {}
    nb = 0
    # Y1 symbolic tables
    Y1 = {'points': 0, 'bad': []}
    for d in range(-3000, 3001):
        # odd w table
        opts = {g1(d + 1), g1(d - 1)}
        opts.add(3 if d == 2 else 1 ^ f0(d - 1))
        ok = mexs(opts) == g1(d)
        Y1['points'] += 1
        if not ok and len(Y1['bad']) < 6: Y1['bad'].append(['odd', d])
        # even w table
        opts = {f0(d + 1), f0(d - 1)}
        opts.add(3 if d == 0 else 1 ^ g1(d + 1))
        ok = mexs(opts) == f0(d)
        Y1['points'] += 1
        if not ok and len(Y1['bad']) < 6: Y1['bad'].append(['even', d])
    nb += len(Y1['bad'])
    res['Y1'] = Y1
    # Y2 wide L-BU-GEN
    Y2 = {'points': 0, 'bad': []}
    for w in range(0, 37):
        for x in range(1, 49):
            for t in range(0, x + 1):
                cf = v(x, w + 1, t)
                want = cpsfG(w, t, t)
                hc = vC(x, w + 1, t)
                Y2['points'] += 1
                if not (cf == want == hc) and len(Y2['bad']) < 6:
                    Y2['bad'].append([w, x, t, cf, want, hc])
            clear()
    nb += len(Y2['bad'])
    res['Y2'] = Y2
    # Y3 core cells far
    Y3 = {'points': 0, 'bad': []}
    for w in (3, 9, 13, 16):
        s = sw(w)
        for m in range(1, 49):
            for dd in (0, 1, 2, 3):
                d = s + dd
                R = 2 * m + d
                # pair needs k<=0: choose g = d (k = 0)
                if d < 1:  # core d values are >= s+0 >= 2
                    continue
                g = d
                k = R - 2 * m - g
                if k != 0:
                    continue
                h = H_canonical(R, tuple(sorted([m, m + g], reverse=True)), w)
                exp = cpsfG(w, R, d)
                Y3['points'] += 1
                if h != exp and len(Y3['bad']) < 6:
                    Y3['bad'].append([w, m, 'pair', dd, h, exp])
            # bed core columns j-s(w) in {0,1,2} need j = s+jj <= 0:
            # impossible for s >= 2 with m<=48 beds (j = R-2m <= 46-2m);
            # covered instead by Y1/Y4 tables; nothing to probe here.
            clear()
    nb += len(Y3['bad'])
    res['Y3'] = Y3
    # Y4 seam constancy (odd w rows R=w, R=w+1): C child = 1^f0(delta-w)
    Y4 = {'points': 0, 'bad': []}
    for w in range(3, 22, 2):
        for R in (w, w + 1):
            for m in range(1, 21):
                for g in range(1, 12):
                    k = R - 2 * m - g
                    if k > 0 or k < -8:
                        continue
                    # C child computed by engine on plane w-1
                    c_eng = 1 ^ H_canonical(R - 1, tuple(sorted([m, m + g], reverse=True)), w - 1)
                    c_tab = 1 ^ cpsfG(w - 1, R - 1, (R - 1) - 2 * m)
                    h = H_canonical(R, tuple(sorted([m, m + g], reverse=True)), w)
                    exp = cpsfG(w, R, R - 2 * m)
                    Y4['points'] += 1
                    if not (c_eng == c_tab and h == exp) and len(Y4['bad']) < 6:
                        Y4['bad'].append([w, R, m, g, k, c_eng, c_tab, h, exp])
            clear()
    nb += len(Y4['bad'])
    res['Y4'] = Y4
    res['bad_total'] = nb
    res['elapsed_s'] = round(time.time() - t0, 1)
    print(json.dumps(res, indent=1, sort_keys=True))

main()
