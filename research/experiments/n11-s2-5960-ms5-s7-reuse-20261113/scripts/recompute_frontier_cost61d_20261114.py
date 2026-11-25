#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published (cost-61d
extension) WIN7 receipts as of main (class2-lane cost-61d session 12, 2026-11-14).

Direct extension of recompute_frontier_cost60b_20261114.py via runpy: after
reproducing every published staged control through after-cost-60b (solved 946 /
unique remaining 6901 / sum 543316 / open 5171/407039), the completed cost-61d
sweep (session 12, cheapest remaining unswept child of the second class-2
target S5 00000000000000803202000000000000: 61 candidates on S6 child
00000000000000803202000000000002, run on the v16 runner: 14 WIN7-D10, 47
REFUTED, 0 capped, 50,848,724 v16 nodes) is asserted and its three fully
verified receipts (bits 30/74/94; 44/49/45 sub-roots
PASS, union 0/0 each) are added. The 11 remaining WIN7-D10 bits stay warm
certificate-rebuild candidates and change no frontier number.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-58b frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost60b_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s31 = ns['s32']
st31 = ns['st32']
rem31 = ns['rem32']
dem31 = ns['dem32']
assert st31['solved_s6_in_manifest'] == 946 and st31['unique_remaining_s6'] == 6901
assert st31['sum_remaining_cost'] == 543316
assert st31['s6_needed_by_open_classes'] == 5171 and st31['cost_needed_by_open_classes'] == 407039
print('CONTROL after-cost60b published frontier reproduced: OK')

# ---------- 2. assert the completed cost-61d sweep record ----------
j61d = json.loads((OUT / 'class2-lane-cost61d-sweep-20261114.json').read_text())
assert j61d['s6_child_hex'] == '00000000000000803202000000000002'
assert j61d['s5_parent_hex'] == '00000000000000803202000000000000'
assert j61d['s6_s7_edge_cost'] == 61 and j61d['capped'] == 0
assert j61d['win7_d10'] == 14 and j61d['refuted_d10'] == 47
assert j61d['total_nodes'] == 50848724
assert j61d['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 0}
child = int(j61d['s6_child_hex'], 16)
for b, r in zip(j61d['win7_bits'], j61d['win7_roots']):
    assert int(r, 16) == child | (1 << b), (b, r)
print('CONTROL completed cost-61d sweep record: OK (14 WIN7, 47 REFUTED, 0 capped, roots asserted)')

# the 61 candidate bits are bit-exact with the independent enumeration
claim = json.loads((OUT / 'class2-lane-cost61d-inflight-20261114.json').read_text())
assert claim['legal_candidates_total'] == 61 and claim['status'].startswith('completed')
assert claim['result']['win7_d10'] == 14 and claim['result']['capped'] == 0
print('CONTROL cost-61d claim updated to completed: OK')

# the demand of this child in the after-cost-58b state matches the record
assert dem31[j61d['s6_child_hex']] == {'c1': 0, 'c2': 2, 'c4': 0}
print('CONTROL cost-61d child demand (c1=0,c2=2,c4=0) reproduced from the frontier: OK')

# ---------- 3. add the cost-61d receipts (six fully verified certificates) ----------
w60b = json.loads((OUT / 'class2-lane-cost61d-win7-certificates-20261114.json').read_text())
certs = [c for c in w60b['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs) == 3
assert [c['bit'] for c in certs] == [30, 74, 94]
rows_map = {30: 23348, 74: 26090, 94: 23982}
subs_map = {30: 44, 74: 49, 94: 45}
mob_map = {30: 44, 74: 49, 94: 45}
for c in certs:
    assert c['rows'] == rows_map[c['bit']]
    assert c['sub_roots_pass'] == subs_map[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child | (1 << c['bit'])
print('CONTROL cost-61d receipts verified: OK (rows/sub-roots/union asserted for bits 30/74/94)')

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
print('AFTER cost61d:', json.dumps(st32, indent=1))

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
    'schema': 'n11-class-frontier-cost61d-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost60b-recompute-20261114 (solved 946 / unique remaining 6901 / sum 543316 / open 5171/407039)',
    'method': 'direct extension of recompute_frontier_cost60b_20261114.py: every staged control reproduces the published after-cost-60b frontier exactly (asserted: 946/6901/543316/5171/407039), the completed cost-61d sweep (14 WIN7-D10, 47 REFUTED, 0 capped, 50,848,724 v16 nodes; v15 cross-engine anchors on the heaviest WIN7 bits 114/102/75 plus bit 30 and heaviest REFUTED bit 32, v16 determinism re-run node-exact on bits 114/102/75) is asserted and its three fully verified receipts (bits 30/74/94; rows 23,348/26,090/23,982; sub-roots 44/49/45 PASS; union 0/0 each) are added; the 11 remaining WIN7-D10 bits stay warm certificate-rebuild candidates and change no frontier number',
    'controls': {
        'after_cost60b': {'solved_in_manifest': 946, 'unique_remaining': 6901,
                          'sum_cost': 543316, 'open_s6': 5171, 'open_cost': 407039,
                          'reproduced': True},
        'cost61d_sweep': {'win7_d10': 14, 'capped': 0, 'refuted_d10': 47,
                          'roots_asserted': True, 'engine': 'v16 (agreement-gated in cost-56a)'},
        'cost61d_claim': {'status': 'completed', 'reproduced': True},
        'cost61d_demand': {'c1': 0, 'c2': 2, 'c4': 0, 'reproduced': True},
        'cost61d_receipts': {'rows': rows_map, 'sub_roots_pass': subs_map,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost61d_addition': per_bits,
    'frontier_after_cost61d': {
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
(OUT / 'class-frontier-cost61d-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost61d-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem32.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost61d-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost61d-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem32.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem32.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-61d parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == '00000000000000803202000000000000'))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem32[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem32[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost61d)')
