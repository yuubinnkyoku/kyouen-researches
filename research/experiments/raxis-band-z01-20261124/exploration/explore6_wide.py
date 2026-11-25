#!/usr/bin/env python3
"""explore6_wide.py -- wide census for the z=0/z=1 R-axis band package.
O1: z=1 frontier classification (mixed->2, allm a>=3 ->2, (m,m)->0)
O2: z=1 d=2 law: mixed H = min(S,R)%2 ; allm a>=2 -> 0
O3: z=0 d=2 law: mixed H=1 iff (mult_min==1 or (m+1) in X) else 0 ;
    allm: a=1 -> v, a=2 -> 0, a=3 -> 1, a>=4 -> 0
O4: FB0 identity: restricted family (mult_min==1, others>=m+1, max>=m+2)
    at z=0,d=2 -> value 1 ; parent A-big child value v(S-1,0,2mu) == 0
O5: z=1 d=3 mixed: values in {1,2} (no 0); dumped table
O6: z=0 d=3 mixed table dump (law open)
O7: z>=2 band probe: collapse H == v(S,z,R) bads at R<=2m (and frontier R=2m+1)
T1-inputs census: for mixed X: A-big child (z=1) value == v(S-1,1,2mu)==1;
    C-child base H(2mu;X;0)==0; A-min child (z=1 d=2 row mu-1) == 0
Observation only. Engine sha-gated.
"""
import json, hashlib, sys, time
from functools import lru_cache
from itertools import combinations_with_replacement

ENGINE_SHA = hashlib.sha256(open('engine_block.py','rb').read()).hexdigest()
assert ENGINE_SHA == 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92', ENGINE_SHA
exec(open('engine_block.py').read())
v = single_token

def shapes(m, lo_tok, hi_tok, amax):
    for k in range(1, amax + 1):
        for c in combinations_with_replacement(range(lo_tok, hi_tok + 1), k):
            if c[0] == m:
                yield tuple(reversed(c))

def mixed_shapes(m, R, amax, cap=None):
    cap = R + 2 if cap is None else cap
    for X in shapes(m, m, cap, amax):
        if max(X) > m:
            yield X

def run():
    out = {'engine_sha': ENGINE_SHA}
    t0 = time.time()

    # ---- O2: z=1 d=2 ----
    o2 = {}
    for m in range(1, 9):
        R = 2 * m + 2
        bad = n = 0
        badex = []
        for X in mixed_shapes(m, R, 5):
            h = H_canonical(R, X, 1)
            pred = min(sum(X), R) % 2
            n += 1
            if h != pred:
                bad += 1
                if len(badex) < 5: badex.append([list(X), sum(X), h, pred])
        allm = []
        for a in range(1, 9):
            X = tuple([m] * a)
            h = H_canonical(R, X, 1)
            predv = v(m * a, 1, R) if a == 1 else 0
            allm.append([a, h, predv])
        o2['m%d' % m] = {'n': n, 'bad': bad, 'badex': badex, 'allm': allm}
        H_canonical.cache_clear(); H_ordered.cache_clear()
        print('O2 m=%d n=%d bad=%d allm_ok=%s' % (m, n, bad,
              all(r[1] == r[2] for r in allm)), flush=True)
    out['O2'] = o2

    # ---- O3: z=0 d=2 ----
    o3 = {}
    for m in range(1, 9):
        R = 2 * m + 2
        bad = n = 0
        badex = []
        for X in mixed_shapes(m, R, 5):
            h = H_canonical(R, X, 0)
            mult = X.count(m)
            pred = 1 if (mult == 1 or (m + 1) in X) else 0
            n += 1
            if h != pred:
                bad += 1
                if len(badex) < 5: badex.append([list(X), sum(X), h, pred])
        allm = []
        for a in range(1, 9):
            X = tuple([m] * a)
            h = H_canonical(R, X, 0)
            pred = v(m * a, 0, R) if a == 1 else (0 if a != 3 else 1)
            allm.append([a, h, pred])
        o3['m%d' % m] = {'n': n, 'bad': bad, 'badex': badex, 'allm': allm}
        H_canonical.cache_clear(); H_ordered.cache_clear()
        print('O3 m=%d n=%d bad=%d allm_ok=%s' % (m, n, bad,
              all(r[1] == r[2] for r in allm)), flush=True)
    out['O3'] = o3

    # ---- O4: FB0 identity (restricted family) ----
    o4 = {'n': 0, 'bad': 0, 'cbad': 0, 'badex': []}
    for mu in range(2, 9):
        Rp = 2 * mu + 1
        for X in mixed_shapes(mu, Rp, 5):
            S = sum(X)
            c = v(S - 1, 0, Rp - 1)
            if c != 0: o4['cbad'] += 1
            Xp = list(X); Xp.remove(mu); Xp.append(mu - 1); Xp.sort(reverse=True)
            Dp = H_canonical(Rp - 1, tuple(Xp), 0)
            o4['n'] += 1
            if Dp != 1 - c:
                o4['bad'] += 1
                if len(o4['badex']) < 5: o4['badex'].append([mu, list(X), c, Dp])
        H_canonical.cache_clear(); H_ordered.cache_clear()
    print('O4 n=%d bad=%d cbad=%d' % (o4['n'], o4['bad'], o4['cbad']), flush=True)
    out['O4'] = o4

    # ---- O1 + T1-inputs: z=1 frontier ----
    o1 = {}
    for mu in range(2, 9):
        Rp = 2 * mu + 1
        n = bad = 0
        badex = []
        ibad = cbad = sbad = 0
        for X in mixed_shapes(mu, Rp, 5):
            S = sum(X)
            h = H_canonical(Rp, X, 1)
            n += 1
            if h != 2:
                bad += 1
                if len(badex) < 5: badex.append([list(X), h])
            # T1 inputs
            # A-big child: any token > mu, becomes mu-... child (2mu; X-1 on big; 1)
            b = max(X)
            Yb = list(X); Yb.remove(b); Yb.append(b - 1); Yb.sort(reverse=True)
            ab = H_canonical(Rp - 1, tuple(Yb), 1)
            if ab != v(S - 1, 1, Rp - 1) or ab != 1: ibad += 1
            cc = H_canonical(Rp - 1, X, 0)
            if cc != 0: cbad += 1
            Xm = list(X); Xm.remove(mu); Xm.append(mu - 1); Xm.sort(reverse=True)
            am = H_canonical(Rp - 1, tuple(Xm), 1)
            if am != 0: sbad += 1
        # allm
        allm_bad = []
        for a in range(1, 9):
            X = tuple([mu] * a)
            h = H_canonical(Rp, X, 1)
            pred = v(mu, 1, Rp) if a == 1 else (0 if a == 2 else 2)
            if h != pred: allm_bad.append([a, h, pred])
        o1['mu%d' % mu] = {'n': n, 'bad': bad, 'ibad': ibad, 'cbad': cbad,
                           'sbad': sbad, 'badex': badex, 'allm_bad': allm_bad}
        H_canonical.cache_clear(); H_ordered.cache_clear()
        print('O1 mu=%d n=%d bad=%d ibad=%d cbad=%d sbad=%d allm_bad=%s' %
              (mu, n, bad, ibad, cbad, sbad, allm_bad), flush=True)
    out['O1'] = o1

    # ---- O5: z=1 d=3 mixed no-0, with feature dump ----
    o5 = {}
    for m in range(2, 7):
        R = 2 * m + 3
        zeros = vals = 0
        hist = {}
        rows = []
        for X in mixed_shapes(m, R, 5):
            h = H_canonical(R, X, 1)
            hist[h] = hist.get(h, 0) + 1
            if h == 0: zeros += 1
            vals += 1
            if len(X) <= 4:
                rows.append([list(X), sum(X), h])
        o5['m%d' % m] = {'n': vals, 'zeros': zeros, 'hist': hist, 'table': rows}
        H_canonical.cache_clear(); H_ordered.cache_clear()
        print('O5 m=%d n=%d zeros=%d hist=%s' % (m, vals, zeros, hist), flush=True)
    out['O5'] = o5

    # ---- O6: z=0 d=3 table (m=2,3) ----
    o6 = {}
    for m in (2, 3):
        R = 2 * m + 3
        hist = {}
        rows = []
        for X in mixed_shapes(m, R, 4):
            h = H_canonical(R, X, 0)
            hist[h] = hist.get(h, 0) + 1
            rows.append([list(X), sum(X), h])
        o6['m%d' % m] = {'hist': hist, 'table': rows}
        H_canonical.cache_clear(); H_ordered.cache_clear()
    out['O6'] = o6

    # ---- O7: z>=2 in-band collapse probe ----
    o7 = {}
    for z in (2, 3):
        for m in range(2, 6):
            bads = {}
            for R in range(max(m + z + 1, 2), 2 * m + 3):
                bad = n = 0
                for X in mixed_shapes(m, R, 3, cap=R + 2):
                    h = H_canonical(R, X, z)
                    n += 1
                    if h != v(sum(X), z, R): bad += 1
                bads[R] = [n, bad]
                H_canonical.cache_clear(); H_ordered.cache_clear()
            o7['z%d_m%d' % (z, m)] = bads
            print('O7 z=%d m=%d' % (z, m), bads, flush=True)
    out['O7'] = o7

    out['elapsed_s'] = round(time.time() - t0, 1)
    json.dump(out, open('explore6_wide.json', 'w'), indent=1)
    print('done in %.1fs; engine_sha=%s' % (out['elapsed_s'], ENGINE_SHA))

run()
