#!/usr/bin/env python3
"""Class-2/4 frontier recomputation merging the two parallel receipt folds
that forked at the cost-67c chain head 1219 (2026-11-15):

- chain A: recompute_frontier_cost78a_receipts_20261115.py folds the 5
  cost-78a WIN7 receipts (bits 36/20/29/8/109) -> head
  1225/6622/522699/4892/386422 (commit 1691d9bb, 03:07:50Z);
- chain B: recompute_frontier_cost69h_receipts_20261115.py folds the 2
  cost-69h WIN7 receipts (bits 58/96) -> head
  1221/6626/523035/4896/386758 (commit 3d2faf3b, 03:11:17Z).

Both fold scripts have been run to completion in their own subprocesses
(each runpy-reproduces the full cost-67c chain to the common 1219 fork
state, re-verifies every published input file against main by git blob
sha, re-derives the sweep audit from the raw batches, asserts the
certificate bytes and root disjointness, and asserts its published head
JSON byte-identical to main). This merge step re-loads the two published
head JSONs, asserts their git blob shas byte-exact against main, then
re-derives both folds from scratch in one process:

1. the cost-67c chain head 1219 is reproduced byte-identically by runpy
   (one full chain reproduction only);
2. the 7 receipt roots (5 cost-78a + 2 cost-69h) are taken from the two
   blob-verified head JSONs and their covers() re-computed with the
   chain-internal covers();
3. chain A is re-derived exactly (s_1225 == s_1219 UNION covers(5 roots),
   per-bit marginals in publication order [36,20,29,8,109] equal to the
   published per-bit records, child-orbit closure at bit 36, head numbers
   1225/6622/522699/4892/386422); chain B likewise ([58,96], bit 58,
   1221/6626/523035/4896/386758);
4. the 7 roots are asserted mutually disjoint raw-hex and D4-canonically;
   the branch additions and covers-level overlap are enumerated;
5. the 7 receipts are re-added in one canonical sequential order (78a
   publication order, then 69h published order) with every per-bit
   marginal re-derived from the growing merged union; cross-chain double
   coverage would surface as a chain-B marginal delta (enumerated);
6. the merged solved set must equal union(A, B); a reverse-order replay
   (69h first) must reproduce the identical set (commutativity control);
7. both child-orbit closures (bit 36, bit 58) occur exactly once; both
   child rows are gone from their parents' remaining rows.

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

# ---------- 1. reproduce the fork state (cost-67c chain head 1219) ----------
nsF = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost67c_receipts_20261115.py'))
sF = set(nsF['s_cur'])
stF = nsF['stG']
covers = nsF['covers']
manifest = nsF['manifest']
classes = nsF['classes']
summary_state = nsF['summary_state']
canon = nsF['canon']
assert stF['solved_s6_in_manifest'] == 1219 and stF['unique_remaining_s6'] == 6628
assert stF['sum_remaining_cost'] == 523173
assert stF['s6_needed_by_open_classes'] == 4898 and stF['cost_needed_by_open_classes'] == 386896
sha67, blen67 = git_blob_sha(OUT / 'class-frontier-cost67c-receipts-recompute-20261115.json')
assert sha67 == '6d187f48420a9b66d527c3c0fb2764ad5f63235a' and blen67 == 9323
print('CONTROL fork (cost-67c chain head) reproduced: '
      '1219/6628/523173/4898/386896, head JSON blob-identical')

# ---------- 2. load the two published branch head JSONs (blob-verified) ----------
headA_path = OUT / 'class-frontier-cost78a-receipts-recompute-20261115.json'
headB_path = OUT / 'class-frontier-cost69h-receipts-recompute-20261115.json'
shaA, _ = git_blob_sha(headA_path)
shaB, _ = git_blob_sha(headB_path)
assert shaA == '3938bb1668c7dfb80049cdac45f8dee50514c064', shaA
# headB is the parallel lane's REBASED v2 head JSON (the cost-69h receipts
# fold rebased on the 78a head 1225 -> 1227/6620/522561/4890/386284,
# commits aa6cdcf4..01877255, schema ...-v2); this merge independently
# re-derives that head from the 1219 fork.
assert shaB == 'd25eb3a00f73cf9ca34fc2816d28045c1e23f3ae', shaB
headA = json.loads(headA_path.read_text())
headB = json.loads(headB_path.read_text())
addA_pub = headA['cost78a_addition']
addB_pub = headB['cost69h_addition']
BITS_A = [r['bit'] for r in addA_pub]   # [36, 20, 29, 8, 109]
BITS_B = [r['bit'] for r in addB_pub]   # [58, 96]
assert BITS_A == [36, 20, 29, 8, 109] and BITS_B == [58, 96]
rootsA = {r['bit']: int(r['root_hex'], 16) for r in addA_pub}
rootsB = {r['bit']: int(r['root_hex'], 16) for r in addB_pub}
print('CONTROL branch head JSONs blob-verified: 78a %s / 69h %s'
      % (shaA[:8], shaB[:8]))

# ---------- 3. root disjointness (raw + D4) ----------
assert len(set(rootsA.values())) == 5 and len(set(rootsB.values())) == 2
assert not (set(rootsA.values()) & set(rootsB.values())), 'raw root hex collision'
d4A = {canon(r) for r in rootsA.values()}
d4B = {canon(r) for r in rootsB.values()}
assert not (d4A & d4B), 'D4-canonical root collision'
print('CONTROL 7 receipt roots mutually disjoint raw and D4-canonically')

# ---------- 4. re-derive chain A and chain B exactly ----------
def replay(bits, roots, s0):
    s = set(s0)
    recs = []
    child_closed_by = None
    for bit in bits:
        cov = covers(roots[bit])
        marg = cov - s
        marg_m = marg & manifest
        recs.append({'bit': bit, 'marginal': len(marg),
                     'marginal_in_manifest': len(marg_m),
                     'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m)})
        s |= marg
    return s, recs, child_closed_by

CHILD_A_V = int('00000000000000809102000000400000', 16)
CHILD_B_V = int('0000000000000080120a000000200000', 16)

# chain A
sA, recsA, _ = replay(BITS_A, rootsA, sF)
for rec, pub in zip(recsA, addA_pub):
    assert rec['bit'] == pub['bit']
    assert rec['marginal'] == pub['marginal'], rec['bit']
    assert rec['marginal_in_manifest'] == pub['marginal_in_manifest'], rec['bit']
    assert rec['marginal_manifest_hexes'] == pub['marginal_manifest_hexes'], rec['bit']
# child-orbit closure: the child is newly solved exactly by the bit-36
# receipt's in-manifest marginal (first in publication order)
marg36_m = (covers(rootsA[36]) - sF) & manifest
assert CHILD_A_V in marg36_m
stA, _, _, _ = summary_state(sA)
assert (stA['solved_s6_in_manifest'], stA['unique_remaining_s6'],
        stA['sum_remaining_cost'], stA['s6_needed_by_open_classes'],
        stA['cost_needed_by_open_classes']) == (1225, 6622, 522699, 4892, 386422), stA
covA_all = set()
for r in rootsA.values():
    covA_all |= covers(r)
assert sA == set(sF) | covA_all, 'chain A set-equality'
print('CONTROL chain A re-derived: 1225/6622/522699/4892/386422, '
      'per-bit marginals == published, child closed by bit 36')

# chain B
sB, recsB, _ = replay(BITS_B, rootsB, sF)
for rec, pub in zip(recsB, addB_pub):
    assert rec['bit'] == pub['bit']
    assert rec['marginal'] == pub['marginal'], rec['bit']
    assert rec['marginal_in_manifest'] == pub['marginal_in_manifest'], rec['bit']
    assert rec['marginal_manifest_hexes'] == pub['marginal_manifest_hexes'], rec['bit']
marg58_m = (covers(rootsB[58]) - sF) & manifest
assert CHILD_B_V in marg58_m
stB, _, _, _ = summary_state(sB)
assert (stB['solved_s6_in_manifest'], stB['unique_remaining_s6'],
        stB['sum_remaining_cost'], stB['s6_needed_by_open_classes'],
        stB['cost_needed_by_open_classes']) == (1221, 6626, 523035, 4896, 386758), stB
covB_all = set()
for r in rootsB.values():
    covB_all |= covers(r)
assert sB == set(sF) | covB_all, 'chain B set-equality'
print('CONTROL chain B re-derived: 1221/6626/523035/4896/386758, '
      'per-bit marginals == published, child closed by bit 58')

# ---------- 5. branch additions, overlap, covers-level overlap ----------
addA = sA - sF
addB = sB - sF
overlap = addA & addB
cov_overlap = covA_all & covB_all
print(f'CONTROL addA={len(addA)} addB={len(addB)} raw overlap={len(overlap)} '
      f'covers overlap={len(cov_overlap)}'
      + (': ' + ', '.join(sorted(f'{k:032x}' for k in cov_overlap)) if cov_overlap else ''))

# ---------- 6. single merged sequential replay (78a then 69h) ----------
s_cur = set(sF)
merged_addition = []
childA_closed_by = childB_closed_by = None
deltas = []
for stage, bits, roots, pub_recs in (('cost-78a', BITS_A, rootsA, addA_pub),
                                     ('cost-69h', BITS_B, rootsB, addB_pub)):
    for bit in bits:
        pub = next(r for r in pub_recs if r['bit'] == bit)
        cov = covers(roots[bit])
        marg = cov - s_cur
        marg_m = marg & manifest
        if stage == 'cost-69h' and (len(marg) != pub['marginal']
                                    or len(marg_m) != pub['marginal_in_manifest']):
            deltas.append({'bit': bit, 'published_marginal': pub['marginal'],
                           'merged_marginal': len(marg),
                           'published_mim': pub['marginal_in_manifest'],
                           'merged_mim': len(marg_m)})
        if CHILD_A_V in marg_m and stage == 'cost-78a':
            assert childA_closed_by is None
            childA_closed_by = bit
        if CHILD_B_V in marg_m and stage == 'cost-69h':
            assert childB_closed_by is None
            childB_closed_by = bit
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
assert childA_closed_by == 36 and childB_closed_by == 58
assert s_cur == sA | sB, 'merged replay must equal union(A, B)'
assert s_cur == set(sF) | covA_all | covB_all, 'merged set-equality vs fork + 7 covers'
stM, remM, uniqM, demM = summary_state(s_cur)
# third-party agreement control: the parallel lane's rebased 69h head JSON
# (schema v2, blob-verified above) holds the identical merged frontier
hb = headB['frontier_after_cost69h']
assert (stM['solved_s6_in_manifest'], stM['unique_remaining_s6'],
        stM['sum_remaining_cost'], stM['s6_needed_by_open_classes'],
        stM['cost_needed_by_open_classes']) == (
    hb['solved_s6_in_manifest'], hb['unique_remaining_s6'],
    hb['sum_remaining_cost'], hb['s6_needed_by_open_classes'],
    hb['cost_needed_by_open_classes']), 'merged head must equal the rebased parallel head'
print('CONTROL merged head equals the parallel lane\'s rebased v2 head JSON '
      'numbers: %d/%d/%d/%d/%d' % (
          hb['solved_s6_in_manifest'], hb['unique_remaining_s6'],
          hb['sum_remaining_cost'], hb['s6_needed_by_open_classes'],
          hb['cost_needed_by_open_classes']))
print('AFTER merged 78a+69h replay:', json.dumps(stM, indent=1))
print('chain-B marginal deltas vs published (cross-chain double coverage):',
      json.dumps(deltas) if deltas else 'none')

# ---------- 7. reverse-order replay (commutativity control) ----------
s_rev = set(sF)
for stage, bits, roots in (('cost-69h', BITS_B, rootsB), ('cost-78a', BITS_A, rootsA)):
    for bit in bits:
        s_rev |= covers(roots[bit]) - s_rev
assert s_rev == s_cur, 'fold application must be order-independent'
print('CONTROL reverse-order replay (69h first) reproduces the identical merged set')

# ---------- 8. per-parent row accounting at the merged head ----------
P1_69 = '00000000000000801202000000200000'
P2_69 = '0000000000000080120a000000000000'
CHILD_B_hex = '0000000000000080120a000000200000'
P1_78 = '00000000000000809102000000000000'
P2_78 = '00000000000000801202000100000000'
CHILD_A_hex = '00000000000000809102000000400000'
r_p1 = {r['s6_hex'] for r in remM.get(P1_69, [])}
r_p2 = {r['s6_hex'] for r in remM.get(P2_69, [])}
r_p1_78 = {r['s6_hex'] for r in remM.get(P1_78, [])}
r_p2_78 = {r['s6_hex'] for r in remM.get(P2_78, [])}
assert CHILD_B_hex not in r_p1 and CHILD_B_hex not in r_p2
assert CHILD_A_hex not in r_p1_78 and CHILD_A_hex not in r_p2_78

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
    "schema": "n11-class-frontier-merged-cost78a-69h-recompute-20261115-v1",
    "date": "2026-11-15",
    "baseline_main": "class-frontier-cost67c-receipts-recompute-20261115.json "
                     "(cost-67c chain head 1219/6628/523173/4898/386896; the "
                     "common fork of the two parallel folds, reproduced "
                     "byte-identically by runpy here)",
    "method": "single merged replay of the two parallel receipt folds that "
              "forked at the cost-67c chain head 1219: the fork state is "
              "reproduced byte-exactly by runpy; both published branch head "
              "JSONs are asserted byte-identical to main by git blob sha "
              "(78a 3938bb16...; 69h d25eb3a0... = the parallel lane's "
              "REBASED v2 head JSON, its cost-69h receipts fold rebased on "
              "the 78a head 1225, resolving the 1219 head fork); both "
              "branch folds have "
              "separately been run to completion by their published fold "
              "scripts (each re-verifies every published input against main, "
              "re-derives the sweep audit from the raw batches, asserts the "
              "certificate bytes and asserts its head JSON byte-identical); "
              "here the 7 receipt roots are re-derived from the two "
              "blob-verified head JSONs, both folds re-derived exactly from "
              "the fork state (per-bit marginals equal to the published "
              "per-bit records, child-orbit closures at bits 36 and 58, head "
              "numbers 1225/6622/522699/4892/386422 and "
              "1221/6626/523035/4896/386758), the 7 roots asserted mutually "
              "disjoint raw-hex and D4-canonically, then the 7 receipts "
              "re-added in one canonical sequential order (78a publication "
              "order then 69h published order) with every per-bit marginal "
              "re-derived from the growing merged union; chain-A marginals "
              "reproduce their published values exactly, chain-B marginals "
              "are recomputed against the merged state and compared with "
              "their published values so cross-chain double coverage is "
              "surfaced; the merged solved set equals union(A, B) and equals "
              "s_1219 UNION covers(7 roots); a reverse-order replay "
              "reproduces the identical set (commutativity control); the "
              "merged head numbers are asserted equal to the parallel "
              "lane's rebased v2 head JSON numbers (third independent "
              "agreement on the resolved canonical head "
              "1227/6620/522561/4890/386284). "
              "Receipts only - no sweep claims",
    "controls": {
        "fork_1219_reproduced_byte_identical": True,
        "branch_head_jsons_blob_verified": {"cost78a": shaA, "cost69h_rebased_v2": shaB},
        "merged_head_equals_parallel_rebased_head_numbers": True,
        "branch_folds_rederived_exactly_from_fork": True,
        "chain_a_marginals_equal_published": True,
        "chain_b_marginals_equal_published": not deltas,
        "chain_b_marginal_deltas_vs_published": deltas,
        "branch_addition_sizes": {"addA": len(addA), "addB": len(addB)},
        "branch_addition_raw_overlap": len(overlap),
        "covers_overlap_between_folds": len(cov_overlap),
        "covers_overlap_hexes": sorted(f'{k:032x}' for k in cov_overlap),
        "roots_mutually_disjoint_raw_and_d4": True,
        "child_closures": {
            "cost_78a_child": "closed by bit 36 at the 78a stage",
            "cost_69h_child": "closed by bit 58 at the 69h stage",
        },
        "set_equality": "s_merged == s_1225 UNION s_1221 == s_1219 UNION covers(7 roots)",
        "reverse_order_replay_identical": True,
    },
    "merged_receipts": merged_addition,
    "totals": {
        "receipts": 7,
        "total_marginal": sum(r['marginal_merged'] for r in merged_addition),
        "total_marginal_in_manifest": sum(r['marginal_in_manifest_merged'] for r in merged_addition),
        "children_closed": {"cost_78a_child_bit": 36, "cost_69h_child_bit": 58},
    },
    "frontier_after_merged": {
        "solved_s6_in_manifest": stM["solved_s6_in_manifest"],
        "remaining_s5_orbits": stM["remaining_s5_orbits"],
        "unique_remaining_s6": stM["unique_remaining_s6"],
        "sum_remaining_cost": stM["sum_remaining_cost"],
        "s6_needed_by_open_classes": stM["s6_needed_by_open_classes"],
        "cost_needed_by_open_classes": stM["cost_needed_by_open_classes"],
        "demand_histogram_open_only": stM["hist"],
        "best_class2": class2[0],
        "audit_blocked_class2": next((c for c in class2 if c["s5_hex"] == AUDIT_BLOCKED), None),
        "best_coverable_class2": next(c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED),
        "next_class2": class2[1:4],
        "best_class4": class4[0],
        "next_class4": class4[1:4],
        "parent_rows_after": {
            "second_coverable_class2_target": {
                "s5_hex": P1_69,
                "remaining_s6_orbits": len(r_p1),
                "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in remM.get(P1_69, [])),
            },
            "class2_69h_parent2": {
                "s5_hex": P2_69,
                "remaining_s6_orbits": len(r_p2),
                "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in remM.get(P2_69, [])),
            },
            "third_coverable_class2_target": {
                "s5_hex": P1_78,
                "remaining_s6_orbits": len(r_p1_78),
                "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in remM.get(P1_78, [])),
            },
            "class2_78a_parent2": {
                "s5_hex": P2_78,
                "remaining_s6_orbits": len(r_p2_78),
                "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in remM.get(P2_78, [])),
            },
        },
    },
    "outstanding_not_folded": {
        "cost65l": "2 WIN7-D10 receipts (bits 21/48) with extraction/verify "
                   "artifacts but no certificate bodies on main; not folded",
        "cost69g_cost65j_cost74e": "in flight on parallel lanes; not folded "
                                   "here; recheck their receipts before the "
                                   "next unified fold",
        "sterile_sweeps": "cost-65k/73f/74f/74c/75/79/79b/70d sterile sweeps "
                          "recorded (all REFUTED-D10, 0 WIN7-D10, frontier "
                          "unchanged); no receipts to fold",
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
                            "7-stone roots only; closing the two child orbits "
                            "removes those rows from their parents' remaining "
                            "rows but does not solve any S5 parent; 11x11 "
                            "empty board / two-stone root {49,60} / S2 {59,60} "
                            "/ class 2 / class 4 remain UNKNOWN",
}
(OUT / "class-frontier-merged-cost78a-69h-recompute-20261115.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-merged-cost78a-69h-recompute-20261115.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in remM.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / "class-frontier-s5-ranking-after-merged-cost78a-69h-20261115.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / "class-frontier-top-candidates-s6-after-merged-cost78a-69h-20261115.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    coverable = [c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED]
    for label, cand in (("best class-4 blocker-candidate S5", class4[0]),
                        ("best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)",
                         next((c for c in class2 if c["s5_hex"] == AUDIT_BLOCKED), None)),
                        ("best coverable class-2 blocker-candidate S5", coverable[0]),
                        ("second coverable class-2 candidate S5",
                         coverable[1] if len(coverable) > 1 else None)):
        if cand is None:
            continue
        rows = remM.get(cand["s5_hex"], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
        for row in sorted(rows, key=lambda r: int(r["s6_s7_edge_cost"])):
            d = demM[row["s6_hex"]]
            w.writerow((cand["s5_hex"], row["s6_hex"], row["s6_s7_edge_cost"],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print("written ranking + top-candidates CSVs (after-merged-cost78a-69h)")
