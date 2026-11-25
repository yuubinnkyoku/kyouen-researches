"""Pre-declaration exploration, PART 2 of 2, for the z=10 slice
(min>=7 band of the critical strip; K1278 candidate).

EXPLORATION ONLY -- no claims. Part 2 consumes part1_z10.json (the
full-family s-only tables of F10/G10/E10/D10/C10/B10/A10) and checks:

  P5   z=10 strip grid m in {5..12} x 222 T-shapes (R=m+11):
       per-m collapse count + separation records (out-of-band
       witnesses for m=5,6 expected; in-band rows m>=7 observed)
  P6   base m=7 structure (33 D33 shapes at R=18=m+11):
       parent options subset of {v(S-1,10,17) [stair],
                                 B10t(S-7) [a=7 child],
                                 1^v(S,9,17) [T-Z9 c' child]},
       a=7 child == B10t(S-7), parent mex == v(S,10,18)
  P7   induction m in {8..12} x 33 shapes (R=m+11): parent option
       set == {v(S-1,10,m+10), 1^v(S,9,m+10)} exactly (a>m stair +
       a=m C(m-1,10) + T-Z9 c' child), parent == v(S,10,m+11)
  P8   cell recursion identities (mismatch counts, theorem-free
       structural facts; c'-children use the PUBLISHED K1277 tables
       F9t..B9t and T-Z9 collapse values):
       F10 {v(s,11,11), v(s,10,11), 1^F9t(s)}               3,657
       G10 {F10t(s), v(s+1,10,12), 1^G9t(s)}                3,657
       E10 cond {G10t(s), 1^E9t(s)} + ghost {v(s+2,10,13)}  3,657
            (both conditional AND unconditional counted: the
             z-fate of the E-rank ghost law: z=8 broke at (3,3),
             z=9 coincided, z=10 = ?)
       D10 {v(s+3,10,14), E10t(s), 1^D9t(s)}                1,650
       C10 {v(s+4,10,15), D10t(s), 1^C9t(s)}                1,078
       B10 {v(s+5,10,16), C10t(s), 1^B9t(s)} [T-Z9 dep]        700
       A10 {v(s+6,10,17), B10t(s), 1^v(s+7,9,17)} [T-Z9 dep]   460
  P9   z=11 next-lane census (open registration): F11/G11/E11
       census 330 each (tokens 3..9), D11 floored census 126 +
       D11 loose 330, C11 floored 70, B11 floored 35, A11 floored
       15, z=11 strip m in {6..11} x 96 census shapes
  P10  crosscheck against the published K1277 audit z10_cells
       census (audit.json sha256 9c0294e9dc413c422a88be17d64aa0325
       aad5236eca2bcb3885e8988473b79ae): the published bounded
       tables must be subtables of the full-family P1 part1 tables

Engine provenance: sha-gated mechanical cut from the published K1264
verifier, pin bd5f22e4... (identical to the published chain). No hand
transcription.
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

BASE = os.path.dirname(os.path.abspath(__file__))
SRC1 = os.path.join(BASE, 'generalx-min-token-lowr-staircase-20261123',
                    'verify_min_token_staircase.py')
SRC1_PIN = '108fdd65a96588b32cfd64503cf2a22f999d6e4eefded775bb6fda32568e69fa'
ENGINE_PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
K1277_AUDIT = os.path.join(BASE, 'published', 'k1277_audit.json')
K1277_AUDIT_PIN = ('9c0294e9dc413c422a88be17d64aa0325aad5236eca2bcb'
                   '3885e8988473b79ae')

data = open(SRC1, 'rb').read()
assert hashlib.sha256(data).hexdigest() == SRC1_PIN, 'K1264 verifier sha mismatch'
engine = cut_k1264(data.decode('utf-8'))
assert hashlib.sha256(engine.encode('utf-8')).hexdigest() == ENGINE_PIN, 'engine pin mismatch'
print('engine block sha256 OK:', ENGINE_PIN, flush=True)
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

# published K1277 (z=9) cell tables -- K1277 is proved and published
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

# part1 full-family tables (verified s-only in part 1)
p1 = json.load(open(os.path.join(BASE, 'part1_z10.json')))
for tag in ['F10', 'G10', 'E10', 'D10', 'C10', 'B10', 'A10']:
    assert p1[tag]['s_only'] and p1[tag]['engine_bad'] == 0, tag
TAB = {tag: {int(k): v[0] for k, v in p1[tag]['table'].items()}
        for tag in ['F10', 'G10', 'E10', 'D10', 'C10', 'B10', 'A10']}
def T10(tag, s):
    v = TAB[tag].get(s)
    if v is None: raise KeyError('s=%d not swept for %s' % (s, tag))
    return v

res = {}

print('== P5 z=10 strip grid m in {5..12} x 222 (R=m+11) ==', flush=True)
strip = {}
for m in range(5, 13):
    z, R = 10, m + 11
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
            if len(seps) < 8:
                seps.append([list(X), hc, single_token(S, z, R)])
    strip[m] = {'total': total, 'collapse': total - coll,
                'engine_bad': engine_bad, 'separations': seps}
    clear_engines()
    print('z10 strip m=%d: %d/%d collapse engine_bad=%d seps=%s' %
          (m, strip[m]['collapse'], total, engine_bad,
           json.dumps(seps[:4])), flush=True)
res['P5_strip'] = strip

print('== P6 base m=7 structure (R=18=m+11, 33 shapes) ==', flush=True)
bad_opts = bad_am = bad_mex = engine_bad = pts = 0
details = []
for X in D33_shapes(7):
    S = sum(X)
    hc = H_canonical(18, X, 10)
    ho = H_ordered(18, X, 10)
    pts += 1
    if hc != ho: engine_bad += 1
    opts = child_opts_ordered(X, 10, 18)
    allowed = set()
    for i, w in enumerate(X):
        if w > 7:
            allowed.add(single_token(S - 1, 10, 17))
    if 7 in X:
        allowed.add(T10('B10', S - 7))
    allowed.add(1 ^ single_token(S, 9, 17))  # T-Z9 c' child
    if not opts <= allowed:
        bad_opts += 1
        details.append({'X': list(X), 'opts': sorted(opts),
                        'allowed': sorted(allowed)})
    if 7 in X:
        amv = am_child_value(X, 7, 10, 18)
        if amv != T10('B10', S - 7):
            bad_am += 1
            details.append({'X': list(X), 'am': amv,
                            'B10t': T10('B10', S - 7)})
    if hc != single_token(S, 10, 18):
        bad_mex += 1
        details.append({'X': list(X), 'parent': hc,
                        'single': single_token(S, 10, 18)})
res['P6_base_m7'] = {'points': pts, 'engine_bad': engine_bad,
                     'bad_opts': bad_opts, 'bad_am': bad_am,
                     'bad_mex': bad_mex, 'details': details[:10]}
clear_engines()
print('base m=7: pts=%d engine_bad=%d bad_opts=%d bad_am=%d bad_mex=%d' %
      (pts, engine_bad, bad_opts, bad_am, bad_mex), flush=True)

print('== P7 induction m in {8..12} x 33 (R=m+11) ==', flush=True)
bad = engine_bad = pts = 0
details = []
for m in range(8, 13):
    z, R = 10, m + 11
    for X in D33_shapes(m):
        S = sum(X)
        hc = H_canonical(R, X, z)
        ho = H_ordered(R, X, z)
        pts += 1
        if hc != ho: engine_bad += 1
        opts = child_opts_ordered(X, z, R)
        exp = {single_token(S - 1, z, R - 1),
               1 ^ single_token(S, 9, R - 1)}
        if opts != exp:
            bad += 1
            details.append({'m': m, 'X': list(X), 'opts': sorted(opts),
                            'exp': sorted(exp)})
        if hc != single_token(S, z, R):
            bad += 1
            details.append({'m': m, 'X': list(X), 'parent': hc,
                            'single': single_token(S, z, R)})
    clear_engines()
res['P7_induction'] = {'points': pts, 'engine_bad': engine_bad,
                       'bad': bad, 'details': details[:10]}
print('induction: pts=%d engine_bad=%d bad=%d' % (pts, engine_bad, bad),
      flush=True)

print('== P8 recursion identities ==', flush=True)
def rec_ident(tag, pre, R, tmin, expfun, ghost=None):
    pts = 0; badengine = 0; mismatch = 0; g_mismatch = 0
    details = []
    srange = sorted(set([0] + list(range(tmin, 41))))
    for s in srange:
        for Y in decomps(s, tmin):
            X = pre + Y
            hc = H_canonical(R, X, 10)
            ho = H_ordered(R, X, 10)
            pts += 1
            if hc != ho: badengine += 1
            opts = child_opts_ordered(X, 10, R)
            exp = set(expfun(s))
            has4 = any(w >= tmin + 1 for w in Y)  # >=floor+1 token present
            if ghost is not None:
                cond = set(exp)
                if has4: cond.add(ghost(s))
                if opts != cond:
                    mismatch += 1
                    details.append({'s': s, 'Y': list(Y),
                                    'opts': sorted(opts),
                                    'exp': sorted(cond)})
                uncond = set(exp) | {ghost(s)}
                if opts != uncond:
                    g_mismatch += 1
                # ghost value when absent from exp (census direction)
            else:
                exp = set(expfun(s))
                if opts != exp:
                    mismatch += 1
                    details.append({'s': s, 'Y': list(Y),
                                    'opts': sorted(opts),
                                    'exp': sorted(exp)})
    clear_engines()
    res['P8_' + tag] = {'points': pts, 'badengine': badengine,
                        'mismatch': mismatch,
                        'ghost_uncond_mismatch': g_mismatch,
                        'details': details[:8]}
    print('P8 %s pts=%d badeng=%d mismatch=%d ghost_uncond=%d' %
          (tag, pts, badengine, mismatch, g_mismatch), flush=True)

rec_ident('F10', (1,), 12, 3,
          lambda s: {single_token(s, 11, 11), single_token(s, 10, 11),
                     1 ^ F9t(s)})
rec_ident('G10', (2,), 13, 3,
          lambda s: {T10('F10', s), single_token(s + 1, 10, 12),
                     1 ^ G9t(s)})
rec_ident('E10', (3,), 14, 3,
          lambda s: {T10('G10', s), 1 ^ E9t(s)},
          ghost=lambda s: single_token(s + 2, 10, 13))
rec_ident('D10', (4,), 15, 5,
          lambda s: {single_token(s + 3, 10, 14), T10('E10', s),
                     1 ^ D9t(s)})
rec_ident('C10', (5,), 16, 6,
          lambda s: {single_token(s + 4, 10, 15), T10('D10', s),
                     1 ^ C9t(s)})
rec_ident('B10', (6,), 17, 7,
          lambda s: {single_token(s + 5, 10, 16), T10('C10', s),
                     1 ^ B9t(s)})
rec_ident('A10', (7,), 18, 8,
          lambda s: {single_token(s + 6, 10, 17), T10('B10', s),
                     1 ^ single_token(s + 7, 9, 17)})

print('== P9 z=11 next-lane census (open registration) ==', flush=True)
z11cells = {}
for tag, pre, R, dvoff, tmin, tmax in [
        ('F11', (1,), 13, 1, 3, 9), ('G11', (2,), 14, 2, 3, 9),
        ('E11', (3,), 15, 3, 3, 9), ('D11', (4,), 16, 4, 5, 9),
        ('C11', (5,), 17, 5, 6, 9), ('B11', (6,), 18, 6, 7, 9),
        ('A11', (7,), 19, 7, 8, 9)]:
    fam = Y_tokens(tmin, tmax)
    tbl = {}; devs = []; engine_bad = 0
    for Y in fam:
        s = sum(Y)
        hc = H_canonical(R, pre + Y, 11)
        ho = H_ordered(R, pre + Y, 11)
        if hc != ho: engine_bad += 1
        tbl.setdefault(s, set()).add(hc)
        if hc != single_token(s + dvoff, 11, R):
            devs.append(list(Y))
    dep = [s for s, v in sorted(tbl.items()) if len(v) > 1]
    z11cells[tag] = {'R': R, 'floor': tmin, 'family': len(fam),
                     'engine_bad': engine_bad,
                     'decomp_dependent_s': dep,
                     'deviant_count': len(devs),
                     'deviants_vs_collapse': devs[:40],
                     'table_s20': {str(s): sorted(v)
                                   for s, v in sorted(tbl.items())
                                   if s <= 20}}
    clear_engines()
    print('%s family=%d dep_s=%s dev_count=%d engine_bad=%d' %
          (tag, len(fam), dep, z11cells[tag]['deviant_count'],
           engine_bad), flush=True)
# D11 loose
fam = Y_tokens(3, 9)
tbl = {}; devs = []; engine_bad = 0
for Y in fam:
    s = sum(Y)
    hc = H_canonical(16, (4,) + Y, 11)
    ho = H_ordered(16, (4,) + Y, 11)
    if hc != ho: engine_bad += 1
    tbl.setdefault(s, set()).add(hc)
    if hc != single_token(s + 4, 11, 16):
        devs.append(list(Y))
dep = [s for s, v in sorted(tbl.items()) if len(v) > 1]
z11cells['D11_loose'] = {'R': 16, 'floor': 3, 'family': len(fam),
                         'engine_bad': engine_bad,
                         'decomp_dependent_s': dep,
                         'deviant_count': len(devs),
                         'deviants_vs_collapse': devs[:40],
                         'table_s20': {str(s): sorted(v)
                                       for s, v in sorted(tbl.items())
                                       if s <= 20}}
clear_engines()
print('D11_loose family=%d dep_s=%s dev_count=%d' %
      (len(fam), z11cells['D11_loose']['decomp_dependent_s'],
       z11cells['D11_loose']['deviant_count']), flush=True)
res['P9_z11_cells'] = z11cells

z11strip = {}
for m in range(6, 12):
    z, R = 11, m + 12
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
    z11strip[m] = {'total': total, 'collapse': total - coll,
                   'engine_bad': engine_bad, 'separations': seps}
    clear_engines()
    print('z11 strip m=%d: %d/%d collapse seps=%s' %
          (m, z11strip[m]['collapse'], total,
           json.dumps(seps[:4])), flush=True)
res['P9_z11_strip'] = z11strip

print('== P10 crosscheck vs published K1277 audit z10_cells ==', flush=True)
data = open(K1277_AUDIT, 'rb').read()
assert hashlib.sha256(data).hexdigest() == K1277_AUDIT_PIN
k1277 = json.loads(data.decode('utf-8'))
pubcells = k1277['D6c_census']['census']['z10_cells']
mine = {tag: p1[tag] for tag in
        ['F10', 'G10', 'E10', 'D10', 'C10', 'B10', 'A10', 'D10_loose']}
match = True
for tag, pv in mine.items():
    pc = pubcells[tag]
    a = {int(k): v for k, v in pv['table'].items()}
    b = pc['table_s20']
    for k, vv in b.items():
        if sorted(a.get(int(k), [])) != sorted(vv):
            match = False
            print('table mismatch at', tag, 's=', k, flush=True)
            print(' mine:', json.dumps(a.get(int(k))),
                  ' pub:', json.dumps(vv), flush=True)
    if pv['engine_bad'] != 0 or pc.get('engine_bad', 0) != 0:
        match = False
        print('engine bad mismatch at', tag, flush=True)
res['P10_crosscheck'] = {'match': match}
print('P10 crosscheck match =', match, flush=True)

out_path = os.path.join(BASE, 'part2_z10.json')
with open(out_path, 'w') as f:
    f.write(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=True)
            + '\n')
print('WROTE', out_path)
print('PART 2 COMPLETE')
