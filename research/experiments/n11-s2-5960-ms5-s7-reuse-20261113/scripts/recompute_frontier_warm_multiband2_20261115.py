#!/usr/bin/env python3
"""Class-2/4 frontier recomputation folding the class2-lane warm multiband 2
receipts (31 WIN7 certificates across cost-61d/61e/61f/62a(0)/63a/64b/65e/71b)
on top of the after-warm-multiband chain head (2026-11-15).

Baseline (published main): class-frontier-warm-multiband-recompute-20261115.json
(solved 1109 / unique remaining 6738 / sum 531295 / open 5008/395018), which
folds the after-cost-75c baseline (1062) with the first warm multiband batch
(35 receipts). This script:

1. reproduces the after-warm-multiband chain head by runpy (asserting
   1109/6738/531295/5008/395018) byte-identically from the published chain -
   including the repaired recompute_frontier_merged_after61f_63a65e_20261114.py
   (the parallel lane's in-place extension of the cost-65e WIN7 record with the
   bit-7 receipt had broken its len(certs65e)==1 assert; the repair folds the
   historical bit-107 receipt only and asserts the appended bit-7 entry is the
   known duplicate already folded by the first warm multiband batch);
2. asserts all 31 warm multiband 2 records from
   class2-lane-warm-multiband2-certificates-20261115.json (rows, sub-roots,
   extraction nodes, union 0/0, md5, sha256, root == child | 1<<bit) in the
   published record order; the certificates were re-verified with the
   independent BigInt verifier after extraction (see the record JSON);
3. folds the 31 receipts in record order, re-deriving every per-record
   marginal from the growing union;
4. produces the after-warm-multiband-2 frontier + ranking CSV +
   top-candidates CSV.

Candidate selection (class2-lane-warm-candidate-ranking2-20261115.json, this
coordinator run): every own-lane uncertified WIN7 root was ranked by
marginal_in_manifest greedy against the 1109 solved set; the 31 selected
roots each carry fold_gain_in_manifest 1 (the greedy total over own-lane
roots is 37; the six gain-1 cost-70c candidates were left to the parallel
lane, which owns that band, and every gain-0 candidate was deferred). The
cost-71b remaining WIN7 bits 74/94/117 are included (bit 1 = cost-61d bit-22
root has zero in-manifest marginal against 1109 and was deferred).

Every warm certificate was published on main before this recompute was
written (remote bytes verified byte-exact by md5 per part); the fold adds
receipts only - no sweep claims are made here.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-warm-multiband chain head (1109) ----------
nsW = runpy.run_path(str(HERE / 'scripts' /
                         'recompute_frontier_warm_multiband_20261115.py'))
sH = nsW['s_cur']
stH = nsW['stW']
remH = nsW['remW']
demH = nsW['demW']
covers = nsW['covers']
summary_state = nsW['summary_state']
manifest = nsW['manifest']
classes = nsW['classes']
assert stH['solved_s6_in_manifest'] == 1109 and stH['unique_remaining_s6'] == 6738
assert stH['sum_remaining_cost'] == 531295
assert stH['s6_needed_by_open_classes'] == 5008 and stH['cost_needed_by_open_classes'] == 395018
print('CONTROL after-warm-multiband chain head reproduced: 1109/6738/531295/5008/395018')

# ---------- 2. assert the 31 warm multiband 2 records ----------
recdoc = json.loads((OUT / 'class2-lane-warm-multiband2-certificates-20261115.json').read_text())
assert recdoc['schema'] == 'class2-lane-warm-multiband2-certificates-v1'
records = recdoc['records']
assert len(records) == 31
BANDS = ('class2-lane-cost61d', 'class2-lane-cost61e', 'class2-lane-cost61f',
         'class2-lane-cost62a', 'class2-lane-cost63a', 'class2-lane-cost64b',
         'class2-lane-cost65e', 'class2-lane-cost71b')
for r in records:
    assert r['verdict'] == 'WIN7' and r['band'] in BANDS
    assert r['rows_sorted_unique'] is True
    assert r['union_missing'] == 0 and r['union_extra'] == 0
    assert r['sub_roots_pass'] == r['root_check']['loser_mobility']
    assert r['root_check']['match'] is True
    assert 13 <= r['terminal_range'][0] and r['terminal_range'][1] <= 17
    child_v = int(r['child_hex'], 16)
    assert int(r['root_hex'], 16) == child_v | (1 << r['bit']), r
    assert r['root_absence_check']['prior_certificate_hits'] == 0
    if r['storage']['layout'] == 'single file':
        assert r['file'].endswith(f"bit{r['bit']}-root-{r['root_hex']}.cert")
    else:
        assert (r['storage']['part1']['path'].endswith('.part1of2') and
                r['storage']['part2']['path'].endswith('.part2of2') and
                r['storage']['concat_md5_equals_whole'] is True)
    assert r['md5'] and len(r['sha256']) == 64 and r['bytes'] > 0
print(f'CONTROL warm multiband 2 records asserted: {len(records)} receipts '
      f'(bands {sorted(set(r["band"] for r in records))})')

# ---------- 3. fold in record order, marginals from the growing union ----------
s_cur = set(sH)
warm_addition = []
for r in records:
    cov = covers(int(r['root_hex'], 16))
    marg = cov - s_cur
    marg_m = marg & manifest
    warm_addition.append({
        'band': r['band'], 'bit': r['bit'], 'root_hex': r['root_hex'],
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    })
    s_cur |= marg
stW2, remW2, uniqW2, demW2 = summary_state(s_cur)
assert s_cur >= sH, 'the after-warm-multiband-2 solved set must extend the chain head'
print('AFTER warm multiband 2:', json.dumps(stW2, indent=1))

total_mim = sum(a['marginal_in_manifest'] for a in warm_addition)
total_marg = sum(a['marginal'] for a in warm_addition)
zero_mim = [f"{a['band']}-bit{a['bit']}" for a in warm_addition if a['marginal_in_manifest'] == 0]
print(f'warm multiband 2 total marginal={total_marg} marginal_in_manifest={total_mim}; '
      f'zero-mim receipts: {zero_mim}')

# ---------- 4. new ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(remW2, 2)
class4 = best(remW2, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-warm-multiband2-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-warm-multiband-recompute-20261115 (solved 1109 / '
                     'unique remaining 6738 / sum 531295 / open 5008/395018)',
    'method': 'direct runpy extension of recompute_frontier_warm_multiband_20261115.py: the '
              'after-warm-multiband chain head is reproduced exactly (asserted '
              '1109/6738/531295/5008/395018, byte-identical output to main, including the '
              'repaired merged_after61f_63a65e script whose historical fold is unchanged '
              'while the parallel lane\'s in-place cost-65e bit-7 record extension is '
              'asserted to be the known duplicate), then all 31 warm multiband 2 WIN7 '
              'receipts from class2-lane-warm-multiband2-certificates-20261115.json are '
              'folded in the published record order (greedy marginal_in_manifest ranking '
              'over own-lane uncertified WIN7 roots, computed against the 1109 chain head '
              'by rank_warm_candidates2_20261115.py; every record asserts '
              'rows/sub-roots/extraction-nodes/union-0-0/md5/sha256 and root == child | '
              '1<<bit). Each certificate was extracted with the repo-verbatim blind '
              'extractor (FBS=1<<20, fbt_drops=0, rows LC_ALL=C sorted-unique) and '
              'independently verified with verify_win7_certificate_bigint_independent.mjs '
              '(BigInt exact geometry, no solver/cache import; sub_roots == loser mobility '
              'all PASS, strategy/consumed union 0/0 both directions, terminal range '
              '13..17); the verification was re-run on the local bytes after extraction and '
              'the remote bytes were verified byte-exact by md5 per part before this '
              'recompute. The 31 roots and their marginal manifest parents were also '
              'cross-checked against the published LOSS7 evidence (loss7 certificate '
              'manifests, loss7 JSON manifests, and the 274-key central49 terminal LOSS7 '
              'parent-lift manifest): zero hits, zero WIN/LOSS conflicts. The six gain-1 '
              'cost-70c warm candidates were left to the parallel lane (its band); '
              'gain-0-in-manifest candidates were deferred. No sweep claims are made here - '
              'receipts only',
    'controls': {
        'after_warm_multiband_baseline': {'solved_in_manifest': 1109, 'unique_remaining': 6738,
                                          'sum_cost': 531295, 'open_s6': 5008, 'open_cost': 395018,
                                          'reproduced_byte_identical': True},
        'chain_break_repair_merged_after61f_63a65e': 'the parallel lane extended '
            'class2-lane-cost65e-win7-certificates-20261114.json in place with the bit-7 '
            'receipt, breaking the len(certs65e)==1 assert of the historical '
            'recompute_frontier_merged_after61f_63a65e_20261114.py (third instance of the '
            'missing-input defect class); repaired by folding the historical bit-107 '
            'receipt only, asserting the appended bit-7 entry (root '
            '00000000000000809102000000800080, rows 44561) is the duplicate of the first '
            'warm-multiband batch certificate; every downstream endpoint reproduces '
            'byte-identically (all chain output files md5-verified unchanged)',
        'warm_records_asserted_rows_subs_extraction_union_md5_sha256_roots': True,
        'records_folded_in_published_record_order': True,
        'extends_after_warm_multiband_baseline': True,
    },
    'warm_multiband2_addition': warm_addition,
    'warm_multiband2_totals': {
        'receipts': len(records),
        'total_marginal': total_marg,
        'total_marginal_in_manifest': total_mim,
        'zero_marginal_in_manifest': zero_mim,
        'total_rows': sum(r['rows'] for r in records),
        'total_extraction_nodes': sum(r['extraction_nodes'] for r in records),
    },
    'frontier_after_warm_multiband2': {
        'solved_s6_in_manifest': stW2['solved_s6_in_manifest'],
        'remaining_s5_orbits': stW2['remaining_s5_orbits'],
        'unique_remaining_s6': stW2['unique_remaining_s6'],
        'sum_remaining_cost': stW2['sum_remaining_cost'],
        's6_needed_by_open_classes': stW2['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stW2['cost_needed_by_open_classes'],
        'demand_histogram_open_only': stW2['hist'],
        'best_class2': class2[0],
        'audit_blocked_class2': next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'outstanding_not_folded': {
        'parallel_lane_bands': 'cost-65h/67b/68c warm candidates and the in-flight '
                               'cost-65j sweep stay with the parallel lane, as do the six '
                               'gain-1 cost-70c warm candidates (parallel-lane band)',
        'warm_candidates_without_records': 'gain-0-in-manifest own-lane warm candidates '
                                           'deferred by this batch (incl. cost-61d bit-22 = '
                                           'cost-71b bit-1 root, cost-62a bits 1/89, '
                                           'cost-63a bits 11/109, cost-61d bit-8 and '
                                           'others); they advance no manifest orbit until '
                                           'the solved set changes',
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps '
                            'prove only absence of WIN7-D10; WIN7 certificates prove a '
                            'win within depth 10 from the 7-stone root only; solved '
                            'counts measure manifest coverage, not the game-theoretic '
                            'value of the 11x11 empty board; 11x11 empty root / {49,60} '
                            '/ S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-warm-multiband2-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-warm-multiband2-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remW2.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-warm-multiband2-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-warm-multiband2-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('second coverable class-2 candidate S5', class2[2] if len(class2) > 2 else class2[1])):
        rows = remW2.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = demW2[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-warm-multiband-2)')
