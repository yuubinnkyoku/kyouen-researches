#!/usr/bin/env python3
"""audit_kit8.py: INDEPENDENT ordered-engine audit of the kit-8 frozen
census. Re-executes every row of explore_m31m32_ladders_trio.out with
H_ordered (the published ordered product engine) instead of the
canonical-sweep engine, then:
 - re-counts all shapes and separations per row (equality with the
   published .out),
 - re-anchors all 180 published spots with the ordered engine,
 - classifies the 28 binding rows against their registered candidates
   (parse the named seats from the candidate text; FULL HIT iff the
   named-seat set equals the measured seat set at the S values named,
   modulo the non-binding trio tracker),
 - reports the trio-tracker outcomes and the probe outcomes explicitly.
"""
import json, re, ast
from functools import lru_cache

src = open('explore_m31m32_ladders_trio.py').read()
i = src.index("ENGINE_BLOCK = '''")
j = src.index("'''\nPIN", i)
content = src[i + 18:j]
ns = {'lru_cache': lru_cache}
exec(content, ns)
H_c = ns['H_canonical']
H_o = ns['H_ordered']
v = ns['single_token']

import importlib
def load_embed(name, nxt):
    m = re.search(name + r' = (.*?)\n' + nxt, src, re.S)
    return json.loads(ast.literal_eval(m.group(1)))
data = load_embed('K8_BINDING_JSON', 'K8_PROBES_JSON')
probes = load_embed('K8_PROBES_JSON', 'BATTERY_TRIPLES_JSON')

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

def ordered_row(R, z, m, smin, smax):
    H_o.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(S, m, 3):
            if not X or X[0] != m:
                continue
            hv = H_o(R, X, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv, 'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return scnt, sep

pub = json.load(open('explore_m31m32_ladders_trio.out'))
secs = pub['sections']
rows = [s for s in secs if s['section'].endswith('_row_record')]

bad = 0
report = []
for r in rows:
    m = r['min']; z = r['z']; R = r['R']
    dom = r['s_domain']
    a, b = dom[1:-1].split('..')
    scnt, sep = ordered_row(R, z, m, int(a), int(b))
    ok_shapes = scnt == r['shapes']
    ok_seps = sep == r['separations']
    if not (ok_shapes and ok_seps):
        bad += 1
        report.append(('MISMATCH', r['section'], scnt, r['shapes'], len(sep), len(r['separations'])))
print('ordered-engine row audit: rows=%d mismatches=%d' % (len(rows), bad))
for x in report:
    print(x)

# anchors ordered
anch = [s for s in secs if s['section'] == 'published_anchor_rechecks'][0]['rows']
bad_a = 0
H_o.cache_clear()
for a in anch:
    XX = tuple(sorted(a['X'], reverse=True))
    hv = H_o(a['R'], XX, a['z'])
    if hv != a['published_value']:
        bad_a += 1
print('ordered-engine anchors: %d/%d exact' % (len(anch) - bad_a, len(anch)))

# battery re-check ordered vs closed
bat = [s for s in secs if s['section'] == 'k0832_battery'][0]['rows']
bad_b = 0
for b in bat:
    if not (v(b['x'], b['z'], b['R']) == ns['vO'](b['x'], b['z'], b['R']) == b['closed']):
        bad_b += 1
print('battery: %d literals, bad=%d' % (len(bat), bad_b))

# classification: parse named seats from candidates of the 28 binding rows
def parse_named(cand):
    # only the seats in the EXACTLY clause; strip conform-DEAD clauses
    kept = []
    for seg in cand.split('; '):
        if 'conform-DEAD' in seg:
            continue
        kept.append(seg)
    txt = '; '.join(kept)
    toks = re.findall(r'[{(](\d+), ?(\d+)[})]', txt)
    return [(int(a), int(b)) for (a, b) in toks]

rows_by_sec = {r['section']: r for r in rows}
verdicts = []
for row in data:
    m, z, item = row['m'], row['z'], row['item']
    sec = ('frontier_m%d_z%d_row_record' % (m, z)) if row.get('frontier') else ('ladder_m%d_z%d_row_record' % (m, z))
    r = rows_by_sec[sec]
    named = parse_named(row['cand'])
    measured = [tuple(sp['X']) for sp in r['separations']]
    named_set = set()
    for (a, b) in named:
        named_set.add(tuple(sorted((a, b), reverse=True)))
    # separate the measured into pairs (2-token) and stacks (3-token)
    measured_pairs = set(tuple(sorted(X, reverse=True)) for X in measured if len(X) == 2)
    tracker = row.get('tracker', [])
    tracker_X = set(tuple(t['X']) for t in tracker)
    measured_stacks = set(X for X in measured if len(X) == 3)
    hit = (measured_pairs == named_set)
    extra_stacks = measured_stacks - tracker_X
    if hit and not extra_stacks:
        verdicts.append((item, m, z, 'FULL HIT', sorted(measured_stacks)))
    elif hit:
        verdicts.append((item, m, z, 'DEVIATION (unregistered stack shadows: %s)' % sorted(extra_stacks), sorted(measured_stacks)))
    else:
        verdicts.append((item, m, z, 'DEVIATION (seat-set mismatch: measured %s named %s)' % (sorted(measured_pairs), sorted(named_set)), sorted(measured_stacks)))
for vd in verdicts:
    print('item%-3d m=%d z=%d %s' % (vd[0], vd[1], vd[2], vd[3]),
          ('| tracker/stacks: %s' % vd[4]) if vd[4] else '')

# probes + hole + windows outcomes
for p in probes:
    sec = 'trio_mid_slice_m%d_z%d_row_record' % (p['m'], p['z'])
    r = rows_by_sec[sec]
    named = parse_named(p['cand'])
    named_set = set(tuple(sorted(x, reverse=True)) for x in named)
    measured_pairs = set(tuple(sorted(sp['X'], reverse=True)) for sp in r['separations'] if len(sp['X']) == 2)
    stack_seps = [sp for sp in r['separations'] if len(sp['X']) == 3]
    print('probe m=%d z=%d: seats %s | trio outcome: %s' % (
        p['m'], p['z'],
        'HIT' if measured_pairs == named_set else 'MISMATCH %s vs %s' % (sorted(measured_pairs), sorted(named_set)),
        [(sp['X'], '%dv%d %s' % (sp['value'], sp['collapse'], sp['direction'])) for sp in stack_seps]))
hole = rows_by_sec['hole_m26_z25_row_record']
print('hole m=26 z=25: shapes=%d separations=%d -> %s' % (
    hole['shapes'], len(hole['separations']), 'CLEAN (m=26 line FULLY SWEPT z {25..56})' if not hole['separations'] else 'DIRTY'))
wc = [rows_by_sec['inband_m29_z%d_row_record' % z] for z in range(49, 57)]
wc += [rows_by_sec['inband_m30_z%d_row_record' % z] for z in range(50, 58)]
print('windows m29/m30: %d rows, %d separations total -> %s' % (
    len(wc), sum(len(r['separations']) for r in wc),
    'ALL CLEAN' if all(not r['separations'] for r in wc) else 'DIRTY'))
# tracker outcomes
for z in (56, 57):
    r = rows_by_sec['ladder_m19_z%d_row_record' % z]
    t = [sp for sp in r['separations'] if sp['X'] == [19, 19, 19]]
    print('trio tracker z=%d outcome: %s' % (z,
          ('%dv%d %s' % (t[0]['value'], t[0]['collapse'], t[0]['direction'])) if t else 'CONFORM'))
