#!/usr/bin/env python3
"""probe_z11_predecl.py -- pre-declaration exploration machine for the
z=11 critical-strip slice (min>=7 band; provisional K1280). Deterministic,
zero hand transcription of values: all claimed values are computed by the
pinned raw engines (engine block sha256 bd5f22e415a78368c9b798296bc84948d5
637decbf3c21a92404d45fb12e3a92, machine-cut from the published K1279
verifier verify_strip_z10.py). Observation only: NO claims are made by this
probe. Outputs predecl_z11.json (part1: P1-P4c cell sweeps; part2: P5-P8
strip/structure/census/crosscheck).

Usage: python3 probe_z11_predecl.py part1|part2
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

# candidate closed forms for the z=11 cells (derived from the published
# z=10 tables via the cell recursions; to be CONFIRMED below against the
# raw engines -- this probe itself claims nothing)
def F11t(s): return {0:1,3:0,4:1,5:0,6:1,7:0,8:1,9:0,10:1,11:0}.get(s, 2)
def G11t(s): return {0:0,3:1,4:0,5:1,6:0,7:1,8:0,9:1,10:0,11:1}.get(s, 1)
def E11t(s): return {0:1,3:0,4:1,5:0,6:1,7:0,8:1,9:0,10:2}.get(s, 0)
def D11t(s): return {8:0}.get(s, v(s+4,11,16))
def C11t(s): return {6:1, 8:2}.get(s, v(s+5,11,17))
def B11t(s): return v(s+6,11,18)
def A11t(s): return v(s+7,11,19)

# published z=10 closed forms (K1279) used by the recursions / ghost forms
def F10t(s): return {0:1,3:0,4:1,5:0,6:1,7:0,8:1,9:0,10:1}.get(s, 0)
def G10t(s): return {0:0,3:1,4:0,5:1,6:0,7:1,8:0,9:1,10:2}.get(s, 1)
def E10t(s): return {0:1,3:0,4:1,5:0,6:1,7:0,8:1}.get(s, 0)

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
        cells = [('F11', 13, 1, 3, S3, F11t),
                 ('G11', 14, 2, 3, S3, G11t),
                 ('E11', 15, 3, 3, S3, E11t),
                 ('D11', 16, 4, 5, [0]+list(range(5,41)), D11t),
                 ('C11', 17, 5, 6, [0]+list(range(6,41)), C11t),
                 ('B11', 18, 6, 7, [0]+list(range(7,41)), B11t),
                 ('A11', 19, 7, 8, [0]+list(range(8,41)), A11t)]
        for nm, R, sgl, tmin, sdom, tab in cells:
            out[nm] = sweep_cell(nm, R, 11, sgl, tmin, sdom, tab)
            print(nm, out[nm]['points'], out[nm]['comparisons'], 'bad', out[nm]['bad'])
        json.dump(out, open('part1_z11.json', 'w'), indent=1)
        print('part1 written,', sum(o['points'] for o in out.values()), 'points,',
              sum(o['comparisons'] for o in out.values()), 'comparisons')
        return
    # part2
    p1 = json.load(open('part1_z11.json'))
    out['cells'] = p1
    # P5 strip z=11 m in {5..12} x 222
    strip = {}
    for m in range(5, 13):
        R = m + 12
        okc = bad = 0; seps = []
        for X in T_shapes(m):
            hv = H_canonical(R, X, 11)
            exp = v(sum(X), 11, R)
            if hv != exp: bad += 1; seps.append([ list(X), hv, exp ])
            else: okc += 1
        clear()
        strip[str(m)] = {'ok': okc, 'bad': bad, 'n': 222, 'seps': seps[:10]}
        print('strip z=11 m', m, strip[str(m)]['ok'], strip[str(m)]['bad'])
    out['strip_z11'] = strip
    # P6 base m=7 structure (33 shapes)
    base = {'ok': 0, 'bad': 0, 'det': []}
    for X in D33_shapes(7):
        S = sum(X)
        hv = H_ordered(19, X, 11)
        exp = v(S, 11, 19)
        A = v(S-1, 11, 18); c = 1 ^ v(S, 10, 18)
        opts = child_opts_ordered(X, 11, 19)
        a7 = am_child_value(X, 7, 11, 19)
        b11 = B11t(S - 7)
        if opts <= {A, c, b11} and a7 == b11 and hv == exp:
            base['ok'] += 1
        else:
            base['bad'] += 1
            base['det'].append([list(X), sorted(opts), a7, b11, hv, exp])
        clear()
    out['base_m7'] = base
    print('base m7', base['ok'], base['bad'])
    # P6b induction m in {8..12} x 33
    ind = {'ok': 0, 'bad': 0, 'det': []}
    for m in range(8, 13):
        R = m + 12
        for X in D33_shapes(m):
            S = sum(X)
            hv = H_ordered(R, X, 11)
            exp = v(S, 11, R)
            A = v(S - 1, 11, R - 1); c = 1 ^ v(S, 10, R - 1)
            opts = child_opts_ordered(X, 11, R)
            if opts == {A, c} and hv == exp:
                ind['ok'] += 1
            else:
                ind['bad'] += 1
                ind['det'].append([m, list(X), sorted(opts), A, c, hv, exp])
            clear()
    out['induction'] = ind
    print('induction', ind['ok'], ind['bad'])
    # P7 E11 conditional- and ghost-form consistency over 3,657
    cond_bad = 0; ghost_bad = 0; cond_det = []
    for s in [0] + list(range(3, 41)):
        for Y in decomps(s, 3):
            opts = child_opts_ordered((3,) + Y, 11, 15)
            expc = {G11t(s), 1 ^ E10t(s)}
            if any(t >= 4 for t in Y):
                expc = expc | {v(s + 2, 11, 14)}
            if opts != expc:
                cond_bad += 1
                if len(cond_det) < 8: cond_det.append([s, list(Y)])
            expu = {G11t(s), 1 ^ E10t(s), v(s + 2, 11, 14)}
            if opts != expu: ghost_bad += 1
        clear()
    out['E11_forms'] = {'cond_mismatch': cond_bad, 'ghost_mismatch': ghost_bad,
                        'det': cond_det}
    print('E11 forms: cond', cond_bad, 'ghost', ghost_bad)
    # P8 D11 loose census (tokens 3..9)
    fam = Y_tokens(3, 9)
    vals = {}; sdep = set()
    for Y in fam:
        s = sum(Y)
        hv = H_canonical(16, (4,) + Y, 11)
        if s in vals and vals[s] != hv: sdep.add(s)
        vals.setdefault(s, hv)
    clear()
    out['D11_loose'] = {'family': len(fam), 'decomp_dependent_s': sorted(sdep)}
    print('D11 loose dep s:', sorted(sdep))
    # P9 z=12 census (observation only, next lane)
    z12 = {}
    for nm, R, sgl, tmin in [('F12',14,1,3), ('G12',15,2,3), ('E12',16,3,3),
                             ('D12',17,4,5), ('D12loose',17,4,3), ('C12',18,5,6),
                             ('B12',19,6,7), ('A12',20,7,8)]:
        k = sgl
        fam = Y_tokens(tmin, 9)
        vals = {}; sonly = True; devs = []
        for Y in fam:
            s = sum(Y)
            hv = H_canonical(R, (sgl,) + Y, 12)
            if s in vals and vals[s] != hv: sonly = False
            vals.setdefault(s, hv)
            if hv != v(s + k, 12, R): devs.append([list(Y), s, hv, v(s + k, 12, R)])
        clear()
        z12[nm] = {'n': len(fam), 's_only': sonly, 'ndev': len(devs),
                   'deviants': devs[:12], 'table_s20': {str(k2): vals[k2] for k2 in sorted(vals) if k2 <= 20}}
        print('z12', nm, z12[nm]['n'], 's_only', sonly, 'ndev', len(devs))
    out['z12_cells'] = z12
    # P9b z=12 strip census
    zs = {}
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
        zs[str(m)] = {'n': len(fam), 'ok': okc, 'bad': bad, 'seps': seps[:10]}
        print('strip z=12 m', m, okc, bad)
    out['strip_z12'] = zs
    # P10 crosscheck vs published K1279 audit z11_census
    ref = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      'published', 'k1279_audit.json')))
    z11c = ref['D6c_census']['census']['z11_cells']
    match = True; mdet = []
    mytab = {'F11': F11t, 'G11': G11t, 'E11': E11t, 'D11': D11t, 'C11': C11t,
             'B11': B11t, 'A11': A11t}
    for nm, tab in mytab.items():
        ref_tab = z11c[nm]['table_s20']
        for ss, refvals in ref_tab.items():
            s = int(ss)
            lo, hi = sorted([0, 40])
            if s > 40: continue
            if refvals != [tab(s)]:
                match = False; mdet.append([nm, s, refvals, tab(s)])
        if nm != 'D11_loose' and sorted(tuple(d) for d in z11c[nm]['deviants_vs_collapse']) != []:
            pass  # deviant full sets are compared in the audit machine
    out['crosscheck_k1279_z11census'] = {'table_match_s20': match, 'det': mdet[:8]}
    print('crosscheck vs published K1279 z11_census table_match:', match)
    json.dump(out, open('predecl_z11.json', 'w'), indent=1)
    print('part2 written')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'part1')
