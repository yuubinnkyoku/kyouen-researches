#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published
(cost-65h + cost-65i extension) WIN7 receipts as of main (class2-lane
cost-65h/65i session 12, 2026-11-14).

Direct extension of recompute_frontier_cost65g_20261114.py via runpy: after
reproducing every published staged control through after-cost-65g (solved 979 /
unique remaining 6868 / sum 541041 / open 5138/404764), TWO completed sibling
sweeps of the second class-2 target's cost-65 band pair are asserted and their
receipts added in a single merged recompute:

- cost-65h (parallel lane session 12, S6 child 00000000000000803202000000001000:
  65 candidates, v16 runner: 13 WIN7-D10, 52 REFUTED, 0 capped, 57,639,642
  v16 nodes; receipts bits 7/109/24; 51/50/50 sub-roots PASS, union 0/0 each).
- cost-65i (this lane session 12, S6 child 00000000000000803202000000080000:
  65 candidates, v16 runner: 3 WIN7-D10, 62 REFUTED, 0 capped, 41,416,752
  v16 nodes; receipts bits 7/43/99; 45/53/50 sub-roots PASS, union 0/0 each -
  zero unverified WIN7 bits for this sweep).

Per the cost-61e correction lesson, both children's membership among the
parent's remaining children and their non-empty demands (65h: c1=0,c2=2,c4=0;
65i: c1=0,c2=2,c4=2) were verified from the after-cost-65g frontier BEFORE the
claims; both are re-derived here (65i's demand is re-derived from the
after-cost-65h intermediate state and recorded). The 10 remaining cost-65h
WIN7-D10 bits stay warm certificate-rebuild candidates and change no frontier
number.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-65g frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost65g_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s56 = ns['s56']
st56 = ns['st56']
rem56 = ns['rem56']
dem56 = ns['dem56']
assert st56['solved_s6_in_manifest'] == 979 and st56['unique_remaining_s6'] == 6868
assert st56['sum_remaining_cost'] == 541041
assert st56['s6_needed_by_open_classes'] == 5138 and st56['cost_needed_by_open_classes'] == 404764
print('CONTROL after-cost65g published frontier reproduced: OK')

PARENT = '00000000000000803202000000000000'

# ---------- 2. assert the completed cost-65h sweep record (parallel lane) ----------
j65h = json.loads((OUT / 'class2-lane-cost65h-sweep-20261114.json').read_text())
assert j65h['s6_child_hex'] == '00000000000000803202000000001000'
assert j65h['s5_parent_hex'] == PARENT
assert j65h['s6_s7_edge_cost'] == 65 and j65h['capped'] == 0
assert j65h['win7_d10'] == 13 and j65h['refuted_d10'] == 52
assert j65h['total_nodes'] == 57639642
assert j65h['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 0}
child65h = int(j65h['s6_child_hex'], 16)
for b, r in zip(j65h['win7_bits'], j65h['win7_roots']):
    assert int(r, 16) == child65h | (1 << b), (b, r)
claim65h = json.loads((OUT / 'class2-lane-cost65h-inflight-20261114.json').read_text())
assert claim65h['legal_candidates_total'] == 65 and claim65h['status'].startswith('completed')
assert claim65h['result']['win7_d10'] == 13 and claim65h['result']['capped'] == 0
assert claim65h['candidate_bits'] == sorted(claim65h['candidate_bits']) and len(claim65h['candidate_bits']) == 65
rem_child_hexes65h = {row['s6_hex'] for row in rem56[PARENT]}
assert j65h['s6_child_hex'] in rem_child_hexes65h, \
    'cost-65h child must be among the parent remaining children (after-cost65g)'
dem65h_child = dem56[j65h['s6_child_hex']]
assert dem65h_child == {'c1': 0, 'c2': 2, 'c4': 0}, dem65h_child
print('CONTROL completed cost-65h sweep/claim/demand (after-cost65g state): OK')

w65h = json.loads((OUT / 'class2-lane-cost65h-win7-certificates-20261114.json').read_text())
certs65h = [c for c in w65h['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs65h) == 3
assert [c['bit'] for c in certs65h] == [7, 109, 24]
rows_map65h = {7: 28375, 109: 26774, 24: 38440}
subs_map65h = {7: 51, 109: 50, 24: 50}
mob_map65h = {7: 51, 109: 50, 24: 50}
for c in certs65h:
    assert c['rows'] == rows_map65h[c['bit']]
    assert c['sub_roots_pass'] == subs_map65h[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map65h[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child65h | (1 << c['bit'])
print('CONTROL cost-65h receipts verified: OK (rows/sub-roots/union asserted for bits 7/109/24)')

# ---------- 3. assert the completed cost-65i sweep record (this lane) ----------
j65i = json.loads((OUT / 'class2-lane-cost65i-sweep-20261114.json').read_text())
assert j65i['s6_child_hex'] == '00000000000000803202000000080000'
assert j65i['s5_parent_hex'] == PARENT
assert j65i['s6_s7_edge_cost'] == 65 and j65i['capped'] == 0
assert j65i['win7_d10'] == 3 and j65i['refuted_d10'] == 62
assert j65i['total_nodes'] == 41416752
assert j65i['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 2}
child65i = int(j65i['s6_child_hex'], 16)
for b, r in zip(j65i['win7_bits'], j65i['win7_roots']):
    assert int(r, 16) == child65i | (1 << b), (b, r)
claim65i = json.loads((OUT / 'class2-lane-cost65i-inflight-20261114.json').read_text())
assert claim65i['legal_candidates_total'] == 65 and claim65i['status'].startswith('completed')
assert claim65i['result']['win7_d10'] == 3 and claim65i['result']['capped'] == 0
assert claim65i['candidate_bits'] == sorted(claim65i['candidate_bits']) and len(claim65i['candidate_bits']) == 65
rem_child_hexes65i = {row['s6_hex'] for row in rem56[PARENT]}
assert j65i['s6_child_hex'] in rem_child_hexes65i, \
    'cost-65i child must be among the parent remaining children (after-cost65g)'
dem65i_child_claim = dem56[j65i['s6_child_hex']]
assert dem65i_child_claim == {'c1': 0, 'c2': 2, 'c4': 2}, dem65i_child_claim
print('CONTROL completed cost-65i sweep/claim/demand (after-cost65g state): OK')

w65i = json.loads((OUT / 'class2-lane-cost65i-win7-certificates-20261114.json').read_text())
certs65i = [c for c in w65i['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs65i) == 3
assert [c['bit'] for c in certs65i] == [7, 43, 99]
rows_map65i = {7: 26034, 43: 44467, 99: 30066}
subs_map65i = {7: 45, 43: 53, 99: 50}
mob_map65i = {7: 45, 43: 53, 99: 50}
for c in certs65i:
    assert c['rows'] == rows_map65i[c['bit']]
    assert c['sub_roots_pass'] == subs_map65i[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map65i[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child65i | (1 << c['bit'])
print('CONTROL cost-65i receipts verified: OK (rows/sub-roots/union asserted for bits 7/43/99)')

# ---------- 4. add the cost-65h receipts, then re-derive the 65i demand ----------
per_bits65h = {}
marg_union65h = set()
for c in certs65h:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s56
    marg_m = marg & manifest
    per_bits65h[c['bit']] = {
        'root_hex': c['root_hex'], 'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union65h |= marg
s57 = s56 | marg_union65h
st57, rem57, uniq57, dem57 = summary_state(s57)
print('AFTER cost65h (intermediate):', json.dumps(st57, indent=1))

# the 65i child's remaining-membership and demand are re-derived from the
# after-cost-65h intermediate state (recorded; asserted non-empty)
rem_child_hexes57 = {row['s6_hex'] for row in rem57[PARENT]}
assert j65i['s6_child_hex'] in rem_child_hexes57, \
    'cost-65i child must still be among the parent remaining children (after-cost65h)'
dem65i_child_after65h = dem57[j65i['s6_child_hex']]
assert (dem65i_child_after65h['c1'] + dem65i_child_after65h['c2'] +
        dem65i_child_after65h['c4']) > 0, dem65i_child_after65h
print('CONTROL cost-65i child still remaining after cost-65h; demand re-derived:',
      json.dumps(dem65i_child_after65h))

# ---------- 5. add the cost-65i receipts ----------
per_bits65i = {}
marg_union65i = set()
for c in certs65i:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s57
    marg_m = marg & manifest
    per_bits65i[c['bit']] = {
        'root_hex': c['root_hex'], 'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union65i |= marg
s58 = s57 | marg_union65i
st58, rem58, uniq58, dem58 = summary_state(s58)
print('AFTER cost65h+65i:', json.dumps(st58, indent=1))

# ---------- 6. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem58, 2)
class4 = best(rem58, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost65h-65i-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost65g-recompute-20261114 (solved 979 / unique remaining 6868 / sum 541041 / open 5138/404764)',
    'method': 'direct runpy extension of recompute_frontier_cost65g_20261114.py in a single merged recompute of the cost-65 band pair (both lanes): every staged control reproduces the published after-cost-65g frontier exactly (asserted: 979/6868/541041/5138/404764), then the parallel lane\'s completed cost-65h sweep (13 WIN7-D10, 52 REFUTED, 0 capped, 57,639,642 v16 nodes) and its three fully verified receipts (bits 7/109/24; rows 28,375/26,774/38,440; sub-roots 51/50/50 PASS; union 0/0 each) are asserted and added, the cost-65i child remaining-membership and demand are re-derived from the after-cost-65h intermediate state (recorded), then this lane\'s completed cost-65i sweep (3 WIN7-D10, 62 REFUTED, 0 capped, 41,416,752 v16 nodes) and its three fully verified receipts (bits 7/43/99; rows 26,034/44,467/30,066; sub-roots 45/53/50 PASS; union 0/0 each; zero unverified WIN7 bits) are asserted and added; per the cost-61e correction lesson both children\'s remaining-memberships and demands are re-derived and asserted; the 10 remaining cost-65h WIN7-D10 bits stay warm certificate-rebuild candidates and change no frontier number',
    'controls': {
        'after_cost65g': {'solved_in_manifest': 979, 'unique_remaining': 6868,
                          'sum_cost': 541041, 'open_s6': 5138, 'open_cost': 404764,
                          'reproduced': True},
        'cost65h_sweep': {'win7_d10': 13, 'capped': 0, 'refuted_d10': 52,
                          'roots_asserted': True, 'engine': 'v16 (agreement-gated in cost-56a)',
                          'lane': 'parallel long-term lane session 12'},
        'cost65h_claim': {'status': 'completed', 'reproduced': True},
        'cost65h_demand': {'c1': 0, 'c2': 2, 'c4': 0,
                           'remaining_membership_reproduced': True, 'reproduced': True},
        'cost65h_receipts': {'rows': rows_map65h, 'sub_roots_pass': subs_map65h,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
        'cost65i_sweep': {'win7_d10': 3, 'capped': 0, 'refuted_d10': 62,
                          'roots_asserted': True, 'engine': 'v16 (agreement-gated in cost-56a)'},
        'cost65i_claim': {'status': 'completed', 'reproduced': True},
        'cost65i_demand_after_cost65g': {'c1': 0, 'c2': 2, 'c4': 2, 'reproduced': True},
        'cost65i_demand_after_cost65h': dem65i_child_after65h,
        'cost65i_receipts': {'rows': rows_map65i, 'sub_roots_pass': subs_map65i,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost65h_addition': per_bits65h,
    'cost65i_addition': per_bits65i,
    'frontier_after_cost65h_intermediate': {
        'solved_s6_in_manifest': st57['solved_s6_in_manifest'],
        'unique_remaining_s6': st57['unique_remaining_s6'],
        'sum_remaining_cost': st57['sum_remaining_cost'],
        's6_needed_by_open_classes': st57['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st57['cost_needed_by_open_classes'],
    },
    'frontier_after_cost65h_65i': {
        'solved_s6_in_manifest': st58['solved_s6_in_manifest'],
        'remaining_s5_orbits': st58['remaining_s5_orbits'],
        'unique_remaining_s6': st58['unique_remaining_s6'],
        'sum_remaining_cost': st58['sum_remaining_cost'],
        's6_needed_by_open_classes': st58['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st58['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st58['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost65h-65i-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost65h-65i-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem58.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost65h-65i-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost65h-65i-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem58.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem58.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-65h/65i parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == PARENT))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem58[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem58[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost65h-65i)')
