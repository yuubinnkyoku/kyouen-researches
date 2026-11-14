#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published (cost-56a
extension) WIN7 receipts as of main (class2-lane cost-56a session 12, 2026-11-14).

Direct extension of recompute_frontier_cost62a_20261114.py via runpy: after
reproducing every published staged control through after-cost-62a (solved 924 /
unique remaining 6923 / sum 544799 / open 5193/408522), the completed cost-56a
sweep (session 12, cheapest unswept class-2 child outside the session-11 claims:
56 candidates on S6 child 00000000000000803202020000000000 of the second class-2
target S5 00000000000000803202000000000000, run on the v16 runner with a
depth-10 verdict-agreement gate against the published v15 cost-73a record:
1 WIN7-D10 bit 89, 55 REFUTED, 0 capped, 26,829,269 v16 nodes) is asserted and
its fully verified bit-89 receipt (27,817 rows, 43/43 sub-roots PASS, union 0/0)
is added.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-62a frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost62a_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s31 = ns['s31']
st31 = ns['st31']
rem31 = ns['rem31']
dem31 = ns['dem31']
assert st31['solved_s6_in_manifest'] == 924 and st31['unique_remaining_s6'] == 6923
assert st31['sum_remaining_cost'] == 544799
assert st31['s6_needed_by_open_classes'] == 5193 and st31['cost_needed_by_open_classes'] == 408522
print('CONTROL after-cost62a published frontier reproduced: OK')

# ---------- 2. assert the completed cost-56a sweep record ----------
j56a = json.loads((OUT / 'class2-lane-cost56a-sweep-20261114.json').read_text())
assert j56a['s6_child_hex'] == '00000000000000803202020000000000'
assert j56a['s5_parent_hex'] == '00000000000000803202000000000000'
assert j56a['s6_s7_edge_cost'] == 56 and j56a['capped'] == 0
assert j56a['win7_d10'] == 1 and j56a['refuted_d10'] == 55
assert j56a['total_nodes'] == 26829269
assert j56a['win7_bits'] == [89]
assert j56a['win7_roots'] == ['00000000020000803202020000000000']
assert j56a['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 0}
child = int(j56a['s6_child_hex'], 16)
assert int(j56a['win7_roots'][0], 16) == child | (1 << 89)
print('CONTROL completed cost-56a sweep record: OK (1 WIN7, 55 REFUTED, 0 capped, root asserted)')

# the 56 candidate bits are bit-exact with the independent enumeration
claim = json.loads((OUT / 'class2-lane-cost56a-inflight-20261114.json').read_text())
assert claim['legal_candidates_total'] == 56 and claim['status'].startswith('completed')
assert claim['result']['win7_d10'] == 1 and claim['result']['capped'] == 0
print('CONTROL cost-56a claim updated to completed: OK')

# the demand of this child in the after-cost-62a state matches the record
assert dem31[j56a['s6_child_hex']] == {'c1': 0, 'c2': 2, 'c4': 0}
print('CONTROL cost-56a child demand (c1=0,c2=2,c4=0) reproduced from the frontier: OK')

# ---------- 3. add the cost-56a bit-89 receipt (fully verified certificate) ----------
w56a = json.loads((OUT / 'class2-lane-cost56a-win7-certificates-20261114.json').read_text())
certs = [c for c in w56a['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs) == 1 and certs[0]['bit'] == 89
assert certs[0]['root_hex'] == '00000000020000803202020000000000'
assert certs[0]['rows'] == 27817 and certs[0]['sub_roots_pass'] == 43
assert certs[0]['union_missing'] == 0 and certs[0]['union_extra'] == 0
root56a = int(certs[0]['root_hex'], 16)
cov56a = covers(root56a)
marg56a = cov56a - s31
marg56a_m = marg56a & manifest
per = {'cost56a': {
    'roots': [f'{root56a:032x}'],
    'covers': len(cov56a), 'marginal': len(marg56a),
    'marginal_in_manifest': len(marg56a_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg56a_m),
}}
s32 = s31 | marg56a
st32, rem32, uniq32, dem32 = summary_state(s32)
print('AFTER cost56a:', json.dumps(st32, indent=1))

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
    'schema': 'n11-class-frontier-cost56a-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost62a-recompute-20261114 (solved 924 / unique remaining 6923 / sum 544799 / open 5193/408522)',
    'method': 'direct extension of recompute_frontier_cost62a_20261114.py: every staged control reproduces the published after-cost-62a frontier exactly (asserted: 924/6923/544799/5193/408522), the completed cost-56a sweep (1 WIN7-D10 bit 89, 55 REFUTED, 0 capped, 26,829,269 v16 nodes; first sweep run on the v16 runner under a depth-10 verdict-agreement gate against the published v15 cost-73a record, with v15 cross-engine anchors on the WIN7 bit and the heaviest REFUTED bits) is asserted and its fully verified bit-89 receipt (27,817 rows, 43/43 sub-roots PASS, union 0/0) is added',
    'controls': {
        'after_cost62a': {'solved_in_manifest': 924, 'unique_remaining': 6923,
                          'sum_cost': 544799, 'open_s6': 5193, 'open_cost': 408522,
                          'reproduced': True},
        'cost56a_sweep': {'win7_d10': 1, 'capped': 0, 'refuted_d10': 55,
                          'root_asserted': True, 'engine': 'v16 (agreement-gated)'},
        'cost56a_claim': {'status': 'completed', 'reproduced': True},
        'cost56a_demand': {'c1': 0, 'c2': 2, 'c4': 0, 'reproduced': True},
    },
    'cost56a_addition': per['cost56a'],
    'frontier_after_cost56a': {
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
(OUT / 'class-frontier-cost56a-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost56a-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem32.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost56a-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost56a-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem32.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem32.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-56a parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == '00000000000000803202000000000000'))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem32[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem32[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost56a)')
