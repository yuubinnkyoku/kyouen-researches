#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published (cost-61f
extension) WIN7 receipts as of main (class2-lane cost-61f session 12, 2026-11-14).

Direct extension of recompute_frontier_cost61e_20261114.py via runpy: after
reproducing every published staged control through after-cost-61e (solved 954 /
unique remaining 6893 / sum 542756 / open 5163/406479), the completed cost-61f
sweep (session 12, S6 child 00000000000000803202000080000000 of the second
class-2 target S5 00000000000000803202000000000000: 61 candidates, run on the
v16 runner: 11 WIN7-D10, 50 REFUTED, 0 capped, 45,925,702 v16 nodes) is
asserted and its three fully verified receipts (bits 23/26/99; 47/49/45
sub-roots PASS, union 0/0 each) are added. Per the cost-61e correction lesson,
the child's membership among the parent's remaining children and its non-empty
demand (c1=0,c2=2,c4=0) were re-verified from the after-cost61e frontier BEFORE
the claim; both are re-derived and asserted here. The 8 remaining WIN7-D10 bits
stay warm certificate-rebuild candidates and change no frontier number.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-61e frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost61e_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s51 = ns['s42']
st51 = ns['st42']
rem51 = ns['rem42']
dem51 = ns['dem42']
assert st51['solved_s6_in_manifest'] == 954 and st51['unique_remaining_s6'] == 6893
assert st51['sum_remaining_cost'] == 542756
assert st51['s6_needed_by_open_classes'] == 5163 and st51['cost_needed_by_open_classes'] == 406479
print('CONTROL after-cost61e published frontier reproduced: OK')

# ---------- 2. assert the completed cost-61f sweep record ----------
j61f = json.loads((OUT / 'class2-lane-cost61f-sweep-20261114.json').read_text())
assert j61f['s6_child_hex'] == '00000000000000803202000080000000'
assert j61f['s5_parent_hex'] == '00000000000000803202000000000000'
assert j61f['s6_s7_edge_cost'] == 61 and j61f['capped'] == 0
assert j61f['win7_d10'] == 11 and j61f['refuted_d10'] == 50
assert j61f['total_nodes'] == 45925702
assert j61f['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 0}
child = int(j61f['s6_child_hex'], 16)
for b, r in zip(j61f['win7_bits'], j61f['win7_roots']):
    assert int(r, 16) == child | (1 << b), (b, r)
print('CONTROL completed cost-61f sweep record: OK (11 WIN7, 50 REFUTED, 0 capped, roots asserted)')

# the 61 candidate bits are bit-exact with the independent enumeration
claim = json.loads((OUT / 'class2-lane-cost61f-inflight-20261114.json').read_text())
assert claim['legal_candidates_total'] == 61 and claim['status'].startswith('completed')
assert claim['result']['win7_d10'] == 11 and claim['result']['capped'] == 0
print('CONTROL cost-61f claim updated to completed: OK')

# per the cost-61e correction lesson: the child must be a remaining child of the
# parent with the recorded non-empty demand in the after-cost-61e state
s5_hex = j61f['s5_parent_hex']
rem_child_hexes = {row['s6_hex'] for row in rem51[s5_hex]}
assert j61f['s6_child_hex'] in rem_child_hexes, \
    'cost-61f child must be among the parent remaining children (after-cost61e)'
assert dem51[j61f['s6_child_hex']] == {'c1': 0, 'c2': 2, 'c4': 0}
print('CONTROL cost-61f child demand (c1=0,c2=2,c4=0) and remaining-membership '
      'reproduced from the after-cost61e frontier: OK')

# ---------- 3. add the cost-61f receipts (three fully verified certificates) ----------
w61f = json.loads((OUT / 'class2-lane-cost61f-win7-certificates-20261114.json').read_text())
certs = [c for c in w61f['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs) == 3
assert [c['bit'] for c in certs] == [23, 26, 99]
rows_map = {23: 26256, 26: 30764, 99: 26575}
subs_map = {23: 47, 26: 49, 99: 45}
mob_map = {23: 47, 26: 49, 99: 45}
for c in certs:
    assert c['rows'] == rows_map[c['bit']]
    assert c['sub_roots_pass'] == subs_map[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child | (1 << c['bit'])
print('CONTROL cost-61f receipts verified: OK (rows/sub-roots/union asserted for bits 23/26/99)')

per_bits = {}
marg_union = set()
for c in certs:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s51
    marg_m = marg & manifest
    per_bits[c['bit']] = {
        'root_hex': c['root_hex'],
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union |= marg
s52 = s51 | marg_union
st52, rem52, uniq52, dem52 = summary_state(s52)
print('AFTER cost61f:', json.dumps(st52, indent=1))

# ---------- 4. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem52, 2)
class4 = best(rem52, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost61f-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost61e-recompute-20261114 (solved 954 / unique remaining 6893 / sum 542756 / open 5163/406479)',
    'method': 'direct extension of recompute_frontier_cost61e_20261114.py: every staged control reproduces the published after-cost-61e frontier exactly (asserted: 954/6893/542756/5163/406479), the completed cost-61f sweep (11 WIN7-D10, 50 REFUTED, 0 capped, 45,925,702 v16 nodes; v15 cross-engine anchors on WIN7 bits 102/77/0 plus REFUTED bit 74, v16 determinism re-run node-exact on bits 102/74/77) is asserted and its three fully verified receipts (bits 23/26/99; rows 26,256/30,764/26,575; sub-roots 47/49/45 PASS; union 0/0 each) are added; per the cost-61e correction lesson the child remaining-membership and demand (c1=0,c2=2,c4=0) are re-derived from the frontier and asserted; the 8 remaining WIN7-D10 bits stay warm certificate-rebuild candidates and change no frontier number',
    'controls': {
        'after_cost61e': {'solved_in_manifest': 954, 'unique_remaining': 6893,
                          'sum_cost': 542756, 'open_s6': 5163, 'open_cost': 406479,
                          'reproduced': True},
        'cost61f_sweep': {'win7_d10': 11, 'capped': 0, 'refuted_d10': 50,
                          'roots_asserted': True, 'engine': 'v16 (agreement-gated in cost-56a)'},
        'cost61f_claim': {'status': 'completed', 'reproduced': True},
        'cost61f_demand': {'c1': 0, 'c2': 2, 'c4': 0,
                           'remaining_membership_reproduced': True, 'reproduced': True},
        'cost61f_receipts': {'rows': rows_map, 'sub_roots_pass': subs_map,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost61f_addition': per_bits,
    'frontier_after_cost61f': {
        'solved_s6_in_manifest': st52['solved_s6_in_manifest'],
        'remaining_s5_orbits': st52['remaining_s5_orbits'],
        'unique_remaining_s6': st52['unique_remaining_s6'],
        'sum_remaining_cost': st52['sum_remaining_cost'],
        's6_needed_by_open_classes': st52['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st52['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st52['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost61f-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost61f-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem52.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost61f-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost61f-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem52.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem52.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-61f parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == '00000000000000803202000000000000'))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem52[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem52[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost61f)')
