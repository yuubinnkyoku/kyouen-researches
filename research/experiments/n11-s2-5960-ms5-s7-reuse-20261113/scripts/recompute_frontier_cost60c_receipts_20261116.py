#!/usr/bin/env python3
"""Fold the single cost-60c WIN7-D10 receipt (bit 92) on the cost-75e chain
head 1407/6441/509300/4711/373023, producing the new canonical head
1410/6438/509109/4711/373023.

The cost-60c child 00000000000000003800000008008020 (edge cost 60, dual
class-1+class-2 demand c1=1,c2=1,c4=0) was selected by the cross-cover
neighbor analysis of the three STERILE rows of the best coverable class-2
candidate S5 (the cost-65k / 70j / 74h children): the cost-60 child is the
cheapest (cost 60) one-stone-replacement open-row neighbor of the STERILE
cost-70j child, and exactly one of its 60 legal candidate roots (bit 119)
covers the STERILE 70j row.  The sweep (commit 57f6678a) found 1 WIN7-D10
(bit 92) / 59 REFUTED-D10 / 0 capped, 25,197,741 nodes; bit 119 is
REFUTED-D10, so the 70j row is NOT closed via this child (negative fact).
The bit-92 WIN7 certificate (27,547 rows / 45 sub-roots / 804,782
extraction nodes, 996,758 bytes) is published with BigInt union 0/0 and
Bareiss 45/45 double verification records.

This script reproduces the cost-75e chain head 1407 (running the published
cost-75e fold script, which internally reproduces the whole reconciliation
chain byte-identically), re-asserts the three cost-75e output blobs, then
re-derives the cost-60c sweep from the 8 blob-pinned raw batch JSONLs,
re-asserts the published sweep audit / claim v2 / win7-certificates manifest
blobs and the published bit-92 certificate (md5 + git blob byte pins,
sorted-unique rows, BigInt union 0/0 + Bareiss 45/45 records), asserts root
disjointness of the single new root against all 717 folded roots (713 + 4
cost-75e), asserts the child genuinely remaining at 1407 (both open parents
hold the child row at edge cost 60, demand c1=1,c2=1,c4=0, and the STERILE
70j row remains open), then folds the single receipt on 1407.

Pre-registered expectations: the receipt's in-manifest marginals are exactly
the child row (edge 60) plus 00000000000000801092200000000000 (edge 59) and
00000000000000801292000000000000 (edge 72) - the two later being rows of
both the class-1 lift parent (74/5399 -> 72/5280, losing the child + the
edge-59 row), the class-2 lift parent (50/3551 -> 49/3491, losing the
child), the class-1 shared parent 00000000000000801092000000000000
(79/6044 -> 77/5913, losing the edge-59 + edge-72 rows) and the class-2
shared parent 00000000000000801212000000000000 (69/5448 -> 68/5376, losing
the edge-72 row); the new head is 1410/174/6438/509109/4711/373023 with the
open-only demand histogram unchanged (all three closed rows have c1>0, so
s6_needed_by_open_classes and cost_needed_by_open_classes are invariant);
the 70j row stays open (demand c1=1,c2=1,c4=0) and the best coverable
class-2 candidate S5 keeps its 3 STERILE rows 65k/70j/74h; the top
candidates (best class-4, audit-blocked class-2, best/second coverable
class-2) are unchanged, so the top-candidates CSV is byte-identical to the
cost-75e one.

Everything is re-derived from published artifacts; the unpublished
tmp-cost* extraction intermediates are reconstructed by the published
reconstruct_tmp_* scripts (plus reconstruct_tmp_cost58c_84a_20261116.py for
the two never-published directories), so no unpublished local state is
required.

11x11 empty board / two-stone root {49,60} / S2 {59,60} / class 1 / class 2 /
class 4 remain UNKNOWN; this is receipt bookkeeping only.
"""
import csv
import hashlib
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost60c-certificates"

CHILD = "00000000000000003800000008008020"
CHILD_V = int(CHILD, 16)
WIN_BIT = 92
ROOT = "00000000100000003800000008008020"
ROOT_D4 = "00000000000000801292200000000000"
P_C2 = "00000000000000003800000008008000"   # class-2 lift parent 50/3551
P_C1 = "00000000000000003800000000008020"   # class-1 lift parent 74/5399
SH_C1 = "00000000000000801092000000000000"  # class-1 shared parent 79/6044
SH_C2 = "00000000000000801212000000000000"  # class-2 shared parent 69/5448
MIM59 = "00000000000000801092200000000000"  # in-manifest marginal, edge 59
MIM72 = "00000000000000801292000000000000"  # in-manifest marginal, edge 72
ROW_70J = "00000000000000801282000000200000"  # STERILE cost-70j row
ROW_65K = "00000000020000801202000000200000"  # STERILE cost-65k row
ROW_74H = "00000000000000889002000000000800"  # STERILE cost-74h row
BEST_COVERABLE_C2 = "00000000000000801202000000200000"  # 3/209, all STERILE
SECOND_COVERABLE_C2 = "00000000000000801202000040000000"  # 5/364
AUDIT_BLOCKED = "00000000000000809082000000000000"  # 10/698
SWEEP_AUDIT_BLOB = "492095735eda127dac9dc465bbff1844f3c818f1"
CERTS_MANIFEST_BLOB = "f76cd7dd10364f8110389e6c3aa082d5dff20b83"
CLAIM_V2_BLOB = "5b9df50226f5420c03af39813c55b247992deaf6"
CERT_BLOB = "b35128897b07f03e4baa11583423453cb378e18d"
E75E_JSON_BLOB = "5cd93de7ee8943681549b8f97918f6112548b373"
E75E_RANKING_BLOB = "2154bcb98afd59239808336763dae7de1f203abd"
E75E_TOPCAND_BLOB = "08aaf31892680668e7e292848235a154eb746407"


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


_orig_write_text = Path.write_text


def _write_text_lf(self, data, encoding=None, errors=None, newline=None):
    with self.open("w", encoding=encoding or "utf-8", errors=errors,
                   newline="\n") as f:
        f.write(data)


Path.write_text = _write_text_lf

# ---------- 1. reproduce the cost-75e chain head 1407 ----------
ns75 = runpy.run_path(str(HERE / "scripts" /
                          "recompute_frontier_cost75e_receipts_"
                          "20261116.py"))
s_1407 = set(ns75["s_after"])
st_1407 = ns75["st_after"]
rem_1407 = ns75["rem_after"]
dem_1407 = ns75["dem_after"]
covers = ns75["covers"]
manifest = ns75["manifest"]
classes = ns75["classes"]
summary_state = ns75["summary_state"]
canon = ns75["canon"]
assert (st_1407["solved_s6_in_manifest"], st_1407["remaining_s5_orbits"],
        st_1407["unique_remaining_s6"], st_1407["sum_remaining_cost"],
        st_1407["s6_needed_by_open_classes"],
        st_1407["cost_needed_by_open_classes"]) == \
    (1407, 174, 6441, 509300, 4711, 373023), st_1407
for name, sha_exp in (
        ("class-frontier-cost75e-receipts-recompute-20261116.json",
         "5cd93de7ee8943681549b8f97918f6112548b373"),
        ("class-frontier-s5-ranking-after-cost75e-receipts-20261116.csv",
         "2154bcb98afd59239808336763dae7de1f203abd"),
        ("class-frontier-top-candidates-s6-after-cost75e-receipts-"
         "20261116.csv",
         "08aaf31892680668e7e292848235a154eb746407")):
    sha, blen = git_blob_sha(OUT / name)
    assert sha == sha_exp, name
roots_75e = {int(h, 16) for h in ns75["ROOTS"].values()}
folded = set(ns75["folded"]) | roots_75e
assert len(folded) == 717, len(folded)
print("CONTROL cost-75e chain head 1407/6441/509300/4711/373023 reproduced; "
      "the three cost-75e output blobs re-asserted byte-identical; 717 "
      "folded roots (713 reconciled + 4 cost-75e)")

# ---------- 2. re-derive the cost-60c sweep from the raw batches ----------
sha, blen = git_blob_sha(OUT / "class2-lane-cost60c-sweep-audit-20261116.json")
assert sha == SWEEP_AUDIT_BLOB and blen == 8168, "sweep audit blob"
audit = json.loads((OUT / "class2-lane-cost60c-sweep-audit-20261116.json")
                   .read_text())
assert audit["target"]["s6_child_hex"] == CHILD
assert audit["target"]["legal_candidate_count"] == 60
sha, blen = git_blob_sha(OUT / "class2-lane-cost60c-inflight-20261116.json")
assert sha == CLAIM_V2_BLOB, "claim v2 blob"
claim = json.loads((OUT / "class2-lane-cost60c-inflight-20261116.json")
                   .read_text())
bit_recs = {}
pilots = 0
for i in range(1, 9):
    p = OUT / f"class2-lane-cost60c-raw-batch{i}-20261116.jsonl"
    lines = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    for rec in lines:
        if "control" in rec:
            pilots += 1
            assert rec["control"] == "pilot_d6" and rec["loss"] is False \
                and rec["capped"] is False and rec["nodes"] == 3402, rec
        else:
            assert rec["bit"] not in bit_recs, "each bit exactly once"
            bit_recs[rec["bit"]] = rec
assert pilots == 8 and len(bit_recs) == 60
win_bits = sorted(b for b, r in bit_recs.items() if r["loss"] is True)
refuted = sum(1 for r in bit_recs.values()
              if r["loss"] is False and r["capped"] is False)
capped = sum(1 for r in bit_recs.values() if r["capped"] is True)
node_sum = sum(r["nodes"] for r in bit_recs.values())
assert win_bits == [WIN_BIT] and refuted == 59 and capped == 0
assert node_sum == 25197741, node_sum
assert all(r["terminalStoneRange"] == [13, 17] for r in bit_recs.values())
assert all(r["andclose"] is True for r in bit_recs.values())
assert bit_recs[119]["loss"] is False, \
    "the unique cross-cover root of the STERILE 70j row is REFUTED-D10"
assert f"{CHILD_V | (1 << WIN_BIT):032x}" == ROOT
assert audit["win_root"]["root_hex"] == ROOT
assert audit["win_root"]["d4_canonical_hex"] == ROOT_D4
# determinism rerun (batch5) node-exact vs raw batch5
det = [json.loads(x) for x in
       (OUT / "class2-lane-cost60c-v16-determinism-rerun-20261116.jsonl")
       .read_text().splitlines() if x.strip()]
det_bits = {r["bit"]: r for r in det if "bit" in r}
for b, r in det_bits.items():
    o = bit_recs[b]
    assert (r["loss"], r["nodes"], r["capped"], r["terminalStoneRange"]) == \
        (o["loss"], o["nodes"], o["capped"], o["terminalStoneRange"]), b
# v15 crosscheck
v15 = [json.loads(x) for x in
       (OUT / "class2-lane-cost60c-v15-crosscheck-20261116.jsonl")
       .read_text().splitlines() if x.strip()]
v15_bits = {r["bit"]: r for r in v15 if "bit" in r}
assert next(r for r in v15 if "control" in r)["nodes"] == 5949
assert v15_bits[WIN_BIT]["loss"] is True
assert all(v15_bits[b]["loss"] is False for b in (119, 0, 120))
print("CONTROL cost-60c sweep re-derived from the 8 raw batches: 60 "
      "candidates, WIN7-D10 bit 92, 59 REFUTED-D10 (incl. bit 119, the "
      "unique cross-cover root of the STERILE 70j row), 0 capped, "
      "25,197,741 nodes, terminal [13,17] all; determinism rerun batch5 "
      "node-exact; v15 crosscheck agrees (pilot 5949)")

# ---------- 3. re-assert the published bit-92 certificate ----------
sha, blen = git_blob_sha(OUT / "class2-lane-cost60c-win7-certificates-"
                         "20261116.json")
assert sha == CERTS_MANIFEST_BLOB and blen == 4542, "certificates manifest blob"
cman = json.loads((OUT / "class2-lane-cost60c-win7-certificates-"
                   "20261116.json").read_text())
e = next(c for c in cman["certificates"] if c["bit"] == WIN_BIT)
assert e["verdict"] == "WIN7" and e["child_hex"] == CHILD
assert e["root_hex"] == ROOT
root_v = int(e["root_hex"], 16)
assert root_v == CHILD_V | (1 << WIN_BIT)
assert e["d4_canonical_hex"] == ROOT_D4 == f"{canon(root_v):032x}"
cert_path = CERTS / f"bit{WIN_BIT}-root-{ROOT}.cert"
sha, blen = git_blob_sha(cert_path)
assert sha == CERT_BLOB and blen == 996758, "cert git blob"
data = cert_path.read_bytes()
assert hashlib.md5(data).hexdigest() == \
    e["published_cert"]["whole_md5"] == "d771ef8275a9889a22974310e5c1e411"
text = data.decode()
lines = text.split("\n")
assert lines[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                    "second_to_move_LOSS")
assert lines[1] == f"root {ROOT}"
rows = lines[2:]
assert rows[-1] == "", "trailing newline"
rows = rows[:-1]
assert len(rows) == e["rows"] == 27547
assert rows == sorted(set(rows)), "sorted-unique rows"
bigint = json.loads((CERTS / f"bit{WIN_BIT}-root-{ROOT}"
                     ".bigint-verify.json").read_text())["bigint_record"]
assert bigint["union_missing"] == 0 and bigint["union_extra"] == 0
assert bigint["subroots_passed"] == e["sub_roots"] == 45
assert bigint["terminal_range"] == [13, 17]
assert bigint["winner_states"] == 38090 and bigint["loser_states"] == 12028
bare = json.loads((CERTS / f"bit{WIN_BIT}-root-{ROOT}"
                   "-bareiss-verify.json").read_text())
assert bare["subroots_verified"] == 45 and bare["all_subroots_pass"] is True
tot = cman["totals"]
assert (tot["published_certificates"], tot["rows"], tot["extraction_nodes"],
        tot["sub_roots"], tot["winner_states"], tot["loser_states"],
        tot["terminal_count"], tot["cert_bytes"]) == \
    (1, 27547, 804782, 45, 38090, 12028, 8543, 996758)
print("CONTROL the published bit-92 certificate re-asserted: manifest blob "
      "pinned, root = child | 1<<92, D4 canonical, md5 + git blob byte pins, "
      "27,547 sorted-unique rows, BigInt union 0/0 (45/45 sub-roots, "
      "terminals [13,17], 38,090 winner / 12,028 loser states) and Bareiss "
      "45/45 double verification")

# ---------- 4. root disjointness against all 717 folded roots ----------
new_root = int(ROOT, 16)
assert new_root not in folded, "raw-hex disjointness vs the 717 folded roots"
folded_d4 = {f"{canon(r):032x}" for r in folded}
assert ROOT_D4 not in folded_d4
print("CONTROL root disjointness: the cost-60c root vs the 717 folded roots "
      "(713 reconciled + 4 cost-75e), raw-hex and D4-canonically")

# ---------- 5. the cost-60c child genuinely remaining at 1407 ----------
assert CHILD_V in manifest and CHILD_V not in s_1407
rows_c2 = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1407[P_C2]}
rows_c1 = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1407[P_C1]}
assert CHILD in rows_c2 and rows_c2[CHILD] == 60
assert CHILD in rows_c1 and rows_c1[CHILD] == 60
assert (len(rows_c2), sum(rows_c2.values())) == (50, 3551)
assert (len(rows_c1), sum(rows_c1.values())) == (74, 5399)
d = dem_1407[CHILD]
assert (d["c1"], d["c2"], d["c4"]) == (1, 1, 0), d
d70 = dem_1407[ROW_70J]
assert (d70["c1"], d70["c2"], d70["c4"]) == (1, 1, 0), d70
print("CONTROL cost-60c child genuinely remaining at 1407: class-2 lift "
      "parent 50 rows/3551 and class-1 lift parent 74 rows/5399 both hold "
      "the child row at edge cost 60, demand c1=1,c2=1,c4=0; the STERILE "
      "70j row also remains open (c1=1,c2=1,c4=0)")

# ---------- 6. fold the single receipt on 1407 ----------
cov = covers(new_root)
assert CHILD_V in cov, "the root covers the child via its added stone"
marg = cov - s_1407
marg_m = marg & manifest
mim_hexes = sorted(f"{k:032x}" for k in marg_m)
assert mim_hexes == [CHILD, MIM59, MIM72], mim_hexes
addition = [{
    "bit": WIN_BIT, "root_hex": ROOT, "d4_canonical_hex": ROOT_D4,
    "certified": True, "covers": len(cov), "marginal": len(marg),
    "marginal_in_manifest": len(marg_m),
    "marginal_manifest_hexes": mim_hexes,
    "marginal_non_manifest_hexes":
        sorted(f"{k:032x}" for k in marg - marg_m),
    "rows": e["rows"], "md5": e["published_cert"]["whole_md5"],
    "sub_roots_pass": e["sub_roots"],
    "extraction_nodes": e["extraction_nodes"],
    "terminal_count": e["terminal_count"],
}]
assert ROW_70J not in {f"{k:032x}" for k in cov}, \
    "the receipt does not cover the STERILE 70j row (bit-119 negative fact)"
s_after = s_1407 | marg
assert s_after == s_1407 | cov, "set-equality: s_after == s_1407 | cov(root)"
total_marg = len(marg)
total_mim = len(marg_m)
assert total_mim == 3
st_after, rem_after, uniq_after, dem_after = summary_state(s_after)
assert st_after["solved_s6_in_manifest"] == 1407 + total_mim == 1410
assert (st_after["solved_s6_in_manifest"], st_after["remaining_s5_orbits"],
        st_after["unique_remaining_s6"], st_after["sum_remaining_cost"],
        st_after["s6_needed_by_open_classes"],
        st_after["cost_needed_by_open_classes"]) == \
    (1410, 174, 6438, 509109, 4711, 373023), \
    "pre-registered prediction: new head 1410/174/6438/509109/4711/373023"
assert st_after["hist"] == st_1407["hist"], \
    "open-only demand histogram unchanged (all 3 closed rows have c1>0)"
print("AFTER cost-60c fold:", json.dumps(st_after, indent=1))

# ---------- 7. per-parent rows at the new head ----------
cov_hexes = {f"{k:032x}" for k in cov}
parents_after = {}
lost_detail = {}
for name, h, old_exp, new_exp in (
        ("class1_lift_parent", P_C1, (74, 5399), (72, 5280)),
        ("class2_lift_parent", P_C2, (50, 3551), (49, 3491)),
        ("class1_shared_parent", SH_C1, (79, 6044), (77, 5913)),
        ("class2_shared_parent", SH_C2, (69, 5448), (68, 5376)),
        ("second_candidate_s5", SECOND_COVERABLE_C2, (5, 364), (5, 364)),
        ("best_coverable_class2", BEST_COVERABLE_C2, (3, 209), (3, 209)),
        ("audit_blocked_class2", AUDIT_BLOCKED, (10, 698), (10, 698)),
        ("cost75e_parent2", "00000000000000801202000000000200",
         (65, 5316), (65, 5316))):
    old = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1407.get(h, [])}
    new = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_after.get(h, [])}
    lost = {k: v for k, v in old.items() if k not in new}
    assert set(lost) <= cov_hexes, (name, sorted(set(lost) - cov_hexes))
    assert new == {k: v for k, v in old.items() if k not in lost}, name
    assert (len(old), sum(old.values())) == old_exp, (name, len(old),
                                                      sum(old.values()))
    assert (len(new), sum(new.values())) == new_exp, (name, len(new),
                                                      sum(new.values()))
    parents_after[name] = {"s5_hex": h, "rows": len(new),
                           "edge_cost": sum(new.values())}
    lost_detail[name] = lost
assert lost_detail["class1_lift_parent"] == {CHILD: 60, MIM59: 59}
assert lost_detail["class2_lift_parent"] == {CHILD: 60}
assert lost_detail["class1_shared_parent"] == {MIM59: 59, MIM72: 72}
assert lost_detail["class2_shared_parent"] == {MIM72: 72}
assert lost_detail["second_candidate_s5"] == {}
assert lost_detail["best_coverable_class2"] == {}
# the three STERILE rows of the best coverable class-2 candidate stay open
rows_bc = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
           for r in rem_after[BEST_COVERABLE_C2]}
assert {rows_bc[ROW_65K], rows_bc[ROW_70J], rows_bc[ROW_74H]} == {65, 70, 74}
d70a = dem_after[ROW_70J]
assert (d70a["c1"], d70a["c2"], d70a["c4"]) == (1, 1, 0)
print("per-parent rows at the new head: " + "; ".join(
    f"{k} {v['rows']}/{v['edge_cost']}" for k, v in parents_after.items()))

# ---------- 8. rankings at the new head ----------


def best(rem, bit):
    return sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"])
                                        for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r["remaining_s6_orbits"], r["remaining_s7_edge_cost"],
                       r["s5_hex"]))


def as_tuples(cands):
    return [(c["s5_hex"], c["classes"], c["remaining_s6_orbits"],
             c["remaining_s7_edge_cost"]) for c in cands]


class2 = best(rem_after, 2)
class4 = best(rem_after, 4)
assert as_tuples([next(c for c in class2
                       if c["s5_hex"] == AUDIT_BLOCKED)]) == \
    [(AUDIT_BLOCKED, 3, 10, 698)]
assert as_tuples(class2[0:1]) == [(BEST_COVERABLE_C2, 2, 3, 209)]
coverable = [c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED]
assert as_tuples(coverable[0:2]) == \
    [(BEST_COVERABLE_C2, 2, 3, 209), (SECOND_COVERABLE_C2, 2, 5, 364)]
assert as_tuples([next(c for c in class2 if c["s5_hex"] == P_C2)]) == \
    [(P_C2, 2, 49, 3491)]
sh_c2_c = next(c for c in class2 if c["s5_hex"] == SH_C2)
assert (sh_c2_c["remaining_s6_orbits"], sh_c2_c["remaining_s7_edge_cost"]) == \
    (68, 5376), sh_c2_c
assert as_tuples(class4[0:2]) == [("00000000020000003800000080000000", 4, 18,
                                  1460),
                                 ("00000000000000003800002000800000", 4, 60,
                                  4216)]

sha_75e, blen_75e = git_blob_sha(
    OUT / "class-frontier-cost75e-receipts-recompute-20261116.json")

result = {
    "schema": "n11-class-frontier-cost60c-receipts-20261116-v1",
    "date": "2026-11-16",
    "baseline_record": {
        "cost75e_head_1407": "class-frontier-cost75e-receipts-"
                            "recompute-20261116.json: head "
                            "1407/174/6441/509300/4711/373023 "
                            f"(git blob sha {sha_75e}, {blen_75e} bytes, "
                            "commit dd623408, re-produced byte-identically "
                            "by this run)",
        "claim": "class2-lane-cost60c-inflight-20261116.json (v1 in-flight "
                 "claim commit a20fff85, republished as the v2 completed "
                 f"record in commit 57f6678a, git blob sha {CLAIM_V2_BLOB})",
        "sweep_audit": "class2-lane-cost60c-sweep-audit-20261116.json "
                       f"(git blob sha {SWEEP_AUDIT_BLOB}, commit "
                       "57f6678a)",
        "selection": "the cheapest unswept one-stone-replacement neighbor of "
                     "the STERILE cost-70j child (dual class-1+class-2 "
                     "demand); exactly one of the 60 legal candidate roots "
                     "(bit 119) covers the STERILE 70j row",
    },
    "method": "runpy reproduction of the published cost-75e fold script "
              "(internally reproducing the whole reconciliation chain and "
              "the cost-75e fold byte-identically, re-asserting the three "
              "cost-75e output blobs), re-derivation of the cost-60c sweep "
              "from the 8 raw batch JSONLs (60 candidates, WIN7-D10 bit 92, "
              "59 REFUTED-D10, 0 capped, 25,197,741 nodes, determinism rerun "
              "batch5 node-exact, v15 crosscheck agreement incl. the "
              "REFUTED bit-119 cross-cover root), re-assertion of the "
              "published bit-92 certificate against the certificates "
              "manifest blob (root = child | 1<<92, D4 canonical hex, md5 "
              "and git blob byte pins, 27,547 sorted-unique rows, BigInt "
              "union 0/0 and Bareiss 45/45 double verification records), "
              "root disjointness of the single new root against all 717 "
              "folded roots raw-hex and D4-canonically, the child asserted "
              "genuinely remaining at 1407 (both lift parents hold the "
              "child row at edge cost 60, demand c1=1,c2=1,c4=0, the "
              "STERILE 70j row also open), then the single receipt folded "
              "on 1407 with pre-registered in-manifest marginals and a "
              "set-equality control",
    "controls": {
        "cost75e_head_1407_reproduced": True,
        "cost75e_output_blobs_byte_identical": True,
        "sweep_rederived_from_raw_batches": True,
        "determinism_rerun_batch5_node_exact": True,
        "v15_crosscheck_agrees": True,
        "bit119_cross_cover_root_refuted": True,
        "certificates_manifest_blob_pinned": True,
        "certificate_md5_and_git_blob_pins_reasserted": True,
        "certificate_bigint_union_0_0_and_bareiss_45_45": True,
        "root_disjointness_1_vs_717": True,
        "child_genuinely_remaining_at_1407": True,
        "sterile_70j_row_not_covered_by_this_receipt": True,
        "set_equality_after": "s_after == s_1407 | cov(cost-60c root)",
        "pre_registered_prediction_holds":
            "1410/174/6438/509109/4711/373023",
    },
    "cost60c_addition_on_cost75e_1407": addition,
    "totals": {
        "receipts": 1,
        "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "child_closed_by_bit": WIN_BIT,
        "in_manifest_marginals": [
            {"hex": MIM59, "edge_cost": 59,
             "was_row_of": {"class1_lift_parent": 59,
                            "class1_shared_parent": 59}},
            {"hex": MIM72, "edge_cost": 72,
             "was_row_of": {"class1_shared_parent": 72,
                            "class2_shared_parent": 72}},
        ],
        "certificate_rows": 27547,
        "certificate_bytes": 996758,
        "certificate_sub_roots": 45,
        "certificate_extraction_nodes": 804782,
        "sweep_nodes": 25197741,
    },
    "frontier_after_cost60c": {
        "solved_s6_in_manifest": st_after["solved_s6_in_manifest"],
        "remaining_s5_orbits": st_after["remaining_s5_orbits"],
        "unique_remaining_s6": st_after["unique_remaining_s6"],
        "sum_remaining_cost": st_after["sum_remaining_cost"],
        "s6_needed_by_open_classes": st_after["s6_needed_by_open_classes"],
        "cost_needed_by_open_classes":
            st_after["cost_needed_by_open_classes"],
        "demand_histogram_open_only": st_after["hist"],
        "best_class2": class2[0] if class2 else None,
        "audit_blocked_class2": next((c for c in class2
                                      if c["s5_hex"] == AUDIT_BLOCKED), None),
        "best_coverable_class2": next((c for c in class2
                                       if c["s5_hex"] != AUDIT_BLOCKED),
                                      None),
        "next_class2": coverable[1:4],
        "best_class4": class4[0] if class4 else None,
        "next_class4": class4[1:4],
    },
    "parents_after": parents_after,
    "lost_rows_per_parent": lost_detail,
    "sterile_rows_status": {
        "row_65k": {"hex": ROW_65K, "open": True, "demand": "c1=1,c2=1,c4=0"},
        "row_70j": {"hex": ROW_70J, "open": True, "demand": "c1=1,c2=1,c4=0",
                    "cross_cover_via_cost60c": "failed: the unique "
                    "cross-cover root (bit 119) is REFUTED-D10; next "
                    "candidate neighbor cost 62 "
                    "00000000000000801282020000000000 to be pre-checked for "
                    "70j-row coverage before sweeping"},
        "row_74h": {"hex": ROW_74H, "open": True, "demand": "c1=1,c2=1,c4=0"},
    },
    "coordination": {
        "cost60c_claim_retires": "class2-lane-cost60c-inflight-20261116.json "
                                 "(v2, completed) is closed by this fold; "
                                 "the fold and the new head 1410 are "
                                 "recorded here",
        "cost76c_inflight_claim": "the cost-76c claim references the 1407 "
                                  "head; if its fold lands, it must re-base "
                                  "onto this 1410 head (root disjointness "
                                  "against this 1 root to be asserted by "
                                  "that fold)",
        "cost76d_cost77e_parallel_claims": "the parallel cost-76d / 77e "
                                           "certificate lanes pin the 1405 "
                                           "head; if their folds land on "
                                           "1405 or 1407, the resulting head "
                                           "must be reconciled with this "
                                           "1410 head",
        "next_neighbor_candidate": "cost 62 00000000000000801282020000000000 "
                                   "(parents 73/5489 and 49/3360 at 1410), "
                                   "the next cheapest unswept "
                                   "one-stone-replacement neighbor of the "
                                   "STERILE 70j child; pre-compute whether "
                                   "any legal root covers the 70j row "
                                   "before sweeping",
    },
    "interpretation_guard": "bookkeeping over published receipts; solved "
                            "counts measure manifest coverage, not the "
                            "game-theoretic value of any position; WIN7 "
                            "certificates prove a first-player win within "
                            "depth 10 from the individual 7-stone roots "
                            "only; REFUTED-D10 sweeps prove only absence of "
                            "WIN7-D10; STERILE rows are unclosable by "
                            "depth-10 WIN7 receipts from their own rows, "
                            "which is NOT a LOSS proof; 11x11 empty board / "
                            "two-stone root {49,60} / S2 {59,60} / "
                            "class 1 / class 2 / class 4 remain UNKNOWN",
}
(OUT / "class-frontier-cost60c-receipts-recompute-20261116.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-cost60c-receipts-recompute-20261116.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in rem_after.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / ("class-frontier-s5-ranking-after-cost60c-receipts-"
             "20261116.csv")).open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits",
                "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / ("class-frontier-top-candidates-s6-after-cost60c-receipts-"
             "20261116.csv")).open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    for label, cand in (("best class-4 blocker-candidate S5",
                         class4[0] if class4 else None),
                        ("best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)",
                         next((c for c in class2
                               if c["s5_hex"] == AUDIT_BLOCKED), None)),
                        ("best coverable class-2 blocker-candidate S5",
                         coverable[0] if coverable else None),
                        ("second coverable class-2 candidate S5",
                         coverable[1] if len(coverable) > 1 else None)):
        if cand is None:
            continue
        rows = rem_after.get(cand["s5_hex"], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} "
                    f"cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
        for row in sorted(rows, key=lambda r: int(r["s6_s7_edge_cost"])):
            d = dem_after.get(row["s6_hex"], {"c1": -1, "c2": -1, "c4": -1})
            w.writerow((cand["s5_hex"], row["s6_hex"], row["s6_s7_edge_cost"],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print("written ranking + top-candidates CSVs (after-cost60c-receipts)")

for p in ("class-frontier-cost60c-receipts-recompute-20261116.json",
          "class-frontier-s5-ranking-after-cost60c-receipts-20261116.csv",
          "class-frontier-top-candidates-s6-after-cost60c-receipts-"
          "20261116.csv"):
    sha, blen = git_blob_sha(OUT / p)
    print(f"blob {p}: {sha} ({blen} bytes)")
