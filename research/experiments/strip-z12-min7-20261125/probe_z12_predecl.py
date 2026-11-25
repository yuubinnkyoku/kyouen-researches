#!/usr/bin/env python3
"""probe_z12_predecl.py -- pre-declaration exploration machine for the
z=12 critical-strip slice (min>=7 band; provisional K1316). Deterministic,
zero hand transcription of values: all claimed values are computed by the
pinned raw engines (engine block sha256 bd5f22e415a78368c9b798296bc84948d5
637decbf3c21a92404d45fb12e3a92, machine-cut from the published K1280
verifier verify_strip_z11.py). Observation only: NO claims are made by this
probe (the strip z=12 m>=7 theorem for the min>=7 band is claimed by the
separate K1316 machine; this file only records the pre-declaration
exploration). Outputs part1_z12.json (part1: P1-P4c cell sweeps of the
CANDIDATE z=12 closed forms) and predecl_z12.json (part2: P5-P8 strip /
base / induction / form records, the P9 z=13 census OBSERVATION (next
lane; no z=13 claims), and the P10 crosscheck of a fresh z=12 census
against the published predecl_z11.json record).

Usage: python3 probe_z12_predecl.py part1|part2
"""
import json, os, sys, hashlib
from functools import lru_cache
from itertools import combinations_with_replacement

# === ENGINE BLOCK (machine-assembled; see build_engine_from_published.py) ===
def mex(values):
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

# === END ENGINE BLOCK ===

v = single_token

# candidate closed forms for the z=12 cells (derived from the published
# z=11 tables via the cell recursions and the published predecl_z11.json
# z12_cells census; CONFIRMED below against the raw engines -- this probe
# itself claims nothing).
# F12: s=0 ->1; s in {3..12} alternating (odd 0, even 1); s>=13 ->0.
#      census deviant direction: s=12 UPWARD (1 > collapse 0; 8 shapes).
# G12: s=0 ->0; s in {3..9} alternating (odd 1, even 0); 10:0, 11:1, 12:2,
#      tail 1. deviant directions: s=10 DOWN (0 < collapse 2; 4 shapes),
#      s=12 UP (2 > collapse 1; 8 shapes).
# E12: s=0 ->1; s in {3..11} alternating (odd 0, even 1); s>=12 ->0.
#      s=10 UP (1 > collapse 0; 4 shapes); unconditional-ghost slice 0.
# D12 floor 5: {8:0, 10:2}, else v(s+4,12,17): (8,) 0<2, (5,5) 2>1.
# C12 floor 6: {8:1}, else v(s+5,12,18): (8,) 1>0.
# B12 floor 7: {8:2}, else v(s+6,12,19): (8,) 2>1.
# A12 floor 8: full single-token collapse v(s+7,12,20) (ndev 0).
def F12t(s): return {0:1,3:0,4:1,5:0,6:1,7:0,8:1,9:0,10:1,11:0,12:1}.get(s, 0)
def G12t(s): return {0:0,3:1,4:0,5:1,6:0,7:1,8:0,9:1,10:0,11:1,12:2}.get(s, 1)
def E12t(s): return {0:1,3:0,4:1,5:0,6:1,7:0,8:1,9:0,10:1,11:0}.get(s, 0)
def D12t(s): return {8:0, 10:2}.get(s, v(s+4, 12, 17))
def C12t(s): return {8:1}.get(s, v(s+5, 12, 18))
def B12t(s): return {8:2}.get(s, v(s+6, 12, 19))
def A12t(s): return v(s+7, 12, 20)

# published z=11 closed forms (K1280) used by the recursions / ghost forms
def F11t(s): return {0:1,3:0,4:1,5:0,6:1,7:0,8:1,9:0,10:1,11:0}.get(s, 2)
def G11t(s): return {0:0,3:1,4:0,5:1,6:0,7:1,8:0,9:1,10:0,11:1}.get(s, 1)
def E11t(s): return {0:1,3:0,4:1,5:0,6:1,7:0,8:1,9:0,10:2}.get(s, 0)

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

def census96(m):
    out = [(m, m + d) for d in range(15)]
    out.extend((m, m + a, m + b) for a in range(9) for b in range(9))
    return out

def clear():
    H_ordered.cache_clear(); H_canonical.cache_clear()

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

def sweep_cell(name, R, z, singleton, tmin, sdomain, table):
    pts = comps = bad = 0
    det = []
    for s in sdomain:
        exp = table(s)
        for Y in decomps(s, tmin):
            X = (singleton,) + Y
            hc = H_canonical(R, X, z); ho = H_ordered(R, X, z)
            comps += 3
            if hc != exp or ho != exp or hc != ho:
                bad += 1
                if len(det) < 25: det.append([s, list(Y), hc, ho, exp])
            pts += 1
        clear()
    return {'cell': name, 'points': pts, 'comparisons': comps, 'bad': bad,
            'details': det}

def main(part):
    out = {}
    if part == 'part1':
        S3 = [0] + list(range(3, 41))
        cells = [('F12', 14, 1, 3, S3, F12t),
                 ('G12', 15, 2, 3, S3, G12t),
                 ('E12', 16, 3, 3, S3, E12t),
                 ('D12', 17, 4, 5, [0]+list(range(5,41)), D12t),
                 ('C12', 18, 5, 6, [0]+list(range(6,41)), C12t),
                 ('B12', 19, 6, 7, [0]+list(range(7,41)), B12t),
                 ('A12', 20, 7, 8, [0]+list(range(8,41)), A12t)]
        for nm, R, sgl, tmin, sdom, tab in cells:
            out[nm] = sweep_cell(nm, R, 12, sgl, tmin, sdom, tab)
            print(nm, out[nm]['points'], out[nm]['comparisons'], 'bad', out[nm]['bad'])
        json.dump(out, open('part1_z12.json', 'w'), indent=1)
        print('part1 written,', sum(o['points'] for o in out.values()), 'points,',
              sum(o['comparisons'] for o in out.values()), 'comparisons')
        return
    # part2
    p1 = json.load(open('part1_z12.json'))
    out['cells'] = {k: p1[k] for k in ('F12','G12','E12','D12','C12','B12','A12')}
    # P5 strip z=12: m in {5..12} (222 T-family for m in {5,6,7}; 96
    # census shapes for m in {8..12}) at z=12, R = m + 13.
    # m in {5,6} are out-of-band records (declared theorem is m>=7).
    strip = {}
    for m in range(5, 13):
        R = m + 13
        fam = T_shapes(m) if m in (5, 6, 7) else census96(m)
        okc = bad = 0; seps = []
        for X in fam:
            hv = H_canonical(R, X, 12)
            exp = v(sum(X), 12, R)
            if hv != exp: bad += 1; seps.append([ list(X), hv, exp ])
            else: okc += 1
        clear()
        strip[str(m)] = {'ok': okc, 'bad': bad, 'n': len(fam), 'seps': seps[:10]}
        print('strip z=12 m', m, strip[str(m)]['ok'], strip[str(m)]['bad'])
    out['strip_z12'] = strip
    # P6 base m=7 structure (33 shapes; z=12, R=20).
    # TOLERANT ABSORPTION: opts <= {A, c, b12} with b12 = B12t(S-7)
    # (the a=7 child position (6)+Y lands exactly on the B12 cell),
    # a7 == b12 always -- the ONLY S=15 shape (7,8) carries the excess
    # option value 2 = B12t(8) where v(15,12,20) = 0, and mex is
    # unaffected (verified here as data, not asserted as law).
    base = {'ok': 0, 'bad': 0, 'det': []}
    for X in D33_shapes(7):
        S = sum(X)
        hv = H_ordered(20, X, 12)
        exp = v(S, 12, 20)
        A = v(S-1, 12, 19); c = 1 ^ v(S, 11, 19)
        opts = child_opts_ordered(X, 12, 20)
        a7 = am_child_value(X, 7, 12, 20)
        b12 = B12t(S - 7)
        if opts <= {A, c, b12} and a7 == b12 and hv == exp:
            base['ok'] += 1
        else:
            base['bad'] += 1
            base['det'].append([list(X), sorted(opts), a7, b12, hv, exp])
        clear()
    out['base_m7'] = base
    print('base m7', base['ok'], base['bad'])
    # P6b induction m in {8..12} x 33 (z=12, R = m + 13)
    ind = {'ok': 0, 'bad': 0, 'det': []}
    for m in range(8, 13):
        R = m + 13
        for X in D33_shapes(m):
            S = sum(X)
            hv = H_ordered(R, X, 12)
            exp = v(S, 12, R)
            A = v(S - 1, 12, R - 1); c = 1 ^ v(S, 11, R - 1)
            opts = child_opts_ordered(X, 12, R)
            if opts == {A, c} and hv == exp:
                ind['ok'] += 1
            else:
                ind['bad'] += 1
                ind['det'].append([m, list(X), sorted(opts), A, c, hv, exp])
            clear()
    out['induction'] = ind
    print('induction', ind['ok'], ind['bad'])
    # P7 E12 conditional- and ghost-form consistency over 3,657
    cond_bad = 0; ghost_bad = 0; cond_det = []
    for s in [0] + list(range(3, 41)):
        for Y in decomps(s, 3):
            opts = child_opts_ordered((3,) + Y, 12, 16)
            expc = {G12t(s), 1 ^ E11t(s)}
            if any(t >= 4 for t in Y):
                expc = expc | {v(s + 2, 12, 15)}
            if opts != expc:
                cond_bad += 1
                if len(cond_det) < 8: cond_det.append([s, list(Y)])
            expu = {G12t(s), 1 ^ E11t(s), v(s + 2, 12, 15)}
            if opts != expu: ghost_bad += 1
        clear()
    out['E12_forms'] = {'cond_mismatch': cond_bad, 'ghost_mismatch': ghost_bad,
                        'det': cond_det}
    print('E12 forms: cond', cond_bad, 'ghost', ghost_bad)
    # P8 D12 loose census (singleton 4, tokens 3..9): decomposition-dependence
    fam = Y_tokens(3, 9)
    vals = {}; sdep = set()
    for Y in fam:
        s = sum(Y)
        hv = H_canonical(17, (4,) + Y, 12)
        if s in vals and vals[s] != hv: sdep.add(s)
        vals.setdefault(s, hv)
    clear()
    out['D12_loose'] = {'family': len(fam), 'decomp_dependent_s': sorted(sdep)}
    print('D12 loose dep s:', sorted(sdep))
    # P9 z=13 census (OBSERVATION ONLY; next lane; no z=13 claims)
    z13 = {}
    for nm, pre, R, dvoff, tmin in [('F13', (1,), 15, 1, 3),
                                    ('G13', (2,), 16, 2, 3),
                                    ('E13', (3,), 17, 3, 3),
                                    ('D13', (4,), 18, 4, 5),
                                    ('C13', (5,), 19, 5, 6),
                                    ('B13', (6,), 20, 6, 7),
                                    ('A13', (7,), 21, 7, 8)]:
        fam = Y_tokens(tmin, 9)
        vals = {}; sonly = True; devs = []; sdep = set()
        for Y in fam:
            s = sum(Y)
            hv = H_canonical(R, pre + Y, 13)
            if s in vals and vals[s] != hv: sonly = False; sdep.add(s)
            vals.setdefault(s, hv)
            if hv != v(s + dvoff, 13, R): devs.append([list(Y), s, hv, v(s + dvoff, 13, R)])
        clear()
        z13[nm] = {'n': len(fam), 's_only': sonly, 'ndev': len(devs),
                   'decomp_dependent_s': sorted(sdep),
                   'deviants': devs[:12],
                   'table_s20': {str(k2): vals[k2] for k2 in sorted(vals) if k2 <= 20}}
        print('z13', nm, z13[nm]['n'], 's_only', sonly, 'sdep', sorted(sdep), 'ndev', len(devs))
    # (a2) D13 loose family (singleton 4, tokens 3..9)
    fam = Y_tokens(3, 9)
    vals = {}; sdep13 = set(); devs13 = []
    for Y in fam:
        s = sum(Y)
        hv = H_canonical(18, (4,) + Y, 13)
        if s in vals and vals[s] != hv: sdep13.add(s)
        vals.setdefault(s, hv)
        if hv != v(s + 4, 13, 18): devs13.append([list(Y), s, hv, v(s + 4, 13, 18)])
    clear()
    z13['D13loose'] = {'n': len(fam), 'decomp_dependent_s': sorted(sdep13),
                       'ndev': len(devs13), 'deviants': devs13[:12],
                       'table_s20': {str(k2): vals[k2] for k2 in sorted(vals) if k2 <= 20}}
    print('z13 D13loose', fam and len(fam), 'sdep', sorted(sdep13), 'ndev', len(devs13))
    out['z13_cells'] = z13
    # P9b z=13 strip census (OBSERVATION ONLY)
    zs = {}
    for m in range(5, 13):
        R = m + 14
        fam = T_shapes(m) if m in (5, 6, 7) else census96(m)
        okc = bad = 0; seps = []
        for X in fam:
            hv = H_canonical(R, X, 13)
            exp = v(sum(X), 13, R)
            if hv != exp: bad += 1; seps.append([list(X), hv, exp])
            else: okc += 1
        clear()
        zs[str(m)] = {'n': len(fam), 'ok': okc, 'bad': bad, 'seps': seps[:10]}
        print('strip z=13 m', m, okc, bad)
    out['strip_z13'] = zs
    # P10 crosscheck: fresh z=12 census recomputed with the published
    # predecl_z11.json enumeration, compared deep-equal against the
    # published record (fetched copy in published/predecl_z11.json).
    refpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'published', 'predecl_z11.json')
    ref = json.load(open(refpath))
    match = True; mdet = []
    z12c = {}
    for nm, pre, R, dvoff, tmin in [('F12', (1,), 14, 1, 3),
                                    ('G12', (2,), 15, 2, 3),
                                    ('E12', (3,), 16, 3, 3),
                                    ('D12', (4,), 17, 4, 5),
                                    ('C12', (5,), 18, 5, 6),
                                    ('B12', (6,), 19, 6, 7),
                                    ('A12', (7,), 20, 7, 8)]:
        fam = Y_tokens(tmin, 9)
        vals = {}; sonly = True; devs = []
        for Y in fam:
            s = sum(Y)
            hv = H_canonical(R, pre + Y, 12)
            if s in vals and vals[s] != hv: sonly = False
            vals.setdefault(s, hv)
            if hv != v(s + dvoff, 12, R): devs.append([list(Y), s, hv, v(s + dvoff, 12, R)])
        clear()
        z12c[nm] = {'n': len(fam), 's_only': sonly, 'ndev': len(devs),
                    'deviants': devs[:12],
                    'table_s20': {str(k2): vals[k2] for k2 in sorted(vals) if k2 <= 20}}
        if z12c[nm] != ref['z12_cells'][nm]:
            match = False; mdet.append([nm, 'cell'])
        print('z12 census recheck', nm, 'ndev', z12c[nm]['ndev'])
    fam = Y_tokens(3, 9)
    vals = {}; sonly = True; devs = []
    for Y in fam:
        s = sum(Y)
        hv = H_canonical(17, (4,) + Y, 12)
        if s in vals and vals[s] != hv: sonly = False
        vals.setdefault(s, hv)
        if hv != v(s + 4, 12, 17): devs.append([list(Y), s, hv, v(s + 4, 12, 17)])
    clear()
    z12c['D12loose'] = {'n': len(fam), 's_only': sonly, 'ndev': len(devs),
                        'deviants': devs[:12],
                        'table_s20': {str(k2): vals[k2] for k2 in sorted(vals) if k2 <= 20}}
    if z12c['D12loose'] != ref['z12_cells']['D12loose']:
        match = False; mdet.append(['D12loose', 'cell'])
    smatch = True
    for m in range(5, 13):
        R = m + 13
        fam = T_shapes(m) if m in (5, 6, 7) else census96(m)
        okc = bad = 0; seps = []
        for X in fam:
            hv = H_canonical(R, X, 12)
            exp = v(sum(X), 12, R)
            if hv != exp: bad += 1; seps.append([list(X), hv, exp])
            else: okc += 1
        clear()
        if {'ok': okc, 'bad': bad, 'n': len(fam), 'seps': seps[:10]} != ref['strip_z12'][str(m)]:
            smatch = False; mdet.append(['strip', m])
    out['crosscheck_published_z12_census'] = {
        'census_deep_match': match, 'strip_deep_match': smatch, 'det': mdet}
    print('crosscheck vs published predecl_z11.json: census', match,
          'strip', smatch)
    json.dump(out, open('predecl_z12.json', 'w'), indent=1)
    print('part2 written')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'part1')
