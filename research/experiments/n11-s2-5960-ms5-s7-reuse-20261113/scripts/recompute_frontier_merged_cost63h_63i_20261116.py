#!/usr/bin/env python3
"""Merged class-2 frontier recomputation reconciling the two parallel cost-63
folds that both descend from the cost-58c chain head 1360 (2026-11-16 fork):

- cost-63h (this lane): the second coverable class-2 candidate S5
  00000000000000801202000040000000's cost-63 child
  00000000000000801202000040080000, 1 WIN7-D10 receipt (bit 89), chain head
  1360 -> 1362/6486/512653/4756/376376;
- cost-63i (parallel lane): the same parent's other cost-63 child
  00000000000000c09002000001000000, 18 WIN7-D10 receipts, chain head
  1360 -> 1367/6481/512295/4751/376018.

Both published folds are reproduced through their own scripts (each asserts
the byte-identical cost-58c chain head 1360, its own sweep/certificates and
its own published output blobs), then the cost-63h bit-89 receipt is folded on
top of the 1367 head. A reverse-order replay (the 18 cost-63i receipt covers
folded on top of the 1362 head) is asserted to reproduce the identical merged
set, proving order-independence of the reconciliation. The merged head is
recorded as the new canonical baseline for all subsequent folds.

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
P1 = "00000000000000801202000040000000"
P2 = "00000000000000801202000000080000"
P3 = "00000000000000003800000001800000"
P2_I = "00000000000000403800000008000000"
AUDIT_BLOCKED = "00000000000000809082000000000000"


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


def git_blob_sha_bytes(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


# ---------- 1. reproduce the cost-63i fold (1360 -> 1367) ----------
ns63i = runpy.run_path(str(HERE / "scripts" / "recompute_frontier_cost63i_receipts_20261116.py"))
s_1360 = set(ns63i["s_base"])
s_1367 = set(ns63i["s_cur"])
st63i = ns63i["stF2"]
covers = ns63i["covers"]
manifest = ns63i["manifest"]
classes = ns63i["classes"]
summary_state = ns63i["summary_state"]
canon = ns63i["canon"]
rem_1367 = ns63i["remF2"]
dem = ns63i["demF2"]
prev649 = set(ns63i["prev"])
certs63i = ns63i["certs"]
win63i = ns63i["WIN_BITS"]
assert st63i["solved_s6_in_manifest"] == 1367 and st63i["unique_remaining_s6"] == 6481
assert st63i["sum_remaining_cost"] == 512295 and st63i["s6_needed_by_open_classes"] == 4751
assert st63i["cost_needed_by_open_classes"] == 376018
sha, blen = git_blob_sha(OUT / "class-frontier-cost63i-receipts-recompute-20261116.json")
assert sha == "db0288f15f1538293e66146542a938c9ebf8b91c" and blen == 16455, (sha, blen)
print("CONTROL cost-63i chain head reproduced through its published script: "
      "1367/6481/512295/4751/376018 (head JSON blob == main)")

# ---------- 2. reproduce the cost-63h fold (1360 -> 1362) ----------
ns63h = runpy.run_path(str(HERE / "scripts" / "recompute_frontier_cost63h_receipts_20261115.py"))
s_1362 = set(ns63h["s_cur"])
st63h = ns63h["stF2"]
certs63h = ns63h["certs"]
assert st63h["solved_s6_in_manifest"] == 1362 and st63h["unique_remaining_s6"] == 6486
assert st63h["sum_remaining_cost"] == 512653 and st63h["s6_needed_by_open_classes"] == 4756
assert st63h["cost_needed_by_open_classes"] == 376376
sha, blen = git_blob_sha(OUT / "class-frontier-cost63h-receipts-recompute-20261115.json")
assert sha == "647498b995770ff87b12e868a5b89015c26be51e" and blen == 6852, (sha, blen)
print("CONTROL cost-63h chain head reproduced through its published script: "
      "1362/6486/512653/4756/376376 (head JSON blob == main)")

# ---------- 3. fork facts and cover sets ----------
cov_i18 = set()
for b in win63i:
    cov_i18 |= covers(int(certs63i[str(b)]["root_hex"], 16))
cov_h = covers(CHILD_H_V | (1 << BIT_H))
assert s_1362 == s_1360 | cov_h, "set-equality of the 63h fold"
assert s_1367 == s_1360 | cov_i18, "set-equality of the 63i fold"
overlap_cov = cov_h & cov_i18
print(f"CONTROL fork covers: |cov(63h root)|={len(cov_h)} |cov(18x63i roots)|={len(cov_i18)} "
      f"overlap={len(overlap_cov)}")
prev_total = prev649 | {int(certs63i[str(b)]["root_hex"], 16) for b in win63i}
assert len(prev_total) == 667, len(prev_total)
root_h_v = CHILD_H_V | (1 << BIT_H)
assert root_h_v not in prev_total, "the 63h root must be raw-disjoint from the 63i folded roots"
prev_total_d4 = {f"{canon(r):032x}" for r in prev_total}
d4_h = f"{canon(root_h_v):032x}"
assert d4_h not in prev_total_d4, "the 63h root must be D4-disjoint from the 63i folded roots"
prev_total.add(root_h_v)
assert len(prev_total) == 668
print("CONTROL root disjointness: the 63h bit-89 root vs the 667 folded roots "
      "(649 through cost-58c + 18 cost-63i), raw-hex and D4-canonically")

# ---------- 4. the 63h child genuinely remaining at the 1367 head ----------
assert CHILD_H_V in manifest and CHILD_H_V not in s_1367, \
    "the 63h child must still be open at the 1367 head"
parents_h = {}
for name, h in (("parent1", P1), ("parent2", P2), ("parent3", P3)):
    rows = rem_1367.get(h, [])
    d = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rows}
    assert CHILD_H in d, (name, "the 63h child must be a remaining row of this open parent")
    parents_h[name] = d
d = dem[CHILD_H]
assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 2), d
del_orbits = {s: canon(CHILD_H_V & ~(1 << s))
              for s in [i for i in range(121) if (CHILD_H_V >> i) & 1]}
lifts = {name: [s for s, o in del_orbits.items() if f"{o:032x}" == h]
         for name, h in (("parent1", P1), ("parent2", P2), ("parent3", P3))}
assert all(lifts.values()) and len(set(del_orbits.values())) == 6, lifts
print("CONTROL 63h child genuinely remaining at head 1367: three open parents "
      f"hold the row ({len(parents_h['parent1'])}/{sum(parents_h['parent1'].values())}, "
      f"{len(parents_h['parent2'])}/{sum(parents_h['parent2'].values())}, "
      f"{len(parents_h['parent3'])}/{sum(parents_h['parent3'].values())}), "
      f"demand c1=0,c2=2,c4=2, lift stones {lifts}")

# ---------- 5. re-assert the published 63h certificate ----------
c89 = certs63h["89"]
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
assert c89["root_hex"] == ROOT_H
assert c89["bigint_verifier"]["union_missing"] == 0 and c89["bigint_verifier"]["union_extra"] == 0
assert c89["bigint_verifier"]["terminal_range"] == [13, 17]
assert c89["ts_verifier"]["union_missing"] == 0 and c89["ts_verifier"]["union_extra"] == 0
assert CHILD_H_V in cov_h, "the root covers the child via its added stone"
print(f"CONTROL 63h certificate re-asserted: {c89['rows']} rows / {c89['bytes']} bytes "
      f"md5 {c89['md5']}, BigInt + tsverify union 0/0, terminal [13,17]")

# ---------- 6. fold the 63h receipt on top of the 1367 head ----------
marg = cov_h - s_1367
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
s_m = s_1367 | marg
assert s_m == s_1360 | cov_i18 | cov_h
st_m, rem_m, uniq_m, dem_m = summary_state(s_m)
print("AFTER merged fold:", json.dumps(st_m, indent=1))
print(f"63h receipt on the 1367 baseline: marginal={len(marg)} "
      f"marginal_in_manifest={len(marg_m)}; child orbit closed by bit{BIT_H}")

# ---------- 7. reverse-order replay control ----------
s_alt = s_1362 | cov_i18
assert s_alt == s_m, "reverse-order replay (63i covers on the 1362 head) must "
"reproduce the identical merged set"
st_alt, rem_alt, uniq_alt, dem_alt = summary_state(s_alt)
assert st_alt == st_m and dem_alt == dem_m
marg_i18_on_1362 = cov_i18 - s_1362
marg_i18_on_1360 = cov_i18 - s_1360
print(f"CONTROL reverse-order replay: identical merged set; 63i covers marginal "
      f"{len(marg_i18_on_1360)} at 1360 vs {len(marg_i18_on_1362)} at 1362 "
      f"(overlap with the 63h covers: {len(marg_i18_on_1360) - len(marg_i18_on_1362)}); "
      f"63h covers marginal 5 at 1360 vs {len(marg)} at 1367")

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
    "schema": "n11-class-frontier-merged-cost63h-63i-recompute-20261116-v1",
    "date": "2026-11-16",
    "fork_record": {
        "common_baseline": "cost-58c chain head 1360/6488/512785/4758/376508 "
                           "(class-frontier-cost58c-receipts-recompute-20261116.json, "
                           "git blob sha 62a411bb1a6debc33782c07062843650c556c747)",
        "branch_63h": "class-frontier-cost63h-receipts-recompute-20261115.json: head "
                      "1362/6486/512653/4756/376376 (1 receipt, bit 89; blob "
                      "647498b995770ff87b12e868a5b89015c26be51e)",
        "branch_63i": "class-frontier-cost63i-receipts-recompute-20261116.json: head "
                      "1367/6481/512295/4751/376018 (18 receipts; blob "
                      "db0288f15f1538293e66146542a938c9ebf8b91c)",
        "resolution": "both folds reproduced through their published scripts, the "
                      "63h bit-89 receipt folded on top of the 1367 head, "
                      "reverse-order replay reproduces the identical merged set",
    },
    "method": "runpy reproduction of both published folds (each asserting the "
              "byte-identical cost-58c chain head 1360 and its own published "
              "output blobs), the 63h child asserted genuinely remaining at the "
              "1367 head (three open parents, demand c1=0,c2=2,c4=2 re-derived, "
              "lift stones 19/30/57 D4-verified), the published 63h certificate "
              "re-asserted against local bytes (rows sorted-unique, BigInt + "
              "tsverify union 0/0, terminal [13,17]), the bit-89 root asserted "
              "disjoint from the 667 folded roots raw-hex and D4-canonically, "
              "then the receipt folded on the 1367 head with a set-equality "
              "control; a reverse-order replay (the 18 cost-63i receipt covers "
              "on the 1362 head) is asserted to reproduce the identical merged "
              "set and summary",
    "controls": {
        "both_branch_heads_reproduced_byte_identical": True,
        "fork_set_equalities": "s_1362 == s_1360 | cov(63h root); s_1367 == s_1360 | cov(18 x 63i roots)",
        "root_disjointness_63h_vs_667": True,
        "child_genuinely_remaining_at_1367": True,
        "three_open_parents_held_child_row_at_1367": True,
        "certificate_63h_bytes_md5_verified": True,
        "child_orbit_closure": "closed by the bit-89 receipt of this merged fold",
        "set_equality_merged": "s_merged == s_1360 | cov(18 x 63i roots) | cov(63h root)",
        "reverse_order_replay_identical": True,
        "cover_overlap_between_branches": len(overlap_cov),
    },
    "cost63h_addition_on_1367": addition_h,
    "totals": {
        "receipts_folded_here": 1,
        "marginal": len(marg),
        "marginal_in_manifest": len(marg_m),
        "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
        "child_closed_by_bit": BIT_H,
        "merged_fold_receipts_total": 19,
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
                              "assert it before extending",
    },
    "interpretation_guard": "bookkeeping over published receipts; solved counts "
                            "measure manifest coverage, not the game-theoretic "
                            "value of any position; REFUTED-D10 sweeps prove only "
                            "absence of WIN7-D10; WIN7 certificates prove a win "
                            "within depth 10 from the individual 7-stone roots "
                            "only; 11x11 empty board / two-stone root {49,60} / "
                            "S2 {59,60} / class 1 / class 2 / class 4 remain UNKNOWN",
}
(OUT / "class-frontier-merged-cost63h-63i-recompute-20261116.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-merged-cost63h-63i-recompute-20261116.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in rem_m.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / "class-frontier-s5-ranking-after-merged-cost63h-63i-20261116.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / "class-frontier-top-candidates-s6-after-merged-cost63h-63i-20261116.csv").open(
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
print("written ranking + top-candidates CSVs (after-merged-cost63h-63i)")

# ---------- 10. output blob shas ----------
for p in ("class-frontier-merged-cost63h-63i-recompute-20261116.json",
          "class-frontier-s5-ranking-after-merged-cost63h-63i-20261116.csv",
          "class-frontier-top-candidates-s6-after-merged-cost63h-63i-20261116.csv"):
    sha, blen = git_blob_sha(OUT / p)
    print(f"blob {p}: {sha} ({blen} bytes)")
