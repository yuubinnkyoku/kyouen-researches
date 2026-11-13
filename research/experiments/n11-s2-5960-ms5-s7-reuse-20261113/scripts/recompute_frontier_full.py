#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published
WIN7 receipts as of main 08e060f0, including class4-batch3 (bit37, child#3/#4,
child#5, child#7). Follows the audit_class_frontier.py logic in this same directory exactly;
snapshot asserts are replaced by staged controls (baseline / after_batch1 /
after_batch2 must reproduce the published frontier-update JSONs) before the
batch3 additions are measured.
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
      'batch3 bit37=1 child34', len(child34), 'child5', len(child5), 'child7', len(child7))

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
print('AFTER batch3:', json.dumps(st3, indent=1))

open3 = {k: v for k, v in dem3.items() if v['c1'] == 0}

def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem3, 2)
class4 = best(rem3, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class4-batch3-frontier-full-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': '08e060f0',
    'method': 'full recomputation of the audit_class_frontier.py logic over '
              'win7-reuse-hits + 12 baseline verified JSONs + class4 batch1/batch2 '
              'verified + batch3 (bit37, child#3/#4 x3, child#5 x4, child#7 x5); '
              'controls reproduce the published baseline/after_batch1/after_batch2 '
              'snapshot values exactly before batch3 is measured',
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
    },
    'batch3_additions': per,
    'frontier_after_batch3': {
        'solved_s6_in_manifest': st3['solved_s6_in_manifest'],
        'remaining_s5_orbits': st3['remaining_s5_orbits'],
        'unique_remaining_s6': st3['unique_remaining_s6'],
        'sum_remaining_cost': st3['sum_remaining_cost'],
        's6_needed_by_open_classes': st3['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st3['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st3['hist'],
        'class_composition': {
            'bit1': sum(1 for k in rem3 if classes.get(k, 0) & 1),
            'bit2': sum(1 for k in rem3 if classes.get(k, 0) & 2),
            'bit4': sum(1 for k in rem3 if classes.get(k, 0) & 4),
        },
        'best_class2': class2[0],
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 '
        'sweeps prove only absence of WIN7-D10; 11x11 empty root / {49,60} / '
        'S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class4-batch3-frontier-full-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class4-batch3-frontier-full-recompute-20261114.json')

# ---------- after-batch3 ranking CSVs (same format as -after-batch1/-batch2) ----------
ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem3.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                  r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-batch3.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))
with (OUT / 'class-frontier-top-candidates-s6-after-batch3.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5', class2[0])):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem3[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem3[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-batch3)')
