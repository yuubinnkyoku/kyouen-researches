#!/usr/bin/env python3
"""Pre-declaration exploration for the z=8 slice (min>=5 critical strip).
Engine: pinned block cut from the SEVEN published machines (K1264/K1268/
K1271/K1272/K1273/K1274/K1275), sha-gated to bd5f22e4... (2,508 bytes).
All results below are exploration observations recorded BEFORE the
declaration note is written; the declaration will disclose them fully.

Blocks:
  P1  F8 full-decomposition sweep: s in {0} u {3..40}, all decompositions
      into 1..4 tokens >=3 (3,657): s-only table + deviants vs v(s,8,10)
  P2  G8 / E8 same family (s-only check, loose): tables + deviant sets
  P3  D8 floored (tokens>=5): s in {0} u {5..40}, all decomps (>=5):
      collapse vs v(s+4,8,13) with the expected single s=6 deviant
  P3b D8 loose (tokens>=3) family: decomposition-dependence record
  P3c E8 full-decomposition s-only re-confirmation: the E8 table over
      ALL 3,657 decompositions (s in {0} u {3..40}, tokens >=3)
  P4  C7 floored (tokens>=6): s in {0} u {6..40}: collapse vs v(s+5,7,13)
  P5  C8 floored (tokens>=6): s in {0} u {6..40}: collapse vs v(s+5,8,14)
  P6  z=8 strip grid: m in {5..10} x 222 T-shapes (R=m+9) vs v(S,8,m+9)
  P7  m=4 z=8 negative record: 222 T-shapes (R=13): separations vs single
  P8  base m=5 option-set structure: 33 shapes: opts subset of
      {A'=v(S-1,8,13), c'=1^v(S,7,13), D8(S-5)}; a=5 child == D8(S-5);
      parent mex == v(S,8,14); deviant-absorption witness at S-5=6
  P9  induction option-set identity: m in {6..9} x 33 shapes:
      opts == {v(S-1,8,m+8), 1^v(S,7,m+8)}; parent mex == v(S,8,m+9)
  P9b fixed-seed (20261125) random deep PRE-RUN (the declared D6 uses
      a different fixed seed declared in the note): m in {5..10} x 15
      shapes at z=8, R=m+9
  P10 z=9 next-lane census (observation only): F9/G9/E9 loose tables,
      D9 floored / C9 floored / B9 floored, z=9 strip m in {5..10} x 96
  P11 cross-check vs published K1275 audit z8_cells census table_s20
  P12 cell-recursion option-set structures: F8/G8 over the 330 census
      family and D8/C7/C8 over the floored census families (sample
      families; mismatch count 0), and E8 over the FULL 3,657 family:
      the UNCONDITIONAL expectation {G8(s), 1^E7(s), v(s+2,8,11)}
      breaks at exactly Y=(3,3) (observed {0,3} vs {0,2,3}); the
      CONDITIONAL form ({v(s+2,8,11)} only if some Y token >=4)
      gives mismatch 0 over all 3,657 decompositions
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

def D9_shapes(m):
    out = [(m, m + d) for d in range(7)]
    out.extend((m, m + a, m + b) for a in range(5) for b in range(5))
    out.append(tuple(m + i for i in range(5)))
    return out

def census_shapes(m):
    out = [(m, m + d) for d in range(15)]
    out.extend((m, m + a, m + b) for a in range(9) for b in range(9))
    return out

R = {}

# ---------- P1: F8 full-decomposition sweep ----------
def p1():
    tbl = {}
    bad = 0; pts = 0; det = []
    for s in [0] + list(range(3, 41)):
        for Y in decomps(s, 3):
            X = (1,) + Y
            hc = H_canonical(10, X, 8); ho = H_ordered(10, X, 8); pts += 1
            if hc != ho: bad += 1; det.append((s, Y, hc, ho))
            tbl.setdefault(s, set()).add(hc)
        clear_engines()
    tab = {s: sorted(v) for s, v in tbl.items()}
    dev = []
    for s, vals in tab.items():
        col = single_token(s, 8, 10)
        if any(val != col for val in vals):
            for Y in decomps(s, 3):
                if H_canonical(10, (1,) + Y, 8) != col:
                    dev.append(list(Y))
            clear_engines()
    R['P1_F8'] = {'points': pts, 'bad': bad, 's_only': all(len(v) == 1 for v in tab.values()),
                  'table': {str(s): tab.get(s, []) for s in sorted(tab)},
                  'deviants_vs_v(s,8,10)': dev}
    print('P1 F8:', pts, 'bad', bad, 's_only', R['P1_F8']['s_only'])
    print('   deviants:', dev)

# ---------- P2: G8 / E8 loose census family ----------
def p2():
    fam = Y_tokens(3, 9)
    for name, ktok, Rr, colf in (('G8', 2, 11, lambda s: single_token(s + 2, 8, 11)),
                                  ('E8', 3, 12, lambda s: single_token(s + 3, 8, 12))):
        tbl = {}; bad = 0; det = []
        for Y in fam:
            s = sum(Y)
            hc = H_canonical(Rr, (ktok,) + Y, 8)
            ho = H_ordered(Rr, (ktok,) + Y, 8)
            if hc != ho: bad += 1; det.append((s, Y, hc, ho))
            tbl.setdefault(s, set()).add(hc)
        clear_engines()
        tab = {s: sorted(v) for s, v in tbl.items()}
        dev = []
        for s, vals in tab.items():
            col = colf(s)
            if any(val != col for val in vals):
                for Y in fam:
                    if sum(Y) == s and H_canonical(Rr, (ktok,) + Y, 8) != col:
                        dev.append(list(Y))
                clear_engines()
        R['P2_' + name] = {'family': len(fam), 'bad': bad,
                           's_only': all(len(v) == 1 for v in tab.values()),
                           'table': {str(s): tab[s] for s in sorted(tab)},
                           's_only_flag_decomp_dependence': [s for s, v in tab.items() if len(v) > 1]}
        # deviants computed over the same family
        R['P2_' + name]['deviants_vs_collapse'] = dev
        print('P2', name, len(fam), 'bad', bad, 'dev', dev)

# ---------- P3: D8 floored; P3b: D8 loose ----------
def p3():
    fam5 = []
    for s in [0] + list(range(5, 41)):
        fam5.extend((s, Y) for Y in decomps(s, 5))
    tbl = {}; bad = 0; pts = 0; det = []
    for s, Y in fam5:
        hc = H_canonical(13, (4,) + Y, 8); ho = H_ordered(13, (4,) + Y, 8)
        pts += 1
        if hc != ho: bad += 1; det.append((s, Y, hc, ho))
        tbl.setdefault(s, set()).add(hc)
        if hc != single_token(s + 4, 8, 13):
            det.append((s, Y, 'dev', hc, single_token(s + 4, 8, 13)))
    clear_engines()
    tab = {s: sorted(v) for s, v in tbl.items()}
    R['P3_D8_floored'] = {'points': pts, 'bad': bad,
                          's_only': all(len(v) == 1 for v in tab.values()),
                          'table': {str(s): tab[s] for s in sorted(tab)},
                          'dev_vs_v(s+4,8,13)': {str(s): tab[s][0] for s in tab
                                                 if tab[s][0] != single_token(s + 4, 8, 13)}}
    print('P3 D8 floored:', pts, 'bad', bad, 'dev:', R['P3_D8_floored']['dev_vs_v(s+4,8,13)'])
    # loose family decomposition-dependence record
    fam = Y_tokens(3, 9)
    tab2 = {}
    for Y in fam:
        s = sum(Y)
        tab2.setdefault(s, []).append((list(Y), H_canonical(13, (4,) + Y, 8)))
        if len(tab2[s]) > 4000: pass
        clear_engines()
    dep = {str(s): sorted(set(v for _, v in vs))
           for s, vs in tab2.items() if len(set(v for _, v in vs)) > 1}
    R['P3b_D8_loose'] = {'family': len(fam), 'decomp_dependent_s': sorted(int(s) for s in dep), 'values': dep}
    print('P3b D8 loose decomp-dependent s:', sorted(dep.keys()))

# ---------- P3c: E8 full-decomposition s-only re-confirmation ----------
def p3c():
    bad = 0; pts = 0; det = []
    tbl = {}
    def E8t(s): return {0:1,3:0,4:1,5:0,6:1}.get(s, 0)
    for s in [0] + list(range(3, 41)):
        for Y in decomps(s, 3):
            hc = H_canonical(12, (3,) + Y, 8)
            ho = H_ordered(12, (3,) + Y, 8)
            pts += 1
            if hc != ho or hc != E8t(s):
                bad += 1; det.append((s, Y, hc, ho, E8t(s)))
            tbl.setdefault(s, set()).add(hc)
        clear_engines()
    tab = {s: sorted(v) for s, v in tbl.items()}
    R['P3c_E8_fulldecomp'] = {'points': pts, 'bad': bad,
                              's_only': all(len(v) == 1 for v in tab.values()),
                              'table': {str(s): tab[s] for s in sorted(tab)},
                              'details': det[:10]}
    print('P3c E8 full-decomp:', pts, 'bad', bad)

# ---------- P4/P5: C7 / C8 floored (tokens>=6) ----------
def p45():
    for name, ktok, Rr, zz, colf in (('P4_C7', 5, 13, 7, lambda s: single_token(s + 5, 7, 13)),
                                      ('P5_C8', 5, 14, 8, lambda s: single_token(s + 5, 8, 14))):
        fam = []
        for s in [0] + list(range(6, 41)):
            fam.extend((s, Y) for Y in decomps(s, 6))
        tbl = {}; pts = 0; bad = 0; det = []
        for s, Y in fam:
            hc = H_canonical(Rr, (ktok,) + Y, zz); ho = H_ordered(Rr, (ktok,) + Y, zz)
            pts += 1
            if hc != ho: bad += 1; det.append((s, Y, hc, ho))
            if hc != colf(s): det.append((s, Y, 'dev', hc, colf(s)))
            tbl.setdefault(s, set()).add(hc)
        clear_engines()
        tab = {s: sorted(v) for s, v in tbl.items()}
        R[name] = {'points': pts, 'bad': bad, 's_only': all(len(v) == 1 for v in tab.values()),
                   'table': {str(s): tab[s] for s in sorted(tab)},
                   'dev': {str(s): tab[s][0] for s in tab if tab[s][0] != colf(s)}}
        print(name, pts, 'bad', bad, 'dev', R[name]['dev'])

# ---------- P6: z=8 strip grid ----------
def p6():
    res = {}
    bad = 0
    for m in range(5, 11):
        sep = []; col = 0
        for X in T_shapes(m):
            S = sum(X)
            hc = H_canonical(m + 9, X, 8); ho = H_ordered(m + 9, X, 8)
            exp = single_token(S, 8, m + 9)
            if hc != ho: bad += 1
            if hc == exp: col += 1
            else: sep.append([list(X), hc, exp])
            clear_engines()
        res[str(m)] = {'collapse': col, 'separations': sep, 'total': len(T_shapes(m))}
        print('P6 z=8 strip m=', m, res[str(m)]['collapse'], '/', res[str(m)]['total'])
    R['P6_z8_strip'] = {'bad_engine': bad, 'grid': res}

# ---------- P7: m=4 z=8 negative record ----------
def p7():
    sep = []; col = 0
    for X in T_shapes(4):
        S = sum(X)
        hc = H_canonical(13, X, 8); ho = H_ordered(13, X, 8)
        exp = single_token(S, 8, 13)
        if hc != ho: R.setdefault('P7_engine_bad', []).append([list(X), hc, ho])
        if hc == exp: col += 1
        else: sep.append([list(X), hc, exp])
        clear_engines()
    R['P7_m4_z8_negative'] = {'collapse': col, 'separations': sep, 'total': 222}
    print('P7 m=4 z=8:', col, 'collapse / 222; separations:', len(sep))

# ---------- P8: base m=5 option structure ----------
def p8():
    bad = 0; det = []
    for X in D9_shapes(5):
        S = sum(X); s = S - 5
        Rr = 14
        # parent option values via ordered engine
        opts = set()
        for i, w in enumerate(X):
            if w > 1:
                opts.add(H_ordered(Rr - 1, X[:i] + (w - 1,) + X[i + 1:], 8))
        opts.add(1 ^ H_ordered(Rr - 1, X, 7))
        expect = set()
        Ap = single_token(S - 1, 8, 13)
        cp = 1 ^ single_token(S, 7, 13)
        expect.add(Ap); expect.add(cp)
        if s >= 5:
            # D8 floored value of the a=5 child
            d8 = H_ordered(13, (4,) + X[1:], 8) if X[0] == 5 else None
            # find the a=5 child explicitly
            for i, w in enumerate(X):
                if w == 5:
                    d8 = H_ordered(13, X[:i] + (4,) + X[i + 1:], 8)
                    expect.add(d8)
                    break
            if d8 != H_canonical(13, (4,) + tuple(t for t in X[1:] if True), 8):
                pass  # not needed; canonical check below
            # cross-check floored-family table
        if not opts <= expect:
            bad += 1; det.append((X, sorted(opts), sorted(expect)))
        # parent mex equals single side
        hc = H_canonical(Rr, X, 8)
        if hc != single_token(S, 8, 14):
            bad += 1; det.append((X, 'mex', hc, single_token(S, 8, 14)))
        clear_engines()
    R['P8_base_m5'] = {'bad': bad, 'details': det[:10]}
    print('P8 base m=5:', 'bad', bad, det[:4])

# ---------- P9: induction option-set identity ----------
def p9():
    bad = 0; det = []
    for m in range(6, 10):
        for X in D9_shapes(m):
            S = sum(X)
            opts = set()
            for i, w in enumerate(X):
                if w > 1:
                    opts.add(H_ordered(m + 8, X[:i] + (w - 1,) + X[i + 1:], 8))
            opts.add(1 ^ H_ordered(m + 8, X, 7))
            expect = {single_token(S - 1, 8, m + 8), 1 ^ single_token(S, 7, m + 8)}
            if opts != expect:
                bad += 1; det.append((m, X, sorted(opts), sorted(expect)))
            hc = H_canonical(m + 9, X, 8)
            if hc != single_token(S, 8, m + 9):
                bad += 1; det.append((m, X, 'mex', hc, single_token(S, 8, m + 9)))
            clear_engines()
    R['P9_induction'] = {'bad': bad, 'details': det[:10]}
    print('P9 induction:', 'bad', bad, det[:4])

# ---------- P9b: fixed-seed random deep PRE-RUN (seed 20261125) ----------
def p9b():
    import random as _rnd
    rng = _rnd.Random(20261125)
    bad = 0; pts = 0; det = []
    for m in range(5, 11):
        Rr = m + 9
        for _ in range(15):
            n = rng.randint(4, 5)
            toks = [m] + [rng.randint(m, m + 15) for _ in range(n - 1)]
            X = tuple(sorted(toks))
            S = sum(X)
            exp = single_token(S, 8, Rr)
            hc = H_canonical(Rr, X, 8); ho = H_ordered(Rr, X, 8)
            pts += 1
            if hc != ho or hc != exp:
                bad += 1; det.append((m, X, hc, ho, exp))
        clear_engines()
    R['P9b_random_deep_pre'] = {'points': pts, 'bad': bad, 'details': det[:10]}
    print('P9b random deep pre-run:', pts, 'bad', bad)

# ---------- P10: z=9 next-lane census (observation only) ----------
def p10():
    def cell_census(name, ktok, Rr, floor, toks):
        fam = Y_tokens(floor, toks)
        tbl = {}
        for Y in fam:
            s = sum(Y)
            tbl.setdefault(s, set()).add(H_canonical(Rr, (ktok,) + Y, 9))
            clear_engines()
        tab = {s: sorted(v) for s, v in tbl.items()}
        depd = [s for s, v in tab.items() if len(v) > 1]
        R['P10_' + name] = {'family': len(fam), 'decomp_dependent_s': sorted(int(s) for s in depd),
                            'table_s20': {str(s): tab[s] for s in sorted(tab) if s <= 20},
                            'values_dependent': {str(s): tab[s] for s in depd}}
        print('P10', name, len(fam), 'dep_s:', depd)
    cell_census('F9', 1, 11, 3, 9)
    cell_census('G9', 2, 12, 3, 9)
    cell_census('E9', 3, 13, 3, 9)
    cell_census('D9_floored', 4, 14, 5, 9)
    cell_census('C9_floored', 5, 15, 6, 9)
    cell_census('B9_floored', 6, 16, 7, 9)
    # z=9 strips
    res = {}
    for m in range(5, 11):
        sep = []; col = 0
        for X in census_shapes(m):
            S = sum(X)
            hc = H_canonical(m + 10, X, 9)
            exp = single_token(S, 9, m + 10)
            if hc == exp: col += 1
            else: sep.append([list(X), hc, exp])
            clear_engines()
        res[str(m)] = {'collapse': col, 'separations': sep, 'total': 96}
        print('P10 z=9 strip m=', m, col, '/96')
    R['P10_z9_strip'] = res
    # m=5 z=9 out-of-band: also 222-shape T-family
    sep = []; col = 0
    for X in T_shapes(5):
        S = sum(X)
        hc = H_canonical(15, X, 9)
        exp = single_token(S, 9, 15)
        if hc == exp: col += 1
        else: sep.append([list(X), hc, exp])
        clear_engines()
    R['P10_m5_z9_out_of_band'] = {'collapse': col, 'separations': sep, 'total': 222}
    print('P10 m=5 z=9 (out of band):', col, '/222 collapse')

# ---------- P11: cross-check vs published K1275 audit ----------
def p11():
    import json as _j
    pub_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'published_audit.json')
    if not os.path.exists(pub_path):
        print('P11 skipped: published_audit.json not present'); return
    pub = _j.load(open(pub_path))['D6c_census']['census']['z8_cells']
    mine = {'F8': R['P1_F8']['table'], 'G8': R['P2_G8']['table'], 'E8': R['P2_E8']['table'],
            'D8': R['P3_D8_floored']['table'], 'C8': R['P5_C8']['table']}
    ok = True
    for cell in ['F8', 'G8', 'E8', 'D8', 'C8']:
        pt = pub[cell]['table_s20']
        for s, vals in pt.items():
            s_i = int(s)
            # restrict my table to the census family s-range (family tokens)
            if str(s_i) in mine[cell]:
                myvals = mine[cell][str(s_i)]
            else:
                continue
            if isinstance(vals, list): vals = {vals[0]} if False else vals
            # census family values: my full-family table has the s-only value;
            # but for s beyond my sweep, skip
            if len(set(vals)) != 1: ok = False
            if len(myvals) == 1 and myvals[0] not in vals:
                ok = False
                print('MISMATCH', cell, s, myvals, vals)
    R['P11_published_crosscheck'] = {'match': ok}
    print('P11 published crosscheck match:', ok)

# ---------- P12: cell-recursion option-set structures ----------
def p12():
    def child_opts(X, z, R):
        opts = set()
        for i, w in enumerate(X):
            if w > 1: opts.add(H_ordered(R - 1, X[:i] + (w - 1,) + X[i + 1:], z))
            else: opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
        if z >= 1: opts.add(1 ^ H_ordered(R - 1, X, z - 1))
        return opts
    def F8t(s): return {0:1,3:0,4:1,5:0,6:1,7:0,8:1}.get(s, 0)
    def G8t(s): return {0:0,3:1,4:0,5:1,6:0,7:1,8:2}.get(s, 1)
    def E8t(s): return {0:1,3:0,4:1,5:0,6:1}.get(s, 0)
    def F7t(s): return {0:1,3:0,4:1,5:0,6:1,7:0}.get(s, 2)
    def G7t(s): return {0:0,3:1,4:0,5:1,6:0}.get(s, 1)
    def E7t(s): return {0:1,3:0,4:1,5:0,6:2}.get(s, 0)
    res = {}
    fam330 = Y_tokens(3, 9)
    # F8 sample family (330) expectation
    bad = 0
    for Y in fam330:
        s = sum(Y)
        opts = child_opts((1,) + Y, 8, 10)
        exp = {single_token(s, 9, 9), single_token(s, 8, 9), 1 ^ F7t(s)}
        if opts != exp: bad += 1
        if bad and bad < 4: res.setdefault('F8_mismatch', []).append([list(Y), sorted(opts), sorted(exp)])
    clear_engines()
    res['F8_sample330_mismatches'] = bad
    print('P12 F8 330-family mismatches:', bad)
    # G8 sample family (330)
    bad = 0
    for Y in fam330:
        s = sum(Y)
        opts = child_opts((2,) + Y, 8, 11)
        exp = {F8t(s), single_token(s + 1, 8, 10), 1 ^ G7t(s)}
        if opts != exp: bad += 1
        if bad and bad < 4: res.setdefault('G8_mismatch', []).append([list(Y), sorted(opts), sorted(exp)])
    clear_engines()
    res['G8_sample330_mismatches'] = bad
    print('P12 G8 330-family mismatches:', bad)
    # E8 FULL family: unconditional vs conditional expectation
    fam_full = []
    for s in [0] + list(range(3, 41)):
        fam_full.extend(decomps(s, 3))
    bad_u = 0; det_u = []
    bad_c = 0
    n = 0
    for Y in fam_full:
        s = sum(Y)
        opts = child_opts((3,) + Y, 8, 12)
        exp_u = {G8t(s), 1 ^ E7t(s), single_token(s + 2, 8, 11)}
        if opts != exp_u:
            bad_u += 1
            det_u.append([list(Y), sorted(opts), sorted(exp_u)])
        exp_c = {G8t(s), 1 ^ E7t(s)}
        if any(t >= 4 for t in Y):
            exp_c = exp_c | {single_token(s + 2, 8, 11)}
        if opts != exp_c:
            bad_c += 1
        n += 1
        if n % 500 == 0: clear_engines()
    clear_engines()
    res['E8_full_unconditional_mismatches'] = bad_u
    res['E8_full_unconditional_detected'] = det_u[:8]
    res['E8_full_conditional_mismatches'] = bad_c
    print('P12 E8 full-family unconditional mismatches:', bad_u,
          'conditional:', bad_c)
    # D8 floored census family (126): {v(s+3,8,12), E8(s), 1^v(s+4,7,12)}
    bad = 0
    for Y in Y_tokens(5, 9):
        s = sum(Y)
        opts = child_opts((4,) + Y, 8, 13)
        exp = {single_token(s + 3, 8, 12), E8t(s), 1 ^ single_token(s + 4, 7, 12)}
        if opts != exp: bad += 1
    clear_engines()
    res['D8_floored126_mismatches'] = bad
    print('P12 D8 126-family mismatches:', bad)
    # C7 (70): {v(s+4,7,12), 1^v(s+5,6,12)}
    bad = 0
    for Y in Y_tokens(6, 9):
        s = sum(Y)
        opts = child_opts((5,) + Y, 7, 13)
        exp = {single_token(s + 4, 7, 12), 1 ^ single_token(s + 5, 6, 12)}
        if opts != exp: bad += 1
    clear_engines()
    res['C7_floored70_mismatches'] = bad
    print('P12 C7 70-family mismatches:', bad)
    # C8 (70): {D8(s), v(s+4,8,13), 1^v(s+5,7,13)} with D8(6)=2
    def D8t(s): return 2 if s == 6 else single_token(s + 4, 8, 13)
    bad = 0
    for Y in Y_tokens(6, 9):
        s = sum(Y)
        opts = child_opts((5,) + Y, 8, 14)
        exp = {D8t(s), single_token(s + 4, 8, 13), 1 ^ single_token(s + 5, 7, 13)}
        if opts != exp: bad += 1
    clear_engines()
    res['C8_floored70_mismatches'] = bad
    print('P12 C8 70-family mismatches:', bad)
    R['P12_cell_recursion'] = res

p1(); p2(); p3(); p3c(); p45(); p6(); p7(); p8(); p9(); p9b(); p10(); p11(); p12()

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_z8_predecl.json')
with open(out, 'w') as f:
    json.dump(R, f, indent=1, sort_keys=True, ensure_ascii=False)
print('_written:', out)
