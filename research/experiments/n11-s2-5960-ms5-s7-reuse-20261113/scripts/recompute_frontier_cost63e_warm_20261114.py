#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published
WIN7 receipts as of main, extended with the cost-63e warm rebuild (class2-lane
session 12, 2026-11-14).

Direct extension of recompute_frontier_cost65h_65i_20261114.py via runpy:
after reproducing every published staged control through after-cost-65h+65i
(solved 991 / unique remaining 6856 / sum 540177 / open 5126/403900), the five
warm-rebuild cost-63e receipts (bits 42/73/100/116/120 - the WIN7-D10 candidates
that stayed unverified in the original cost-63e sweep; class2-lane-cost63e-
warm-certificates-20261114.json, a NEW record that leaves the original
published 3-cert records untouched so the recompute chain keeps asserting
them) are asserted and added. This closes the cost-63e band: all 8 of its
WIN7-D10 candidates now carry fully verified certificates. No new sweep is
involved; only certificates move the frontier.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-65h+65i frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost65h_65i_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s58 = ns['s58']
st58 = ns['st58']
rem58 = ns['rem58']
dem58 = ns['dem58']
assert st58['solved_s6_in_manifest'] == 991 and st58['unique_remaining_s6'] == 6856
assert st58['sum_remaining_cost'] == 540177
assert st58['s6_needed_by_open_classes'] == 5126 and st58['cost_needed_by_open_classes'] == 403900
print('CONTROL after-cost65h-65i published frontier reproduced: OK')

# ---------- 2. tie the warm rebuild to the original cost-63e sweep ----------
j63e = json.loads((OUT / 'class2-lane-cost63e-sweep-20261114.json').read_text())
assert j63e['s6_child_hex'] == '00000000000000803202200000000000'
assert j63e['win7_d10'] == 8 and j63e['capped'] == 0
assert j63e['win7_bits'] == [28, 42, 73, 90, 97, 100, 116, 120]
assert j63e['unverified_win7_bits'] == [42, 73, 100, 116, 120], \
    'the warm rebuild must cover exactly the original unverified cost-63e WIN7 bits'
print('CONTROL original cost-63e sweep record: OK (unverified bits 42/73/100/116/120 confirmed)')

# ---------- 3. assert the warm receipts record ----------
w = json.loads((OUT / 'class2-lane-cost63e-warm-certificates-20261114.json').read_text())
certs = [c for c in w['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs) == 5
assert [c['bit'] for c in certs] == [42, 73, 100, 116, 120]
rows_map = {42: 45348, 73: 40313, 100: 33856, 116: 48268, 120: 44172}
subs_map = {42: 54, 73: 50, 100: 49, 116: 53, 120: 55}
mob_map = {42: 54, 73: 50, 100: 49, 116: 53, 120: 55}
child63e = int(j63e['s6_child_hex'], 16)
for c in certs:
    assert c['rows'] == rows_map[c['bit']]
    assert c['sub_roots_pass'] == subs_map[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child63e | (1 << c['bit'])
print('CONTROL cost-63e warm receipts verified: OK (rows/sub-roots/union asserted for bits 42/73/100/116/120)')

# ---------- 4. add the warm receipts ----------
per_bits = {}
marg_union = set()
for c in certs:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s58
    marg_m = marg & manifest
    per_bits[c['bit']] = {
        'root_hex': c['root_hex'], 'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union |= marg
s59 = s58 | marg_union
st59, rem59, uniq59, dem59 = summary_state(s59)
print('AFTER cost63e-warm:', json.dumps(st59, indent=1))

# ---------- 5. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem59, 2)
class4 = best(rem59, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost63e-warm-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost65h-65i-recompute-20261114 (solved 991 / unique remaining 6856 / sum 540177 / open 5126/403900)',
    'method': 'direct runpy extension of recompute_frontier_cost65h_65i_20261114.py: every staged control reproduces the published after-cost-65h+65i frontier exactly (asserted: 991/6856/540177/5126/403900), the original cost-63e sweep record is asserted (unverified_win7_bits exactly 42/73/100/116/120), then the five warm-rebuild receipts of the NEW class2-lane-cost63e-warm-certificates-20261114.json record (bits 42/73/100/116/120; rows 45,348/40,313/33,856/48,268/44,172; sub-roots 54/50/49/53/55 PASS; union 0/0 each; the original 3-cert records untouched so the chain keeps asserting them) are added; this closes the cost-63e band - all 8 WIN7-D10 candidates certified; no new sweep, only certificates move the frontier',
    'controls': {
        'after_cost65h_65i': {'solved_in_manifest': 991, 'unique_remaining': 6856,
                              'sum_cost': 540177, 'open_s6': 5126, 'open_cost': 403900,
                              'reproduced': True},
        'cost63e_sweep_original': {'win7_d10': 8, 'unverified_bits': [42, 73, 100, 116, 120],
                                   'reproduced': True},
        'cost63e_warm_receipts': {'rows': rows_map, 'sub_roots_pass': subs_map,
                                  'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost63e_warm_addition': per_bits,
    'frontier_after_cost63e_warm': {
        'solved_s6_in_manifest': st59['solved_s6_in_manifest'],
        'remaining_s5_orbits': st59['remaining_s5_orbits'],
        'unique_remaining_s6': st59['unique_remaining_s6'],
        'sum_remaining_cost': st59['sum_remaining_cost'],
        's6_needed_by_open_classes': st59['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st59['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st59['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost63e-warm-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost63e-warm-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem59.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost63e-warm-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost63e-warm-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem59.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem59.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('second class-2 target S5',
                         next(c for c in class2 if c['s5_hex'] == '00000000000000803202000000000000'))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem59[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem59[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost63e-warm)')
