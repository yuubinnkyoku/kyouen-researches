#!/usr/bin/env python3
"""Pre-declaration exploration for the z=9 slice (min>=6 row of the
critical strip; observation HEAD 190820c7, K1276 = published z=8 slice).
Engine: pinned block cut from the SEVEN published machines (K1264/K1268/
K1271/K1272/K1273/K1274/K1275), sha-gated to bd5f22e4... (2,508 bytes).
All results below are exploration observations recorded BEFORE the
declaration note is written; the declaration will disclose them fully.

Blocks:
  P1  F9 full-decomposition sweep: s in {0} u {3..40}, all decompositions
      into 1..4 tokens >=3 (expected 3,657): s-only table + deviant
      record vs v(s+1,9,11)
  P2  G9 / E9 same 330 census family: s-only tables + deviant
      decomposition sets vs v(s+2,9,12) / v(s+3,9,13)
  P2b E9 full-decomposition s-only re-confirmation: the E9 table over
      ALL 3,657 decompositions (s in {0} u {3..40}, tokens >=3)
  P3  D9 floored (tokens>=5): s in {0} u {5..40}, all decomps (1,650):
      s-only + table {6:0, else v(s+4,9,14)} (expect the single s=6
      DOWNWARD deviant; the D-rank collapse series D6/D7 -> D8(up) ->
      D9(down) direction flip)
  P3b D9 loose (tokens>=3) family: decomposition-dependence record
  P4  C9 floored (tokens>=6): s in {0} u {6..40} (1,078): s-only +
      table {6:2, else v(s+5,9,15)} (expect the single s=6 UPWARD
      deviant, same position as the published m=5 z=9 out-of-band
      witness (5,6))
  P4b B9 floored (tokens>=7): s in {0} u {7..40}: full-collapse check
      vs v(s+6,9,16) (the B-rank full-collapse cell candidate at z=9)
  P5  z=9 strip grid: m in {5..11} x 222 T-shapes (R=m+10): m>=6 full
      collapse expected; m=5 out-of-band (z*(5)=9), the single (5,6)
      separation expected
  P5b m=6 z=10 out-of-band record (z*(6)=10): 222 T-shapes (R=16):
      witness record (the next row's frontier)
  P5c m=5 z=9 out-of-band record: 222 T-shapes (R=15): the published
      (5,6) separation re-recorded
  P6  base m=6 option-set structure: 33 shapes: opts subset of
      {A'=v(S-1,9,15), c'=1^v(S,8,15), C9t(S-6)}; a=6 child ==
      C9t(S-6) (the s=6 deviant absorption observed at face value);
      parent mex == v(S,9,16)
  P7  induction option-set identity: m in {7..10} x 33 shapes:
      opts == {v(S-1,9,m+9), 1^v(S,8,m+9)}; parent mex == v(S,9,m+10)
  P7b fixed-seed (20261127) random deep PRE-RUN (the declared D6 uses
      a different fixed seed declared in the note): m in {6..11} x 15
      shapes at z=9, R=m+10
  P8  cell-recursion option-set structures over the FULL families
      (mismatch counts, ordered child option sets vs arithmetic
      expectation sets):
      F9 {v(s,10,10), v(s,9,10), 1^F8t(s)};
      G9 {F9t(s), v(s+1,9,11), 1^G8t(s)};
      E9 CONDITIONAL {G9t(s), 1^E8t(s)} + ({v(s+2,9,12)}: some Y
         token >= 4), plus the UNCONDITIONAL form mismatch count
         over the same family (z=8 E8 broke at Y=(3,3); z=9 status
         pre-established by this machine);
      D9 {v(s+3,9,13), E9t(s), 1^D8t(s)};
      C9 {v(s+4,9,14), D9t(s), 1^v(s+5,8,14)};
      B9 {v(s+5,9,15), C9t(s), 1^v(s+6,8,15)}
  P9  z=10 next-lane census (observation only; registered open):
      F10/G10/E10 (330), D10 floored 126 / loose 330, C10 floored 70,
      B10 floored 35, A10 floored (min=7 rung; tokens 8..9), z=10
      strip m in {6..11} x 96 collapse record (m=6 out-of-band)
  P10 cross-check vs the published K1276 audit z9_cells census
      table_s20 (published audit.json sha256 84605d3b41eb54fa8663c2
      4403dffb5ff36edd1faac7735df3c5d0cd6f885dc1): the published
      census families are subfamilies of the probe sweeps (bounded
      token ranges vs all tokens >= floor), so every published
      table_s20 entry must be reproduced by the probe tables:
      match=True expected
"""
import json, hashlib, os, sys
from functools import lru_cache
from itertools import combinations_with_replacement

sys.setrecursionlimit(1_000_000)

def cut_k1264(text):
    lines = text.split('\n'); s = None
    for i, ln in enumerate(lines):
        if ln == 'def mex(values):': s = i; break
    e = None
    for j in range(s, len(lines)):
        if lines[j].startswith('SELF_SHA = hashlib'): e = j; break
    block = lines[s:e]
    while block and block[-1].strip() == '': block.pop()
    return '\n'.join(block) + '\n'

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC1 = os.path.join(BASE, 'generalx-min-token-lowr-staircase-20261123', 'verify_min_token_staircase.py')
SRC1_PIN = '108fdd65a96588b32cfd64503cf2a22f999d6e4eefded775bb6fda32568e69fa'
ENGINE_PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'

data = open(SRC1, 'rb').read()
assert hashlib.sha256(data).hexdigest() == SRC1_PIN, 'K1264 verifier sha mismatch'
engine = cut_k1264(data.decode('utf-8'))
assert hashlib.sha256(engine.encode('utf-8')).hexdigest() == ENGINE_PIN, 'engine pin mismatch'
print('engine block sha256 OK:', ENGINE_PIN)
exec(engine)

def clear_engines():
    H_ordered.cache_clear(); H_canonical.cache_clear()

def decomps(s, tmin, amax=4):
    if s == 0: return [()]
    out = []
    for k in range(1, amax + 1):
        for c in combinations_with_replacement(range(tmin, s + 1), k):
            if sum(c) == s: out.append(c)
    return out

def Y_tokens(tmin, tmax):
    out = []
    for k in range(0, 5):
        out.extend(combinations_with_replacement(range(tmin, tmax + 1), k))
    return out

def T_shapes(m):
    out = [(m,)]
    out.extend((m, m + d) for d in range(15))
    out.extend((m, m + a, m + b) for a in range(9) for b in range(9))
    out.extend((m, m + a, m + b, m + c)
               for a in range(5) for b in range(5) for c in range(5))
    return out

def D33_shapes(m):
    out = [(m, m + d) for d in range(7)]
    out.extend((m, m + a, m + b) for a in range(5) for b in range(5))
    out.append(tuple(m + i for i in range(5)))
    return out

def census_shapes(m):
    out = [(m, m + d) for d in range(15)]
    out.extend((m, m + a, m + b) for a in range(9) for b in range(9))
    return out

def child_opts_ordered(X, z, R):
    opts = set()
    for i, w in enumerate(X):
        if w > 1:
            opts.add(H_ordered(R - 1, X[:i] + (w - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return opts

def am_child_value(X, m, z, R):
    for i, w in enumerate(X):
        if w == m:
            return H_ordered(R - 1, X[:i] + (m - 1,) + X[i + 1:], z)
    raise ValueError('no token == m')

# --------------------------------------------------------------------
# declared/expected z=9 closed forms (hand arithmetic; machine-checked
# below against BOTH engines), plus the published z=8 tables (K1276)
# --------------------------------------------------------------------
def F9t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1, 9: 0}.get(s, 2)

def G9t(s):
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 0, 9: 1}.get(s, 1)

def E9t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 2}.get(s, 0)

def D9t(s):
    return 0 if s == 6 else single_token(s + 4, 9, 14)

def C9t(s):
    return 2 if s == 6 else single_token(s + 5, 9, 15)

def B9t(s):
    return single_token(s + 6, 9, 16)

# published z=8 tables (K1276 declaration, verbatim semantics)
def F8t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1}.get(s, 0)

def G8t(s):
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 2}.get(s, 1)

def E8t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1}.get(s, 0)

def D8t(s):
    return 2 if s == 6 else single_token(s + 4, 8, 13)

res = {}

def sweep_cell(pre, R, z, tab, tmin, smax=40, svals=None, tag=''):
    """full-decomposition sweep of a cell H(R;pre+Y;z) over
    s in {0} u {tmin..smax} (or given svals), tokens >= tmin, arity 1..4"""
    pts = 0; badengine = 0; badtab = 0; dep = {}; details = []
    if svals is None:
        svals = [0] + list(range(tmin, smax + 1))
    total_decomps = 0
    for s in svals:
        for Y in decomps(s, tmin):
            X = pre + Y
            hc = H_canonical(R, X, z)
            ho = H_ordered(R, X, z)
            pts += 1
            total_decomps += 1
            if hc != ho:
                badengine += 1
                if len(details) < 20: details.append(('engine', s, Y, hc, ho))
            exp = tab(s)
            if hc != exp:
                badtab += 1
                if len(details) < 20: details.append(('table', s, Y, hc, exp))
            dep.setdefault(s, set()).add(hc)
            if pts % 400 == 0:
                clear_engines()
    decomp_dependent_s = sorted(s for s, v in dep.items() if len(v) > 1)
    clear_engines()
    return {'tag': tag, 'R': R, 'z': z, 'floor': tmin,
            'decomps': total_decomps, 'points': pts,
            'engine_bad': badengine, 'table_bad': badtab,
            'decomp_dependent_s': decomp_dependent_s,
            'table_s20': {str(s): sorted(v) for s, v in sorted(dep.items())
                           if s <= 20},
            'details': details}

print('== P1 F9 full-decomposition sweep ==', flush=True)
res['P1_F9'] = sweep_cell((1,), 11, 9, F9t, 3, tag='F9 full')
print(json.dumps({k: res['P1_F9'][k] for k in
                  ('decomps', 'points', 'engine_bad', 'table_bad',
                   'decomp_dependent_s')}), flush=True)

print('== P2 G9/E9 census family ==', flush=True)
fam330 = Y_tokens(3, 9)
def census_cell(pre, R, z, tab, dvoff, fam, tag):
    pts = 0; badengine = 0; badtab = 0; dep = {}; devs = []
    for Y in fam:
        s = sum(Y)
        X = pre + Y
        hc = H_canonical(R, X, z)
        ho = H_ordered(R, X, z)
        pts += 1
        if hc != ho:
            badengine += 1
        exp = tab(s)
        if hc != exp: badtab = badtab + 1
        dep.setdefault(s, set()).add(hc)
        if hc != single_token(s + dvoff, z, R):
            devs.append(list(Y))
        if pts % 400 == 0: clear_engines()
    decomp_dependent_s = sorted(s for s, v in dep.items() if len(v) > 1)
    clear_engines()
    return {'tag': tag, 'family': len(fam), 'engine_bad': badengine,
            'table_bad': badtab, 'decomp_dependent_s': decomp_dependent_s,
            'deviant_count': len(devs),
            'deviants_vs_collapse': devs[:40],
            'table_s20': {str(s): sorted(v) for s, v in sorted(dep.items())
                           if s <= 20}}
res['P2_G9'] = census_cell((2,), 12, 9, G9t, 2, fam330, 'G9 330')
res['P2_E9'] = census_cell((3,), 13, 9, E9t, 3, fam330, 'E9 330')
print(json.dumps({k: res['P2_G9'][k] for k in
                  ('family', 'engine_bad', 'table_bad', 'deviant_count',
                   'deviants_vs_collapse', 'decomp_dependent_s')}), flush=True)
print(json.dumps({k: res['P2_E9'][k] for k in
                  ('family', 'engine_bad', 'table_bad', 'deviant_count',
                   'deviants_vs_collapse', 'decomp_dependent_s')}), flush=True)

print('== P2b E9 full-decomposition re-confirmation ==', flush=True)
res['P2b_E9'] = sweep_cell((3,), 13, 9, E9t, 3, tag='E9 full')
print(json.dumps({k: res['P2b_E9'][k] for k in
                  ('decomps', 'engine_bad', 'table_bad',
                   'decomp_dependent_s')}), flush=True)

print('== P3 D9 floored sweep ==', flush=True)
res['P3_D9'] = sweep_cell((4,), 14, 9, D9t, 5, tag='D9 floored')
print(json.dumps({k: res['P3_D9'][k] for k in
                  ('decomps', 'engine_bad', 'table_bad',
                   'decomp_dependent_s')}), flush=True)

print('== P3b D9 loose ==', flush=True)
res['P3b_D9_loose'] = census_cell((4,), 14, 9, D9t, 4, fam330, 'D9 loose')
print(json.dumps({k: res['P3b_D9_loose'][k] for k in
                  ('family', 'engine_bad', 'table_bad', 'deviant_count',
                   'decomp_dependent_s')}), flush=True)

print('== P4 C9 floored sweep ==', flush=True)
res['P4_C9'] = sweep_cell((5,), 15, 9, C9t, 6, tag='C9 floored')
print(json.dumps({k: res['P4_C9'][k] for k in
                  ('decomps', 'engine_bad', 'table_bad',
                   'decomp_dependent_s')}), flush=True)

print('== P4b B9 floored sweep (full collapse) ==', flush=True)
res['P4b_B9'] = sweep_cell((6,), 16, 9, B9t, 7, tag='B9 floored')
print(json.dumps({k: res['P4b_B9'][k] for k in
                  ('decomps', 'engine_bad', 'table_bad',
                   'decomp_dependent_s')}), flush=True)

print('== P5 z=9 strip grid m in {5..11} x 222 ==', flush=True)
strip = {}
for m in range(5, 12):
    z, R = 9, m + 10
    coll = engine_bad = total = 0
    seps = []
    for X in T_shapes(m):
        S = sum(X)
        hc = H_canonical(R, X, z)
        ho = H_ordered(R, X, z)
        total += 1
        if hc != ho: engine_bad += 1
        if hc != single_token(S, z, R):
            coll += 1
            if len(seps) < 8: seps.append([list(X), hc, single_token(S, z, R)])
    strip[m] = {'total': total, 'collapse': total - coll,
                'engine_bad': engine_bad, 'separations': seps}
    clear_engines()
    print('m=%d: %d/%d collapse engine_bad=%d seps=%s' %
          (m, total - coll, total, engine_bad,
           json.dumps(seps[:3])), flush=True)
res['P5_strip_z9'] = strip

print('== P5b m=6 z=10 out-of-band record ==', flush=True)
def oob_record(m, z, tag):
    out = {'total': 0, 'separations': [], 'engine_bad': 0}
    R = m + z + 1
    for X in T_shapes(m):
        S = sum(X)
        hc = H_canonical(R, X, z)
        ho = H_ordered(R, X, z)
        out['total'] += 1
        if hc != ho: out['engine_bad'] += 1
        if hc != single_token(S, z, R):
            out['separations'].append([list(X), hc, single_token(S, z, R)])
    clear_engines()
    return out
res['P5b_m6_z10_oob'] = oob_record(6, 10, 'm6 z10')
print(json.dumps(res['P5b_m6_z10_oob']), flush=True)

print('== P5c m=5 z=9 out-of-band record ==', flush=True)
res['P5c_m5_z9_oob'] = oob_record(5, 9, 'm5 z9')
print(json.dumps({'total': res['P5c_m5_z9_oob']['total'],
                  'separations': res['P5c_m5_z9_oob']['separations']}), flush=True)

print('== P6 base m=6 option-set structure ==', flush=True)
def base_check(m, z, tab_child, tag):
    pts = 0; bad = 0; details = []
    R = m + z + 1
    for X in D33_shapes(m):
        S = sum(X)
        opts = child_opts_ordered(X, z, R)
        Am = single_token(S - 1, z, R - 1)
        Cm = 1 ^ single_token(S, z - 1, R - 1)
        Dv = tab_child(S - m)
        am = am_child_value(X, m, z, R)
        ok = (opts <= {Am, Cm, Dv}) and (am == Dv)
        ho = H_ordered(R, X, z)
        hc = H_canonical(R, X, z)
        vp = single_token(S, z, R)
        pts += 1
        if (not ok) or (ho != vp) or (hc != vp):
            bad += 1
            if len(details) < 20:
                details.append((list(X), sorted(opts),
                                sorted({Am, Cm, Dv}), am, Dv, ho, hc, vp))
        clear_engines()
    return {'tag': tag, 'points': pts, 'bad': bad, 'details': details}
res['P6_base_m6'] = base_check(6, 9, C9t, 'base m=6 z=9')
print(json.dumps({k: res['P6_base_m6'][k] for k in ('points', 'bad')}),
      flush=True)

print('== P7 induction option-set identity m in {7..10} ==', flush=True)
def indu_check(mm, z, tag):
    pts = 0; bad = 0; details = []
    for m in mm:
        R = m + z + 1
        for X in D33_shapes(m):
            S = sum(X)
            opts = child_opts_ordered(X, z, R)
            A = single_token(S - 1, z, R - 1)
            C = 1 ^ single_token(S, z - 1, R - 1)
            ok = (opts == {A, C})
            ho = H_ordered(R, X, z)
            hc = H_canonical(R, X, z)
            vp = single_token(S, z, R)
            pts += 1
            if (not ok) or (ho != vp) or (hc != vp):
                bad += 1
                if len(details) < 20:
                    details.append((m, list(X), sorted(opts),
                                    sorted({A, C}), ho, hc, vp))
            clear_engines()
    return {'tag': tag, 'points': pts, 'bad': bad, 'details': details}
res['P7_induction'] = indu_check(range(7, 11), 9, 'induction z=9')
print(json.dumps({k: res['P7_induction'][k] for k in ('points', 'bad')}),
      flush=True)

print('== P7b random deep PRE-RUN seed 20261127 ==', flush=True)
import random
rng = random.Random(20261127)
pts = 0; bad = 0
for m in range(6, 12):
    R = m + 10
    for _ in range(15):
        n = rng.randint(4, 5)
        toks = [m] + [rng.randint(m, m + 15) for _ in range(n - 1)]
        X = tuple(sorted(toks))
        S = sum(X)
        hc = H_canonical(R, X, 9)
        ho = H_ordered(R, X, 9)
        pts += 1
        if hc != single_token(S, 9, R) or ho != single_token(S, 9, R) \
                or hc != ho:
            bad += 1
    clear_engines()
res['P7b_random'] = {'seed': 20261127, 'points': pts, 'bad': bad}
print(json.dumps(res['P7b_random']), flush=True)

print('== P8 cell-recursion option-set identities (full families) ==',
      flush=True)
def rec_check(pre, R, z, expfun, fam, tag):
    pts = 0; mism = 0; details = []
    for i, Y in enumerate(fam):
        s = sum(Y)
        opts = child_opts_ordered(pre + Y, z, R)
        exp = expfun(Y, s)
        pts += 1
        if opts != exp:
            mism += 1
            if len(details) < 20:
                details.append((tag, list(Y), sorted(opts), sorted(exp)))
        if i % 400 == 0:
            clear_engines()
    clear_engines()
    return {'tag': tag, 'points': pts, 'mismatch': mism, 'details': details}

famF = []
for s in [0] + list(range(3, 41)):
    famF.extend(decomps(s, 3))
famD = []
for s in [0] + list(range(5, 41)):
    famD.extend(decomps(s, 5))
famC = []
for s in [0] + list(range(6, 41)):
    famC.extend(decomps(s, 6))
famB = []
for s in [0] + list(range(7, 41)):
    famB.extend(decomps(s, 7))
res['P8_F9'] = rec_check((1,), 11, 9,
    lambda Y, s: {single_token(s, 10, 10), single_token(s, 9, 10),
                 1 ^ F8t(s)}, famF, 'F9')
res['P8_G9'] = rec_check((2,), 12, 9,
    lambda Y, s: {F9t(s), single_token(s + 1, 9, 11), 1 ^ G8t(s)},
    famF, 'G9')
def e9_cond(Y, s):
    exp = {G9t(s), 1 ^ E8t(s)}
    if any(t >= 4 for t in Y):
        exp.add(single_token(s + 2, 9, 12))
    return exp
res['P8_E9_cond'] = rec_check((3,), 13, 9, e9_cond, famF, 'E9cond')
res['P8_E9_uncond_mismatch'] = rec_check((3,), 13, 9,
    lambda Y, s: {G9t(s), 1 ^ E8t(s), single_token(s + 2, 9, 12)},
    famF, 'E9uncond')
res['P8_D9'] = rec_check((4,), 14, 9,
    lambda Y, s: {single_token(s + 3, 9, 13), E9t(s), 1 ^ D8t(s)},
    famD, 'D9')
res['P8_C9'] = rec_check((5,), 15, 9,
    lambda Y, s: {single_token(s + 4, 9, 14), D9t(s),
                 1 ^ single_token(s + 5, 8, 14)}, famC, 'C9')
res['P8_B9'] = rec_check((6,), 16, 9,
    lambda Y, s: {single_token(s + 5, 9, 15), C9t(s),
                 1 ^ single_token(s + 6, 8, 15)}, famB, 'B9')
for k in ('P8_F9', 'P8_G9', 'P8_E9_cond', 'P8_E9_uncond_mismatch',
          'P8_D9', 'P8_C9', 'P8_B9'):
    print(k, json.dumps({kk: res[k][kk] for kk in ('points', 'mismatch')}),
          flush=True)
    if res[k]['mismatch']:
        print('  details:', json.dumps(res[k]['details'][:6]), flush=True)

print('== P9 z=10 next-lane census (open registration) ==', flush=True)
z10cells = {}
for tag, pre, R, dvoff, tmin, tmax in [
        ('F10', (1,), 12, 1, 3, 9), ('G10', (2,), 13, 2, 3, 9),
        ('E10', (3,), 14, 3, 3, 9), ('D10', (4,), 15, 4, 5, 9),
        ('C10', (5,), 16, 5, 6, 9), ('B10', (6,), 17, 6, 7, 9),
        ('A10', (7,), 18, 7, 8, 9)]:
    fam = Y_tokens(tmin, tmax)
    tbl = {}; devs = []; engine_bad = 0
    for Y in fam:
        s = sum(Y)
        hc = H_canonical(R, pre + Y, 10)
        ho = H_ordered(R, pre + Y, 10)
        if hc != ho: engine_bad += 1
        tbl.setdefault(s, set()).add(hc)
        if hc != single_token(s + dvoff, 10, R):
            devs.append(list(Y))
    dep = [s for s, v in sorted(tbl.items()) if len(v) > 1]
    z10cells[tag] = {'R': R, 'floor': tmin, 'family': len(fam),
                     'engine_bad': engine_bad,
                     'decomp_dependent_s': dep,
                     'deviant_count': len(devs),
                     'deviants_vs_collapse': devs[:40],
                     'table_s20': {str(s): sorted(v)
                                   for s, v in sorted(tbl.items())
                                   if s <= 20}}
    clear_engines()
# D10 loose family
fam = Y_tokens(3, 9)
tbl = {}; devs = []; engine_bad = 0
for Y in fam:
    s = sum(Y)
    hc = H_canonical(15, (4,) + Y, 10)
    ho = H_ordered(15, (4,) + Y, 10)
    if hc != ho: engine_bad += 1
    tbl.setdefault(s, set()).add(hc)
    if hc != single_token(s + 4, 10, 15):
        devs.append(list(Y))
dep = [s for s, v in sorted(tbl.items()) if len(v) > 1]
z10cells['D10_loose'] = {'R': 15, 'floor': 3, 'family': len(fam),
                         'engine_bad': engine_bad,
                         'decomp_dependent_s': dep,
                         'deviant_count': len(devs),
                         'deviants_vs_collapse': devs[:40],
                         'table_s20': {str(s): sorted(v)
                                       for s, v in sorted(tbl.items())
                                       if s <= 20}}
clear_engines()
res['P9_z10_cells'] = z10cells
for k, v in z10cells.items():
    print(k, 'family', v['family'], 'dep_s', v['decomp_dependent_s'],
          'dev_count', v['deviant_count'], 'engine_bad', v['engine_bad'],
          flush=True)
# z=10 strip m in {6..11} x 96
z10strip = {}
for m in range(6, 12):
    z, R = 10, m + 11
    coll = engine_bad = total = 0
    seps = []
    for X in census_shapes(m):
        S = sum(X)
        hc = H_canonical(R, X, z)
        ho = H_ordered(R, X, z)
        total += 1
        if hc != ho: engine_bad += 1
        if hc != single_token(S, z, R):
            coll += 1
            if len(seps) < 8:
                seps.append([list(X), hc, single_token(S, z, R)])
    z10strip[m] = {'total': total, 'collapse': total - coll,
                   'engine_bad': engine_bad, 'separations': seps}
    clear_engines()
res['P9_z10_strip'] = z10strip
for m, v in z10strip.items():
    print('z10 strip m=%d: %d/%d collapse seps=%s' %
          (m, v['collapse'], v['total'], json.dumps(v['separations'][:4])),
          flush=True)

print('== P10 cross-check vs published K1276 audit z9_cells census ==',
      flush=True)
K1276_AUDIT = os.path.join(BASE, 'strip-z8-min5-20261124', 'output',
                           'audit.json')
K1276_AUDIT_PIN = ('84605d3b41eb54fa8663c24403dffb5ff36edd1faac'
                   '7735df3c5d0cd6f885dc1')
data = open(K1276_AUDIT, 'rb').read()
gotsz = hashlib.sha256(data).hexdigest()
assert gotsz == K1276_AUDIT_PIN, 'K1276 audit sha mismatch: ' + gotsz
k1276 = json.loads(data.decode('utf-8'))
pubcells = k1276['D6c_census']['census']['z9_cells']
mine = {'F9': res['P1_F9'], 'G9': res['P2_G9'],
        'E9': res['P2b_E9'], 'D9': res['P3_D9'],
        'D9_loose': res['P3b_D9_loose'],
        'C9': res['P4_C9'], 'B9': res['P4b_B9']}
match = True
for tag, pv in mine.items():
    pc = pubcells[tag]
    # the published census families are SUBfamilies of the probe sweeps
    # (bounded token ranges 6..9 / 7..9 vs all tokens >= floor), so the
    # published table_s20 must be a sub-table of the probe table_s20
    a = pv['table_s20']
    b = pc['table_s20']
    for k, vv in b.items():
        if a.get(k) != vv:
            match = False
            print('table mismatch at', tag, 's=', k, flush=True)
            print(' mine[s]:', json.dumps(a.get(k)), ' pub[s]:',
                  json.dumps(vv), flush=True)
res['P10_crosscheck'] = {'match': match}
print('P10 crosscheck match =', match, flush=True)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'probe_z9_predecl.json')
with open(out_path, 'w') as f:
    f.write(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=True)
            + '\n')
print('WROTE', out_path)
print('PREDECL PROBE COMPLETE')
