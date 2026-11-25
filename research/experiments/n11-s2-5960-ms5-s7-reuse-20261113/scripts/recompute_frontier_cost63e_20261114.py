#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published
(cost-63e extension) WIN7 receipts as of main (class2-lane cost-63e session 12,
2026-11-14).

Direct extension of recompute_frontier_merged_after61f_63a65e_20261114.py via
runpy: after reproducing every published staged control through the merged
after-61f+63a+65e frontier (solved 965 / unique remaining 6882 / sum 542020 /
open 5152/405743), the completed cost-63e sweep (session 12, S6 child
00000000000000803202200000000000 of the second class-2 target S5
00000000000000803202000000000000: 63 candidates, run on the v16 runner:
8 WIN7-D10, 55 REFUTED, 0 capped, 50,421,919 v16 nodes) is asserted and its
three fully verified receipts (bits 28/90/97; 47/49/44 sub-roots PASS, union
0/0 each) are added. Per the cost-61e correction lesson, the child's membership
among the parent's remaining children and its non-empty demand (c1=0,c2=2,c4=0)
were re-verified from the after-cost61f frontier BEFORE the claim; both are
re-derived and asserted here against the actual merged baseline (fork
reconciliation: membership in a merged baseline is informative, not assumed).
The 5 remaining WIN7-D10 bits stay warm certificate-rebuild candidates and
change no frontier number.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the merged after-61f+63a+65e frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_merged_after61f_63a65e_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s53 = ns['s53']
st53 = ns['st53']
rem53 = ns['rem53']
dem53 = ns['dem53']
assert st53['solved_s6_in_manifest'] == 965 and st53['unique_remaining_s6'] == 6882
assert st53['sum_remaining_cost'] == 542020
assert st53['s6_needed_by_open_classes'] == 5152 and st53['cost_needed_by_open_classes'] == 405743
print('CONTROL merged after-61f+63a+65e published frontier reproduced: OK')

# ---------- 2. assert the completed cost-63e sweep record ----------
j63e = json.loads((OUT / 'class2-lane-cost63e-sweep-20261114.json').read_text())
assert j63e['s6_child_hex'] == '00000000000000803202200000000000'
assert j63e['s5_parent_hex'] == '00000000000000803202000000000000'
assert j63e['s6_s7_edge_cost'] == 63 and j63e['capped'] == 0
assert j63e['win7_d10'] == 8 and j63e['refuted_d10'] == 55
assert j63e['total_nodes'] == 50421919
assert j63e['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 0}
child63e = int(j63e['s6_child_hex'], 16)
for b, r in zip(j63e['win7_bits'], j63e['win7_roots']):
    assert int(r, 16) == child63e | (1 << b), (b, r)
print('CONTROL completed cost-63e sweep record: OK (8 WIN7, 55 REFUTED, 0 capped, roots asserted)')

# the 63 candidate bits are bit-exact with the independent enumeration
claim63e = json.loads((OUT / 'class2-lane-cost63e-inflight-20261114.json').read_text())
assert claim63e['legal_candidates_total'] == 63 and claim63e['status'].startswith('completed')
assert claim63e['result']['win7_d10'] == 8 and claim63e['result']['capped'] == 0
assert claim63e['candidate_bits'] == sorted(claim63e['candidate_bits']) and len(claim63e['candidate_bits']) == 63
print('CONTROL cost-63e claim updated to completed: OK')

# per the cost-61e correction lesson: the child must be a remaining child of the
# parent with the recorded non-empty demand in the ACTUAL merged baseline
s5_hex63e = j63e['s5_parent_hex']
rem_child_hexes63e = {row['s6_hex'] for row in rem53[s5_hex63e]}
assert j63e['s6_child_hex'] in rem_child_hexes63e, \
    'cost-63e child must be among the parent remaining children (merged baseline)'
dem63e_child = dem53[j63e['s6_child_hex']]
assert dem63e_child == {'c1': 0, 'c2': 2, 'c4': 0}, dem63e_child
print('CONTROL cost-63e child demand (c1=0,c2=2,c4=0) and remaining-membership '
      'reproduced from the merged after-61f+63a+65e frontier: OK')

# ---------- 3. add the cost-63e receipts (three fully verified certificates) ----------
w63e = json.loads((OUT / 'class2-lane-cost63e-win7-certificates-20261114.json').read_text())
certs63e = [c for c in w63e['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs63e) == 3
assert [c['bit'] for c in certs63e] == [28, 90, 97]
rows_map63e = {28: 30830, 90: 26272, 97: 31528}
subs_map63e = {28: 47, 90: 49, 97: 44}
mob_map63e = {28: 47, 90: 49, 97: 44}
for c in certs63e:
    assert c['rows'] == rows_map63e[c['bit']]
    assert c['sub_roots_pass'] == subs_map63e[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map63e[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child63e | (1 << c['bit'])
print('CONTROL cost-63e receipts verified: OK (rows/sub-roots/union asserted for bits 28/90/97)')

per_bits63e = {}
marg_union63e = set()
for c in certs63e:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s53
    marg_m = marg & manifest
    per_bits63e[c['bit']] = {
        'root_hex': c['root_hex'], 'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union63e |= marg
s54 = s53 | marg_union63e
st54, rem54, uniq54, dem54 = summary_state(s54)
print('AFTER cost63e:', json.dumps(st54, indent=1))

# ---------- 4. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem54, 2)
class4 = best(rem54, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost63e-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-merged-recompute-after61f-63a65e-20261114 (solved 965 / unique remaining 6882 / sum 542020 / open 5152/405743)',
    'method': 'direct extension of recompute_frontier_merged_after61f_63a65e_20261114.py: every staged control reproduces the published merged after-61f+63a+65e frontier exactly (asserted: 965/6882/542020/5152/405743), the completed cost-63e sweep (8 WIN7-D10, 55 REFUTED, 0 capped, 50,421,919 v16 nodes; v15 cross-engine anchors on WIN7 bits 116/120/28 plus REFUTED bit 87, v16 determinism re-run node-exact on bits 116/87/120) is asserted and its three fully verified receipts (bits 28/90/97; rows 30,830/26,272/31,528; sub-roots 47/49/44 PASS; union 0/0 each) are added; per the cost-61e correction lesson the child remaining-membership and demand (c1=0,c2=2,c4=0) are re-derived from the ACTUAL merged baseline and asserted (fork reconciliation, not assumed); the 5 remaining WIN7-D10 bits stay warm certificate-rebuild candidates and change no frontier number',
    'controls': {
        'merged_after61f_63a65e': {'solved_in_manifest': 965, 'unique_remaining': 6882,
                                   'sum_cost': 542020, 'open_s6': 5152, 'open_cost': 405743,
                                   'reproduced': True},
        'cost63e_sweep': {'win7_d10': 8, 'capped': 0, 'refuted_d10': 55,
                          'roots_asserted': True, 'engine': 'v16 (agreement-gated in cost-56a)'},
        'cost63e_claim': {'status': 'completed', 'reproduced': True},
        'cost63e_demand': {'c1': 0, 'c2': 2, 'c4': 0,
                           'remaining_membership_reproduced': True, 'reproduced': True},
        'cost63e_receipts': {'rows': rows_map63e, 'sub_roots_pass': subs_map63e,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost63e_addition': per_bits63e,
    'frontier_after_cost63e': {
        'solved_s6_in_manifest': st54['solved_s6_in_manifest'],
        'remaining_s5_orbits': st54['remaining_s5_orbits'],
        'unique_remaining_s6': st54['unique_remaining_s6'],
        'sum_remaining_cost': st54['sum_remaining_cost'],
        's6_needed_by_open_classes': st54['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st54['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st54['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost63e-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost63e-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem54.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost63e-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost63e-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem54.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem54.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-63e parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == '00000000000000803202000000000000'))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem54[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem54[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost63e)')
