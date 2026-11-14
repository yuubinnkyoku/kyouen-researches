#!/usr/bin/env python3
"""Class-2/4 frontier recomputation adding the class2-lane cost-71b sweep
receipts on top of the after-cost-70c frontier (2026-11-15).

Baseline (published main): class-frontier-cost70c-recompute-20261115.json
(solved 1022 / unique remaining 6825 / sum 537921 / open 5095/401644),
itself the runpy extension of recompute_frontier_cost69e_20261115.py (1019)
on the merged 1012 state.

This script:
1. reproduces the after-cost-70c baseline by runpy (asserting
   1022/6825/537921/5095/401644);
2. re-derives the cost-71b child's remaining membership with string keys
   (the child was claimed at this state as the cheapest remaining unswept
   child of the second class-2 target, parent at 6 orbits / 443, and -
   unlike the cost-69e and cost-70c mid-flight closures - it was genuinely
   still remaining when swept);
3. asserts the completed cost-71b sweep (71 candidates: 9 WIN7-D10 + 62
   REFUTED, 0 capped, 87,586,636 v16 nodes; all 9 raw batches re-summed
   from the published JSONL; the v16 determinism rerun bits 32/113 and the
   v15 cross-engine anchors on all 9 WIN7 bits asserted from the published
   JSONL);
4. adds the three fully verified cost-71b receipts (bits 109/21/105) in the
   published record order, re-deriving every per-bit marginal from the
   growing union, and produces the after-cost-71b frontier + ranking CSV +
   top-candidates CSV. The bit-21 root 00000000000000803202000000600000 was
   independently warm-rebuilt by the parallel lane as the cost-60b bit-22
   certificate (byte-identical file, md5 0bca8499e98e1a0197db2a6f6bd2d6ab)
   - an unplanned cross-lane reproduction; whichever receipt enters the
   frontier first claims the marginal and the other contributes 0 by
   construction.
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
CHILD = '00000000000000803202000000400000'

# ---------- 2. re-derive the child's remaining membership (string keys) ----------
parent_rows_after70c = rem70.get(PARENT, [])
child_hexes_remaining = {r['s6_hex'] for r in parent_rows_after70c}
assert len(parent_rows_after70c) == 6, 'parent expected at 6 remaining orbits after cost-70c'
child_still_remaining = CHILD in child_hexes_remaining
child_in_solved = int(CHILD, 16) in s70
assert child_still_remaining is True, 'cost-71b child expected to be genuinely remaining at the claim state'
assert child_in_solved is False
membership = {
    'child_hex': CHILD,
    'claimed_as': 'cheapest remaining unswept child of the second class-2 target '
                 '(parent at 6 orbits / 443 after the cost-70c frontier; claim verified from '
                 'class-frontier-top-candidates-s6-after-cost70c-20261115.csv)',
    'still_in_parent_remaining_children_at_claim': True,
    'midflight_manifest_closure': None,
    'note': 'unlike cost-69e and cost-70c, this child was genuinely still remaining when swept '
            '(no mid-flight closure); its own WIN7 receipts may now cover it',
}
print(f'CONTROL child membership re-derived (string keys): still_remaining=True at claim state')

# ---------- 3. assert the completed cost-71b sweep ----------
sweep = json.loads((OUT / 'class2-lane-cost71b-sweep-20261115.json').read_text())
assert sweep['s6_child_hex'] == CHILD
assert sweep['s6_s7_edge_cost'] == 71
assert sweep['win7_d10'] == 9 and sweep['refuted_d10'] == 62 and sweep['capped'] == 0
assert sweep['total_nodes'] == 87586636
assert sweep['win7_bits'] == [1, 14, 21, 32, 74, 94, 105, 109, 117]

tot_nodes = 0
seen_bits = set()
win_from_raw = set()
n_pilot = 0
for i in range(1, 10):
    for line in (OUT / f'class2-lane-cost71b-raw-batch{i}-20261115.jsonl').read_text().splitlines():
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
assert n_pilot == 9 and len(seen_bits) == 71 and tot_nodes == 87586636
assert win_from_raw == {1, 14, 21, 32, 74, 94, 105, 109, 117}
print('CONTROL cost-71b sweep asserted from published raw batches: '
      '71 candidates, 9 pilots, 9 WIN7 + 62 REFUTED, 87,586,636 nodes')

det = [json.loads(l) for l in (OUT / 'class2-lane-cost71b-v16-determinism-rerun-20261115.jsonl')
       .read_text().splitlines() if l.strip()]
det_bits = {r['bit']: r for r in det if 'bit' in r}
assert det_bits[32]['nodes'] == 8488319 and det_bits[32]['loss'] is True
assert det_bits[113]['nodes'] == 9070237 and det_bits[113]['loss'] is False

v15 = [json.loads(l) for l in (OUT / 'class2-lane-cost71b-v15-crosscheck-20261115.jsonl')
       .read_text().splitlines() if l.strip()]
v15_pilot = [r for r in v15 if 'control' in r]
assert len(v15_pilot) == 2 and all(r['loss'] is False and r['nodes'] == 5949 for r in v15_pilot)
v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
v15_expect = {109: 2323226, 105: 3864960, 21: 2576152, 1: 4375357, 117: 7210014,
              74: 6756758, 94: 5520204, 14: 14083030, 32: 18454344}
assert set(v15_bits) == set(v15_expect)
for b, n in v15_expect.items():
    assert v15_bits[b]['loss'] is True and v15_bits[b]['nodes'] == n, (b, v15_bits[b]['nodes'])
print('CONTROL determinism rerun (32/113 node-exact) and v15 anchors '
      '(all 9 WIN7 bits loss=true) asserted')

# ---------- 4. the three verified receipts, marginals from the growing union ----------
certs_rec = json.loads((OUT / 'class2-lane-cost71b-win7-certificates-20261115.json').read_text())
assert certs_rec['child_hex'] == CHILD
certs = [c for c in certs_rec['certificates'] if c.get('verdict') == 'WIN7']
assert [c['bit'] for c in certs] == [109, 21, 105]
ROWS = {109: 32492, 21: 29242, 105: 38589}
SUBS = {109: 51, 21: 52, 105: 54}
MD5 = {109: '513b87f7b8edc6d1ebcb25c725d79789',
       21: '0bca8499e98e1a0197db2a6f6bd2d6ab',
       105: '7243ac5da980fbd8899fd5d93735e5ab'}
child_v = int(CHILD, 16)
group_covers = {}
for c in certs:
    assert c['rows'] == ROWS[c['bit']] and c['sub_roots_pass'] == SUBS[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['md5'] == MD5[c['bit']]
    assert int(c['root_hex'], 16) == child_v | (1 << c['bit'])
    group_covers[c['bit']] = covers(int(c['root_hex'], 16))
print('CONTROL cost-71b receipts asserted: bits 109/21/105 (rows/sub-roots/union/md5/roots)')

s_cur = set(s70)
cost71b_addition = {}
for bit in (109, 21, 105):
    cov = group_covers[bit]
    marg = cov - s_cur
    marg_m = marg & manifest
    cost71b_addition[str(bit)] = {
        'root_hex': format(child_v | (1 << bit), '032x'),
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    s_cur |= marg
st71, rem71, uniq71, dem71 = summary_state(s_cur)
assert s_cur >= s70, 'the after-cost-71b solved set must extend the after-70c baseline'
print('AFTER cost-71b:', json.dumps(st71, indent=1))

# child closure check after the additions
child_closed_now = int(CHILD, 16) in s_cur
print(f'cost-71b child in solved set after additions: {child_closed_now}')
membership['child_closed_by_own_receipts'] = child_closed_now
if child_closed_now:
    covering_bits = [b for b in (109, 21, 105) if int(CHILD, 16) in group_covers[b]]
    membership['child_covered_by_receipt_bits'] = covering_bits

# ---------- 5. new ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem71, 2)
class4 = best(rem71, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-cost71b-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-cost70c-recompute-20261115 (solved 1022 / unique remaining 6825 / sum 537921 / open 5095/401644)',
    'method': 'direct runpy extension of recompute_frontier_cost70c_20261115.py: the after-cost-70c baseline is reproduced exactly '
              '(asserted 1022/6825/537921/5095/401644), the cost-71b child remaining-membership is re-derived with string keys '
              '(the child was genuinely still remaining at the claim state, unlike the cost-69e/70c mid-flight closures), the '
              'completed cost-71b sweep is asserted from the published raw batches (71 candidates: 9 WIN7-D10 + 62 REFUTED, 0 '
              'capped, 87,586,636 v16 nodes; 9 pilot d6 controls; determinism rerun bits 32/113 node-exact; v15 cross-engine '
              'anchors on all 9 WIN7 bits loss=true at 2,323,226/3,864,960/2,576,152/4,375,357/7,210,014/6,756,758/5,520,204/'
              '14,083,030/18,454,344 nodes), and the three fully verified receipts (bits 109/21/105; rows 32,492/29,242/38,589; '
              'sub-roots 51/52/54 PASS; union 0/0 each; independent BigInt audit) are added in the published record order with '
              'per-bit marginals re-derived from the growing union; the bit-21 root 00000000000000803202000000600000 duplicates '
              'the cost-60b bit-22 win7_roots listing and was independently warm-rebuilt by the parallel lane as the cost-60b '
              'bit-22 certificate with a byte-identical file (md5 0bca8499e98e1a0197db2a6f6bd2d6ab) - an unplanned cross-lane '
              'reproduction; this receipt enters the frontier here and the parallel cost-60b bit-22 rebuild contributes 0 '
              'marginal by construction when it is folded into a later recompute; the bit-1 root 00000000000000803202000000400002 '
              'duplicates the cost-61d bit-22 win7_roots listing with no prior certificate (certified bits 30/74/94 only) - a '
              'warm certificate-rebuild candidate that would close the cost-61d bit-22 warm entry; the remaining WIN7-D10 bits '
              '(1/14/32/74/94/117) stay warm certificate-rebuild candidates and change no frontier number',
    'controls': {
        'after_cost70c_baseline': {'solved_in_manifest': 1022, 'unique_remaining': 6825,
                                   'sum_cost': 537921, 'open_s6': 5095, 'open_cost': 401644,
                                   'reproduced': True},
        'child_membership_reproduced_string_keys': True,
        'sweep_asserted_from_raw_batches': True,
        'extends_after_cost70c_baseline': True,
    },
    'child_membership': membership,
    'cost71b_addition': cost71b_addition,
    'frontier_after_cost71b': {
        'solved_s6_in_manifest': st71['solved_s6_in_manifest'],
        'remaining_s5_orbits': st71['remaining_s5_orbits'],
        'unique_remaining_s6': st71['unique_remaining_s6'],
        'sum_remaining_cost': st71['sum_remaining_cost'],
        's6_needed_by_open_classes': st71['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st71['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st71['hist'],
        'best_class2': class2[0],
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
(OUT / 'class-frontier-cost71b-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost71b-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem71.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost71b-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-cost71b-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('cost-71b parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == PARENT))):
        rows = rem71.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem71[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost71b)')
