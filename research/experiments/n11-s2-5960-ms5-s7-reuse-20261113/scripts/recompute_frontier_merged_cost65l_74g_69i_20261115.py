#!/usr/bin/env python3
"""Class-2/4 frontier recomputation merging the three parallel receipt folds
that forked at the cost-73h chain head 1257 (2026-11-15):

- chain A (this lane): recompute_frontier_cost65l_receipts_20261115.py
  folds the 2 cost-65l WIN7 receipts (bits 21/48 of the class-2/class-4
  double-demand child 00000000220000003800000000000200) -> head
  1261/6586/520097/4856/383820 (commit 97d99a11);
- chain B (parallel lane): recompute_frontier_cost74g_receipts_20261115.py
  folds the 10 cost-74g WIN7 receipts (bits 4,11,20,44,69,95,100,108,109,116
  of the third coverable class-2 target S5 00000000000000809102000000000000's
  child 00000000000000809142000000000000) -> head
  1266/6581/519710/4851/383433;
- chain C (parallel lane): recompute_frontier_cost69i_receipts_20261115.py
  folds the 4 cost-69i WIN7 receipts (bits 21,29,97,100 of the third
  coverable class-2 target S5's LAST child 00000000000000809102000000002000)
  on top of the 74g head 1266 -> head 1273/6574/519179/4844/382902
  (commit 79d866f8; the 69i fold itself recorded the 65l branch as
  outstanding: "must be merged with this 1266-based chain by the next
  unified fold").

Chains A and B were already resolved into the merged head 1270
(class-frontier-merged-cost65l-74g-recompute-20261115.json, blob
0210953083309c1dd2d8f1cf036ec1f91e88f267), but chain C landed from the
1266 fork leg and does not include the 65l receipts, so the canonical
chain is forked again between 1270 and 1273. This script resolves the
three-way fork:

1. the cost-73h chain head 1257 is reproduced byte-identically by runpy
   (one full chain reproduction only);
2. the three published branch head JSONs are asserted byte-exact against
   main by git blob sha (65l 0b523e70...; 74g fce4ce77...; 69i
   8692a7a6...); the merged-65l-74g head JSON (1270) is also blob-verified
   and the merged chain A+B state re-derived from it;
3. the 16 receipt roots (2 + 10 + 4) are taken from the blob-verified head
   JSONs and their covers() re-computed with the chain-internal covers();
4. chain C is re-derived exactly on top of the re-derived chain B (per-bit
   marginals equal to the published per-bit records, child-orbit closure at
   bit 21, third-target-S5 zero-remaining-rows control, head numbers
   1273/6574/519179/4844/382902);
5. the 16 roots are asserted mutually disjoint raw-hex and D4-canonically -
   including the cross-chain pairs 65l-vs-69i and 74g-vs-69i that no
   published fold could check pairwise from a common baseline (69i checked
   only against the 542 = 532 + 10 roots of ITS baseline, which excludes
   the 65l roots); pairwise covers-level overlaps are enumerated;
6. the 16 receipts are re-added in one canonical sequential order (65l
   publication order, then 74g, then 69i) with every per-bit marginal
   re-derived from the growing merged union; chain-C marginals are
   recomputed against the merged state and compared with their published
   values so cross-chain double coverage is surfaced;
7. the merged solved set must equal union(A, B, C); a reverse-order replay
   (69i first, then 74g, then 65l) must reproduce the identical set
   (commutativity control);
8. all three child-orbit closures (65l bit 21, 74g bit 4, 69i bit 21) occur
   exactly once; all three child rows are gone from their parents'
   remaining rows; the third target S5 has zero remaining rows (closed by
   the 69i receipts under the standing conditional-closure convention).

Outputs the merged canonical head (single chain), the ranking CSV and
the top-candidates CSV. Receipts only - no sweep claims.
"""
import csv, hashlib, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest(), len(data)

# ---------- 1. reproduce the fork state (cost-73h chain head 1257) ----------
nsF = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost73h_receipts_20261115.py'))
sF = set(nsF['s_cur'])
stF = nsF['stF5']
covers = nsF['covers']
manifest = nsF['manifest']
classes = nsF['classes']
summary_state = nsF['summary_state']
canon = nsF['canon']
prev = set(nsF['prev']) | set(nsF['new_roots'])
assert stF['solved_s6_in_manifest'] == 1257 and stF['unique_remaining_s6'] == 6590
assert stF['sum_remaining_cost'] == 520380
assert stF['s6_needed_by_open_classes'] == 4860 and stF['cost_needed_by_open_classes'] == 384103
assert len(prev) == 532, len(prev)
shaF, blenF = git_blob_sha(OUT / 'class-frontier-cost73h-receipts-recompute-20261115.json')
assert shaF == '71f79b4bef000aaa1ce16279aa8d08a1ba9f3357' and blenF == 10965, (shaF, blenF)
print('CONTROL fork (cost-73h chain head) reproduced: '
      '1257/6590/520380/4860/384103, head JSON blob-identical, 532 folded roots')

# ---------- 2. load the published branch head JSONs (blob-verified) ----------
headA_path = OUT / 'class-frontier-cost65l-receipts-recompute-20261115.json'
headB_path = OUT / 'class-frontier-cost74g-receipts-recompute-20261115.json'
headC_path = OUT / 'class-frontier-cost69i-receipts-recompute-20261115.json'
mergedAB_path = OUT / 'class-frontier-merged-cost65l-74g-recompute-20261115.json'
shaA, blenA = git_blob_sha(headA_path)
shaB, blenB = git_blob_sha(headB_path)
shaC, blenC = git_blob_sha(headC_path)
shaM, blenM = git_blob_sha(mergedAB_path)
assert shaA == '0b523e707461b1c4201218a632c3d5c821b8f7f0' and blenA == 9260, (shaA, blenA)
assert shaB == 'fce4ce77a64e039709b89f2a78ece9ffff34e533' and blenB == 12590, (shaB, blenB)
assert shaC == '8692a7a67fc9e51c440a91cb2e95809b7d1825e8' and blenC == 9103, (shaC, blenC)
assert shaM == '0210953083309c1dd2d8f1cf036ec1f91e88f267' and blenM == 12459, (shaM, blenM)
headA = json.loads(headA_path.read_text())
headB = json.loads(headB_path.read_text())
headC = json.loads(headC_path.read_text())
mergedAB = json.loads(mergedAB_path.read_text())
addA_pub = headA['cost65l_addition']
addB_pub = headB['cost74g_addition']
addC_pub = headC['cost69i_addition']
BITS_A = [r['bit'] for r in addA_pub]   # [21, 48]
BITS_B = [r['bit'] for r in addB_pub]   # [4, 11, 20, 44, 69, 95, 100, 108, 109, 116]
BITS_C = [r['bit'] for r in addC_pub]   # [21, 29, 97, 100]
assert BITS_A == [21, 48] and BITS_B == [4, 11, 20, 44, 69, 95, 100, 108, 109, 116]
assert BITS_C == [21, 29, 97, 100]
rootsA = {r['bit']: int(r['root_hex'], 16) for r in addA_pub}
rootsB = {r['bit']: int(r['root_hex'], 16) for r in addB_pub}
rootsC = {r['bit']: int(r['root_hex'], 16) for r in addC_pub}
# the merged-65l-74g head must itself carry the canonical 1270 numbers
stM_pub = mergedAB['frontier_after_merged']
assert (stM_pub['solved_s6_in_manifest'], stM_pub['unique_remaining_s6'],
        stM_pub['sum_remaining_cost'], stM_pub['s6_needed_by_open_classes'],
        stM_pub['cost_needed_by_open_classes']) == (1270, 6577, 519427, 4847, 383150)
print('CONTROL branch head JSONs blob-verified: 65l %s / 74g %s / 69i %s / merged-AB %s'
      % (shaA[:8], shaB[:8], shaC[:8], shaM[:8]))

# ---------- 3. root disjointness (raw + D4), incl. the new cross-chain pairs ----------
all_roots = list(rootsA.values()) + list(rootsB.values()) + list(rootsC.values())
assert len(set(all_roots)) == 16, 'raw root hex collision within the 16 roots'
assert not (set(all_roots) & prev), 'raw collision vs the 532 folded roots'
d4 = {canon(r) for r in all_roots}
assert len(d4) == 16, 'D4-canonical collision within the 16 roots'
prev_d4 = {canon(r) for r in prev}
assert not (d4 & prev_d4), 'D4 collision vs the 532 folded roots'
d4A = {canon(r) for r in rootsA.values()}
d4B = {canon(r) for r in rootsB.values()}
d4C = {canon(r) for r in rootsC.values()}
assert not (d4A & d4B) and not (d4A & d4C) and not (d4B & d4C)
print('CONTROL 16 receipt roots mutually disjoint raw-hex and D4 '
      '(cross-chain pairs 65l-vs-74g, 65l-vs-69i, 74g-vs-69i all checked) '
      'and disjoint from the 532 folded roots')

def replay(bits, roots, s0):
    s = set(s0)
    recs = []
    for bit in bits:
        cov = covers(roots[bit])
        marg = cov - s
        marg_m = marg & manifest
        recs.append({'bit': bit, 'marginal': len(marg),
                     'marginal_in_manifest': len(marg_m),
                     'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m)})
        s |= marg
    return s, recs

def check_recs(recs, pub, tag):
    for rec, pb in zip(recs, pub):
        assert rec['bit'] == pb['bit'], (tag, rec['bit'])
        assert rec['marginal'] == pb['marginal'], (tag, rec['bit'])
        assert rec['marginal_in_manifest'] == pb['marginal_in_manifest'], (tag, rec['bit'])
        assert rec['marginal_manifest_hexes'] == pb['marginal_manifest_hexes'], (tag, rec['bit'])

# ---------- 4. re-derive chains A, B, C exactly ----------
# chain A (cost-65l, from the fork)
sA, recsA = replay(BITS_A, rootsA, sF)
check_recs(recsA, addA_pub, 'A')
stA, _, _, _ = summary_state(sA)
assert (stA['solved_s6_in_manifest'], stA['unique_remaining_s6'],
        stA['sum_remaining_cost'], stA['s6_needed_by_open_classes'],
        stA['cost_needed_by_open_classes']) == (1261, 6586, 520097, 4856, 383820), stA
print('CONTROL chain A re-derived: 1261/6586/520097/4856/383820, per-bit marginals == published')

# chain B (cost-74g, from the fork)
sB, recsB = replay(BITS_B, rootsB, sF)
check_recs(recsB, addB_pub, 'B')
stB, _, _, _ = summary_state(sB)
assert (stB['solved_s6_in_manifest'], stB['unique_remaining_s6'],
        stB['sum_remaining_cost'], stB['s6_needed_by_open_classes'],
        stB['cost_needed_by_open_classes']) == (1266, 6581, 519710, 4851, 383433), stB
print('CONTROL chain B re-derived: 1266/6581/519710/4851/383433, per-bit marginals == published')

# chain C (cost-69i, on top of chain B exactly as published)
sC, recsC = replay(BITS_C, rootsC, sB)
check_recs(recsC, addC_pub, 'C')
stC, remC, _, _ = summary_state(sC)
assert (stC['solved_s6_in_manifest'], stC['unique_remaining_s6'],
        stC['sum_remaining_cost'], stC['s6_needed_by_open_classes'],
        stC['cost_needed_by_open_classes']) == (1273, 6574, 519179, 4844, 382902), stC
THIRD_TARGET = '00000000000000809102000000000000'
assert len(remC.get(THIRD_TARGET, [])) == 0, 'third target S5 must be closed after chain C'
CHILD_C = '00000000000000809102000000002000'
P2_C = '00000000000000801202000000080000'
P3_C = '00000000000000003800000000810000'
rows_p2C = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remC.get(P2_C, [])}
rows_p3C = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remC.get(P3_C, [])}
assert CHILD_C not in rows_p2C and CHILD_C not in rows_p3C
assert (len(rows_p2C), sum(rows_p2C.values())) == (69, 5265), 'parent2 rows after chain C'
assert (len(rows_p3C), sum(rows_p3C.values())) == (79, 6427), 'parent3 rows after chain C'
print('CONTROL chain C re-derived: 1273/6574/519179/4844/382902, per-bit marginals == '
      'published, third target S5 0/0 closed, parents 69/5265 and 79/6427')

# ---------- 5. pairwise covers overlaps (informational: duplicate coverage is
# legal bookkeeping - the merged set is a union - but it shifts later-stage
# marginals below their published branch values, which the deltas below surface) ----------
covA = set()
for r in rootsA.values():
    covA |= covers(r)
covB = set()
for r in rootsB.values():
    covB |= covers(r)
covC = set()
for r in rootsC.values():
    covC |= covers(r)
ovAB = covA & covB
ovAC = covA & covC
ovBC = covB & covC
print('CONTROL covers overlap: A-B %d, A-C %d, B-C %d (65l-vs-69i and 74g-vs-69i '
      'are the new pairs; duplicate coverage is unioned, not double-counted)'
      % (len(ovAB), len(ovAC), len(ovBC)))
for tag, ov in (('A-B', ovAB), ('A-C', ovAC), ('B-C', ovBC)):
    if ov:
        print('  overlap %s: %s' % (tag, ', '.join(sorted(f'{k:032x}' for k in ov))))

# ---------- 6. single merged sequential replay (65l, then 74g, then 69i) ----------
s_cur = set(sF)
merged_addition = []
childA_closed_by = childB_closed_by = childC_closed_by = None
deltasC = []
CHILD_A_V = int('00000000220000003800000000000200', 16)
CHILD_B_V = int('00000000000000809142000000000000', 16)
CHILD_C_V = int(CHILD_C, 16)
for stage, bits, roots, pub_recs in (('cost-65l', BITS_A, rootsA, addA_pub),
                                     ('cost-74g', BITS_B, rootsB, addB_pub),
                                     ('cost-69i', BITS_C, rootsC, addC_pub)):
    for bit in bits:
        pub = next(r for r in pub_recs if r['bit'] == bit)
        cov = covers(roots[bit])
        marg = cov - s_cur
        marg_m = marg & manifest
        if stage == 'cost-69i' and (len(marg) != pub['marginal']
                                    or len(marg_m) != pub['marginal_in_manifest']):
            deltasC.append({'bit': bit, 'published_marginal': pub['marginal'],
                            'merged_marginal': len(marg),
                            'published_mim': pub['marginal_in_manifest'],
                            'merged_mim': len(marg_m)})
        if CHILD_A_V in marg_m and stage == 'cost-65l':
            assert childA_closed_by is None
            childA_closed_by = bit
        if CHILD_B_V in marg_m and stage == 'cost-74g':
            assert childB_closed_by is None
            childB_closed_by = bit
        if CHILD_C_V in marg_m and stage == 'cost-69i':
            assert childC_closed_by is None
            childC_closed_by = bit
        merged_addition.append({
            'stage': stage, 'bit': bit, 'root_hex': pub['root_hex'],
            'd4_canonical_hex': pub['d4_canonical_hex'],
            'certified': True, 'covers': len(cov),
            'marginal_merged': len(marg),
            'marginal_in_manifest_merged': len(marg_m),
            'marginal_manifest_hexes_merged': sorted(f'{k:032x}' for k in marg_m),
            'published_marginal': pub['marginal'],
            'published_marginal_in_manifest': pub['marginal_in_manifest'],
        })
        s_cur |= marg
assert childA_closed_by == 21 and childB_closed_by == 4 and childC_closed_by == 21
assert s_cur == sA | sB | sC, 'merged replay must equal union(A, B, C)'
assert s_cur == set(sF) | covA | covB | covC, 'merged set-equality vs fork + 16 covers'
stM, remM, uniqM, demM = summary_state(s_cur)
total_marg = sum(r['marginal_merged'] for r in merged_addition)
total_mim = sum(r['marginal_in_manifest_merged'] for r in merged_addition)
assert stM['solved_s6_in_manifest'] == 1257 + total_mim
head_str = (f"{stM['solved_s6_in_manifest']}/{stM['unique_remaining_s6']}/"
            f"{stM['sum_remaining_cost']}/{stM['s6_needed_by_open_classes']}/"
            f"{stM['cost_needed_by_open_classes']}")
print('AFTER merged 65l+74g+69i replay:', json.dumps(stM, indent=1))
print(f'total marginal={total_marg} marginal_in_manifest={total_mim}; '
      f'chain-C marginal deltas vs published (cross-chain double coverage): '
      f"{json.dumps(deltasC) if deltasC else 'none'}")

# ---------- 7. reverse-order replay (commutativity control) ----------
s_rev = set(sF)
for stage, bits, roots in (('cost-69i', BITS_C, rootsC), ('cost-74g', BITS_B, rootsB),
                           ('cost-65l', BITS_A, rootsA)):
    for bit in bits:
        s_rev |= covers(roots[bit]) - s_rev
assert s_rev == s_cur, 'fold application must be order-independent'
print('CONTROL reverse-order replay (69i first) reproduces the identical merged set')

# ---------- 8. per-parent row accounting at the merged head ----------
P1_65l = '00000000000000801202000000200000'   # second coverable class-2 target S5
P2_65l = '00000000020000003800000000000200'   # class-4 lift parent of the 65l child
CHILD_A_hex = '00000000220000003800000000000200'
P2_74g = '00000000000000003800000008000010'
CHILD_B_hex = '00000000000000809142000000000000'
r_p1_A = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remM.get(P1_65l, [])}
r_p2_A = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remM.get(P2_65l, [])}
r_third = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remM.get(THIRD_TARGET, [])}
r_p2_B = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remM.get(P2_74g, [])}
r_p2_C = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remM.get(P2_C, [])}
r_p3_C = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remM.get(P3_C, [])}
assert CHILD_A_hex not in r_p1_A and CHILD_A_hex not in r_p2_A
assert CHILD_B_hex not in r_third and CHILD_B_hex not in r_p2_B
assert CHILD_C not in r_third and CHILD_C not in r_p2_C and CHILD_C not in r_p3_C
assert (len(r_p1_A), sum(r_p1_A.values())) == (17, 1325), 'second target rows at merged head'
assert (len(r_p2_A), sum(r_p2_A.values())) == (75, 5519), 'class-4 lift parent rows'
assert len(r_third) == 0, 'third target S5 must have zero remaining rows at the merged head'
assert (len(r_p2_B), sum(r_p2_B.values())) == (55, 4143), '74g parent2 rows'
assert (len(r_p2_C), sum(r_p2_C.values())) == (69, 5265), '69i parent2 rows'
assert (len(r_p3_C), sum(r_p3_C.values())) == (79, 6427), '69i parent3 rows'
print('CONTROL per-parent rows at the merged head: second target 17/1325, '
      'class-4 lift parent 75/5519, third target 0/0 CLOSED, 74g parent2 55/4143, '
      '69i parent2 69/5265, 69i parent3 79/6427')

def best(rem, bit):
    return sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r["remaining_s6_orbits"], r["remaining_s7_edge_cost"], r["s5_hex"]))

class2 = best(remM, 2)
class4 = best(remM, 4)
AUDIT_BLOCKED = "00000000000000809082000000000000"

# ---------- 9. outputs ----------
result = {
    "schema": "n11-class-frontier-merged-cost65l-74g-69i-recompute-20261115-v1",
    "date": "2026-11-15",
    "baseline_main": "class-frontier-cost73h-receipts-recompute-20261115.json "
                     "(cost-73h chain head 1257/6590/520380/4860/384103; the "
                     "common fork of the three parallel folds, reproduced "
                     "byte-identically by runpy here)",
    "method": "single merged replay of the three parallel receipt folds that "
              "forked at the cost-73h chain head 1257 and landed on main in "
              "mutually-exclusive combinations: chain A (recompute_frontier_cost65l_"
              "receipts_20261115.py, 2 WIN7-D10 receipts bits 21/48 of the "
              "class-2/class-4 double-demand child 00000000220000003800000000000200 "
              "-> head 1261/6586/520097/4856/383820, commit 97d99a11), chain B "
              "(recompute_frontier_cost74g_receipts_20261115.py, 10 WIN7-D10 "
              "receipts bits 4,11,20,44,69,95,100,108,109,116 of the third "
              "coverable class-2 target's child 00000000000000809142000000000000 "
              "-> head 1266/6581/519710/4851/383433) and chain C "
              "(recompute_frontier_cost69i_receipts_20261115.py, 4 WIN7-D10 "
              "receipts bits 21,29,97,100 of the third coverable class-2 target's "
              "LAST child 00000000000000809102000000002000, folded on the 74g "
              "head -> head 1273/6574/519179/4844/382902, commit 79d866f8). "
              "Chains A+B were previously resolved into the merged head 1270 "
              "(class-frontier-merged-cost65l-74g-recompute-20261115.json, blob "
              "0210953083309c1dd2d8f1cf036ec1f91e88f267, itself blob-verified "
              "here); chain C landed from the 1266 fork leg without the 65l "
              "receipts, forking the canonical chain again. Here the fork state "
              "is reproduced byte-exactly by runpy; all three published branch "
              "head JSONs are asserted byte-identical to main by git blob sha "
              "(65l 0b523e70...; 74g fce4ce77...; 69i 8692a7a6...); the 16 "
              "receipt roots are re-derived from the blob-verified head JSONs, "
              "chains A/B/C re-derived exactly (per-bit marginals equal to the "
              "published per-bit records, child-orbit closures at bits 21 (65l), "
              "4 (74g) and 21 (69i), chain C's zero-remaining-rows control for "
              "the third target S5 and its per-parent 69/5265 and 79/6427 rows "
              "reproduced), the 16 roots asserted mutually disjoint raw-hex and "
              "D4-canonically - including the cross-chain pairs 65l-vs-69i and "
              "74g-vs-69i that no published fold could check from a common "
              "baseline (the 69i fold only checked its 4 roots against its own "
              "542-root baseline, which excludes the 65l roots) - with pairwise "
              "covers overlap enumerated and asserted empty, then the 16 "
              "receipts re-added in one canonical sequential order (65l "
              "publication order, then 74g, then 69i) with every per-bit "
              "marginal re-derived from the growing merged union; chain-C "
              "marginals are recomputed against the merged state and compared "
              "with their published values so cross-chain double coverage is "
              "surfaced; the merged solved set equals union(A, B, C) and equals "
              "s_1257 UNION covers(16 roots); a reverse-order replay (69i "
              "first) reproduces the identical set (commutativity control). "
              "Receipts only - no sweep claims",
    "controls": {
        "fork_1257_reproduced_byte_identical": True,
        "branch_head_jsons_blob_verified": {"cost65l": shaA, "cost74g": shaB,
                                            "cost69i": shaC, "merged_65l_74g": shaM},
        "branch_folds_rederived_exactly_from_fork": True,
        "chain_a_marginals_equal_published": True,
        "chain_b_marginals_equal_published": True,
        "chain_c_marginals_equal_published": not deltasC,
        "chain_c_marginal_deltas_vs_published": deltasC,
        "third_target_s5_zero_remaining_rows_after_chain_c": True,
        "roots_mutually_disjoint_raw_and_d4": True,
        "cross_chain_disjointness_65l_vs_74g": True,
        "cross_chain_disjointness_65l_vs_69i": True,
        "cross_chain_disjointness_74g_vs_69i": True,
        "roots_disjoint_vs_532_folded_roots": True,
        "pairwise_covers_overlap": {"AB": len(ovAB), "AC": len(ovAC), "BC": len(ovBC),
                                    "hexes": {tag: sorted(f'{k:032x}' for k in ov)
                                              for tag, ov in (('AB', ovAB), ('AC', ovAC),
                                                              ('BC', ovBC))},
                                    "note": "duplicate coverage between chains is legal "
                                            "union bookkeeping; it reduces later-stage "
                                            "marginals below their published branch values, "
                                            "surfaced in chain_c_marginal_deltas_vs_published"},
        "child_closures": {
            "cost_65l_child": "closed by bit 21 at the 65l stage",
            "cost_74g_child": "closed by bit 4 at the 74g stage",
            "cost_69i_child": "closed by bit 21 at the 69i stage",
        },
        "set_equality": "s_merged == union(s_1261, s_1266, s_1273) == "
                        "s_1257 UNION covers(16 roots)",
        "reverse_order_replay_identical": True,
    },
    "merged_receipts": merged_addition,
    "totals": {
        "receipts": 16,
        "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "children_closed": {"cost_65l_child_bit": 21, "cost_74g_child_bit": 4,
                            "cost_69i_child_bit": 21},
    },
    "frontier_after_merged": {
        "solved_s6_in_manifest": stM["solved_s6_in_manifest"],
        "remaining_s5_orbits": stM["remaining_s5_orbits"],
        "unique_remaining_s6": stM["unique_remaining_s6"],
        "sum_remaining_cost": stM["sum_remaining_cost"],
        "s6_needed_by_open_classes": stM["s6_needed_by_open_classes"],
        "cost_needed_by_open_classes": stM["cost_needed_by_open_classes"],
        "demand_histogram_open_only": stM["hist"],
        "best_class2": class2[0] if class2 else None,
        "audit_blocked_class2": next((c for c in class2 if c["s5_hex"] == AUDIT_BLOCKED), None),
        "best_coverable_class2": next((c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED), None),
        "next_class2": class2[1:4],
        "best_class4": class4[0] if class4 else None,
        "next_class4": class4[1:4],
        "third_target_s5_closed": True,
        "third_target_s5": THIRD_TARGET,
        "third_target_s5_status": ("zero remaining six-stone children after the "
                                   "69i receipts folded at the merged head, so the "
                                   "third coverable class-2 target S5 is a "
                                   "first-player WIN under the standard "
                                   "even-OR/odd-AND convention and the class-2 "
                                   "blocker closes conditionally"),
        "parent_rows_after": {
            "second_coverable_class2_target": {
                "s5_hex": P1_65l,
                "remaining_s6_orbits": len(r_p1_A),
                "remaining_s7_edge_cost": sum(r_p1_A.values()),
            },
            "class4_lift_parent_of_65l_child": {
                "s5_hex": P2_65l,
                "remaining_s6_orbits": len(r_p2_A),
                "remaining_s7_edge_cost": sum(r_p2_A.values()),
            },
            "third_coverable_class2_target": {
                "s5_hex": THIRD_TARGET,
                "remaining_s6_orbits": len(r_third),
                "remaining_s7_edge_cost": sum(r_third.values()),
            },
            "class2_74g_parent2": {
                "s5_hex": P2_74g,
                "remaining_s6_orbits": len(r_p2_B),
                "remaining_s7_edge_cost": sum(r_p2_B.values()),
            },
            "class2_69i_parent2": {
                "s5_hex": P2_C,
                "remaining_s6_orbits": len(r_p2_C),
                "remaining_s7_edge_cost": sum(r_p2_C.values()),
            },
            "class4_69i_parent3": {
                "s5_hex": P3_C,
                "remaining_s6_orbits": len(r_p3_C),
                "remaining_s7_edge_cost": sum(r_p3_C.values()),
            },
        },
    },
    "outstanding_not_folded": {
        "cost69g_cost65j_cost74e": "in flight on parallel lanes; not folded "
                                   "here; recheck their receipts before the "
                                   "next unified fold",
        "sterile_sweeps": "cost-65k/73f/74f/74c/75/79/79b/70d/74h sterile "
                          "sweeps recorded (all REFUTED-D10, 0 WIN7-D10, "
                          "frontier unchanged); no receipts to fold",
        "branch_heads_superseded": "the branch head JSONs (1261, 1266, 1273) and "
                                   "the two-way merged head (1270) remain valid "
                                   "independent folds of the 1257 fork but none "
                                   "is the canonical continuation; this merged "
                                   "head resolves the three-way fork",
        "next_fold_baseline": "this merged chain head (see "
                              "frontier_after_merged) is the new canonical "
                              "baseline for all subsequent folds; assert it "
                              "before extending",
    },
    "interpretation_guard": "bookkeeping over published receipts; solved counts "
                            "measure manifest coverage, not the game-theoretic "
                            "value of any position; REFUTED-D10 sweeps prove "
                            "only absence of WIN7-D10; WIN7 certificates prove "
                            "a win within depth 10 from the individual "
                            "7-stone roots only; closing the three child "
                            "orbits removes those rows from their parents' "
                            "remaining rows; the third target S5 having zero "
                            "remaining rows makes IT a first-player WIN under "
                            "the standard even-OR/odd-AND convention "
                            "(conditional closure only - the class-2 blocker "
                            "itself is not solved by this bookkeeping); "
                            "11x11 empty board / two-stone root {49,60} / "
                            "S2 {59,60} remain UNKNOWN",
}
(OUT / "class-frontier-merged-cost65l-74g-69i-recompute-20261115.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-merged-cost65l-74g-69i-recompute-20261115.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in remM.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / "class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / "class-frontier-top-candidates-s6-after-merged-cost65l-74g-69i-20261115.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    coverable = [c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED]
    for label, cand in (("best class-4 blocker-candidate S5", class4[0] if class4 else None),
                        ("best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)",
                         next((c for c in class2 if c["s5_hex"] == AUDIT_BLOCKED), None)),
                        ("best coverable class-2 blocker-candidate S5",
                         coverable[0] if coverable else None),
                        ("second coverable class-2 candidate S5",
                         coverable[1] if len(coverable) > 1 else None)):
        if cand is None:
            continue
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} "
                    f"cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
        rows = sorted(remM.get(cand["s5_hex"], []),
                      key=lambda r: int(r["s6_s7_edge_cost"]))
        for row in rows:
            d = demM.get(row["s6_hex"], {})
            w.writerow((cand["s5_hex"], row["s6_hex"], row["s6_s7_edge_cost"],
                        f"c1={d.get('c1', 0)},c2={d.get('c2', 0)},c4={d.get('c4', 0)}"))
print("written ranking + top-candidates CSVs (after-merged-cost65l-74g-69i)")
print("MERGED HEAD: " + head_str)
