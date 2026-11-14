#!/usr/bin/env python3
"""Merged manifest-level class-2/4 frontier recomputation unifying BOTH lanes'
receipts as of main (long-term lane session 11 second run, 2026-11-14).

The class2-lane forked at after-cost-61d: session 12 continued with cost-61e /
cost-61f on the second class-2 target (published chain through
class-frontier-cost61f-recompute-20261114, solved 959 / unique remaining 6888 /
sum 542417 / open 5158/406140), while the long-term lane session 11 completed
cost-63a (10 WIN7-D10, 53 REFUTED, 0 capped, 288,069,056 v15 nodes; bit-119
receipt fully verified) and cost-65e (21 WIN7-D10 - most receipt-rich child so
far, 44 REFUTED, 0 capped, 308,092,253 v15 nodes; bit-107 receipt fully
verified) on the first class-2 target S5 00000000000000809102000000000000.

This script reproduces the published after-cost-61f frontier via runpy (every
staged control asserted), then asserts the completed cost-63a and cost-65e
sweep records, claims and receipts, and adds both receipts: the two branches
merge into a single chain here. Cross-branch coverage interactions are not
assumed: the marginal of each receipt is recomputed against the actual merged
state, and the 63a/65e children's remaining-membership in the after-cost-61f
state is recorded as a control (per the cost-61e correction lesson, membership
in a fork baseline is informative, not guaranteed).
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-61f frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost61f_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s51 = ns['s52']
st51 = ns['st52']
rem51 = ns['rem52']
dem51 = ns['dem52']
assert st51['solved_s6_in_manifest'] == 959 and st51['unique_remaining_s6'] == 6888
assert st51['sum_remaining_cost'] == 542417
assert st51['s6_needed_by_open_classes'] == 5158 and st51['cost_needed_by_open_classes'] == 406140
print('CONTROL after-cost61f published frontier reproduced: OK')

# ---------- 2. assert the completed cost-63a sweep and add its receipt ----------
j63a = json.loads((OUT / 'class2-lane-cost63a-sweep-20261114.json').read_text())
assert j63a['s6_child_hex'] == '00000000000000809102000800000000'
assert j63a['s5_parent_hex'] == '00000000000000809102000000000000'
assert j63a['s6_s7_edge_cost'] == 63 and j63a['capped'] == 0
assert j63a['win7_d10'] == 10 and j63a['refuted_d10'] == 53
assert j63a['total_nodes'] == 288069056
assert j63a['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 0}
child63a = int(j63a['s6_child_hex'], 16)
for b, r in zip(j63a['win7_bits'], j63a['win7_roots']):
    assert int(r, 16) == child63a | (1 << b), (b, r)
claim63a = json.loads((OUT / 'class2-lane-cost63a-inflight-20261114.json').read_text())
assert claim63a['legal_candidates_total'] == 63 and claim63a['status'].startswith('completed')
print('CONTROL completed cost-63a sweep record + claim: OK (10 WIN7, 53 REFUTED, 0 capped)')

# remaining-membership of the 63a child in the after-cost-61f state (informative)
s5_1st = j63a['s5_parent_hex']
mem63a = j63a['s6_child_hex'] in {row['s6_hex'] for row in rem51[s5_1st]}
print(f'CONTROL cost-63a child remaining in after-cost61f state: {mem63a} (recorded)')

w63a = json.loads((OUT / 'class2-lane-cost63a-win7-certificates-20261114.json').read_text())
certs63a = [c for c in w63a['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs63a) == 1 and certs63a[0]['bit'] == 119
c = certs63a[0]
assert c['rows'] == 28509 and c['sub_roots_pass'] == 49
assert c['root_check']['loser_mobility'] == 49
assert c['union_missing'] == 0 and c['union_extra'] == 0
assert int(c['root_hex'], 16) == child63a | (1 << 119)
print('CONTROL cost-63a bit-119 receipt verified: OK (rows/sub-roots/union asserted)')

m63a = {}
marg_union = set()
for c in certs63a:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s51
    marg_m = marg & manifest
    m63a[c['bit']] = {
        'root_hex': c['root_hex'], 'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union |= marg
s52 = s51 | marg_union
st52, rem52, uniq52, dem52 = summary_state(s52)
print('AFTER cost63a-merge:', json.dumps(st52, indent=1))

# ---------- 3. assert the completed cost-65e sweep and add its receipt ----------
j65e = json.loads((OUT / 'class2-lane-cost65e-sweep-20261114.json').read_text())
assert j65e['s6_child_hex'] == '00000000000000809102000000800000'
assert j65e['s5_parent_hex'] == '00000000000000809102000000000000'
assert j65e['s6_s7_edge_cost'] == 65 and j65e['capped'] == 0
assert j65e['win7_d10'] == 21 and j65e['refuted_d10'] == 44
assert j65e['total_nodes'] == 308092253
assert j65e['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 0}
child65e = int(j65e['s6_child_hex'], 16)
for b, r in zip(j65e['win7_bits'], j65e['win7_roots']):
    assert int(r, 16) == child65e | (1 << b), (b, r)
claim65e = json.loads((OUT / 'class2-lane-cost65e-inflight-20261114.json').read_text())
assert claim65e['legal_candidates_total'] == 65 and claim65e['status'].startswith('completed')
assert claim65e['candidate_bits'] == sorted(claim65e['candidate_bits']) and len(claim65e['candidate_bits']) == 65
print('CONTROL completed cost-65e sweep record: OK (21 WIN7, 44 REFUTED, 0 capped, roots asserted)')

# remaining-membership + demand of the 65e child in the merged after-63a state
mem65e = j65e['s6_child_hex'] in {row['s6_hex'] for row in rem52[s5_1st]}
print(f'CONTROL cost-65e child remaining in merged after-63a state: {mem65e} (recorded)')
assert dem52[j65e['s6_child_hex']] == {'c1': 0, 'c2': 2, 'c4': 0}
print('CONTROL cost-65e child demand (c1=0,c2=2,c4=0) reproduced from the merged state: OK')

w65e = json.loads((OUT / 'class2-lane-cost65e-win7-certificates-20261114.json').read_text())
certs65e = [c for c in w65e['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs65e) == 1 and certs65e[0]['bit'] == 107
c = certs65e[0]
assert c['rows'] == 18930 and c['sub_roots_pass'] == 44
assert c['root_check']['loser_mobility'] == 44
assert c['union_missing'] == 0 and c['union_extra'] == 0
assert int(c['root_hex'], 16) == child65e | (1 << 107)
print('CONTROL cost-65e bit-107 receipt verified: OK (rows/sub-roots/union asserted)')

m65e = {}
marg_union2 = set()
for c in certs65e:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s52
    marg_m = marg & manifest
    m65e[c['bit']] = {
        'root_hex': c['root_hex'], 'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union2 |= marg
s53 = s52 | marg_union2
st53, rem53, uniq53, dem53 = summary_state(s53)
print('AFTER cost65e:', json.dumps(st53, indent=1))

# ---------- 4. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem53, 2)
class4 = best(rem53, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-merged-recompute-after61f-63a65e-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost61f-recompute-20261114 (solved 959 / unique remaining 6888 / sum 542417 / open 5158/406140)',
    'method': 'fork reconciliation: the published after-cost-61f frontier is reproduced via runpy of recompute_frontier_cost61f_20261114.py with every staged control asserted (959/6888/542417/5158/406140), then the long-term lane session-11 fork receipts are added: cost-63a (10 WIN7-D10, 53 REFUTED, 0 capped, 288,069,056 v15 nodes; env-reset cross-restart control; bit-119 receipt: 28,509 rows, 49/49 sub-roots, union 0/0) and cost-65e (21 WIN7-D10 - most receipt-rich child so far, 44 REFUTED, 0 capped, 308,092,253 v15 nodes; determinism node-exact on bits 102/88/120/107, fbs20 crosscheck bit-exact on bits 102/88/120 with fbtDrops=0; bit-107 receipt: 18,930 rows, 44/44 sub-roots, union 0/0); cross-branch coverage is recomputed, not assumed: each receipt marginal is derived against the actual merged state and the 63a/65e children remaining-membership in the fork baseline is recorded as a control; the remaining WIN7 bits stay warm certificate-rebuild candidates and change no frontier number',
    'controls': {
        'after_cost61f': {'solved_in_manifest': 959, 'unique_remaining': 6888,
                          'sum_cost': 542417, 'open_s6': 5158, 'open_cost': 406140,
                          'reproduced': True},
        'cost63a_merge': {'win7_d10': 10, 'capped': 0, 'refuted_d10': 53,
                          'receipt_bit': 119, 'roots_asserted': True,
                          'child_remaining_in_after61f': mem63a},
        'cost65e_sweep': {'win7_d10': 21, 'capped': 0, 'refuted_d10': 44,
                          'roots_asserted': True, 'engine': 'v15 (repo-verbatim class4_child1_runner.ts)'},
        'cost65e_claim': {'status': 'completed', 'reproduced': True},
        'cost65e_demand': {'c1': 0, 'c2': 2, 'c4': 0, 'reproduced': True,
                           'child_remaining_in_merged_after63a': mem65e},
        'cost65e_receipts': {'rows': 18930, 'sub_roots_pass': 44,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost63a_merge_addition': m63a,
    'cost65e_addition': m65e,
    'frontier_merged': {
        'solved_s6_in_manifest': st53['solved_s6_in_manifest'],
        'remaining_s5_orbits': st53['remaining_s5_orbits'],
        'unique_remaining_s6': st53['unique_remaining_s6'],
        'sum_remaining_cost': st53['sum_remaining_cost'],
        's6_needed_by_open_classes': st53['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st53['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st53['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'concurrent_lane_note': 'cost-63e (S6 00000000000000803202200000000000 of the second class-2 target, 63 candidates) was an early in-flight claim by session 12 at merge time; its receipts are NOT included here and will fold into the next recompute when completed',
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-merged-recompute-after61f-63a65e-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-merged-recompute-after61f-63a65e-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem53.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-merged-63a65e-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-merged-63a65e-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem53.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem53.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('first class-2 target S5 (cost-63a + cost-65e receipts, this merge)',
                         next(c for c in class2 if c['s5_hex'] == '00000000000000809102000000000000'))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem53[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem53[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-merged-63a65e)')
