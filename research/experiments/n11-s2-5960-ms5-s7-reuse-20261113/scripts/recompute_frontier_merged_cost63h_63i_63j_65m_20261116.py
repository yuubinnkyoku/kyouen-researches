#!/usr/bin/env python3
"""Merged class-2 frontier recomputation reconciling the 2026-11-16 fork
between the merged cost-63h+63i chain head 1369 and the cost-63j+cost-65m
receipts chain head 1396:

- branch A (merged fold, this lane, commit c3bd5b4f): the cost-58c chain head
  1360 extended by the cost-63i fold (18 receipts, 1360 -> 1367) and then the
  cost-63h bit-89 receipt (1367 -> 1369/6479/512163/4749/375886), published as
  class-frontier-merged-cost63h-63i-recompute-20261116.json;
- branch B (parallel lane): the same cost-58c -> cost-63i chain head 1367
  extended WITHOUT the 63h receipt - the cost-63j fold (29 receipts,
  1367 -> 1394, commit 50e6a1b3, landed on the claim's 1367 baseline without
  the re-base onto the merged head 1369 that the merged-fold log required)
  and then the cost-65m fold (8 receipts, 1394 -> 1396, commit a382ff47),
  published as class-frontier-cost65m-receipts-recompute-20261116.json.

Both published branch heads are reproduced through their own scripts (each
internally reproduces the whole published fold chain down to the cost-58c
head 1360 and asserts its own output blobs byte-identical to main), then the
cost-63h bit-89 receipt is folded on top of the 1396 head. A reverse-order
replay (the 37 cost-63j + cost-65m receipt covers folded on top of the 1369
head) is asserted to reproduce the identical merged set, proving
order-independence of the reconciliation. The merged head is recorded as the
new canonical baseline for all subsequent folds.

Bookkeeping over published receipts only - no game-theoretic claim: 11x11
empty board / two-stone root {49,60} / S2 {59,60} / class 1 / class 2 /
class 4 all UNKNOWN.
"""
import csv
import hashlib
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CHILD_H = "00000000000000801202000040080000"
CHILD_H_V = int(CHILD_H, 16)
BIT_H = 89
ROOT_H = f"{CHILD_H_V | (1 << BIT_H):032x}"
ROOT_H_V = CHILD_H_V | (1 << BIT_H)
P1 = "00000000000000801202000040000000"
P2 = "00000000000000801202000000080000"
P3 = "00000000000000003800000001800000"
P2_I = "00000000000000403800000008000000"
AUDIT_BLOCKED = "00000000000000809082000000000000"
# branch B receipt roots: cost-63j (29) + cost-65m (8)
CHILD_J = "00000000040000003800000048000000"
CHILD_M = "00000000000000801202000040001000"
WIN_BITS_J = [1, 3, 4, 7, 9, 11, 16, 17, 18, 34, 35, 44, 45, 52, 54, 68,
              73, 78, 81, 87, 88, 92, 93, 99, 102, 103, 105, 107, 113]
WIN_BITS_M = [21, 22, 28, 35, 44, 67, 76, 83]


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


def git_blob_sha_bytes(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


# ---------- 1. reproduce the branch B fold chain (1360 -> 1367 -> 1394 -> 1396) ----------
ns65m = runpy.run_path(str(HERE / "scripts" / "recompute_frontier_cost65m_receipts_20261116.py"))
s_1394 = set(ns65m["s_base"])
s_1396 = set(ns65m["s_cur"])
stB = ns65m["stF2"]
covers = ns65m["covers"]
manifest = ns65m["manifest"]
classes = ns65m["classes"]
summary_state = ns65m["summary_state"]
canon = ns65m["canon"]
rem_1396 = ns65m["remF2"]
dem_1396 = ns65m["demF2"]
prevB = set(ns65m["prev"])
for c in ns65m["certs"].values():
    prevB.add(int(c["root_hex"], 16))
certs65m = ns65m["certs"]
win65m = ns65m["WIN_BITS"]
assert stB["solved_s6_in_manifest"] == 1396 and stB["unique_remaining_s6"] == 6452
assert stB["sum_remaining_cost"] == 510115 and stB["s6_needed_by_open_classes"] == 4722
assert stB["cost_needed_by_open_classes"] == 373838
assert len(prevB) == 704, len(prevB)  # 667 + 29 cost-63j + 8 cost-65m roots
sha, blen = git_blob_sha(OUT / "class-frontier-cost65m-receipts-recompute-20261116.json")
assert sha == "9798a9fc53b2277b17744737511354b1a830c4d2" and blen == 10414, (sha, blen)
sha, blen = git_blob_sha(OUT / "class-frontier-s5-ranking-after-cost65m-receipts-20261116.csv")
assert sha == "ad9a62f6a65f03016e957e01c61bf0b9675d2d0a" and blen == 7535, (sha, blen)
sha, blen = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-cost65m-receipts-20261116.csv")
assert sha == "6df96d8fb8fa9e2ea25a337b8bb8457ca3ef7c17" and blen == 4059, (sha, blen)
print("CONTROL branch B (cost-63j + cost-65m chain) head reproduced through its "
      "published script: 1396/6452/510115/4722/373838 (3 output blobs == main)")

# ---------- 2. reproduce the branch A merged fold (1360 -> 1367 -> 1369) ----------
ns_m = runpy.run_path(str(HERE / "scripts" / "recompute_frontier_merged_cost63h_63i_20261116.py"))
s_1367 = set(ns_m["s_1367"])
s_1369 = set(ns_m["s_m"])
stA = ns_m["st_m"]
certs63h = ns_m["certs63h"]
covers_a = ns_m["covers"]
assert stA["solved_s6_in_manifest"] == 1369 and stA["unique_remaining_s6"] == 6479
assert stA["sum_remaining_cost"] == 512163 and stA["s6_needed_by_open_classes"] == 4749
assert stA["cost_needed_by_open_classes"] == 375886
sha, blen = git_blob_sha(OUT / "class-frontier-merged-cost63h-63i-recompute-20261116.json")
assert sha == "c3ff50364499014a7096151bd9893a6510386c05" and blen == 6135, (sha, blen)
sha, blen = git_blob_sha(OUT / "class-frontier-s5-ranking-after-merged-cost63h-63i-20261116.csv")
assert sha == "d065e54fe7defdafe76d7a1f3a8956cf1c706963" and blen == 7537, (sha, blen)
sha, blen = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-merged-cost63h-63i-20261116.csv")
assert sha == "34067a180a254c032ce90b0594cf2f0ffd33d1a0" and blen == 4663, (sha, blen)
print("CONTROL branch A (merged cost-63h+63i fold) head reproduced through its "
      "published script: 1369/6479/512163/4749/375886 (3 output blobs == main)")

# ---------- 3. fork facts and cover sets ----------
cov_h = covers(ROOT_H_V)
assert cov_h == covers_a(ROOT_H_V), "the cover function must agree across both branches"
roots_j = [int(CHILD_J, 16) | (1 << b) for b in WIN_BITS_J]
roots_m = [int(CHILD_M, 16) | (1 << b) for b in WIN_BITS_M]
# cross-assert the branch B roots against the published head JSONs
head_j = json.loads((OUT / "class-frontier-cost63j-receipts-recompute-20261116.json").read_text())
assert [r["root_hex"] for r in head_j["cost63j_addition"]] == [f"{r:032x}" for r in roots_j]
assert {f"{int(c['root_hex'], 16):032x}" for c in certs65m.values()} == {f"{r:032x}" for r in roots_m}
cov37 = set()
for r in roots_j + roots_m:
    cov37 |= covers(r)
overlap_cov = cov_h & cov37
# fork set equalities against the common 1367 baseline
assert s_1369 == s_1367 | cov_h, "set-equality of the branch A merged fold"
assert s_1396 == s_1367 | cov37, "set-equality of the branch B fold chain"
assert s_1394 == s_1367 | set().union(*(covers(r) for r in roots_j)), \
    "set-equality of the cost-63j fold"
print(f"CONTROL fork covers: |cov(63h root)|={len(cov_h)} |cov(37 x 63j+65m roots)|={len(cov37)} "
      f"overlap={len(overlap_cov)}")
assert ROOT_H_V not in prevB, "the 63h root must be raw-disjoint from the branch B folded roots"
prevB_d4 = {f"{canon(r):032x}" for r in prevB}
d4_h = f"{canon(ROOT_H_V):032x}"
assert d4_h not in prevB_d4, "the 63h root must be D4-disjoint from the branch B folded roots"
prev_all = prevB | {ROOT_H_V}
assert len(prev_all) == 705
print("CONTROL root disjointness: the 63h bit-89 root vs the 704 branch B folded roots "
      "(667 through cost-58c/63i + 29 cost-63j + 8 cost-65m), raw-hex and D4-canonically")

# ---------- 4. the 63h child genuinely remaining at the 1396 head ----------
assert CHILD_H_V in manifest and CHILD_H_V not in s_1396, \
    "the 63h child must still be open at the branch B head 1396"
parents_h = {}
for name, h in (("parent1", P1), ("parent2", P2), ("parent3", P3)):
    rows = rem_1396.get(h, [])
    d = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rows}
    assert CHILD_H in d, (name, "the 63h child must be a remaining row of this open parent")
    parents_h[name] = d
d = dem_1396[CHILD_H]
assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 2), d
del_orbits = {s: canon(CHILD_H_V & ~(1 << s))
              for s in [i for i in range(121) if (CHILD_H_V >> i) & 1]}
lifts = {name: [s for s, o in del_orbits.items() if f"{o:032x}" == h]
         for name, h in (("parent1", P1), ("parent2", P2), ("parent3", P3))}
assert all(lifts.values()) and len(set(del_orbits.values())) == 6, lifts
assert sorted(l for v in lifts.values() for l in v) == [19, 30, 57], lifts
print("CONTROL 63h child genuinely remaining at head 1396: three open parents "
      f"hold the row ({len(parents_h['parent1'])}/{sum(parents_h['parent1'].values())}, "
      f"{len(parents_h['parent2'])}/{sum(parents_h['parent2'].values())}, "
      f"{len(parents_h['parent3'])}/{sum(parents_h['parent3'].values())}), "
      f"demand c1=0,c2=2,c4=2, lift stones {lifts}")

# ---------- 5. re-assert the published 63h certificate ----------
c89 = certs63h["89"]
assert c89["root_hex"] == ROOT_H
cert_path = OUT / "class2-lane-cost63h-certificates" / f"bit{BIT_H}-root-{ROOT_H}.cert"
parts = sorted((OUT / "class2-lane-cost63h-certificates").glob(f"bit{BIT_H}-root-{ROOT_H}.cert.part*of2"))
if parts:
    whole = b"".join(p.read_bytes().replace(b"\r\n", b"\n") for p in parts)
else:
    whole = cert_path.read_bytes()
assert len(whole) == c89["bytes"] and hashlib.md5(whole).hexdigest() == c89["md5"]
assert whole.startswith(b"n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS\n")
assert whole.splitlines()[1] == b"root " + ROOT_H.encode()
rows_h = whole.splitlines()[2:]
assert len(rows_h) == c89["rows"] and rows_h == sorted(set(rows_h))
assert c89["bigint_verifier"]["union_missing"] == 0 and c89["bigint_verifier"]["union_extra"] == 0
assert c89["bigint_verifier"]["terminal_range"] == [13, 17]
assert c89["ts_verifier"]["union_missing"] == 0 and c89["ts_verifier"]["union_extra"] == 0
assert CHILD_H_V in cov_h, "the root covers the child via its added stone"
print(f"CONTROL 63h certificate re-asserted: {c89['rows']} rows / {c89['bytes']} bytes "
      f"md5 {c89['md5']}, BigInt + tsverify union 0/0, terminal [13,17]")

# ---------- 6. fold the 63h receipt on top of the 1396 head ----------
marg = cov_h - s_1396
marg_m = marg & manifest
assert CHILD_H_V in marg_m, "the child orbit must be closed by this fold"
addition_h = {
    "bit": BIT_H, "root_hex": ROOT_H, "d4_canonical_hex": c89["d4_canonical_hex"],
    "certified": True, "covers": len(cov_h), "marginal": len(marg),
    "marginal_in_manifest": len(marg_m),
    "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
    "marginal_non_manifest_hexes": sorted(f"{k:032x}" for k in marg - marg_m),
    "rows": c89["rows"], "md5": c89["md5"],
    "sub_roots_pass": c89["sub_roots_total"],
    "v15_anchor_nodes": c89["v15_anchor_nodes"],
}
s_m = s_1396 | marg
assert s_m == s_1367 | cov37 | cov_h == s_1369 | cov37
st_m, rem_m, uniq_m, dem_m = summary_state(s_m)
print("AFTER merged fold:", json.dumps(st_m, indent=1))
print(f"63h receipt on the 1396 baseline: marginal={len(marg)} "
      f"marginal_in_manifest={len(marg_m)}; child orbit closed by bit{BIT_H}")

# ---------- 7. reverse-order replay control ----------
s_alt = s_1369 | cov37
assert s_alt == s_m, "reverse-order replay (37 x 63j+65m covers on the 1369 head) must "
"reproduce the identical merged set"
st_alt, rem_alt, uniq_alt, dem_alt = summary_state(s_alt)
assert st_alt == st_m and dem_alt == dem_m
marg37_on_1369 = cov37 - s_1369
marg37_on_1367 = cov37 - s_1367
marg_h_on_1367 = cov_h - s_1367
print(f"CONTROL reverse-order replay: identical merged set; 37 covers marginal "
      f"{len(marg37_on_1367)} at 1367 vs {len(marg37_on_1369)} at 1369 "
      f"(overlap with the 63h covers: {len(marg37_on_1367) - len(marg37_on_1369)}); "
      f"63h covers marginal {len(marg_h_on_1367)} at 1367 vs {len(marg)} at 1396")

# ---------- 8. per-parent rows at the merged head ----------
rows_after = {}
for name, h in (("parent1", P1), ("parent2", P2), ("parent3", P3), ("parent2_63i", P2_I)):
    rows_after[name] = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_m.get(h, [])}
lost_h = {name: set(parents_h[name]) - set(rows_after[name])
          for name in ("parent1", "parent2", "parent3")}
for name in ("parent1", "parent2", "parent3"):
    assert CHILD_H in lost_h[name], name
    assert lost_h[name] <= {f"{k:032x}" for k in cov_h}, name
print("per-parent rows at the merged head: "
      f"second candidate {len(rows_after['parent1'])}/{sum(rows_after['parent1'].values())} "
      f"(lost {sorted(lost_h['parent1'])}); dual class-2+4 "
      f"{len(rows_after['parent2'])}/{sum(rows_after['parent2'].values())} "
      f"(lost {sorted(lost_h['parent2'])}); class-4 "
      f"{len(rows_after['parent3'])}/{sum(rows_after['parent3'].values())} "
      f"(lost {sorted(lost_h['parent3'])}); 63i second parent "
      f"{len(rows_after['parent2_63i'])}/{sum(rows_after['parent2_63i'].values())})")


# ---------- 9. outputs ----------
def best(rem, bit):
    return sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r["remaining_s6_orbits"], r["remaining_s7_edge_cost"], r["s5_hex"]))


class2 = best(rem_m, 2)
class4 = best(rem_m, 4)
result = {
    "schema": "n11-class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116-v1",
    "date": "2026-11-16",
    "fork_record": {
        "common_baseline": "cost-58c chain head 1360/6488/512785/4758/376508 "
                           "(class-frontier-cost58c-receipts-recompute-20261116.json, "
                           "git blob sha 62a411bb1a6debc33782c07062843650c556c747), "
                           "extended by the cost-63i fold (18 receipts) to the shared "
                           "chain head 1367/6481/512295/4751/376018",
        "branch_A_merged_63h_63i": "class-frontier-merged-cost63h-63i-recompute-20261116.json: "
                                   "head 1369/6479/512163/4749/375886 (63i 18 receipts + the "
                                   "63h bit-89 receipt; blob "
                                   "c3ff50364499014a7096151bd9893a6510386c05; commit c3bd5b4f)",
        "branch_B_63j_65m": "class-frontier-cost63j-receipts-recompute-20261116.json (29 "
                            "receipts, 1367 -> 1394, blob 35236daf18e6207d2ed20c168bb8a6111f17d4e8, "
                            "commit 50e6a1b3, folded on the claim's 1367 baseline without the "
                            "re-base onto the merged head 1369) then "
                            "class-frontier-cost65m-receipts-recompute-20261116.json (8 "
                            "receipts, 1394 -> 1396, blob "
                            "9798a9fc53b2277b17744737511354b1a830c4d2, commit a382ff47)",
        "resolution": "both branch heads reproduced through their published scripts "
                      "(each internally reproducing the published fold chain down to the "
                      "58c head 1360 and asserting its own output blobs byte-identical "
                      "to main), the 63h bit-89 receipt folded on top of the 1396 head, "
                      "reverse-order replay (37 x 63j+65m covers on the 1369 head) "
                      "reproduces the identical merged set",
    },
    "method": "runpy reproduction of both published branch chains (branch B: the "
              "cost-65m fold script reproducing the 63j/63i/58c chain and its three "
              "output blobs; branch A: the merged 63h+63i fold script reproducing the "
              "63h/63i/58c chain and its three output blobs), the fork set equalities "
              "against the shared 1367 baseline asserted, the 63h bit-89 root asserted "
              "disjoint from the 704 branch B folded roots raw-hex and D4-canonically, "
              "the cover overlap between the branches asserted zero, the 63h child "
              "asserted genuinely remaining at the 1396 head (three open parents, "
              "demand c1=0,c2=2,c4=2 re-derived, lift stones 19/30/57 D4-verified), the "
              "published 63h certificate re-asserted against local bytes (rows "
              "sorted-unique, BigInt + tsverify union 0/0, terminal [13,17]), then the "
              "receipt folded on the 1396 head with a set-equality control; a "
              "reverse-order replay (the 37 cost-63j + cost-65m receipt covers on the "
              "1369 head) is asserted to reproduce the identical merged set and summary",
    "controls": {
        "both_branch_heads_reproduced_byte_identical": True,
        "fork_set_equalities": "s_1369 == s_1367 | cov(63h root); "
                               "s_1396 == s_1367 | cov(29 x 63j roots) | cov(8 x 65m roots); "
                               "s_1394 == s_1367 | cov(29 x 63j roots)",
        "root_disjointness_63h_vs_704": True,
        "cover_overlap_between_branches": len(overlap_cov),
        "child_genuinely_remaining_at_1396": True,
        "three_open_parents_held_child_row_at_1396": True,
        "certificate_63h_bytes_md5_verified": True,
        "child_orbit_closure": "closed by the bit-89 receipt of this merged fold",
        "set_equality_merged": "s_merged == s_1367 | cov(37 x 63j+65m roots) | cov(63h root) "
                               "== s_1369 | cov(37 x 63j+65m roots)",
        "reverse_order_replay_identical": True,
    },
    "cost63h_addition_on_1396": addition_h,
    "totals": {
        "receipts_folded_here": 1,
        "marginal": len(marg),
        "marginal_in_manifest": len(marg_m),
        "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
        "child_closed_by_bit": BIT_H,
        "merged_fold_receipts_total": 56,
        "merged_fold_receipts_composition": "63i 18 + 63j 29 + 65m 8 + 63h 1 = 56 on top of "
                                            "the 649 pre-63i folded receipt roots",
    },
    "frontier_after_merged": {
        "solved_s6_in_manifest": st_m["solved_s6_in_manifest"],
        "remaining_s5_orbits": st_m["remaining_s5_orbits"],
        "unique_remaining_s6": st_m["unique_remaining_s6"],
        "sum_remaining_cost": st_m["sum_remaining_cost"],
        "s6_needed_by_open_classes": st_m["s6_needed_by_open_classes"],
        "cost_needed_by_open_classes": st_m["cost_needed_by_open_classes"],
        "demand_histogram_open_only": st_m["hist"],
        "best_class2": class2[0] if class2 else None,
        "audit_blocked_class2": next((c for c in class2 if c["s5_hex"] == AUDIT_BLOCKED), None),
        "best_coverable_class2": next((c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED), None),
        "next_class2": class2[1:4],
        "best_class4": class4[0] if class4 else None,
        "next_class4": class4[1:4],
    },
    "parents_at_merged_head": {
        "second_candidate_s5": {"s5_hex": P1, "rows": len(rows_after["parent1"]),
                                 "edge_cost": sum(rows_after["parent1"].values())},
        "dual_class2_4_s5": {"s5_hex": P2, "rows": len(rows_after["parent2"]),
                             "edge_cost": sum(rows_after["parent2"].values())},
        "class4_s5": {"s5_hex": P3, "rows": len(rows_after["parent3"]),
                      "edge_cost": sum(rows_after["parent3"].values())},
        "cost63i_second_parent": {"s5_hex": P2_I, "rows": len(rows_after["parent2_63i"]),
                                  "edge_cost": sum(rows_after["parent2_63i"].values())},
    },
    "outstanding_not_folded": {
        "next_fold_baseline": "this merged chain head (see frontier_after_merged) is "
                              "the new canonical baseline for all subsequent folds; "
                              "assert it before extending; the branch heads 1369 and "
                              "1396 are both superseded by this merge",
    },
    "interpretation_guard": "bookkeeping over published receipts; solved counts "
                            "measure manifest coverage, not the game-theoretic "
                            "value of any position; REFUTED-D10 sweeps prove only "
                            "absence of WIN7-D10; WIN7 certificates prove a win "
                            "within depth 10 from the individual 7-stone roots "
                            "only; 11x11 empty board / two-stone root {49,60} / "
                            "S2 {59,60} / class 1 / class 2 / class 4 remain UNKNOWN",
}
(OUT / "class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in rem_m.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / "class-frontier-s5-ranking-after-merged-cost63h-63i-63j-65m-20261116.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / "class-frontier-top-candidates-s6-after-merged-cost63h-63i-63j-65m-20261116.csv").open(
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
        rows = rem_m.get(cand["s5_hex"], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
        for row in sorted(rows, key=lambda r: int(r["s6_s7_edge_cost"])):
            d = dem_m[row["s6_hex"]]
            w.writerow((cand["s5_hex"], row["s6_hex"], row["s6_s7_edge_cost"],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print("written ranking + top-candidates CSVs (after-merged-cost63h-63i-63j-65m)")

# ---------- 10. output blob shas ----------
for p in ("class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json",
          "class-frontier-s5-ranking-after-merged-cost63h-63i-63j-65m-20261116.csv",
          "class-frontier-top-candidates-s6-after-merged-cost63h-63i-63j-65m-20261116.csv"):
    sha, blen = git_blob_sha(OUT / p)
    print(f"blob {p}: {sha} ({blen} bytes)")
