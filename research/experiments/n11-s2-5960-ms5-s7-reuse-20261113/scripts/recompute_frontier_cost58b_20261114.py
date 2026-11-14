#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published (cost-58b
extension) WIN7 receipts as of main (class2-lane cost-58b session 12, 2026-11-14).

Direct extension of recompute_frontier_cost56a_20261114.py via runpy: after
reproducing every published staged control through after-cost-56a (solved 927 /
unique remaining 6920 / sum 544617 / open 5190/408340), the completed cost-58b
sweep (session 12, second-cheapest unswept child of the second class-2 target
S5 00000000000000803202000000000000: 58 candidates on S6 child
00000000000000803202000000002000, run on the v16 runner: 3 WIN7-D10 bits
18/77/120, 55 REFUTED, 0 capped, 30,690,766 v16 nodes) is asserted and its
three fully verified receipts (bit18: 33,459 rows, 48/48 sub-roots PASS;
bit77: 35,070 rows, 46/46; bit120: 41,969 rows, 51/51; union 0/0 each) are
added.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-56a frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost56a_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s31 = ns['s32']
st31 = ns['st32']
rem31 = ns['rem32']
dem31 = ns['dem32']
assert st31['solved_s6_in_manifest'] == 927 and st31['unique_remaining_s6'] == 6920
assert st31['sum_remaining_cost'] == 544617
assert st31['s6_needed_by_open_classes'] == 5190 and st31['cost_needed_by_open_classes'] == 408340
print('CONTROL after-cost56a published frontier reproduced: OK')

# ---------- 2. assert the completed cost-58b sweep record ----------
j58b = json.loads((OUT / 'class2-lane-cost58b-sweep-20261114.json').read_text())
assert j58b['s6_child_hex'] == '00000000000000803202000000002000'
assert j58b['s5_parent_hex'] == '00000000000000803202000000000000'
assert j58b['s6_s7_edge_cost'] == 58 and j58b['capped'] == 0
assert j58b['win7_d10'] == 3 and j58b['refuted_d10'] == 55
assert j58b['total_nodes'] == 30690766
assert j58b['win7_bits'] == [18, 77, 120]
assert j58b['win7_roots'] == ['00000000000000803202000000042000',
                              '00000000000020803202000000002000',
                              '01000000000000803202000000002000']
assert j58b['demand_classes'] == {'c1': 0, 'c2': 1, 'c4': 1}
child = int(j58b['s6_child_hex'], 16)
for b, r in zip(j58b['win7_bits'], j58b['win7_roots']):
    assert int(r, 16) == child | (1 << b), (b, r)
print('CONTROL completed cost-58b sweep record: OK (3 WIN7, 55 REFUTED, 0 capped, roots asserted)')

# the 58 candidate bits are bit-exact with the independent enumeration
claim = json.loads((OUT / 'class2-lane-cost58b-inflight-20261114.json').read_text())
assert claim['legal_candidates_total'] == 58 and claim['status'].startswith('completed')
assert claim['result']['win7_d10'] == 3 and claim['result']['capped'] == 0
print('CONTROL cost-58b claim updated to completed: OK')

# the demand of this child in the after-cost-56a state matches the record
assert dem31[j58b['s6_child_hex']] == {'c1': 0, 'c2': 1, 'c4': 1}
print('CONTROL cost-58b child demand (c1=0,c2=1,c4=1) reproduced from the frontier: OK')

# ---------- 3. add the cost-58b receipts (three fully verified certificates) ----------
w58b = json.loads((OUT / 'class2-lane-cost58b-win7-certificates-20261114.json').read_text())
certs = [c for c in w58b['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs) == 3
assert [c['bit'] for c in certs] == [18, 77, 120]
rows_map = {18: 33459, 77: 35070, 120: 41969}
subs_map = {18: 48, 77: 46, 120: 51}
for c in certs:
    assert c['root_hex'] == {
        18: '00000000000000803202000000042000',
        77: '00000000000020803202000000002000',
        120: '01000000000000803202000000002000'}[c['bit']]
    assert c['rows'] == rows_map[c['bit']]
    assert c['sub_roots_pass'] == subs_map[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child | (1 << c['bit'])
print('CONTROL cost-58b receipts verified: OK (rows/sub-roots/union asserted for bits 18/77/120)')

per_bits = {}
marg_union = set()
for c in certs:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s31
    marg_m = marg & manifest
    per_bits[c['bit']] = {
        'root_hex': c['root_hex'],
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union |= marg
s32 = s31 | marg_union
st32, rem32, uniq32, dem32 = summary_state(s32)
print('AFTER cost58b:', json.dumps(st32, indent=1))

# ---------- 4. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem32, 2)
class4 = best(rem32, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost58b-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost56a-recompute-20261114 (solved 927 / unique remaining 6920 / sum 544617 / open 5190/408340)',
    'method': 'direct extension of recompute_frontier_cost56a_20261114.py: every staged control reproduces the published after-cost-56a frontier exactly (asserted: 927/6920/544617/5190/408340), the completed cost-58b sweep (3 WIN7-D10 bits 18/77/120, 55 REFUTED, 0 capped, 30,690,766 v16 nodes; v15 cross-engine anchors on all three WIN7 bits plus the heaviest REFUTED bit 43, and a v16 determinism re-run node-exact on bits 120/43/18) is asserted and its three fully verified receipts (bit18: 33,459 rows, 48/48 sub-roots PASS, union 0/0; bit77: 35,070 rows, 46/46; bit120: 41,969 rows, 51/51) are added',
    'controls': {
        'after_cost56a': {'solved_in_manifest': 927, 'unique_remaining': 6920,
                          'sum_cost': 544617, 'open_s6': 5190, 'open_cost': 408340,
                          'reproduced': True},
        'cost58b_sweep': {'win7_d10': 3, 'capped': 0, 'refuted_d10': 55,
                          'roots_asserted': True, 'engine': 'v16 (agreement-gated in cost-56a)'},
        'cost58b_claim': {'status': 'completed', 'reproduced': True},
        'cost58b_demand': {'c1': 0, 'c2': 1, 'c4': 1, 'reproduced': True},
        'cost58b_receipts': {'rows': rows_map, 'sub_roots_pass': subs_map,
                            'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost58b_addition': per_bits,
    'frontier_after_cost58b': {
        'solved_s6_in_manifest': st32['solved_s6_in_manifest'],
        'remaining_s5_orbits': st32['remaining_s5_orbits'],
        'unique_remaining_s6': st32['unique_remaining_s6'],
        'sum_remaining_cost': st32['sum_remaining_cost'],
        's6_needed_by_open_classes': st32['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st32['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st32['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost58b-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost58b-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem32.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost58b-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost58b-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem32.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem32.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-58b parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == '00000000000000803202000000000000'))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem32[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem32[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost58b)')
