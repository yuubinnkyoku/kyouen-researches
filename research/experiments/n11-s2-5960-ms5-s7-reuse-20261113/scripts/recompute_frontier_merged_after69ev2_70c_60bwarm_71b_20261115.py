#!/usr/bin/env python3
"""Class-2/4 frontier recomputation merging the three post-69e-v2 receipt
groups (cost-70c + cost-60b-warm + cost-71b) into the current published
baseline (2026-11-15). Doubles as the repair of the 69e-v2 chain break.

Chain break being repaired: the cost-69e layer on main was updated to v2
(recompute_frontier_cost69e_20261115.py + class2-lane-cost69e-win7-certificates
-20261114.json + class-frontier-cost69e-recompute-20261115.json schema v2),
folding ALL TEN cost-69e receipts (bits 21/99/87/84/76/90 + the 2026-11-15
warm rebuilds 89/94/108/116) into the recompute and moving the after-cost-69e
endpoint 1019 -> 1023 / 6824 / 537833 / 5094/401556. The three downstream
published scripts recompute_frontier_cost70c_20261115.py (asserts the 1019
baseline and the 1022 endpoint), recompute_frontier_cost60b_warm_20261115.py
(asserts 1022/1040) and recompute_frontier_cost71b_20261115.py (asserts
1022/1026) all runpy the cost-69e script and now FAIL their baseline asserts
(verified: recompute_frontier_cost70c_20261115.py raises AssertionError at
line 47 against current main). This script supersedes the three scripts as
the canonical chain head:

1. reproduces the cost-69e v2 baseline by runpy (asserting
   1023/6824/537833/5094/401556);
2. re-derives the pre-v2 six-receipt state (1019) and from it the three
   superseded published endpoints exactly: after-cost-70c 1022, after-cost-
   60b-warm 1040, after-cost-71b 1026 (reproduced from raw records, without
   runpy-ing the now-failing scripts, so the historical endpoints stay
   verifiable);
3. asserts the completed cost-70c sweep (70 candidates: 13 WIN7-D10 + 57
   REFUTED, 0 capped, 100,935,666 v16 nodes; all 9 raw batches re-summed;
   determinism rerun bits 86/66 node-exact; v15 anchors on all 13 WIN7
   bits) and its three receipts (bits 94/20/23);
4. asserts the cost-60b sweep record (25 WIN7-D10, unverified_win7_bits 19)
   and the warm rebuild record (17 certificates: rows/sub-roots/union/md5/
   extraction-nodes/roots; bits 15/34 are cross-child duplicates already in
   the manifest and are NOT re-added);
5. asserts the completed cost-71b sweep (71 candidates: 9 WIN7-D10 + 62
   REFUTED, 0 capped, 87,586,636 v16 nodes; raw batches re-summed;
   determinism rerun bits 32/113 node-exact; v15 anchors on all 9 WIN7
   bits; the two control JSONLs re-published by this lane in commit 86bbe2ef
   after they were found missing) and its three receipts (bits 109/21/105);
6. re-adds all 23 receipts in one canonical chronological order
   (70c 94/20/23 -> 60b-warm 40/77/26/74/44/28/8/88/95/106/87/22/100/108/
   32/114/43 -> 71b 109/21/105) from the 69e v2 baseline, re-deriving every
   per-bit marginal from the growing union and comparing each with its
   published stage marginal (marginal_reduced_vs_published flags; the 71b
   bit-21 root duplicates the 60b-warm bit-22 root - the duplicate-fold rule
   applies);
7. produces the merged frontier + ranking CSV + top-candidates CSV.

The merged solved set equals the 69e v2 baseline union all 23 receipt
covers and contains every superseded endpoint's solved set. The cost-72
sweep (parallel lane in flight: 9 raw batches + audit, 2 WIN7-D10 bits
52/111, bit-111 certificate, no completed sweep record) is NOT folded:
certificates without records are not receipts.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the cost-69e v2 baseline (1023) ----------
ns69 = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost69e_20261115.py'))
s69v2 = ns69['s_cur']
st69v2 = ns69['st69']
assert st69v2['solved_s6_in_manifest'] == 1023 and st69v2['unique_remaining_s6'] == 6824
assert st69v2['sum_remaining_cost'] == 537833
assert st69v2['s6_needed_by_open_classes'] == 5094
assert st69v2['cost_needed_by_open_classes'] == 401556
sM = ns69['sM']
c69 = ns69['group_covers']
covers = ns69['covers']
summary_state = ns69['summary_state']
manifest = ns69['manifest']
classes = ns69['classes']
print('CONTROL cost-69e v2 baseline reproduced: 1023/6824/537833/5094/401556')

PARENT = '00000000000000803202000000000000'

# ---------- 2. re-derive the superseded endpoints (1019/1022/1040/1026) ----------
SIX69 = (21, 99, 87, 84, 76, 90)
s69v1 = set(sM)
for b in SIX69:
    s69v1 |= c69[b]
st69v1, _, _, _ = summary_state(s69v1)
assert st69v1['solved_s6_in_manifest'] == 1019, st69v1
assert s69v1 <= s69v2, 'the v2 six-receipt state must be a subset of the v2 endpoint'
print('CONTROL pre-v2 six-receipt state reproduced: 1019 (subset of 1023)')

# ---------- 3. cost-70c sweep + receipts ----------
CHILD_70C = '00000000000000803242000000000000'
sweep70 = json.loads((OUT / 'class2-lane-cost70c-sweep-20261115.json').read_text())
assert sweep70['s6_child_hex'] == CHILD_70C
assert sweep70['s6_s7_edge_cost'] == 70
assert sweep70['win7_d10'] == 13 and sweep70['refuted_d10'] == 57 and sweep70['capped'] == 0
assert sweep70['total_nodes'] == 100935666
assert sweep70['win7_bits'] == [3, 8, 11, 20, 23, 24, 40, 42, 86, 92, 94, 103, 105]
tot70 = 0
seen70 = set()
win70 = set()
np70 = 0
for i in range(1, 10):
    for line in (OUT / f'class2-lane-cost70c-raw-batch{i}-20261115.jsonl').read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if 'control' in row:
            assert row['loss'] is False and row['nodes'] == 3402 and not row['capped']
            np70 += 1
            continue
        assert row['capped'] is False
        assert row['terminalStoneRange'] == [13, 17]
        assert row['bit'] not in seen70
        seen70.add(row['bit'])
        tot70 += row['nodes']
        if row['loss']:
            win70.add(row['bit'])
assert np70 == 9 and len(seen70) == 70 and tot70 == 100935666
assert win70 == {3, 8, 11, 20, 23, 24, 40, 42, 86, 92, 94, 103, 105}
det70 = [json.loads(l) for l in (OUT / 'class2-lane-cost70c-v16-determinism-rerun-20261115.jsonl')
         .read_text().splitlines() if l.strip()]
d70 = {r['bit']: r for r in det70 if 'bit' in r}
assert d70[86]['nodes'] == 6414891 and d70[86]['loss'] is True
assert d70[66]['nodes'] == 8291296 and d70[66]['loss'] is False
v15_70 = [json.loads(l) for l in (OUT / 'class2-lane-cost70c-v15-crosscheck-20261115.jsonl')
          .read_text().splitlines() if l.strip()]
p70 = [r for r in v15_70 if 'control' in r]
assert len(p70) == 2 and all(r['loss'] is False and r['nodes'] == 5949 for r in p70)
b70 = {r['bit']: r for r in v15_70 if 'bit' in r}
v70_expect = {94: 1013979, 20: 2508065, 23: 2093938, 40: 2398259, 11: 3661352,
              105: 3649378, 24: 4853985, 92: 6634458, 103: 7921123, 42: 7805543,
              8: 8467137, 3: 8568846, 86: 17475934}
assert set(b70) == set(v70_expect)
for bb, nn in v70_expect.items():
    assert b70[bb]['loss'] is True and b70[bb]['nodes'] == nn, (bb, b70[bb]['nodes'])
print('CONTROL cost-70c sweep asserted: 70 candidates, 13 WIN7 + 57 REFUTED, '
      '100,935,666 nodes; det 86/66 node-exact; v15 anchors 13/13')

rec70 = json.loads((OUT / 'class2-lane-cost70c-win7-certificates-20261115.json').read_text())
assert rec70['child_hex'] == CHILD_70C
certs70 = [c for c in rec70['certificates'] if c.get('verdict') == 'WIN7']
assert [c['bit'] for c in certs70] == [94, 20, 23]
R70 = {94: 20527, 20: 32576, 23: 33954}
S70 = {94: 46, 20: 52, 23: 54}
M70 = {94: 'c5d3232b9c9acd5e788b72b8e4d10c34',
       20: '4365967e4fc10d7643b7707296398096',
       23: '84c0d9ee69aa372b2c6bb349fd431e3b'}
cv70 = int(CHILD_70C, 16)
c70c = {}
for c in certs70:
    assert c['rows'] == R70[c['bit']] and c['sub_roots_pass'] == S70[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['md5'] == M70[c['bit']]
    assert int(c['root_hex'], 16) == cv70 | (1 << c['bit'])
    c70c[c['bit']] = covers(int(c['root_hex'], 16))
print('CONTROL cost-70c receipts asserted: bits 94/20/23 (rows/sub-roots/union/md5/roots)')

# superseded after-cost-70c endpoint (1022) re-derived from raw records
s_old1022 = set(s69v1)
for b in (94, 20, 23):
    s_old1022 |= c70c[b]
st_old1022, _, _, _ = summary_state(s_old1022)
assert st_old1022['solved_s6_in_manifest'] == 1022, st_old1022
print('CONTROL superseded after-cost-70c endpoint re-derived: 1022')

# ---------- 4. cost-60b sweep + warm record ----------
CHILD_60B = '00000000000000803202000000200000'
sweep60 = json.loads((OUT / 'class2-lane-cost60b-sweep-20261114.json').read_text())
assert sweep60['s6_child_hex'] == CHILD_60B
assert sweep60['win7_d10'] == 25 and sweep60['refuted_d10'] == 35 and sweep60['capped'] == 0
assert sweep60['win7_bits'] == [8, 15, 22, 23, 26, 28, 32, 34, 40, 43, 44, 73, 74, 77, 87, 88,
                                94, 95, 96, 100, 105, 106, 108, 114, 117]
assert sweep60['unverified_win7_bits'] == [8, 15, 22, 26, 28, 32, 34, 40, 43, 44, 74, 77, 87,
                                           88, 95, 100, 106, 108, 114]
warm = json.loads((OUT / 'class2-lane-cost60b-warm-certificates-20261115.json').read_text())
assert warm['child_hex'] == CHILD_60B
assert [d['bit'] for d in warm['duplicate_cross_child_entries']] == [15, 34]
wcerts = [c for c in warm['certificates'] if c.get('verdict') == 'WIN7']
WARM_ORDER = [40, 77, 26, 74, 44, 28, 8, 88, 95, 106, 87, 22, 100, 108, 32, 114, 43]
assert [c['bit'] for c in wcerts] == WARM_ORDER
WR = {40: 21115, 77: 24881, 26: 23978, 74: 26957, 44: 28432, 28: 17776, 8: 25431,
      88: 33554, 95: 27875, 106: 28496, 87: 30672, 22: 29242, 100: 27369, 108: 29454,
      32: 41391, 114: 35351, 43: 36424}
WS = {40: 44, 77: 48, 26: 51, 74: 48, 44: 51, 28: 42, 8: 48, 88: 51, 95: 47, 106: 51,
      87: 51, 22: 52, 100: 50, 108: 50, 32: 54, 114: 54, 43: 51}
WM = {40: '56b950b9b51f8608fb136ee2df526b06', 77: '46512a5d30cb31079f95b4547d3a6a36',
      26: 'e3fd1dd2667da65644c392b7100483fb', 74: 'ca2b07c7db11de35f7ea80d184b0b2b3',
      44: '84c22e9e7f7597cb50b08467f41651ab', 28: '4a028a955cf1f037eac3355ebbdd61ce',
      8: '5ada7ba5b639eadef4790f088afb9a7e', 88: 'cc01c0c72a66811222ffd3639939a55f',
      95: '10ba4b046fc26e2d07195f190337c8e3', 106: '140f28ab429970b7f993344adf914646',
      87: '7e198eea86b9c03d71893e8a17345c99', 22: '0bca8499e98e1a0197db2a6f6bd2d6ab',
      100: 'a53826ed8448b68ee38a0c64c93318c4', 108: '6914fa1ec2f6709bf0a59cce1a2fd3e8',
      32: 'b8c5e9cbae8d935c9c4c1bc950f7a9da', 114: 'a6ca671ae1db518a2238bf85196f8b0d',
      43: 'f2590a956c4a976d686de3e63008b3e2'}
WE = {40: 1510483, 77: 2381950, 26: 2458043, 74: 1953702, 44: 2505216, 28: 3494345,
      8: 2727531, 88: 3072584, 95: 8535755, 106: 4269102, 87: 4109578, 22: 4454710,
      100: 4377221, 108: 5242890, 32: 5524659, 114: 6292430, 43: 7640986}
cv60 = int(CHILD_60B, 16)
cwarm = {}
for c in wcerts:
    b = c['bit']
    assert c['rows'] == WR[b] and c['sub_roots_pass'] == WS[b]
    assert c['extraction_nodes'] == WE[b]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['md5'] == WM[b]
    assert int(c['root_hex'], 16) == cv60 | (1 << b)
    cwarm[b] = covers(int(c['root_hex'], 16))
print('CONTROL cost-60b warm receipts asserted: 17 certificates '
      '(rows/sub-roots/union/md5/extraction-nodes/roots)')

# superseded after-cost-60b-warm endpoint (1040) re-derived from raw records
s_old1040 = set(s_old1022)
for b in WARM_ORDER:
    s_old1040 |= cwarm[b]
st_old1040, _, _, _ = summary_state(s_old1040)
assert st_old1040['solved_s6_in_manifest'] == 1040, st_old1040
print('CONTROL superseded after-cost-60b-warm endpoint re-derived: 1040')

# ---------- 5. cost-71b sweep + receipts ----------
CHILD_71B = '00000000000000803202000000400000'
sweep71 = json.loads((OUT / 'class2-lane-cost71b-sweep-20261115.json').read_text())
assert sweep71['s6_child_hex'] == CHILD_71B
assert sweep71['s6_s7_edge_cost'] == 71
assert sweep71['win7_d10'] == 9 and sweep71['refuted_d10'] == 62 and sweep71['capped'] == 0
assert sweep71['total_nodes'] == 87586636
assert sweep71['win7_bits'] == [1, 14, 21, 32, 74, 94, 105, 109, 117]
tot71 = 0
seen71 = set()
win71 = set()
np71 = 0
for i in range(1, 10):
    for line in (OUT / f'class2-lane-cost71b-raw-batch{i}-20261115.jsonl').read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if 'control' in row:
            assert row['loss'] is False and row['nodes'] == 3402 and not row['capped']
            np71 += 1
            continue
        assert row['capped'] is False
        assert row['terminalStoneRange'] == [13, 17]
        assert row['bit'] not in seen71
        seen71.add(row['bit'])
        tot71 += row['nodes']
        if row['loss']:
            win71.add(row['bit'])
assert np71 == 9 and len(seen71) == 71 and tot71 == 87586636
assert win71 == {1, 14, 21, 32, 74, 94, 105, 109, 117}
det71 = [json.loads(l) for l in (OUT / 'class2-lane-cost71b-v16-determinism-rerun-20261115.jsonl')
         .read_text().splitlines() if l.strip()]
d71 = {r['bit']: r for r in det71 if 'bit' in r}
assert d71[32]['nodes'] == 8488319 and d71[32]['loss'] is True
assert d71[113]['nodes'] == 9070237 and d71[113]['loss'] is False
v15_71 = [json.loads(l) for l in (OUT / 'class2-lane-cost71b-v15-crosscheck-20261115.jsonl')
          .read_text().splitlines() if l.strip()]
p71 = [r for r in v15_71 if 'control' in r]
assert len(p71) == 2 and all(r['loss'] is False and r['nodes'] == 5949 for r in p71)
b71 = {r['bit']: r for r in v15_71 if 'bit' in r}
v71_expect = {109: 2323226, 105: 3864960, 21: 2576152, 1: 4375357, 117: 7210014,
              74: 6756758, 94: 5520204, 14: 14083030, 32: 18454344}
assert set(b71) == set(v71_expect)
for bb, nn in v71_expect.items():
    assert b71[bb]['loss'] is True and b71[bb]['nodes'] == nn, (bb, b71[bb]['nodes'])
print('CONTROL cost-71b sweep asserted: 71 candidates, 9 WIN7 + 62 REFUTED, '
      '87,586,636 nodes; det 32/113 node-exact; v15 anchors 9/9 '
      '(control JSONLs re-published in commit 86bbe2ef)')

rec71 = json.loads((OUT / 'class2-lane-cost71b-win7-certificates-20261115.json').read_text())
assert rec71['child_hex'] == CHILD_71B
certs71 = [c for c in rec71['certificates'] if c.get('verdict') == 'WIN7']
assert [c['bit'] for c in certs71] == [109, 21, 105]
R71 = {109: 32492, 21: 29242, 105: 38589}
S71 = {109: 51, 21: 52, 105: 54}
M71 = {109: '513b87f7b8edc6d1ebcb25c725d79789',
       21: '0bca8499e98e1a0197db2a6f6bd2d6ab',
       105: '7243ac5da980fbd8899fd5d93735e5ab'}
cv71 = int(CHILD_71B, 16)
c71b = {}
for c in certs71:
    assert c['rows'] == R71[c['bit']] and c['sub_roots_pass'] == S71[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['md5'] == M71[c['bit']]
    assert int(c['root_hex'], 16) == cv71 | (1 << c['bit'])
    c71b[c['bit']] = covers(int(c['root_hex'], 16))
print('CONTROL cost-71b receipts asserted: bits 109/21/105 (rows/sub-roots/union/md5/roots)')

# superseded after-cost-71b endpoint (1026) re-derived from raw records
s_old1026 = set(s_old1022)
for b in (109, 21, 105):
    s_old1026 |= c71b[b]
st_old1026, _, _, _ = summary_state(s_old1026)
assert st_old1026['solved_s6_in_manifest'] == 1026, st_old1026
print('CONTROL superseded after-cost-71b endpoint re-derived: 1026')

# ---------- 6. canonical sequential merge from the 69e v2 baseline ----------
PUB = {
    'cost70c': json.loads((OUT / 'class-frontier-cost70c-recompute-20261115.json')
                          .read_text())['cost70c_addition'],
    'cost60b_warm': json.loads((OUT / 'class-frontier-cost60b-warm-recompute-20261115.json')
                               .read_text())['cost60b_warm_addition'],
    'cost71b': json.loads((OUT / 'class-frontier-cost71b-recompute-20261115.json')
                          .read_text())['cost71b_addition'],
}
GROUPS = [
    ('cost70c', (94, 20, 23), c70c, cv70),
    ('cost60b_warm', tuple(WARM_ORDER), cwarm, cv60),
    ('cost71b', (109, 21, 105), c71b, cv71),
]
s_cur = set(s69v2)
group_additions = {}
stage_frontiers = {}
for gname, bits, gc, cv in GROUPS:
    per_bits = {}
    for bit in bits:
        cov = gc[bit]
        marg = cov - s_cur
        marg_m = marg & manifest
        entry = {
            'root_hex': format(cv | (1 << bit), '032x'),
            'covers': len(cov), 'marginal': len(marg),
            'marginal_in_manifest': len(marg_m),
            'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
        }
        pub = PUB[gname].get(str(bit))
        if pub:
            entry['published_stage_marginal'] = pub['marginal']
            entry['published_stage_marginal_in_manifest'] = pub['marginal_in_manifest']
            entry['marginal_reduced_vs_published'] = len(marg) < pub['marginal']
        per_bits[str(bit)] = entry
        s_cur |= marg
    stg, _, _, _ = summary_state(s_cur)
    stage_frontiers[gname] = {
        'solved_s6_in_manifest': stg['solved_s6_in_manifest'],
        'unique_remaining_s6': stg['unique_remaining_s6'],
        'sum_remaining_cost': stg['sum_remaining_cost'],
        's6_needed_by_open_classes': stg['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stg['cost_needed_by_open_classes'],
    }
    group_additions[gname] = per_bits
    print(f'AFTER {gname}: {json.dumps(stage_frontiers[gname])}')

# ---------- 7. final controls ----------
s_expected = set(s69v2)
for gname, bits, gc, cv in GROUPS:
    for bit in bits:
        s_expected |= gc[bit]
assert s_cur == s_expected, 'sequential replay must equal baseline union all covers'
assert s_old1022 <= s_cur and s_old1040 <= s_cur and s_old1026 <= s_cur, \
    'every superseded endpoint solved set must be contained in the merged frontier'
stF, remF, uniqF, demF = summary_state(s_cur)
print('AFTER merged:', json.dumps(stF, indent=1))

# ---------- 8. ranking + records ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(remF, 2)
class4 = best(remF, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-merged-after69ev2-70c-60bwarm-71b-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-cost69e-recompute-20261115 schema v2 '
                      '(solved 1023 / unique remaining 6824 / sum 537833 / open 5094/401556)',
    'method': 'merged replay of the three post-69e-v2 receipt groups on the current published '
              'baseline: the cost-69e v2 state (1023) is reproduced by runpy, the pre-v2 '
              'six-receipt state (1019) and the three superseded published endpoints '
              '(after-cost-70c 1022, after-cost-60b-warm 1040, after-cost-71b 1026) are '
              're-derived exactly from raw records (their scripts now fail their baseline '
              'asserts on main because the 69e v2 update postdates them), all three sweeps and '
              'receipt groups are asserted from their published records (70c: 70 candidates, '
              '13 WIN7 + 57 REFUTED, 100,935,666 nodes, det 86/66, v15 anchors 13/13, receipts '
              '94/20/23; 60b warm: sweep unverified 19, 17 warm certificates, cross-child '
              'duplicates 15/34 not re-added; 71b: 71 candidates, 9 WIN7 + 62 REFUTED, '
              '87,586,636 nodes, det 32/113, v15 anchors 9/9 - control JSONLs re-published in '
              'commit 86bbe2ef after being found missing - receipts 109/21/105), and all 23 '
              'receipts are re-added in canonical chronological order (70c -> 60b-warm -> 71b) '
              'with per-bit marginals re-derived from the growing union and compared with their '
              'published stage marginals (marginal_reduced_vs_published flags; the 71b bit-21 '
              'root duplicates the 60b-warm bit-22 root - duplicate-fold rule); the merged '
              'solved set equals the 69e v2 baseline union all 23 receipt covers and contains '
              'every superseded endpoint solved set',
    'chain_break': {
        'discovered': '2026-11-15 (this session)',
        'cause': 'the cost-69e layer was updated to v2 on main (recompute_frontier_cost69e_'
                 '20261115.py + class2-lane-cost69e-win7-certificates-20261114.json + '
                 'class-frontier-cost69e-recompute-20261115.json schema v2) folding all ten '
                 'cost-69e receipts (21/99/87/84/76/90 + warm rebuilds 89/94/108/116) and '
                 'moving the after-cost-69e endpoint 1019 -> 1023, without rebasing the '
                 'downstream scripts',
        'broken_scripts': [
            'recompute_frontier_cost70c_20261115.py (asserts the 1019 baseline; fails at line '
            '47 against current main - verified locally)',
            'recompute_frontier_cost60b_warm_20261115.py (runpy-extends the 70c script)',
            'recompute_frontier_cost71b_20261115.py (runpy-extends the 70c script)',
        ],
        'superseded_endpoints_reproduced_here': {
            'after_cost69e_pre_v2_six_receipts': 1019,
            'after_cost70c': 1022,
            'after_cost60b_warm': 1040,
            'after_cost71b': 1026,
        },
        'repair': 'this script re-derives every superseded endpoint from raw records and is '
                  'the canonical chain head from the 69e v2 baseline onward; the three '
                  'superseded scripts remain on main as historical stage documentation and '
                  'their failing asserts are an experiment fact, not a game-theoretic claim',
    },
    'controls': {
        'baseline_after_cost69e_v2': {'solved_in_manifest': 1023, 'unique_remaining': 6824,
                                      'sum_cost': 537833, 'open_s6': 5094, 'open_cost': 401556,
                                      'reproduced': True},
        'pre_v2_six_receipt_state_1019_reproduced': True,
        'superseded_1022_reproduced': True,
        'superseded_1040_reproduced': True,
        'superseded_1026_reproduced': True,
        'sweeps_asserted_from_raw_batches': True,
        'receipts_asserted_rows_subs_union_md5_roots': True,
        'sequential_replay_equals_baseline_union_all_covers': True,
        'superseded_endpoints_contained_in_merged': True,
    },
    'stage_frontiers': stage_frontiers,
    'group_additions': group_additions,
    'frontier_after_merged': {
        'solved_s6_in_manifest': stF['solved_s6_in_manifest'],
        'remaining_s5_orbits': stF['remaining_s5_orbits'],
        'unique_remaining_s6': stF['unique_remaining_s6'],
        'sum_remaining_cost': stF['sum_remaining_cost'],
        's6_needed_by_open_classes': stF['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stF['cost_needed_by_open_classes'],
        'demand_histogram_open_only': stF['hist'],
        'best_class2': class2[0],
        'audit_blocked_class2': next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'outstanding_not_folded': {
        'cost72_sweep': 'parallel lane in flight (9 raw batches + batches1-9 audit published; '
                        '2 WIN7-D10 bits 52/111; bit-111 certificate published; no completed '
                        'sweep record yet) - certificates without records are not receipts',
        'warm_rebuild_candidates_without_records': 'cost-61d bit-22 (= cost-71b bit-1 root), '
                                                   'cost-71b remaining WIN7 bits '
                                                   '1/14/32/74/94/117, and other unverified '
                                                   'WIN7 bits of earlier bands',
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only '
                            'absence of WIN7-D10; WIN7 certificates prove a win within depth 10 '
                            'from the 7-stone root only; 11x11 empty root / {49,60} / S2 '
                            '{59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-merged-cost60bwarm-cost71b-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-merged-cost60bwarm-cost71b-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remF.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-merged-cost60bwarm-cost71b-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-merged-cost60bwarm-cost71b-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next(c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED)),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
                        ('second class-2 target S5 (merged-lane parent)',
                         next(c for c in class2 if c['s5_hex'] == PARENT))):
        rows = remF.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = demF[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-merged)')
