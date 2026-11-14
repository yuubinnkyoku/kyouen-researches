#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published
(cost-67b extension) WIN7 receipts as of main (class2-lane cost-67b, 2026-11-14).

Direct extension of recompute_frontier_cost65h_65i_20261114.py via runpy: after
reproducing every published staged control through after-cost-65h+65i (solved
991 / unique remaining 6856 / sum 540177 / open 5126/403900), the completed
cost-67b sweep (long-term lane parallel execution, S6 child
00000000000000803202000020000000 of the second class-2 target S5
00000000000000803202000000000000: 67 candidates, run on the v16 runner:
7 WIN7-D10, 60 REFUTED, 0 capped, 64,859,548 v16 nodes; all 7 WIN7 bits have
v15 loss=true cross-engine anchors; node-exact determinism rerun on bits
33/6/99) is asserted and its three fully verified receipts (bits 17/117/109;
rows 34,860/32,441/27,559; sub-roots 47/50/47 PASS; union 0/0 each) are added.
Per the cost-61e correction lesson, the child's membership among the parent's
remaining children and its non-empty demand (c1=0,c2=2,c4=0) were verified from
the after-cost-65h-65i frontier BEFORE the claim; both are re-derived and
asserted here. The bit-20 WIN7 root 00000000000000803202000020100000 is a
cross-child duplicate of the cost-64b bit-29 win7_roots listing (cost-61e
bit-1 pattern) but has no prior published certificate; it stays a warm
certificate-rebuild candidate together with bits 11/33/99 and changes no
frontier number.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-65h-65i frontier (asserts all controls) ----------
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

PARENT = '00000000000000803202000000000000'

# ---------- 2. assert the completed cost-67b sweep record ----------
j67b = json.loads((OUT / 'class2-lane-cost67b-sweep-20261114.json').read_text())
assert j67b['s6_child_hex'] == '00000000000000803202000020000000'
assert j67b['s5_parent_hex'] == PARENT
assert j67b['s6_s7_edge_cost'] == 67 and j67b['capped'] == 0
assert j67b['win7_d10'] == 7 and j67b['refuted_d10'] == 60
assert j67b['total_nodes'] == 64859548
assert j67b['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 0}
child67b = int(j67b['s6_child_hex'], 16)
for b, r in zip(j67b['win7_bits'], j67b['win7_roots']):
    assert int(r, 16) == child67b | (1 << b), (b, r)
claim67b = json.loads((OUT / 'class2-lane-cost67b-inflight-20261114.json').read_text())
assert claim67b['legal_candidates_total'] == 67 and claim67b['status'].startswith('completed')
assert claim67b['result']['win7_d10'] == 7 and claim67b['result']['capped'] == 0
assert claim67b['candidate_bits'] == sorted(claim67b['candidate_bits']) and len(claim67b['candidate_bits']) == 67
print('CONTROL completed cost-67b sweep record: OK (7 WIN7, 60 REFUTED, 0 capped, roots asserted)')

# per the cost-61e correction lesson: the child must be a remaining child of the
# parent with the recorded non-empty demand in the after-cost-65h-65i state
rem_child_hexes67b = {row['s6_hex'] for row in rem58[PARENT]}
assert j67b['s6_child_hex'] in rem_child_hexes67b, \
    'cost-67b child must be among the parent remaining children (after-cost65h-65i)'
dem67b_child = dem58[j67b['s6_child_hex']]
assert dem67b_child == {'c1': 0, 'c2': 2, 'c4': 0}, dem67b_child
print('CONTROL cost-67b child demand (c1=0,c2=2,c4=0) and remaining-membership '
      'reproduced from the after-cost65h-65i frontier: OK')

# ---------- 3. add the cost-67b receipts (three fully verified certificates) ----------
w67b = json.loads((OUT / 'class2-lane-cost67b-win7-certificates-20261114.json').read_text())
certs67b = [c for c in w67b['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs67b) == 3
assert [c['bit'] for c in certs67b] == [17, 117, 109]
rows_map67b = {17: 34860, 117: 32441, 109: 27559}
subs_map67b = {17: 47, 117: 50, 109: 47}
mob_map67b = {17: 47, 117: 50, 109: 47}
for c in certs67b:
    assert c['rows'] == rows_map67b[c['bit']]
    assert c['sub_roots_pass'] == subs_map67b[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map67b[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child67b | (1 << c['bit'])
print('CONTROL cost-67b receipts verified: OK (rows/sub-roots/union asserted for bits 17/117/109)')

per_bits67b = {}
marg_union67b = set()
for c in certs67b:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s58
    marg_m = marg & manifest
    per_bits67b[c['bit']] = {
        'root_hex': c['root_hex'], 'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union67b |= marg
s59 = s58 | marg_union67b
st59, rem59, uniq59, dem59 = summary_state(s59)
print('AFTER cost67b:', json.dumps(st59, indent=1))

# ---------- 4. new ranking ----------
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
    'schema': 'n11-class-frontier-cost67b-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost65h-65i-recompute-20261114 (solved 991 / unique remaining 6856 / sum 540177 / open 5126/403900)',
    'method': 'direct runpy extension of recompute_frontier_cost65h_65i_20261114.py: every staged control reproduces the published after-cost-65h-65i frontier exactly (asserted: 991/6856/540177/5126/403900), the completed cost-67b sweep (7 WIN7-D10, 60 REFUTED, 0 capped, 64,859,548 v16 nodes; all 7 WIN7 bits have v15 loss=true cross-engine anchors at 3,201,038/1,775,234/2,055,608/6,238,220/2,176,741/2,011,805/1,840,199 nodes; node-exact v16 determinism rerun on bits 33/6/99) is asserted and its three fully verified receipts (bits 17/117/109; rows 34,860/32,441/27,559; sub-roots 47/50/47 PASS; union 0/0 each) are added; per the cost-61e correction lesson the child remaining-membership and demand (c1=0,c2=2,c4=0) are re-derived from the frontier and asserted; the bit-20 WIN7 root 00000000000000803202000020100000 is a cross-child duplicate of the cost-64b bit-29 win7_roots listing (cost-61e bit-1 pattern) with no prior published certificate, so a future certificate for it is new coverage; the 4 remaining WIN7-D10 bits (11/20/33/99) stay warm certificate-rebuild candidates and change no frontier number',
    'controls': {
        'after_cost65h_65i': {'solved_in_manifest': 991, 'unique_remaining': 6856,
                              'sum_cost': 540177, 'open_s6': 5126, 'open_cost': 403900,
                              'reproduced': True},
        'cost67b_sweep': {'win7_d10': 7, 'capped': 0, 'refuted_d10': 60,
                          'roots_asserted': True, 'engine': 'v16 (agreement-gated in cost-56a)',
                          'lane': 'long-term lane parallel execution'},
        'cost67b_claim': {'status': 'completed', 'reproduced': True},
        'cost67b_demand': {'c1': 0, 'c2': 2, 'c4': 0,
                           'remaining_membership_reproduced': True, 'reproduced': True},
        'cost67b_receipts': {'rows': rows_map67b, 'sub_roots_pass': subs_map67b,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost67b_addition': per_bits67b,
    'frontier_after_cost67b': {
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
(OUT / 'class-frontier-cost67b-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost67b-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem59.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost67b-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost67b-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem59.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem59.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-67b parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == PARENT))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem59[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem59[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost67b)')
