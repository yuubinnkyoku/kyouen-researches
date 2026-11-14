#!/usr/bin/env python3
"""Class-2/4 frontier recomputation adding the class2-lane cost-69e sweep
receipts on top of the merged warm+sweep frontier (2026-11-15).

Baseline (published main): class-frontier-merged-recompute-after65h65i-warm67b68c
-20261115.json (solved 1012 / unique remaining 6835 / sum 538670 / open
5105/402393), itself the single merged replay of the two parallel class2-lane
branches that forked at the after-cost-65h+65i frontier (chain A: 63e-warm +
65g-warm rebuilds; chain B: 67b + 68c child sweeps).

This script:
1. reproduces the merged baseline byte-exactly by runpy (asserting
   1012/6835/538670/5105/402393);
2. re-derives the cost-69e child's remaining membership and demand from the
   merged frontier and records the mid-flight manifest closure: the child
   00000000000000803202000000008000 was claimed (commit 41693097) as one of
   the two cheapest remaining unswept children of the second class-2 target
   (12 orbits / 864 after cost-68c, demand c1=0,c2=2,c4=0), but the parallel
   warm-merged recompute (commit a7f3fc97) closed it in the manifest mid-flight
   via the cost-65g-warm bit-15 receipt (root 00000000000000803202000000008004,
   the same 7-stone root this sweep independently re-derived as WIN7 bit 2);
   the sweep therefore completed on an already-receipt-closed child and its
   certificates are pure new-coverage additions;
3. asserts the completed cost-69e sweep (69 candidates: 11 WIN7-D10 + 58
   REFUTED, 0 capped, 80,172,332 v16 nodes; all 9 raw batches re-summed from
   the published JSONL; the v16 determinism rerun and the v15 cross-engine
   anchors on all 11 WIN7 bits are asserted from the published JSONL files);
4. adds the ten fully verified cost-69e receipts (bits 21/99/87/84/76/90 +
   the 2026-11-15 warm rebuilds 89/94/108/116) in the published record order,
   re-deriving every per-bit marginal from the growing union, and produces the
   after-cost-69e frontier + ranking CSV + top-candidates CSV.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the merged baseline (after merged-warm67b68c, 1012) ----------
nsM = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_merged_after65h65i_warm_67b68c_20261115.py'))
sM = nsM['sM']
stM = nsM['stM']
remM = nsM['remM']
demM = nsM['demM']
covers = nsM['covers']
summary_state = nsM['summary_state']
manifest = nsM['manifest']
classes = nsM['classes']
assert stM['solved_s6_in_manifest'] == 1012 and stM['unique_remaining_s6'] == 6835
assert stM['sum_remaining_cost'] == 538670
assert stM['s6_needed_by_open_classes'] == 5105 and stM['cost_needed_by_open_classes'] == 402393
print('CONTROL merged baseline reproduced: 1012/6835/538670/5105/402393')

PARENT = '00000000000000803202000000000000'
CHILD = '00000000000000803202000000008000'

# ---------- 2. re-derive the child's remaining membership and demand ----------
parent_rows_after_merged = remM.get(int(PARENT, 16), [])
child_still_remaining = any(r['s6_hex'] == CHILD for r in parent_rows_after_merged)
child_demand_after_merged = demM.get(int(CHILD, 16))
membership = {
    'child_hex': CHILD,
    'claimed_as': 'one of the two cheapest remaining unswept children of the second class-2 target '
                  '(12 orbits / 864 after cost-68c, demand c1=0,c2=2,c4=0; claim commit 41693097)',
    'still_in_parent_remaining_children_after_merged': child_still_remaining,
    'demand_after_merged': child_demand_after_merged,
    'midflight_manifest_closure': 'the parallel warm-merged recompute (commit a7f3fc97) closed this '
                                  'child in the manifest via the cost-65g-warm bit-15 receipt '
                                  '(root 00000000000000803202000000008004, the same 7-stone root this '
                                  'sweep independently re-derived as WIN7 bit 2); the sweep completed '
                                  'on an already-receipt-closed child; its certificates are pure '
                                  'new-coverage additions',
}
assert child_still_remaining is False, 'child expected to be closed in the merged manifest'
assert int(CHILD, 16) not in {int(r['s6_hex'], 16) for r in parent_rows_after_merged}
print(f'CONTROL child membership re-derived: still_remaining={child_still_remaining} '
      f'(mid-flight manifest closure confirmed)')

# ---------- 3. assert the completed cost-69e sweep ----------
sweep = json.loads((OUT / 'class2-lane-cost69e-sweep-20261114.json').read_text())
assert sweep['s6_child_hex'] == CHILD
assert sweep['s6_s7_edge_cost'] == 69
assert sweep['win7_d10'] == 11 and sweep['refuted_d10'] == 58 and sweep['capped'] == 0
assert sweep['total_nodes'] == 80172332
assert sweep['win7_bits'] == [2, 21, 76, 84, 87, 89, 90, 94, 99, 108, 116]

# re-sum the published raw batches
tot_nodes = 0
seen_bits = set()
win_from_raw = set()
n_pilot = 0
for i in range(1, 10):
    for line in (OUT / f'class2-lane-cost69e-raw-batch{i}-20261114.jsonl').read_text().splitlines():
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
assert n_pilot == 9 and len(seen_bits) == 69 and tot_nodes == 80172332
assert win_from_raw == {2, 21, 76, 84, 87, 89, 90, 94, 99, 108, 116}
print('CONTROL cost-69e sweep asserted from published raw batches: '
      '69 candidates, 9 pilots, 11 WIN7 + 58 REFUTED, 80,172,332 nodes')

# determinism rerun control
det = [json.loads(l) for l in (OUT / 'class2-lane-cost69e-v16-determinism-rerun-20261114.jsonl')
       .read_text().splitlines() if l.strip()]
det_bits = {r['bit']: r for r in det if 'bit' in r}
assert det_bits[116]['nodes'] == 6683450 and det_bits[116]['loss'] is True
assert det_bits[44]['nodes'] == 5674763 and det_bits[44]['loss'] is False

# v15 cross-engine anchors control
v15 = [json.loads(l) for l in (OUT / 'class2-lane-cost69e-v15-crosscheck-20261114.jsonl')
       .read_text().splitlines() if l.strip()]
v15_pilot = [r for r in v15 if 'control' in r]
assert all(r['loss'] is False and r['nodes'] == 5949 for r in v15_pilot)
v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
v15_expect = {21: 1131809, 99: 1746232, 87: 4764589, 84: 9765935, 2: 5510814,
              76: 5109539, 90: 6478505, 108: 5747330, 89: 5599058, 94: 6171899,
              116: 16776783}
assert set(v15_bits) == set(v15_expect)
for b, n in v15_expect.items():
    assert v15_bits[b]['loss'] is True and v15_bits[b]['nodes'] == n, (b, v15_bits[b]['nodes'])
print('CONTROL determinism rerun (116/44 node-exact) and v15 anchors '
      '(all 11 WIN7 bits loss=true) asserted')

# ---------- 4. the ten verified receipts, marginals from the growing union ----------
certs_rec = json.loads((OUT / 'class2-lane-cost69e-win7-certificates-20261114.json').read_text())
assert certs_rec['child_hex'] == CHILD
certs = [c for c in certs_rec['certificates'] if c.get('verdict') == 'WIN7']
assert [c['bit'] for c in certs] == [21, 99, 87, 84, 76, 90, 89, 94, 108, 116]
ROWS = {21: 22261, 99: 25149, 87: 43838, 84: 29614, 76: 45665, 90: 46959,
       89: 47035, 94: 42538, 108: 33942, 116: 74113}
SUBS = {21: 45, 99: 50, 87: 59, 84: 50, 76: 57, 90: 58,
        89: 54, 94: 52, 108: 51, 116: 59}
MD5 = {21: 'b229fe7c0c96901fe04ddf05763ffb9e',
       99: '69f5fae13d3c712df7b2883ec79d7c2a',
       87: '5f5063233ff919b704e01a105e1fb132',
       84: '41adac3c1d684d4b4dde25c416c2ae20',
       76: '2358870d7a2625b4d40a0c178f8cba66',
       90: 'b0e6f779b229ef4993c8715691db7ede',
       89: '1e2c8db6cd9303fcf0167f59ccb83bae',
       94: '4dc6076b96edc3a472b4b23f38739451',
       108: '74d071466140e1b0a48b67134431a570',
       116: '691140486067132237d8c11d93a12559'}
# bit-116 md5 is the uncompressed certificate md5 (file published as base64
# (76 cols) of gzip -9; the records file pins uncompressed md5/sha256 and the
# gz_b64 md5), so the records-field assert holds unchanged.
child_v = int(CHILD, 16)
group_covers = {}
for c in certs:
    assert c['rows'] == ROWS[c['bit']] and c['sub_roots_pass'] == SUBS[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['md5'] == MD5[c['bit']]
    assert int(c['root_hex'], 16) == child_v | (1 << c['bit'])
    group_covers[c['bit']] = covers(int(c['root_hex'], 16))
print('CONTROL cost-69e receipts asserted: bits 21/99/87/84/76/90/89/94/108/116 '
      '(rows/sub-roots/union/md5/roots; 116 md5 = uncompressed, file published as base64(gzip))')

s_cur = set(sM)
cost69e_addition = {}
for bit in (21, 99, 87, 84, 76, 90, 89, 94, 108, 116):
    cov = group_covers[bit]
    marg = cov - s_cur
    marg_m = marg & manifest
    cost69e_addition[str(bit)] = {
        'root_hex': format(child_v | (1 << bit), '032x'),
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    s_cur |= marg
st69, rem69, uniq69, dem69 = summary_state(s_cur)
assert s_cur >= sM, 'the after-cost-69e solved set must extend the merged baseline'
print('AFTER cost-69e:', json.dumps(st69, indent=1))

# ---------- 5. new ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem69, 2)
class4 = best(rem69, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost69e-recompute-20261115-v2',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-merged-recompute-after65h65i-warm67b68c-20261115 '
                     '(solved 1012 / unique remaining 6835 / sum 538670 / open 5105/402393)',
    'method': 'direct runpy extension of recompute_frontier_merged_after65h65i_warm_67b68c_20261115.py: '
              'the merged baseline is reproduced exactly (asserted 1012/6835/538670/5105/402393), the '
              'cost-69e child remaining-membership and demand are re-derived from the merged frontier '
              '(the child was closed in the manifest mid-flight by the parallel cost-65g-warm bit-15 '
              'receipt; the sweep completed on an already-receipt-closed child and its certificates are '
              'pure new-coverage additions), the completed cost-69e sweep is asserted from the published '
              'raw batches (69 candidates: 11 WIN7-D10 + 58 REFUTED, 0 capped, 80,172,332 v16 nodes; '
              '9 pilot d6 controls; determinism rerun bits 116/44 node-exact; v15 cross-engine anchors '
              'on all 11 WIN7 bits loss=true at 1,131,809/1,746,232/4,764,589/9,765,935/5,510,814/'
              '5,109,539/6,478,505/5,747,330/5,599,058/6,171,899/16,776,783 nodes), and the ten fully '
              'verified receipts (bits 21/99/87/84/76/90 plus the 2026-11-15 warm rebuilds '
              '89/94/108/116; rows 22,261/25,149/43,838/29,614/45,665/46,959/47,035/42,538/33,942/'
              '74,113; sub-roots 45/50/59/50/57/58/54/52/51/59 PASS; union 0/0 each; bit-116 '
              'published as base64(gzip -9) with records-pinned uncompressed md5/sha256) are added '
              'in the published record order with per-bit marginals re-derived from the growing '
              'union; the bit-21 WIN7 root 00000000000000803202000000208000 is a '
              'cross-child duplicate of the cost-60b bit-15 win7_roots listing with no prior published '
              'certificate, so that receipt is new coverage and also closes the cost-60b bit-15 warm '
              'entry; the bit-2 WIN7 root duplicates the cost-65g-warm bit-15 certificate (cross-lane '
              'reproduction, no new certificate needed); each of the four warm-rebuilt bits '
              '89/94/108/116 closes exactly one additional manifest S6 orbit (marginal 5, '
              'in-manifest 1 each), advancing solved 1019->1023 / remaining 6,828->6,824 / '
              'sum 538,143->537,833 / open 5,098->5,094 / 401,866->401,556 over the six-receipt '
              'publication',
    'controls': {
        'merged_baseline': {'solved_in_manifest': 1012, 'unique_remaining': 6835,
                            'sum_cost': 538670, 'open_s6': 5105, 'open_cost': 402393,
                            'reproduced': True},
        'child_membership_reproduced': True,
        'sweep_asserted_from_raw_batches': True,
        'extends_merged_baseline': True,
    },
    'child_membership': membership,
    'cost69e_addition': cost69e_addition,
    'frontier_after_cost69e': {
        'solved_s6_in_manifest': st69['solved_s6_in_manifest'],
        'remaining_s5_orbits': st69['remaining_s5_orbits'],
        'unique_remaining_s6': st69['unique_remaining_s6'],
        'sum_remaining_cost': st69['sum_remaining_cost'],
        's6_needed_by_open_classes': st69['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st69['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st69['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'best_class2 and best_coverable_class2 are the same coverable S5; '
                            'the separate receipt-unclosable S5 is recorded in receipt_unclosable_class2.',
        'receipt_unclosable_class2': {
            's5_hex': '00000000000000809082000000000000',
            'classes': classes.get('00000000000000809082000000000000', 0),
            'remaining_s6_orbits': len(rem69.get('00000000000000809082000000000000', [])),
            'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rem69.get('00000000000000809082000000000000', [])),
            'all_remaining_children_sterile_swept': True,
            'status': 'unresolved; no WIN7-D10 was found in the recorded sweeps',
        },
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only '
                            'absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from '
                            'the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / '
                            'class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost69e-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost69e-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem69.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost69e-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
assert all(isinstance(k, str) for k in rem69), 'summary_state S5 keys must be hex strings'
assert b2 in rem69 and len(rem69[b2]) == 10, 'receipt-unclosable S5 must retain its 10 children'
assert PARENT in rem69 and len(rem69[PARENT]) == 6, 'cost-69e parent must retain six children'
with (OUT / 'class-frontier-top-candidates-s6-after-cost69e-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem69.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem69.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-69e parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == PARENT))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem69[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem69[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost69e)')
