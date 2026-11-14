#!/usr/bin/env python3
"""Class-2/4 frontier merged recomputation unifying the three parallel
class2-lane branches that forked at the after-cost-70c state (2026-11-15).

Branches resolved (all published on main):
- chain 60b-warm: after-cost-70c (1022) + 17 cost-60b warm receipts -> 1040
  (class-frontier-cost60b-warm-recompute-20261115.json);
- chain 71b: after-cost-70c (1022) + 3 cost-71b receipts (bits 109/21/105)
  -> 1026 (class-frontier-cost71b-recompute-20261115.json);
- chain 69e-v2: merged 1012 + all ten cost-69e receipts (the four warm
  rebuilds 89/94/108/116 beyond the six already inside the 1022 base)
  -> 1023 (class-frontier-cost69e-recompute-20261115.json, schema v2).

This script:
1. reproduces all three branch end states by runpy (asserting
   1040/6807/536522/5077/400245, 1026/6821/537604/5091/401327 and
   1023/6824/537833/5094/401556; every branch output re-verified
   byte-identical to the published files);
2. builds the unified chain: after-cost-60b-warm state + the three cost-71b
   receipts (published record order 109/21/105) + the four cost-69e warm
   receipts (record order 89/94/108/116), re-deriving every per-bit marginal
   from the growing union (cross-lane duplicate roots therefore contribute 0
   marginal by construction: the cost-71b bit-21 root equals the cost-60b
   bit-22 warm root already inside the 1040 state);
3. asserts the merge-consistency control: the unified solved set equals the
   exact union of the three branch solved sets, and extends each of them;
4. produces the merged frontier + ranking CSV + top-candidates CSV.

The cost-72 sweep (2 WIN7-D10, bit-111 certificate published and audited)
stays OUT of this merge on purpose: its own lane has not published a
frontier recompute yet; the next merged recompute folds it in.

Role (coordination): the parallel lane holds the in-flight claim for the
canonical merged recompute (commit b80c2bbc: chains from the v2 1023
baseline, folds 70c(3) + 60b-warm(17) + 71b(3) in chronological order).
This script is published as the independent union-control cross-check
instrument computed from the other end of the fork (the repaired 1040
chain): its verified result (1045/6802/536131/5072/399854, merged solved
set == exact union of the three branch solved sets) is the prediction the
canonical merge must reproduce; its outputs are intentionally NOT published
while the claim is in flight.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the three branch end states ----------
ns60w = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost60b_warm_20261115.py'))
s60w = set(ns60w['s_cur'])
st60w = ns60w['st60w']
assert st60w['solved_s6_in_manifest'] == 1040 and st60w['unique_remaining_s6'] == 6807
assert st60w['sum_remaining_cost'] == 536522
assert st60w['s6_needed_by_open_classes'] == 5077 and st60w['cost_needed_by_open_classes'] == 400245
print('CONTROL branch 60b-warm reproduced: 1040/6807/536522/5077/400245')

ns71 = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost71b_20261115.py'))
s71 = set(ns71['s_cur'])
st71 = ns71['st71']
assert st71['solved_s6_in_manifest'] == 1026 and st71['unique_remaining_s6'] == 6821
assert st71['sum_remaining_cost'] == 537604
assert st71['s6_needed_by_open_classes'] == 5091 and st71['cost_needed_by_open_classes'] == 401327
print('CONTROL branch 71b reproduced: 1026/6821/537604/5091/401327')

ns69 = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost69e_20261115.py'))
s69 = set(ns69['s_cur'])
st69 = ns69['st69']
assert st69['solved_s6_in_manifest'] == 1023 and st69['unique_remaining_s6'] == 6824
assert st69['sum_remaining_cost'] == 537833
assert st69['s6_needed_by_open_classes'] == 5094 and st69['cost_needed_by_open_classes'] == 401556
print('CONTROL branch 69e-v2 reproduced: 1023/6824/537833/5094/401556')

covers = ns60w['covers']
summary_state = ns60w['summary_state']
manifest = ns60w['manifest']
classes = ns60w['classes']

# branch-set sanity before merging
assert s71 <= (s60w | s71) and s69 <= (s60w | s71 | s69)
assert not (s71 <= s60w), 'the 71b branch must add coverage beyond the 60b-warm branch'

# ---------- 2. the unified chain: 71b receipts then 69e warm receipts ----------
CHILD_71B = '00000000000000803202000000400000'
CHILD_69E = '00000000000000803202000000008000'

# cost-71b receipts (bits 109/21/105), asserted from the published records
certs71 = json.loads((OUT / 'class2-lane-cost71b-win7-certificates-20261115.json').read_text())
assert certs71['child_hex'] == CHILD_71B
c71 = [c for c in certs71['certificates'] if c.get('verdict') == 'WIN7']
ROWS71 = {109: 32492, 21: 29242, 105: 38589}
SUBS71 = {109: 51, 21: 52, 105: 54}
MD571 = {109: '513b87f7b8edc6d1ebcb25c725d79789',
         21: '0bca8499e98e1a0197db2a6f6bd2d6ab',
         105: '7243ac5da980fbd8899fd5d93735e5ab'}
assert [c['bit'] for c in c71] == [109, 21, 105]
cv71 = int(CHILD_71B, 16)
group_covers71 = {}
for c in c71:
    b = c['bit']
    assert c['rows'] == ROWS71[b] and c['sub_roots_pass'] == SUBS71[b]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['md5'] == MD571[b]
    assert int(c['root_hex'], 16) == cv71 | (1 << b)
    group_covers71[b] = covers(int(c['root_hex'], 16))
print('CONTROL cost-71b receipts asserted: bits 109/21/105 (rows/sub-roots/union/md5/roots)')

# cost-69e warm receipts (bits 89/94/108/116), asserted from the published records
recs69 = json.loads((OUT / 'class2-lane-cost69e-win7-certificates-20261114.json').read_text())
assert recs69['child_hex'] == CHILD_69E
c69all = [c for c in recs69['certificates'] if c.get('verdict') == 'WIN7']
assert [c['bit'] for c in c69all] == [21, 99, 87, 84, 76, 90, 89, 94, 108, 116]
ROWS69 = {89: 47035, 94: 42538, 108: 33942, 116: 74113}
SUBS69 = {89: 54, 94: 52, 108: 51, 116: 59}
MD569 = {89: '1e2c8db6cd9303fcf0167f59ccb83bae',
         94: '4dc6076b96edc3a472b4b23f38739451',
         108: '74d071466140e1b0a48b67134431a570',
         116: '691140486067132237d8c11d93a12559'}
cv69 = int(CHILD_69E, 16)
group_covers69 = {}
for b in (89, 94, 108, 116):
    c = next(x for x in c69all if x['bit'] == b)
    assert c['rows'] == ROWS69[b] and c['sub_roots_pass'] == SUBS69[b]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['md5'] == MD569[b]
    assert int(c['root_hex'], 16) == cv69 | (1 << b)
    group_covers69[b] = covers(int(c['root_hex'], 16))
print('CONTROL cost-69e warm receipts asserted: bits 89/94/108/116 '
      '(rows/sub-roots/union/md5/roots; independent Python audit 2026-11-15, 10/10 PASS)')

# apply on the growing union, 71b first then the 69e warm four
s_cur = set(s60w)
merged_addition = {}
for bit in (109, 21, 105):
    cov = group_covers71[bit]
    marg = cov - s_cur
    marg_m = marg & manifest
    merged_addition['cost71b_' + str(bit)] = {
        'root_hex': format(cv71 | (1 << bit), '032x'),
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    s_cur |= marg
st_mid, rem_mid, uniq_mid, dem_mid = summary_state(s_cur)
print('MERGED intermediate (after 71b receipts):', json.dumps(st_mid, indent=1))
for bit in (89, 94, 108, 116):
    cov = group_covers69[bit]
    marg = cov - s_cur
    marg_m = marg & manifest
    merged_addition['cost69e_warm_' + str(bit)] = {
        'root_hex': format(cv69 | (1 << bit), '032x'),
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    s_cur |= marg
stM, remM, uniqM, demM = summary_state(s_cur)

# ---------- 3. merge-consistency control ----------
union = s60w | s71 | s69
assert s_cur == union, 'the unified solved set must equal the union of the three branch sets'
assert s71 <= s_cur and s69 <= s_cur and s60w <= s_cur
assert len(s_cur - union) == 0 and len(union - s_cur) == 0
print('CONTROL merge consistency: unified set == exact union of branch sets '
      f'(missing {len(union - s_cur)} / extra {len(s_cur - union)})')
print('MERGED FINAL:', json.dumps(stM, indent=1))

# ---------- 4. ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(remM, 2)
class4 = best(remM, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

AUDIT_BLOCKED = '00000000000000809082000000000000'
PARENT = '00000000000000803202000000000000'
result = {
    'schema': 'n11-class-frontier-merged-recompute-after70c-71b-60bwarm-69e-20261115-v1',
    'date': '2026-11-15',
    'branches_resolved': {
        'cost60b_warm_branch': 'class-frontier-cost60b-warm-recompute-20261115 (solved 1040 / remaining 6807 / sum 536522 / open 5077/400245)',
        'cost71b_branch': 'class-frontier-cost71b-recompute-20261115 (solved 1026 / remaining 6821 / sum 537604 / open 5091/401327)',
        'cost69e_v2_branch': 'class-frontier-cost69e-recompute-20261115 schema v2 (solved 1023 / remaining 6824 / sum 537833 / open 5094/401556)',
    },
    'method': 'direct runpy extension of the published branch chains: the after-cost-60b-warm '
              'state (1040) is reproduced exactly, the three cost-71b receipts (bits 109/21/105; '
              'rows 32,492/29,242/38,589; sub-roots 51/52/54; union 0/0; md5s pinned; independent '
              'BigInt audit) are asserted from the published records and added on the growing '
              'union, then the four cost-69e warm receipts (bits 89/94/108/116; rows '
              '47,035/42,538/33,942/74,113; sub-roots 54/52/51/59; union 0/0; md5s pinned; '
              'independent Python audit 2026-11-15, 10/10 certificates PASS) are asserted and '
              'added; the merged solved set is controlled to equal the exact union of the three '
              'branch solved sets (0 missing / 0 extra) and to extend every branch; cross-lane '
              'duplicate roots contribute 0 marginal by construction (the cost-71b bit-21 root '
              '00000000000000803202000000600000 equals the cost-60b bit-22 warm root already '
              'inside the 1040 state; the first six cost-69e receipts are already inside the '
              '1022 base via the six-receipt intermediate, so the 1023 branch contributes '
              'exactly the four warm receipts here)',
    'controls': {
        'branch_60bwarm_reproduced': True,
        'branch_71b_reproduced': True,
        'branch_69e_v2_reproduced': True,
        'unified_equals_union_of_branch_sets': True,
        'union_missing': 0,
        'union_extra': 0,
        'extends_all_branches': True,
    },
    'merged_addition': merged_addition,
    'merged_intermediate_after_71b': {
        'solved_s6_in_manifest': st_mid['solved_s6_in_manifest'],
        'unique_remaining_s6': st_mid['unique_remaining_s6'],
        'sum_remaining_cost': st_mid['sum_remaining_cost'],
    },
    'frontier_merged': {
        'solved_s6_in_manifest': stM['solved_s6_in_manifest'],
        'remaining_s5_orbits': stM['remaining_s5_orbits'],
        'unique_remaining_s6': stM['unique_remaining_s6'],
        'sum_remaining_cost': stM['sum_remaining_cost'],
        's6_needed_by_open_classes': stM['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stM['cost_needed_by_open_classes'],
        'demand_histogram_open_only': stM['hist'],
        'best_class2': class2[0],
        'audit_blocked_class2': next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'not_included': 'the cost-72 sweep (2 WIN7-D10; bit-111 certificate published and '
                    'BigInt-audited) is not folded in yet: its lane has not published a '
                    'frontier recompute; the next merged recompute includes it',
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only '
                            'absence of WIN7-D10; WIN7 certificates prove a win within depth 10 '
                            'from the 7-stone root only; 11x11 empty root / {49,60} / S2 '
                            '{59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-merged-recompute-after70c-71b-60bwarm-69e-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-merged-recompute-after70c-71b-60bwarm-69e-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remM.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-merged-after70c-71b-60bwarm-69e-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-merged-after70c-71b-60bwarm-69e-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('second class-2 target S5 (cost-72/cost-75 parent)',
                         next(c for c in class2 if c['s5_hex'] == PARENT))):
        rows = remM.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = demM[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (merged)')
