#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published (cost-63a
extension) WIN7 receipts as of main (class2-lane cost-63a, long-term lane session 11
second run, 2026-11-14).

Direct extension of recompute_frontier_cost61d_20261114.py via runpy: after
reproducing every published staged control through after-cost-61d (solved 951 /
unique remaining 6896 / sum 542952 / open 5166/406675), the completed cost-63a
sweep (cheapest remaining unswept child of the class-2 target S5
00000000000000809102000000000000: 63 candidates on S6 child
00000000000000809102000800000000, v15 engine: 10 WIN7-D10, 53 REFUTED, 0 capped,
288,069,056 nodes; determinism re-runs node-exact on bits 32/2/119/11, fbs20
cross-engine bit-exact on bits 32/2/119 with fbtDrops=0, env-reset cross-restart
reproduction control) is asserted and its fully verified bit-119 receipt (28,509
rows, 49/49 sub-roots PASS, union 0/0, fbt_drops=0) is added. The 9 remaining
WIN7-D10 bits stay warm certificate-rebuild candidates and change no frontier
number. The parallel lane's cost-61e sweep is in flight at this baseline and is not
counted; the completed cost-61d sweep (14 WIN7-D10, 3 verified receipts, frontier
946 -> 951) is part of the asserted baseline.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-61d frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost61d_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s31 = ns['s32']
st31 = ns['st32']
rem31 = ns['rem32']
dem31 = ns['dem32']
assert st31['solved_s6_in_manifest'] == 951 and st31['unique_remaining_s6'] == 6896
assert st31['sum_remaining_cost'] == 542952
assert st31['s6_needed_by_open_classes'] == 5166 and st31['cost_needed_by_open_classes'] == 406675
print('CONTROL after-cost61d published frontier reproduced: OK')

# ---------- 2. assert the completed cost-63a sweep record ----------
j63a = json.loads((OUT / 'class2-lane-cost63a-sweep-20261114.json').read_text())
assert j63a['s6_child_hex'] == '00000000000000809102000800000000'
assert j63a['s5_parent_hex'] == '00000000000000809102000000000000'
assert j63a['s6_s7_edge_cost'] == 63 and j63a['capped'] == 0
assert j63a['win7_d10'] == 10 and j63a['refuted_d10'] == 53
assert j63a['total_nodes'] == 288069056
assert j63a['demand_classes'] == {'c1': 0, 'c2': 2, 'c4': 0}
child = int(j63a['s6_child_hex'], 16)
for b, r in zip(j63a['win7_bits'], j63a['win7_roots']):
    assert int(r, 16) == child | (1 << b), (b, r)
print('CONTROL completed cost-63a sweep record: OK (10 WIN7, 53 REFUTED, 0 capped, roots asserted)')

# the 63 candidate bits are bit-exact with the independent enumeration
claim = json.loads((OUT / 'class2-lane-cost63a-inflight-20261114.json').read_text())
assert claim['legal_candidates_total'] == 63 and claim['status'].startswith('completed')
assert claim['result']['win7_d10'] == 10 and claim['result']['capped'] == 0
assert claim['candidate_bits'] == sorted(claim['candidate_bits']) and len(claim['candidate_bits']) == 63
print('CONTROL cost-63a claim updated to completed: OK (63 candidates, sorted, bit-exact)')

# the demand of this child in the after-cost-61d state matches the record
assert dem31[j63a['s6_child_hex']] == {'c1': 0, 'c2': 2, 'c4': 0}
print('CONTROL cost-63a child demand (c1=0,c2=2,c4=0) reproduced from the frontier: OK')

# the child is the cheapest remaining unswept child of its S5 in the after-61d state
rem_parent = rem31['00000000000000809102000000000000']
min_cost = min(int(r['s6_s7_edge_cost']) for r in rem_parent)
assert min_cost == 63 and any(
    r['s6_hex'] == j63a['s6_child_hex'] and int(r['s6_s7_edge_cost']) == 63
    for r in rem_parent)
print('CONTROL cost-63a child is the cheapest remaining child (edge cost 63) of its S5: OK')

# ---------- 3. add the cost-63a receipts (one fully verified certificate) ----------
w63a = json.loads((OUT / 'class2-lane-cost63a-win7-certificates-20261114.json').read_text())
certs = [c for c in w63a['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs) == 1 and certs[0]['bit'] == 119
rows_map = {119: 28509}
subs_map = {119: 49}
mob_map = {119: 49}
for c in certs:
    assert c['rows'] == rows_map[c['bit']]
    assert c['sub_roots_pass'] == subs_map[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child | (1 << c['bit'])
print('CONTROL cost-63a receipts verified: OK (bit 119: rows/sub-roots/union asserted)')

per_bits = {}
marg_union = set()
for c in certs:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s31
    marg_m = marg & manifest
    per_bits[c['bit']] = {
        'root_hex': c['root_hex'], 'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union |= marg
s32 = s31 | marg_union
st32, rem32, uniq32, dem32 = summary_state(s32)
print('AFTER cost63a:', json.dumps(st32, indent=1))

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
    'schema': 'n11-class-frontier-cost63a-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost61d-recompute-20261114 (solved 951 / unique remaining 6896 / sum 542952 / open 5166/406675)',
    'method': 'direct extension of recompute_frontier_cost61d_20261114.py: every staged control reproduces the published after-cost-61d frontier exactly (asserted: 951/6896/542952/5166/406675), the completed cost-63a sweep (10 WIN7-D10, 53 REFUTED, 0 capped, 288,069,056 v15 nodes; determinism re-runs node-exact on bits 32/2/119/11, runner_fbs20 cross-engine bit-exact on bits 32/2/119 with fbtDrops=0, env-reset cross-restart reproduction control, batch1 independently audited in flight) is asserted and its fully verified bit-119 receipt (28,509 rows, 49/49 sub-roots PASS, union 0/0, fbt_drops=0) is added; the 9 remaining WIN7-D10 bits stay warm certificate-rebuild candidates and change no frontier number; the parallel cost-61d sweep is in flight at this baseline and not counted',
    'controls': {
        'after_cost61d': {'solved_in_manifest': 951, 'unique_remaining': 6896,
                          'sum_cost': 542952, 'open_s6': 5166, 'open_cost': 406675,
                          'reproduced': True},
        'cost63a_sweep': {'win7_d10': 10, 'capped': 0, 'refuted_d10': 53,
                          'roots_asserted': True, 'engine': 'v15 (repo-verbatim class4_child1_runner.ts)'},
        'cost63a_claim': {'status': 'completed', 'reproduced': True},
        'cost63a_demand': {'c1': 0, 'c2': 2, 'c4': 0, 'reproduced': True},
        'cost63a_receipts': {'rows': rows_map, 'sub_roots_pass': subs_map,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost63a_addition': per_bits,
    'frontier_after_cost63a': {
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
(OUT / 'class-frontier-cost63a-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost63a-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem32.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost63a-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost63a-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem32.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem32.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-63a parent S5 (class-2 target, two receipts so far)',
                         next(c for c in class2 if c['s5_hex'] == '00000000000000809102000000000000'))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem32[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem32[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost63a)')
