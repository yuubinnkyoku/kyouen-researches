#!/usr/bin/env python3
"""probe_strip_z7_predecl.py -- pre-declaration probe for the z=7 slice
(min>=5 critical-strip z=7; provisional K1275).

Engine: machine-cut ENGINE BLOCK from the published K1274 machine
verify_strip_z6.py (sha256 61cb0b60...), sha-gated to the published
engine pin bd5f22e4... (zero hand transcription). All probe results
below are UNDECLARED observations and will be fully disclosed in the
declaration note. Nothing here is pushed as a claim.

Blocks:
  P1  F7 table sweep: s in {0} u {3..40}, all decompositions into
      1..4 tokens >=3; s-only property + table.
  P2  G7 table sweep: same full decomposition family; s-only + table
      + deviant set vs v(s+2,7,10).
  P3  E7 table sweep: same; + deviant set vs v(s+3,7,11).
  P4  D7 floored sweep: s in {0} u {5..40}, tokens >=5; full collapse
      vs v(s+4,7,12) claim candidate.
  P4b D7 loose (tokens >=3) decomposition-dependence record (floor
      essentiality support).
  P5  cell recursion option sets vs arithmetic expectations.
  P6  T-Z7 grid: m in {5..10} x 222 shapes at z=7 (R=m+8): collapse.
  P7  m=4 negative at z=7 over 222 shapes (beyond-front record).
  P8  random deep, seed 20261125, m in {5..10} x 15 shapes.
  P9  base m=5 option-structure over 33 shapes.
  P10 induction m in {6..9} option-structure over 33 shapes.
  P11 z=8 census (next lane): F8/G8/E8 (330 family), D8 (126), C8 (70)
      + z=8 strip grid m in {5..10} x 96.
  P12 published K1274 audit.json D6c z7-census cross-check.
"""
import sys, os, json, hashlib, random
from functools import lru_cache
from itertools import combinations_with_replacement

sys.setrecursionlimit(1_000_000)

# --- engine extraction (sha-gated) ---
def cut_markers(text):
    lines = text.split('\n')
    s = e = None
    for i, ln in enumerate(lines):
        if ln.startswith('# === ENGINE BLOCK'):
            s = i + 1
            break
    for j in range(s, len(lines)):
        if lines[j].startswith('# === END ENGINE BLOCK'):
            e = j
            break
    block = lines[s:e]
    while block and block[-1].strip() == '':
        block.pop()
    return '\n'.join(block) + '\n'

ENGINE_PIN = ('bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12'
              'e3a92')
K1274_REL = os.path.join('..', 'strip-z6-min5-20261123', 'verify_strip_z6.py')
K1274_PIN = ('61cb0b60b9012320e2146f4b49566a3b6fc5cee4cfb42c8911db9dc5321'
             'cb134')
src = open(K1274_REL, 'rb').read()
assert hashlib.sha256(src).hexdigest() == K1274_PIN, 'K1274 machine pin'
engine = cut_markers(src.decode('utf-8'))
esha = hashlib.sha256(engine.encode('utf-8')).hexdigest()
assert esha == ENGINE_PIN, ('engine pin', esha)
print('engine block cut from published K1274 machine:', esha[:16])

scope = {'lru_cache': lru_cache}
exec(engine, scope)
mex = scope['mex']
H_ordered = scope['H_ordered']
H_canonical = scope['H_canonical']
single_token = scope['single_token']

def clear_engines():
    H_ordered.cache_clear()
    H_canonical.cache_clear()

def decomps(s, tmin, amax=4):
    if s == 0:
        return [()]
    out = []
    for k in range(1, amax + 1):
        for c in combinations_with_replacement(range(tmin, s + 1), k):
            if sum(c) == s:
                out.append(c)
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

def census_shapes(m):
    out = [(m, m + d) for d in range(15)]
    out.extend((m, m + a, m + b) for a in range(9) for b in range(9))
    return out

def D9_shapes(m):
    out = [(m, m + d) for d in range(7)]
    out.extend((m, m + a, m + b) for a in range(5) for b in range(5))
    out.append(tuple(m + i for i in range(5)))
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

report = {}

# ---------- P1: F7 table sweep ----------
famF = []
for s in [0] + list(range(3, 41)):
    famF.extend(decomps(s, 3))
tbl = {}
bad_sonly = 0
for Y in famF:  # (s, Y)
    s = sum(Y)
    hc = H_canonical(9, (1,) + Y, 7)
    ho = H_ordered(9, (1,) + Y, 7)
    if hc != ho:
        bad_sonly += 1
    tbl.setdefault(s, set()).add(hc)
    if len(famF) % 500:
        pass
report['P1_F7'] = {
    'family': len(famF),
    'engine_disagree': bad_sonly,
    's_only': all(len(v) == 1 for v in tbl.values()),
    'table': {str(k): sorted(v)[0] if len(v) == 1 else sorted(v)
              for k, v in sorted(tbl.items())},
}
clear_engines()

# ---------- P2: G7 table sweep (full decomposition family) ----------
tbl = {}
bad = 0
devs = []
for Y in famF:
    s = sum(Y)
    X = (2,) + Y
    hc = H_canonical(10, X, 7)
    ho = H_ordered(10, X, 7)
    if hc != ho:
        bad += 1
    tbl.setdefault(s, set()).add(hc)
    if hc != single_token(s + 2, 7, 10):
        devs.append(list(Y))
report['P2_G7'] = {
    'family': len(famF), 'engine_disagree': bad,
    's_only': all(len(v) == 1 for v in tbl.values()),
    'table': {str(k): sorted(v)[0] if len(v) == 1 else sorted(v)
              for k, v in sorted(tbl.items())},
    'deviants_vs_v(s+2,7,10)': devs[:60],
    'deviant_count': len(devs),
}
clear_engines()

# ---------- P3: E7 table sweep ----------
tbl = {}
bad = 0
devs = []
for Y in famF:
    s = sum(Y)
    X = (3,) + Y
    hc = H_canonical(11, X, 7)
    ho = H_ordered(11, X, 7)
    if hc != ho:
        bad += 1
    tbl.setdefault(s, set()).add(hc)
    if hc != single_token(s + 3, 7, 11):
        devs.append(list(Y))
report['P3_E7'] = {
    'family': len(famF), 'engine_disagree': bad,
    's_only': all(len(v) == 1 for v in tbl.values()),
    'table': {str(k): sorted(v)[0] if len(v) == 1 else sorted(v)
              for k, v in sorted(tbl.items())},
    'deviants_vs_v(s+3,7,11)': devs[:60],
    'deviant_count': len(devs),
}
clear_engines()

# ---------- P4: D7 floored sweep (tokens >=5) ----------
famD = []
for s in [0] + list(range(5, 41)):
    famD.extend(decomps(s, 5))
bad = 0
badc = 0
for Y in famD:
    s = sum(Y)
    X = (4,) + Y
    hc = H_canonical(12, X, 7)
    ho = H_ordered(12, X, 7)
    if hc != ho:
        bad += 1
    if hc != single_token(s + 4, 7, 12):
        badc += 1
report['P4_D7_floored'] = {
    'family': len(famD), 'engine_disagree': bad,
    'collapse_violations': badc,
}
clear_engines()

# ---------- P4b: D7 loose (tokens >=3) decomposition-dependence ----------
tbl = {}
bad = 0
for Y in famF:
    s = sum(Y)
    X = (4,) + Y
    hc = H_canonical(12, X, 7)
    ho = H_ordered(12, X, 7)
    if hc != ho:
        bad += 1
    tbl.setdefault(s, set()).add(hc)
dep = {s: sorted(v) for s, v in sorted(tbl.items()) if len(v) > 1}
viol = [list(Y) for Y in famF
        if H_canonical(12, (4,) + Y, 7) != single_token(sum(Y) + 4, 7, 12)]
report['P4b_D7_loose'] = {
    'family': len(famF), 'engine_disagree': bad,
    'decomp_dependent_s': dep,
    'collapse_violations_count': len(viol),
    'collapse_violations_first': viol[:30],
}
clear_engines()

# ---------- P5: cell recursion option sets ----------
def opts_check(R, pre, z, expfun, fam, tag):
    bad = 0
    n = 0
    det = []
    for Y in fam:
        s = sum(Y)
        opts = child_opts_ordered(pre + Y, z, R)
        exp = expfun(s)
        if opts != exp:
            bad += 1
            if len(det) < 10:
                det.append((Y, sorted(opts), sorted(exp)))
        n += 1
        if n % 400 == 0:
            clear_engines()
    return {'cell': tag, 'points': n, 'bad': bad, 'details': det}

r5 = opts_check(9, (1,), 7,
                lambda s: {single_token(s, 8, 8), single_token(s, 7, 8),
                           1 ^ ({0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0}
                                .get(s, 0))}, famF, 'F7')
r5b = opts_check(10, (2,), 7,
                 lambda s: {single_token(s + 1, 7, 9),
                            ({0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0}
                             .get(s, 2)),
                            1 ^ {0: 0, 3: 1, 4: 0, 5: 1, 6: 2}.get(s, 1)},
                 famF, 'G7')
r5c = opts_check(11, (3,), 7,
                 lambda s: {single_token(s + 2, 7, 10),
                            {0: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1}.get(s, 1),
                            1 ^ {0: 1, 3: 0, 4: 1, 5: 0}.get(s, 0)},
                 famF, 'E7')
r5d = opts_check(12, (4,), 7,
                 lambda s: {single_token(s + 3, 7, 11),
                            {0: 1, 3: 0, 4: 1, 5: 0, 6: 2}.get(s, 0),
                            1 ^ single_token(s + 4, 6, 11)},
                 famD, 'D7')
report['P5_cell_recursion'] = [r5, r5b, r5c, r5d]
clear_engines()

# ---------- P6: T-Z7 grid ----------
grid = {}
bad = 0
for m in range(5, 11):
    R = m + 8
    b = 0
    seps = []
    for X in T_shapes(m):
        S = sum(X)
        hc = H_canonical(R, X, 7)
        ho = H_ordered(R, X, 7)
        if hc != ho:
            b += 1
        if hc != single_token(S, 7, R):
            seps.append([list(X), hc, single_token(S, 7, R)])
    grid[m] = {'bad_engine': b, 'separations': seps}
    bad += b
    clear_engines()
report['P6_TZ7_grid'] = {'separations_total':
                         sum(len(g['separations']) for g in grid.values()),
                         'engine_bad': bad, 'grid': grid}

# ---------- P7: m=4 negative at z=7 ----------
neg = []
bade = 0
for X in T_shapes(4):
    S = sum(X)
    hc = H_canonical(12, X, 7)
    ho = H_ordered(12, X, 7)
    if hc != ho:
        bade += 1
    if hc != single_token(S, 7, 12):
        neg.append([list(X), hc, single_token(S, 7, 12)])
report['P7_m4_z7_negative'] = {'total': 222, 'engine_bad': bade,
                               'separation_count': len(neg),
                               'separations_first20': neg[:20]}

# ---------- P8: random deep, seed 20261125 ----------
rng = random.Random(20261125)
bad = 0
det = []
for m in range(5, 11):
    R = m + 8
    for _ in range(15):
        n = rng.randint(4, 5)
        toks = [m] + [rng.randint(m, m + 15) for _ in range(n - 1)]
        X = tuple(sorted(toks))
        S = sum(X)
        hc = H_canonical(R, X, 7)
        ho = H_ordered(R, X, 7)
        if hc != ho or hc != single_token(S, 7, R):
            bad += 1
            det.append([m, list(X), hc, ho, single_token(S, 7, R)])
    clear_engines()
report['P8_random_deep'] = {'points': 90, 'bad': bad, 'details': det[:10]}

# ---------- P9: base m=5 structure ----------
bad = 0
det = []
for X in D9_shapes(5):
    S = sum(X)
    R = 13
    opts = child_opts_ordered(X, 7, R)
    Ap = single_token(S - 1, 7, 12)
    cp = 1 ^ single_token(S, 6, 12)
    Dv = single_token(S - 1, 7, 12)  # D7(S-5) = v(s+4,7,12), s=S-5
    a5 = am_child_value(X, 5, 7, R)
    if (not (opts <= {Ap, cp, Dv})) or (a5 != Dv):
        bad += 1
        det.append([list(X), sorted(opts), sorted({Ap, cp, Dv}), a5, Dv])
    if H_canonical(R, X, 7) != single_token(S, 7, R):
        bad += 1
        det.append([list(X), 'parent', H_canonical(R, X, 7),
                    single_token(S, 7, R)])
clear_engines()
report['P9_base_m5'] = {'points': 33, 'bad': bad, 'details': det[:10]}

# ---------- P10: induction m in {6..9} ----------
bad = 0
det = []
for m in range(6, 10):
    R = m + 8
    for X in D9_shapes(m):
        S = sum(X)
        opts = child_opts_ordered(X, 7, R)
        A = single_token(S - 1, 7, m + 7)
        C = 1 ^ single_token(S, 6, m + 7)
        if opts != {A, C}:
            bad += 1
            det.append([m, list(X), sorted(opts), sorted({A, C})])
        if H_canonical(R, X, 7) != single_token(S, 7, R):
            bad += 1
            det.append([m, list(X), 'parent', H_canonical(R, X, 7),
                        single_token(S, 7, R)])
    clear_engines()
report['P10_induction'] = {'points': 132, 'bad': bad, 'details': det[:10]}

# ---------- P11: z=8 census (next lane) ----------
cells = {}
for tag, pre, R, dvoff, tmin, tmax in [
        ('F8', (1,), 10, 1, 3, 9), ('G8', (2,), 11, 2, 3, 9),
        ('E8', (3,), 12, 3, 3, 9), ('D8', (4,), 13, 4, 5, 9),
        ('C8', (5,), 14, 5, 6, 9)]:
    fam = Y_tokens(tmin, tmax)
    tbl = {}
    bad = 0
    devs = []
    for Y in fam:
        s = sum(Y)
        X = pre + Y
        hc = H_canonical(R, X, 8)
        ho = H_ordered(R, X, 8)
        if hc != ho:
            bad += 1
        tbl.setdefault(s, set()).add(hc)
        if hc != single_token(s + dvoff, 8, R):
            devs.append(list(Y))
    dep = {str(s): sorted(v) for s, v in sorted(tbl.items()) if len(v) > 1}
    tbl2 = {str(s): (sorted(v)[0] if len(v) == 1 else sorted(v))
            for s, v in sorted(tbl.items()) if s <= 20}
    cells[tag] = {'R': R, 'floor': tmin, 'family': len(fam),
                  'engine_bad': bad, 'table_s20': tbl2,
                  'decomp_dependent_s': dep,
                  'deviant_count': len(devs),
                  'deviants_first': devs[:25]}
    clear_engines()
strip = {}
for m in range(5, 11):
    z, R = 8, m + 9
    seps = []
    bad = 0
    for X in census_shapes(m):
        S = sum(X)
        hc = H_canonical(R, X, z)
        ho = H_ordered(R, X, z)
        if hc != ho:
            bad += 1
        if hc != single_token(S, z, R):
            seps.append([list(X), hc, single_token(S, z, R)])
    strip[m] = {'engine_bad': bad, 'separations': seps[:10],
                'separation_count': len(seps)}
    clear_engines()
report['P11_z8_census'] = {'cells': cells, 'strip': strip}

# ---------- P12: published K1274 audit census cross-check ----------
try:
    with open('..', 'strip-z6-min5-20261123', 'output', 'audit.json') as f:
        pass
except Exception:
    pass
p12 = None
k1274_audit_path = os.path.join('..', 'strip-z6-min5-20261123',
                               'output', 'audit.json')
if os.path.exists(k1274_audit_path):
    with open(k1274_audit_path) as f:
        pub = json.load(f)
    zc = pub['D6c_census']['census']['z7_cells']
    raw = {}
    for tag, pre, R, dvoff, tmin, tmax in [
            ('F7', (1,), 9, 1, 3, 9), ('G7', (2,), 10, 2, 3, 9),
            ('E7', (3,), 11, 3, 3, 9), ('D7', (4,), 12, 4, 5, 9),
            ('C7', (5,), 13, 5, 6, 9)]:
        fam = Y_tokens(tmin, tmax)
        tbl = {}
        for Y in fam:
            s = sum(Y)
            hc = H_canonical(R, pre + Y, 7)
            tbl.setdefault(s, set()).add(hc)
        tbl2 = {str(s): sorted(v)[0] if len(v) == 1 else sorted(v)
                for s, v in sorted(tbl.items()) if s <= 20}
        raw[tag] = {'published': zc[tag]['table_s20'], 'mine': tbl2,
                    'match': tbl2 == zc[tag]['table_s20']}
        clear_engines()
    # strip cross-check
    zstrip = pub['D6c_census']['census']['z7_strip']
    ok = True
    for m in range(5, 11):
        z, R = 7, m + 8
        cnt = 0
        for X in census_shapes(m):
            if H_canonical(R, X, z) != single_token(sum(X), z, R):
                cnt += 1
        ok = ok and (cnt == zstrip[str(m)]['separations'].__len__()
                     if isinstance(zstrip.get(str(m)), dict) and
                     'separations' in zstrip.get(str(m), {}) else True)
        clear_engines()
    p12 = {'cells_match': all(v['match'] for v in raw.values()),
           'cells': {k: v['match'] for k, v in raw.items()}}
    report['P12_published_crosscheck'] = p12
report['engine_pin'] = esha
print(json.dumps(report, indent=1, sort_keys=True, ensure_ascii=True))
with open('output/probe_predecl.json', 'w') as f:
    f.write(json.dumps(report, indent=1, sort_keys=True, ensure_ascii=True)
            + '\n')
print('PROBE DONE')
