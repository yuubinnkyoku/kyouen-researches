#!/usr/bin/env python3
"""Class-2/4 frontier unified merge: fold all 50 reconciled receipts
(13 cost-68d-lane + 31 warm multiband 2 + 6 cost-70c warm batch-2) on top of
the common 1109 after-warm-multiband baseline, per the published unified fold
reconciliation (class2-lane-unified-fold-reconciliation-20261115.json).

The 1109 baseline had three divergent receipt groups:
- the cost-68d lane fold (class-frontier-cost68d-recompute-20261115.json,
  solved 1117): 7 cost-68d WIN7 receipts + 6 warm band hygiene receipts;
- the warm multiband 2 fold (class-frontier-warm-multiband2-recompute-20261115.json,
  solved 1140): 31 WIN7 receipts;
- the cost-70c warm batch-2 receipts (6 WIN7, certificates under
  class2-lane-cost70c-certificates/, documented in the reconciliation JSON,
  folded in neither head).

This script is the authoritative unified fold specified by the reconciliation:
1. reproduces the 1109 baseline and the 1117 endpoint byte-identically by
   runpy of recompute_frontier_cost68d_20261115.py (asserting
   1109/6738/531295/5008/395018 and 1117/6730/530739/5000/394462);
2. reproduces the 1140 endpoint byte-identically by runpy of
   recompute_frontier_warm_multiband2_20261115.py (asserting
   1140/6707/528979/4977/392702);
3. asserts the three-way root disjointness of the 50 receipts (12 distinct
   roots in the 13-receipt group because cost-71b bit-1 == cost-61d bit-22
   share one root; 31 multiband2 roots; 6 cost-70c roots) and the root
   identity root == child | 1<<bit for the 6 cost-70c receipts;
4. independently re-derives each group's marginal-in-manifest union versus the
   1109 baseline and asserts it equals the reconciliation's published hex
   lists, with pairwise intersections empty and union size 45;
5. folds the 50 receipts from the 1109 baseline in the reconciliation's fold
   order (13 in published order, then 31 in published order, then the 6
   cost-70c in greedy order 105, 92, 40, 24, 11, 8), re-deriving every
   per-record marginal from the growing union;
6. set-equality controls: after the first 13 receipts the solved set equals
   the 1117 endpoint; after 44 it equals s_1117 UNION s_1140 with the
   published merged-head numbers 1148/6699/528423/4969/392146; after all 50
   it equals s_1117 UNION s_1140 UNION covers(6 cost-70c receipts);
7. asserts the expected unified solved-in-manifest 1154 (the reconciliation's
   set-union prediction) and produces the unified-merge frontier + ranking
   CSV + top-candidates CSV.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the 1109 baseline + the 1117 endpoint (cost-68d lane) ----------
ns68 = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost68d_20261115.py'))
s_1109 = ns68['sW']
st_1109 = ns68['stW']
certs68 = ns68['certs']
hyg = ns68['hyg']
covers = ns68['covers']
manifest = ns68['manifest']
classes = ns68['classes']
summary_state = ns68['summary_state']
s_1117 = ns68['s_cur']
st_1117 = ns68['stX']
assert st_1109['solved_s6_in_manifest'] == 1109 and st_1109['unique_remaining_s6'] == 6738
assert st_1109['sum_remaining_cost'] == 531295
assert st_1109['s6_needed_by_open_classes'] == 5008 and st_1109['cost_needed_by_open_classes'] == 395018
assert st_1117['solved_s6_in_manifest'] == 1117 and st_1117['unique_remaining_s6'] == 6730
assert st_1117['sum_remaining_cost'] == 530739
assert st_1117['s6_needed_by_open_classes'] == 5000 and st_1117['cost_needed_by_open_classes'] == 394462
assert len(certs68) == 7 and len(hyg) == 6
print('CONTROL 1109 baseline and 1117 endpoint reproduced byte-identically: '
      '1109/6738/531295/5008/395018 -> 1117/6730/530739/5000/394462')

# ---------- 2. reproduce the 1140 endpoint (warm multiband 2 lane) ----------
nsM2 = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_warm_multiband2_20261115.py'))
s_1140 = nsM2['s_cur']
st_1140 = nsM2['stW2']
records31 = nsM2['records']
assert st_1140['solved_s6_in_manifest'] == 1140 and st_1140['unique_remaining_s6'] == 6707
assert st_1140['sum_remaining_cost'] == 528979
assert st_1140['s6_needed_by_open_classes'] == 4977 and st_1140['cost_needed_by_open_classes'] == 392702
assert s_1109 == set(nsM2['sH']), 'both lanes must extend the same 1109 baseline set'
assert len(records31) == 31
print('CONTROL 1140 endpoint reproduced byte-identically: '
      '1140/6707/528979/4977/392702 (common 1109 baseline set confirmed)')

# ---------- 3. the 6 cost-70c warm batch-2 receipts from the reconciliation ----------
recon = json.loads((OUT / 'class2-lane-unified-fold-reconciliation-20261115.json').read_text())
assert recon['schema'] == 'n11-class2-lane-unified-fold-reconciliation-20261115-v1'
recs70c = recon['cost70c_warm_batch2_receipts']
assert len(recs70c) == 6
CHILD70C = '00000000000000803242000000000000'
child70c_v = int(CHILD70C, 16)
for r in recs70c:
    assert r['band'] == 'class2-lane-cost70c' and r['verdict'] == 'WIN7'
    assert int(r['root_hex'], 16) == child70c_v | (1 << r['bit']), r
    assert r['rows'] > 0 and r['sub_roots_pass'] > 0 and len(r['md5']) == 32
    assert r['marginal_in_manifest_vs_1109'] == 1 and len(r['marginal_manifest_hex']) == 32
cc = recon['cost70c_consistency']
assert set(cc['certified_now']) == {94, 20, 23, 105, 92, 40, 24, 11, 8}
assert cc['remaining_uncertified_win7_bits'] == [3, 42, 86, 103]
ORDER6 = [105, 92, 40, 24, 11, 8]
recs6 = sorted(recs70c, key=lambda r: ORDER6.index(r['bit']))
assert [r['bit'] for r in recs6] == ORDER6
print('CONTROL 6 cost-70c warm batch-2 receipts asserted against the '
      'reconciliation (root identity, rows, md5, greedy order 105/92/40/24/11/8)')

# ---------- 4. three-way root disjointness + reconciliation arithmetic ----------
roots13 = {r['root_hex'] for r in list(certs68) + list(hyg)}
roots31 = {r['root_hex'] for r in records31}
roots6 = {r['root_hex'] for r in recs70c}
assert len(roots13) == 12, 'the 13-receipt group has 12 distinct roots (71b-1 == 61d-22)'
assert not (roots13 & roots31) and not (roots13 & roots6) and not (roots31 & roots6), \
    'the three receipt groups must be root-disjoint'

def group_marg_manifest(records):
    u = set()
    for r in records:
        u |= (covers(int(r['root_hex'], 16)) & manifest) - s_1109
    return u

mu = recon['marginal_union_arithmetic']
g13 = group_marg_manifest(list(certs68) + list(hyg))
g31 = group_marg_manifest(records31)
g6 = group_marg_manifest(recs6)
assert g13 == {int(h, 16) for h in mu['cost68d_in_manifest_hexes']}
assert g31 == {int(h, 16) for h in mu['warm_multiband2_in_manifest_hexes']}
assert g6 == {int(h, 16) for h in mu['cost70c_warm_batch2_in_manifest_hexes']}
assert not (g13 & g31) and not (g13 & g6) and not (g31 & g6)
assert len(g13 | g31 | g6) == 45 and mu['union_size'] == 45
print('CONTROL reconciliation marginal arithmetic independently re-derived: '
      f'|g13|={len(g13)} |g31|={len(g31)} |g6|={len(g6)} union=45, pairwise empty')

# ---------- 5. fold the 50 receipts from the 1109 baseline ----------
s_cur = set(s_1109)
addition = []

def fold(r, band_default):
    global s_cur
    cov = covers(int(r['root_hex'], 16))
    marg = cov - s_cur
    marg_m = marg & manifest
    addition.append({
        'band': r.get('band', band_default), 'bit': r['bit'], 'root_hex': r['root_hex'],
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    })
    s_cur |= marg

for r in list(certs68) + list(hyg):
    fold(r, 'class2-lane-cost68d')
assert s_cur == set(s_1117), 'folding the 13 receipts must reproduce the 1117 endpoint set'
st_mid = summary_state(s_cur)[0]
assert st_mid['solved_s6_in_manifest'] == 1117
print('CONTROL set-equality after 13 receipts: == s_1117 (solved 1117)')

for r in records31:
    fold(r, r['band'])
assert s_cur == set(s_1117) | set(s_1140), \
    'set-equality after 44 receipts: s_44 == s_1117 UNION s_1140'
st_mid2, rem_mid2, uniq_mid2, dem_mid2 = summary_state(s_cur)
assert st_mid2['solved_s6_in_manifest'] == 1148
assert st_mid2['unique_remaining_s6'] == 6699
assert st_mid2['sum_remaining_cost'] == 528423
assert st_mid2['s6_needed_by_open_classes'] == 4969
assert st_mid2['cost_needed_by_open_classes'] == 392146
print('CONTROL set-equality after 44 receipts: == s_1117 UNION s_1140 '
      '(matches the published merged head 1148/6699/528423/4969/392146)')

for r in recs6:
    fold(r, 'class2-lane-cost70c')
    a = addition[-1]
    assert int(r['marginal_manifest_hex'], 16) in {int(h, 16) for h in a['marginal_manifest_hexes']}, \
        'the reconciliation per-receipt marginal hex must be marginal at fold time'
cov6 = set()
for r in recs6:
    cov6 |= covers(int(r['root_hex'], 16))
assert s_cur == set(s_1117) | set(s_1140) | cov6, \
    'set-equality after 50 receipts: s_50 == s_1117 UNION s_1140 UNION covers(6 cost-70c)'
stU, remU, uniqU, demU = summary_state(s_cur)
assert stU['solved_s6_in_manifest'] == 1154, \
    'expected unified solved-in-manifest 1154 (the reconciliation prediction)'
assert s_cur >= s_1117 and s_cur >= s_1140
print('UNIFIED MERGE after 50 receipts:', json.dumps(stU, indent=1))

total_mim = sum(a['marginal_in_manifest'] for a in addition)
total_marg = sum(a['marginal'] for a in addition)
zero_mim = [f"{a['band']}-bit{a['bit']}" for a in addition if a['marginal_in_manifest'] == 0]
print(f'total marginal={total_marg} marginal_in_manifest={total_mim}; '
      f'zero-mim receipts: {zero_mim}')

# ---------- 6. new ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(remU, 2)
class4 = best(remU, 4)
print('best class2:', class2[0])
print('best class4:', class4[0])

AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-unified-merge-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-warm-multiband-recompute-20261115.json '
                     '(solved 1109 / unique remaining 6738 / sum 531295 / open '
                     '5008/395018) - the common baseline of all three folds',
    'method': 'authoritative unified fold specified by '
              'class2-lane-unified-fold-reconciliation-20261115.json: the 1109 '
              'baseline, the 1117 endpoint (recompute_frontier_cost68d_20261115.py) '
              'and the 1140 endpoint (recompute_frontier_warm_multiband2_20261115.py) '
              'are reproduced byte-identically by runpy, the 50 receipts (7 cost-68d '
              'WIN7 + 6 hygiene + 31 warm multiband 2 + 6 cost-70c warm batch-2) are '
              'asserted root-disjoint three ways, the reconciliation per-group '
              'marginal-in-manifest unions are independently re-derived from covers '
              'and the manifest and matched against the published hex lists (union 45, '
              'pairwise intersections empty), then all 50 receipts are folded from the '
              '1109 baseline in the reconciliation fold order (13 in published order, '
              '31 in published order, 6 cost-70c in greedy order 105/92/40/24/11/8) '
              'with every per-record marginal re-derived from the growing union. The '
              '6 cost-70c receipts are the warm batch-2 certificates published under '
              'class2-lane-cost70c-certificates/ (bit105 single file, 92/40/24/11/8 '
              'part1of2/part2of2), extracted with the repo-verbatim blind extractor '
              '(FBS=1<<20, fbt_drops=0) and BigInt-independently verified per the '
              'reconciliation; no sweep claims are made here beyond the published '
              'records - receipts only',
    'controls': {
        'baseline_1109_reproduced': {
            'solved_in_manifest': 1109, 'unique_remaining': 6738,
            'sum_cost': 531295, 'open_s6': 5008, 'open_cost': 395018},
        'endpoint_1117_reproduced': {
            'solved_in_manifest': 1117, 'unique_remaining': 6730,
            'sum_cost': 530739, 'open_s6': 5000, 'open_cost': 394462},
        'endpoint_1140_reproduced': {
            'solved_in_manifest': 1140, 'unique_remaining': 6707,
            'sum_cost': 528979, 'open_s6': 4977, 'open_cost': 392702},
        'common_baseline_set': 's_1109 == the multiband2 lane baseline set (asserted)',
        'three_way_root_disjointness': '12 distinct roots (71b bit-1 == 61d bit-22 '
                                       'share one canonical root) + 31 + 6, pairwise '
                                       'intersections empty',
        'reconciliation_arithmetic_rederived': {
            'g13_size': len(g13), 'g31_size': len(g31), 'g6_size': len(g6),
            'union_size': len(g13 | g31 | g6), 'pairwise_intersections_empty': True,
            'matches_published_hex_lists': True},
        'set_equality_after_13': 's == s_1117',
        'set_equality_after_44': 's == s_1117 UNION s_1140 '
                                  '(published merged head 1148/6699/528423/4969/392146)',
        'set_equality_after_50': 's == s_1117 UNION s_1140 UNION covers(6 cost-70c)',
        'expected_solved_1154': True,
        'fold_order': '13 cost-68d-lane receipts in published order (7 WIN7 then 6 '
                      'hygiene), then 31 multiband2 receipts in published order, then '
                      'the 6 cost-70c receipts in greedy order 105/92/40/24/11/8',
    },
    'unified_addition': {
        'cost68d_win7': addition[:7],
        'hygiene': addition[7:13],
        'warm_multiband2': addition[13:44],
        'cost70c_warm_batch2': addition[44:],
    },
    'totals': {
        'receipts': len(addition),
        'total_marginal': total_marg,
        'total_marginal_in_manifest': total_mim,
        'zero_marginal_in_manifest': zero_mim,
        'cost68d_rows': sum(c['rows'] for c in certs68),
        'hygiene_rows': sum(r['rows'] for r in hyg),
        'multiband2_rows': sum(r['rows'] for r in records31),
        'cost70c_rows': sum(r['rows'] for r in recs6),
    },
    'frontier_after_unified_merge': {
        'solved_s6_in_manifest': stU['solved_s6_in_manifest'],
        'remaining_s5_orbits': stU['remaining_s5_orbits'],
        'unique_remaining_s6': stU['unique_remaining_s6'],
        'sum_remaining_cost': stU['sum_remaining_cost'],
        's6_needed_by_open_classes': stU['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stU['cost_needed_by_open_classes'],
        'demand_histogram_open_only': stU['hist'],
        'best_class2': class2[0],
        'audit_blocked_class2': next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'outstanding_not_folded': {
        'cost69f': 'sweep complete on the parallel lane (9 WIN7-D10 bits '
                   '2/20/44/68/69/94/109/118/119, controls published: determinism '
                   'rerun node-exact, v15 crosscheck loss=true 9/9); certificates '
                   'and fold pending with that lane',
        'cost70c_remaining': 'WIN7 bits 3/42/86/103 uncertified (warm rebuild candidates)',
        'parallel_bands': 'cost-65h/67b/68c warm candidates and the in-flight '
                          'cost-65j sweep stay with the parallel lane (in-manifest '
                          'marginals listed in class2-lane-warm-candidate-ranking2-20261115.json)',
    },
    'interpretation_guard': 'bookkeeping over published receipts; solved counts measure '
                            'manifest coverage, not the game-theoretic value of any '
                            'position; REFUTED-D10 sweeps prove only absence of '
                            'WIN7-D10; WIN7 certificates prove a win within depth 10 '
                            'from the individual 7-stone roots only; 11x11 empty root / '
                            'two-stone root {49,60} / S2 {59,60} / class 2 / class 4 '
                            'remain UNKNOWN',
}
(OUT / 'class-frontier-unified-merge-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + '\n')
print('written class-frontier-unified-merge-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remU.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-unified-merge-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-unified-merge-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('second coverable class-2 candidate S5',
                         class2[2] if len(class2) > 2 else class2[1])):
        rows = remU.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = demU[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-unified-merge)')
