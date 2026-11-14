#!/usr/bin/env python3
"""Class-2/4 frontier recomputation adding the class2-lane cost-70c sweep
receipts on top of the after-cost-69e frontier (2026-11-15).

Baseline (published main): class-frontier-cost69e-recompute-20261115.json
(solved 1019 / unique remaining 6828 / sum 538143 / open 5098/401866),
itself the runpy extension of recompute_frontier_merged_after65h65i_
warm_67b68c_20261115.py (merged 1012 state) with the six verified cost-69e
receipts (bits 21/99/87/84/76/90).

This script:
1. reproduces the after-cost-69e baseline by runpy (asserting
   1019/6828/538143/5098/401866);
2. re-derives the cost-70c child's remaining membership with STRING keys
   (the published after-cost-69e top-candidates CSV was generated with
   integer lookups against the string-keyed remaining map, so its data
   sections came out empty and its audit-blocked line showed remaining=0
   instead of 10/698; the cost-69e script's own child-membership control
   was vacuous for the same reason - its conclusion is nonetheless
   correct and is re-verified here with the right key type);
3. asserts the completed cost-70c sweep (70 candidates: 13 WIN7-D10 + 57
   REFUTED, 0 capped, 100,935,666 v16 nodes; all 9 raw batches re-summed
   from the published JSONL; the v16 determinism rerun and the v15
   cross-engine anchors on all 13 WIN7 bits asserted from the published
   JSONL files);
4. adds the three fully verified cost-70c receipts (bits 94/20/23) in the
   published record order, re-deriving every per-bit marginal from the
   growing union, and produces the after-cost-70c frontier + ranking CSV +
   top-candidates CSV (with the corrected string-keyed sections).
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-69e baseline (1019) ----------
ns69 = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost69e_20261115.py'))
s69 = ns69['s_cur']
st69 = ns69['st69']
rem69 = ns69['rem69']
dem69 = ns69['dem69']
covers = ns69['covers']
summary_state = ns69['summary_state']
manifest = ns69['manifest']
classes = ns69['classes']
assert st69['solved_s6_in_manifest'] == 1019 and st69['unique_remaining_s6'] == 6828
assert st69['sum_remaining_cost'] == 538143
assert st69['s6_needed_by_open_classes'] == 5098 and st69['cost_needed_by_open_classes'] == 401866
print('CONTROL after-cost-69e baseline reproduced: 1019/6828/538143/5098/401866')

PARENT = '00000000000000803202000000000000'
CHILD = '00000000000000803242000000000000'

# ---------- 2. re-derive the child's remaining membership (string keys) ----------
parent_rows_after69e = rem69.get(PARENT, [])
child_hexes_remaining = {r['s6_hex'] for r in parent_rows_after69e}
assert len(parent_rows_after69e) == 6, 'parent expected at 6 remaining orbits after cost-69e'
child_still_remaining = CHILD in child_hexes_remaining
child_in_solved = int(CHILD, 16) in s69
membership = {
    'child_hex': CHILD,
    'claimed_as': 'cheapest remaining unswept child of the second class-2 target '
                 '(7 orbits / 513 after the merged 1012 frontier; claim commit fee1a57b)',
    'still_in_parent_remaining_children_after_69e': child_still_remaining,
    'in_solved_set_after_69e': child_in_solved,
    'midflight_manifest_closure': 'the parallel cost-69e warm bit-76 receipt '
                                  '(root 00000000000010803202000000008000, verified certificate pushed in '
                                  'class2-lane-cost69e-win7-certificates-20261114.json) closed this child in the '
                                  'manifest while this sweep was in flight (cost-69e recompute v2, commit '
                                  '7cec3e7e); the sweep completed on an already-receipt-closed child; its '
                                  'certificates are pure new-coverage additions',
}
assert child_still_remaining is False, 'child expected to be closed in the after-69e manifest'
assert child_in_solved is True, 'child expected to be in the solved set after cost-69e'
print(f'CONTROL child membership re-derived (string keys): still_remaining={child_still_remaining}, '
      f'in_solved={child_in_solved} (mid-flight manifest closure confirmed for real this time)')

# ---------- 3. assert the completed cost-70c sweep ----------
sweep = json.loads((OUT / 'class2-lane-cost70c-sweep-20261115.json').read_text())
assert sweep['s6_child_hex'] == CHILD
assert sweep['s6_s7_edge_cost'] == 70
assert sweep['win7_d10'] == 13 and sweep['refuted_d10'] == 57 and sweep['capped'] == 0
assert sweep['total_nodes'] == 100935666
assert sweep['win7_bits'] == [3, 8, 11, 20, 23, 24, 40, 42, 86, 92, 94, 103, 105]

# re-sum the published raw batches
tot_nodes = 0
seen_bits = set()
win_from_raw = set()
n_pilot = 0
for i in range(1, 10):
    for line in (OUT / f'class2-lane-cost70c-raw-batch{i}-20261115.jsonl').read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if 'control' in row:
            assert row['loss'] is False and row['nodes'] == 3402 and not row['capped']
            n_pilot += 1
            continue
        assert row['capped'] is False
        assert row['terminalStoneRange'] == [13, 17]
        assert row['bit'] not in seen_bits
        seen_bits.add(row['bit'])
        tot_nodes += row['nodes']
        if row['loss']:
            win_from_raw.add(row['bit'])
assert n_pilot == 9 and len(seen_bits) == 70 and tot_nodes == 100935666
assert win_from_raw == {3, 8, 11, 20, 23, 24, 40, 42, 86, 92, 94, 103, 105}
print('CONTROL cost-70c sweep asserted from published raw batches: '
      '70 candidates, 9 pilots, 13 WIN7 + 57 REFUTED, 100,935,666 nodes')

# determinism rerun control
det = [json.loads(l) for l in (OUT / 'class2-lane-cost70c-v16-determinism-rerun-20261115.jsonl')
       .read_text().splitlines() if l.strip()]
det_bits = {r['bit']: r for r in det if 'bit' in r}
assert det_bits[86]['nodes'] == 6414891 and det_bits[86]['loss'] is True
assert det_bits[66]['nodes'] == 8291296 and det_bits[66]['loss'] is False

# v15 cross-engine anchors control (all 13 WIN7 bits)
v15 = [json.loads(l) for l in (OUT / 'class2-lane-cost70c-v15-crosscheck-20261115.jsonl')
       .read_text().splitlines() if l.strip()]
v15_pilot = [r for r in v15 if 'control' in r]
assert len(v15_pilot) == 2 and all(r['loss'] is False and r['nodes'] == 5949 for r in v15_pilot)
v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
v15_expect = {94: 1013979, 20: 2508065, 23: 2093938, 40: 2398259, 11: 3661352,
               105: 3649378, 24: 4853985, 92: 6634458, 103: 7921123, 42: 7805543,
               8: 8467137, 3: 8568846, 86: 17475934}
assert set(v15_bits) == set(v15_expect)
for b, n in v15_expect.items():
    assert v15_bits[b]['loss'] is True and v15_bits[b]['nodes'] == n, (b, v15_bits[b]['nodes'])
print('CONTROL determinism rerun (86/66 node-exact) and v15 anchors '
      '(all 13 WIN7 bits loss=true) asserted')

# ---------- 4. the three verified receipts, marginals from the growing union ----------
certs_rec = json.loads((OUT / 'class2-lane-cost70c-win7-certificates-20261115.json').read_text())
assert certs_rec['child_hex'] == CHILD
certs = [c for c in certs_rec['certificates'] if c.get('verdict') == 'WIN7']
assert [c['bit'] for c in certs] == [94, 20, 23]
ROWS = {94: 20527, 20: 32576, 23: 33954}
SUBS = {94: 46, 20: 52, 23: 54}
MD5 = {94: 'c5d3232b9c9acd5e788b72b8e4d10c34',
       20: '4365967e4fc10d7643b7707296398096',
       23: '84c0d9ee69aa372b2c6bb349fd431e3b'}
child_v = int(CHILD, 16)
group_covers = {}
for c in certs:
    assert c['rows'] == ROWS[c['bit']] and c['sub_roots_pass'] == SUBS[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['md5'] == MD5[c['bit']]
    assert int(c['root_hex'], 16) == child_v | (1 << c['bit'])
    group_covers[c['bit']] = covers(int(c['root_hex'], 16))
print('CONTROL cost-70c receipts asserted: bits 94/20/23 (rows/sub-roots/union/md5/roots)')

s_cur = set(s69)
cost70c_addition = {}
for bit in (94, 20, 23):
    cov = group_covers[bit]
    marg = cov - s_cur
    marg_m = marg & manifest
    cost70c_addition[str(bit)] = {
        'root_hex': format(child_v | (1 << bit), '032x'),
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    s_cur |= marg
st70, rem70, uniq70, dem70 = summary_state(s_cur)
assert s_cur >= s69, 'the after-cost-70c solved set must extend the after-69e baseline'
print('AFTER cost-70c:', json.dumps(st70, indent=1))

# ---------- 5. new ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem70, 2)
class4 = best(rem70, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-cost70c-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-cost69e-recompute-20261115 (solved 1019 / unique remaining 6828 / sum 538143 / open 5098/401866)',
    'method': 'direct runpy extension of recompute_frontier_cost69e_20261115.py: the after-cost-69e baseline is reproduced exactly '
              '(asserted 1019/6828/538143/5098/401866), the cost-70c child remaining-membership is re-derived with STRING keys '
              '(the published after-cost-69e top-candidates CSV was generated with integer lookups against the string-keyed '
              'remaining map, so all four of its data sections came out empty and its audit-blocked line showed remaining=0 '
              'instead of the real 10/698; the cost-69e script child-membership control was vacuous for the same reason - its '
              'conclusion is nonetheless correct and is re-verified here), the mid-flight manifest closure is documented (the '
              'parallel cost-69e warm bit-76 receipt closed this child while the sweep was in flight), the completed cost-70c '
              'sweep is asserted from the published raw batches (70 candidates: 13 WIN7-D10 + 57 REFUTED, 0 capped, '
              '100,935,666 v16 nodes; 9 pilot d6 controls; determinism rerun bits 86/66 node-exact; v15 cross-engine anchors '
              'on all 13 WIN7 bits loss=true at 1,013,979/2,508,065/2,093,938/2,398,259/3,661,352/3,649,378/4,853,985/'
              '6,634,458/7,921,123/7,805,543/8,467,137/8,568,846/17,475,934 nodes), and the three fully verified receipts '
              '(bits 94/20/23; rows 20,527/32,576/33,954; sub-roots 46/52/54 PASS; union 0/0 each) are added in the published '
              'record order with per-bit marginals re-derived from the growing union; the bit-20 WIN7 root '
              '00000000000000803242000000100000 is a cross-child duplicate of the cost-64b bit-54 win7_roots listing with no '
              'prior published certificate (cost-64b certified bits 73/7/99 only), so that receipt is new coverage and also '
              'closes the cost-64b bit-54 warm entry; the remaining WIN7-D10 bits (3/8/11/24/40/42/86/92/103/105) stay warm '
              'certificate-rebuild candidates and change no frontier number',
    'controls': {
        'after_cost69e_baseline': {'solved_in_manifest': 1019, 'unique_remaining': 6828,
                                   'sum_cost': 538143, 'open_s6': 5098, 'open_cost': 401866,
                                   'reproduced': True},
        'child_membership_reproduced_string_keys': True,
        'sweep_asserted_from_raw_batches': True,
        'extends_after_cost69e_baseline': True,
        'after_cost69e_top_candidates_csv_defect': 'class-frontier-top-candidates-s6-after-cost69e-20261115.csv '
                                                   'was generated with rem69[int(...)] lookups against a string-keyed '
                                                   'defaultdict, so every data section is empty and the audit-blocked '
                                                   'line reads remaining=0 cost=0 (real values 10/698); superseded by '
                                                   'class-frontier-top-candidates-s6-after-cost70c-20261115.csv',
    },
    'child_membership': membership,
    'cost70c_addition': cost70c_addition,
    'frontier_after_cost70c': {
        'solved_s6_in_manifest': st70['solved_s6_in_manifest'],
        'remaining_s5_orbits': st70['remaining_s5_orbits'],
        'unique_remaining_s6': st70['unique_remaining_s6'],
        'sum_remaining_cost': st70['sum_remaining_cost'],
        's6_needed_by_open_classes': st70['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st70['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st70['hist'],
        'best_class2': class2[0],
        'best_class2_note': ('receipt-unclosable per class-frontier-uncoverability-audit-20261114.json '
                             '(all remaining children sterile-swept); shown for reference only'
                             if class2[0]['s5_hex'] == AUDIT_BLOCKED else
                             'remaining children checked against published sweep records in the session log '
                             '(see research/log/2026-11-15-n11-class2-lane-cost70c-sweep.md)'),
        'audit_blocked_class2': next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of '
                            'WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; '
                            '11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost70c-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost70c-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem70.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost70c-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-cost70c-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('cost-70c parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == PARENT))):
        rows = rem70.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem70[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost70c, string-keyed sections fixed)')
