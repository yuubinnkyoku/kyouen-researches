#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published
WIN7 receipts as of main 8055d4be, including class4-batch3 (bit37, child#3/#4,
child#5, child#7), the class2-lane cost-60 sweep's 19 WIN7 certificates, and
the class2-lane cost-61 sweep's 4 WIN7 certificates.
Follows the recompute_frontier_full.py logic in this same directory exactly;
staged controls (baseline / after_batch1 / after_batch2 / after_batch3 /
after_cost60 must reproduce the published values) run before the cost61
additions are measured.
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
      'cost60', len(cost60), 'cost61', len(cost61), 'cost61b', len(cost61b), 'cost64', len(cost64), 'cost65', len(cost65))

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

open6 = {k: v for k, v in dem6.items() if v['c1'] == 0}

def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem8, 2)
class4 = best(rem8, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class2-lane-cost65-frontier-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'e42d9c96',
    'method': 'full recomputation of the audit_class_frontier.py logic over '
              'win7-reuse-hits + 12 baseline verified JSONs + class4 batch1/batch2 '
              'verified + batch3 (bit37, child#3/#4 x3, child#5 x4, child#7 x5) + '
              'class2-lane cost-60 (19) + cost-61 (4) + cost-61b (12) + cost-64 (24) + cost-65 (7 WIN7 '
              'certificates); controls reproduce the published baseline/'
              'after_batch1/after_batch2/after_batch3/after_cost60/after_cost61/'
              'after_cost61b/after_cost64 values exactly before the cost-65 additions are measured',
    'controls': {
        'baseline': {'solved_in_manifest': 638, 'unique_remaining': 7208,
                      'sum_cost': 565500, 'reproduced': True},
        'after_batch1': {'solved_in_manifest': 657, 'unique_remaining': 7189,
                         'sum_cost': 564070, 'reproduced': True},
        'after_batch2': {'solved_in_manifest': 665, 'unique_remaining': 7181,
                         'sum_cost': 563509, 'open_s6': 5398,
                         'open_cost': 423516, 'reproduced': True},
        'batch2_newly_solved_distinct_keys': len(newly2),
        'bit37_covers_matches_published_frontier_effect': True,
        'after_batch3': {'solved_in_manifest': 690, 'unique_remaining': 7156,
                         'sum_cost': 561764, 'open_s6': 5373,
                         'open_cost': 421771, 'reproduced': True},
        'after_cost60': {'solved_in_manifest': 724, 'unique_remaining': 7122,
                         'sum_cost': 559294, 'open_s6': 5339,
                         'open_cost': 419301, 'reproduced': True},
        'after_cost61': {'solved_in_manifest': 735, 'unique_remaining': 7111,
                         'sum_cost': 558480, 'open_s6': 5328,
                         'open_cost': 418487, 'reproduced': True},
        'after_cost61b': {'solved_in_manifest': 749, 'unique_remaining': 7097,
                          'sum_cost': 557548, 'open_s6': 5314,
                          'open_cost': 417555, 'reproduced': True},
        'after_cost64': {'solved_in_manifest': 779, 'unique_remaining': 7067,
                         'sum_cost': 555327, 'open_s6': 5284,
                         'open_cost': 415334, 'reproduced': True},
    },
    'batch3_additions': {k: v for k, v in per.items() if k not in ('cost60', 'cost61', 'cost61b')},
    'cost60_addition': per['cost60'],
    'cost61_addition': per['cost61'],
    'cost61b_addition': per['cost61b'],
    'cost64_addition': per['cost64'],
    'cost65_addition': per['cost65'],
    'frontier_after_cost65': {
        'solved_s6_in_manifest': st8['solved_s6_in_manifest'],
        'remaining_s5_orbits': st8['remaining_s5_orbits'],
        'unique_remaining_s6': st8['unique_remaining_s6'],
        'sum_remaining_cost': st8['sum_remaining_cost'],
        's6_needed_by_open_classes': st8['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st8['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st8['hist'],
        'class_composition': {
            'bit1': sum(1 for k in rem8 if classes.get(k, 0) & 1),
            'bit2': sum(1 for k in rem8 if classes.get(k, 0) & 2),
            'bit4': sum(1 for k in rem8 if classes.get(k, 0) & 4),
        },
        'best_class2': class2[0],
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 '
        'sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win '
        'within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / '
        'S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class2-lane-cost65-frontier-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class2-lane-cost65-frontier-recompute-20261114.json')

# ---------- after-cost61b ranking CSVs (same format as -after-batch1/-batch2/-batch3/-cost60) ----------
ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem8.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                  r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost65.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))
with (OUT / 'class-frontier-top-candidates-s6-after-cost65.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5', class2[0])):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem8[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem8[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost64)')
