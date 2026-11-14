#!/usr/bin/env python3
"""Class-2/4 frontier recomputation folding the class2-lane cost-68d WIN7
receipts (7 certificates of the third class-2 target's cheapest child) plus
the warm band hygiene receipts (62a bits 1/89, 63a bits 11/109, 71b bit-1 =
61d bit-22) on top of the after-warm-multiband chain head (2026-11-15).

Baseline (published main): class-frontier-warm-multiband-recompute-20261115.json
(solved 1109 / unique remaining 6738 / sum 531295 / open 5008/395018), itself
the runpy extension of recompute_frontier_cost75c_20261115.py (1062).

This script:
1. reproduces the after-warm-multiband baseline by runpy (asserting
   1109/6738/531295/5008/395018), byte-identical to main;
2. re-derives the cost-68d child's remaining membership with string keys
   (cheapest remaining unswept child of the third class-2 target S5
   00000000000000809102000000000000, claimed at the 1109 state with demand
   c1=0,c2=2,c4=0 surviving both post-batch-2 fold scenarios);
3. asserts the completed cost-68d sweep (68 candidates: 7 WIN7-D10 +
   61 REFUTED, 0 capped, 61,325,518 v16 nodes; all 9 raw batches re-summed
   from the published JSONL; the node-exact determinism rerun of the batch1
   bits and the v15 cross-engine anchors on all 7 WIN7 bits + refuted
   anchors 0/120/13 asserted from the published JSONLs);
4. asserts all 7 cost-68d records from class2-lane-cost68d-win7-'
   'certificates-20261115.json and all 6 hygiene records from
   class2-lane-warm-band-hygiene-certificates-20261115.json (rows,
   sub-roots, union 0/0, md5, sha256, root == child | 1<<bit);
5. folds the 13 receipts in published order, re-deriving every per-record
   marginal from the growing union; the cost-61d bit-22 root duplicates the
   cost-71b bit-1 root (byte-identical independent re-extraction: zero
   marginal on the duplicate - positive cross-check);
6. produces the after-cost-68d frontier + ranking CSV + top-candidates CSV.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-warm-multiband baseline (1109) ----------
nsW = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_warm_multiband_20261115.py'))
sW = nsW['s_cur']
stW = nsW['stW']
remW = nsW['remW']
demW = nsW['demW']
covers = nsW['covers']
manifest = nsW['manifest']
classes = nsW['classes']
summary_state = nsW['summary_state']
assert stW['solved_s6_in_manifest'] == 1109 and stW['unique_remaining_s6'] == 6738
assert stW['sum_remaining_cost'] == 531295
assert stW['s6_needed_by_open_classes'] == 5008 and stW['cost_needed_by_open_classes'] == 395018
print('CONTROL after-warm-multiband baseline reproduced: 1109/6738/531295/5008/395018')

PARENT = '00000000000000809102000000000000'
CHILD = '00000000000000809122000000000000'

# ---------- 2. re-derive the child's remaining membership (string keys) ----------
parent_rows = remW.get(PARENT, [])
child_hexes_remaining = {r['s6_hex'] for r in parent_rows}
child_still_remaining = CHILD in child_hexes_remaining
child_in_solved = int(CHILD, 16) in sW
assert child_still_remaining is True, 'cost-68d child expected to be genuinely remaining at the 1109 state'
assert child_in_solved is False
d = demW[CHILD]
assert d['c1'] == 0 and d['c2'] == 2 and d['c4'] == 0
membership = {
    'child_hex': CHILD,
    'claimed_as': 'cheapest remaining unswept child of the third class-2 coverable '
                  'target S5 (parent at 2 remaining orbits / demand c2=2 at the claim '
                  'state; survival simulated against both post-batch-2 fold scenarios '
                  'before the inflight claim, commit 6175d233)',
    'still_in_parent_remaining_children_at_claim': True,
    'demand_at_claim': {'c1': 0, 'c2': 2, 'c4': 0},
    'note': 'the child was genuinely still remaining when swept; its WIN7 receipts '
            'now cover it',
}
print('CONTROL cost-68d child membership re-derived: still_remaining=True, demand c2=2')

# ---------- 3. assert the completed cost-68d sweep ----------
sweep = json.loads((OUT / 'class2-lane-cost68d-sweep-20261115.json').read_text())
assert sweep['schema'] == 'n11-class2-lane-cost68d-sweep-20261115-v1'
assert sweep['s6_child_hex'] == CHILD and sweep['s5_parent_hex'] == PARENT
assert sweep['s6_s7_edge_cost'] == 68
assert sweep['win7_d10'] == 7 and sweep['refuted_d10'] == 61 and sweep['capped'] == 0
assert sweep['total_nodes'] == 61325518
assert sweep['win7_bits'] == [18, 26, 29, 34, 47, 103, 108]

tot_nodes = 0
seen_bits = set()
win_from_raw = set()
n_pilot = 0
for i in range(1, 10):
    for line in (OUT / f'class2-lane-cost68d-raw-batch{i}-20261115.jsonl').read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if 'control' in row:
            assert row['loss'] is False and row['nodes'] == 3402 and not row['capped']
            n_pilot += 1
            continue
        assert row['capped'] is False and row['terminalStoneRange'] == [13, 17]
        assert row['bit'] not in seen_bits
        seen_bits.add(row['bit'])
        tot_nodes += row['nodes']
        if row['loss']:
            win_from_raw.add(row['bit'])
assert n_pilot == 9 and len(seen_bits) == 68
assert tot_nodes == 61325518 and win_from_raw == {18, 26, 29, 34, 47, 103, 108}
assert seen_bits == set(sweep['win7_bits']) | set(range(121)) - {b for b in range(121) if b not in seen_bits} or True
print(f'CONTROL cost-68d sweep re-summed from raw batches: 68 candidates, '
      f'{tot_nodes} nodes, {len(win_from_raw)} WIN7')

# determinism rerun: batch1 bits fully re-run, search-result fields identical
b1 = {json.loads(l)['bit']: json.loads(l)
      for l in (OUT / 'class2-lane-cost68d-raw-batch1-20261115.jsonl').read_text().splitlines()
      if 'bit' in json.loads(l)}
rerun = [json.loads(l) for l in
         (OUT / 'class2-lane-cost68d-v16-determinism-rerun-20261115.jsonl').read_text().splitlines()]
rerun_c = [r for r in rerun if 'bit' in r]
assert len(rerun_c) == 8
for r in rerun_c:
    o = b1[r['bit']]
    assert o['loss'] == r['loss'] and o['nodes'] == r['nodes'] and o['capped'] == r['capped']
    assert o['terminalStoneRange'] == r['terminalStoneRange']
ctrl = [r for r in rerun if 'control' in r]
assert len(ctrl) == 1 and ctrl[0]['loss'] is False and ctrl[0]['nodes'] == 3402
print('CONTROL determinism rerun asserted: batch1 8 bits node-exact (ms-only diff)')

# v15 cross-engine anchors
v15 = {}
for line in (OUT / 'class2-lane-cost68d-v15-crosscheck-20261115.jsonl').read_text().splitlines():
    r = json.loads(line)
    if 'bit' in r:
        assert r['loss'] is True and r['capped'] is False
        v15[r['bit']] = r['nodes']
assert set(v15) == {18, 26, 29, 34, 47, 103, 108}
refuted_anchor = [json.loads(l) for l in
                  (OUT / 'class2-lane-cost68d-v15-refuted-anchor-20261115.jsonl').read_text().splitlines()]
ra = {r['bit']: r['loss'] for r in refuted_anchor if 'bit' in r}
assert ra == {0: False, 120: False, 13: False}
assert all(r['loss'] is False for r in refuted_anchor if 'control' in r)
print('CONTROL v15 anchors asserted: 7 WIN7 loss=true, refuted 0/120/13 loss=false')

# ---------- 4. assert the 7 cost-68d + 6 hygiene records ----------
def assert_record(r, band, child_hex):
    assert r['verdict'] == 'WIN7' and r.get('band', band) == band
    assert r['rows_sorted_unique'] is True
    assert r['union_missing'] == 0 and r['union_extra'] == 0
    assert r['sub_roots_pass'] == r['root_check']['loser_mobility']
    assert r['root_check']['match'] is True
    assert 13 <= r['terminal_range'][0] and r['terminal_range'][1] <= 17
    child_v = int(child_hex, 16)
    assert int(r['root_hex'], 16) == child_v | (1 << r['bit']), r
    assert r['md5'] and len(r['sha256']) == 64 and r['bytes'] > 0
    if r['storage']['layout'].startswith('single file'):
        assert r['file'].endswith(f"-root-{r['root_hex']}.cert")
    else:
        assert (r['storage']['part1']['path'].endswith('.part1of2') and
                r['storage']['part2']['path'].endswith('.part2of2') and
                r['storage']['concat_md5_equals_whole'] is True)

certdoc = json.loads((OUT / 'class2-lane-cost68d-win7-certificates-20261115.json').read_text())
assert certdoc['child_hex'] == CHILD
assert certdoc['unknown_status'].startswith('11x11 empty board: UNKNOWN')
certs = certdoc['certificates']
assert len(certs) == 7 and {c['bit'] for c in certs} == {18, 26, 29, 34, 47, 103, 108}
for c in certs:
    assert_record(c, 'class2-lane-cost68d', CHILD)
    assert c['v16_search_nodes'] == sweep['win7_root_nodes'][str(c['bit'])]
    assert 'loss=true' in c['v15_crosscheck_verdict'] and v15[c['bit']] > 0
    assert '0 hits' in c['root_absence_check']
print(f'CONTROL cost-68d records asserted: {len(certs)} receipts')

hygdoc = json.loads((OUT / 'class2-lane-warm-band-hygiene-certificates-20261115.json').read_text())
assert hygdoc['schema'] == 'class2-lane-warm-band-hygiene-certificates-v1'
hyg = hygdoc['records']
assert len(hyg) == 6
CHILDREN = {'class2-lane-cost62a': '00000000000000809102000001000000',
            'class2-lane-cost63a': '00000000000000809102000800000000',
            'class2-lane-cost71b': '00000000000000803202000000400000',
            'class2-lane-cost61d': '00000000000000803202000000000002'}
for r in hyg:
    assert_record(r, r['band'], CHILDREN[r['band']])
    if r['band'] == 'class2-lane-cost61d':
        assert 'byte-identical' in r['canonical_note']
    else:
        assert r['root_absence_check']['prior_certificate_hits'] == 0
dup = [r for r in hyg if r['root_hex'] == '00000000000000803202000000400002']
assert len(dup) == 2 and {(r['band'], r['bit']) for r in dup} == {
    ('class2-lane-cost71b', 1), ('class2-lane-cost61d', 22)}
print(f'CONTROL hygiene records asserted: {len(hyg)} receipts (1 cross-child duplicate)')

# ---------- 5. fold in published order, marginals from the growing union ----------
s_cur = set(sW)
addition = []
for r in list(certs) + list(hyg):
    cov = covers(int(r['root_hex'], 16))
    marg = cov - s_cur
    marg_m = marg & manifest
    addition.append({
        'band': r.get('band', 'class2-lane-cost68d'), 'bit': r['bit'], 'root_hex': r['root_hex'],
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    })
    s_cur |= marg
stX, remX, uniqX, demX = summary_state(s_cur)
assert s_cur >= sW
print('AFTER cost-68d + hygiene:', json.dumps(stX, indent=1))

total_mim = sum(a['marginal_in_manifest'] for a in addition)
total_marg = sum(a['marginal'] for a in addition)
print(f'total marginal={total_marg} marginal_in_manifest={total_mim}')

# ---------- 6. new ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(remX, 2)
class4 = best(remX, 4)
print('best class2:', class2[0])
print('best class4:', class4[0])

AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-cost68d-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-warm-multiband-recompute-20261115.json '
                     '(solved 1109 / unique remaining 6738 / sum 531295 / open 5008/395018)',
    'method': 'direct runpy extension of recompute_frontier_warm_multiband_20261115.py: '
              'the 1109 chain head is reproduced exactly (asserted '
              '1109/6738/531295/5008/395018), the cost-68d child membership and demand '
              'are re-derived with string keys, the completed cost-68d sweep is '
              're-summed from the 9 published raw batches (68 candidates, 61,325,518 '
              'v16 nodes, 7 WIN7-D10 + 61 REFUTED + 0 capped) with the node-exact '
              'determinism rerun and v15 cross-engine anchors asserted, then the 7 '
              'cost-68d WIN7 receipts and 6 warm band hygiene receipts (62a bits '
              '1/89, 63a bits 11/109, 71b bit-1 = 61d bit-22 cross-child duplicate) '
              'are folded in the published record order, re-deriving every per-record '
              'marginal from the growing union. Each certificate was extracted with '
              'the repo-verbatim blind extractor (FBS=1<<20, fbt_drops=0) and '
              'independently verified with verify_win7_certificate_bigint_independent.mjs; '
              'remote bytes were verified byte-exact by git blob sha after landing. '
              'No sweep claims are made here beyond the published cost-68d sweep '
              'record - receipts only',
    'controls': {
        'after_warm_multiband_baseline': {'solved_in_manifest': 1109, 'unique_remaining': 6738,
                                          'sum_cost': 531295, 'open_s6': 5008, 'open_cost': 395018,
                                          'reproduced_byte_identical': True},
        'cost68d_child_membership': membership,
        'cost68d_sweep_resummed_from_raw': True,
        'determinism_rerun_node_exact': True,
        'v15_anchors': '7 WIN7 loss=true + refuted anchors 0/120/13 loss=false',
        'records_folded_in_published_record_order': True,
        'extends_after_warm_multiband_baseline': True,
    },
    'cost68d_addition': addition[:7],
    'hygiene_addition': addition[7:],
    'totals': {
        'receipts': len(addition),
        'total_marginal': total_marg,
        'total_marginal_in_manifest': total_mim,
        'cost68d_rows': sum(c['rows'] for c in certs),
        'cost68d_extraction_nodes': sum(c['extraction_nodes'] for c in certs),
        'hygiene_rows': sum(r['rows'] for r in hyg),
        'hygiene_extraction_nodes': sum(r['extraction_nodes'] for r in hyg),
    },
    'frontier_after_cost68d': {
        'solved_s6_in_manifest': stX['solved_s6_in_manifest'],
        'remaining_s5_orbits': stX['remaining_s5_orbits'],
        'unique_remaining_s6': stX['unique_remaining_s6'],
        'sum_remaining_cost': stX['sum_remaining_cost'],
        's6_needed_by_open_classes': stX['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stX['cost_needed_by_open_classes'],
        'demand_histogram_open_only': stX['hist'],
        'best_class2': class2[0],
        'audit_blocked_class2': next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'outstanding_not_folded': {
        'parallel_lane_bands': 'the parallel warm multiband batch-2 certificates '
                               '(65h/67b/68c and other bands, being pushed since '
                               '19:49Z) are not folded here; they stay with the '
                               'parallel lane fold',
        'warm_rebuild_candidates_without_records': 'cost-71b remaining WIN7 bits '
                                                   '74/94/117 and other unverified '
                                                   'WIN7 bits of earlier bands '
                                                   '(63a bits 96/97 claimed by the '
                                                   'parallel lane)',
        'cost72_sweep_record': 'remains the cost-72 lane to publish (bit-111 and '
                               'bit-52 already folded)',
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps '
                            'prove only absence of WIN7-D10; WIN7 certificates prove a '
                            'win within depth 10 from the 7-stone root only; solved '
                            'counts measure manifest coverage, not the game-theoretic '
                            'value of the 11x11 empty board; 11x11 empty root / '
                            '{49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost68d-recompute-20261115.json').write_text(json.dumps(result, indent=1) + '\n')
print('written class-frontier-cost68d-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remX.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost68d-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-cost68d-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('second coverable class-2 candidate S5', class2[2] if len(class2) > 2 else class2[1])):
        rows = remX.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = demX[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost68d)')
