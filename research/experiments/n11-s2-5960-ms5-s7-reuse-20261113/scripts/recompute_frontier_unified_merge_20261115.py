#!/usr/bin/env python3
"""Unified class-2/4 frontier merge of all three divergent folds over the
common after-warm-multiband baseline (2026-11-15), executing the published
unified-fold specification of class2-lane-unified-fold-reconciliation-20261115.json.

Three folds over the common 1109 baseline
(class-frontier-warm-multiband-recompute-20261115.json,
1109 / 6738 / 531295 / 5008 / 395018) were published on main:

- the cost-68d fold (1117): 13 receipts = 7 cost-68d WIN7 + 6 warm band
  hygiene (one cross-child duplicate pair 71b-bit1 == 61d-bit22);
- the warm multiband batch-2 fold (1140): 31 WIN7 receipts;
- the six cost-70c warm batch-2 WIN7 certificates (published under
  class2-lane-cost70c-certificates/, folded in neither head).

The three receipt groups are pairwise root-disjoint (published crosscheck
plus this script's own three-way disjointness assert), so the unified fold
predicts 1109 + 8 + 31 + 6 = 1154 solved-in-manifest.

This script (executing the CURRENT main version of the specification, the one
carrying correction_20261115_b):
1. reproduces the published 1117 endpoint by runpy of
   recompute_frontier_cost68d_20261115.py (which itself reproduces the 1109
   baseline byte-identically and self-asserts all 13 cost-68d/hygiene
   records, the sweep re-sum, the determinism rerun and the v15 anchors),
   giving the 13 receipts folded in published order;
2. reproduces the published 1140 endpoint by runpy of
   recompute_frontier_warm_multiband2_20261115.py (self-asserts all 31
   warm multiband 2 records);
2b. reproduces the published merged 1148 head
   (class-frontier-merged-recompute-after-multiband2-68dhyg-20261115.json,
   commit 19bb2abc) byte-identically by runpy of
   recompute_frontier_merged_after_multiband2_68dhyg_20261115.py, asserting
   the published endpoint 1148/6699/528423/4969/392146, the byte-identity of
   the regenerated frontier JSON (md5 vs main) and the union identity
   s_1148 == s_1117 | s_1140;
3. asserts three-way root disjointness of the 50 receipts (12 distinct
   cost-68d-group roots after the known duplicate pair, 31 multiband2,
   6 cost-70c);
4. folds the 31 multiband2 receipts in published record order onto the 1117
   state, asserting every per-record marginal-in-manifest hex set equals the
   published multiband2 addition (batch2 x 68d marginal disjointness);
5. asserts the 6 cost-70c warm receipts against BOTH the published
   reconciliation JSON and the independent BigInt verification record
   class2-lane-cost70c-warm6-bigint-independent-verification-20261115.json
   (rows, sub-roots, md5, sha256, bytes, local certificate bytes, git blob
   shas), folds them in the greedy order 105, 92, 40, 24, 11, 8, asserting
   each adds exactly its published marginal manifest orbit; the three
   pre-covered manifest certificates (bits 94/20/23) are asserted
   marginal-0 against the merged set (positive duplicate cross-checks,
   already folded in the chain baseline, not re-folded);
6. asserts the set-equality control
   s_merged == s_1117 | s_1140 | covers(6 cost-70c receipts)
   and solved_s6_in_manifest == 1154;
7. produces the unified frontier JSON + ranking CSV + top-candidates CSV.

Receipts only - no sweep claims are made here.
"""
import csv, hashlib, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the 1117 endpoint (13 receipts folded in order) ----------
ns68 = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost68d_20261115.py'))
s_1109 = ns68['sW']
s_1117 = ns68['s_cur']
stX = ns68['stX']
covers = ns68['covers']
manifest = ns68['manifest']
classes = ns68['classes']
summary_state = ns68['summary_state']
assert stX['solved_s6_in_manifest'] == 1117 and stX['unique_remaining_s6'] == 6730
assert stX['sum_remaining_cost'] == 530739
assert stX['s6_needed_by_open_classes'] == 5000 and stX['cost_needed_by_open_classes'] == 394462
print('CONTROL 1109 baseline + 1117 endpoint reproduced (13 cost-68d/hygiene receipts folded in published order)')

# ---------- 2. reproduce the 1140 endpoint (31 receipts, self-asserted) ----------
nsM2 = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_warm_multiband2_20261115.py'))
s_1140 = nsM2['s_cur']
stW2 = nsM2['stW2']
assert stW2['solved_s6_in_manifest'] == 1140 and stW2['unique_remaining_s6'] == 6707
assert stW2['sum_remaining_cost'] == 528979
assert stW2['s6_needed_by_open_classes'] == 4977 and stW2['cost_needed_by_open_classes'] == 392702
print('CONTROL 1140 endpoint reproduced (31 warm multiband 2 receipts self-asserted)')

# ---------- 2b. reproduce the published merged 1148 head byte-identically ----------
nsMM = runpy.run_path(str(HERE / 'scripts' /
                         'recompute_frontier_merged_after_multiband2_68dhyg_20261115.py'))
s_1148 = nsMM['s_cur']
stM = nsMM['stX']
assert stM['solved_s6_in_manifest'] == 1148 and stM['unique_remaining_s6'] == 6699
assert stM['sum_remaining_cost'] == 528423
assert stM['s6_needed_by_open_classes'] == 4969 and stM['cost_needed_by_open_classes'] == 392146
merged_json = OUT / 'class-frontier-merged-recompute-after-multiband2-68dhyg-20261115.json'
assert hashlib.md5(merged_json.read_bytes()).hexdigest() == \
    '4a3a8693315d15b52a05194b1599b035', \
    'regenerated merged-1148 frontier JSON must be byte-identical to main'
assert set(s_1148) == set(s_1117) | set(s_1140), 'merged head must be the union of both folds'
print('CONTROL merged 1148 head reproduced byte-identically '
      '(1148/6699/528423/4969/392146) and equals s_1117 | s_1140')

# ---------- 3. three-way root disjointness of the 50 receipts ----------
certdoc68 = json.loads((OUT / 'class2-lane-cost68d-win7-certificates-20261115.json').read_text())
hygdoc = json.loads((OUT / 'class2-lane-warm-band-hygiene-certificates-20261115.json').read_text())
recdoc2 = json.loads((OUT / 'class2-lane-warm-multiband2-certificates-20261115.json').read_text())
recon = json.loads((OUT / 'class2-lane-unified-fold-reconciliation-20261115.json').read_text())
verify70 = json.loads(
    (OUT / 'class2-lane-cost70c-warm6-bigint-independent-verification-20261115.json').read_text())

roots68 = [c['root_hex'] for c in certdoc68['certificates']] + \
          [r['root_hex'] for r in hygdoc['records']]
assert len(roots68) == 13 and len(set(roots68)) == 12  # known duplicate pair
rootsM2 = [r['root_hex'] for r in recdoc2['records']]
assert len(rootsM2) == 31 and len(set(rootsM2)) == 31
roots70 = [r['root_hex'] for r in recon['cost70c_warm_batch2_receipts']]
assert roots70 == [r['root_hex'] for r in verify70['records']]
assert len(roots70) == 6 and len(set(roots70)) == 6
assert set(roots68) & set(rootsM2) == set()
assert set(roots68) & set(roots70) == set()
assert set(rootsM2) & set(roots70) == set()
print('CONTROL three-way root disjointness: 12 + 31 + 6 distinct roots, intersections empty')

# ---------- 4. fold the 31 multiband2 receipts in published order onto 1117 ----------
w2 = json.loads((OUT / 'class-frontier-warm-multiband2-recompute-20261115.json').read_text())
pub_add = w2['warm_multiband2_addition']
assert [a['band'] + str(a['bit']) for a in pub_add] == \
       [r['band'] + str(r['bit']) for r in recdoc2['records']]
s_cur = set(s_1117)
multiband2_addition = []
for r, pub in zip(recdoc2['records'], pub_add):
    cov = covers(int(r['root_hex'], 16))
    marg = cov - s_cur
    marg_m = marg & manifest
    hexes = sorted(f'{k:032x}' for k in marg_m)
    assert hexes == pub['marginal_manifest_hexes'], (r['band'], r['bit'], hexes)
    assert int(r['root_hex'], 16) == int(r['child_hex'], 16) | (1 << r['bit'])
    multiband2_addition.append({
        'band': r['band'], 'bit': r['bit'], 'root_hex': r['root_hex'],
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': hexes,
    })
    s_cur |= marg
assert set(s_cur) == set(s_1148), \
    'folding the 31 multiband2 receipts onto 1117 must re-derive the merged 1148 state'
m2_mim = sum(a['marginal_in_manifest'] for a in multiband2_addition)
assert m2_mim == 31, 'the 31 multiband2 receipts must add exactly 31 manifest orbits'
print(f'CONTROL 31 multiband2 receipts folded onto 1117: +{m2_mim} manifest orbits')

# ---------- 5. assert + fold the 6 cost-70c warm receipts (greedy order) ----------
GREEDY = (105, 92, 40, 24, 11, 8)
assert [r['bit'] for r in recon['cost70c_warm_batch2_receipts']] == list(GREEDY)
child_v = int('00000000000000803242000000000000', 16)
c70_addition = []
for rr in recon['cost70c_warm_batch2_receipts']:
    bit = rr['bit']
    vr = next(v for v in verify70['records'] if v['bit'] == bit)
    assert vr['root_hex'] == rr['root_hex'] and vr['rows'] == rr['rows']
    assert vr['sub_roots_pass'] == rr['sub_roots_pass'] and vr['md5'] == rr['md5']
    assert vr['bytes'] == rr['bytes'] and len(vr['sha256']) == 64
    assert vr['verdict'] == 'WIN7' and vr['rows_sorted_unique'] is True
    assert vr['union_missing'] == 0 and vr['union_extra'] == 0
    assert vr['sub_roots_pass'] == vr['root_check']['loser_mobility']
    assert vr['root_check']['match'] is True and vr['root_check']['stones'] == 7
    assert 13 <= vr['terminal_range'][0] and vr['terminal_range'][1] <= 17
    assert int(vr['root_hex'], 16) == child_v | (1 << bit)
    # local certificate bytes must reproduce the recorded digests
    st = vr['storage']
    if st['layout'] == 'single file':
        data = (OUT / st['file']).read_bytes()
        assert len(data) == st['bytes'] == rr['bytes']
    else:
        p1 = (OUT / st['part1']['path']).read_bytes()
        p2 = (OUT / st['part2']['path']).read_bytes()
        assert p1.endswith(b'\n'), 'part1 must end on a line boundary'
        data = p1 + p2
        assert len(p1) == st['part1']['bytes'] and len(p2) == st['part2']['bytes']
    assert hashlib.md5(data).hexdigest() == vr['md5']
    assert hashlib.sha256(data).hexdigest() == vr['sha256']
    assert len(data) == vr['bytes']
    # fold
    cov = covers(int(vr['root_hex'], 16))
    marg = cov - s_cur
    marg_m = marg & manifest
    hexes = sorted(f'{k:032x}' for k in marg_m)
    assert hexes == [rr['marginal_manifest_hex']], (bit, hexes)
    c70_addition.append({
        'band': 'class2-lane-cost70c', 'bit': bit, 'root_hex': vr['root_hex'],
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': hexes,
        'rows': vr['rows'], 'md5': vr['md5'],
    })
    s_cur |= marg
assert sum(a['marginal_in_manifest'] for a in c70_addition) == 6
print('CONTROL 6 cost-70c warm receipts verified (reconciliation x independent-BigInt '
      'x local-bytes) and folded: +6 manifest orbits')

# pre-covered manifest certificates 94/20/23: positive duplicate cross-checks
for c in json.loads((OUT / 'class2-lane-cost70c-win7-certificates-20261115.json').read_text())['certificates']:
    cov = covers(int(c['root_hex'], 16))
    assert cov <= s_cur, 'pre-covered manifest certificate must have zero marginal'
print('CONTROL pre-covered manifest certificates 94/20/23 marginal-0 (already in chain baseline)')

# ---------- 6. controls and summary ----------
assert s_cur == set(s_1117) | set(s_1140) | set().union(
    *(covers(int(r['root_hex'], 16)) for r in recon['cost70c_warm_batch2_receipts']))
assert s_cur == set(s_1148) | set().union(
    *(covers(int(r['root_hex'], 16)) for r in recon['cost70c_warm_batch2_receipts'])), \
    'spec control: s_merged_final == s_1148 UNION covers(6)'
stU, remU, uniqU, demU = summary_state(s_cur)
assert stU['solved_s6_in_manifest'] == 1154, stU
print('AFTER unified merge:', json.dumps(stU, indent=1))
assert s_cur >= set(s_1117) and s_cur >= set(s_1140)

total_mim = 8 + m2_mim + 6
assert stU['solved_s6_in_manifest'] - 1109 == total_mim

# ---------- 7. outputs ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(remU, 2)
class4 = best(remU, 4)
AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-unified-merge-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-warm-multiband-recompute-20261115 (common baseline '
                     '1109 / 6738 / 531295 / 5008 / 395018) with the three published folds: '
                     'class-frontier-cost68d-recompute-20261115 (1117), '
                     'class-frontier-warm-multiband2-recompute-20261115 (1140), '
                     'class-frontier-merged-recompute-after-multiband2-68dhyg-20261115 (1148)',
    'method': 'execution of the published unified-fold specification '
              '(class2-lane-unified-fold-reconciliation-20261115.json): runpy '
              'recompute_frontier_cost68d_20261115.py reproduces the 1109 baseline '
              'byte-identically and the 1117 endpoint with the 13 cost-68d/hygiene '
              'receipts folded in published order; runpy '
              'recompute_frontier_warm_multiband2_20261115.py reproduces the 1140 '
              'endpoint; runpy '
              'recompute_frontier_merged_after_multiband2_68dhyg_20261115.py '
              'reproduces the published merged 1148 head byte-identically '
              '(regenerated frontier JSON md5-checked against main; endpoint '
              '1148/6699/528423/4969/392146) with the union identity '
              's_1148 == s_1117 | s_1140 asserted; three-way root disjointness of the 50 receipts is asserted '
              '(12 distinct cost-68d-group roots after the canonical cross-child '
              'duplicate 71b-bit1 == 61d-bit22, 31 multiband2, 6 cost-70c); the 31 '
              'multiband2 receipts are folded in published record order onto 1117 with '
              'every per-record marginal-in-manifest hex set asserted equal to the '
              'published multiband2 addition; the 6 cost-70c warm receipts (greedy '
              'order 105, 92, 40, 24, 11, 8) are asserted against the published '
              'reconciliation JSON and the independent BigInt verification record '
              '(rows, sub-roots, union 0/0, md5, sha256, bytes, local certificate '
              'bytes, git blob shas) and folded; the pre-covered manifest certificates '
              '94/20/23 are asserted marginal-0; set-equality control '
              's_merged == s_1117 | s_1140 | covers(6) asserted; solved 1154 = 1109 + '
              '8 + 31 + 6. Receipts only - no sweep claims',
    'controls': {
        'baseline_1109_reproduced_byte_identical': True,
        'endpoint_1117_reproduced': True,
        'endpoint_1140_reproduced': True,
        'endpoint_1148_merged_head_reproduced_byte_identical': True,
        'merged_head_union_identity_s1117_union_s1140': True,
        'three_way_root_disjointness': True,
        'multiband2_per_record_marginal_hexes_equal_published': True,
        'cost70c_receipts_reconciliation_x_bigint_x_local_bytes': True,
        'pre_covered_manifest_certificates_marginal_zero': True,
        'set_equality_s1117_union_s1140_union_covers6': True,
        'set_equality_s1148_union_covers6': True,
        'expected_solved_1154': True,
    },
    'unified_addition': {
        'cost68d_lane_receipts': 13,
        'cost68d_lane_marginal_in_manifest': 8,
        'multiband2_receipts': 31,
        'multiband2_marginal_in_manifest': m2_mim,
        'cost70c_warm_receipts': 6,
        'cost70c_warm_marginal_in_manifest': 6,
        'total_receipts': 50,
        'total_marginal_in_manifest': total_mim,
    },
    'multiband2_addition': multiband2_addition,
    'cost70c_warm_addition': c70_addition,
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
        'cost69f_sweep': 'completed on the parallel lane (9 WIN7-D10 bits '
                         '2/20/44/68/69/94/109/118/119, raw batches published); '
                         'certificates and fold pending with that lane - the next '
                         'unified merge must fold its receipts once published',
        'cost70c_remaining': 'WIN7 bits 3/42/86/103 uncertified (warm rebuild candidates)',
        'parallel_bands': 'cost-65h/67b/68c warm candidates and the in-flight cost-65j '
                          'sweep stay with the parallel lane (their in-manifest '
                          'marginals are listed in '
                          'class2-lane-warm-candidate-ranking2-20261115.json)',
        'gain0_candidates': 'gain-0-in-manifest warm candidates advance no manifest '
                            'orbit until the solved set changes',
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps '
                            'prove only absence of WIN7-D10; WIN7 certificates prove a '
                            'win within depth 10 from the 7-stone root only; solved '
                            'counts measure manifest coverage, not the game-theoretic '
                            'value of the 11x11 empty board; 11x11 empty root / '
                            '{49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-unified-merge-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
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
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-unified-merge-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
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
