#!/usr/bin/env python3
"""Class-2/4 frontier recomputation adding the class2-lane cost-75b sweep
receipts on top of the after-merged (cost-60bwarm + cost-71b) frontier
(2026-11-15).

Baseline (published main): class-frontier-merged-cost60bwarm-cost71b-
recompute-20261115.json (solved 1045 / unique remaining 6802 / sum 536131 /
open 5072/399854), the canonical chain head repaired after the cost-69e v2
chain break.

This script:
1. reproduces the after-merged baseline by runpy (asserting
   1045/6802/536131/5072/399854);
2. re-derives the cost-75b child's remaining membership with string keys
   (the child 00000000000000803202000000000008 was claimed at commit 8cba4498
   as one of the three remaining unswept children of the second class-2
   target, parent at 3 remaining orbits / cost 222, demand c1=0,c2=2,c4=0;
   it was genuinely still remaining when swept - no mid-flight closure);
3. asserts the completed cost-75b sweep (75 candidates: 7 WIN7-D10 + 68
   REFUTED, 0 capped, 139,705,045 v16 nodes; all 10 raw batches re-summed
   from the published JSONL; determinism rerun bits 7/86/116 node-exact and
   the v15 cross-engine anchors on all 7 WIN7 bits asserted from the
   published JSONL);
4. asserts all seven fully verified cost-75b receipts (bits
   7/51/54/84/89/99/116) in the published record order, re-deriving every
   per-bit marginal from the growing union, and produces the after-cost-75b
   frontier + ranking CSV + top-candidates CSV. The bit-54 root duplicates
   the cost-70c bit-3 win7_roots listing (uncertified there), so this is the
   first published certificate for that root and it also closes the
   cost-70c bit-3 warm entry;
5. records the parent's remaining children after the additions (expected:
   the parallel-lane cost-72 child 00000000000000803202000000000200 and the
   sibling cost-75 child 00000000000000803202000000004000).
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-merged baseline (1045) ----------
nsM = runpy.run_path(str(HERE / 'scripts' /
                         'recompute_frontier_merged_after69ev2_70c_60bwarm_71b_20261115.py'))
sM = nsM['s_cur']
stM = nsM['stF']
remM = nsM['remF']
demM = nsM['demF']
covers = nsM['covers']
summary_state = nsM['summary_state']
manifest = nsM['manifest']
classes = nsM['classes']
assert stM['solved_s6_in_manifest'] == 1045 and stM['unique_remaining_s6'] == 6802
assert stM['sum_remaining_cost'] == 536131
assert stM['s6_needed_by_open_classes'] == 5072 and stM['cost_needed_by_open_classes'] == 399854
print('CONTROL after-merged baseline reproduced: 1045/6802/536131/5072/399854')

PARENT = '00000000000000803202000000000000'
CHILD = '00000000000000803202000000000008'

# ---------- 2. re-derive the child's remaining membership (string keys) ----------
parent_rows_after_merged = remM.get(PARENT, [])
child_hexes_remaining = {r['s6_hex'] for r in parent_rows_after_merged}
assert len(parent_rows_after_merged) == 3, 'parent expected at 3 remaining orbits after the merged baseline'
assert {r['s6_s7_edge_cost'] for r in parent_rows_after_merged} == {'75', '72', '75'}, \
    'parent remaining cost expected 222 = 75+72+75'
child_still_remaining = CHILD in child_hexes_remaining
child_in_solved = int(CHILD, 16) in sM
assert child_still_remaining is True, 'cost-75b child expected to be genuinely remaining at the claim state'
assert child_in_solved is False
child_demand = demM[CHILD]
assert child_demand == {'c1': 0, 'c2': 2, 'c4': 0}
membership = {
    'child_hex': CHILD,
    'claimed_as': 'one of the three remaining unswept children of the second class-2 '
                 'target (parent at 3 orbits / cost 222 after the merged frontier; claim '
                 'at commit 8cba4498, verified from class-frontier-top-candidates-s6-'
                 'after-merged-cost60bwarm-cost71b-20261115.csv)',
    'still_in_parent_remaining_children_at_claim': True,
    'midflight_manifest_closure': None,
    'demand_at_claim': dict(child_demand),
    'note': 'genuinely still remaining when swept (no mid-flight closure); its own '
            'WIN7 receipts may now cover it',
}
print('CONTROL child membership re-derived (string keys): still_remaining=True, '
      'demand c1=0,c2=2,c4=0')

# ---------- 3. assert the completed cost-75b sweep ----------
sweep = json.loads((OUT / 'class2-lane-cost75b-sweep-20261115.json').read_text())
assert sweep['s5_parent_hex'] == PARENT
assert sweep['s6_child_hex'] == CHILD
assert sweep['s6_s7_edge_cost'] == 75
assert sweep['win7_d10'] == 7 and sweep['refuted_d10'] == 68 and sweep['capped'] == 0
assert sweep['total_nodes'] == 139705045
assert sweep['win7_bits'] == [7, 51, 54, 84, 89, 99, 116]
assert sweep['unverified_win7_bits'] == []

tot_nodes = 0
seen_bits = set()
win_from_raw = set()
n_pilot = 0
for i in range(1, 11):
    for line in (OUT / f'class2-lane-cost75b-raw-batch{i}-20261115.jsonl').read_text().splitlines():
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
assert n_pilot == 10 and len(seen_bits) == 75 and tot_nodes == 139705045
assert win_from_raw == {7, 51, 54, 84, 89, 99, 116}
heaviest = sorted(((r['bit'], r['nodes']) for r in
                   (json.loads(l) for b in range(1, 11) for l in
                    (OUT / f'class2-lane-cost75b-raw-batch{b}-20261115.jsonl').read_text().splitlines()
                    if l.strip() and 'control' not in l)), key=lambda t: -t[1])[:6]
assert heaviest == [(52, 11503887), (116, 10699729), (86, 10402959),
                    (43, 8608953), (88, 6378258), (44, 5538830)]
print('CONTROL cost-75b sweep asserted from published raw batches: '
      '75 candidates, 10 pilots, 7 WIN7 + 68 REFUTED, 139,705,045 nodes')

det = [json.loads(l) for l in (OUT / 'class2-lane-cost75b-v16-determinism-rerun-20261115.jsonl')
       .read_text().splitlines() if l.strip()]
det_pilot = [r for r in det if 'control' in r]
assert len(det_pilot) == 1 and det_pilot[0]['loss'] is False and det_pilot[0]['nodes'] == 3402
det_bits = {r['bit']: r for r in det if 'bit' in r}
assert det_bits[7]['nodes'] == 2971923 and det_bits[7]['loss'] is True
assert det_bits[86]['nodes'] == 10402959 and det_bits[86]['loss'] is False
assert det_bits[116]['nodes'] == 10699729 and det_bits[116]['loss'] is True

v15 = [json.loads(l) for l in (OUT / 'class2-lane-cost75b-v15-crosscheck-20261115.jsonl')
       .read_text().splitlines() if l.strip()]
v15_pilot = [r for r in v15 if 'control' in r]
assert len(v15_pilot) == 1 and v15_pilot[0]['loss'] is False and v15_pilot[0]['nodes'] == 5949
v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
v15_expect = {7: 5462984, 51: 3050228, 54: 8568846, 84: 9025519,
               89: 5605094, 99: 3953206, 116: 18631277}
assert set(v15_bits) == set(v15_expect)
for b, n in v15_expect.items():
    assert v15_bits[b]['loss'] is True and v15_bits[b]['nodes'] == n, (b, v15_bits[b]['nodes'])
print('CONTROL determinism rerun (7/86/116 node-exact) and v15 anchors '
      '(all 7 WIN7 bits loss=true) asserted')

# ---------- 4. the seven verified receipts, marginals from the growing union ----------
certs_rec = json.loads((OUT / 'class2-lane-cost75b-win7-certificates-20261115.json').read_text())
assert certs_rec['child_hex'] == CHILD
certs = [c for c in certs_rec['certificates'] if c.get('verdict') == 'WIN7']
assert [c['bit'] for c in certs] == [7, 51, 54, 84, 89, 99, 116]
ROWS = {7: 47257, 51: 32508, 54: 50955, 84: 55484, 89: 45501, 99: 40056, 116: 80911}
SUBS = {7: 57, 51: 51, 54: 63, 84: 61, 89: 55, 99: 55, 116: 64}
EXT = {7: 8706242, 51: 4703026, 54: 11537642, 84: 13021801, 89: 8793296,
       99: 6172262, 116: 27980913}
MD5 = {7: '2e20e75c305962b4bc46045185778d14', 51: '6b78713f6af3b72817fca15194623873',
       54: 'ae02f4b95be3e50518ce7830d2083434', 84: 'cdfbd1bede75265c774af02cba1c7e9f',
       89: 'bc52efa62fe7794ad121f3d295e627a8', 99: '84e8444599ab0ba7d71989a88a9412bc',
       116: '85f01799e61b1f1fb402861924c4b2af'}
child_v = int(CHILD, 16)
group_covers = {}
for c in certs:
    assert c['rows'] == ROWS[c['bit']] and c['sub_roots_pass'] == SUBS[c['bit']]
    assert c['extraction_nodes'] == EXT[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['md5'] == MD5[c['bit']]
    assert int(c['root_hex'], 16) == child_v | (1 << c['bit'])
    group_covers[c['bit']] = covers(int(c['root_hex'], 16))
print('CONTROL cost-75b receipts asserted: bits 7/51/54/84/89/99/116 '
      '(rows/sub-roots/extraction-nodes/union/md5/roots)')

s_cur = set(sM)
cost75b_addition = {}
for bit in (7, 51, 54, 84, 89, 99, 116):
    cov = group_covers[bit]
    marg = cov - s_cur
    marg_m = marg & manifest
    cost75b_addition[str(bit)] = {
        'root_hex': format(child_v | (1 << bit), '032x'),
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    s_cur |= marg
st75, rem75, uniq75, dem75 = summary_state(s_cur)
assert s_cur >= sM, 'the after-cost-75b solved set must extend the after-merged baseline'
print('AFTER cost-75b:', json.dumps(st75, indent=1))

# child closure check after the additions
child_closed_now = int(CHILD, 16) in s_cur
print(f'cost-75b child in solved set after additions: {child_closed_now}')
membership['child_closed_by_own_receipts'] = child_closed_now
if child_closed_now:
    covering_bits = [b for b in (7, 51, 54, 84, 89, 99, 116) if child_v in group_covers[b]]
    membership['child_covered_by_receipt_bits'] = covering_bits

# parent remaining children after the additions
parent_rows_after75b = rem75.get(PARENT, [])
parent_children_after = [(r['s6_hex'], r['s6_s7_edge_cost']) for r in
                         sorted(parent_rows_after75b, key=lambda r: int(r['s6_s7_edge_cost']))]
print('parent remaining children after cost-75b:', parent_children_after)

# ---------- 5. new ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem75, 2)
class4 = best(rem75, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-cost75b-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-merged-cost60bwarm-cost71b-recompute-20261115 '
                     '(solved 1045 / unique remaining 6802 / sum 536131 / open 5072/399854)',
    'method': 'direct runpy extension of recompute_frontier_merged_after69ev2_70c_60bwarm_71b_'
              '20261115.py: the after-merged baseline is reproduced exactly (asserted '
              '1045/6802/536131/5072/399854), the cost-75b child remaining-membership is '
              're-derived with string keys (parent at 3 remaining orbits / cost 222, demand '
              'c1=0,c2=2,c4=0; genuinely still remaining when swept - no mid-flight closure), '
              'the completed cost-75b sweep is asserted from the published raw batches '
              '(75 candidates: 7 WIN7-D10 + 68 REFUTED, 0 capped, 139,705,045 v16 nodes; '
              '10 pilot d6 controls; determinism rerun bits 7/86/116 node-exact at '
              '2,971,923/10,402,959/10,699,729; v15 cross-engine anchors on all 7 WIN7 bits '
              'loss=true at 5,462,984/3,050,228/8,568,846/9,025,519/5,605,094/3,953,206/'
              '18,631,277 nodes), and all seven fully verified receipts (bits '
              '7/51/54/84/89/99/116; rows 47,257/32,508/50,955/55,484/45,501/40,056/80,911; '
              'sub-roots 57/51/63/61/55/55/64 PASS; union 0/0 each; independent BigInt audit '
              're-run PASS on the remote-rejoined bytes) are added in the published record '
              'order with per-bit marginals re-derived from the growing union; the bit-54 '
              'root 00000000000000803242000000000008 duplicates the cost-70c bit-3 win7_roots '
              'listing with no prior certificate (cost-70c certified bits 94/20/23 only) - '
              'this receipt is new coverage and also closes the cost-70c bit-3 warm entry; '
              'unverified_win7_bits is empty for this sweep (every WIN7-D10 candidate is '
              'certified)',
    'controls': {
        'after_merged_baseline': {'solved_in_manifest': 1045, 'unique_remaining': 6802,
                                  'sum_cost': 536131, 'open_s6': 5072, 'open_cost': 399854,
                                  'reproduced': True},
        'child_membership_reproduced_string_keys': True,
        'sweep_asserted_from_raw_batches': True,
        'receipts_asserted_rows_subs_extraction_union_md5_roots': True,
        'extends_after_merged_baseline': True,
    },
    'child_membership': membership,
    'parent_children_after_cost75b': parent_children_after,
    'cost75b_addition': cost75b_addition,
    'frontier_after_cost75b': {
        'solved_s6_in_manifest': st75['solved_s6_in_manifest'],
        'remaining_s5_orbits': st75['remaining_s5_orbits'],
        'unique_remaining_s6': st75['unique_remaining_s6'],
        'sum_remaining_cost': st75['sum_remaining_cost'],
        's6_needed_by_open_classes': st75['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st75['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st75['hist'],
        'best_class2': class2[0],
        'audit_blocked_class2': next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'outstanding_not_folded': {
        'cost72_sweep': 'parallel lane in flight (raw batches + audits + bit-111 certificate '
                        'published; 2 WIN7-D10 bits 52/111; no completed sweep record yet) - '
                        'certificates without records are not receipts',
        'sibling_cost75_child': '00000000000000803202000000004000 (cost 75, same parent) '
                                'remains an unswept warm candidate',
        'warm_rebuild_candidates_without_records': 'cost-61d bit-22 (= cost-71b bit-1 root), '
                                                   'cost-71b remaining WIN7 bits '
                                                   '1/14/32/74/94/117, and other unverified '
                                                   'WIN7 bits of earlier bands',
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove '
                            'only absence of WIN7-D10; WIN7 certificates prove a win within '
                            'depth 10 from the 7-stone root only; 11x11 empty root / {49,60} '
                            '/ S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost75b-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost75b-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem75.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost75b-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-cost75b-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('second class-2 target S5 (cost-75b parent)',
                         next(c for c in class2 if c['s5_hex'] == PARENT))):
        rows = rem75.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem75[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost75b)')
