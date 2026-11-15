#!/usr/bin/env python3
"""Class-2 frontier reconciliation of the cost-70g fork onto the canonical
merged head 1400.

The canonical merged fold (class-frontier-merged-cost63h-63i-63j-65m-67d-
recompute-20261116.json, head 1400/6448/509842/4718/373565, commit 2fbb5aa2)
folded the cost-63h bit-89 receipt and the cost-67d bit-97 receipt on the
common 1396 baseline.  The later cost-70g landing
(class-frontier-cost70g-receipts-recompute-20261116.json, commit dee808f0)
folded its 7 WIN7-D10 receipts (bits 18/24/28/59/89/112/120 of the second
coverable class-2 candidate S5's cost-70 child 00000000000000801202000040000001)
onto the SUPERSEDED branch D head 1398/6450/509974/4720/373697 instead of the
canonical 1400 head, producing the non-nested fork head 1403/6445/509589/4715/
373312.  This script closes that fork: it reproduces the published cost-70g
fold script (which internally reproduces the whole cost-67d chain
byte-identically, re-derives the sweep from the raw batches, re-asserts all 7
certificates and the completed-claim fold record), reconstructs the canonical
1400 head on top of the reproduced branch D head via the 63h bit-89 receipt
cover, asserts the canonical head against every published 1400 number (all
five parents, best/next rankings and a byte-identical regenerated ranking
CSV), asserts the child genuinely remaining at 1400 and the 7 roots disjoint
from all 706 folded roots, then folds the 7 receipts on the canonical 1400
baseline and emits the reconciled head.  The fork commutes:
s_reconciled == s_1400 | cov(70g roots) == s_1403 | cov(63h root).

11x11 empty board / two-stone root {49,60} / class 1 / class 2 / class 4
remain UNKNOWN; this is receipt bookkeeping only.
"""
import csv
import hashlib
import io
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

# cost-63h lane constants (the receipt whose cover defines canonical 1400)
CHILD_H = "00000000000000801202000040080000"
CHILD_H_V = int(CHILD_H, 16)
BIT_H = 89
ROOT_H_V = CHILD_H_V | (1 << BIT_H)
# published (branch C merged fold) in-manifest marginals of the 63h receipt
MARG_H_MANIFEST_PUB = {
    "00000000000000801202000040080000",
    "00000000020000801002000040080000",
}
# published (cost-70g fold, at the branch D baseline) in-manifest marginals
MIM70G_BASE_PUB = {
    "00000000000000801202000000040001",
    "00000000000000801202000040000001",
    "00000000000000003800000009000001",
    "00000000000000103800000008000001",
    "00004000000000003800000008000400",
}


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


_orig_write_text = Path.write_text


def _write_text_lf(self, data, encoding=None, errors=None, newline=None):
    with self.open("w", encoding=encoding or "utf-8", errors=errors,
                   newline="\n") as f:
        f.write(data)


Path.write_text = _write_text_lf

# ---------- 1. reproduce the published cost-70g fold (head 1403) ----------
nsB = runpy.run_path(str(HERE / "scripts" /
                         "recompute_frontier_cost70g_receipts_20261116.py"))
s_base = set(nsB["s_base"])            # branch D head (superseded 1398')
st_base = nsB["st_base"]
s_1403 = set(nsB["s_cur"])             # published 70g fork head
st_1403 = nsB["stF2"]
covers = nsB["covers"]
manifest = nsB["manifest"]
classes = nsB["classes"]
summary_state = nsB["summary_state"]
canon = nsB["canon"]
prev = set(nsB["prev"])                # 705 branch D folded roots
certs = nsB["certs"]                   # the 7 re-asserted 70g certificates
addition_base = nsB["addition"]        # per-bit marginals at the branch D base
WIN_BITS = list(nsB["WIN_BITS"])
CHILD = nsB["CHILD"]
CHILD_V = int(CHILD, 16)
PARENT1 = nsB["PARENT1"]
PARENT2 = nsB["PARENT2"]
sums = {"rows": sum(c["rows"] for c in certs.values()),
        "bytes": sum(c["bytes"] for c in certs.values()),
        "sub_roots_total": sum(c["sub_roots_total"] for c in certs.values())}
assert (st_base["solved_s6_in_manifest"], st_base["unique_remaining_s6"],
        st_base["sum_remaining_cost"], st_base["s6_needed_by_open_classes"],
        st_base["cost_needed_by_open_classes"]) == (1398, 6450, 509974, 4720,
                                                    373697)
assert (st_1403["solved_s6_in_manifest"], st_1403["unique_remaining_s6"],
        st_1403["sum_remaining_cost"], st_1403["s6_needed_by_open_classes"],
        st_1403["cost_needed_by_open_classes"]) == (1403, 6445, 509589, 4715,
                                                    373312)
assert sums["rows"] == 350567 and sums["bytes"] == 12679157 \
    and sums["sub_roots_total"] == 395
assert len(prev) == 705, len(prev)
assert WIN_BITS == [18, 24, 28, 59, 89, 112, 120]
print("CONTROL cost-70g fold reproduced (its own asserts passed): branch D "
      "head 1398/6450/509974/4720/373697, fork head 1403/6445/509589/4715/"
      "373312, 7 certificates "
      f"{sums['rows']} rows / {sums['bytes']} bytes / {sums['sub_roots_total']} "
      "sub-roots, three output blobs re-asserted byte-identical to the "
      "completed claim")

# ---------- 2. reconstruct the canonical 1400 head on the branch D head ----------
cov_h = covers(ROOT_H_V)
assert len(cov_h) == 7, len(cov_h)
marg_h = cov_h - s_base
assert len(marg_h) == 5, sorted(f"{k:032x}" for k in marg_h)
marg_h_m = marg_h & manifest
assert len(marg_h_m) == 2 and CHILD_H_V in marg_h_m
assert {f"{k:032x}" for k in marg_h_m} == MARG_H_MANIFEST_PUB, \
    "the 63h in-manifest marginals must match the published branch C fold"
s_1400 = s_base | cov_h
assert s_1400 == set(s_base) | marg_h
st_1400, rem_1400, uniq_1400, dem_1400 = summary_state(s_1400)
pub = json.loads((OUT / ("class-frontier-merged-cost63h-63i-63j-65m-67d-"
                         "recompute-20261116.json")).read_text())
pf = pub["frontier_after_merged"]
assert (st_1400["solved_s6_in_manifest"], st_1400["unique_remaining_s6"],
        st_1400["sum_remaining_cost"], st_1400["s6_needed_by_open_classes"],
        st_1400["cost_needed_by_open_classes"]) == \
    (pf["solved_s6_in_manifest"], pf["unique_remaining_s6"],
     pf["sum_remaining_cost"], pf["s6_needed_by_open_classes"],
     pf["cost_needed_by_open_classes"]) == (1400, 6448, 509842, 4718, 373565)
assert st_1400["remaining_s5_orbits"] == pf["remaining_s5_orbits"] == 174
assert st_1400["hist"] == pf["demand_histogram_open_only"]
pp = pub["parents_at_merged_head"]
for name in ("second_candidate_s5", "dual_class2_4_s5", "class4_s5",
             "cost67d_parent2", "cost63i_second_parent"):
    h = pp[name]["s5_hex"]
    rows = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1400.get(h, [])}
    assert (len(rows), sum(rows.values())) == (pp[name]["rows"],
                                               pp[name]["edge_cost"]), name
print("CONTROL canonical 1400 head reconstructed on the branch D head "
      "(s_1400 == s_base | cov(63h bit-89 root)): 1400/6448/509842/4718/373565 "
      "+ histogram + all five published parents match")


def best(rem, bit):
    return sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r["remaining_s6_orbits"], r["remaining_s7_edge_cost"],
                       r["s5_hex"]))


def as_tuples(cands):
    return [(c["s5_hex"], c["classes"], c["remaining_s6_orbits"],
             c["remaining_s7_edge_cost"]) for c in cands]


class2_1400 = best(rem_1400, 2)
class4_1400 = best(rem_1400, 4)
assert as_tuples(class2_1400[0:1]) == as_tuples([pf["best_class2"]])
assert as_tuples(class2_1400[1:4]) == as_tuples(pf["next_class2"])
assert as_tuples(class4_1400[0:1]) == as_tuples([pf["best_class4"]])
assert as_tuples(class4_1400[1:4]) == as_tuples(pf["next_class4"])
# byte-identical regenerated ranking CSV control
ranking_1400 = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in rem_1400.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
buf = io.StringIO()
w = csv.writer(buf, lineterminator="\n")
w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
for r in ranking_1400:
    w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                r["remaining_s7_edge_cost"]))
pub_rank_path = OUT / ("class-frontier-s5-ranking-after-merged-cost63h-"
                      "63i-63j-65m-67d-20261116.csv")
assert buf.getvalue().encode() == pub_rank_path.read_bytes(), \
    "regenerated 1400 ranking CSV must be byte-identical to the published one"
print("CONTROL 1400 rankings match the published merged fold and the "
      "regenerated ranking CSV is byte-identical to main")

# ---------- 3. root disjointness against all 706 folded roots ----------
prev1400 = prev | {ROOT_H_V}
assert len(prev1400) == 706
new_roots = {int(certs[str(b)]["root_hex"], 16) for b in WIN_BITS}
assert not (new_roots & prev1400)
assert f"{canon(ROOT_H_V):032x}" not in {f"{canon(r):032x}" for r in prev}
prev1400_d4 = {f"{canon(r):032x}" for r in prev1400}
new_d4 = {certs[str(b)]["d4_canonical_hex"] for b in WIN_BITS}
assert not (new_d4 & prev1400_d4) and len(new_d4) == 7
print("CONTROL root disjointness: the 7 cost-70g roots vs the 706 folded "
      "roots (705 branch D + the 63h bit-89 root), raw-hex and D4-canonically")

# ---------- 4. the cost-70g child genuinely remaining at 1400 ----------
assert CHILD_V in manifest and CHILD_V not in s_1400
rows_p1 = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1400.get(PARENT1, [])}
rows_p2 = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1400.get(PARENT2, [])}
assert CHILD in rows_p1 and rows_p1[CHILD] == 70
assert (len(rows_p1), sum(rows_p1.values())) == (7, 509)
assert CHILD in rows_p2, "the child must remain a row of the 70g parent2 at 1400"
p2_1400 = (len(rows_p2), sum(rows_p2.values()))
d = dem_1400[CHILD]
assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 0), d
mim70g_base = {int(h, 16) for a in addition_base
               for h in a["marginal_manifest_hexes"]}
assert {f"{k:032x}" for k in mim70g_base} == MIM70G_BASE_PUB
already = mim70g_base & s_1400
assert already == mim70g_base & cov_h and len(already) == 0, \
    "the 70g in-manifest marginals must be untouched by the 63h cover"
print(f"CONTROL child genuinely remaining at 1400: parent1 (second candidate "
      f"S5) 7 rows / 509 with the child row at edge cost 70, parent2 "
      f"{p2_1400[0]} rows / {p2_1400[1]}, demand c1=0,c2=2,c4=0; the 5 "
      "published 70g in-manifest marginals are all still open at 1400 "
      "(overlap with the 63h cover: 0)")

# ---------- 5. fold the 7 receipts on the canonical 1400 head ----------
s_run = set(s_1400)
addition_1400 = []
zero_mim_1400 = []
child_closed_by = None
cov70g = set()
for bit in WIN_BITS:
    c = certs[str(bit)]
    root = int(c["root_hex"], 16)
    cov = covers(root)
    assert CHILD_V in cov, "every root covers the child via its added stone"
    cov70g |= cov
    marg = cov - s_run
    marg_m = marg & manifest
    if CHILD_V in marg_m:
        assert child_closed_by is None, "the child must be closed exactly once"
        child_closed_by = bit
    base_hexes = set(next(a for a in addition_base if a["bit"] == bit)
                     ["marginal_manifest_hexes"])
    assert {f"{k:032x}" for k in marg_m} == base_hexes, \
        "per-bit in-manifest marginals at 1400 must equal the published ones"
    addition_1400.append({
        "bit": bit, "root_hex": c["root_hex"],
        "d4_canonical_hex": c["d4_canonical_hex"],
        "certified": True, "covers": len(cov), "marginal": len(marg),
        "marginal_in_manifest": len(marg_m),
        "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
        "marginal_non_manifest_hexes": sorted(f"{k:032x}" for k in marg - marg_m),
        "rows": c["rows"], "md5": c["md5"],
        "sub_roots_pass": c["sub_roots_total"],
        "v15_anchor_nodes": c["v15_anchor_nodes"],
    })
    if not marg_m:
        zero_mim_1400.append(bit)
    s_run |= marg
assert child_closed_by == 18, "the child orbit must be closed by the bit-18 receipt"
s_new = s_run
assert s_new == s_1400 | cov70g, "set-equality: s_reconciled == s_1400 | cov(7 roots)"
total_mim_1400 = sum(a["marginal_in_manifest"] for a in addition_1400)
total_marg_1400 = sum(a["marginal"] for a in addition_1400)
assert total_mim_1400 == 5 - len(already) == 5
st_new, rem_new, uniq_new, dem_new = summary_state(s_new)
assert st_new["solved_s6_in_manifest"] == 1400 + total_mim_1400 == 1405
print("AFTER reconciliation fold:", json.dumps(st_new, indent=1))

# ---------- 6. reverse-order replay across the fork ----------
s_alt = s_1403 | cov_h
assert s_alt == s_new, "the fork must commute: s_1403 | cov(63h) == s_1400 | cov(70g)"
st_alt = summary_state(s_alt)[0]
assert st_alt == st_new
print("CONTROL reverse-order replay: folding the 63h cover on the published "
      "fork head 1403 reproduces the identical reconciled set and summary")

# ---------- 7. pre-registered frontier prediction ----------
assert (st_new["solved_s6_in_manifest"], st_new["remaining_s5_orbits"],
        st_new["unique_remaining_s6"], st_new["sum_remaining_cost"],
        st_new["s6_needed_by_open_classes"],
        st_new["cost_needed_by_open_classes"]) == \
    (1405, 174, 6443, 509457, 4713, 373180), \
    "the reconciled head must be 1405/6443/509457/4713/373180 (same 5 orbits, " \
    "identical parent multiplicities as at the branch D baseline, -385/-385)"
print("CONTROL pre-registered prediction holds: reconciled head "
      "1405/6443/509457/4713/373180")

# ---------- 8. per-parent rows at the reconciled head ----------
rows_p1_new = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
               for r in rem_new.get(PARENT1, [])}
rows_p2_new = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
               for r in rem_new.get(PARENT2, [])}
cov70g_hexes = {f"{k:032x}" for k in cov70g}
lost_p1 = set(rows_p1) - set(rows_p1_new)
lost_p2 = set(rows_p2) - set(rows_p2_new)
assert CHILD in lost_p1 and lost_p1 <= cov70g_hexes, sorted(lost_p1)
assert CHILD in lost_p2 and lost_p2 <= cov70g_hexes, sorted(lost_p2)
assert (len(rows_p1_new), sum(rows_p1_new.values())) == (6, 439), \
    "the second candidate S5 must drop from 7 rows/509 to 6 rows/439"
p2_new = (len(rows_p2_new), sum(rows_p2_new.values()))
parents_after = {}
for name, h in (("second_candidate_s5", PARENT1), ("cost70g_parent2", PARENT2),
               ("dual_class2_4_s5", "00000000000000801202000000080000"),
               ("class4_s5", "00000000000000003800000001800000"),
               ("cost67d_parent2", "00000000000000801002000001080000"),
               ("cost63i_second_parent", "00000000000000403800000008000000")):
    rows = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_new.get(h, [])}
    parents_after[name] = {"s5_hex": h, "rows": len(rows),
                           "edge_cost": sum(rows.values())}
print("per-parent rows at the reconciled head: "
      + "; ".join(f"{k} {v['rows']}/{v['edge_cost']}"
                  for k, v in parents_after.items()))

# ---------- 9. rankings at the reconciled head ----------
class2 = best(rem_new, 2)
class4 = best(rem_new, 4)
AUDIT_BLOCKED = "00000000000000809082000000000000"
assert as_tuples(class2[0:1]) == [("00000000000000801202000000200000", 2, 3, 209)]
assert as_tuples(class2[1:4])[0] == (PARENT1, 2, 6, 439)
assert as_tuples([next(c for c in class2 if c["s5_hex"] == AUDIT_BLOCKED)]) == \
    [(AUDIT_BLOCKED, 3, 10, 698)]
assert as_tuples(class4[0:1]) == [("00000000020000003800000080000000", 4, 18, 1460)]
assert as_tuples(class4[1:4])[0] == ("00000000000000003800002000800000", 4, 60, 4216)

sha_merged, blen_merged = git_blob_sha(
    OUT / "class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json")
sha_70g, blen_70g = git_blob_sha(
    OUT / "class-frontier-cost70g-receipts-recompute-20261116.json")

result = {
    "schema": "n11-class-frontier-reconciled-canonical1400-cost70g-20261116-v1",
    "date": "2026-11-16",
    "fork_record": {
        "canonical_1400": "class-frontier-merged-cost63h-63i-63j-65m-67d-"
                          "recompute-20261116.json: head 1400/6448/509842/4718/"
                          f"373565 (commit 2fbb5aa2, git blob sha {sha_merged}, "
                          f"{blen_merged} bytes)",
        "cost70g_fork_1403": "class-frontier-cost70g-receipts-recompute-"
                             "20261116.json: head 1403/6445/509589/4715/373312 "
                             f"(commit dee808f0, git blob sha {sha_70g}, "
                             f"{blen_70g} bytes) - the 7 receipts were folded "
                             "on the superseded branch D head 1398/6450/509974/"
                             "4720/373697 instead of the canonical 1400 head",
        "resolution": "the cost-70g fold script reproduced byte-identically "
                      "(its completed-claim control re-asserted all three "
                      "output blobs), the canonical 1400 head reconstructed on "
                      "the reproduced branch D head via the 63h bit-89 receipt "
                      "cover and pinned against every published 1400 number "
                      "(summary, histogram, all five parents, best/next "
                      "rankings and a byte-identical regenerated ranking CSV), "
                      "the 7 receipts folded on the canonical 1400 baseline; "
                      "both fork heads 1400 and 1403 are superseded by this "
                      "reconciled head",
    },
    "method": "runpy reproduction of the published cost-70g fold script "
              "(internally reproducing the cost-67d chain byte-identically, "
              "re-deriving the sweep from the raw batches, re-asserting all 7 "
              "certificates against the joined LF bytes with BigInt + tsverify "
              "union 0/0 and the completed-claim fold record), reconstruction "
              "of the canonical 1400 head as s_base | cov(63h bit-89 root) "
              "with the 63h in-manifest marginals asserted equal to the "
              "published branch C fold, root disjointness of the 7 roots "
              "against all 706 folded roots (705 branch D + the 63h root) "
              "raw-hex and D4-canonically, the child asserted genuinely "
              "remaining at 1400 (parent1 7 rows/509 holding the child row at "
              "edge cost 70, parent2 open, demand c1=0,c2=2,c4=0), the five "
              "published in-manifest marginals asserted untouched by the 63h "
              "cover (overlap 0), then the 7 receipts folded on 1400 in "
              "publication order with per-bit marginal re-derivation, the "
              "child orbit closed exactly once by the bit-18 receipt, a "
              "set-equality control and a reverse-order replay across the fork "
              "(the 63h cover on the 1403 head) reproducing the identical set",
    "controls": {
        "cost70g_fold_reproduced_byte_identical": True,
        "canonical_1400_reconstructed_on_branch_D": True,
        "canonical_1400_pinned_to_published_numbers": True,
        "regenerated_1400_ranking_csv_byte_identical": True,
        "root_disjointness_7_vs_706": True,
        "child_genuinely_remaining_at_1400": True,
        "mim_overlap_with_63h_cover": 0,
        "certificates_bytes_md5_verified": True,
        "child_orbit_closure": "closed by the bit-18 receipt, exactly once",
        "set_equality_reconciled": "s_reconciled == s_1400 | cov(7 cost-70g "
                                   "roots) == s_1403 | cov(63h root)",
        "reverse_order_replay_identical": True,
        "pre_registered_prediction_holds": "1405/6443/509457/4713/373180",
    },
    "cost70g_addition_on_canonical1400": addition_1400,
    "totals": {
        "receipts": 7,
        "total_marginal": total_marg_1400,
        "total_marginal_in_manifest": total_mim_1400,
        "zero_marginal_in_manifest": [f"bit{b}" for b in zero_mim_1400],
        "child_closed_by_bit": child_closed_by,
        "marginal_in_manifest_at_branch_D_baseline": 5,
        "mim_shrink_vs_branch_D_baseline": len(already),
        "certificate_rows": sums["rows"],
        "certificate_bytes": sums["bytes"],
        "certificate_sub_roots": sums["sub_roots_total"],
    },
    "frontier_after_reconciled": {
        "solved_s6_in_manifest": st_new["solved_s6_in_manifest"],
        "remaining_s5_orbits": st_new["remaining_s5_orbits"],
        "unique_remaining_s6": st_new["unique_remaining_s6"],
        "sum_remaining_cost": st_new["sum_remaining_cost"],
        "s6_needed_by_open_classes": st_new["s6_needed_by_open_classes"],
        "cost_needed_by_open_classes": st_new["cost_needed_by_open_classes"],
        "demand_histogram_open_only": st_new["hist"],
        "best_class2": class2[0] if class2 else None,
        "audit_blocked_class2": next((c for c in class2
                                      if c["s5_hex"] == AUDIT_BLOCKED), None),
        "best_coverable_class2": next((c for c in class2
                                       if c["s5_hex"] != AUDIT_BLOCKED), None),
        "next_class2": class2[1:4],
        "best_class4": class4[0] if class4 else None,
        "next_class4": class4[1:4],
    },
    "parents_at_reconciled_head": parents_after,
    "coordination": {
        "cost75e_inflight_claim": "the cost-75e claim (child "
                                  "00000000040000809002000000000002, baseline "
                                  "the merged head 1400/6448/509842/4718/373565) "
                                  "references a superseded head and must re-"
                                  "base onto this reconciled head before "
                                  "folding",
        "cost76c_inflight_claim": "the cost-76c claim (child "
                                  "00000000010000809002000001000000, baseline "
                                  "the fork head 1403/6445/509589/4715/373312) "
                                  "references a superseded head and must re-"
                                  "base onto this reconciled head before "
                                  "folding",
        "zero_mim_bits_note": "bits 59/89/112 remain zero-marginal-in-manifest "
                              "at the canonical 1400 baseline exactly as at "
                              "the branch D baseline",
    },
    "interpretation_guard": "bookkeeping over published receipts; solved counts "
                            "measure manifest coverage, not the "
                            "game-theoretic value of any position; REFUTED-D10 "
                            "sweeps prove only absence of WIN7-D10; WIN7 "
                            "certificates prove a win within depth 10 from the "
                            "individual 7-stone roots only; 11x11 empty board / "
                            "two-stone root {49,60} / S2 {59,60} / class 1 / "
                            "class 2 / class 4 remain UNKNOWN",
}
(OUT / ("class-frontier-reconciled-canonical1400-cost70g-"
        "recompute-20261116.json")).write_text(json.dumps(result, indent=1) + "\n")
print("written class-frontier-reconciled-canonical1400-cost70g-"
      "recompute-20261116.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in rem_new.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / ("class-frontier-s5-ranking-after-reconciled-"
             "canonical1400-cost70g-20261116.csv")).open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits",
                "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / ("class-frontier-top-candidates-s6-after-reconciled-"
             "canonical1400-cost70g-20261116.csv")).open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    coverable = [c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED]
    for label, cand in (("best class-4 blocker-candidate S5",
                         class4[0] if class4 else None),
                        ("best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)",
                         next((c for c in class2 if c["s5_hex"] == AUDIT_BLOCKED),
                              None)),
                        ("best coverable class-2 blocker-candidate S5",
                         coverable[0] if coverable else None),
                        ("second coverable class-2 candidate S5",
                         coverable[1] if len(coverable) > 1 else None)):
        if cand is None:
            continue
        rows = rem_new.get(cand["s5_hex"], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} "
                    f"cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
        for row in sorted(rows, key=lambda r: int(r["s6_s7_edge_cost"])):
            d = dem_new[row["s6_hex"]]
            w.writerow((cand["s5_hex"], row["s6_hex"], row["s6_s7_edge_cost"],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print("written ranking + top-candidates CSVs (after-reconciled-canonical1400-"
      "cost70g)")

for p in ("class-frontier-reconciled-canonical1400-cost70g-"
          "recompute-20261116.json",
          "class-frontier-s5-ranking-after-reconciled-"
          "canonical1400-cost70g-20261116.csv",
          "class-frontier-top-candidates-s6-after-reconciled-"
          "canonical1400-cost70g-20261116.csv"):
    sha, blen = git_blob_sha(OUT / p)
    print(f"blob {p}: {sha} ({blen} bytes)")
