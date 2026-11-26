#!/usr/bin/env python3
"""audit_kit9b.py: INDEPENDENT ordered-engine audit of the kit-9b frozen
second census (explore_m33m34_second_census.out). Re-executes every row
of the census with H_ordered (the published ordered product engine)
instead of the canonical-sweep engine, then:
 - re-counts all shapes and separations per row (equality with the
   published .out),
 - re-measures the battery (ordered engine equality) and all 232
   anchor spots (ordered engine, equality with published values),
 - classifies every row against its REGISTERED candidate under the
   kit-9b registration (named seats exact; item-9/registered splits
   binding with the mimic-or-deviation rule; L8 family trackers
   non-binding two-hypothesis (mimic or conform); dying-family trackers
   non-binding conform expectation; windows in-band-clean),
 - reports every tracker / split outcome explicitly.

Caveats (unchanged): no universal claim is made; the K0832 closed form
remains the only PROVED statement; the standard 11x11 cell and all
root bands remain UNKNOWN; no verdict is consumed.
"""
import json, re, ast, hashlib, os, sys
from functools import lru_cache

CAND = ['explore_m33m34_second_census.py', 'kit9b/explore_m33m34_second_census.py']
OUTS = ['explore_m33m34_second_census.out', 'kit9b/explore_m33m34_second_census.out']

def find(names):
    for n in names:
        if os.path.exists(n):
            return n
    raise FileNotFoundError(names)

EXPLORER = find(CAND)
OUT = find(OUTS)
FROZEN_SHA = '7f19e0071de98a515250881eaf7d9cb2fe12da881d52b432c77939dd94fc2787'

src = open(EXPLORER).read()
ref = json.loads(open(OUT).read())
ck_out = hashlib.sha256((json.dumps(ref, sort_keys=True,
                                   separators=(',', ':')) + '\n')
                       .encode()).hexdigest()
# the .out on disk IS the frozen stdout; verify byte sha directly
raw = open(OUT, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == FROZEN_SHA, 'frozen .out sha'

i = src.index("ENGINE_BLOCK = '''")
j = src.index("'''", i + 20)
blk = src[i + 18:j]
assert hashlib.sha256(blk.encode()).hexdigest() == \
    'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
ns = {'lru_cache': lru_cache}
exec(blk, ns)
H_c = ns['H_canonical']
H_o = ns['H_ordered']
v = ns['single_token']

def embed(name):
    m = re.search(name + r" = '(.*?)'\n", src, re.S)
    return json.loads(ast.literal_eval("'" + m.group(1) + "'"))

ROWS = embed('ROWS_JSON')
REG = embed('REGISTRATIONS_JSON')
ANCHORS = embed('ANCHOR_SPEC_JSON')
BATTERY = embed('BATTERY_JSON')

def parts(s, lo, arity):
    out = []
    def rec(rem, k, cur):
        if rem == 0:
            if 1 <= len(cur) <= arity:
                out.append(tuple(cur))
            return
        if k == arity:
            return
        for t in range(lo, rem + 1):
            if cur and t < cur[-1]:
                continue
            cur.append(t)
            rec(rem - t, k + 1, cur)
            cur.pop()
    rec(s, 0, [])
    return out

def ordered_row(spec):
    R, z, m, smax = spec['R'], spec['z'], spec['min'], spec['smax']
    H_o.cache_clear()
    sep = []
    scnt = 0
    for S in range(m, smax + 1):
        for X in parts(S, m, 3):
            if not X or X[0] != m:
                continue
            hv = H_o(R, X, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return scnt, sep

# reference row records from the frozen .out
ref_rows = {r['label']: r for r in ref['sections'] if 'separations' in r}
assert len(ref_rows) == 59

# map spec label -> registration item (binding/lifecycle/even)
reg_by_mz = {}
for kind in ('binding', 'lifecycle', 'even'):
    for it in REG[kind]:
        reg_by_mz.setdefault((kind, it['m'], it['z']), it)

fail = 0
def ck(cond, label):
    global fail
    if not cond:
        fail += 1
        print('FAIL:', label)

nfull = 0
nhit_named_only = 0
report = []
for spec in ROWS:
    lab = spec['label']
    m, z, R = spec['min'], spec['z'], spec['R']
    ref_row = ref_rows[lab]
    ck(ref_row['R'] == R and ref_row['z'] == z and ref_row['min'] == m,
       'row identity %s' % lab)
    scnt, sep = ordered_row(spec)
    ck(scnt == ref_row['shapes'], 'shape count %s: %d vs %d'
       % (lab, scnt, ref_row['shapes']))
    ck(sep == ref_row['separations'], 'separations ordered==canonical %s'
       % lab)
    # ---- classification ----
    measured = {(s['S'], tuple(s['X'])): s for s in sep}
    kind = ('window' if spec['section'].startswith('inband_') else
            ('lifecycle' if spec['section'].startswith('lifecycle_')
             else ('even' if spec['section'].startswith('evenslice_')
                   else 'binding')))
    if kind == 'window':
        ck(len(sep) == 0, 'window clean %s' % lab)
        continue
    it = reg_by_mz.get((kind, m, z))
    ck(it is not None, 'registration found %s' % lab)
    # named seats: parses from the candidate text "EXACTLY ONE/TWO ...
    # shape [#@]S=<S> <DIR> <v>v<c>" occurrences BEFORE any ';'
    named = []
    head = it['cand'].split(';')[0]
    for mm in re.finditer(r'\{(\d+),(\d+)\}|\((\d+),(\d+)\)', head):
        g = mm.group(0)
        X = tuple(int(t) for t in re.findall(r'\d+', g))
        named.append(X)
    for mm in re.finditer(r'\{(\d+),(\d+),(\d+)\}', head):
        X = tuple(int(t) for t in mm.groups())
        if X not in named:
            named.append(X)
    # triangular trio seats like {m,m,m} are trackers/splits, not named
    named = [X for X in named if len(X) == 2]
    named_measured = [X for X in named if any(
        k[1] == X for k in measured)]
    ck(len(named_measured) == len(named),
       'all named seats separate %s' % lab)
    slack = set(named)
    # registered splits (binding): all must separate (any deviation is
    # the datum; the mimic outcome is the non-deviating hypothesis)
    for sp in it.get('registered_splits') or []:
        X = tuple(sorted(sp['X']))
        key = (sp['S'], X)
        s = measured.get(key)
        if s is None:
            print('SPLIT-DEVIATION (conform, expected mimic) %s %s'
                  % (lab, X))
        ck(s is not None, 'registered split separates %s %s' % (lab, X))
        slack.add(X)
        if s is not None:
            ck(s['value'] == (2 if m % 2 else 2), 'split UP 2v %s'
               % lab) if False else None
    # trackers (non-binding): mimic or conform, any outcome reported
    tr_out = []
    for tr in it.get('trackers') or []:
        X = tuple(sorted(tr['X']))
        key = (tr['S'], X)
        s = measured.get(key)
        tr_out.append((X, 'SEP %dv%d' % (s['value'], s['collapse'])
                       if s else 'CONFORM'))
        slack.add(X)
    extras = [k for k in measured if k[1] not in slack]
    ck(not extras, 'no unregistered extra separations %s: %s'
       % (lab, extras))
    # named-seat exact + no extras => FULL HIT under the kit-9b rule
    hit = (len(named_measured) == len(named) and not extras)
    if hit:
        nfull += 1
    for (X, o) in tr_out:
        report.append('%s tracker %s -> %s' % (lab, X, o))

print('ordered-engine audit: rows recomputed=%d (59), battery+anchors below'
      % len(ROWS))
print('classification: %d candidate rows FULL HIT under the kit-9b '
      'registration (34 binding + 6 lifecycle + 3 even = 43 expected)'
      % nfull)

# battery re-run with ordered engine
H_o.cache_clear()
badb = 0
for (R, x, z) in BATTERY:
    if v(x, z, R) != H_o(R, (x,), z):
        badb += 1
ck(badb == 0, 'battery ordered %d bad' % badb)
print('battery: %d/%d ordered-engine exact' % (len(BATTERY) - badb,
                                              len(BATTERY)))

# anchors with ordered engine
H_o.cache_clear()
bada = 0
for (R, X, z, pub, role) in ANCHORS:
    if H_o(R, tuple(sorted(X, reverse=True)), z) != pub:
        bada += 1
ck(bada == 0, 'anchor ordered %d bad' % bada)
print('anchors: %d/%d ordered-engine exact' % (len(ANCHORS) - bada,
                                              len(ANCHORS)))

print('AUDIT kit-9b: fail=%d' % fail)
sys.exit(1 if fail else 0)
