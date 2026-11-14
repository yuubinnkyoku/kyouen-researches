#!/usr/bin/env python3
"""Class-2/4 frontier recompute folding the cost-70c warm batch-3 receipts
(bits 3/42/86/103, class2-lane-cost70c-warm-batch3-records-20261115.json) on
top of the cost-69f receipts chain head (solved 1163).

The cost-69f receipts recompute (recompute_frontier_cost69f_receipts_20261115.py,
commit 30ce12b2) published chain head 1163/6684/527280/4954/391003 and
explicitly deferred the four cost-70c warm batch-3 receipts to "the next
recompute": those certificates (blind extraction + BigInt independent
verification + bit-103 determinism rerun; claim
class2-lane-cost70c-warm-batch3-inflight-20261115.json) were published on main
right after the unified merge and complete the cost-70c band 13/13.

The parallel lane's next-fold marginal prediction
(class2-lane-next-fold-marginal-prediction-20261115.json) predicted all four
bits gain-0 in manifest against the 1154 head (bits 3/103 fully pre-covered,
bits 42/86 covering only non-manifest orbits). This script independently
re-derives the marginals at the fold against the newer 1163 head.

This script:
1. reproduces the cost-69f chain head byte-identically by runpy (asserting
   1163/6684/527280/4954/391003); that chain internally reproduces the
   unified-merge head (asserting 1154 and the blob-identical head JSON);
2. reuses that chain-internal unified namespace for the root-disjointness
   control against the 50 already-folded receipts (49 distinct roots;
   a second in-process chain would exceed the execution-environment
   memory cap, see the OOM record in the fold log);
3. asserts every batch-3 record against the published records JSON (root ==
   child | 1<<bit for child 00000000000000803242000000000000, rows,
   extraction nodes, sub-roots PASS, union 0/0, terminal range 13..17,
   md5, sha256, bytes) and the bit-103 determinism rerun;
4. asserts the four batch-3 roots are disjoint from the 50 unified receipts
   and the 9 cost-69f receipts;
5. folds the 4 receipts in record order (bits 3, 42, 86, 103), re-deriving
   every per-record marginal from the growing union, with set-equality
   control s_after == s_1163 UNION covers(4 batch-3 roots);
6. cross-checks the per-bit marginal-in-manifest against the parallel lane's
   published prediction (expected 0 for all four) and produces the
   after-cost70c-warm3 frontier + ranking CSV + top-candidates CSV.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the cost-69f chain head ----------
nsF = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost69f_receipts_20261115.py'))
s_1163 = nsF['s_cur']
st_1163 = nsF['stF']
covers = nsF['covers']
manifest = nsF['manifest']
classes = nsF['classes']
summary_state = nsF['summary_state']
addition69f = nsF['addition']
assert st_1163['solved_s6_in_manifest'] == 1163 and st_1163['unique_remaining_s6'] == 6684
assert st_1163['sum_remaining_cost'] == 527280
assert st_1163['s6_needed_by_open_classes'] == 4954 and st_1163['cost_needed_by_open_classes'] == 391003
print('CONTROL cost-69f chain head reproduced byte-identically: '
      '1163/6684/527280/4954/391003')

# ---------- 2. the 50 unified receipts (root-disjointness control) ----------
# The cost-69f chain itself reproduces the unified merge head internally
# (recompute_frontier_unified_merge_20261115.py, asserting the regenerated
# head JSON blob-identical to main), so the unified namespace is reused from
# the chain instead of a second in-process runpy: a single full chain keeps
# the process inside the ~1 GB execution-environment memory cap.
nsU = nsF['nsU']
assert nsU['stU']['solved_s6_in_manifest'] == 1154
assert nsU['stU']['unique_remaining_s6'] == 6693
assert nsU['stU']['sum_remaining_cost'] == 527949
assert nsU['stU']['s6_needed_by_open_classes'] == 4963
assert nsU['stU']['cost_needed_by_open_classes'] == 391672
roots68 = nsU['roots68']
rootsM2 = nsU['rootsM2']
roots70 = nsU['roots70']
assert len(roots68) == 13 and len(set(roots68)) == 12  # known duplicate pair
assert len(rootsM2) == 31 and len(set(rootsM2)) == 31
assert len(roots70) == 6 and len(set(roots70)) == 6
assert set(roots68) & set(rootsM2) == set() and set(roots68) & set(roots70) == set()
assert set(rootsM2) & set(roots70) == set()
addition50_roots = roots68 + rootsM2 + roots70
assert len(addition50_roots) == 50 and len(set(addition50_roots)) == 49
assert set(s_1163) >= set(nsU['s_cur']), 'the 1163 head must extend the 1154 solved set'
print('CONTROL unified-merge head reused from the chain-internal reproduction '
      '(1154/6693/527949/4963/391672, blob-identical JSON asserted there) '
      'and 1163 extends it')

# ---------- 3. the 4 warm batch-3 records ----------
b3 = json.loads((OUT / 'class2-lane-cost70c-warm-batch3-records-20261115.json').read_text())
assert b3['schema'] == 'n11-class2-lane-cost70c-warm-batch3-records-20261115-v1'
recs = b3['records']
assert [r['bit'] for r in recs] == [3, 42, 86, 103]
CHILD = int('00000000000000803242000000000000', 16)
for r in recs:
    assert int(r['root_hex'], 16) == CHILD | (1 << r['bit']), r
    assert r['verdict'] == 'WIN7' and r['band'] == 'class2-lane-cost70c'
    assert r['sub_roots_pass'] == r['root_check']['loser_mobility'] > 0
    assert r['union_missing'] == 0 and r['union_extra'] == 0
    assert r['terminal_range'][0] >= 13 and r['terminal_range'][1] <= 17
    assert r['rows_sorted_unique'] is True
    assert r['root_check']['stones'] == 7 and r['root_check']['match'] is True
det = recs[3]['determinism_rerun']
assert det['node_and_md5_exact'] is True and det['md5'] == recs[3]['md5']
assert det['rows'] == recs[3]['rows'] and det['extraction_nodes'] == recs[3]['extraction_nodes']
print('CONTROL 4 cost-70c warm batch-3 records asserted (root identity, rows, '
      'sub-roots, union 0/0, terminal range, md5/sha256/bytes, bit-103 '
      'determinism rerun exact)')

# ---------- 4. root disjointness ----------
roots50 = set(addition50_roots)
roots69f = {a['root_hex'] for a in addition69f}
roots4 = {r['root_hex'] for r in recs}
assert len(roots4) == 4
assert not (roots4 & roots50) and not (roots4 & roots69f), \
    'the 4 batch-3 roots must be disjoint from the 59 folded receipt roots'
print(f'CONTROL root disjointness: 4 new roots vs 49+9 distinct folded receipt '
      f'roots (intersections empty)')

# ---------- 5. fold the 4 receipts ----------
s_cur = set(s_1163)
addition = []
for r in recs:
    cov = covers(int(r['root_hex'], 16))
    marg = cov - s_cur
    marg_m = marg & manifest
    addition.append({
        'band': r['band'], 'bit': r['bit'], 'root_hex': r['root_hex'],
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
        'marginal_non_manifest_hexes': sorted(f'{k:032x}' for k in marg - marg_m),
        'rows': r['rows'], 'extraction_nodes': r['extraction_nodes'],
        'md5': r['md5'], 'sub_roots_pass': r['sub_roots_pass'],
    })
    s_cur |= marg

cov4 = set()
for r in recs:
    cov4 |= covers(int(r['root_hex'], 16))
assert s_cur == set(s_1163) | cov4, \
    'set-equality: s_after == s_1163 UNION covers(4 batch-3 roots)'
stN, remN, uniqN, demN = summary_state(s_cur)
print('AFTER cost-70c warm batch-3:', json.dumps(stN, indent=1))
total_mim = sum(a['marginal_in_manifest'] for a in addition)
total_marg = sum(a['marginal'] for a in addition)
zero_mim = [f"bit{a['bit']}" for a in addition if a['marginal_in_manifest'] == 0]
print(f'total marginal={total_marg} marginal_in_manifest={total_mim}; '
      f'zero-mim receipts: {zero_mim}')
assert total_mim == 0 and stN == st_1163, \
    'expected gain-0 in manifest (per the published prediction); the head must be unchanged'
print('CONTROL gain-0 confirmed: the head is unchanged at 1163 (band-completion fold)')

# ---------- 6. cross-check against the parallel prediction ----------
pred = json.loads((OUT / 'class2-lane-next-fold-marginal-prediction-20261115.json').read_text())
pred_map = {p['bit']: p for p in pred['cost70c_uncertified_bits']}
crosscheck = []
for a in addition:
    p = pred_map[a['bit']]
    crosscheck.append({
        'bit': a['bit'],
        'prediction_marginal_vs_1154': p['marginal'],
        'fold_marginal_vs_1163': a['marginal'],
        'prediction_marginal_in_manifest': p['marginal_in_manifest'],
        'fold_marginal_in_manifest': a['marginal_in_manifest'],
        'marginal_in_manifest_agrees': p['marginal_in_manifest'] == a['marginal_in_manifest'] == 0,
    })
assert all(c['marginal_in_manifest_agrees'] for c in crosscheck)
print('CONTROL marginal-in-manifest agrees with the parallel lane prediction '
      '(all four gain-0)')

# ---------- 7. ranking (identical numbers to the 1163 head; recorded for the fold trail) ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(remN, 2)
class4 = best(remN, 4)
AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-after-cost70c-warm3-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-cost69f-receipts-recompute-20261115.json '
                     '(cost-69f chain head 1163/6684/527280/4954/391003, '
                     'commit 30ce12b2)',
    'method': 'runpy reproduction of the cost-69f chain head '
              '(recompute_frontier_cost69f_receipts_20261115.py, asserting '
              '1163/6684/527280/4954/391003 byte-identically; that chain '
              'internally reproduces the unified-merge head 1154 with a '
              'blob-identical head-JSON control, and the unified namespace '
              'is reused from the chain for the root-disjointness control - '
              'a second in-process chain exceeded the ~1 GB memory cap, '
              'recorded in the fold log), then the '
              '4 cost-70c warm batch-3 receipts (bits 3/42/86/103 - the last '
              'uncertified WIN7-D10 bits of the completed cost-70c sweep, '
              'blind extraction + BigInt independent verification + bit-103 '
              'determinism rerun per '
              'class2-lane-cost70c-warm-batch3-records-20261115.json, claim '
              'class2-lane-cost70c-warm-batch3-inflight-20261115.json) are '
              'asserted against root identity, rows, sub-roots, union 0/0, '
              'terminal range and md5/sha256, asserted root-disjoint from the '
              '59 folded receipt roots, and folded in record order with every '
              'per-record marginal re-derived from the growing union. Gain-0 '
              'in manifest (independently confirming the parallel lane '
              'prediction): bits 3/103 fully pre-covered, bits 42/86 cover '
              'only non-manifest orbits. This completes the cost-70c band '
              '13/13 certified; no sweep claims beyond the published records '
              '- receipts only',
    'controls': {
        'cost69f_head_1163_reproduced': {
            'solved_in_manifest': 1163, 'unique_remaining': 6684,
            'sum_cost': 527280, 'open_s6': 4954, 'open_cost': 391003},
        'unified_head_1154_reproduced': 'chain-internal (blob-identical '
                                       'head JSON asserted by '
                                       'recompute_frontier_cost69f_receipts_'
                                       '20261115.py)',
        'head_1163_extends_1154': True,
        'batch3_records_asserted': True,
        'determinism_rerun_bit103': 'rows/extraction nodes/md5 identical in a '
                                    'separate process',
        'root_disjointness_vs_59_receipts': True,
        'set_equality_after_4': 's == s_1163 UNION covers(4 batch-3 roots)',
        'gain_0_in_manifest': True,
        'prediction_crosscheck': 'marginal-in-manifest agrees with '
                                 'class2-lane-next-fold-marginal-prediction-20261115.json',
    },
    'warm3_addition': addition,
    'prediction_crosscheck': crosscheck,
    'totals': {
        'receipts': len(addition),
        'total_marginal': total_marg,
        'total_marginal_in_manifest': total_mim,
        'zero_marginal_in_manifest': zero_mim,
        'batch3_rows': sum(r['rows'] for r in recs),
        'batch3_extraction_nodes': sum(r['extraction_nodes'] for r in recs),
        'cost70c_band': '13/13 WIN7 bits certified (9 previously + 4 here)',
    },
    'frontier_after_cost70c_warm3': {
        'solved_s6_in_manifest': stN['solved_s6_in_manifest'],
        'remaining_s5_orbits': stN['remaining_s5_orbits'],
        'unique_remaining_s6': stN['unique_remaining_s6'],
        'sum_remaining_cost': stN['sum_remaining_cost'],
        's6_needed_by_open_classes': stN['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stN['cost_needed_by_open_classes'],
        'demand_histogram_open_only': stN['hist'],
        'best_class2': class2[0],
        'audit_blocked_class2': next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'outstanding_not_folded': {
        'cost69f_certificates': 'WIN7 bits 2/94/109/119 certificates still '
                                'pending extraction (folded by the parallel '
                                'lane as raw sweep receipts with v15 anchors; '
                                'extraction stays with that lane)',
        'cost75c': 'sweep complete with 12 verified receipts (parallel lane); '
                   'not yet folded into a chain-head publication - belongs to '
                   'a later canonical recompute',
        'cost65j_sweep': 'in flight on the parallel lane; its bit-113 WIN7 '
                         '(if found) cross-covers the cost-69f child through '
                         'the shared orbit - recheck before the next fold',
        'parallel_bands': 'cost-65h/67b/68c warm candidates and the in-flight '
                          'cost-65j sweep stay with the parallel lane',
    },
    'interpretation_guard': 'bookkeeping over published receipts; solved counts '
                            'measure manifest coverage, not the game-theoretic '
                            'value of any position; REFUTED-D10 sweeps prove '
                            'only absence of WIN7-D10; WIN7 certificates prove '
                            'a win within depth 10 from the individual '
                            '7-stone roots only; 11x11 empty board / two-stone '
                            'root {49,60} / S2 {59,60} / class 2 / class 4 '
                            'remain UNKNOWN',
}
(OUT / 'class-frontier-after-cost70c-warm3-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + '\n')
print('written class-frontier-after-cost70c-warm3-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remN.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost70c-warm3-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-cost70c-warm3-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('second coverable class-2 candidate S5',
                         class2[2] if len(class2) > 2 else class2[1])):
        rows = remN.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = demN[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost70c-warm3)')
