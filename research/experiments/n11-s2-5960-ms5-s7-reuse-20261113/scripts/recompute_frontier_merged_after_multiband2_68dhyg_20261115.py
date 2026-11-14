#!/usr/bin/env python3
"""Class-2/4 frontier merged recomputation: fold the class2-lane cost-68d WIN7
receipts (7 certificates) plus the warm band hygiene receipts (62a bits 1/89,
63a bits 11/109, 71b bit-1 = 61d bit-22) on top of the after-warm-multiband-2
chain head (2026-11-15).

The 1109 after-warm-multiband chain head had two divergent published folds:

- class-frontier-cost68d-recompute-20261115.json (this lane: solved 1117),
  folding the 7 cost-68d WIN7 receipts + 6 hygiene receipts;
- class-frontier-warm-multiband2-recompute-20261115.json (the concurrent
  batch-2 lane takeover: solved 1140), folding the 31 warm multiband 2
  receipts.

Both folds extend the same 1109 baseline with pairwise-disjoint receipt
sets (verified by class2-lane-warm-multiband2-duplicate-crosscheck-20261115.json:
31 roots, 54 entries, byte-exact duplicates only, zero WIN/LOSS conflicts; the
batch-2 selection explicitly deferred this lane's hygiene bits 62a 1/89,
63a 11/109, 61d bit-22 = 71b bit-1 and never touched the cost-68d band).
This script merges the fork by:

1. reproducing the after-warm-multiband-2 chain head (solved 1140 / unique
   remaining 6707 / sum 528979 / open 4977/392702) by runpy,
   byte-identically from the published chain;
2. asserting the disjointness of the two receipt sets against the published
   duplicate crosscheck;
3. re-deriving the cost-68d child's remaining membership with string keys
   at the 1140 state (the child is genuinely still remaining there: the 31
   batch-2 roots never covered it);
4. asserting the completed cost-68d sweep (68 candidates: 7 WIN7-D10 + 61
   REFUTED, 0 capped, 61,325,518 v16 nodes; raw batches re-summed, the
   node-exact determinism rerun and the v15 cross-engine anchors asserted);
5. asserting all 7 cost-68d records and all 6 hygiene records (rows,
   sub-roots, union 0/0, md5, sha256, root == child | 1<<bit);
6. folding the 13 receipts in published order, re-deriving every per-record
   marginal from the growing union that already contains the 31 batch-2
   receipts; the cost-61d bit-22 root duplicates the cost-71b bit-1 root
   (byte-identical independent re-extraction: zero marginal on the duplicate
   - positive cross-check);
7. producing the merged frontier + ranking CSV + top-candidates CSV.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ------- 1. reproduce the after-warm-multiband-2 chain head (1140) --------
ns2 = runpy.run_path(str(HERE / 'scripts' /
                         'recompute_frontier_warm_multiband2_20261115.py'))
s2 = ns2['s_cur']
st2 = ns2['stW2']
rem2 = ns2['remW2']
dem2 = ns2['demW2']
covers = ns2['covers']
manifest = ns2['manifest']
classes = ns2['classes']
summary_state = ns2['summary_state']
records_mb2 = ns2['records']
assert st2['solved_s6_in_manifest'] == 1140 and st2['unique_remaining_s6'] == 6707
assert st2['sum_remaining_cost'] == 528979
assert st2['s6_needed_by_open_classes'] == 4977 and st2['cost_needed_by_open_classes'] == 392702
print('CONTROL after-warm-multiband-2 chain head reproduced: '
      '1140/6707/528979/4977/392702')

# ------- 2. receipt-set disjointness against the published crosscheck -------
cross = json.loads(
    (OUT / 'class2-lane-warm-multiband2-duplicate-crosscheck-20261115.json').read_text())
mb2_roots = {r['root_hex'] for r in records_mb2}
assert len(mb2_roots) == 31
certdoc = json.loads((OUT / 'class2-lane-cost68d-win7-certificates-20261115.json').read_text())
hygdoc = json.loads((OUT / 'class2-lane-warm-band-hygiene-certificates-20261115.json').read_text())
certs = certdoc['certificates']
hyg = hygdoc['records']
own_roots = {r['root_hex'] for r in list(certs) + list(hyg)}
assert len(own_roots) == 12, ('7 cost-68d roots + 5 distinct hygiene roots '
                             '(71b bit-1 and 61d bit-22 share one root)')
assert not (mb2_roots & own_roots), 'the merged receipt sets must be disjoint'
cs = cross['summary']
assert cs['win_loss_conflicts'] == 0 and cs['byte_exact_all'] is True
print('CONTROL receipt-set disjointness asserted: 31 batch-2 roots vs 12 distinct '
      f"cost-68d/hygiene roots, intersection empty (published crosscheck: "
      f"{cs['roots_checked']} roots checked, {cs['remote_entries_checked']} remote "
      f"entries, 0 WIN/LOSS conflicts)")

PARENT = '00000000000000809102000000000000'
CHILD = '00000000000000809122000000000000'

# ------- 3. re-derive the cost-68d child membership at the 1140 state -------
parent_rows = rem2.get(PARENT, [])
child_hexes_remaining = {r['s6_hex'] for r in parent_rows}
child_still_remaining = CHILD in child_hexes_remaining
child_in_solved = int(CHILD, 16) in s2
assert child_still_remaining is True, (
    'cost-68d child expected to still be remaining at the 1140 merged state')
assert child_in_solved is False
d = dem2[CHILD]
assert d['c1'] == 0 and d['c2'] == 2 and d['c4'] == 0
membership = {
    'child_hex': CHILD,
    'claimed_as': 'cheapest remaining unswept child of the third class-2 coverable '
                  'target S5 (claim at the 1109 state, commit 6175d233; swept by this '
                  'lane as the cost-68d sweep)',
    'still_in_parent_remaining_children_at_1140': True,
    'demand_at_1140': {'c1': 0, 'c2': 2, 'c4': 0},
    'note': 'the 31 batch-2 receipts never covered this child; it is genuinely '
            'still remaining at the 1140 state, and the 7 cost-68d WIN7 receipts '
            'folded below close it',
}
print('CONTROL cost-68d child membership re-derived at 1140: '
      'still_remaining=True, demand c2=2')

# ------- 4. assert the completed cost-68d sweep ------------------------------
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
print(f'CONTROL cost-68d sweep re-summed from raw batches: 68 candidates, '
      f'{tot_nodes} nodes, {len(win_from_raw)} WIN7')

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

# ------- 5. assert the 7 cost-68d + 6 hygiene records ------------------------
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

assert certdoc['child_hex'] == CHILD
assert certdoc['unknown_status'].startswith('11x11 empty board: UNKNOWN')
assert len(certs) == 7 and {c['bit'] for c in certs} == {18, 26, 29, 34, 47, 103, 108}
for c in certs:
    assert_record(c, 'class2-lane-cost68d', CHILD)
    assert c['v16_search_nodes'] == sweep['win7_root_nodes'][str(c['bit'])]
    assert 'loss=true' in c['v15_crosscheck_verdict'] and v15[c['bit']] > 0
    assert '0 hits' in c['root_absence_check']
print(f'CONTROL cost-68d records asserted: {len(certs)} receipts')

assert hygdoc['schema'] == 'class2-lane-warm-band-hygiene-certificates-v1'
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

# ------- 6. fold the 13 receipts over the 1140-grown union ------------------
s_cur = set(s2)
addition = []
for r in list(certs) + list(hyg):
    cov = covers(int(r['root_hex'], 16))
    marg = cov - s_cur
    marg_m = marg & manifest
    addition.append({
        'band': r.get('band', 'class2-lane-cost68d'), 'bit': r['bit'],
        'root_hex': r['root_hex'],
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    })
    s_cur |= marg
stX, remX, uniqX, demX = summary_state(s_cur)
assert s_cur >= s2, 'the merged solved set must extend the 1140 chain head'
print('MERGED after-multiband2 + cost-68d + hygiene:', json.dumps(stX, indent=1))

total_mim = sum(a['marginal_in_manifest'] for a in addition)
total_marg = sum(a['marginal'] for a in addition)
zero_mim = [f"{a['band']}-bit{a['bit']}" for a in addition if a['marginal_in_manifest'] == 0]
print(f'total marginal={total_marg} marginal_in_manifest={total_mim}; '
      f'zero-mim receipts: {zero_mim}')

# ------- 7. new ranking + records -------------------------------------------
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
    'schema': 'n11-class-frontier-merged-recompute-after-multiband2-68dhyg-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-warm-multiband2-recompute-20261115.json '
                     '(solved 1140 / unique remaining 6707 / sum 528979 / open '
                     '4977/392702)',
    'method': 'merged fold of the two divergent published forks of the 1109 '
              'after-warm-multiband chain head: this lane\'s cost-68d + warm band '
              'hygiene fold (class-frontier-cost68d-recompute-20261115.json, solved '
              '1117) and the concurrent lane\'s warm multiband 2 fold '
              '(class-frontier-warm-multiband2-recompute-20261115.json, solved 1140). '
              'The receipt sets are pairwise disjoint (published duplicate crosscheck: '
              '31 batch-2 roots vs the 13 cost-68d/hygiene roots, intersection empty, '
              'zero WIN/LOSS conflicts; the batch-2 selection explicitly deferred the '
              'hygiene bits 62a 1/89, 63a 11/109 and 61d bit-22 = 71b bit-1 and never '
              'touched the cost-68d band). This script reproduces the published 1140 '
              'chain head by runpy (asserted 1140/6707/528979/4977/392702, '
              'byte-identical output), re-derives the cost-68d child membership at the '
              '1140 state with string keys (genuinely still remaining, demand '
              'c1=0,c2=2,c4=0), re-sums the completed cost-68d sweep from the 9 '
              'published raw batches (68 candidates, 61,325,518 v16 nodes, 7 WIN7-D10 '
              '+ 61 REFUTED + 0 capped) with the node-exact determinism rerun and the '
              'v15 cross-engine anchors asserted, then folds the 13 receipts in the '
              'published record order, re-deriving every per-record marginal from the '
              'growing union that already contains the 31 batch-2 receipts. Each '
              'certificate was extracted with the repo-verbatim blind extractor '
              '(FBS=1<<20, fbt_drops=0) and independently verified with '
              'verify_win7_certificate_bigint_independent.mjs; remote bytes were '
              'verified byte-exact by git blob sha after landing. No sweep claims are '
              'made here beyond the published cost-68d sweep record - receipts only',
    'controls': {
        'after_warm_multiband2_baseline': {
            'solved_in_manifest': 1140, 'unique_remaining': 6707,
            'sum_cost': 528979, 'open_s6': 4977, 'open_cost': 392702,
            'reproduced_byte_identical': True},
        'fork_disjointness': 'the 31 warm-multiband-2 roots and the 13 '
                             'cost-68d/hygiene roots are disjoint; the fold order '
                             '(batch-2 first, this lane\'s 13 second) cannot create '
                             'double coverage because every marginal is re-derived '
                             'from the growing union',
        'cost68d_child_membership_at_1140': membership,
        'cost68d_sweep_resummed_from_raw': True,
        'determinism_rerun_node_exact': True,
        'v15_anchors': '7 WIN7 loss=true + refuted anchors 0/120/13 loss=false',
        'records_folded_in_published_record_order': True,
        'extends_after_warm_multiband2_baseline': True,
    },
    'merged_addition': {
        'cost68d': addition[:7],
        'hygiene': addition[7:],
    },
    'totals': {
        'receipts': len(addition),
        'total_marginal': total_marg,
        'total_marginal_in_manifest': total_mim,
        'zero_marginal_in_manifest': zero_mim,
        'cost68d_rows': sum(c['rows'] for c in certs),
        'cost68d_extraction_nodes': sum(c['extraction_nodes'] for c in certs),
        'hygiene_rows': sum(r['rows'] for r in hyg),
        'hygiene_extraction_nodes': sum(r['extraction_nodes'] for r in hyg),
    },
    'frontier_after_merged': {
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
        'parallel_lane_bands': 'cost-65h/67b/68c warm candidates and the in-flight '
                               'cost-65j sweep stay with the parallel lane, as do the '
                               'six gain-1 cost-70c warm candidates (parallel-lane band)',
        'warm_candidates_without_records': 'gain-0-in-manifest own-lane warm '
                                           'candidates deferred by the batch-2 '
                                           'selection (incl. cost-61d bit-8 and '
                                           'others); they advance no manifest orbit '
                                           'until the solved set changes',
        'note': 'the six gain-1 cost-70c warm candidates may now have non-zero '
                'marginal against this merged head; their fold belongs to the '
                'parallel lane (its band) or a later canonical recompute',
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps '
                            'prove only absence of WIN7-D10; WIN7 certificates prove a '
                            'win within depth 10 from the 7-stone root only; solved '
                            'counts measure manifest coverage, not the game-theoretic '
                            'value of the 11x11 empty board; 11x11 empty root / '
                            '{49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-merged-recompute-after-multiband2-68dhyg-20261115.json').write_text(
    json.dumps(result, indent=1) + '\n')
print('written class-frontier-merged-recompute-after-multiband2-68dhyg-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remX.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-merged-multiband2-68dhyg-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-merged-multiband2-68dhyg-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('second coverable class-2 candidate S5',
                         class2[2] if len(class2) > 2 else class2[1])):
        rows = remX.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = demX[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-merged-multiband2-68dhyg)')
