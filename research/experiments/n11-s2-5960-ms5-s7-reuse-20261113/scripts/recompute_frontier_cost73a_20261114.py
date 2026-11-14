#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published (cost-73a extension)
WIN7 receipts as of main (class2-lane cost-73a session 11, 2026-11-14).

Direct extension of recompute_frontier_cost73d_20261114.py: after reproducing every
published staged control through after-cost73d (solved 920 / unique remaining 6927 /
sum 545068 / open 5196/408718), the completed cost-73a sweep (session-11 takeover of
the session-9 claim: 1 WIN7-D10 bit81, fully verified certificate) is asserted
(1 WIN7, 0 capped) and its receipt is added. The sterile class2-lane cost-74 sweep
(session 10) is asserted receipt-free. cost-73a completes the cost-73 band and the
child sweeps of the best class-2 S5 target.
"""
import csv, gzip, json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
MS5 = HERE.parent / 'n11-s2-5960-milestone5-20261112' / 'output'

BASELINE_VERIFIED = (
    'priority-certificates-verified.json',
    'class2-certificates-verified.json',
    'class2-next-certificates-verified.json',
    'class2-next2-certificates-verified.json',
    'class2-next3-certificates-verified.json',
    'class2-next4-certificates-verified.json',
    'class2-batch5-certificates-verified.json',
    'class2-batch3-certificates-verified.json',
    'class2-batch2-certificates-verified.json',
    'class2-batch2b-certificates-verified.json',
    'class2-batch1-certificates-verified.json',
    'class2-batch1b-certificates-verified.json',
)
LOSS6 = (
    '00000000000000809202000400000000',
    '00000000000000003800004008000008',
    '00000000000000805202000000002000',
)

def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x,y), (y,10-x), (10-x,10-y), (10-y,x),
                      (10-x,y), (x,10-y), (y,x), (10-y,10-x))
            for i, (a,b) in enumerate(coords):
                result[i] |= 1 << (11*b+a)
    return result

IMG = [images(1 << p) for p in range(121)]

def canon(mask):
    """min image without rebuilding all 8 from scratch: fold per-stone images."""
    best = None
    for r in range(8):
        v = 0
        for p in range(121):
            if mask >> p & 1:
                v |= IMG[p][r]
        if best is None or v < best:
            best = v
    return best

def covers(root):
    return {canon(root ^ (1 << i)) for i in range(121) if root >> i & 1}

# ---------- inputs ----------
winners = set()
with gzip.open(OUT / 'win7-reuse-hits.csv.gz', 'rt', newline='') as f:
    for row in csv.DictReader(f):
        winners.add(int(row['s6_hex'], 16))

def roots_of(name):
    return [int(rec['root'], 16) for rec in
            json.loads((OUT / name).read_text())['certificates']
            if rec.get('verdict') == 'WIN7']

batch1 = roots_of('class4-batch1-certificates-verified.json')
batch2 = roots_of('class4-batch2-certificates-verified.json')

bit37 = int(json.loads((OUT / 'class4-batch3-bit37-certificate.json').read_text())['root_hex'], 16)
child34 = [int(c['root'], 16) for c in
           json.loads((OUT / 'class4-batch3-win7-certificates-20261114.json').read_text())['certificates']]
child5 = [int(c['root'], 16) for c in
          json.loads((OUT / 'class4-batch3-win7-certificates-child5-20261114.json').read_text())['certificates']]
child7 = [int(c['root_hex'], 16) for c in
          json.loads((OUT / 'class4-batch3-win7-certificates-child7-20261114.json').read_text())['certificates']]

cost60 = [int(c['root'], 16) for c in
          json.loads((OUT / 'class2-lane-cost60-win7-certificates-20261114.json').read_text())['certificates']]
cost61 = [int(c['root'], 16) for c in
          json.loads((OUT / 'class2-lane-cost61-win7-certificates-20261114.json').read_text())['certificates']]
cost64 = [int(c['root'], 16) for c in
          json.loads((OUT / 'class2-lane-cost64-win7-certificates-20261114.json').read_text())['certificates']]
cost65 = [int(c['root'], 16) for c in
          json.loads((OUT / 'class2-lane-cost65-win7-certificates-20261114.json').read_text())['certificates']]
cost61b = [int(c['root'], 16) for c in
           json.loads((OUT / 'class2-lane-cost61b-win7-certificates-20261114.json').read_text())['certificates']]
cost68 = [int(c['root'], 16) for c in
          json.loads((OUT / 'class2-lane-cost68-win7-certificates-20261114.json').read_text())['certificates']]
cost58 = [int(c['root'], 16) for c in
          json.loads((OUT / 'class2-lane-cost58-win7-certificates-20261114.json').read_text())['certificates']]

manifest = set()
for path in sorted(MS5.glob('ms5_s6_manifest_part*.csv')):
    with path.open(newline='') as f:
        manifest.update(int(row['hex'], 16) for row in csv.DictReader(f))
classes = {}
with gzip.open(OUT / 's5-remaining-after-reuse.csv.gz', 'rt', newline='') as f:
    for row in csv.DictReader(f):
        classes[row['s5_hex']] = int(row['classes'])
incidences = []
with gzip.open(OUT / 's5-s6-remaining-incidences.csv.gz', 'rt', newline='') as f:
    incidences = list(csv.DictReader(f))

print('inputs:', len(incidences), 'incidences,', len(winners), 'winners,',
      len(classes), 'classes,', len(manifest), 'manifest,',
      'batch1', len(batch1), 'batch2', len(batch2),
      'batch3 bit37=1 child34', len(child34), 'child5', len(child5), 'child7', len(child7),
      'cost60', len(cost60), 'cost61', len(cost61), 'cost61b', len(cost61b), 'cost64', len(cost64), 'cost65', len(cost65), 'cost68', len(cost68), 'cost58', len(cost58))

loss = {int(x, 16) for x in LOSS6}
rejected = {r['s5_hex'] for r in incidences if int(r['s6_hex'], 16) in loss}

def frontier(solved):
    remaining = defaultdict(list)
    for row in incidences:
        if row['s5_hex'] not in rejected and int(row['s6_hex'], 16) not in solved:
            remaining[row['s5_hex']].append(row)
    unique = {r['s6_hex']: int(r['s6_s7_edge_cost'])
              for rows in remaining.values() for r in rows}
    demand = defaultdict(lambda: {'c1': 0, 'c2': 0, 'c4': 0})
    for s5, rows in remaining.items():
        bits = classes.get(s5, 0)
        for row in rows:
            d = demand[row['s6_hex']]
            if bits & 1: d['c1'] += 1
            if bits & 2: d['c2'] += 1
            if bits & 4: d['c4'] += 1
    open_only = {k: v for k, v in demand.items() if v['c1'] == 0}
    return remaining, unique, demand, open_only

def summary_state(solved):
    remaining, unique, demand, open_only = frontier(solved)
    hist = defaultdict(int)
    for v in open_only.values():
        hist[f"c2={v['c2']},c4={v['c4']}"] += 1
    state = {
        'solved_s6_in_manifest': len(solved & manifest),
        'remaining_s5_orbits': len(remaining),
        'unique_remaining_s6': len(unique),
        'sum_remaining_cost': sum(unique.values()),
        's6_needed_by_open_classes': len(open_only),
        'cost_needed_by_open_classes': sum(int(unique[k]) for k in open_only),
        'hist': dict(sorted(hist.items())),
    }
    return state, remaining, unique, demand

# ---------- staged controls ----------
base = set(winners)
for name in BASELINE_VERIFIED:
    for r in roots_of(name):
        base |= covers(r)
s0, _, _, _ = summary_state(base)
print('CONTROL baseline:', s0['solved_s6_in_manifest'], s0['unique_remaining_s6'],
      s0['sum_remaining_cost'])
assert s0['solved_s6_in_manifest'] == 638 and s0['unique_remaining_s6'] == 7208
assert s0['sum_remaining_cost'] == 565500

s1 = base | set().union(*(covers(r) for r in batch1))
st1, _, _, _ = summary_state(s1)
print('CONTROL after_batch1:', st1['solved_s6_in_manifest'], st1['unique_remaining_s6'],
      st1['sum_remaining_cost'])
assert st1['solved_s6_in_manifest'] == 657 and st1['unique_remaining_s6'] == 7189
assert st1['sum_remaining_cost'] == 564070

s2 = s1 | set().union(*(covers(r) for r in batch2))
st2, rem2, uniq2, dem2 = summary_state(s2)
print('CONTROL after_batch2:', st2['solved_s6_in_manifest'], st2['unique_remaining_s6'],
      st2['sum_remaining_cost'], st2['s6_needed_by_open_classes'],
      st2['cost_needed_by_open_classes'])
assert st2['solved_s6_in_manifest'] == 665 and st2['unique_remaining_s6'] == 7181
assert st2['sum_remaining_cost'] == 563509
assert st2['s6_needed_by_open_classes'] == 5398
assert st2['cost_needed_by_open_classes'] == 423516

# also reproduce the batch2 newly-solved list to settle the duplicate audit
newly2 = sorted((s2 & manifest) - (s1 & manifest))
print('CONTROL batch2 newly_solved distinct count:', len(newly2),
      [f'{k:032x}' for k in newly2])

# ---------- batch3 additions ----------
per = {}
s3 = s2
for label, roots in (('bit37', [bit37]), ('child34', child34),
                     ('child5', child5), ('child7', child7)):
    cov = set().union(*(covers(r) for r in roots)) if roots else set()
    marg = cov - s3
    marg_m = marg & manifest
    per[label] = {
        'roots': [f'{r:032x}' for r in roots],
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    s3 = s3 | marg
# cross-check bit37 covers against its own published frontier_effect
b37 = json.loads((OUT / 'class4-batch3-bit37-certificate.json').read_text())
pub37 = set(int(h, 16) for h in b37['frontier_effect']['covers_canonical_s6'])
assert pub37 == covers(bit37), 'bit37 covers mismatch vs published frontier_effect'
print('CONTROL bit37 covers == published frontier_effect covers: OK')

st3, rem3, uniq3, dem3 = summary_state(s3)
print('CONTROL after_batch3:', st3['solved_s6_in_manifest'], st3['unique_remaining_s6'],
      st3['sum_remaining_cost'], st3['s6_needed_by_open_classes'],
      st3['cost_needed_by_open_classes'])
assert st3['solved_s6_in_manifest'] == 690 and st3['unique_remaining_s6'] == 7156
assert st3['sum_remaining_cost'] == 561764
assert st3['s6_needed_by_open_classes'] == 5373
assert st3['cost_needed_by_open_classes'] == 421771

# ---------- class2-lane cost-60 additions (batch4) ----------
per['cost60'] = None
cov60 = set().union(*(covers(r) for r in cost60))
marg60 = cov60 - s3
marg60_m = marg60 & manifest
per['cost60'] = {
    'roots': [f'{r:032x}' for r in cost60],
    'covers': len(cov60), 'marginal': len(marg60),
    'marginal_in_manifest': len(marg60_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg60_m),
}
s4 = s3 | marg60
st4, rem4, uniq4, dem4 = summary_state(s4)
print('CONTROL after_cost60:', st4['solved_s6_in_manifest'], st4['unique_remaining_s6'],
      st4['sum_remaining_cost'], st4['s6_needed_by_open_classes'],
      st4['cost_needed_by_open_classes'])
assert st4['solved_s6_in_manifest'] == 724 and st4['unique_remaining_s6'] == 7122
assert st4['sum_remaining_cost'] == 559294
assert st4['s6_needed_by_open_classes'] == 5339
assert st4['cost_needed_by_open_classes'] == 419301

# ---------- class2-lane cost-61 additions ----------
cov61 = set().union(*(covers(r) for r in cost61))
marg61 = cov61 - s4
marg61_m = marg61 & manifest
per['cost61'] = {
    'roots': [f'{r:032x}' for r in cost61],
    'covers': len(cov61), 'marginal': len(marg61),
    'marginal_in_manifest': len(marg61_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg61_m),
}
s5f = s4 | marg61
st5, rem6, uniq6, dem6 = summary_state(s5f)
print('CONTROL after_cost51:', st5['solved_s6_in_manifest'], st5['unique_remaining_s6'],
      st5['sum_remaining_cost'], st5['s6_needed_by_open_classes'],
      st5['cost_needed_by_open_classes'])
assert st5['solved_s6_in_manifest'] == 735 and st5['unique_remaining_s6'] == 7111
assert st5['sum_remaining_cost'] == 558480
assert st5['s6_needed_by_open_classes'] == 5328
assert st5['cost_needed_by_open_classes'] == 418487

# ---------- class2-lane cost-61 (b) additions ----------
cov61b = set().union(*(covers(r) for r in cost61b))
marg61b = cov61b - s5f
marg61b_m = marg61b & manifest
per['cost61b'] = {
    'roots': [f'{r:032x}' for r in cost61b],
    'covers': len(cov61b), 'marginal': len(marg61b),
    'marginal_in_manifest': len(marg61b_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg61b_m),
}
s6f = s5f | marg61b
st6, rem6, uniq6, dem6 = summary_state(s6f)
print('AFTER cost61b:', json.dumps(st6, indent=1))


assert st6['solved_s6_in_manifest'] == 749 and st6['unique_remaining_s6'] == 7097
assert st6['sum_remaining_cost'] == 557548
assert st6['s6_needed_by_open_classes'] == 5314
assert st6['cost_needed_by_open_classes'] == 417555

# ---------- class2-lane cost-64 additions ----------
cov64 = set().union(*(covers(r) for r in cost64))
marg64 = cov64 - s6f
marg64_m = marg64 & manifest
per['cost64'] = {
    'roots': [f'{r:032x}' for r in cost64],
    'covers': len(cov64), 'marginal': len(marg64),
    'marginal_in_manifest': len(marg64_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg64_m),
}
s7f = s6f | marg64
st7, rem7, uniq7, dem7 = summary_state(s7f)
print('AFTER cost64:', json.dumps(st7, indent=1))

assert st7['solved_s6_in_manifest'] == 779 and st7['unique_remaining_s6'] == 7067
assert st7['sum_remaining_cost'] == 555327
assert st7['s6_needed_by_open_classes'] == 5284
assert st7['cost_needed_by_open_classes'] == 415334

# ---------- class2-lane cost-65 additions ----------
cov65 = set().union(*(covers(r) for r in cost65))
marg65 = cov65 - s7f
marg65_m = marg65 & manifest
per['cost65'] = {
    'roots': [f'{r:032x}' for r in cost65],
    'covers': len(cov65), 'marginal': len(marg65),
    'marginal_in_manifest': len(marg65_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg65_m),
}
s8f = s7f | marg65
st8, rem8, uniq8, dem8 = summary_state(s8f)
print('AFTER cost65:', json.dumps(st8, indent=1))
assert st8['solved_s6_in_manifest'] == 786 and st8['unique_remaining_s6'] == 7060
assert st8['sum_remaining_cost'] == 554836
assert st8['s6_needed_by_open_classes'] == 5277
assert st8['cost_needed_by_open_classes'] == 414843

# ---------- class2-lane cost-68 additions (blocker closure) ----------
cov68 = set().union(*(covers(r) for r in cost68))
marg68 = cov68 - s8f
marg68_m = marg68 & manifest
per['cost68'] = {
    'roots': [f'{r:032x}' for r in cost68],
    'covers': len(cov68), 'marginal': len(marg68),
    'marginal_in_manifest': len(marg68_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg68_m),
}
s9f = s8f | marg68
st9, rem9, uniq9, dem9 = summary_state(s9f)
print('AFTER cost68:', json.dumps(st9, indent=1))
assert st9['solved_s6_in_manifest'] == 804 and st9['unique_remaining_s6'] == 7042
assert st9['sum_remaining_cost'] == 553474
assert st9['s6_needed_by_open_classes'] == 5259
assert st9['cost_needed_by_open_classes'] == 413481

blocker = '00000000000000003802000008000000'
assert blocker not in rem9, 'class-2 blocker S5 still present after cost-68!'
print('CONTROL class-2 blocker S5 absent from after-cost68 ranking: OK')

# ---------- class2-lane cost-58 additions (new class-2 target, child #1) ----------
cov58 = set().union(*(covers(r) for r in cost58))
marg58 = cov58 - s9f
marg58_m = marg58 & manifest
per['cost58'] = {
    'roots': [f'{r:032x}' for r in cost58],
    'covers': len(cov58), 'marginal': len(marg58),
    'marginal_in_manifest': len(marg58_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg58_m),
}
s10 = s9f | marg58
st10, rem10, uniq10, dem10 = summary_state(s10)
print('AFTER cost58:', json.dumps(st10, indent=1))
assert len(cov58) == 19 and len(marg58) == 19 and len(marg58_m) == 10, 'cost58 frontier effect mismatch vs published record'

assert st10['solved_s6_in_manifest'] == 814 and st10['unique_remaining_s6'] == 7032
assert st10['sum_remaining_cost'] == 552811
assert st10['s6_needed_by_open_classes'] == 5256
assert st10['cost_needed_by_open_classes'] == 413283
print('CONTROL after-cost58 published frontier reproduced: OK')

# ---------- class2-lane cost-75 additions (second child of the cost-75 S5) ----------
cost75 = [int(c['root'], 16) for c in
          json.loads((OUT / 'class2-lane-cost75-win7-certificates-20261114.json').read_text())['certificates']]
cov75 = set().union(*(covers(r) for r in cost75))
marg75 = cov75 - s10
marg75_m = marg75 & manifest
per['cost75'] = {
    'roots': [f'{r:032x}' for r in cost75],
    'covers': len(cov75), 'marginal': len(marg75),
    'marginal_in_manifest': len(marg75_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg75_m),
}
s11 = s10 | marg75
st11, rem11, uniq11, dem11 = summary_state(s11)
print('AFTER cost75:', json.dumps(st11, indent=1))

blocker75 = '00000000000000801a02000000000000'
assert blocker75 not in rem11, 'cost-75 target S5 still present after cost-75!'
print('CONTROL cost-75 target S5 absent from after-cost75 ranking: OK')

# ---------- CONTROL after-cost75 published frontier ----------
assert st11['solved_s6_in_manifest'] == 831, st11
assert st11['unique_remaining_s6'] == 7016, st11
assert st11['sum_remaining_cost'] == 551482, st11
assert st11['s6_needed_by_open_classes'] == 5240, st11
assert st11['cost_needed_by_open_classes'] == 411954, st11
print('CONTROL after-cost75 published frontier reproduced: OK')

# ---------- class2-lane cost-61-c additions ----------
json61c = json.loads((OUT / 'class2-lane-cost61c-win7-certificates-20261114.json').read_text())
cost61c = [int(c['root'], 16) for c in json61c['certificates'] if c.get('verdict') == 'WIN7']
cov61c = set().union(*(covers(r) for r in cost61c)) if cost61c else set()
marg61c = cov61c - s11
marg61c_m = marg61c & manifest
pub61c = set(int(h, 16) for h in json61c['frontier_effect']['marginal_manifest_hexes'])
assert pub61c <= cov61c, 'cost61c published marginals not all covered by its roots'
per['cost61c'] = {
    'roots': [f'{r:032x}' for r in cost61c],
    'covers': len(cov61c), 'marginal': len(marg61c),
    'marginal_in_manifest': len(marg61c_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg61c_m),
    'published_effect_note': 'published frontier_effect (7 covers/5 marginal/2 in-manifest) was measured against the smaller after-cost58 solved set; marginals here are measured against the full through-cost75 solved set',
    'published_marginals_still_marginal': sorted(f'{k:032x}' for k in (pub61c - s11) & manifest),
    'published_marginals_already_solved': sorted(f'{k:032x}' for k in pub61c & s11 & manifest),
}
s12 = s11 | marg61c
st12, rem12, uniq12, dem12 = summary_state(s12)
print('AFTER cost61c:', json.dumps(st12, indent=1))

# ---------- class2-lane cost-63 additions ----------
json63 = json.loads((OUT / 'class2-lane-cost63-win7-certificates-20261114.json').read_text())
cost63 = [int(c['root'], 16) for c in json63['certificates'] if c.get('verdict') == 'WIN7']
cov63 = set().union(*(covers(r) for r in cost63)) if cost63 else set()
marg63 = cov63 - s12
marg63_m = marg63 & manifest
pub63 = set(int(h, 16) for h in json63['frontier_effect']['marginal_manifest_hexes'])
assert pub63 <= cov63, 'cost63 published marginals not all covered by its roots'
per['cost63'] = {
    'roots': [f'{r:032x}' for r in cost63],
    'covers': len(cov63), 'marginal': len(marg63),
    'marginal_in_manifest': len(marg63_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg63_m),
    'published_effect_note': 'published frontier_effect (25 covers/20 marginal/8 in-manifest) was measured against the through-cost61-c solved set; marginals here are measured against the full through-cost75+cost61c solved set',
    'published_marginals_still_marginal': sorted(f'{k:032x}' for k in (pub63 - s12) & manifest),
    'published_marginals_already_solved': sorted(f'{k:032x}' for k in pub63 & s12 & manifest),
}
s13 = s12 | marg63
st13, rem13, uniq13, dem13 = summary_state(s13)
print('AFTER cost63:', json.dumps(st13, indent=1))

# the class-2 target S5 of the cost-58/61c/63 sweeps must still be trackable
# ---------- CONTROL after-cost63 published frontier ----------
assert st13['solved_s6_in_manifest'] == 841, st13
assert st13['unique_remaining_s6'] == 7006, st13
assert st13['sum_remaining_cost'] == 550810, st13
assert st13['s6_needed_by_open_classes'] == 5236, st13
assert st13['cost_needed_by_open_classes'] == 411675, st13
print('CONTROL after-cost63 published frontier reproduced: OK')

# ---------- class2-lane cost-63b additions (S6 child 00000000000000809082000000001000) ----------
cost63b = [int(h, 16) for h in (
    '00000000000000809083000000001000',
    '00001000000000809082000000001000',
    '00400000000000809082000000001000')]
cov63b = set().union(*(covers(r) for r in cost63b))
marg63b = cov63b - s13
marg63b_m = marg63b & manifest
per['cost63b'] = {
    'roots': [f'{r:032x}' for r in cost63b],
    'covers': len(cov63b), 'marginal': len(marg63b),
    'marginal_in_manifest': len(marg63b_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg63b_m),
}
s14 = s13 | marg63b
st14, rem14, uniq14, dem14 = summary_state(s14)
print('AFTER cost63b:', json.dumps(st14, indent=1))

# ---------- CONTROL after-cost63b published frontier ----------
assert st14['solved_s6_in_manifest'] == 849, st14
assert st14['unique_remaining_s6'] == 6998, st14
assert st14['sum_remaining_cost'] == 550269, st14
assert st14['s6_needed_by_open_classes'] == 5233, st14
assert st14['cost_needed_by_open_classes'] == 411475, st14
print('CONTROL after-cost63b published frontier reproduced: OK')

# ---------- class2-lane cost-63c additions (S6 child 000000000000008090a2000000000000) ----------
cost63c = [int(h, 16) for h in ('000000000000008090a2400000000000',)]
cov63c = set().union(*(covers(r) for r in cost63c))
marg63c = cov63c - s14
marg63c_m = marg63c & manifest
per['cost63c'] = {
    'roots': [f'{r:032x}' for r in cost63c],
    'covers': len(cov63c), 'marginal': len(marg63c),
    'marginal_in_manifest': len(marg63c_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg63c_m),
}
s15 = s14 | marg63c
st15, rem15, uniq15, dem15 = summary_state(s15)
print('AFTER cost63c:', json.dumps(st15, indent=1))

# ---------- class2-lane cost-63d additions (S6 child 00000000000000809082000000080000) ----------
cost63d = [int(h, 16) for h in ('00000000000000c09082000000080000',)]
cov63d = set().union(*(covers(r) for r in cost63d))
marg63d = cov63d - s15
marg63d_m = marg63d & manifest
per['cost63d'] = {
    'roots': [f'{r:032x}' for r in cost63d],
    'covers': len(cov63d), 'marginal': len(marg63d),
    'marginal_in_manifest': len(marg63d_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg63d_m),
}
s16 = s15 | marg63d
st16, rem16, uniq16, dem16 = summary_state(s16)
print('AFTER cost63d:', json.dumps(st16, indent=1))

# ---------- CONTROL after-cost63d published frontier (855) ----------
assert st16['solved_s6_in_manifest'] == 855, st16
assert st16['unique_remaining_s6'] == 6992, st16
assert st16['sum_remaining_cost'] == 549862, st16
assert st16['s6_needed_by_open_classes'] == 5232, st16
assert st16['cost_needed_by_open_classes'] == 411408, st16
print('CONTROL after-cost63d published frontier reproduced: OK')

# ---------- class4-lane cost-74b additions (S6 child 00000000020000003801000080000000, 6 WIN7) ----------
json74b = json.loads((OUT / 'class4-lane-cost74b-win7-certificates-20261114.json').read_text())
cost74b = [int(c['root'], 16) for c in json74b['certificates']]
assert len(cost74b) == 6
cov74b = set().union(*(covers(r) for r in cost74b))
marg74b = cov74b - s16
marg74b_m = marg74b & manifest
per['cost74b'] = {
    'roots': [f'{r:032x}' for r in cost74b],
    'covers': len(cov74b), 'marginal': len(marg74b),
    'marginal_in_manifest': len(marg74b_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg74b_m),
}
s17 = s16 | marg74b
st17, rem17, uniq17, dem17 = summary_state(s17)
print('AFTER cost74b:', json.dumps(st17, indent=1))

# ---------- class4-lane cost-78 additions (S6 child 00000000020000003800000080000040, 2 WIN7) ----------
json78 = json.loads((OUT / 'class4-lane-cost78-win7-certificates-20261114.json').read_text())
cost78 = [int(c['root'], 16) for c in json78['certificates']]
assert len(cost78) == 2
cov78 = set().union(*(covers(r) for r in cost78))
marg78 = cov78 - s17
marg78_m = marg78 & manifest
per['cost78'] = {
    'roots': [f'{r:032x}' for r in cost78],
    'covers': len(cov78), 'marginal': len(marg78),
    'marginal_in_manifest': len(marg78_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg78_m),
}
s18 = s17 | marg78
st18, rem18, uniq18, dem18 = summary_state(s18)
print('AFTER cost78:', json.dumps(st18, indent=1))

# ---------- class4-lane cost-78b additions (S6 child 00000000020000003800001080000000, 2 WIN7) ----------
json78b = json.loads((OUT / 'class4-lane-cost78b-win7-certificates-20261114.json').read_text())
cost78b = [int(c['root'], 16) for c in json78b['certificates']]
assert len(cost78b) == 2
cov78b = set().union(*(covers(r) for r in cost78b))
marg78b = cov78b - s18
marg78b_m = marg78b & manifest
reuse_note = ('bit48 root 00000000020000003801001080000000 is the SAME 7-stone root as '
              'cost-74b bit36 (cross-child root reuse); its covers are therefore already '
              'counted in the cost-74b stage and contribute no additional marginals here')
per['cost78b'] = {
    'roots': [f'{r:032x}' for r in cost78b],
    'covers': len(cov78b), 'marginal': len(marg78b),
    'marginal_in_manifest': len(marg78b_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg78b_m),
    'root_reuse_note': reuse_note,
}
s19 = s18 | marg78b
st19, rem19, uniq19, dem19 = summary_state(s19)
print('AFTER cost78b:', json.dumps(st19, indent=1))



# ---------- CONTROL after-cost78b published frontier ----------
assert st19['solved_s6_in_manifest'] == 875, st19
assert st19['unique_remaining_s6'] == 6972, st19
assert st19['sum_remaining_cost'] == 548362, st19
assert st19['s6_needed_by_open_classes'] == 5212, st19
assert st19['cost_needed_by_open_classes'] == 409908, st19
print('CONTROL after-cost78b published frontier reproduced: OK')

# ---------- sterile sweep controls (no receipts) ----------
json79 = json.loads((OUT / 'class4-lane-cost79-sweep-20261114.json').read_text())
assert json79['summary']['win7_d10'] == [] and json79['summary']['capped'] == []
json79b = json.loads((OUT / 'class4-lane-cost79b-sweep-20261114.json').read_text())
assert json79b['summary']['win7_d10'] == [] and json79b['summary']['capped'] == []
json80 = json.loads((OUT / 'class4-lane-cost80-sweep-20261114.json').read_text())
assert json80['summary']['win7_d10'] == [] and json80['summary']['capped'] == []
json65b = json.loads((OUT / 'class2-lane-cost65b-sweep-20261114.json').read_text())
assert json65b['win7_d10'] == 0 and json65b['capped'] == 0
print('CONTROL sterile sweeps cost-79 / cost-79b / cost-80 (class4) and cost-65b (class2): OK')

# ---------- class2-lane cost-65c additions (3 WIN7) ----------
json65c = json.loads((OUT / 'class2-lane-cost65c-win7-certificates-20261114.json').read_text())
cost65c = [int(c['root'], 16) for c in json65c['certificates']]
assert len(cost65c) == 3
cov65c = set().union(*(covers(r) for r in cost65c))
marg65c = cov65c - s19
marg65c_m = marg65c & manifest
per['cost65c'] = {
    'roots': [f'{r:032x}' for r in cost65c],
    'covers': len(cov65c), 'marginal': len(marg65c),
    'marginal_in_manifest': len(marg65c_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg65c_m),
}
s20 = s19 | marg65c
st20, rem20, uniq20, dem20 = summary_state(s20)
print('AFTER cost65c:', json.dumps(st20, indent=1))
assert st20['solved_s6_in_manifest'] == 881 and st20['unique_remaining_s6'] == 6966
assert st20['sum_remaining_cost'] == 547927
assert st20['s6_needed_by_open_classes'] == 5210
assert st20['cost_needed_by_open_classes'] == 409767
print('CONTROL after-cost65c published frontier reproduced: OK')

# ---------- class2-lane cost-65d additions (S6 child 00000000000000809082000010000000, 1 WIN7) ----------
json65d = json.loads((OUT / 'class2-lane-cost65d-win7-certificates-20261114.json').read_text())
cost65d = [int(c['root'], 16) for c in json65d['certificates']]
assert len(cost65d) == 1
cov65d = set().union(*(covers(r) for r in cost65d))
marg65d = cov65d - s20
marg65d_m = marg65d & manifest
per['cost65d'] = {
    'roots': [f'{r:032x}' for r in cost65d],
    'covers': len(cov65d), 'marginal': len(marg65d),
    'marginal_in_manifest': len(marg65d_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg65d_m),
}
s21 = s20 | marg65d
st21, rem21, uniq21, dem21 = summary_state(s21)
print('AFTER cost65d:', json.dumps(st21, indent=1))


# ---------- CONTROL after-cost65d published frontier ----------
assert st21['solved_s6_in_manifest'] == 884, st21
assert st21['unique_remaining_s6'] == 6963, st21
assert st21['sum_remaining_cost'] == 547712, st21
assert st21['s6_needed_by_open_classes'] == 5209, st21
assert st21['cost_needed_by_open_classes'] == 409691, st21
print('CONTROL after-cost65d published frontier reproduced: OK')

# ---------- class4-lane cost-80b additions (1 WIN7, published by the parallel lane) ----------
json80b = json.loads((OUT / 'class4-lane-cost80b-win7-certificates-20261114.json').read_text())
cost80b = [int(c['root'], 16) for c in json80b['certificates']]
assert len(cost80b) == 1
cov80b = set().union(*(covers(r) for r in cost80b))
marg80b2 = cov80b - s21
marg80b2_m = marg80b2 & manifest
per['cost80b'] = {
    'roots': [f'{r:032x}' for r in cost80b],
    'covers': len(cov80b), 'marginal': len(marg80b2),
    'marginal_in_manifest': len(marg80b2_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg80b2_m),
}
s22 = s21 | marg80b2
st22, rem22, uniq22, dem22 = summary_state(s22)
print('AFTER cost80b (merged):', json.dumps(st22, indent=1))


# ---------- CONTROL after-merged published frontier ----------
assert st22['solved_s6_in_manifest'] == 887, st22
assert st22['unique_remaining_s6'] == 6960, st22
assert st22['sum_remaining_cost'] == 547472, st22
assert st22['s6_needed_by_open_classes'] == 5206, st22
assert st22['cost_needed_by_open_classes'] == 409451, st22
print('CONTROL after-merged published frontier reproduced: OK')

# ---------- sterile sweep controls (class4-lane cost-80c / 81 / 82; class2-lane cost-66a / 66b) ----------
json80c = json.loads((OUT / 'class4-lane-cost80c-sweep-20261114.json').read_text())
assert json80c['summary']['win7_d10'] == [] and json80c['summary']['capped'] == []
json81 = json.loads((OUT / 'class4-lane-cost81-sweep-20261114.json').read_text())
assert json81['summary']['win7_d10'] == [] and json81['summary']['capped'] == []
json82 = json.loads((OUT / 'class4-lane-cost82-sweep-20261114.json').read_text())
assert json82['summary']['win7_d10'] == [] and json82['summary']['capped'] == []
json66a = json.loads((OUT / 'class2-lane-cost66a-sweep-20261114.json').read_text())
assert json66a['win7_d10'] == 0 and json66a['capped'] == 0 and json66a['candidates'] == 66
json66b = json.loads((OUT / 'class2-lane-cost66b-sweep-20261114.json').read_text())
assert json66b['win7_d10'] == 0 and json66b['capped'] == 0 and json66b['candidates'] == 66
print('CONTROL sterile sweeps cost-80c/81/82 (class4) and cost-66a/66b (class2): OK')

# ---------- class2-lane cost-67 additions (4 WIN7, this session) ----------
json67 = json.loads((OUT / 'class2-lane-cost67-win7-certificates-20261114.json').read_text())
cost67 = [int(c['root'], 16) for c in json67['certificates']]
assert len(cost67) == 4
cov67 = set().union(*(covers(r) for r in cost67))
marg67 = cov67 - s22
marg67_m = marg67 & manifest
per['cost67'] = {
    'roots': [f'{r:032x}' for r in cost67],
    'covers': len(cov67), 'marginal': len(marg67),
    'marginal_in_manifest': len(marg67_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg67_m),
}
s23 = s22 | marg67
st23, rem23, uniq23, dem23 = summary_state(s23)
print('AFTER cost67:', json.dumps(st23, indent=1))


# ---------- CONTROL after-cost67 published frontier ----------
assert st23['solved_s6_in_manifest'] == 898, st23
assert st23['unique_remaining_s6'] == 6949, st23
assert st23['sum_remaining_cost'] == 546687, st23
assert st23['s6_needed_by_open_classes'] == 5202, st23
assert st23['cost_needed_by_open_classes'] == 409163, st23
print('CONTROL after-cost67 published frontier reproduced: OK')

# ---------- class2-lane cost-68b additions (2 WIN7, this session) ----------
json68b = json.loads((OUT / 'class2-lane-cost68b-win7-certificates-20261114.json').read_text())
cost68b = [int(c['root'], 16) for c in json68b['certificates']]
assert len(cost68b) == 2
cov68b = set().union(*(covers(r) for r in cost68b))
marg68b = cov68b - s23
marg68b_m = marg68b & manifest
per['cost68b'] = {
    'roots': [f'{r:032x}' for r in cost68b],
    'covers': len(cov68b), 'marginal': len(marg68b),
    'marginal_in_manifest': len(marg68b_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg68b_m),
}
s24 = s23 | marg68b
st24, rem24, uniq24, dem24 = summary_state(s24)
print('AFTER cost68b:', json.dumps(st24, indent=1))

# ---------- CONTROL after-cost68b published frontier ----------
assert st24['solved_s6_in_manifest'] == 903, st24
assert st24['unique_remaining_s6'] == 6944, st24
assert st24['sum_remaining_cost'] == 546334, st24
assert st24['s6_needed_by_open_classes'] == 5201, st24
assert st24['cost_needed_by_open_classes'] == 409091, st24
print('CONTROL after-cost68b published frontier reproduced: OK')

# ---------- class2-lane cost-69a additions (3 WIN7, this session) ----------
json69a = json.loads((OUT / 'class2-lane-cost69a-win7-certificates-20261114.json').read_text())
cost69a = [int(c['root'], 16) for c in json69a['certificates']]
assert len(cost69a) == 3
cov69a = set().union(*(covers(r) for r in cost69a))
marg69a = cov69a - s24
marg69a_m = marg69a & manifest
per['cost69a'] = {
    'roots': [f'{r:032x}' for r in cost69a],
    'covers': len(cov69a), 'marginal': len(marg69a),
    'marginal_in_manifest': len(marg69a_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg69a_m),
}
s25 = s24 | marg69a
st25, rem25, uniq25, dem25 = summary_state(s25)

# ---------- CONTROL after-cost69a published frontier ----------
assert st25['solved_s6_in_manifest'] == 909, st25
assert st25['unique_remaining_s6'] == 6938, st25
assert st25['sum_remaining_cost'] == 545893, st25
assert st25['s6_needed_by_open_classes'] == 5199, st25
assert st25['cost_needed_by_open_classes'] == 408942, st25
print('CONTROL after-cost69a published frontier reproduced: OK')

# ---------- sterile sweep controls (no receipts) ----------
json69b = json.loads((OUT / 'class2-lane-cost69b-sweep-20261114.json').read_text())
assert json69b['win7_d10'] == 0 and json69b['capped'] == 0 and json69b['refuted_d10'] == 69
json69d = json.loads((OUT / 'class2-lane-cost69d-sweep-20261114.json').read_text())
assert json69d['win7_d10'] == 0 and json69d['capped'] == 0
json70 = json.loads((OUT / 'class2-lane-cost70-sweep-20261114.json').read_text())
assert json70['win7_d10'] == 0 and json70['capped'] == 0
print('CONTROL sterile sweeps cost-69b / cost-69d / cost-70 (class2): OK')

# ---------- class2-lane cost-69c additions (1 WIN7, this session) ----------
json69c = json.loads((OUT / 'class2-lane-cost69c-win7-certificates-20261114.json').read_text())
cost69c = [int(c['root'], 16) for c in json69c['certificates'] if c.get('verdict') == 'WIN7']
assert len(cost69c) == 1
cov69c = set().union(*(covers(r) for r in cost69c))
marg69c = cov69c - s25
marg69c_m = marg69c & manifest
per['cost69c'] = {
    'roots': [f'{r:032x}' for r in cost69c],
    'covers': len(cov69c), 'marginal': len(marg69c),
    'marginal_in_manifest': len(marg69c_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg69c_m),
}
s26 = s25 | marg69c
st26, rem26, uniq26, dem26 = summary_state(s26)
print('AFTER cost69c:', json.dumps(st26, indent=1))

# ---------- CONTROL after-cost69c published frontier ----------
assert st26['solved_s6_in_manifest'] == 912, st26
assert st26['unique_remaining_s6'] == 6935, st26
assert st26['sum_remaining_cost'] == 545666, st26
assert st26['s6_needed_by_open_classes'] == 5198, st26
assert st26['cost_needed_by_open_classes'] == 408868, st26
print('CONTROL after-cost69c published frontier reproduced: OK')

# ---------- class2-lane cost-70b additions (1 WIN7, this session) ----------
json70b = json.loads((OUT / 'class2-lane-cost70b-win7-certificates-20261114.json').read_text())
cost70b = [int(c['root_hex'], 16) for c in json70b['certificates']]
assert len(cost70b) == 1
cov70b = set().union(*(covers(r) for r in cost70b))
marg70b = cov70b - s26
marg70b_m = marg70b & manifest
per['cost70b'] = {
    'roots': [f'{r:032x}' for r in cost70b],
    'covers': len(cov70b), 'marginal': len(marg70b),
    'marginal_in_manifest': len(marg70b_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg70b_m),
}
s27 = s26 | marg70b
st27, rem27, uniq27, dem27 = summary_state(s27)
print('AFTER cost70b:', json.dumps(st27, indent=1))

# ---------- CONTROL after-cost70b published frontier ----------
assert st27['solved_s6_in_manifest'] == 913, st27
assert st27['unique_remaining_s6'] == 6934, st27
assert st27['sum_remaining_cost'] == 545596, st27
assert st27['s6_needed_by_open_classes'] == 5198, st27
assert st27['cost_needed_by_open_classes'] == 408868, st27
print('CONTROL after-cost70b published frontier reproduced: OK')

# ---------- class2-lane cost-71 additions (2 WIN7, this session) ----------
json71 = json.loads((OUT / 'class2-lane-cost71-win7-certificates-20261114.json').read_text())
cost71 = [int(c['root_hex'], 16) for c in json71['certificates'] if c.get('verdict') == 'WIN7']
assert len(cost71) == 2
cov71 = set().union(*(covers(r) for r in cost71))
marg71 = cov71 - s27
marg71_m = marg71 & manifest
per['cost71'] = {
    'roots': [f'{r:032x}' for r in cost71],
    'covers': len(cov71), 'marginal': len(marg71),
    'marginal_in_manifest': len(marg71_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg71_m),
}
s28 = s27 | marg71
st28, rem28, uniq28, dem28 = summary_state(s28)
print('AFTER cost71:', json.dumps(st28, indent=1))

# ---------- CONTROL after-cost71 published frontier ----------
assert st28['solved_s6_in_manifest'] == 917, st28
assert st28['unique_remaining_s6'] == 6930, st28
assert st28['sum_remaining_cost'] == 545301, st28
assert st28['s6_needed_by_open_classes'] == 5197, st28
assert st28['cost_needed_by_open_classes'] == 408797, st28
print('CONTROL after-cost71 published frontier reproduced: OK')

# ---------- class2-lane cost-73 band: sterile sweeps 73b / 73c / 73e / 74 (no receipts) ----------
for _name in ('class2-lane-cost73b-sweep-20261114.json',
              'class2-lane-cost73c-sweep-20261114.json',
              'class2-lane-cost73e-sweep-20261114.json',
              'class2-lane-cost74-sweep-20261114.json'):
    _j = json.loads((OUT / _name).read_text())
    assert _j['win7_d10'] == 0 and _j['capped'] == 0, (_name, _j['win7_d10'], _j['capped'])
print('CONTROL sterile sweeps cost-73b / cost-73c / cost-73e / cost-74 (class2): OK')
# cost-73a completed by session 11 (takeover of the session-9 claim): 1 WIN7-D10 bit81,
# 72 REFUTED, 0 capped, 383,290,602 nodes; raw batches 1-11, determinism rerun,
# runner_fbs20 cross-engine check and the fully verified certificate are published.
_j73a = json.loads((OUT / 'class2-lane-cost73a-sweep-20261114.json').read_text())
assert _j73a['win7_d10'] == 1 and _j73a['capped'] == 0 and _j73a['refuted_d10'] == 72, _j73a
assert _j73a['win7_roots'] == ['00000000000200809082000000000010'], _j73a
print('CONTROL completed cost-73a sweep record: OK (1 WIN7, 0 capped, root asserted)')

# ---------- class2-lane cost-73d additions (1 WIN7, long-term lane session 9) ----------
json73d = json.loads((OUT / 'class2-lane-cost73d-win7-certificates-20261114.json').read_text())
cost73d = [int(c['root_hex'], 16) for c in json73d['certificates'] if c.get('verdict') == 'WIN7']
assert len(cost73d) == 1
cov73d = set().union(*(covers(r) for r in cost73d))
marg73d = cov73d - s28
marg73d_m = marg73d & manifest
per['cost73d'] = {
    'roots': [f'{r:032x}' for r in cost73d],
    'covers': len(cov73d), 'marginal': len(marg73d),
    'marginal_in_manifest': len(marg73d_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg73d_m),
}
s29 = s28 | marg73d
st29, rem29, uniq29, dem29 = summary_state(s29)
print('AFTER cost73d:', json.dumps(st29, indent=1))

# ---------- CONTROL after-cost73d published frontier (920) ----------
assert st29['solved_s6_in_manifest'] == 920, st29
assert st29['unique_remaining_s6'] == 6927, st29
assert st29['sum_remaining_cost'] == 545068, st29
assert st29['s6_needed_by_open_classes'] == 5196, st29
assert st29['cost_needed_by_open_classes'] == 408718, st29
print('CONTROL after-cost73d published frontier reproduced: OK')

# ---------- class2-lane cost-73a additions (1 WIN7, long-term lane session 11 takeover) ----------
json73a = json.loads((OUT / 'class2-lane-cost73a-win7-certificates-20261114.json').read_text())
cost73a = [int(c['root_hex'], 16) for c in json73a['certificates'] if c.get('verdict') == 'WIN7']
assert len(cost73a) == 1
cov73a = set().union(*(covers(r) for r in cost73a))
marg73a = cov73a - s29
marg73a_m = marg73a & manifest
per['cost73a'] = {
    'roots': [f'{r:032x}' for r in cost73a],
    'covers': len(cov73a), 'marginal': len(marg73a),
    'marginal_in_manifest': len(marg73a_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg73a_m),
}
s30 = s29 | marg73a
st30, rem30, uniq30, dem30 = summary_state(s30)
print('AFTER cost73a:', json.dumps(st30, indent=1))

def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem30, 2)
class4 = best(rem30, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost73a-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost73d-recompute-20261114 (solved 920 / unique remaining 6927 / sum 545068 / open 5196/408718)',
    'method': 'direct extension of recompute_frontier_cost73d_20261114.py: every staged control reproduces the published after-cost73d frontier exactly (asserted: 920/6927/545068/5196/408718), the sterile cost-73b/73c/73e/74 sweeps are asserted receipt-free, then the class2-lane cost-73a receipt (1 WIN7 root: bit 81 of S6 child 00000000000000809082000000000010, fully verified certificate, 51/51 sub-roots PASS, union 0/0) is added. cost-73a completes the cost-73 band: 73a WIN7 (bit81), 73b/73c/73e sterile, 73d WIN7 (bit48).',
    'controls': {
        'after_cost71': {'solved_in_manifest': 917, 'unique_remaining': 6930, 'sum_cost': 545301, 'open_s6': 5197, 'open_cost': 408797, 'reproduced': True},
        'after_cost73d': {'solved_in_manifest': 920, 'unique_remaining': 6927, 'sum_cost': 545068, 'open_s6': 5196, 'open_cost': 408718, 'reproduced': True},
        'sterile_73b_73c_73e_74': {'win7_d10': 0, 'capped': 0, 'reproduced': True},
        'cost73a_sweep': {'win7_d10': 1, 'capped': 0, 'refuted_d10': 72, 'root_asserted': True},
    },
    'cost73a_addition': per['cost73a'],
    'frontier_after_cost73a': {
        'solved_s6_in_manifest': st30['solved_s6_in_manifest'],
        'remaining_s5_orbits': st30['remaining_s5_orbits'],
        'unique_remaining_s6': st30['unique_remaining_s6'],
        'sum_remaining_cost': st30['sum_remaining_cost'],
        's6_needed_by_open_classes': st30['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st30['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st30['hist'],
        'best_class2': class2[0],
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost73a-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost73a-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem30.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                  r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost73a-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))
with (OUT / 'class-frontier-top-candidates-s6-after-cost73a-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5', class2[0])):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem30[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem30[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost73a)')
