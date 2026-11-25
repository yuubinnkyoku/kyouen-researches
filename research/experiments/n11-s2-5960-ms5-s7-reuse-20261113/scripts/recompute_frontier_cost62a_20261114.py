#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published (cost-62a
extension) WIN7 receipts as of main (class2-lane cost-62a session 11, 2026-11-14).

Direct extension of recompute_frontier_cost73a_20261114.py via runpy: after
reproducing every published staged control through after-cost-73a (solved 921 /
unique remaining 6926 / sum 544995 / open 5196/408718), the completed cost-62a
sweep (session 11, cheapest unswept child of the next class-2 target S5 after the
uncoverability audit declared the previous best class-2 S5 receipt-unclosable:
11 WIN7-D10 bits 1,11,32,66,86,89,95,105,109,112,118, 51 REFUTED, 0 capped,
245,781,099 nodes) is asserted, its fully verified bit-11 receipt is added, and the
newly completed sterile class4-lane cost-86a/86b/86c sweeps are asserted
receipt-free. The uncoverability audit (best class-2 S5 00000000000000809082000000000000
permanently blocked) is re-asserted against the new frontier.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-73a frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost73a_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s30 = ns['s30']
st30 = ns['st30']
rem30 = ns['rem30']
assert st30['solved_s6_in_manifest'] == 921 and st30['unique_remaining_s6'] == 6926
assert st30['sum_remaining_cost'] == 544995
assert st30['s6_needed_by_open_classes'] == 5196 and st30['cost_needed_by_open_classes'] == 408718
print('CONTROL after-cost73a published frontier reproduced: OK')

# ---------- 2. assert the completed cost-62a sweep record ----------
j62a = json.loads((OUT / 'class2-lane-cost62a-sweep-20261114.json').read_text())
assert j62a['s6_child_hex'] == '00000000000000809102000001000000'
assert j62a['s6_s7_edge_cost'] == 62 and j62a['capped'] == 0
assert j62a['win7_d10'] == 11 and j62a['refuted_d10'] == 51
assert j62a['total_nodes'] == 245781099
assert j62a['win7_bits'] == [1, 11, 32, 66, 86, 89, 95, 105, 109, 112, 118]
child = int(j62a['s6_child_hex'], 16)
for b in j62a['win7_bits']:
    assert j62a['win7_roots'].index(format(child | (1 << b), '032x')) == \
        j62a['win7_bits'].index(b)
print('CONTROL completed cost-62a sweep record: OK (11 WIN7, 51 REFUTED, 0 capped, roots asserted)')

# the 62 candidate bits are bit-exact with the independent enumeration
claim = json.loads((OUT / 'class2-lane-cost62a-inflight-20261114.json').read_text())
assert claim['legal_candidates_total'] == 62 and claim['status'].startswith('completed')
assert claim['result']['win7_d10'] == 11 and claim['result']['capped'] == 0
print('CONTROL cost-62a claim updated to completed: OK')

# ---------- 3. assert the newly completed sterile class4-lane sweeps (no receipts) ----------
for name, n in (('class4-lane-cost86a-sweep-20261114.json', 86),
                ('class4-lane-cost86b-sweep-20261114.json', 86),
                ('class4-lane-cost86c-sweep-20261114.json', 86)):
    j = json.loads((OUT / name).read_text())
    summ = j.get('summary') or {}
    w = summ.get('win7_d10', j.get('win7_d10'))
    assert w == 0 or w == [], (name, w)
    c = summ.get('capped', j.get('capped'))
    assert c == 0 or c == [], (name, c)
    r = summ.get('refuted_d10', j.get('refuted_d10'))
    assert len(r) == n if isinstance(r, list) else r == n, (name, r)
print('CONTROL sterile sweeps cost-86a / cost-86b / cost-86c (class4): OK')

# ---------- 4. add the cost-62a bit-11 receipt (fully verified certificate) ----------
w62a = json.loads((OUT / 'class2-lane-cost62a-win7-certificates-20261114.json').read_text())
certs = [c for c in w62a['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs) == 1 and certs[0]['bit'] == 11
assert certs[0]['root_hex'] == '00000000000000809102000001000800'
assert certs[0]['rows'] == 24728 and certs[0]['sub_roots_pass'] == 47
assert certs[0]['union_missing'] == 0 and certs[0]['union_extra'] == 0
root62a = int(certs[0]['root_hex'], 16)
cov62a = covers(root62a)
marg62a = cov62a - s30
marg62a_m = marg62a & manifest
per = {'cost62a': {
    'roots': [f'{root62a:032x}'],
    'covers': len(cov62a), 'marginal': len(marg62a),
    'marginal_in_manifest': len(marg62a_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg62a_m),
}}
s31 = s30 | marg62a
st31, rem31, uniq31, dem31 = summary_state(s31)
print('AFTER cost62a:', json.dumps(st31, indent=1))

# ---------- 5. re-assert the uncoverability audit against the new frontier ----------
b2 = '00000000000000809082000000000000'
rows2 = rem31.get(b2, [])
aud = json.loads((OUT / 'class-frontier-uncoverability-audit-20261114.json').read_text())
assert len(rows2) == aud['best_class2']['remaining'] == 10, len(rows2)
assert sum(int(r['s6_s7_edge_cost']) for r in rows2) == aud['best_class2']['unclosable_cost'] == 698
print('CONTROL uncoverability audit still holds (best class-2 S5: 10 remaining, all sterile-swept): OK')

# ---------- 6. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem31, 2)
class4 = best(rem31, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost62a-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost73a-recompute-20261114 (solved 921 / unique remaining 6926 / sum 544995 / open 5196/408718)',
    'method': 'direct extension of recompute_frontier_cost73a_20261114.py: every staged control reproduces the published after-cost-73a frontier exactly (asserted: 921/6926/544995/5196/408718), the completed cost-62a sweep (11 WIN7-D10, 51 REFUTED, 0 capped, 245,781,099 nodes; first sweep after the uncoverability audit declared the previous best class-2 S5 receipt-unclosable) is asserted, its fully verified bit-11 receipt (24,728 rows, 47/47 sub-roots PASS, union 0/0) is added, and the newly completed sterile class4-lane cost-86a/86b/86c sweeps are asserted receipt-free',
    'controls': {
        'after_cost73a': {'solved_in_manifest': 921, 'unique_remaining': 6926,
                          'sum_cost': 544995, 'open_s6': 5196, 'open_cost': 408718,
                          'reproduced': True},
        'cost62a_sweep': {'win7_d10': 11, 'capped': 0, 'refuted_d10': 51,
                          'roots_asserted': True},
        'sterile_86a_86b_86c': {'win7_d10': 0, 'capped': 0, 'reproduced': True},
        'uncoverability_audit': {'best_class2_remaining': 10, 'all_sterile': True,
                                 'reproduced': True},
    },
    'cost62a_addition': per['cost62a'],
    'frontier_after_cost62a': {
        'solved_s6_in_manifest': st31['solved_s6_in_manifest'],
        'remaining_s5_orbits': st31['remaining_s5_orbits'],
        'unique_remaining_s6': st31['unique_remaining_s6'],
        'sum_remaining_cost': st31['sum_remaining_cost'],
        's6_needed_by_open_classes': st31['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st31['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st31['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != b2),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost62a-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost62a-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem31.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost62a-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))
with (OUT / 'class-frontier-top-candidates-s6-after-cost62a-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem31.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem31.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem31[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem31[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost62a)')
