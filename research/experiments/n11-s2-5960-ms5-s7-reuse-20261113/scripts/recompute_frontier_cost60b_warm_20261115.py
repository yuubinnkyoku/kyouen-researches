#!/usr/bin/env python3
"""Class-2/4 frontier recomputation adding the class2-lane cost-60b warm
certificate receipts on top of the after-cost-70c frontier (2026-11-15).

Baseline (published main): class-frontier-cost70c-recompute-20261115.json
(solved 1022 / unique remaining 6825 / sum 537921 / open 5095/401644), itself
the runpy extension of recompute_frontier_cost69e_20261115.py (1019 state)
with the three verified cost-70c receipts (bits 94/20/23).

This script:
1. reproduces the after-cost-70c baseline by runpy (asserting
   1022/6825/537921/5095/401644);
2. re-derives the cost-60b child's solved/remaining status with STRING keys
   (the child 00000000000000803202000000200000 was swept by the original
   cost-60b sweep, its 6 original receipts are in the manifest since the
   after-cost-60b recompute, and the cross-child duplicate certificates of
   bits 15 (cost-69e bit-21) and 34 (cost-68c bit-21) were already added by
   those bands' recomputes - none of them is re-added here);
3. asserts the published cost-60b sweep record's unverified_win7_bits
   (19 bits) and the new warm record's 17 certificates (bits 40/77/26/74/44/
   28/8/88/95/106/87/22/100/108/32/114/43; rows/sub-roots/union/md5/roots);
4. adds the 17 verified warm receipts in the warm record order, re-deriving
   every per-bit marginal from the growing union, and produces the
   after-cost-60b-warm frontier + ranking CSV + top-candidates CSV;
5. the parallel cost-69e warm receipts (bits 89/94/108/116, records updated
   on main) are NOT part of this chain yet - they stay warm candidates for
   the next merged recompute (the two lanes forked at the after-cost-70c
   state; the established merged-recompute pattern will unify them).
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-70c baseline (1022) ----------
ns70 = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost70c_20261115.py'))
s70 = ns70['s_cur']
st70 = ns70['st70']
rem70 = ns70['rem70']
dem70 = ns70['dem70']
covers = ns70['covers']
summary_state = ns70['summary_state']
manifest = ns70['manifest']
classes = ns70['classes']
assert st70['solved_s6_in_manifest'] == 1022 and st70['unique_remaining_s6'] == 6825
assert st70['sum_remaining_cost'] == 537921
assert st70['s6_needed_by_open_classes'] == 5095 and st70['cost_needed_by_open_classes'] == 401644
print('CONTROL after-cost-70c baseline reproduced: 1022/6825/537921/5095/401644')

PARENT = '00000000000000803202000000000000'
CHILD = '00000000000000803202000000200000'

# ---------- 2. re-derive the cost-60b child's solved/remaining status ----------
parent_rows_after70c = rem70.get(PARENT, [])
child_hexes_remaining = {r['s6_hex'] for r in parent_rows_after70c}
child_still_remaining = CHILD in child_hexes_remaining
child_in_solved = int(CHILD, 16) in s70
membership = {
    'child_hex': CHILD,
    'status': 'swept child of the second class-2 target; its 6 original receipts '
              '(bits 117/96/94/105/73/23) have been in the manifest since the '
              'after-cost-60b recompute; the cross-child duplicate roots of bits 15 '
              '(cost-69e bit-21) and 34 (cost-68c bit-21) were already added by those '
              "bands' recomputes and are NOT re-added here (no double counting)",
    'still_in_parent_remaining_children_after_cost70c': child_still_remaining,
    'in_solved_manifest_after_cost70c': child_in_solved,
}
assert child_in_solved is True, 'cost-60b child expected solved in the after-70c manifest'
assert child_still_remaining is False
print(f'CONTROL cost-60b child status re-derived: in_solved={child_in_solved} '
      f'still_remaining={child_still_remaining}')

# ---------- 3. assert the sweep record and the warm record ----------
sweep = json.loads((OUT / 'class2-lane-cost60b-sweep-20261114.json').read_text())
assert sweep['s6_child_hex'] == CHILD
assert sweep['win7_d10'] == 25 and sweep['refuted_d10'] == 35 and sweep['capped'] == 0
assert sweep['win7_bits'] == [8, 15, 22, 23, 26, 28, 32, 34, 40, 43, 44, 73, 74, 77, 87, 88,
                              94, 95, 96, 100, 105, 106, 108, 114, 117]
assert sweep['unverified_win7_bits'] == [8, 15, 22, 26, 28, 32, 34, 40, 43, 44, 74, 77, 87,
                                         88, 95, 100, 106, 108, 114]

warm = json.loads((OUT / 'class2-lane-cost60b-warm-certificates-20261115.json').read_text())
assert warm['child_hex'] == CHILD
assert [d['bit'] for d in warm['duplicate_cross_child_entries']] == [15, 34]
certs = [c for c in warm['certificates'] if c.get('verdict') == 'WIN7']
WARM_ORDER = [40, 77, 26, 74, 44, 28, 8, 88, 95, 106, 87, 22, 100, 108, 32, 114, 43]
assert [c['bit'] for c in certs] == WARM_ORDER
ROWS = {40: 21115, 77: 24881, 26: 23978, 74: 26957, 44: 28432, 28: 17776, 8: 25431,
        88: 33554, 95: 27875, 106: 28496, 87: 30672, 22: 29242, 100: 27369, 108: 29454,
        32: 41391, 114: 35351, 43: 36424}
SUBS = {40: 44, 77: 48, 26: 51, 74: 48, 44: 51, 28: 42, 8: 48, 88: 51, 95: 47, 106: 51,
        87: 51, 22: 52, 100: 50, 108: 50, 32: 54, 114: 54, 43: 51}
MD5 = {40: '56b950b9b51f8608fb136ee2df526b06', 77: '46512a5d30cb31079f95b4547d3a6a36',
       26: 'e3fd1dd2667da65644c392b7100483fb', 74: 'ca2b07c7db11de35f7ea80d184b0b2b3',
       44: '84c22e9e7f7597cb50b08467f41651ab', 28: '4a028a955cf1f037eac3355ebbdd61ce',
       8: '5ada7ba5b639eadef4790f088afb9a7e', 88: 'cc01c0c72a66811222ffd3639939a55f',
       95: '10ba4b046fc26e2d07195f190337c8e3', 106: '140f28ab429970b7f993344adf914646',
       87: '7e198eea86b9c03d71893e8a17345c99', 22: '0bca8499e98e1a0197db2a6f6bd2d6ab',
       100: 'a53826ed8448b68ee38a0c64c93318c4', 108: '6914fa1ec2f6709bf0a59cce1a2fd3e8',
       32: 'b8c5e9cbae8d935c9c4c1bc950f7a9da', 114: 'a6ca671ae1db518a2238bf85196f8b0d',
       43: 'f2590a956c4a976d686de3e63008b3e2'}
EXN = {40: 1510483, 77: 2381950, 26: 2458043, 74: 1953702, 44: 2505216, 28: 3494345,
       8: 2727531, 88: 3072584, 95: 8535755, 106: 4269102, 87: 4109578, 22: 4454710,
       100: 4377221, 108: 5242890, 32: 5524659, 114: 6292430, 43: 7640986}
child_v = int(CHILD, 16)
group_covers = {}
for c in certs:
    b = c['bit']
    assert c['rows'] == ROWS[b] and c['sub_roots_pass'] == SUBS[b]
    assert c['extraction_nodes'] == EXN[b]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['md5'] == MD5[b]
    assert int(c['root_hex'], 16) == child_v | (1 << b)
    group_covers[b] = covers(int(c['root_hex'], 16))
print('CONTROL cost-60b warm receipts asserted: 17 certificates '
      '(rows/sub-roots/union/md5/extraction-nodes/roots)')

# ---------- 4. add the 17 warm receipts, marginals from the growing union ----------
s_cur = set(s70)
cost60b_warm_addition = {}
for b in WARM_ORDER:
    cov = group_covers[b]
    marg = cov - s_cur
    marg_m = marg & manifest
    cost60b_warm_addition[str(b)] = {
        'root_hex': format(child_v | (1 << b), '032x'),
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    s_cur |= marg
st60w, rem60w, uniq60w, dem60w = summary_state(s_cur)
assert s_cur >= s70, 'the after-cost-60b-warm solved set must extend the after-70c baseline'
print('AFTER cost-60b-warm:', json.dumps(st60w, indent=1))

# ---------- 5. new ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem60w, 2)
class4 = best(rem60w, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-cost60b-warm-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-cost70c-recompute-20261115 '
                     '(solved 1022 / unique remaining 6825 / sum 537921 / open 5095/401644)',
    'method': 'direct runpy extension of recompute_frontier_cost70c_20261115.py: the '
              'after-cost-70c baseline is reproduced exactly (asserted '
              '1022/6825/537921/5095/401644), the cost-60b child solved-status is '
              're-derived (swept child, 6 original receipts in the manifest since the '
              'after-cost-60b recompute), the published sweep record unverified bits '
              '(19: 8/15/22/26/28/32/34/40/43/44/74/77/87/88/95/100/106/108/114) and the '
              'new warm record (17 certificates, bits 40/77/26/74/44/28/8/88/95/106/87/22/'
              '100/108/32/114/43; rows 21,115/24,881/23,978/26,957/28,432/17,776/25,431/'
              '33,554/27,875/28,496/30,672/29,242/27,369/29,454/41,391/35,351/36,424; '
              'sub-roots 44/48/51/48/51/42/48/51/47/51/51/52/50/50/54/54/51 PASS; union 0/0 '
              'each; extraction nodes 1,510,483..8,535,755; fbt_drops=0) are asserted, and '
              'the 17 receipts are added in the warm record order with per-bit marginals '
              're-derived from the growing union; the 2 cross-child duplicates (bit 15 = '
              'cost-69e bit-21, bit 34 = cost-68c bit-21) are NOT re-added (already in the '
              'manifest via those bands); the parallel cost-69e warm receipts (bits '
              '89/94/108/116, records updated on main) are NOT part of this chain yet and '
              'stay warm candidates for the next merged recompute (the lanes forked at the '
              'after-cost-70c state)',
    'controls': {
        'after_cost70c_baseline': {'solved_in_manifest': 1022, 'unique_remaining': 6825,
                                   'sum_cost': 537921, 'open_s6': 5095, 'open_cost': 401644,
                                   'reproduced': True},
        'child_solved_status_reproduced_string_keys': True,
        'warm_record_asserted': True,
        'extends_after_cost70c_baseline': True,
    },
    'child_membership': membership,
    'cost60b_warm_addition': cost60b_warm_addition,
    'frontier_after_cost60b_warm': {
        'solved_s6_in_manifest': st60w['solved_s6_in_manifest'],
        'remaining_s5_orbits': st60w['remaining_s5_orbits'],
        'unique_remaining_s6': st60w['unique_remaining_s6'],
        'sum_remaining_cost': st60w['sum_remaining_cost'],
        's6_needed_by_open_classes': st60w['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st60w['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st60w['hist'],
        'best_class2': class2[0],
        'best_class2_note': ('receipt-unclosable per class-frontier-uncoverability-audit-20261114.json '
                             '(all remaining children sterile-swept); shown for reference only'
                             if class2[0]['s5_hex'] == AUDIT_BLOCKED else ''),
        'audit_blocked_class2': next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only '
                            'absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from '
                            'the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / '
                            'class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost60b-warm-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost60b-warm-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem60w.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost60b-warm-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-cost60b-warm-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('cost-60b parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == PARENT))):
        rows = rem60w.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem60w[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost60b-warm)')
