#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published
(cost-64b extension) WIN7 receipts as of main (class2-lane cost-64b session 12,
2026-11-14).

Direct extension of recompute_frontier_cost63e_20261114.py via runpy: after
reproducing every published staged control through after-cost-63e (solved 970 /
unique remaining 6877 / sum 541680 / open 5147/405403), the completed cost-64b
sweep (session 12, S6 child 00000000000000803202000000100000 of the second
class-2 target S5 00000000000000803202000000000000: 64 candidates, run on the
v16 runner: 20 WIN7-D10, 44 REFUTED, 0 capped, 50,655,645 v16 nodes) is
asserted and its three fully verified receipts (bits 73/7/99; 49/48/48
sub-roots PASS, union 0/0 each) are added. Per the cost-61e correction lesson,
the child's membership among the parent's remaining children and its non-empty
demand (c1=0,c2=2,c4=0) were re-verified from the after-cost-63e frontier
BEFORE the claim; both are re-derived and asserted here. The 17 remaining
WIN7-D10 bits stay warm certificate-rebuild candidates and change no frontier
number.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-63e frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost63e_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s54 = ns['s54']
st54 = ns['st54']
rem54 = ns['rem54']
dem54 = ns['dem54']
assert st54['solved_s6_in_manifest'] == 970 and st54['unique_remaining_s6'] == 6877
assert st54['sum_remaining_cost'] == 541680
assert st54['s6_needed_by_open_classes'] == 5147 and st54['cost_needed_by_open_classes'] == 405403
print('CONTROL after-cost63e published frontier reproduced: OK')

# ---------- 2. assert the completed cost-64b sweep record ----------
j64b = json.loads((OUT / 'class2-lane-cost64b-sweep-20261114.json').read_text())
assert j64b['s6_child_hex'] == '00000000000000803202000000100000'
assert j64b['s5_parent_hex'] == '00000000000000803202000000000000'
assert j64b['s6_s7_edge_cost'] == 64 and j64b['capped'] == 0
assert j64b['win7_d10'] == 20 and j64b['refuted_d10'] == 44
assert j64b['total_nodes'] == 50655645
assert j64b['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 0}
child64b = int(j64b['s6_child_hex'], 16)
for b, r in zip(j64b['win7_bits'], j64b['win7_roots']):
    assert int(r, 16) == child64b | (1 << b), (b, r)
print('CONTROL completed cost-64b sweep record: OK (20 WIN7, 44 REFUTED, 0 capped, roots asserted)')

# the 64 candidate bits are bit-exact with the independent enumeration
claim64b = json.loads((OUT / 'class2-lane-cost64b-inflight-20261114.json').read_text())
assert claim64b['legal_candidates_total'] == 64 and claim64b['status'].startswith('completed')
assert claim64b['result']['win7_d10'] == 20 and claim64b['result']['capped'] == 0
assert claim64b['candidate_bits'] == sorted(claim64b['candidate_bits']) and len(claim64b['candidate_bits']) == 64
print('CONTROL cost-64b claim updated to completed: OK')

# per the cost-61e correction lesson: the child must be a remaining child of the
# parent with the recorded non-empty demand in the after-cost-63e state
s5_hex64b = j64b['s5_parent_hex']
rem_child_hexes64b = {row['s6_hex'] for row in rem54[s5_hex64b]}
assert j64b['s6_child_hex'] in rem_child_hexes64b, \
    'cost-64b child must be among the parent remaining children (after-cost63e)'
dem64b_child = dem54[j64b['s6_child_hex']]
assert dem64b_child == {'c1': 0, 'c2': 2, 'c4': 0}, dem64b_child
print('CONTROL cost-64b child demand (c1=0,c2=2,c4=0) and remaining-membership '
      'reproduced from the after-cost63e frontier: OK')

# ---------- 3. add the cost-64b receipts (three fully verified certificates) ----------
w64b = json.loads((OUT / 'class2-lane-cost64b-win7-certificates-20261114.json').read_text())
certs64b = [c for c in w64b['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs64b) == 3
assert [c['bit'] for c in certs64b] == [73, 7, 99]
rows_map64b = {73: 28046, 7: 21382, 99: 26812}
subs_map64b = {73: 49, 7: 48, 99: 48}
mob_map64b = {73: 49, 7: 48, 99: 48}
for c in certs64b:
    assert c['rows'] == rows_map64b[c['bit']]
    assert c['sub_roots_pass'] == subs_map64b[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map64b[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child64b | (1 << c['bit'])
print('CONTROL cost-64b receipts verified: OK (rows/sub-roots/union asserted for bits 73/7/99)')

per_bits64b = {}
marg_union64b = set()
for c in certs64b:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s54
    marg_m = marg & manifest
    per_bits64b[c['bit']] = {
        'root_hex': c['root_hex'], 'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union64b |= marg
s55 = s54 | marg_union64b
st55, rem55, uniq55, dem55 = summary_state(s55)
print('AFTER cost64b:', json.dumps(st55, indent=1))

# ---------- 4. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem55, 2)
class4 = best(rem55, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost64b-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost63e-recompute-20261114 (solved 970 / unique remaining 6877 / sum 541680 / open 5147/405403)',
    'method': 'direct extension of recompute_frontier_cost63e_20261114.py: every staged control reproduces the published after-cost-63e frontier exactly (asserted: 970/6877/541680/5147/405403), the completed cost-64b sweep (20 WIN7-D10 - the second most WIN7-rich class-2 child after cost-60b, 44 REFUTED, 0 capped, 50,655,645 v16 nodes; v15 cross-engine anchors on WIN7 bits 73/43/92 plus REFUTED bit 77, v16 determinism re-run node-exact on bits 43/77/92) is asserted and its three fully verified receipts (bits 73/7/99; rows 28,046/21,382/26,812; sub-roots 49/48/48 PASS; union 0/0 each) are added; per the cost-61e correction lesson the child remaining-membership and demand (c1=0,c2=2,c4=0) are re-derived from the frontier and asserted; the 17 remaining WIN7-D10 bits stay warm certificate-rebuild candidates and change no frontier number',
    'controls': {
        'after_cost63e': {'solved_in_manifest': 970, 'unique_remaining': 6877,
                          'sum_cost': 541680, 'open_s6': 5147, 'open_cost': 405403,
                          'reproduced': True},
        'cost64b_sweep': {'win7_d10': 20, 'capped': 0, 'refuted_d10': 44,
                          'roots_asserted': True, 'engine': 'v16 (agreement-gated in cost-56a)'},
        'cost64b_claim': {'status': 'completed', 'reproduced': True},
        'cost64b_demand': {'c1': 0, 'c2': 2, 'c4': 0,
                           'remaining_membership_reproduced': True, 'reproduced': True},
        'cost64b_receipts': {'rows': rows_map64b, 'sub_roots_pass': subs_map64b,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost64b_addition': per_bits64b,
    'frontier_after_cost64b': {
        'solved_s6_in_manifest': st55['solved_s6_in_manifest'],
        'remaining_s5_orbits': st55['remaining_s5_orbits'],
        'unique_remaining_s6': st55['unique_remaining_s6'],
        'sum_remaining_cost': st55['sum_remaining_cost'],
        's6_needed_by_open_classes': st55['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st55['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st55['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost64b-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost64b-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem55.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost64b-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost64b-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem55.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem55.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-64b parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == '00000000000000803202000000000000'))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem55[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem55[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost64b)')
