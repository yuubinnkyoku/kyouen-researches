#!/usr/bin/env python3
"""Frontier recomputation including the class2-lane cost-60 WIN7 certificates
(19 roots, output/class2-lane-cost60-win7-certificates-20261114.json).

Extends scripts/recompute_frontier_full.py: the after-batch3 frontier
(690 / 7156 / 561764 / 5373 / 421771) is recomputed as a STAGED CONTROL
(assert) over the same inputs, then the 19 new certificate covers are added.
Outputs the after-cost60 frontier JSON and ranking CSVs.
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
      'cost60 certs', len(cost60))

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

# ---------- staged control: after-batch3 ----------
solved = set(winners)
for name in BASELINE_VERIFIED:
    for r in roots_of(name):
        solved |= covers(r)
for roots in (batch1, batch2, child34, child5, child7, [bit37]):
    solved |= set().union(*(covers(r) for r in roots))
s3, rem3, uniq3, dem3 = summary_state(solved)
print('CONTROL after_batch3:', s3['solved_s6_in_manifest'], s3['unique_remaining_s6'],
      s3['sum_remaining_cost'], s3['s6_needed_by_open_classes'],
      s3['cost_needed_by_open_classes'])
assert s3['solved_s6_in_manifest'] == 690, s3['solved_s6_in_manifest']
assert s3['unique_remaining_s6'] == 7156
assert s3['sum_remaining_cost'] == 561764
assert s3['s6_needed_by_open_classes'] == 5373
assert s3['cost_needed_by_open_classes'] == 421771

# ---------- cost-60 additions ----------
cost60_cov = set().union(*(covers(r) for r in cost60))
marg = cost60_cov - solved
marg_m = marg & manifest
print('cost60 covers:', len(cost60_cov), 'marginal:', len(marg),
      'marginal_in_manifest:', len(marg_m))

solved4 = solved | cost60_cov
st4, rem4, uniq4, dem4 = summary_state(solved4)
print('AFTER cost60:', json.dumps(st4, indent=1))

def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem4, 2)
class4 = best(rem4, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class2-lane-cost60-frontier-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main_before': 'b9a908b9 (frontier after batch3 published at 08e060f0 lineage)',
    'method': 'recompute_frontier_full.py logic + the 19 verified cost-60 WIN7 '
              'certificates (output/class2-lane-cost60-win7-certificates-20261114.json); '
              'after-batch3 values recomputed as a staged control (assert) before '
              'the cost-60 covers are added',
    'controls': {
        'after_batch3': {'solved_in_manifest': 690, 'unique_remaining': 7156,
                         'sum_cost': 561764, 'open_s6': 5373,
                         'open_cost': 421771, 'reproduced': True},
    },
    'cost60_additions': {
        'certificates': len(cost60),
        'covers': len(cost60_cov),
        'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    },
    'frontier_after_cost60': {
        'solved_s6_in_manifest': st4['solved_s6_in_manifest'],
        'remaining_s5_orbits': st4['remaining_s5_orbits'],
        'unique_remaining_s6': st4['unique_remaining_s6'],
        'sum_remaining_cost': st4['sum_remaining_cost'],
        's6_needed_by_open_classes': st4['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st4['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st4['hist'],
        'best_class2': class2[0],
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; every counted '
        'cover comes from an independently verified certificate; REFUTED-D10 sweeps '
        'prove only absence of WIN7-D10; 11x11 empty root / {49,60} / S2 {59,60} / '
        'class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class2-lane-cost60-frontier-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class2-lane-cost60-frontier-recompute-20261114.json')

# ---------- after-cost60 ranking CSV ----------
ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem4.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost60.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))
print('written class-frontier-s5-ranking-after-cost60.csv')
