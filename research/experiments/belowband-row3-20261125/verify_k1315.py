#!/usr/bin/env python3
"""verify_k1315: audit machine for the K1315 observation packet
(third below-band row k = z+n-5: OBS-BBL3 class-layered collapse census,
L-BR3 single-token transcription lemma, CONJ-BBL3 unifying conjecture
stated but NOT proven; everything below is OBSERVATION grade unless the
word GRID-VERIFIED appears).

Claims audited here (scopes in the single-owner declaration note):
  L-BR3 (GRID-VERIFIED, x,z <= 30): the n=1 slice of the third below-band
      row (k = z-4, R = x+z-4) equals the published K0832 single-token
      closed form `single_token` for all 924 reachable cells.
  OBS-BBL3 (census, frozen in explore_k1315.out): on row k = z+n-5 with
      E := 2*max(X)-S, w := E+z, j := #1-heaps:
      (a) raw (E,z) layer: multivalue cells {n=3:17, 4:21, 5:48, 6:61,
          7:90} -> NO raw-layer collapse (negative observation);
      (b) class (n,j) layer: near-collapse; (6,0),(6,1),(7,1)..(7,7)
          EXACTLY 0 multivalue cells in-sweep; (7,0) has 33 (the
          two-tail-family conflict band, all cells w in [-17,-15]);
      (c) the swept 2-lines: within-class per-tail-family constants A:
          V = 2 on w = A, [E even] left (w < A), [E odd] right (w > A);
          with the anchor measured from each row's own 2, the 3-piece
          law has ZERO genuine violations in-sweep for n=4..8
          (5,779 single-2 rows incl. the n=7 two-family class and all
          three n=8 ladder levels); off-level outliers (law-conformant
          rows off the class modal A) are declared: 8 rows at n=4,
          2 rows at n=5, 0 elsewhere in-sweep; n=3 carries the two
          declared wall families (t+3,t,1) and (t+2,t,2) whose z=0
          cell is absorbed into the right plateau (26+8+2 = 36 in-sweep
          rows, all in those clans plus (2,2,2));
      (d) tail-family ladders: n=7 j=0: A=-15 iff min-heap=2 (hi=8
          re-confirmation of 639+636 votes outside the frozen sweep)
          else A=-17; n=8 j=0: A=-20 (>=2 twos) / -22 (exactly one 2)
          / -24 (min 3) / -26 (min>=4); A_{n,j} shape
          eta(n)+2j-2*[j>=n-3], eta = 1,0,-5,-10,-15 or -17 per family;
      (e) suppression: rows with line at z* <= 0 read [E odd] over the
          whole window; the declared wall families (t+3,t,1), (t+2,t,2)
          left-cell absorption and all-2s-top mountain suppression
          ((2^4,1,1)- and (2,2,1^4)-clans) are the ONLY in-sweep
          violators at n=3..4 (at n=6: (2,2,2,2,1,1) reads no 2 in
          window vs (3,3,2,2,1,1) line at z*=0; (2,2,1^4),(3,3,1^4)
          mountain absent vs (4,4,1^4) line at z*=0).
  CONJ-BBL3 (CONJECTURE, disclaimed): the per-family 3-piece law holds
  for ALL instances and ALL n >= 3.  NOT proven; NOT checked beyond
  the frozen grids here.

MODES: default = full battery (rc 0 iff overall_bad == 0).
  --tamper-engine   rc 2 (engine block sha mismatch)
  --tamper=law      flip one V_LAW row value   -> rc 1, D2 bad
  --tamper=cells    flip one V_CELLS witness   -> rc 1, D3 bad
  --tamper=xen      flip one V_XEN value       -> rc 1, D4 bad
  --tamper=anchors  declare an anchor mismatch-> rc 1, D5 bad
  --tamper=census   declare a census mismatch -> rc 1, D5 bad
"""
import hashlib
import json
import os
import sys

sys.setrecursionlimit(100000)

ENGINE_BLOCK = '''def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

# ------------------------------------------------------------------
# Raw engines (verbatim from the published K1138 verifier block; the same
# transcription is embedded in the published y22 machine K1257).
# ------------------------------------------------------------------
@lru_cache(maxsize=6_000_000)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(maxsize=6_000_000)
def H_canonical(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def vC(x, z, R):  # canonical-engine single token
    return H_canonical(R, (x,), z)
def vO(x, z, R):  # ordered-engine single token
    return H_ordered(R, (x,), z)

# ------------------------------------------------------------------
# Published K0832 single-token closed form (transcription of the published
# single_token block in the y22 machine K1257; see report provenance).
# ------------------------------------------------------------------
def q_odd(k):
    return k if k % 2 else k - 1

def single_token(x, z, R):
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))
'''

PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
FROZEN_EXPLORE_SHA = '29f7080ae59ff9852b62a8c2f6d4300b3db2c713dae90589c7d9e09eda37e195'
FROZEN_OUT_SHA = '558ed202ebdd0d80b6159856a836842dd10e73807d37c6eb392437f1175032eb'

sha = hashlib.sha256(ENGINE_BLOCK.encode('utf-8')).hexdigest()
if '--tamper-engine' in sys.argv:
    sha = sha[:-1] + ('0' if sha[-1] != '0' else '1')
    assert sha != PIN
    print(json.dumps({'mode': 'tamper-engine', 'engine_sha': sha,
                     'engine_gate': 'FAIL'}))
    sys.exit(2)
assert sha == PIN, sha
from functools import lru_cache
ns = {'lru_cache': lru_cache}
exec(ENGINE_BLOCK, ns)
H_canonical = ns['H_canonical']
H_ordered = ns['H_ordered']
single_token = ns['single_token']

TAMPER = [a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--tamper=')]
if TAMPER:
    assert len(TAMPER) == 1 and TAMPER[0] in (
        'law', 'cells', 'xen', 'anchors', 'census'), TAMPER

V_LAW = [{'X': [3, 3, 1], 'n': 3, 'E': -1, 'A': 3, 'conform': True, 'vals': [0, 0, 0, 0, 2, 1, 1]}, {'X': [4, 2, 2], 'n': 3, 'E': 0, 'A': 1, 'conform': False, 'vals': [0, 2, 0, 0, 0, 0, 0]}, {'X': [5, 2, 1], 'n': 3, 'E': 2, 'A': 3, 'conform': False, 'vals': [0, 2, 0, 0, 0, 0, 0]}, {'X': [2, 2, 2], 'n': 3, 'E': -2, 'A': -1, 'conform': False, 'vals': [0, 2, 0, 0, 0, 0, 0]}, {'X': [10, 7, 1], 'n': 3, 'E': 2, 'A': 3, 'conform': False, 'vals': [0, 2, 0, 0, 0, 0, 0]}, {'X': [9, 7, 2], 'n': 3, 'E': 0, 'A': 1, 'conform': False, 'vals': [0, 2, 0, 0, 0, 0, 0]}, {'X': [3, 3, 1, 1], 'n': 4, 'E': -2, 'A': 0, 'conform': True, 'vals': [1, 1, 2, 0, 0, 0, 0, 0, 0]}, {'X': [4, 4, 3, 3], 'n': 4, 'E': -6, 'A': 0, 'conform': True, 'vals': [1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0]}, {'X': [4, 4, 1, 1], 'n': 4, 'E': -2, 'A': 2, 'conform': True, 'vals': [1, 1, 1, 1, 2, 0, 0, 0, 0]}, {'X': [2, 2, 1, 1], 'n': 4, 'E': -2, 'A': -2, 'conform': True, 'vals': [2, 0, 0, 0, 0, 0, 0, 0, 0]}, {'X': [4, 4, 4, 3, 3], 'n': 5, 'E': -10, 'A': -5, 'conform': True, 'vals': [1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0]}, {'X': [4, 4, 4, 4, 3, 3], 'n': 6, 'E': -14, 'A': -10, 'conform': True, 'vals': [1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0]}, {'X': [5, 4, 3, 2, 2, 2], 'n': 6, 'E': -8, 'A': None, 'conform': None, 'vals': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {'X': [2, 2, 2, 2, 1, 1], 'n': 6, 'E': -6, 'A': None, 'conform': None, 'vals': [0, 0, 0, 0, 0, 0]}, {'X': [3, 3, 2, 2, 1, 1], 'n': 6, 'E': -6, 'A': -6, 'conform': True, 'vals': [2, 0, 0, 0, 0, 0, 0]}, {'X': [2, 2, 1, 1, 1, 1], 'n': 6, 'E': -4, 'A': None, 'conform': None, 'vals': [0, 0, 0, 0, 0, 0, 0]}, {'X': [3, 3, 1, 1, 1, 1], 'n': 6, 'E': -4, 'A': None, 'conform': None, 'vals': [0, 0, 0, 0, 0, 0, 0]}, {'X': [4, 4, 1, 1, 1, 1], 'n': 6, 'E': -4, 'A': -4, 'conform': True, 'vals': [2, 0, 0, 0, 0, 0, 0]}, {'X': [6, 6, 4, 3, 2, 2, 2], 'n': 7, 'E': -13, 'A': None, 'conform': None, 'vals': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}, {'X': [6, 6, 6, 3, 3, 3, 3], 'n': 7, 'E': -18, 'A': -17, 'conform': True, 'vals': [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {'X': [6, 6, 6, 6, 2, 2, 2, 2], 'n': 8, 'E': -20, 'A': -20, 'conform': True, 'vals': [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {'X': [6, 6, 6, 5, 3, 3, 3, 2], 'n': 8, 'E': -22, 'A': -22, 'conform': True, 'vals': [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {'X': [6, 6, 6, 4, 3, 3, 3, 1], 'n': 8, 'E': -20, 'A': -20, 'conform': True, 'vals': [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {'X': [6, 6, 6, 6, 2, 2, 2, 1], 'n': 8, 'E': -19, 'A': -18, 'conform': True, 'vals': [0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}]
V_CELLS = [{'w1': [[5, 5, 3, 2, 1, 1], -7, 1], 'w2': [[6, 4, 4, 3, 1, 1], -7, 1], 'z': 3}, {'w1': [[6, 6, 4, 3, 3, 1, 1], -12, 0], 'w2': [[7, 6, 5, 3, 3, 1, 1], -12, 0], 'z': 5}]
V_XEN = [{'X': [4, 2, 1], 'R': 9, 'z': 4, 'can': 1, 'ord': 1}, {'X': [3, 3, 1], 'R': 7, 'z': 2, 'can': 0, 'ord': 0}, {'X': [5, 3, 2], 'R': 9, 'z': 1, 'can': 2, 'ord': 2}, {'X': [4, 4, 2, 2], 'R': 14, 'z': 3, 'can': 1, 'ord': 1}, {'X': [5, 4, 3, 1], 'R': 18, 'z': 6, 'can': 1, 'ord': 1}, {'X': [2, 2, 2, 2, 1, 1], 'R': 13, 'z': 2, 'can': 0, 'ord': 0}, {'X': [4, 4, 1, 1, 1, 1], 'R': 13, 'z': 0, 'can': 2, 'ord': 2}, {'X': [6, 3, 2, 2, 2, 2, 1], 'R': 24, 'z': 4, 'can': 0, 'ord': 0}, {'X': [5, 5, 4, 3, 3, 3], 'R': 31, 'z': 7, 'can': 1, 'ord': 1}, {'X': [6, 6, 6, 3, 3, 3, 3], 'R': 33, 'z': 1, 'can': 2, 'ord': 2}]

if TAMPER and TAMPER[0] == 'law':
    V_LAW[0]['vals'][0] = (V_LAW[0]['vals'][0] + 1) % 3
if TAMPER and TAMPER[0] == 'cells':
    V_CELLS[0]['w1'][2] = (V_CELLS[0]['w1'][2] + 1) % 3
if TAMPER and TAMPER[0] == 'xen':
    V_XEN[0]['can'] = (V_XEN[0]['can'] + 1) % 3

# ----------------------------------------------------------------- D1
bad = []
count = 0
for x in range(1, 31):
    for z in range(0, 31):
        R = x + z - 4
        if R < 0:
            continue
        count += 1
        if H_canonical(R, (x,), z) != single_token(x, z, R):
            bad.append(['D1', x, z])
        H_canonical.cache_clear()
D1 = {'count': count, 'bad': bad}

# ----------------------------------------------------------------- D2
count = 0
bad2 = []
for e in V_LAW:
    Xd = tuple(e['X'])
    n = e['n']
    S = sum(Xd)
    E = 2 * Xd[0] - S
    count += 1
    if E != e['E']:
        bad2.append(['D2-E', e['X'], E, e['E']])
    vs = []
    for z in range(len(e['vals'])):
        R = S + z + n - 5
        vs.append(H_canonical(R, Xd, z) if R >= 0 else None)
        count += 1
    H_canonical.cache_clear()
    if vs != e['vals']:
        bad2.append(['D2-vals', e['X'], vs, e['vals']])
    twos = [z for z, v in enumerate(vs) if v == 2]
    A = E + twos[0] if len(twos) == 1 else None
    count += 1
    if A != e['A']:
        bad2.append(['D2-A', e['X'], A, e['A']])
    if e['conform'] is not None and A is not None:
        conform = all((v == (2 if E + z == A else
                             (E % 2 == 0 if E + z < A else E % 2 == 1)))
                      for z, v in enumerate(vs) if v is not None)
        count += 1
        if conform != e['conform']:
            bad2.append(['D2-conform', e['X'], conform, e['conform']])
D2 = {'count': count, 'bad': bad2}

# ----------------------------------------------------------------- D3
count = 0
bad3 = []
for c in V_CELLS:
    for w in ('w1', 'w2'):
        Xd = tuple(c[w][0])
        n = len(Xd)
        S = sum(Xd)
        E = 2 * Xd[0] - S
        count += 2
        if E != c[w][1]:
            bad3.append(['D3-E', Xd, E, c[w][1]])
            continue
        R = S + c['z'] + n - 5
        v = H_canonical(R, Xd, c['z'])
        if v != c[w][2]:
            bad3.append(['D3-v', Xd, v, c[w][2]])
        H_canonical.cache_clear()
    count += 1
    if c['w1'][2] != c['w2'][2]:
        bad3.append(['D3-uniform', c['w1'], c['w2']])
D3 = {'count': count, 'bad': bad3}

# ----------------------------------------------------------------- D4
count = 0
bad4 = []
for e in V_XEN:
    count += 1
    vc = H_canonical(e['R'], tuple(e['X']), e['z'])
    vo = H_ordered(e['R'], tuple(e['X']), e['z'])
    H_canonical.cache_clear()
    H_ordered.cache_clear()
    if vc != vo or vc != e['can'] or vo != e['ord']:
        bad4.append(['D4', e['X'], e['z'], vc, vo, e['can'], e['ord']])
D4 = {'count': count, 'bad': bad4}

# ----------------------------------------------------------------- D5
# frozen-artifact + headline consistency battery (parses explore_k1315.out
# and explore_k1315.py from the kit directory when present).
count = 0
bad5 = []
here = os.path.dirname(os.path.abspath(__file__))
p_out = os.path.join(here, 'explore_k1315.out')
p_exp = os.path.join(here, 'explore_k1315.py')
if os.path.exists(p_out):
    count += 2
    o_sha = hashlib.sha256(open(p_out, 'rb').read()).hexdigest()
    if o_sha != FROZEN_OUT_SHA:
        bad5.append(['D5-out-sha', o_sha])
    if os.path.exists(p_exp):
        count += 1
        e_sha = hashlib.sha256(open(p_exp, 'rb').read()).hexdigest()
        if e_sha != FROZEN_EXPLORE_SHA:
            bad5.append(['D5-explore-sha', e_sha])
    data = json.load(open(p_out))
    count += 1
    if not (data['WA_LBR3']['pass'] and data['WA_LBR3']['cells'] == 924):
        bad5.append(['D5-wa'])
    exp_wb = {'3': 17, '4': 21, '5': 48, '6': 61, '7': 90}
    for n, mv in exp_wb.items():
        count += 1
        if data['WB_raw_layer_noncollapse'][n]['multivalue_cells'] != mv:
            bad5.append(['D5-wb', n])
    exp_wc = {'3': {'0': 4, '1': 4, '2': 0}, '4': {'0': 3, '1': 3, '2': 8},
              '5': {'0': 2, '1': 3, '2': 2, '3': 5},
              '6': {'0': 0, '1': 0, '2': 1, '3': 0, '4': 1},
              '7': {'0': 33, '1': 0, '2': 0, '3': 0, '4': 0}}
    for n, d in exp_wc.items():
        for j, mv in d.items():
            count += 1
            if data['WC_class_census'][n][j]['multivalue'] != mv:
                bad5.append(['D5-wc', n, j])
    anchors = {'3': {'0': {'1': 185, '-1': 1}},
               '4': {'0': {'-2': 1, '0': 464}}, '5': {'0': {'-5': 673}},
               '6': {'0': {'-10': 374}},
               '7': {'0': {'-15': 114, '-17': 98}, '1': {'-13': 135},
                     '2': {'-11': 73}, '3': {'-9': 35}, '4': {'-9': 3}},
               '8': {'0': {'-26': 35, '-24': 55, '-22': 67, '-20': 58},
                     '1': {'-20': 79, '-18': 75}, '2': {'-16': 95}}}
    for n, d in anchors.items():
        for j, votes in d.items():
            count += 1
            if data['WD_anchor_census'][n][j]['votes'] != votes:
                bad5.append(['D5-anchor', n, j])
    exp_off = {'4': {'0': 1, '1': 1, '2': 3, '3': 3},
               '5': {'1': 1, '3': 1}}
    exp_viol3 = {'0': 26, '1': 8, '2': 2}
    for n in ('4', '5', '6', '7'):
        for j in sorted(data['WEWF_suppression_and_law'][n]):
            st = data['WEWF_suppression_and_law'][n][j]
            count += 1
            if st['line_violate'] != 0 or st['supp_bad_violating'] != 0:
                bad5.append(['D5-law-clean', n, j])
            off = st.get('off_level', 0)
            if off != exp_off.get(n, {}).get(j, 0):
                bad5.append(['D5-off-level', n, j, off])
    for j in sorted(data['WEWF_suppression_and_law']['3']):
        st = data['WEWF_suppression_and_law']['3'][j]
        count += 1
        if st['line_violate'] != exp_viol3.get(j, 0):
            bad5.append(['D5-viol3', j, st['line_violate']])
    for k in sorted(data['WEWF_n8']):
        st = data['WEWF_n8'][k]
        count += 1
        if (st['line_conform'] != st['line'] or st['multi2'] != 0 or
                st.get('off_level', 0) != 0):
            bad5.append(['D5-n8', k])
    if TAMPER and TAMPER[0] == 'anchors':
        bad5.append(['D5-anchor-tamper'])
    if TAMPER and TAMPER[0] == 'census':
        bad5.append(['D5-census-tamper'])
else:
    if TAMPER and TAMPER[0] in ('anchors', 'census'):
        bad5.append(['D5-battery-unavailable-tamper'])
D5 = {'count': count, 'bad': bad5}

res = {'mode': (TAMPER[0] if TAMPER else 'full'),
       'engine_gate': 'PASS',
       'D1_LBR3': D1, 'D2_LAW': D2, 'D3_CELLS': D3,
       'D4_XENGINE': D4, 'D5_FROZEN': D5}
res['overall_bad'] = (len(D1['bad']) + len(D2['bad']) + len(D3['bad']) +
                      len(D4['bad']) + len(D5['bad']))
print(json.dumps(res, sort_keys=True))
sys.exit(0 if res['overall_bad'] == 0 else 1)
