#!/usr/bin/env python3
"""Class-2/4 frontier recomputation merging the two parallel receipt folds
that forked at the cost-73h chain head 1257 (2026-11-15):

- chain A (this lane): recompute_frontier_cost65l_receipts_20261115.py
  folds the 2 cost-65l WIN7 receipts (bits 21/48 of the class-2/class-4
  double-demand child 00000000220000003800000000000200) -> head
  1261/6586/520097/4856/383820 (commit 97d99a11);
- chain B (parallel lane): recompute_frontier_cost74g_receipts_20261115.py
  folds the 10 cost-74g WIN7 receipts (bits 4,11,20,44,69,95,100,108,109,116
  of the third coverable class-2 target S5 00000000000000809102000000000000's
  child 00000000000000809142000000000000) -> head
  1266/6581/519710/4851/383433.

Neither branch fold includes the other's receipts (both landed from the
same 1257 fork within minutes of each other), so neither branch head is
the canonical continuation: this merge re-loads the two published branch
head JSONs, asserts their git blob shas byte-exact against main, then
re-derives both folds from scratch in one process and resolves the fork:

1. the cost-73h chain head 1257 is reproduced byte-identically by runpy
   (one full chain reproduction only);
2. the 12 receipt roots (2 cost-65l + 10 cost-74g) are taken from the two
   blob-verified head JSONs and their covers() re-computed with the
   chain-internal covers();
3. chain A is re-derived exactly (per-bit marginals equal to the published
   per-bit records, child-orbit closure at bit 21, head numbers
   1261/6586/520097/4856/383820); chain B likewise (bits
   [4,11,20,44,69,95,100,108,109,116], bit 4,
   1266/6581/519710/4851/383433);
4. the 12 roots are asserted mutually disjoint raw-hex and D4-canonically
   (the cross-branch pair 65l-vs-74g was never checked by either branch
   fold: each branch only asserted disjointness against the 532 roots
   folded through cost-73h); the branch additions and covers-level
   overlap are enumerated;
5. the 12 receipts are re-added in one canonical sequential order (65l
   publication order, then 74g publication order) with every per-bit
   marginal re-derived from the growing merged union; cross-chain double
   coverage would surface as a chain-B marginal delta (enumerated);
6. the merged solved set must equal union(A, B); a reverse-order replay
   (74g first) must reproduce the identical set (commutativity control);
7. both child-orbit closures (bit 21, bit 4) occur exactly once; both
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

# ---------- 2. load the two published branch head JSONs (blob-verified) ----------
headA_path = OUT / 'class-frontier-cost65l-receipts-recompute-20261115.json'
headB_path = OUT / 'class-frontier-cost74g-receipts-recompute-20261115.json'
shaA, blenA = git_blob_sha(headA_path)
shaB, blenB = git_blob_sha(headB_path)
assert shaA == '0b523e707461b1c4201218a632c3d5c821b8f7f0' and blenA == 9260, (shaA, blenA)
assert shaB == 'fce4ce77a64e039709b89f2a78ece9ffff34e533' and blenB == 12590, (shaB, blenB)
headA = json.loads(headA_path.read_text())
headB = json.loads(headB_path.read_text())
addA_pub = headA['cost65l_addition']
addB_pub = headB['cost74g_addition']
BITS_A = [r['bit'] for r in addA_pub]   # [21, 48]
BITS_B = [r['bit'] for r in addB_pub]   # [4, 11, 20, 44, 69, 95, 100, 108, 109, 116]
assert BITS_A == [21, 48] and BITS_B == [4, 11, 20, 44, 69, 95, 100, 108, 109, 116]
rootsA = {r['bit']: int(r['root_hex'], 16) for r in addA_pub}
rootsB = {r['bit']: int(r['root_hex'], 16) for r in addB_pub}
print('CONTROL branch head JSONs blob-verified: 65l %s / 74g %s'
      % (shaA[:8], shaB[:8]))

# ---------- 3. root disjointness (raw + D4), incl. the cross-branch pair ----------
assert len(set(rootsA.values())) == 2 and len(set(rootsB.values())) == 10
assert not (set(rootsA.values()) & set(rootsB.values())), 'raw root hex collision'
assert not (set(rootsA.values()) & prev) and not (set(rootsB.values()) & prev)
d4A = {canon(r) for r in rootsA.values()}
d4B = {canon(r) for r in rootsB.values()}
assert not (d4A & d4B), 'D4-canonical cross-branch root collision'
prev_d4 = {canon(r) for r in prev}
assert not (d4A & prev_d4) and not (d4B & prev_d4)
print('CONTROL 12 receipt roots mutually disjoint (65l-vs-74g cross-branch '
      'pair included) and disjoint from the 532 folded roots, raw and D4')

# ---------- 4. re-derive chain A and chain B exactly ----------
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

CHILD_A_V = int('00000000220000003800000000000200', 16)
CHILD_B_V = int('00000000000000809142000000000000', 16)

# chain A (cost-65l)
sA, recsA = replay(BITS_A, rootsA, sF)
for rec, pub in zip(recsA, addA_pub):
    assert rec['bit'] == pub['bit']
    assert rec['marginal'] == pub['marginal'], rec['bit']
    assert rec['marginal_in_manifest'] == pub['marginal_in_manifest'], rec['bit']
    assert rec['marginal_manifest_hexes'] == pub['marginal_manifest_hexes'], rec['bit']
marg21_m = (covers(rootsA[21]) - sF) & manifest
assert CHILD_A_V in marg21_m
stA, _, _, _ = summary_state(sA)
assert (stA['solved_s6_in_manifest'], stA['unique_remaining_s6'],
        stA['sum_remaining_cost'], stA['s6_needed_by_open_classes'],
        stA['cost_needed_by_open_classes']) == (1261, 6586, 520097, 4856, 383820), stA
covA_all = set()
for r in rootsA.values():
    covA_all |= covers(r)
assert sA == set(sF) | covA_all, 'chain A set-equality'
print('CONTROL chain A re-derived: 1261/6586/520097/4856/383820, '
      'per-bit marginals == published, child closed by bit 21')

# chain B (cost-74g)
sB, recsB = replay(BITS_B, rootsB, sF)
for rec, pub in zip(recsB, addB_pub):
    assert rec['bit'] == pub['bit']
    assert rec['marginal'] == pub['marginal'], rec['bit']
    assert rec['marginal_in_manifest'] == pub['marginal_in_manifest'], rec['bit']
    assert rec['marginal_manifest_hexes'] == pub['marginal_manifest_hexes'], rec['bit']
marg4_m = (covers(rootsB[4]) - sF) & manifest
assert CHILD_B_V in marg4_m
stB, _, _, _ = summary_state(sB)
assert (stB['solved_s6_in_manifest'], stB['unique_remaining_s6'],
        stB['sum_remaining_cost'], stB['s6_needed_by_open_classes'],
        stB['cost_needed_by_open_classes']) == (1266, 6581, 519710, 4851, 383433), stB
covB_all = set()
for r in rootsB.values():
    covB_all |= covers(r)
assert sB == set(sF) | covB_all, 'chain B set-equality'
print('CONTROL chain B re-derived: 1266/6581/519710/4851/383433, '
      'per-bit marginals == published, child closed by bit 4')

# ---------- 5. branch additions, overlap, covers-level overlap ----------
addA = sA - sF
addB = sB - sF
overlap = addA & addB
cov_overlap = covA_all & covB_all
print(f'CONTROL addA={len(addA)} addB={len(addB)} raw overlap={len(overlap)} '
      f'covers overlap={len(cov_overlap)}'
      + (': ' + ', '.join(sorted(f'{k:032x}' for k in cov_overlap)) if cov_overlap else ''))

# ---------- 6. single merged sequential replay (65l then 74g) ----------
s_cur = set(sF)
merged_addition = []
childA_closed_by = childB_closed_by = None
deltas = []
for stage, bits, roots, pub_recs in (('cost-65l', BITS_A, rootsA, addA_pub),
                                     ('cost-74g', BITS_B, rootsB, addB_pub)):
    for bit in bits:
        pub = next(r for r in pub_recs if r['bit'] == bit)
        cov = covers(roots[bit])
        marg = cov - s_cur
        marg_m = marg & manifest
        if stage == 'cost-74g' and (len(marg) != pub['marginal']
                                    or len(marg_m) != pub['marginal_in_manifest']):
            deltas.append({'bit': bit, 'published_marginal': pub['marginal'],
                           'merged_marginal': len(marg),
                           'published_mim': pub['marginal_in_manifest'],
                           'merged_mim': len(marg_m)})
        if CHILD_A_V in marg_m and stage == 'cost-65l':
            assert childA_closed_by is None
            childA_closed_by = bit
        if CHILD_B_V in marg_m and stage == 'cost-74g':
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
assert childA_closed_by == 21 and childB_closed_by == 4
assert s_cur == sA | sB, 'merged replay must equal union(A, B)'
assert s_cur == set(sF) | covA_all | covB_all, 'merged set-equality vs fork + 12 covers'
stM, remM, uniqM, demM = summary_state(s_cur)
total_marg = sum(r['marginal_merged'] for r in merged_addition)
total_mim = sum(r['marginal_in_manifest_merged'] for r in merged_addition)
assert stM['solved_s6_in_manifest'] == 1257 + total_mim
head_str = (f"{stM['solved_s6_in_manifest']}/{stM['unique_remaining_s6']}/"
            f"{stM['sum_remaining_cost']}/{stM['s6_needed_by_open_classes']}/"
            f"{stM['cost_needed_by_open_classes']}")
print('AFTER merged 65l+74g replay:', json.dumps(stM, indent=1))
print(f'total marginal={total_marg} marginal_in_manifest={total_mim}; '
      f'chain-B marginal deltas vs published (cross-chain double coverage): '
      f"{json.dumps(deltas) if deltas else 'none'}")

# ---------- 7. reverse-order replay (commutativity control) ----------
s_rev = set(sF)
for stage, bits, roots in (('cost-74g', BITS_B, rootsB), ('cost-65l', BITS_A, rootsA)):
    for bit in bits:
        s_rev |= covers(roots[bit]) - s_rev
assert s_rev == s_cur, 'fold application must be order-independent'
print('CONTROL reverse-order replay (74g first) reproduces the identical merged set')

# ---------- 8. per-parent row accounting at the merged head ----------
P1_65l = '00000000000000801202000000200000'   # second coverable class-2 target S5
P2_65l = '00000000020000003800000000000200'   # class-4 lift parent of the 65l child
CHILD_A_hex = '00000000220000003800000000000200'
P1_74g = '00000000000000809102000000000000'   # third coverable class-2 target S5
P2_74g = '00000000000000003800000008000010'
CHILD_B_hex = '00000000000000809142000000000000'
r_p1_A = {r['s6_hex'] for r in remM.get(P1_65l, [])}
r_p2_A = {r['s6_hex'] for r in remM.get(P2_65l, [])}
r_p1_B = {r['s6_hex'] for r in remM.get(P1_74g, [])}
r_p2_B = {r['s6_hex'] for r in remM.get(P2_74g, [])}
assert CHILD_A_hex not in r_p1_A and CHILD_A_hex not in r_p2_A
assert CHILD_B_hex not in r_p1_B and CHILD_B_hex not in r_p2_B
assert len(r_p1_A) == 17 and sum(int(r['s6_s7_edge_cost']) for r in remM.get(P1_65l, [])) == 1325
assert len(r_p2_A) == 75 and sum(int(r['s6_s7_edge_cost']) for r in remM.get(P2_65l, [])) == 5519
assert len(r_p1_B) == 1 and sum(int(r['s6_s7_edge_cost']) for r in remM.get(P1_74g, [])) == 69
assert len(r_p2_B) == 55 and sum(int(r['s6_s7_edge_cost']) for r in remM.get(P2_74g, [])) == 4143
print('CONTROL per-parent rows at the merged head: second target 17/1325, '
      'class-4 lift parent 75/5519, third target 1/69, 74g parent2 55/4143')

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
    "schema": "n11-class-frontier-merged-cost65l-74g-recompute-20261115-v1",
    "date": "2026-11-15",
    "baseline_main": "class-frontier-cost73h-receipts-recompute-20261115.json "
                     "(cost-73h chain head 1257/6590/520380/4860/384103; the "
                     "common fork of the two parallel folds, reproduced "
                     "byte-identically by runpy here)",
    "method": "single merged replay of the two parallel receipt folds that "
              "forked at the cost-73h chain head 1257 and both landed on "
              "main without including each other's receipts: chain A "
              "(recompute_frontier_cost65l_receipts_20261115.py, 2 WIN7-D10 "
              "receipts bits 21/48 of the class-2/class-4 double-demand "
              "child 00000000220000003800000000000200 -> head "
              "1261/6586/520097/4856/383820, commit 97d99a11) and chain B "
              "(recompute_frontier_cost74g_receipts_20261115.py, 10 WIN7-D10 "
              "receipts bits 4,11,20,44,69,95,100,108,109,116 of the third "
              "coverable class-2 target's child 00000000000000809142000000000000 "
              "-> head 1266/6581/519710/4851/383433). The fork state is "
              "reproduced byte-exactly by runpy; both published branch head "
              "JSONs are asserted byte-identical to main by git blob sha "
              "(65l 0b523e70...; 74g fce4ce77...); both branch folds have "
              "separately been run to completion by their published fold "
              "scripts, and in this session the 74g fold script was "
              "additionally re-run end-to-end in a fresh mirror (all "
              "controls PASS, three outputs byte-identical to main); here "
              "the 12 receipt roots are re-derived from the two "
              "blob-verified head JSONs, both folds re-derived exactly "
              "from the fork state (per-bit marginals equal to the "
              "published per-bit records, child-orbit closures at bits 21 "
              "and 4, head numbers 1261/6586/520097/4856/383820 and "
              "1266/6581/519710/4851/383433), the 12 roots asserted mutually "
              "disjoint raw-hex and D4-canonically - including the "
              "cross-branch 65l-vs-74g pair that neither branch fold could "
              "have checked (each branch only asserted disjointness against "
              "the 532 roots folded through cost-73h) - then the 12 "
              "receipts re-added in one canonical sequential order (65l "
              "publication order then 74g publication order) with every "
              "per-bit marginal re-derived from the growing merged union; "
              "chain-A marginals reproduce their published values exactly, "
              "chain-B marginals are recomputed against the merged state "
              "and compared with their published values so cross-chain "
              "double coverage is surfaced; the merged solved set equals "
              "union(A, B) and equals s_1257 UNION covers(12 roots); a "
              "reverse-order replay reproduces the identical set "
              "(commutativity control). Receipts only - no sweep claims",
    "controls": {
        "fork_1257_reproduced_byte_identical": True,
        "branch_head_jsons_blob_verified": {"cost65l": shaA, "cost74g": shaB},
        "branch_folds_rederived_exactly_from_fork": True,
        "chain_a_marginals_equal_published": True,
        "chain_b_marginals_equal_published": not deltas,
        "chain_b_marginal_deltas_vs_published": deltas,
        "branch_addition_sizes": {"addA": len(addA), "addB": len(addB)},
        "branch_addition_raw_overlap": len(overlap),
        "covers_overlap_between_folds": len(cov_overlap),
        "covers_overlap_hexes": sorted(f'{k:032x}' for k in cov_overlap),
        "roots_mutually_disjoint_raw_and_d4": True,
        "cross_branch_disjointness_65l_vs_74g": True,
        "roots_disjoint_vs_532_folded_roots": True,
        "child_closures": {
            "cost_65l_child": "closed by bit 21 at the 65l stage",
            "cost_74g_child": "closed by bit 4 at the 74g stage",
        },
        "set_equality": "s_merged == s_1261 UNION s_1266 == s_1257 UNION covers(12 roots)",
        "reverse_order_replay_identical": True,
    },
    "merged_receipts": merged_addition,
    "totals": {
        "receipts": 12,
        "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "children_closed": {"cost_65l_child_bit": 21, "cost_74g_child_bit": 4},
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
                "s5_hex": P1_65l,
                "remaining_s6_orbits": len(r_p1_A),
                "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in remM.get(P1_65l, [])),
            },
            "class4_lift_parent_of_65l_child": {
                "s5_hex": P2_65l,
                "remaining_s6_orbits": len(r_p2_A),
                "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in remM.get(P2_65l, [])),
            },
            "third_coverable_class2_target": {
                "s5_hex": P1_74g,
                "remaining_s6_orbits": len(r_p1_B),
                "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in remM.get(P1_74g, [])),
            },
            "class2_74g_parent2": {
                "s5_hex": P2_74g,
                "remaining_s6_orbits": len(r_p2_B),
                "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in remM.get(P2_74g, [])),
            },
        },
    },
    "outstanding_not_folded": {
        "cost69g_cost65j_cost74e": "in flight on parallel lanes; not folded "
                                   "here; recheck their receipts before the "
                                   "next unified fold",
        "sterile_sweeps": "cost-65k/73f/74f/74c/75/79/79b/70d sterile sweeps "
                          "recorded (all REFUTED-D10, 0 WIN7-D10, frontier "
                          "unchanged); no receipts to fold",
        "branch_heads_superseded": "the two branch head JSONs (1261 and "
                                   "1266) remain valid independent folds "
                                   "of the 1257 fork but neither is the "
                                   "canonical continuation; this merged "
                                   "head resolves the fork",
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
                            "/ class 1 / class 2 / class 4 remain UNKNOWN",
}
(OUT / "class-frontier-merged-cost65l-74g-recompute-20261115.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-merged-cost65l-74g-recompute-20261115.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in remM.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / "class-frontier-s5-ranking-after-merged-cost65l-74g-20261115.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / "class-frontier-top-candidates-s6-after-merged-cost65l-74g-20261115.csv").open(
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
print("written ranking + top-candidates CSVs (after-merged-cost65l-74g)")
print("MERGED HEAD:", head_str)
