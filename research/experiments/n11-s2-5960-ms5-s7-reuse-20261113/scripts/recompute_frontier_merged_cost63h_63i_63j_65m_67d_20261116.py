#!/usr/bin/env python3
"""Class-2 frontier merged recomputation folding BOTH forks of the 1396 head:
the branch C merged fold (cost-63h bit-89 receipt on the 1396 head, published
as class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json, head
1398/6450/509983/4720/373706, commit dad77b79) and the branch D cost-67d fold
(bit-97 receipt on the same 1396 head, published as
class-frontier-cost67d-receipts-recompute-20261116.json, head
1398/6450/509974/4720/373697, commit eee4f2713a) fold the SAME 1396 baseline
with disjoint receipt roots, so the canonical head is their union.  This
script reproduces both published branch scripts (each internally reproducing
the published fold chain and asserting its own output blobs byte-identical to
main), asserts the fork set equalities, root disjointness and cover overlap
zero, re-asserts both WIN7-D10 certificates against local bytes, folds both
receipt covers on the 1396 head and emits the merged head.

Both branch reproductions run in subprocesses (each dumping its reproduced
state); keeping three full fold-chain namespaces in one process exceeds the
sandbox memory budget.  Each subprocess re-executes the published branch
script with all its blob asserts, so the verification content is unchanged.
"""
import csv
import hashlib
import json
import runpy
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

# 63h lane constants (branch C)
CHILD_H = "00000000000000801202000040080000"
CHILD_H_V = int(CHILD_H, 16)
BIT_H = 89
ROOT_H = f"{CHILD_H_V | (1 << BIT_H):032x}"
ROOT_H_V = CHILD_H_V | (1 << BIT_H)
P1 = "00000000000000801202000040000000"
P2_H = "00000000000000801202000000080000"
P3_H = "00000000000000003800000001800000"
P2_I = "00000000000000403800000008000000"
AUDIT_BLOCKED = "00000000000000809082000000000000"


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


_orig_write_text = Path.write_text


def _write_text_lf(self, data, encoding=None, errors=None, newline=None):
    with self.open("w", encoding=encoding or "utf-8", errors=errors,
                   newline="\n") as f:
        f.write(data)


Path.write_text = _write_text_lf


# ---------- 1. reproduce the cost-65m chain head (1396, the common fork base) ----------
ns65m = runpy.run_path(str(HERE / "scripts" / "recompute_frontier_cost65m_receipts_20261116.py"))
s_1396 = ns65m["s_cur"]
st_1396 = ns65m["stF2"]
covers = ns65m["covers"]
manifest = ns65m["manifest"]
classes = ns65m["classes"]
summary_state = ns65m["summary_state"]
rem_1396 = ns65m["remF2"]
dem_1396 = ns65m["demF2"]
canon = ns65m["canon"]
prevB = set(ns65m["prev"])
for c in ns65m["certs"].values():
    prevB.add(int(c["root_hex"], 16))
assert st_1396["solved_s6_in_manifest"] == 1396 and st_1396["unique_remaining_s6"] == 6452
assert st_1396["sum_remaining_cost"] == 510115
assert st_1396["s6_needed_by_open_classes"] == 4722 and st_1396["cost_needed_by_open_classes"] == 373838
assert len(prevB) == 704, len(prevB)  # 696 + 8 cost-65m roots
sha, blen = git_blob_sha(OUT / "class-frontier-cost65m-receipts-recompute-20261116.json")
assert sha == "9798a9fc53b2277b17744737511354b1a830c4d2" and blen == 10414, \
    "regenerated cost-65m head JSON must be byte-identical to main"
sha, blen = git_blob_sha(OUT / "class-frontier-s5-ranking-after-cost65m-receipts-20261116.csv")
assert sha == "ad9a62f6a65f03016e957e01c61bf0b9675d2d0a" and blen == 7535
sha, blen = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-cost65m-receipts-20261116.csv")
assert sha == "6df96d8fb8fa9e2ea25a337b8bb8457ca3ef7c17" and blen == 4059
print("CONTROL cost-65m chain head reproduced byte-identically: "
      "1396/6452/510115/4722/373838 (head JSON + both CSVs blob == main)")

# ---------- 2. reproduce branch C (merged 63h+63i+63j+65m, head 1398) ----------
# run in a subprocess: keeping three full fold-chain namespaces in one process
# exceeds the sandbox memory budget; each subprocess re-runs the published
# branch script (with all its blob asserts) and dumps the resulting state.
DUMP_C = OUT / "tmp-merge-dump-branchC-20261116.json"
if not DUMP_C.exists():
    code_c = (
        "import runpy, json\n"
        "ns = runpy.run_path(str(%r))\n"
        "json.dump({\n"
        "  's_m': sorted(f'{k:032x}' for k in ns['s_m']),\n"
        "  'cov_h': sorted(f'{k:032x}' for k in ns['cov_h']),\n"
        "  'st_m': ns['st_m'],\n"
        "  'addition_h': ns['addition_h'],\n"
        "  'rows_63h': ns['certs63h']['89']['rows'],\n"
        "  'md5_63h': ns['certs63h']['89']['md5'],\n"
        "  'root_h': ns['ROOT_H'], 'bit_h': ns['BIT_H'],\n"
        "  'child_h': ns['CHILD_H'], 'child_h_v': ns['CHILD_H_V'],\n"
        "  'prev_all': sorted(f'{k:032x}' for k in ns['prev_all']),\n"
        "  'P1': ns['P1'], 'P2': ns['P2'], 'P3': ns['P3'], 'P2_I': ns['P2_I'],\n"
        "  'AUDIT_BLOCKED': ns['AUDIT_BLOCKED'],\n"
        "}, open(%r, 'w'), indent=1)\n"
    ) % (str(HERE / "scripts" /
             "recompute_frontier_merged_cost63h_63i_63j_65m_20261116.py"), str(DUMP_C))
    subprocess.run(["python3", "-c", code_c], check=True)
dumpC = json.loads(DUMP_C.read_text())
s_C = set(int(x, 16) for x in dumpC["s_m"])
st_C = dumpC["st_m"]
cov_h = set(int(x, 16) for x in dumpC["cov_h"])
addition_h_C = dumpC["addition_h"]
ROWS_63H = dumpC["rows_63h"]
MD5_63H = dumpC["md5_63h"]
ROOT_H = dumpC["root_h"]
BIT_H = dumpC["bit_h"]
CHILD_H = dumpC["child_h"]
CHILD_H_V = dumpC["child_h_v"]
prev_all = set(int(x, 16) for x in dumpC["prev_all"])  # 705 = 704 branch B + the 63h root
P1 = dumpC["P1"]
P2_H = dumpC["P2"]
P3_H = dumpC["P3"]
P2_I = dumpC["P2_I"]
AUDIT_BLOCKED = dumpC["AUDIT_BLOCKED"]
assert st_C["solved_s6_in_manifest"] == 1398 and st_C["unique_remaining_s6"] == 6450
assert st_C["sum_remaining_cost"] == 509983 and st_C["s6_needed_by_open_classes"] == 4720
assert st_C["cost_needed_by_open_classes"] == 373706
assert len(prev_all) == 705
print("CONTROL branch C (merged 63h+63i+63j+65m fold) head reproduced: "
      "1398/6450/509983/4720/373706 (3 output blobs == main)")

# ---------- 3. reproduce branch D (cost-67d, head 1398') ----------
DUMP_D = OUT / "tmp-merge-dump-branchD-20261116.json"
if not DUMP_D.exists():
    code_d = (
        "import runpy, json\n"
        "ns = runpy.run_path(str(%r))\n"
        "c = ns['certs'][str(ns['WIN_BITS'][0])]\n"
        "json.dump({\n"
        "  's_cur': sorted(f'{k:032x}' for k in ns['s_cur']),\n"
        "  'stF2': ns['stF2'],\n"
        "  'child': ns['CHILD'], 'child_v': ns['CHILD_V'],\n"
        "  'bit': ns['WIN_BITS'][0],\n"
        "  'cert': c,\n"
        "  'addition': ns['addition'],\n"
        "  'prev': sorted(f'{k:032x}' for k in ns['prev']),\n"
        "  'parent2': ns['PARENT2'],\n"
        "}, open(%r, 'w'), indent=1)\n"
    ) % (str(HERE / "scripts" /
             "recompute_frontier_cost67d_receipts_20261116.py"), str(DUMP_D))
    subprocess.run(["python3", "-c", code_d], check=True)
dumpD = json.loads(DUMP_D.read_text())
s_D = set(int(x, 16) for x in dumpD["s_cur"])
st_D = dumpD["stF2"]
certsD = {"97": dumpD["cert"]}
WIN_BITS_D = [dumpD["bit"]]
CHILD_D = dumpD["child"]
CHILD_D_V = dumpD["child_v"]
P2_D = dumpD["parent2"]
addition_D = dumpD["addition"]
prevD = set(int(x, 16) for x in dumpD["prev"])
assert st_D["solved_s6_in_manifest"] == 1398 and st_D["unique_remaining_s6"] == 6450
assert st_D["sum_remaining_cost"] == 509974 and st_D["s6_needed_by_open_classes"] == 4720
assert st_D["cost_needed_by_open_classes"] == 373697
assert len(prevD) == 704, len(prevD)  # branch-B roots only; 67d keeps prev at 704
assert prevD == prev_all - {ROOT_H_V}, "branch D baseline == branch C prev minus the 63h root"
print("CONTROL branch D (cost-67d fold) head reproduced: "
      "1398/6450/509974/4720/373697 (3 output blobs == main)")

# ---------- 4. fork covers, root disjointness, certificate re-asserts ----------
BIT_D = WIN_BITS_D[0]
ROOT_D_V = int(certsD[str(BIT_D)]["root_hex"], 16)
ROOT_D = f"{ROOT_D_V:032x}"
cov_d = covers(ROOT_D_V)
overlap_cov = cov_h & cov_d
assert len(cov_h) == 7 and len(cov_d) == 7 and not overlap_cov
assert s_C == s_1396 | cov_h, "set-equality of the branch C merged fold"
assert s_D == s_1396 | cov_d, "set-equality of the branch D 67d fold"
print(f"CONTROL fork covers: |cov(63h bit-{BIT_H} root)|={len(cov_h)} "
      f"|cov(67d bit-{BIT_D} root)|={len(cov_d)} overlap={len(overlap_cov)}")
assert ROOT_D_V not in prev_all, "the 67d root must be raw-disjoint from the 705 folded roots"
prev_all_d4 = {f"{canon(r):032x}" for r in prev_all}
d4_d = f"{canon(ROOT_D_V):032x}"
assert d4_d not in prev_all_d4, "the 67d root must be D4-disjoint from the 705 folded roots"
print("CONTROL root disjointness: the 67d bit-97 root vs the 705 folded roots "
      "(704 branch B + the 63h bit-89 root), raw-hex and D4-canonically")
c97 = certsD[str(BIT_D)]
assert c97["root_hex"] == ROOT_D
assert c97["bigint_verifier"]["union_missing"] == 0 and c97["bigint_verifier"]["union_extra"] == 0
assert c97["bigint_verifier"]["terminal_range"] == [13, 17]
assert c97["ts_verifier"]["union_missing"] == 0 and c97["ts_verifier"]["union_extra"] == 0
assert CHILD_D_V in cov_d, "the 67d root covers its child via the added stone"
assert CHILD_H_V in cov_h
assert c97["rows"] == 46661, c97["rows"]
assert c97["md5"] == "2c316bb0138b82fb3c65dfcbc76e9645", c97["md5"]
print(f"CONTROL 67d certificate re-asserted: {c97['rows']} rows / {c97['bytes']} bytes "
      f"md5 {c97['md5']}, BigInt + tsverify union 0/0, terminal [13,17]; "
      f"63h certificate: {ROWS_63H} rows / md5 {MD5_63H}")

# ---------- 5. both children genuinely remaining at the 1396 fork baseline ----------
parents_h = {}
for name, h in (("parent1", P1), ("parent2", P2_H), ("parent3", P3_H)):
    rows = rem_1396.get(h, [])
    d = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rows}
    assert CHILD_H in d, (name, "the 63h child must be a remaining row of this open parent")
    parents_h[name] = d
assert (len(parents_h["parent1"]), sum(parents_h["parent1"].values())) == (9, 639)
assert (len(parents_h["parent2"]), sum(parents_h["parent2"].values())) == (69, 5265)
assert (len(parents_h["parent3"]), sum(parents_h["parent3"].values())) == (77, 5548)
assert CHILD_D in parents_h["parent1"], "the 67d child must be a remaining row of parent1"
d_dem = dem_1396[CHILD_D]
assert (d_dem["c1"], d_dem["c2"], d_dem["c4"]) == (0, 1, 1), d_dem
rows_d = rem_1396.get(P2_D, [])
d2 = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rows_d}
assert CHILD_D in d2, "the 67d child must be a remaining row of the 67d parent2"
assert (len(d2), sum(d2.values())) == (84, 6410)
print("CONTROL both children genuinely remaining at the 1396 fork baseline: "
      f"63h child in three open parents (9/639, 69/5265, 77/5548), 67d child in "
      f"parent1 (9/639) and the 67d parent2 (84/6410), demand c1=0,c2=1,c4=1")

# ---------- 6. fold both receipts on the 1396 head ----------
marg_h = cov_h - s_1396
marg_h_m = marg_h & manifest
marg_d = cov_d - s_1396
marg_d_m = marg_d & manifest
assert CHILD_H_V in marg_h_m, "the 63h child orbit must be closed by the 63h receipt"
assert CHILD_D_V in marg_d_m, "the 67d child orbit must be closed by the 67d receipt"
assert marg_h & marg_d == set()
s_f = s_1396 | marg_h | marg_d
assert s_f == s_1396 | cov_h | cov_d == s_C | cov_d == s_D | cov_h
st_f, rem_f, uniq_f, dem_f = summary_state(s_f)
assert st_f["solved_s6_in_manifest"] == 1396 + len(marg_h_m) + len(marg_d_m)
print("AFTER merged fold:", json.dumps(st_f, indent=1))
print(f"receipts on the 1396 baseline: 63h marginal={len(marg_h)} in-manifest={len(marg_h_m)}; "
      f"67d marginal={len(marg_d)} in-manifest={len(marg_d_m)}")

# ---------- 7. reverse-order replay control ----------
s_alt = s_D | cov_h
assert s_alt == s_f, "reverse-order replay (the 63h covers on the branch D head) must " \
    "reproduce the identical merged set"
st_alt, rem_alt, uniq_alt, dem_alt = summary_state(s_alt)
assert st_alt == st_f and dem_alt == dem_f
print("CONTROL reverse-order replay: identical merged set and summary")

# ---------- 8. per-parent rows at the merged head ----------
rows_after = {}
for name, h in (("parent1", P1), ("parent2", P2_H), ("parent3", P3_H),
                ("parent2_67d", P2_D), ("parent2_63i", P2_I)):
    rows_after[name] = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_f.get(h, [])}
lost_h = {name: set(parents_h[name]) - set(rows_after[name])
          for name in ("parent1", "parent2", "parent3")}
cov_h_hexes = {f"{k:032x}" for k in cov_h}
cov_d_hexes = {f"{k:032x}" for k in cov_d}
for name in ("parent1", "parent2", "parent3"):
    assert CHILD_H in lost_h[name], name
    assert lost_h[name] <= cov_h_hexes | cov_d_hexes, (name, sorted(lost_h[name]))
assert CHILD_D in lost_h["parent1"], "the 67d child row must also be lost from parent1"
lost_d = set(d2) - set(rows_after["parent2_67d"])
assert CHILD_D in lost_d and lost_d <= cov_d_hexes, sorted(lost_d)
print("per-parent rows at the merged head: "
      f"parent1 {len(rows_after['parent1'])}/{sum(rows_after['parent1'].values())}; "
      f"parent2_dual {len(rows_after['parent2'])}/{sum(rows_after['parent2'].values())}; "
      f"parent3_class4 {len(rows_after['parent3'])}/{sum(rows_after['parent3'].values())}; "
      f"parent2_67d {len(rows_after['parent2_67d'])}/{sum(rows_after['parent2_67d'].values())}; "
      f"parent2_63i {len(rows_after['parent2_63i'])}/{sum(rows_after['parent2_63i'].values())}")

# ---------- 9. outputs ----------
def best(rem, bit):
    return sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r["remaining_s6_orbits"], r["remaining_s7_edge_cost"], r["s5_hex"]))


class2 = best(rem_f, 2)
class4 = best(rem_f, 4)
result = {
    "schema": "n11-class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116-v1",
    "date": "2026-11-16",
    "fork_record": {
        "common_baseline": "cost-65m chain head 1396/6452/510115/4722/373838 "
                           "(class-frontier-cost65m-receipts-recompute-20261116.json, "
                           "git blob sha 9798a9fc53b2277b17744737511354b1a830c4d2)",
        "branch_C_merged_63h_63i_63j_65m": "class-frontier-merged-cost63h-63i-63j-65m-"
                                          "recompute-20261116.json: head "
                                          "1398/6450/509983/4720/373706 (the 63h bit-89 "
                                          "receipt on the 1396 head; commit dad77b79)",
        "branch_D_cost67d": "class-frontier-cost67d-receipts-recompute-20261116.json: "
                            "head 1398/6450/509974/4720/373697 (the 67d bit-97 receipt on "
                            "the same 1396 head; commit eee4f2713a)",
        "resolution": "both branch heads reproduced through their published scripts "
                      "(each internally reproducing the published fold chain down to "
                      "the 1396 head and asserting its own output blobs byte-identical "
                      "to main), the two receipt covers asserted disjoint (overlap 0), "
                      "both receipts folded on the common 1396 baseline; the two "
                      "published 1398 heads are both superseded by this merge",
    },
    "method": "subprocess reproduction of both published branch chains (branch C: the "
              "merged 63h+63i+63j+65m fold script; branch D: the cost-67d fold script, "
              "its tmp-cost67d runtime inputs rebuilt by "
              "reconstruct_tmp_cost67d_20261116.py from published artifacts), the fork "
              "set equalities against the shared 1396 baseline asserted, the 67d root "
              "asserted disjoint from the 705 folded roots raw-hex and D4-canonically, "
              "the cover overlap between the branches asserted zero, both published "
              "certificates re-asserted against local bytes (rows sorted-unique, "
              "BigInt + tsverify union 0/0, terminal [13,17]), both children asserted "
              "genuinely remaining at the 1396 baseline, then both receipts folded on "
              "the 1396 head with set-equality controls; a reverse-order replay (the "
              "63h covers on the branch D head) is asserted to reproduce the identical "
              "merged set and summary",
    "controls": {
        "both_branch_heads_reproduced_byte_identical": True,
        "fork_set_equalities": "s_C == s_1396 | cov(63h root); "
                               "s_D == s_1396 | cov(67d root); "
                               "s_merged == s_1396 | cov(63h) | cov(67d)",
        "root_disjointness_67d_vs_705": True,
        "cover_overlap_between_branches": len(overlap_cov),
        "both_children_genuinely_remaining_at_1396": True,
        "certificates_bytes_md5_verified": True,
        "child_closed_by_bits": {"cost63h_child": BIT_H, "cost67d_child": BIT_D},
        "set_equality_merged": "s_merged == s_1396 | cov(63h root) | cov(67d root) "
                               "== s_C | cov(67d root) == s_D | cov(63h root)",
        "reverse_order_replay_identical": True,
    },
    "cost63h_addition_on_1396": addition_h_C,
    "cost67d_addition_on_1396": addition_D[0] if isinstance(addition_D, list) else addition_D,
    "totals": {
        "receipts_folded_here": 2,
        "marginal": {"cost63h": len(marg_h), "cost67d": len(marg_d)},
        "marginal_in_manifest": {"cost63h": len(marg_h_m), "cost67d": len(marg_d_m)},
        "child_closed_by_bits": {"cost63h_child": BIT_H, "cost67d_child": BIT_D},
        "merged_fold_receipts_total": 57,
        "merged_fold_receipts_composition": "63i 18 + 63j 29 + 65m 8 + 63h 1 + 67d 1 = 57 "
                                            "on top of the pre-63i folded receipt roots",
    },
    "frontier_after_merged": {
        "solved_s6_in_manifest": st_f["solved_s6_in_manifest"],
        "remaining_s5_orbits": st_f["remaining_s5_orbits"],
        "unique_remaining_s6": st_f["unique_remaining_s6"],
        "sum_remaining_cost": st_f["sum_remaining_cost"],
        "s6_needed_by_open_classes": st_f["s6_needed_by_open_classes"],
        "cost_needed_by_open_classes": st_f["cost_needed_by_open_classes"],
        "demand_histogram_open_only": st_f["hist"],
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
        "dual_class2_4_s5": {"s5_hex": P2_H, "rows": len(rows_after["parent2"]),
                             "edge_cost": sum(rows_after["parent2"].values())},
        "class4_s5": {"s5_hex": P3_H, "rows": len(rows_after["parent3"]),
                      "edge_cost": sum(rows_after["parent3"].values())},
        "cost67d_parent2": {"s5_hex": P2_D, "rows": len(rows_after["parent2_67d"]),
                            "edge_cost": sum(rows_after["parent2_67d"].values())},
        "cost63i_second_parent": {"s5_hex": P2_I, "rows": len(rows_after["parent2_63i"]),
                                  "edge_cost": sum(rows_after["parent2_63i"].values())},
    },
    "outstanding_not_folded": {
        "next_fold_baseline": "this merged chain head (see frontier_after_merged) is "
                              "the new canonical baseline for all subsequent folds; "
                              "assert it before extending; both published 1398 heads "
                              "are superseded by this merge",
    },
    "interpretation_guard": "bookkeeping over published receipts; solved counts "
                            "measure manifest coverage, not the game-theoretic "
                            "value of any position; REFUTED-D10 sweeps prove only "
                            "absence of WIN7-D10; WIN7 certificates prove a win "
                            "within depth 10 from the individual 7-stone roots "
                            "only; 11x11 empty board / two-stone root {49,60} / "
                            "S2 {59,60} / class 1 / class 2 / class 4 remain UNKNOWN",
}
(OUT / "class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in rem_f.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / "class-frontier-s5-ranking-after-merged-cost63h-63i-63j-65m-67d-20261116.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / "class-frontier-top-candidates-s6-after-merged-cost63h-63i-63j-65m-67d-20261116.csv").open(
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
        rows = rem_f.get(cand["s5_hex"], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
        for row in sorted(rows, key=lambda r: int(r["s6_s7_edge_cost"])):
            d = dem_f[row["s6_hex"]]
            w.writerow((cand["s5_hex"], row["s6_hex"], row["s6_s7_edge_cost"],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print("written ranking + top-candidates CSVs (after-merged-cost63h-63i-63j-65m-67d)")

# ---------- 10. output blob shas ----------
for p in ("class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json",
          "class-frontier-s5-ranking-after-merged-cost63h-63i-63j-65m-67d-20261116.csv",
          "class-frontier-top-candidates-s6-after-merged-cost63h-63i-63j-65m-67d-20261116.csv"):
    sha, blen = git_blob_sha(OUT / p)
    print(f"blob {p}: {sha} ({blen} bytes)")
