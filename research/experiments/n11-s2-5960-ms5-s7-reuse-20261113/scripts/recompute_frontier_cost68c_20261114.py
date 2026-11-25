#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published
(cost-68c extension) WIN7 receipts as of main (class2-lane cost-68c, 2026-11-14).

Direct extension of recompute_frontier_cost67b_20261114.py via runpy: after
reproducing every published staged control through after-cost-67b (solved 993 /
unique remaining 6854 / sum 540035 / open 5124/403758), the completed cost-68c
sweep (long-term lane parallel execution, S6 child
00000000000000803202000400000000 of the second class-2 target S5
00000000000000803202000000000000: 68 candidates, run on the v16 runner:
5 WIN7-D10, 63 REFUTED, 0 capped, 104,482,623 v16 nodes; all 5 WIN7 bits have
v15 loss=true cross-engine anchors; node-exact determinism rerun on bits
24/75) is asserted and its three fully verified receipts (bits 21/11/118;
rows 23,096/40,600/31,576; sub-roots 47/50/56 PASS; union 0/0 each) are added.
Per the cost-61e correction lesson, the child's membership among the parent's
remaining children and its non-empty demand (c1=0,c2=1,c4=0) were verified from
the after-cost-67b frontier BEFORE the claim; both are re-derived and asserted
here. The bit-21 WIN7 root 00000000000000803202000400200000 is a cross-child
duplicate of the cost-60b bit-34 win7_roots listing (cost-61e bit-1 pattern)
with no prior published certificate; its certificate here is new coverage and
also closes the cost-60b bit-34 warm entry. The 2 remaining WIN7-D10 bits
(24/53) stay warm certificate-rebuild candidates and change no frontier number.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-67b frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost67b_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s59 = ns['s59']
st59 = ns['st59']
rem59 = ns['rem59']
dem59 = ns['dem59']
assert st59['solved_s6_in_manifest'] == 993 and st59['unique_remaining_s6'] == 6854
assert st59['sum_remaining_cost'] == 540035
assert st59['s6_needed_by_open_classes'] == 5124 and st59['cost_needed_by_open_classes'] == 403758
print('CONTROL after-cost67b published frontier reproduced: OK')

PARENT = '00000000000000803202000000000000'

# ---------- 2. assert the completed cost-68c sweep record ----------
j68c = json.loads((OUT / 'class2-lane-cost68c-sweep-20261114.json').read_text())
assert j68c['s6_child_hex'] == '00000000000000803202000400000000'
assert j68c['s5_parent_hex'] == PARENT
assert j68c['s6_s7_edge_cost'] == 68 and j68c['capped'] == 0
assert j68c['win7_d10'] == 5 and j68c['refuted_d10'] == 63
assert j68c['total_nodes'] == 104482623
assert j68c['demand_classes'] == {'c1': 0, 'c2': 1, 'c4': 0}
child68c = int(j68c['s6_child_hex'], 16)
for b, r in zip(j68c['win7_bits'], j68c['win7_roots']):
    assert int(r, 16) == child68c | (1 << b), (b, r)
claim68c = json.loads((OUT / 'class2-lane-cost68c-inflight-20261114.json').read_text())
assert claim68c['legal_candidates_total'] == 68 and claim68c['status'].startswith('completed')
assert claim68c['result']['win7_d10'] == 5 and claim68c['result']['capped'] == 0
assert claim68c['candidate_bits'] == sorted(claim68c['candidate_bits']) and len(claim68c['candidate_bits']) == 68
print('CONTROL completed cost-68c sweep record: OK (5 WIN7, 63 REFUTED, 0 capped, roots asserted)')

# per the cost-61e correction lesson: the child must be a remaining child of the
# parent with the recorded non-empty demand in the after-cost-67b state
rem_child_hexes68c = {row['s6_hex'] for row in rem59[PARENT]}
assert j68c['s6_child_hex'] in rem_child_hexes68c, \
    'cost-68c child must be among the parent remaining children (after-cost67b)'
dem68c_child = dem59[j68c['s6_child_hex']]
assert dem68c_child == {'c1': 0, 'c2': 1, 'c4': 0}, dem68c_child
print('CONTROL cost-68c child demand (c1=0,c2=1,c4=0) and remaining-membership '
      'reproduced from the after-cost67b frontier: OK')

# ---------- 3. add the cost-68c receipts (three fully verified certificates) ----------
w68c = json.loads((OUT / 'class2-lane-cost68c-win7-certificates-20261114.json').read_text())
certs68c = [c for c in w68c['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs68c) == 3
assert [c['bit'] for c in certs68c] == [21, 11, 118]
rows_map68c = {21: 23096, 11: 40600, 118: 31576}
subs_map68c = {21: 47, 11: 50, 118: 56}
mob_map68c = {21: 47, 11: 50, 118: 56}
for c in certs68c:
    assert c['rows'] == rows_map68c[c['bit']]
    assert c['sub_roots_pass'] == subs_map68c[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map68c[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child68c | (1 << c['bit'])
print('CONTROL cost-68c receipts verified: OK (rows/sub-roots/union asserted for bits 21/11/118)')

per_bits68c = {}
marg_union68c = set()
for c in certs68c:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s59
    marg_m = marg & manifest
    per_bits68c[c['bit']] = {
        'root_hex': c['root_hex'], 'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union68c |= marg
s60 = s59 | marg_union68c
st60, rem60, uniq60, dem60 = summary_state(s60)
print('AFTER cost68c:', json.dumps(st60, indent=1))

# ---------- 4. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem60, 2)
class4 = best(rem60, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost68c-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost67b-recompute-20261114 (solved 993 / unique remaining 6854 / sum 540035 / open 5124/403758)',
    'method': 'direct runpy extension of recompute_frontier_cost67b_20261114.py: every staged control reproduces the published after-cost-67b frontier exactly (asserted: 993/6854/540035/5124/403758), the completed cost-68c sweep (5 WIN7-D10, 63 REFUTED, 0 capped, 104,482,623 v16 nodes; all 5 WIN7 bits have v15 loss=true cross-engine anchors at 1,662,130/4,310,842/2,163,356/7,811,750/4,957,133 nodes; node-exact v16 determinism rerun on bits 24/75) is asserted and its three fully verified receipts (bits 21/11/118; rows 23,096/40,600/31,576; sub-roots 47/50/56 PASS; union 0/0 each) are added; per the cost-61e correction lesson the child remaining-membership and demand (c1=0,c2=1,c4=0) are re-derived from the frontier and asserted; the bit-21 WIN7 root 00000000000000803202000400200000 is a cross-child duplicate of the cost-60b bit-34 win7_roots listing (cost-61e bit-1 pattern) with no prior published certificate, so this certificate is new coverage and also closes the cost-60b bit-34 warm entry; the 2 remaining WIN7-D10 bits (24/53) stay warm certificate-rebuild candidates and change no frontier number',
    'controls': {
        'after_cost67b': {'solved_in_manifest': 993, 'unique_remaining': 6854,
                          'sum_cost': 540035, 'open_s6': 5124, 'open_cost': 403758,
                          'reproduced': True},
        'cost68c_sweep': {'win7_d10': 5, 'capped': 0, 'refuted_d10': 63,
                          'roots_asserted': True, 'engine': 'v16 (agreement-gated in cost-56a)',
                          'lane': 'long-term lane parallel execution'},
        'cost68c_claim': {'status': 'completed', 'reproduced': True},
        'cost68c_demand': {'c1': 0, 'c2': 1, 'c4': 0,
                           'remaining_membership_reproduced': True, 'reproduced': True},
        'cost68c_receipts': {'rows': rows_map68c, 'sub_roots_pass': subs_map68c,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost68c_addition': per_bits68c,
    'frontier_after_cost68c': {
        'solved_s6_in_manifest': st60['solved_s6_in_manifest'],
        'remaining_s5_orbits': st60['remaining_s5_orbits'],
        'unique_remaining_s6': st60['unique_remaining_s6'],
        'sum_remaining_cost': st60['sum_remaining_cost'],
        's6_needed_by_open_classes': st60['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st60['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st60['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost68c-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost68c-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem60.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost68c-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost68c-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem60.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem60.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-68c parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == PARENT))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem60[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem60[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost68c)')
