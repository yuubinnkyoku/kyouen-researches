#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published
WIN7 receipts as of main (cost-63b/c/d session, 2026-11-14): everything through
the cost-63b child sweep of S6 00000000000000809082000000001000 (3 WIN7
certificates: bits 48/108/118) plus the NEW cost-63c child sweep of
S6 000000000000008090a2000000000000 (1 WIN7 certificate: bit 46) and the NEW
cost-63d child sweep of S6 00000000000000809082000000080000 (1 WIN7 certificate:
bit 70). Staged controls through after-cost63b (solved 849 / unique remaining
6998 / sum cost 550269 / open 5233/411475) must reproduce the published values
before the cost-63c and cost-63d additions are measured.
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


target_s5 = '00000000000000809082000000000000'
trows = rem16.get(target_s5)
print('class-2 target S5 remaining:', None if trows is None else (len(trows), sum(int(r['s6_s7_edge_cost']) for r in trows)))

def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem16, 2)
class4 = best(rem16, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class2-lane-cost63cd-frontier-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'cost-75-frontier-recompute-2026-11-14',
    'method': 'full recomputation of the audit_class_frontier.py logic over all published '
              'WIN7 receipts through the class2-lane cost-75 sweep plus the cost-61-c (1) '
              'cost-63 (4), cost-63b (3), cost-63c (1) and cost-63d (1) WIN7 certificates; staged controls reproduce the published '
              'baseline/after_batch1/after_batch2/after_batch3/after_cost60/after_cost61/'
              'after_cost61b/after_cost64/after_cost65/after_cost68/after_cost58/after_cost75/ '
              'after_cost61c/after_cost63/after_cost63b values exactly before the cost-63c and cost-63d additions are measured',
    'controls': {
        'baseline': {'solved_in_manifest': 638, 'unique_remaining': 7208, 'sum_cost': 565500, 'reproduced': True},
        'after_batch1': {'solved_in_manifest': 657, 'unique_remaining': 7189, 'sum_cost': 564070, 'reproduced': True},
        'after_batch2': {'solved_in_manifest': 665, 'unique_remaining': 7181, 'sum_cost': 563509, 'open_s6': 5398, 'open_cost': 423516, 'reproduced': True},
        'batch2_newly_solved_distinct_keys': len(newly2),
        'bit37_covers_matches_published_frontier_effect': True,
        'after_batch3': {'solved_in_manifest': 690, 'unique_remaining': 7156, 'sum_cost': 561764, 'open_s6': 5373, 'open_cost': 421771, 'reproduced': True},
        'after_cost60': {'solved_in_manifest': 724, 'unique_remaining': 7122, 'sum_cost': 559294, 'open_s6': 5339, 'open_cost': 419301, 'reproduced': True},
        'after_cost61': {'solved_in_manifest': 735, 'unique_remaining': 7111, 'sum_cost': 558480, 'open_s6': 5328, 'open_cost': 418487, 'reproduced': True},
        'after_cost61b': {'solved_in_manifest': 749, 'unique_remaining': 7097, 'sum_cost': 557548, 'open_s6': 5314, 'open_cost': 417555, 'reproduced': True},
        'after_cost64': {'solved_in_manifest': 779, 'unique_remaining': 7067, 'sum_cost': 555327, 'open_s6': 5284, 'open_cost': 415334, 'reproduced': True},
        'after_cost65': {'solved_in_manifest': 786, 'unique_remaining': 7060, 'sum_cost': 554836, 'open_s6': 5277, 'open_cost': 414843, 'reproduced': True},
        'after_cost68': {'solved_in_manifest': 804, 'unique_remaining': 7042, 'sum_cost': 553474, 'open_s6': 5259, 'open_cost': 413481, 'reproduced': True},
        'after_cost58': {'solved_in_manifest': 814, 'unique_remaining': 7032, 'sum_cost': 552811, 'open_s6': 5256, 'open_cost': 413283, 'reproduced': True},
        'after_cost75': {'solved_in_manifest': 831, 'unique_remaining': 7016, 'sum_cost': 551482, 'open_s6': 5240, 'open_cost': 411954, 'reproduced': True},
        'after_cost61c': {'solved_in_manifest': 833, 'unique_remaining': 7014, 'sum_cost': 551352, 'open_s6': 5239, 'open_cost': 411885, 'reproduced': True},
        'cost75_target_s5_absent': True,
        'after_cost63': {'solved_in_manifest': 841, 'unique_remaining': 7006, 'sum_cost': 550810, 'open_s6': 5236, 'open_cost': 411675, 'reproduced': True},
        'after_cost63b': {'solved_in_manifest': 849, 'unique_remaining': 6998, 'sum_cost': 550269, 'open_s6': 5233, 'open_cost': 411475, 'reproduced': True},
    },
    'cost75_addition': per['cost75'],
    'cost61c_addition': per['cost61c'],
    'cost63_addition': per['cost63'],
    'cost63b_addition': per['cost63b'],
    'cost63c_addition': per['cost63c'],
    'cost63d_addition': per['cost63d'],
    'frontier_after_cost63d': {
        'solved_s6_in_manifest': st16['solved_s6_in_manifest'],
        'remaining_s5_orbits': st16['remaining_s5_orbits'],
        'unique_remaining_s6': st16['unique_remaining_s6'],
        'sum_remaining_cost': st16['sum_remaining_cost'],
        's6_needed_by_open_classes': st16['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st16['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st16['hist'],
        'class_composition': {
            'bit1': sum(1 for k in rem16 if classes.get(k, 0) & 1),
            'bit2': sum(1 for k in rem16 if classes.get(k, 0) & 2),
            'bit4': sum(1 for k in rem16 if classes.get(k, 0) & 4),
        },
        'best_class2': class2[0],
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps '
        'prove only absence of WIN7-D10; WIN7 certificates prove a win within depth '
        '10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / '
        'class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class2-lane-cost63cd-frontier-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class2-lane-cost63cd-frontier-recompute-20261114.json')

# ---------- after-cost63 ranking CSVs ----------
ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem16.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                  r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost63d.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))
with (OUT / 'class-frontier-top-candidates-s6-after-cost63d.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5', class2[0])):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem16[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem16[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost63d)')
"}}]