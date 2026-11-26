#!/usr/bin/env python3
"""derive_check_kit9b.py: ENGINE-FREE pre-freeze verification of the
second-census explorer explore_m33m34_second_census.py. No raw engine
is invoked anywhere: every check is paper arithmetic on the published
K0832 closed form (independent re-transcription below) plus structural
comparison against the PUBLISHED kit-8 / kit-8b chain artifacts.

Checks:
 (A) embedded constants parse; counts 34/6/3/16/59/232/1594/39.
 (B) every row: R=m+z+1, smax=max(m+38,z+2), co-token registration,
     unique labels/sections; exactly 4 smax z+2 extensions
     (m19 z58/z59, m20 z59/z60).
 (C) every collapse literal "v(a,b,c)=d" in every candidate / tracker
     / split / future text: vv(a,b,c)==d (local closed form).
 (D) direction claims "UP 2v0 (collapse v(a,b,c)=d)": vv(a,b,c)==d and
     the claimed value is consistent with UP/DOWN ordering.
 (E) 34 binding texts: independently re-derived from the lifecycle
     formulas are prefixes of the embedded texts (transcription).
 (F) anchors 0..179 content-identical to the PUBLISHED kit-8 explorer
     anchor table; new 52 = exactly the kit-8 .out separation spots
     not already anchored, same published values.
 (G) battery: 1594 valid triples, superset of the published kit-8
     battery (order-normalized).
 (H) kit-10 future constants: 38 items independently re-derived
     (prefix match) + the smax note appended at this build.
 (I) engine pin: embedded ENGINE_BLOCK sha256 == the chain startup pin
     bd5f22e4... and the disclosed clone sha 582c93c1... matches
     engine_block.py = ENGINE_BLOCK + import line.
"""
import json, re, ast, hashlib, os, sys

CAND = ['explore_m33m34_second_census.py', 'kit9b/explore_m33m34_second_census.py']

def find(names):
    for n in names:
        if os.path.exists(n):
            return n
    raise FileNotFoundError(names)

K8_EXPLORER = find(['explore_m31m32_ladders_trio.py',
                    'kit9b/explore_m31m32_ladders_trio.py',
                    'research_experiments_strip-newband-m31m32-'
                    'ladders-trio-20261126_explore_m31m32_ladders_trio.py'])
K8_OUT = find([K8_EXPLORER[:-3] + '.out'])

def embed(src, name):
    m = re.search(name + r" = '(.*?)'\n", src, re.S)
    assert m, name
    return json.loads(ast.literal_eval("'" + m.group(1) + "'"))

src = open(find(CAND)).read()
ROWS = embed(src, 'ROWS_JSON')
REG = embed(src, 'REGISTRATIONS_JSON')
ANCHORS = embed(src, 'ANCHOR_SPEC_JSON')
BATTERY = embed(src, 'BATTERY_JSON')
FUTURE = embed(src, 'FUTURE_BODY_JSON')
AMETA = embed(src, 'ANCHOR_META_JSON')

# ---- local closed form (independent transcription) ----
def vv(x, z, R):
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
    q = lambda k: k if k % 2 else k - 1
    if 1 <= z <= x - 1:
        m = q(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))

zstar = lambda m: 2 * m - 2 + (m % 2)
co = lambda m, d: (m + 2 * d + 1 if m % 2 else m + 2 * d)
S_of = lambda m, d: (2 * m + 2 * d + 1 if m % 2 else 2 * m + 2 * d)

fail = 0
def ck(cond, label):
    global fail
    if not cond:
        fail += 1
        print('FAIL:', label)

# (A)
ck(len(REG['binding']) == 34, 'binding 34')
ck(len(REG['lifecycle']) == 6, 'lifecycle 6')
ck(len(REG['even']) == 3, 'even 3')
ck(len(REG['windows']) == 2 and
   sorted(int(k) for k in REG['windows']) == [31, 32], 'windows keys')
ck(sum(len(v) for v in REG['windows'].values()) == 16, 'windows 16')
ck(len(ROWS) == 59, 'rows 59')
ck(len(ANCHORS) == 232, 'anchors 232')
ck(len(BATTERY) == 1594, 'battery 1594')
ck(len(FUTURE['registered_for_next_execution_kit10']) == 39, 'future 39')

# (B) row specs
ext = []
for r in ROWS:
    m, z, R = r['min'], r['z'], r['R']
    ck(R == m + z + 1, 'R=m+z+1 %s' % r['label'])
    ck(r['smax'] == max(m + 38, z + 2), 'smax %s' % r['label'])
    ck(r['smax'] > r['min'], 'smax>min %s' % r['label'])
    ck(r['co_token_key'] == 'co_token_%d_allowed' % m and
       r['co_token_val'] is True, 'co-token %s' % r['label'])
    ck(r['candidate'] and r['registered_by'] and r['seat_kind'],
       'text fields %s' % r['label'])
    if r['smax'] > m + 38:
        ext.append((m, z))
ck(len(ext) == 4 and set(ext) == {(19, 58), (19, 59), (20, 59), (20, 60)},
   'smax extensions = %s' % (ext,))
ck(len({r['label'] for r in ROWS}) == 59, 'labels unique')
ck(len({r['section'] for r in ROWS}) == 59, 'sections unique')

# (C) collapse literals in all texts
lit = re.compile(r'v\((\d+),(\d+),(\d+)\)=(\d)')
dirn = re.compile(r'(UP|DOWN) (\d)v(\d) \(collapse v\((\d+),(\d+),(\d+)\)=(\d)\)')
texts = []
for it in REG['binding'] + REG['lifecycle'] + REG['even']:
    texts.append(it['cand'])
    for tr in it.get('trackers') or []:
        texts.append(tr['cand'])
    for sp in it.get('registered_splits') or []:
        texts.append(sp['cand'])
for it in FUTURE['registered_for_next_execution_kit10']:
    texts.append(it.get('prediction', ''))
nlit = 0
for t in texts:
    for (a, b, c, d) in lit.findall(t):
        nlit += 1
        ck(vv(int(a), int(b), int(c)) == int(d),
           'literal v(%s,%s,%s)=%s' % (a, b, c, d))
    for (upval, val, col, a, b, c, d) in dirn.findall(t):
        ck(vv(int(a), int(b), int(c)) == int(d),
           'dir literal v(%s,%s,%s)=%s' % (a, b, c, d))
        ck((int(val) > int(col)) == (upval == 'UP'),
           'direction %s%sv%s' % (upval, val, col))
ck(nlit >= 100, 'literal count %d' % nlit)

# (D2) trackers/splits in-sweep structural checks
for it in REG['binding'] + REG['lifecycle'] + REG['even']:
    m = it['m']
    for tr in it.get('trackers') or []:
        X = sorted(tr['X'])
        ck(X[0] == m and sum(X) == tr['S'], 'tracker shape %s' % (X,))
    for sp in it.get('registered_splits') or []:
        X = sorted(sp['X'])
        ck(X[0] == m and sum(X) == sp['S'], 'split shape %s' % (X,))
        ck(len(X) == 3, 'split arity %s' % (X,))

# (E) binding texts re-derived (independent transcription)
def one_past_txt(m, d):
    z = zstar(m) + 2 * d + 1
    R = m + z + 1
    if m % 2:
        return ('EXACTLY ONE: {%d,%d}@S=%d UP 1v0 (collapse v(%d,%d,%d)=%d)'
                % (m, co(m, d), S_of(m, d), S_of(m, d), z, R,
                   vv(S_of(m, d), z, R)))
    return ('EXACTLY ONE: (%d,%d)@S=%d DOWN 0v1 (collapse v(%d,%d,%d)=%d)'
            % (m, co(m, d), S_of(m, d), S_of(m, d), z, R,
               vv(S_of(m, d), z, R)))

def birth_txt(m, d):
    z = S_of(m, d - 1)
    R = m + z + 1
    if m % 2:
        return ('EXACTLY TWO: stick {%d,%d} DOWN 1v2 (collapse v(%d,%d,%d)=%d)'
                % (m, co(m, d - 1), S_of(m, d - 1), z, R,
                   vv(S_of(m, d - 1), z, R))) + \
               (' + NEW {%d,%d}@S=%d UP 2v%d (collapse v(%d,%d,%d)=%d), '
                'd=%d seat gap %d' % (m, co(m, d), S_of(m, d),
                                      vv(S_of(m, d), z, R), S_of(m, d),
                                      z, R, vv(S_of(m, d), z, R), d,
                                      co(m, d) - m))
    return ('EXACTLY TWO: stick (%d,%d) DOWN 0v2 (collapse v(%d,%d,%d)=%d)'
            % (m, co(m, d - 1), S_of(m, d - 1), z, R,
               vv(S_of(m, d - 1), z, R))) + \
           (' + NEW (%d,%d)@S=%d UP 2v%d (collapse v(%d,%d,%d)=%d), '
            'd=%d seat gap %d' % (m, co(m, d), S_of(m, d),
                                  vv(S_of(m, d), z, R), S_of(m, d),
                                  z, R, vv(S_of(m, d), z, R), d,
                                  co(m, d) - m))

def frontier_txt(m):
    z = zstar(m)
    R = m + z + 1
    S = 2 * m + 1 if m % 2 else 2 * m
    if m % 2:
        return ('EXACTLY ONE: {%d,%d}@S=%d UP 2v%d (collapse v(%d,%d,%d)=%d)'
                % (m, m + 1, S, vv(S, z, R), S, z, R, vv(S, z, R)))
    return ('EXACTLY ONE: (%d,%d)@S=%d UP 2v%d (collapse v(%d,%d,%d)=%d)'
            % (m, m, S, vv(S, z, R), S, z, R, vv(S, z, R)))

derived = (
    [one_past_txt(19, 10), birth_txt(19, 11),
     one_past_txt(20, 10), birth_txt(20, 11),
     one_past_txt(21, 6), birth_txt(21, 7),
     one_past_txt(22, 6), birth_txt(22, 7),
     one_past_txt(23, 5), birth_txt(23, 6),
     one_past_txt(24, 5), birth_txt(24, 6),
     one_past_txt(25, 4), birth_txt(25, 5),
     one_past_txt(26, 4), birth_txt(26, 5),
     one_past_txt(27, 2), birth_txt(27, 3),
     one_past_txt(28, 2), birth_txt(28, 3),
     birth_txt(29, 2), one_past_txt(29, 2), birth_txt(29, 3),
     birth_txt(30, 2), one_past_txt(30, 2), birth_txt(30, 3),
     one_past_txt(31, 0), birth_txt(31, 1), one_past_txt(31, 1),
     one_past_txt(32, 0), birth_txt(32, 1), one_past_txt(32, 1),
     frontier_txt(33), frontier_txt(34)])
ck(len(derived) == 34, 'derived 34')
by_mz = {(it['m'], it['z']): it for it in REG['binding']}
for txt in derived:
    mm = re.search(r'v\((\d+),(\d+),(\d+)\)', txt)
    hits = [(it_m, it_z) for (it_m, it_z) in by_mz]
    # match by unique z literal set in the text
    lits = lit.findall(txt)
    matched = None
    for (k, it) in by_mz.items():
        if it['cand'].startswith(txt) or it['cand'] == txt:
            matched = k
            break
    ck(matched is not None, 'no binding row starts with derived text: %s'
       % txt[:60])
taken = set()
for txt in derived:
    for (k, it) in by_mz.items():
        if k in taken:
            continue
        if it['cand'].startswith(txt):
            taken.add(k)
            break
ck(len(taken) == 34, 'derived texts map 1-1 to binding rows %d' % len(taken))

# frontier K1268 double-check
ck(zstar(33) == 65 and zstar(34) == 66, 'K1268 z* 33/34')

# (F) anchors
k8src = open(K8_EXPLORER).read()
i = k8src.index('    anchor_spec = [')
k = k8src.index('[', i)
depth = 0
for p in range(k, len(k8src)):
    if k8src[p] == '[':
        depth += 1
    elif k8src[p] == ']':
        depth -= 1
        if depth == 0:
            break
k8spec = ast.literal_eval(k8src[k:p + 1])
ck(len(k8spec) == 180, 'kit-8 anchor table 180')
for idx in range(180):
    a, b = ANCHORS[idx], k8spec[idx]
    ck(a[0] == b[0] and list(a[1]) == list(b[1]) and a[2] == b[2]
       and a[3] == b[3], 'anchor[%d] inherited' % idx)

kout = json.loads(open(K8_OUT).read())
seps8 = {}
for sec in kout['sections']:
    for r in sec.get('rows', []) if isinstance(sec, dict) else []:
        pass
for sec in kout['sections']:
    if sec.get('section') == 'published_anchor_rechecks':
        continue
    for r in (sec.get('rows') or []):
        pass
# extract measured separations from every row record
for sec in kout['sections']:
    if 'separations' in sec:
        for s in sec['separations']:
            key = (sec['R'], tuple(sorted(s['X'], reverse=True)), sec['z'])
            seps8[key] = s['value']
ck(len(seps8) == 54, 'kit-8 .out separation spots %d' % len(seps8))
have = set((a[0], tuple(sorted(a[1], reverse=True)), a[2]) for a in k8spec)
new_keys = set()
for a in ANCHORS[180:]:
    key = (a[0], tuple(sorted(a[1], reverse=True)), a[2])
    new_keys.add(key)
    ck(key not in have, 'new anchor not already anchored %s' % (key,))
    ck(seps8.get(key) == a[3], 'new anchor value == kit-8 .out %s' % (key,))
expected_new = {k for k in seps8 if k not in have}
ck(new_keys == expected_new, 'new anchors = non-anchored kit-8 spots')

# (G) battery
m8 = re.search(r'BATTERY_TRIPLES_JSON = (\".*?\")\n', k8src, re.S)
k8bat = json.loads(ast.literal_eval(m8.group(1)))
k8set = {(t[0], t[1], t[2]) for t in k8bat}  # (x,z,R) storage
k9set = {(t[1], t[2], t[0]) for t in BATTERY}  # embedded is (R,x,z)
ck(k8set <= k9set, 'battery superset of kit-8 published battery')
for (x, z, R) in k9set:
    ck(vv(x, z, R) in (0, 1, 2), 'battery triple valid (%d,%d,%d)' % (x, z, R))
litset = {(int(a), int(b), int(c)) for t in texts
          for (a, b, c, d) in lit.findall(t)}
ck(litset <= k9set, 'battery covers every named collapse literal')

# (H) future constants
FUT = FUTURE['registered_for_next_execution_kit10']
fmap = {}
for it in FUT:
    if 'm' in it and 'z' in it:
        fmap.setdefault((it['m'], it['z']), []).append(it)
exp_rows = [[19, 60], [19, 61], [20, 61], [20, 62], [21, 57], [21, 58],
            [22, 58], [22, 59], [23, 58], [23, 59], [24, 59], [24, 60],
            [25, 60], [25, 61], [26, 61], [26, 62], [27, 60], [27, 61],
            [28, 61], [28, 62], [29, 63], [29, 64], [30, 64], [30, 65],
            [31, 65], [31, 66], [31, 67], [32, 66], [32, 67], [32, 68],
            [33, 67], [34, 68], [35, 69], [36, 70]]
fderived = {'one-past': one_past_txt, 'birth': birth_txt}
matched = 0
for it in FUT:
    if 'm' not in it:
        continue
    m, z = it['m'], it['z'] if isinstance(it['z'], int) else None
    if it['kind'].startswith('frontier') and m in (33, 34, 35, 36):
        t = frontier_txt(m)
        ck(it['prediction'].startswith(t), 'future frontier m=%d' % m)
        matched += 1
    elif it['kind'].startswith('one-past'):
        d = (z - zstar(m) - 1 - 0) // 2 if m % 2 else (z - zstar(m) - 1) // 2
        t = one_past_txt(m, d)
        ck(it['prediction'].startswith(t), 'future one-past m=%d z=%s'
           % (m, it['z']))
        matched += 1
    elif it['kind'].startswith('birth'):
        d = None
        for dd in range(0, 14):
            if birth_txt(m, dd).startswith('EXAC') and \
               S_of(m, dd - 1) == z:
                d = dd
                break
        ck(d is not None, 'future birth m=%d z=%s derive' % (m, it['z']))
        if d is not None:
            ck(it['prediction'].startswith(birth_txt(m, d)),
               'future birth m=%d z=%s' % (m, it['z']))
        matched += 1
ck(FUT[-1]['kind'] == 'smax note for future builds', 'smax note last')

# (I) engine pin
i = src.index("ENGINE_BLOCK = '''")
j = src.index("'''", i + 20)
blk = src[i + 18:j]
ck(hashlib.sha256(blk.encode()).hexdigest() ==
   'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92',
   'engine startup pin')
eb = 'from functools import lru_cache\n' + blk
ck(hashlib.sha256(eb.encode()).hexdigest() ==
   '582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0',
   'engine_block clone sha')

print('DERIVE-CHECK kit-9b: fail=%d (literals checked=%d)' % (fail, nlit))
sys.exit(1 if fail else 0)
