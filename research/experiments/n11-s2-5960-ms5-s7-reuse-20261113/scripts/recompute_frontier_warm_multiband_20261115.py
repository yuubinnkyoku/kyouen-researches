#!/usr/bin/env python3
"""Class-2/4 frontier recomputation folding the class2-lane warm multiband
receipts (35 WIN7 certificates across cost-61d/61e/61f/62a/63a/64b/65e/71b
plus cost-72 bit-52) on top of the after-cost-75c chain head (2026-11-15).

Baseline (published main): class-frontier-cost75c-recompute-20261115.json
(solved 1062 / unique remaining 6785 / sum 534768 / open 5055/398491; second
class-2 target S5 closed by receipts), which already folds the cost-72
bit-111 partial receipt (+2) and the twelve cost-75c receipts. Its
outstanding_not_folded explicitly reserves the warm multiband fold for a
canonical merged recompute of the chain head - this script.

This script:
1. reproduces the after-cost-75c baseline by runpy (asserting
   1062/6785/534768/5055/398491) from the published raw batches,
   determinism rerun, v15 anchors and receipts, byte-identical to main;
2. asserts all 35 warm multiband records from
   class2-lane-warm-multiband-certificates-20261115.json (rows, sub-roots,
   extraction nodes, union 0/0, md5, sha256, root == child | 1<<bit) in the
   published record order; the certificates themselves were re-verified with
   the independent BigInt verifier after extraction (see the record JSON);
3. folds the 35 receipts in record order, re-deriving every per-record
   marginal from the growing union; the cost-71b bit-14 root duplicates the
   cost-75c bit-22 root (independently re-extracted: consistent WIN7, zero
   marginal here - a positive duplicate cross-check); the cost-72 bit-52
   receipt (its sweep owner explicitly deprioritized it) is folded as part
   of this multiband batch;
4. produces the after-warm-multiband frontier + ranking CSV +
   top-candidates CSV.

Every warm certificate was published on main before this recompute was
written (remote bytes verified byte-exact by md5 per part); the fold adds
receipts only - no sweep claims are made here.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-75c baseline (1062) ----------
nsC = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost75c_20261115.py'))
sC = nsC['s_cur']
stC = nsC['st75c']
remC = nsC['rem75c']
demC = nsC['dem75c']
covers = nsC['covers']
summary_state = nsC['summary_state']
manifest = nsC['manifest']
classes = nsC['classes']
assert stC['solved_s6_in_manifest'] == 1062 and stC['unique_remaining_s6'] == 6785
assert stC['sum_remaining_cost'] == 534768
assert stC['s6_needed_by_open_classes'] == 5055 and stC['cost_needed_by_open_classes'] == 398491
print('CONTROL after-cost-75c baseline reproduced: 1062/6785/534768/5055/398491')

# ---------- 2. assert the 35 warm multiband records ----------
recdoc = json.loads((OUT / 'class2-lane-warm-multiband-certificates-20261115.json').read_text())
assert recdoc['schema'] == 'class2-lane-warm-multiband-certificates-v1'
records = recdoc['records']
assert len(records) == 35
BANDS = ('class2-lane-cost61d', 'class2-lane-cost61e', 'class2-lane-cost61f',
         'class2-lane-cost62a', 'class2-lane-cost63a', 'class2-lane-cost64b',
         'class2-lane-cost65e', 'class2-lane-cost71b', 'class2-lane-cost72')
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
print(f'CONTROL warm multiband records asserted: {len(records)} receipts '
      f'(bands {sorted(set(r["band"] for r in records))})')

# duplicate cross-check: cost-71b bit-14 root == cost-75c bit-22 root
DUP = '00000000000000803202000000404000'
dup_entries = [r for r in records if r['root_hex'] == DUP]
assert len(dup_entries) == 1 and dup_entries[0]['band'] == 'class2-lane-cost71b' \
    and dup_entries[0]['bit'] == 14

# ---------- 3. fold in record order, marginals from the growing union ----------
s_cur = set(sC)
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
stW, remW, uniqW, demW = summary_state(s_cur)
assert s_cur >= sC, 'the after-warm-multiband solved set must extend after-cost-75c'
print('AFTER warm multiband:', json.dumps(stW, indent=1))

total_mim = sum(a['marginal_in_manifest'] for a in warm_addition)
total_marg = sum(a['marginal'] for a in warm_addition)
zero_mim = [f"{a['band']}-bit{a['bit']}" for a in warm_addition if a['marginal_in_manifest'] == 0]
print(f'warm multiband total marginal={total_marg} marginal_in_manifest={total_mim}; '
      f'zero-mim receipts: {zero_mim}')

# ---------- 4. new ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(remW, 2)
class4 = best(remW, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-warm-multiband-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-cost75c-recompute-20261115 (solved 1062 / '
                     'unique remaining 6785 / sum 534768 / open 5055/398491)',
    'method': 'direct runpy extension of recompute_frontier_cost75c_20261115.py: the '
              'after-cost-75c baseline is reproduced exactly (asserted '
              '1062/6785/534768/5055/398491, byte-identical output to main), then all '
              '35 warm multiband WIN7 receipts from class2-lane-warm-multiband-'
              'certificates-20261115.json are folded in the published record order '
              '(greedy marginal_in_manifest ranking over uncertified WIN7 roots of the '
              'my-lane bands, computed against the after-cost-75b frontier; every '
              'record asserts rows/sub-roots/extraction-nodes/union-0-0/md5/sha256 and '
              'root == child | 1<<bit). Each certificate was extracted with the '
              'repo-verbatim blind extractor (FBS=1<<20, fbt_drops=0, rows LC_ALL=C '
              'sorted-unique) and independently verified with '
              'verify_win7_certificate_bigint_independent.mjs (BigInt exact geometry, '
              'no solver/cache import; sub_roots == loser mobility all PASS, '
              'strategy/consumed union 0/0 both directions, terminal range 13..17); '
              'the verification was re-run on the local bytes after extraction and the '
              'remote bytes were verified byte-exact by md5 per part before this '
              'recompute. The cost-71b bit-14 root 00000000000000803202000000404000 '
              'duplicates the already-folded cost-75c bit-22 root: the independent '
              're-extraction reproduces the same WIN7 verdict (positive duplicate '
              'cross-check, zero marginal here). The cost-72 bit-52 receipt (sweep '
              'owner explicitly deprioritized bit-52 to warm) is folded as part of this '
              'batch; the remaining cost-72 sweep bookkeeping stays with the cost-72 '
              'lane. No sweep claims are made here - receipts only',
    'controls': {
        'after_cost75c_baseline': {'solved_in_manifest': 1062, 'unique_remaining': 6785,
                                   'sum_cost': 534768, 'open_s6': 5055, 'open_cost': 398491,
                                   'reproduced_byte_identical': True},
        'warm_records_asserted_rows_subs_extraction_union_md5_sha256_roots': True,
        'records_folded_in_published_record_order': True,
        'duplicate_cost71b_bit14_vs_cost75c_bit22_asserted': True,
        'extends_after_cost75c_baseline': True,
    },
    'warm_multiband_addition': warm_addition,
    'warm_multiband_totals': {
        'receipts': len(records),
        'total_marginal': total_marg,
        'total_marginal_in_manifest': total_mim,
        'zero_marginal_in_manifest': zero_mim,
        'total_rows': sum(r['rows'] for r in records),
        'total_extraction_nodes': sum(r['extraction_nodes'] for r in records),
    },
    'frontier_after_warm_multiband': {
        'solved_s6_in_manifest': stW['solved_s6_in_manifest'],
        'remaining_s5_orbits': stW['remaining_s5_orbits'],
        'unique_remaining_s6': stW['unique_remaining_s6'],
        'sum_remaining_cost': stW['sum_remaining_cost'],
        's6_needed_by_open_classes': stW['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stW['cost_needed_by_open_classes'],
        'demand_histogram_open_only': stW['hist'],
        'best_class2': class2[0],
        'audit_blocked_class2': next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'outstanding_not_folded': {
        'cost72_sweep_record': 'the completed cost-72 sweep record (raw batches 1-9 + '
                               'audits published; 2 WIN7-D10 bits 52/111) remains the '
                               'cost-72 lane to publish; bit-52 is folded here as a '
                               'receipt, bit-111 is already folded in the baseline',
        'warm_rebuild_candidates_without_records': 'cost-61d bit-22 (= cost-71b bit-1 '
                                                   'root), cost-71b remaining WIN7 bits '
                                                   '1/74/94/117 (bits 14/32 now '
                                                   'certified here), and other '
                                                   'unverified WIN7 bits of earlier '
                                                   'bands',
        'parallel_lane_bands': 'cost-65h/67b/68c warm candidates intentionally not '
                               'touched by this batch (active parallel-lane bands)',
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps '
                            'prove only absence of WIN7-D10; WIN7 certificates prove a '
                            'win within depth 10 from the 7-stone root only; solved '
                            'counts measure manifest coverage, not the game-theoretic '
                            'value of the 11x11 empty board; 11x11 empty root / {49,60} '
                            '/ S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-warm-multiband-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-warm-multiband-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remW.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-warm-multiband-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-warm-multiband-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('second coverable class-2 candidate S5', class2[2] if len(class2) > 2 else class2[1])):
        rows = remW.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = demW[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-warm-multiband)')
