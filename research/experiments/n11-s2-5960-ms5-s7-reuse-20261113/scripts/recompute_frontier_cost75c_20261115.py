#!/usr/bin/env python3
"""Class-2/4 frontier recomputation folding the cost-72 bit-111 partial
receipt and the class2-lane cost-75c sweep receipts on top of the
after-cost-75b frontier (2026-11-15).

Baseline (published main): class-frontier-cost75b-recompute-20261115.json
(solved 1049 / unique remaining 6798 / sum 535812 / open 5068/399535),
produced by recompute_frontier_cost75b_20261115.py (commit c6941de2).

This script:
1. reproduces the after-cost-75b baseline by runpy (asserting
   1049/6798/535812/5068/399535);
2. re-derives the cost-75c child's remaining membership with string keys
   (the child 00000000000000803202000000004000 was claimed at commit
   f7a6d53b as one of the two remaining unswept children of the second
   class-2 target, parent at 2 remaining orbits / cost 147, demand
   c1=0,c2=2,c4=0; it was genuinely still remaining when swept - no
   mid-flight closure);
3. folds the published cost-72 bit-111 partial receipt first (record
   class2-lane-cost72-win7-certificates-20261115.json, commit ffb69196;
   root 00008000000000803202000000000200, 46,160 rows, 54 sub-roots
   PASS, union 0/0, git blob sha verified), leaving the parent with only
   the cost-75c child outstanding; the cost-72 bit-52 WIN7-D10 candidate
   remains without a certificate and the cost-72 sweep record remains
   in-flight, so nothing else from that sweep is folded;
4. asserts the completed cost-75c sweep (75 candidates: 12 WIN7-D10 + 63
   REFUTED, 0 capped, 138,240,690 v16 nodes; all 10 raw batches re-summed
   from the published JSONL; determinism rerun bits 66/75/111 node-exact
   and the v15 cross-engine anchors on all 12 WIN7 bits asserted from
   the published JSONL);
5. asserts all twelve fully verified cost-75c receipts (bits
   8/12/22/66/84/89/96/97/98/100/108/111) in the published record order,
   re-deriving every per-bit marginal from the growing union, and produces
   the after-cost-75c frontier + ranking CSV + top-candidates CSV. The
   bit-12 root duplicates the cost-65h bit-14 win7_roots listing and the
   bit-22 root the cost-71b bit-14 win7_roots listing (both uncertified
   there: cost-65h certified bits 7/109/24, cost-71b certified bits
   109/21/105), so these receipts are the first certificates for those
   roots and close the respective warm entries;
6. records the parent's remaining children after the additions (expected:
   none - the second class-2 target S5 00000000000000803202000000000000 is
   fully closed by receipts on all of its remaining children).
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-75b baseline (1049) ----------
nsB = runpy.run_path(str(HERE / 'scripts' /
                         'recompute_frontier_cost75b_20261115.py'))
sB = nsB['s_cur']
stB = nsB['st75']
remB = nsB['rem75']
demB = nsB['dem75']
covers = nsB['covers']
summary_state = nsB['summary_state']
manifest = nsB['manifest']
classes = nsB['classes']
PARENT = nsB['PARENT']
assert stB['solved_s6_in_manifest'] == 1049 and stB['unique_remaining_s6'] == 6798
assert stB['sum_remaining_cost'] == 535812
assert stB['s6_needed_by_open_classes'] == 5068 and stB['cost_needed_by_open_classes'] == 399535
print('CONTROL after-cost-75b baseline reproduced: 1049/6798/535812/5068/399535')

CHILD = '00000000000000803202000000004000'
CHILD72 = '00000000000000803202000000000200'

# ---------- 2. re-derive the cost-75c child's remaining membership ----------
parent_rows_after75b = remB.get(PARENT, [])
child_hexes_remaining = {r['s6_hex'] for r in parent_rows_after75b}
assert len(parent_rows_after75b) == 2, 'parent expected at 2 remaining orbits after cost-75b'
assert {r['s6_s7_edge_cost'] for r in parent_rows_after75b} == {'72', '75'}, \
    'parent remaining cost expected 147 = 72+75'
child_still_remaining = CHILD in child_hexes_remaining
child_in_solved = int(CHILD, 16) in sB
assert child_still_remaining is True, 'cost-75c child expected to be genuinely remaining at the claim state'
assert child_in_solved is False
child_demand = demB[CHILD]
assert child_demand == {'c1': 0, 'c2': 2, 'c4': 0}
membership = {
    'child_hex': CHILD,
    'claimed_as': 'one of the two remaining unswept children of the second class-2 '
                 'target (parent at 2 orbits / cost 147 after the cost-75b frontier; '
                 'claim at commit f7a6d53b, verified from class-frontier-top-'
                 'candidates-s6-after-cost75b-20261115.csv)',
    'still_in_parent_remaining_children_at_claim': True,
    'midflight_manifest_closure': None,
    'demand_at_claim': dict(child_demand),
    'note': 'genuinely still remaining when swept (no mid-flight closure); its own '
            'WIN7 receipts may now cover it',
}
print('CONTROL cost-75c child membership re-derived (string keys): '
      'still_remaining=True, demand c1=0,c2=2,c4=0')

# ---------- 3. fold the cost-72 bit-111 partial receipt first ----------
rec72 = json.loads((OUT / 'class2-lane-cost72-win7-certificates-20261115.json').read_text())
assert rec72['schema'] == 'n11-class2-lane-partial-win7-receipt-v1'
assert rec72['status'] == 'partial_receipt'
assert rec72['child_s6_hex'] == CHILD72 and rec72['s5_parent_hex'] == PARENT
assert rec72['child_edge_cost'] == 72
assert rec72['unverified_win7_bits'] == [52]
c72 = rec72['certificate']
assert c72['bit'] == 111
assert c72['root_hex'] == '00008000000000803202000000000200'
assert int(c72['root_hex'], 16) == int(CHILD72, 16) | (1 << 111)
assert c72['strategy_rows'] == 46160 and c72['subroots_pass'] == 54
assert c72['union_missing'] == 0 and c72['union_extra'] == 0
assert c72['git_blob_sha'] == 'b0fee80a9a2c906bccf20983ef97279309f95367'
assert c72['bytes'] == 1664895
s_cur = set(sB)
cov72 = covers(int(c72['root_hex'], 16))
marg72 = cov72 - s_cur
marg72_m = marg72 & manifest
cost72_fold = {
    'root_hex': c72['root_hex'],
    'covers': len(cov72), 'marginal': len(marg72),
    'marginal_in_manifest': len(marg72_m),
    'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg72_m),
}
s_cur |= cov72
child72_closed_now = int(CHILD72, 16) in s_cur
print('CONTROL cost-72 bit-111 receipt folded; cost-72 child closed by it:',
      child72_closed_now)
parent_children_after72 = [(r['s6_hex'], r['s6_s7_edge_cost']) for r in
                           sorted(parent_rows_after75b, key=lambda r: int(r['s6_s7_edge_cost']))
                           if int(r['s6_hex'], 16) not in s_cur]
print('parent remaining children after the cost-72 fold:', parent_children_after72)
assert parent_children_after72 == [(CHILD, '75')], \
    'after the cost-72 fold only the cost-75c child must remain'

# ---------- 4. assert the completed cost-75c sweep ----------
sweep = json.loads((OUT / 'class2-lane-cost75c-sweep-20261115.json').read_text())
assert sweep['schema'] == 'n11-class2-lane-cost75c-sweep-20261115-v1'
assert sweep['s5_parent_hex'] == PARENT
assert sweep['s6_child_hex'] == CHILD
assert sweep['s6_s7_edge_cost'] == 75
assert sweep['win7_d10'] == 12 and sweep['refuted_d10'] == 63 and sweep['capped'] == 0
assert sweep['total_nodes'] == 138240690
assert sweep['win7_bits'] == [8, 12, 22, 66, 84, 89, 96, 97, 98, 100, 108, 111]
assert sweep['unverified_win7_bits'] == []

tot_nodes = 0
seen_bits = set()
win_from_raw = set()
n_pilot = 0
for i in range(1, 11):
    for line in (OUT / f'class2-lane-cost75c-raw-batch{i}-20261115.jsonl').read_text().splitlines():
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
assert n_pilot == 10 and len(seen_bits) == 75 and tot_nodes == 138240690
assert win_from_raw == {8, 12, 22, 66, 84, 89, 96, 97, 98, 100, 108, 111}
heaviest = sorted(((r['bit'], r['nodes']) for r in
                   (json.loads(l) for b in range(1, 11) for l in
                    (OUT / f'class2-lane-cost75c-raw-batch{b}-20261115.jsonl').read_text().splitlines()
                    if l.strip() and 'control' not in l)), key=lambda t: -t[1])[:6]
assert heaviest == [(66, 10845926), (75, 8628305), (4, 8136345),
                    (6, 6949289), (22, 6943892), (97, 5426364)]
print('CONTROL cost-75c sweep asserted from published raw batches: '
      '75 candidates, 10 pilots, 12 WIN7 + 63 REFUTED, 138,240,690 nodes')

det = [json.loads(l) for l in (OUT / 'class2-lane-cost75c-v16-determinism-rerun-20261115.jsonl')
       .read_text().splitlines() if l.strip()]
det_pilot = [r for r in det if 'control' in r]
assert len(det_pilot) == 1 and det_pilot[0]['loss'] is False and det_pilot[0]['nodes'] == 3402
det_bits = {r['bit']: r for r in det if 'bit' in r}
assert det_bits[66]['nodes'] == 10845926 and det_bits[66]['loss'] is True
assert det_bits[75]['nodes'] == 8628305 and det_bits[75]['loss'] is False
assert det_bits[111]['nodes'] == 1611883 and det_bits[111]['loss'] is True

v15 = [json.loads(l) for l in (OUT / 'class2-lane-cost75c-v15-crosscheck-20261115.jsonl')
       .read_text().splitlines() if l.strip()]
v15_pilot = [r for r in v15 if 'control' in r]
assert len(v15_pilot) == 3 and all(r['loss'] is False and r['nodes'] == 5949 for r in v15_pilot)
v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
v15_expect = {8: 8372581, 12: 7865566, 22: 14083030, 66: 21096647, 84: 7350763,
              89: 7039706, 96: 4292180, 97: 9304101, 98: 8165861, 100: 7067263,
              108: 5643984, 111: 3568856}
assert set(v15_bits) == set(v15_expect)
for b, n in v15_expect.items():
    assert v15_bits[b]['loss'] is True and v15_bits[b]['nodes'] == n, (b, v15_bits[b]['nodes'])
print('CONTROL determinism rerun (66/75/111 node-exact) and v15 anchors '
      '(all 12 WIN7 bits loss=true) asserted')

# ---------- 5. the twelve verified receipts, marginals from the growing union ----------
certs_rec = json.loads((OUT / 'class2-lane-cost75c-win7-certificates-20261115.json').read_text())
assert certs_rec['child_hex'] == CHILD
assert certs_rec['unverified_win7_bits'] == []
certs = [c for c in certs_rec['certificates'] if c.get('verdict') == 'WIN7']
assert [c['bit'] for c in certs] == [8, 12, 22, 66, 84, 89, 96, 97, 98, 100, 108, 111]
ROWS = {8: 66236, 12: 60023, 22: 78999, 66: 86401, 84: 59056, 89: 60677,
        96: 42471, 97: 55851, 98: 68738, 100: 48859, 108: 42639, 111: 43428}
SUBS = {8: 66, 12: 57, 22: 63, 66: 62, 84: 59, 89: 58,
        96: 55, 97: 55, 98: 66, 100: 58, 108: 57, 111: 54}
EXT = {8: 13452039, 12: 12936955, 22: 22433703, 66: 31224950, 84: 12031200,
       89: 11714155, 96: 6589016, 97: 15206431, 98: 13729984, 100: 10758610,
       108: 8310219, 111: 6630448}
MD5 = {8: '635d1fda7ef0afa43d480fb787edc0e3', 12: '5293ef1e140eea8bc048c22fc2a83e76',
       22: 'aaa837e0ef6e75890f2bfbaa6d2b4f52', 66: '07800808777f60a21df188b6a3db7481',
       84: '7548731a2cf010bd908b68f89cb09985', 89: '87b6683334d46ef1991db72f9259cfba',
       96: 'dbf142eeb14d62c7c139185046eb7d0f', 97: '8d9e0917daaa30e01e85c86689ea49ee',
       98: '079a29e46784a5733e684815b48236fb', 100: '6c0cf7159e73cfa37b2c310922bef707',
       108: 'a703f79d3240322ed7ed5bba6f411765', 111: '643a8fc92a0327075d00acea390ea9fc'}
SHA = {8: 'c32d6f1a17d8df25ebaa08c10eea0db20f7cdad15974b92d3d38473fcb66388e',
       12: '7fe951160cfd247520b9e8a8bbda7f788c76caba0b32cf64294e9005294e7ee0',
       22: '5b4cfab235e4c1ffff6683ef974566f15996ae7203b80a0bd2c21b72b31c3261',
       66: 'd71328839310757ef75f42acd3289d2776c9a9603f8d873b4998d83732c6f583',
       84: '9a3b94aa7bf358061eab24c9e277938c1a90014d88308c3b70bd1c957badf244',
       89: '351207ef894878858108ae8d2ce620b1f160f5ce5d16b842929cfcf617c85768',
       96: '7dee9026332ae4a7fd409e357d55d228f1c2b24cdfefba24a06b148c912ce388',
       97: '49912205820abcc315991768a61da3d8af0cace107505740d1982d2f3571692c',
       98: '185222550a31e835ebc353554fb2da24ca8d0182466047343702776513a3f9c1',
       100: '9d969a138e2c267ab5b75da589aeea59d2411eab514db0ffaf7da71b5f81136b',
       108: 'b8def7be901359b1cb574834cec4cd9f8bb763d52d5140bb8d8bcd2932309d63',
       111: '4dc436e4201953ef2df1389d079dc7f7465504c9edd42dc446b0e8d6725b1edf'}
child_v = int(CHILD, 16)
group_covers = {}
for c in certs:
    assert c['rows'] == ROWS[c['bit']] and c['sub_roots_pass'] == SUBS[c['bit']]
    assert c['extraction_nodes'] == EXT[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['md5'] == MD5[c['bit']] and c['sha256'] == SHA[c['bit']]
    assert int(c['root_hex'], 16) == child_v | (1 << c['bit'])
    group_covers[c['bit']] = covers(int(c['root_hex'], 16))
print('CONTROL cost-75c receipts asserted: bits 8/12/22/66/84/89/96/97/98/'
      '100/108/111 (rows/sub-roots/extraction-nodes/union/md5/sha256/roots)')

# duplicate-root cross-checks against the published records
rec65h = json.loads((OUT / 'class2-lane-cost65h-sweep-20261114.json').read_text())
assert rec65h['win7_roots'][rec65h['win7_bits'].index(14)] == '00000000000000803202000000005000'
certs65h = json.loads((OUT / 'class2-lane-cost65h-win7-certificates-20261114.json').read_text())
assert [c['bit'] for c in certs65h['certificates']] == [7, 109, 24]
rec71b = json.loads((OUT / 'class2-lane-cost71b-sweep-20261115.json').read_text())
assert rec71b['win7_roots'][rec71b['win7_bits'].index(14)] == '00000000000000803202000000404000'
certs71b = json.loads((OUT / 'class2-lane-cost71b-win7-certificates-20261115.json').read_text())
assert [c['bit'] for c in certs71b['certificates']] == [109, 21, 105]
print('CONTROL duplicate roots verified: bit-12 root = cost-65h bit-14 listing '
      '(uncertified there), bit-22 root = cost-71b bit-14 listing (uncertified there)')

cost75c_addition = {}
for c in certs:
    bit = c['bit']
    cov = group_covers[bit]
    marg = cov - s_cur
    marg_m = marg & manifest
    cost75c_addition[str(bit)] = {
        'root_hex': format(child_v | (1 << bit), '032x'),
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    s_cur |= marg
st75c, rem75c, uniq75c, dem75c = summary_state(s_cur)
assert s_cur >= sB | cov72, 'the after-cost-75c solved set must extend the folded baseline'
print('AFTER cost-75c:', json.dumps(st75c, indent=1))

# child closure check after the additions
child_closed_now = child_v in s_cur
print(f'cost-75c child in solved set after additions: {child_closed_now}')
membership['child_closed_by_own_receipts'] = child_closed_now
if child_closed_now:
    covering_bits = [b for b in (8, 12, 22, 66, 84, 89, 96, 97, 98, 100, 108, 111)
                     if child_v in group_covers[b]]
    membership['child_covered_by_receipt_bits'] = covering_bits

# parent remaining children after the additions
parent_rows_after75c = rem75c.get(PARENT, [])
parent_children_after = [(r['s6_hex'], r['s6_s7_edge_cost']) for r in
                         sorted(parent_rows_after75c, key=lambda r: int(r['s6_s7_edge_cost']))]
print('parent remaining children after cost-75c:', parent_children_after)
second_target_closed = len(parent_children_after) == 0
print('second class-2 target S5 fully closed by receipts:', second_target_closed)

# ---------- 6. new ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem75c, 2)
class4 = best(rem75c, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-cost75c-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-cost75b-recompute-20261115 '
                     '(solved 1049 / unique remaining 6798 / sum 535812 / open 5068/399535)',
    'method': 'direct runpy extension of recompute_frontier_cost75b_20261115.py: the '
              'after-cost-75b baseline is reproduced exactly (asserted '
              '1049/6798/535812/5068/399535), the cost-75c child remaining-membership '
              'is re-derived with string keys (parent at 2 remaining orbits / cost 147, '
              'demand c1=0,c2=2,c4=0; genuinely still remaining when swept - no '
              'mid-flight closure), the published cost-72 bit-111 partial receipt is '
              'folded first (root 00008000000000803202000000000200, 46,160 rows, 54 '
              'sub-roots PASS, union 0/0, git blob sha b0fee80a... asserted), the '
              'completed cost-75c sweep is asserted from the published raw batches '
              '(75 candidates: 12 WIN7-D10 + 63 REFUTED, 0 capped, 138,240,690 v16 '
              'nodes; 10 pilot d6 controls; determinism rerun bits 66/75/111 node-exact '
              'at 10,845,926/8,628,305/1,611,883; v15 cross-engine anchors on all 12 '
              'WIN7 bits loss=true), and all twelve fully verified receipts (bits '
              '8/12/22/66/84/89/96/97/98/100/108/111; rows 66,236/60,023/78,999/86,401/'
              '59,056/60,677/42,471/55,851/68,738/48,859/42,639/43,428; sub-roots '
              '66/57/63/62/59/58/55/55/66/58/57/54 PASS; union 0/0 each; independent '
              'BigInt audit on every certificate; remote bytes verified byte-exact by '
              'git blob sha on every pushed part) are added in the published record '
              'order with per-bit marginals re-derived from the growing union; the '
              'bit-12 root 00000000000000803202000000005000 duplicates the uncertified '
              'cost-65h bit-14 win7_roots listing and the bit-22 root '
              '00000000000000803202000000404000 the uncertified cost-71b bit-14 '
              'win7_roots listing, so both receipts are first certificates and close '
              'the respective warm entries; unverified_win7_bits is empty for this '
              'sweep (every WIN7-D10 candidate is certified)',
    'controls': {
        'after_cost75b_baseline': {'solved_in_manifest': 1049, 'unique_remaining': 6798,
                                   'sum_cost': 535812, 'open_s6': 5068, 'open_cost': 399535,
                                   'reproduced': True},
        'child_membership_reproduced_string_keys': True,
        'cost72_receipt_asserted_before_folding': True,
        'sweep_asserted_from_raw_batches': True,
        'receipts_asserted_rows_subs_extraction_union_md5_sha256_roots': True,
        'duplicate_roots_asserted_against_65h_71b_records': True,
        'extends_after_cost75b_baseline': True,
    },
    'child_membership': membership,
    'cost72_fold': cost72_fold,
    'parent_children_after_cost72_fold': parent_children_after72,
    'parent_children_after_cost75c': parent_children_after,
    'second_class2_target_closed': second_target_closed,
    'cost75c_addition': cost75c_addition,
    'frontier_after_cost75c': {
        'solved_s6_in_manifest': st75c['solved_s6_in_manifest'],
        'remaining_s5_orbits': st75c['remaining_s5_orbits'],
        'unique_remaining_s6': st75c['unique_remaining_s6'],
        'sum_remaining_cost': st75c['sum_remaining_cost'],
        's6_needed_by_open_classes': st75c['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st75c['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st75c['hist'],
        'best_class2': class2[0],
        'audit_blocked_class2': next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'outstanding_not_folded': {
        'cost72_bit52': 'the cost-72 bit-52 WIN7-D10 candidate had no receipt record '
                        'on main when this recompute was written (the parallel lane '
                        'was publishing its certificate parts during this session; '
                        'the completed-sweep record and its fold belong to the '
                        'cost-72 lane), so only the bit-111 partial receipt is '
                        'folded here',
        'warm_multiband_certificates_after_baseline': 'warm multiband certificates '
                        'published by the parallel lane after the after-cost-75b '
                        'baseline (cost-62a bits 32/66/86/95, cost-63a bits 15/100, '
                        'cost-65e bits 42/94, ...) are not folded here; their fold '
                        'belongs to a canonical merged recompute of the chain head',
        'warm_rebuild_candidates_without_records': 'cost-61d bit-22 (= cost-71b bit-1 root), '
                        'cost-71b remaining WIN7 bits 1/14/32/74/94/117 (bit-14 root now '
                        'certified by this sweep), and other unverified WIN7 bits of '
                        'earlier bands',
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove '
                            'only absence of WIN7-D10; WIN7 certificates prove a win within '
                            'depth 10 from the 7-stone root only; closing the second '
                            'class-2 target S5 by receipts covers exactly its manifest '
                            'children and does not decide the class-2 demand in general; '
                            '11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 '
                            'remain UNKNOWN',
}
(OUT / 'class-frontier-cost75c-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost75c-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem75c.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost75c-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-cost75c-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED))):
        rows = rem75c.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem75c[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost75c)')
