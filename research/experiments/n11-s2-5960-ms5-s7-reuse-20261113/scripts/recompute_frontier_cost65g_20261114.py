#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published
(cost-65g extension) WIN7 receipts as of main (class2-lane cost-65g session 12,
2026-11-14).

Direct extension of recompute_frontier_cost64b_20261114.py via runpy: after
reproducing every published staged control through after-cost-64b (solved 974 /
unique remaining 6873 / sum 541401 / open 5143/405124), the completed cost-65g
sweep (session 12, S6 child 00000000000000803202000000000004 of the second
class-2 target S5 00000000000000803202000000000000: 65 candidates, run on the
v16 runner: 9 WIN7-D10, 56 REFUTED, 0 capped, 69,332,778 v16 nodes) is
asserted and its three fully verified receipts (bits 94/1/86; 48/45/57
sub-roots PASS, union 0/0 each) are added. Per the cost-61e correction lesson,
the child's membership among the parent's remaining children and its non-empty
demand (c1=0,c2=2,c4=0) were re-verified from the after-cost-64b frontier
BEFORE the claim; both are re-derived and asserted here. The bit-1 root
00000000000000803202000000000006 is a cross-child duplicate of the cost-61d
win7_roots listing (cost-61e bit-1 pattern) but had NO prior published
certificate, so its receipt is new coverage, not a re-publication. The 6
remaining WIN7-D10 bits stay warm certificate-rebuild candidates and change
no frontier number.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-64b frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost64b_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s55 = ns['s55']
st55 = ns['st55']
rem55 = ns['rem55']
dem55 = ns['dem55']
assert st55['solved_s6_in_manifest'] == 974 and st55['unique_remaining_s6'] == 6873
assert st55['sum_remaining_cost'] == 541401
assert st55['s6_needed_by_open_classes'] == 5143 and st55['cost_needed_by_open_classes'] == 405124
print('CONTROL after-cost64b published frontier reproduced: OK')

# ---------- 2. assert the completed cost-65g sweep record ----------
j65g = json.loads((OUT / 'class2-lane-cost65g-sweep-20261114.json').read_text())
assert j65g['s6_child_hex'] == '00000000000000803202000000000004'
assert j65g['s5_parent_hex'] == '00000000000000803202000000000000'
assert j65g['s6_s7_edge_cost'] == 65 and j65g['capped'] == 0
assert j65g['win7_d10'] == 9 and j65g['refuted_d10'] == 56
assert j65g['total_nodes'] == 69332778
assert j65g['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 0}
child65g = int(j65g['s6_child_hex'], 16)
for b, r in zip(j65g['win7_bits'], j65g['win7_roots']):
    assert int(r, 16) == child65g | (1 << b), (b, r)
print('CONTROL completed cost-65g sweep record: OK (9 WIN7, 56 REFUTED, 0 capped, roots asserted)')

# the 65 candidate bits are bit-exact with the independent enumeration
claim65g = json.loads((OUT / 'class2-lane-cost65g-inflight-20261114.json').read_text())
assert claim65g['legal_candidates_total'] == 65 and claim65g['status'].startswith('completed')
assert claim65g['result']['win7_d10'] == 9 and claim65g['result']['capped'] == 0
assert claim65g['candidate_bits'] == sorted(claim65g['candidate_bits']) and len(claim65g['candidate_bits']) == 65
print('CONTROL cost-65g claim updated to completed: OK')

# per the cost-61e correction lesson: the child must be a remaining child of the
# parent with the recorded non-empty demand in the after-cost-64b state
s5_hex65g = j65g['s5_parent_hex']
rem_child_hexes65g = {row['s6_hex'] for row in rem55[s5_hex65g]}
assert j65g['s6_child_hex'] in rem_child_hexes65g, \
    'cost-65g child must be among the parent remaining children (after-cost64b)'
dem65g_child = dem55[j65g['s6_child_hex']]
assert dem65g_child == {'c1': 0, 'c2': 2, 'c4': 0}, dem65g_child
print('CONTROL cost-65g child demand (c1=0,c2=2,c4=0) and remaining-membership '
      'reproduced from the after-cost64b frontier: OK')

# ---------- 3. add the cost-65g receipts (three fully verified certificates) ----------
w65g = json.loads((OUT / 'class2-lane-cost65g-win7-certificates-20261114.json').read_text())
certs65g = [c for c in w65g['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs65g) == 3
assert [c['bit'] for c in certs65g] == [94, 1, 86]
rows_map65g = {94: 30777, 1: 29005, 86: 39834}
subs_map65g = {94: 48, 1: 45, 86: 57}
mob_map65g = {94: 48, 1: 45, 86: 57}
for c in certs65g:
    assert c['rows'] == rows_map65g[c['bit']]
    assert c['sub_roots_pass'] == subs_map65g[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map65g[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child65g | (1 << c['bit'])
print('CONTROL cost-65g receipts verified: OK (rows/sub-roots/union asserted for bits 94/1/86)')

per_bits65g = {}
marg_union65g = set()
for c in certs65g:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s55
    marg_m = marg & manifest
    per_bits65g[c['bit']] = {
        'root_hex': c['root_hex'], 'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union65g |= marg
s56 = s55 | marg_union65g
st56, rem56, uniq56, dem56 = summary_state(s56)
print('AFTER cost65g:', json.dumps(st56, indent=1))

# ---------- 4. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem56, 2)
class4 = best(rem56, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost65g-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost64b-recompute-20261114 (solved 974 / unique remaining 6873 / sum 541401 / open 5143/405124)',
    'method': 'direct extension of recompute_frontier_cost64b_20261114.py: every staged control reproduces the published after-cost-64b frontier exactly (asserted: 974/6873/541401/5143/405124), the completed cost-65g sweep (9 WIN7-D10, 56 REFUTED, 0 capped, 69,332,778 v16 nodes; v15 cross-engine anchors on WIN7 bits 0/105/44/94 plus REFUTED bit 77, v16 determinism re-run node-exact on bits 0/77/105) is asserted and its three fully verified receipts (bits 94/1/86; rows 30,777/29,005/39,834; sub-roots 48/45/57 PASS; union 0/0 each) are added; the bit-1 root 00000000000000803202000000000006 is a cross-child duplicate of the cost-61d win7_roots listing (cost-61e bit-1 pattern) but had no prior published certificate, so this is new coverage; per the cost-61e correction lesson the child remaining-membership and demand (c1=0,c2=2,c4=0) are re-derived from the frontier and asserted; the 6 remaining WIN7-D10 bits stay warm certificate-rebuild candidates and change no frontier number',
    'controls': {
        'after_cost64b': {'solved_in_manifest': 974, 'unique_remaining': 6873,
                          'sum_cost': 541401, 'open_s6': 5143, 'open_cost': 405124,
                          'reproduced': True},
        'cost65g_sweep': {'win7_d10': 9, 'capped': 0, 'refuted_d10': 56,
                          'roots_asserted': True, 'engine': 'v16 (agreement-gated in cost-56a)'},
        'cost65g_claim': {'status': 'completed', 'reproduced': True},
        'cost65g_demand': {'c1': 0, 'c2': 2, 'c4': 0,
                           'remaining_membership_reproduced': True, 'reproduced': True},
        'cost65g_receipts': {'rows': rows_map65g, 'sub_roots_pass': subs_map65g,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost65g_addition': per_bits65g,
    'frontier_after_cost65g': {
        'solved_s6_in_manifest': st56['solved_s6_in_manifest'],
        'remaining_s5_orbits': st56['remaining_s5_orbits'],
        'unique_remaining_s6': st56['unique_remaining_s6'],
        'sum_remaining_cost': st56['sum_remaining_cost'],
        's6_needed_by_open_classes': st56['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st56['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st56['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost65g-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost65g-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem56.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost65g-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost65g-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem56.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem56.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-65g parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == '00000000000000803202000000000000'))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem56[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem56[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost65g)')
