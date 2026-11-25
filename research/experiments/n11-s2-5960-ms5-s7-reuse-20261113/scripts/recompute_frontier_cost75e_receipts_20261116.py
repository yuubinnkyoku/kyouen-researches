#!/usr/bin/env python3
"""Fold the four cost-75e WIN7-D10 receipts on the reconciled canonical head
1405/6443/509457/4713/373180.

The cost-75e claim (class2-lane-cost75e-inflight-20261116.json, commit bc893758)
recorded a sweep completed locally (75 candidates, 4 WIN7-D10 bits 6/10/11/37,
0 capped, 108,292,517 nodes) whose raw artifacts were lost to an environment
outage before publication.  The 2026-11-16 continuation session republished the
evidence and completed the missing pieces: the raw batches, the determinism
rerun and the v15 crosscheck (commit 725f4b65), the four WIN7-D10 certificates
(bits 10/11/37 whole, bit 6 as part1of2/part2of2 with a receipt, commits
dca46d09/5cf7f657/a27d240d/beb6c605/0fd2b1f9) and the certificates manifest.
This script re-derives the sweep totals from the raw batch JSONLs, re-asserts
all four published certificates (byte pins, md5, sorted-unique rows, BigInt
union 0/0 and Bareiss sub-root verification records), reproduces the
reconciled canonical head 1405 (running the published reconciliation script,
which re-asserts the whole chain, the 70g fold and the three reconciliation
output blobs byte-identical to main), asserts root disjointness of the 4 roots
against all 713 folded roots (706 + 7 cost-70g), asserts the child genuinely
remaining at 1405 (both open parents, demand c1=0,c2=2,c4=0), then folds the
4 receipts on 1405 in publication order.  Pre-registered prediction: the
child orbit closes exactly once (bit 6), bit 10 contributes one further
in-manifest marginal (00000000000000801202000000000201), bits 11 and 37 are
zero-marginal-in-manifest, and the new head is 1407/6441/509300/4711/373023;
the second coverable class-2 candidate S5 drops from 6 rows/439 to 5 rows/364
and the cost-75e parent2 from 67 rows/5473 to 65 rows/5316.  A reverse-order
replay reproduces the identical final set and summary.

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
CERTS = OUT / "class2-lane-cost75e-certificates"

CHILD = "00000000040000809002000000000002"
CHILD_V = int(CHILD, 16)
WIN_BITS = [6, 10, 11, 37]
ROOTS = {
    6: "00000000040000809002000000000042",
    10: "00000000040000809002000000000402",
    11: "00000000040000809002000000000802",
    37: "00000000040000809002002000000002",
}
P1_75E = "00000000000000801202000040000000"   # second coverable class-2 cand
P2_75E = "00000000000000801202000000000200"   # the 67-row cost-75e parent2
MIM10_HEX = "00000000000000801202000000000201"
AUDIT_BLOCKED = "00000000000000809082000000000000"
SWEEP_AUDIT_BLOB = "ef813af4b9046e390962cfc09214d645c8f00727"
CERTS_MANIFEST_BLOB = "a8127435e1a32e117d9dc5540acf77c6631af7c0"
REBASE_FACTS_BLOB = "8a811317b27c4006b3a43b36bfe2c61bcd438483"


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


_orig_write_text = Path.write_text


def _write_text_lf(self, data, encoding=None, errors=None, newline=None):
    with self.open("w", encoding=encoding or "utf-8", errors=errors,
                   newline="\n") as f:
        f.write(data)


Path.write_text = _write_text_lf

# ---------- 1. reproduce the reconciled canonical head 1405 ----------
nsR = runpy.run_path(str(HERE / "scripts" /
                         "recompute_frontier_reconcile_canonical1400_"
                         "cost70g_20261116.py"))
s_1405 = set(nsR["s_new"])
st_1405 = nsR["st_new"]
rem_1405 = nsR["rem_new"]
dem_1405 = nsR["dem_new"]
covers = nsR["covers"]
manifest = nsR["manifest"]
classes = nsR["classes"]
summary_state = nsR["summary_state"]
canon = nsR["canon"]
prev1400 = set(nsR["prev1400"])            # 705 branch D + the 63h root
roots_70g = {int(nsR["certs"][str(b)]["root_hex"], 16)
             for b in nsR["WIN_BITS"]}     # 7 cost-70g roots
assert (st_1405["solved_s6_in_manifest"], st_1405["remaining_s5_orbits"],
        st_1405["unique_remaining_s6"], st_1405["sum_remaining_cost"],
        st_1405["s6_needed_by_open_classes"],
        st_1405["cost_needed_by_open_classes"]) == \
    (1405, 174, 6443, 509457, 4713, 373180)
for name, sha_exp, blen_exp in (
        ("class-frontier-reconciled-canonical1400-cost70g-"
         "recompute-20261116.json",
         "b3ad19d7bfd48c771d5a6827707a9f26940dc1bb", 11352),
        ("class-frontier-s5-ranking-after-reconciled-canonical1400-"
         "cost70g-20261116.csv",
         "26fa720b9935ea3bfa1445409d941a5063c52694", 7535),
        ("class-frontier-top-candidates-s6-after-reconciled-canonical1400-"
         "cost70g-20261116.csv",
         "c3433eeecccf0098a04f227af876b37196c7c0a5", 3801)):
    sha, blen = git_blob_sha(OUT / name)
    assert sha == sha_exp and blen == blen_exp, name
sha, blen = git_blob_sha(OUT / "class2-lane-rebase-facts-75e-76c-on-"
                         "canonical1405-20261116.json")
assert sha == REBASE_FACTS_BLOB and blen == 4907, "published rebase facts"
folded = prev1400 | roots_70g
assert len(folded) == 713, len(folded)
print("CONTROL reconciled canonical head 1405/6443/509457/4713/373180 "
      "reproduced; three reconciliation output blobs + the rebase-facts blob "
      "re-asserted byte-identical; 713 folded roots (706 + 7 cost-70g)")

# ---------- 2. re-derive the sweep from the raw batches ----------
sha, blen = git_blob_sha(OUT / "class2-lane-cost75e-sweep-audit-"
                         "20261116.json")
assert sha == SWEEP_AUDIT_BLOB, "sweep audit blob"
audit = json.loads((OUT / "class2-lane-cost75e-sweep-audit-20261116.json")
                   .read_text())
assert audit["target"]["s6_child_hex"] == CHILD
assert audit["target"]["legal_candidate_count"] == 75
bit_recs = {}
pilots = 0
for b in audit["batches"]:
    p = OUT / Path(b["input_path"]).name
    sha, blen = git_blob_sha(p)
    assert sha == b["git_blob_sha"] and blen > 0, b["input_path"]
    lines = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    for rec in lines:
        if "control" in rec:
            pilots += 1
            assert rec["control"] == "pilot_d6" and rec["loss"] is False \
                and rec["capped"] is False and rec["nodes"] == 3402, rec
        else:
            assert rec["bit"] not in bit_recs, "each bit exactly once"
            bit_recs[rec["bit"]] = rec
    assert sorted(r["bit"] for r in lines if "bit" in r) == \
        b["candidate_bits"], b["input_path"]
assert pilots == 10 and len(bit_recs) == 75
win_bits = sorted(b for b, r in bit_recs.items() if r["loss"] is True)
refuted = sum(1 for r in bit_recs.values()
              if r["loss"] is False and r["capped"] is False)
capped = sum(1 for r in bit_recs.values() if r["capped"] is True)
node_sum = sum(r["nodes"] for r in bit_recs.values())
assert win_bits == WIN_BITS and refuted == 71 and capped == 0
assert node_sum == 108292517, node_sum
assert all(r["terminalStoneRange"] == [13, 17] for r in bit_recs.values())
assert all(r["andclose"] is True for r in bit_recs.values())
assert {b: f"{CHILD_V | (1 << b):032x}" for b in WIN_BITS} == \
    {int(k): v for k, v in audit["sweep_totals"]["win_roots"].items()}
# determinism rerun batch5 node-exact vs raw batch5
det = [json.loads(x) for x in
       (OUT / "class2-lane-cost75e-determinism-rerun-batch5-20261116.jsonl")
       .read_text().splitlines() if x.strip()]
det_bits = {r["bit"]: r for r in det if "bit" in r}
raw5 = {r["bit"]: r for r in bit_recs.values() if r["bit"] in det_bits}
assert len(det_bits) == 8 and set(det_bits) == set(raw5)
for b, r in det_bits.items():
    o = raw5[b]
    assert (r["loss"], r["nodes"], r["capped"], r["terminalStoneRange"]) == \
        (o["loss"], o["nodes"], o["capped"], o["terminalStoneRange"]), b
# v15 crosscheck
v15 = [json.loads(x) for x in
       (OUT / "class2-lane-cost75e-v15-crosscheck-20261116.jsonl")
       .read_text().splitlines() if x.strip()]
v15_bits = {r["bit"]: r for r in v15 if "bit" in r}
assert next(r for r in v15 if "control" in r)["nodes"] == 5949
assert all(v15_bits[b]["loss"] is True for b in WIN_BITS)
assert all(v15_bits[b]["loss"] is False for b in (96, 98, 114))
print(f"CONTROL sweep re-derived from the 10 raw batches (blob-pinned): "
      f"75 candidates, WIN7-D10 bits {win_bits}, {refuted} REFUTED-D10, "
      f"{capped} capped, {node_sum} nodes, terminal [13,17] all, andclose "
      f"all; determinism rerun batch5 node-exact; v15 crosscheck agrees "
      f"(pilot 5949, win bits loss=true, anchors 96/98/114 loss=false)")

# ---------- 3. re-assert the four published certificates ----------
sha, blen = git_blob_sha(OUT / "class2-lane-cost75e-win7-certificates-"
                         "20261116.json")
assert sha == CERTS_MANIFEST_BLOB, "certificates manifest blob"
cman = json.loads((OUT / "class2-lane-cost75e-win7-certificates-"
                   "20261116.json").read_text())
certs = {}
for bit in WIN_BITS:
    e = next(c for c in cman["certificates"] if c["bit"] == bit)
    assert e["verdict"] == "WIN7" and e["child_hex"] == CHILD
    assert e["root_hex"] == ROOTS[bit]
    root_v = int(e["root_hex"], 16)
    assert root_v == CHILD_V | (1 << bit), bit
    assert e["d4_canonical_hex"] == f"{canon(root_v):032x}", bit
    if bit == 6:
        pc = e["published_cert"]
        p1 = CERTS / "bit6-root-00000000040000809002000000000042.cert.part1of2"
        p2 = CERTS / "bit6-root-00000000040000809002000000000042.cert.part2of2"
        data = p1.read_bytes() + p2.read_bytes()
        assert len(data) == pc["whole_bytes"] == 2207870
        for part, ppath in zip(pc["parts"], (p1, p2)):
            assert part["path"].endswith(ppath.name)
            assert len(ppath.read_bytes()) == part["bytes"]
            psha, _ = git_blob_sha(ppath)
            assert psha == part["git_blob_sha"], ppath.name
        rcpt = json.loads((CERTS / "bit6.cert-receipt.json").read_text())
        assert rcpt["whole_md5"] == pc["whole_md5"] and \
            rcpt["whole_sha256"] == pc["whole_sha256"] and \
            rcpt["whole_bytes"] == pc["whole_bytes"]
    else:
        data = (CERTS / f"bit{bit}-root-{ROOTS[bit]}.cert").read_bytes()
        assert len(data) == e["published_cert"]["bytes"], bit
    assert hashlib.md5(data).hexdigest() == \
        (e["published_cert"]["md5"] if bit != 6
         else e["published_cert"]["whole_md5"]), bit
    text = data.decode()
    lines = text.split("\n")
    assert lines[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                       "second_to_move_LOSS"), bit
    assert lines[1] == f"root {ROOTS[bit]}", bit
    rows = lines[2:]
    assert rows[-1] == "", "trailing newline"
    rows = rows[:-1]
    assert len(rows) == e["rows"], bit
    assert rows == sorted(set(rows)), "sorted-unique rows"
    bigint = json.loads((CERTS / f"bit{bit}-root-{ROOTS[bit]}"
                         ".bigint-verify.json").read_text())
    assert bigint["union_missing"] == 0 and bigint["union_extra"] == 0, bit
    assert bigint["subroots_passed"] == e["sub_roots"], bit
    bare = json.loads((CERTS / f"bit{bit}-root-{ROOTS[bit]}"
                       "-bareiss-verify.json").read_text())
    assert bare["subroots_verified"] == e["sub_roots"], bit
    certs[bit] = e
tot = cman["totals"]
assert (tot["published_certificates"], tot["rows"], tot["extraction_nodes"],
        tot["sub_roots"], tot["winner_states"], tot["loser_states"],
        tot["terminal_count"], tot["cert_bytes"]) == \
    (4, 203163, 62175955, 234, 269254, 81278, 67334, 7352075)
print("CONTROL all four published certificates re-asserted: manifest blob "
      "pinned, root = child | 1<<bit, D4 canonical, md5 byte pins (bit 6 via "
      "part1of2+part2of2 with per-part blob shas and the receipt), "
      "sorted-unique rows, BigInt union 0/0 and Bareiss sub-roots; manifest "
      "totals 203,163 rows / 62,175,955 nodes / 234 sub-roots")

# ---------- 4. root disjointness against all 713 folded roots ----------
new_roots = {int(ROOTS[b], 16) for b in WIN_BITS}
assert not (new_roots & folded), "raw-hex disjointness vs the 713 folded roots"
folded_d4 = {f"{canon(r):032x}" for r in folded}
new_d4 = {f"{canon(r):032x}" for r in new_roots}
assert not (new_d4 & folded_d4) and len(new_d4) == 4
print("CONTROL root disjointness: the 4 cost-75e roots vs the 713 folded "
      "roots (706 reconciled + 7 cost-70g), raw-hex and D4-canonically")

# ---------- 5. the cost-75e child genuinely remaining at 1405 ----------
assert CHILD_V in manifest and CHILD_V not in s_1405
rows_p1 = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
           for r in rem_1405.get(P1_75E, [])}
rows_p2 = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
           for r in rem_1405.get(P2_75E, [])}
assert CHILD in rows_p1 and rows_p1[CHILD] == 75
assert CHILD in rows_p2 and rows_p2[CHILD] == 75
assert (len(rows_p1), sum(rows_p1.values())) == (6, 439)
assert (len(rows_p2), sum(rows_p2.values())) == (67, 5473)
d = dem_1405[CHILD]
assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 0), d
print("CONTROL cost-75e child genuinely remaining at 1405: second candidate "
      "S5 6 rows/439 and the 67-row parent2 67 rows/5473 both hold the child "
      "row at edge cost 75, demand c1=0,c2=2,c4=0")

# ---------- 6. fold the 4 receipts on 1405 (publication order) ----------
MIM_PRE = {6: [CHILD], 10: [MIM10_HEX], 11: [], 37: []}
s_run = set(s_1405)
addition = []
child_closed_by = None
cov4 = set()
for bit in WIN_BITS:
    e = certs[bit]
    root = int(e["root_hex"], 16)
    cov = covers(root)
    assert CHILD_V in cov, "every root covers the child via its added stone"
    cov4 |= cov
    marg = cov - s_run
    marg_m = marg & manifest
    mim_hexes = sorted(f"{k:032x}" for k in marg_m)
    assert mim_hexes == MIM_PRE[bit], (bit, mim_hexes)
    if CHILD_V in marg_m:
        assert child_closed_by is None, "the child must be closed exactly once"
        child_closed_by = bit
    addition.append({
        "bit": bit, "root_hex": e["root_hex"],
        "d4_canonical_hex": e["d4_canonical_hex"],
        "certified": True, "covers": len(cov), "marginal": len(marg),
        "marginal_in_manifest": len(marg_m),
        "marginal_manifest_hexes": mim_hexes,
        "marginal_non_manifest_hexes":
            sorted(f"{k:032x}" for k in marg - marg_m),
        "rows": e["rows"],
        "md5": e["published_cert"]["md5"] if bit != 6
        else e["published_cert"]["whole_md5"],
        "sub_roots_pass": e["sub_roots"],
        "extraction_nodes": e["extraction_nodes"],
        "terminal_count": e["terminal_count"],
    })
    s_run |= marg
assert child_closed_by == 6, "the child orbit must be closed by the bit-6 receipt"
s_after = s_run
assert s_after == s_1405 | cov4, "set-equality: s_after == s_1405 | cov(4 roots)"
total_mim = sum(a["marginal_in_manifest"] for a in addition)
total_marg = sum(a["marginal"] for a in addition)
assert total_mim == 2 and total_marg == 19
st_after, rem_after, uniq_after, dem_after = summary_state(s_after)
assert st_after["solved_s6_in_manifest"] == 1405 + total_mim == 1407
assert (st_after["solved_s6_in_manifest"], st_after["remaining_s5_orbits"],
        st_after["unique_remaining_s6"], st_after["sum_remaining_cost"],
        st_after["s6_needed_by_open_classes"],
        st_after["cost_needed_by_open_classes"]) == \
    (1407, 174, 6441, 509300, 4711, 373023), \
    "pre-registered prediction: new head 1407/6441/509300/4711/373023"
assert st_after["hist"] == {
    "c2=0,c4=1": 526, "c2=0,c4=2": 3013, "c2=0,c4=3": 12,
    "c2=1,c4=0": 214, "c2=1,c4=1": 54, "c2=1,c4=2": 9,
    "c2=2,c4=0": 826, "c2=2,c4=1": 5, "c2=2,c4=2": 52}, st_after["hist"]
print("AFTER cost-75e fold:", json.dumps(st_after, indent=1))

# ---------- 7. reverse-order replay ----------
s_alt = set(s_1405)
closed_alt = []
for bit in reversed(WIN_BITS):
    cov = covers(int(ROOTS[bit], 16))
    marg = cov - s_alt
    if CHILD_V in marg & manifest:
        assert not closed_alt, "the child must be closed exactly once"
        closed_alt.append(bit)
    s_alt |= marg
assert s_alt == s_after and summary_state(s_alt)[0] == st_after
assert closed_alt == [37], "in reverse order the bit-37 receipt closes the child"
print("CONTROL reverse-order replay: folding bits 37/11/10/6 reproduces the "
      "identical final set and summary; the child closes exactly once (by "
      "the bit-37 receipt there)")

# ---------- 8. per-parent rows at the new head ----------
cov4_hexes = {f"{k:032x}" for k in cov4}
parents_after = {}
lost_detail = {}
for name, h in (("second_candidate_s5", P1_75E),
                ("cost75e_parent2", P2_75E),
                ("cost70g_parent2", nsR["PARENT2"]),
                ("dual_class2_4_s5", "00000000000000801202000000080000"),
                ("class4_s5", "00000000000000003800000001800000"),
                ("cost67d_parent2", "00000000000000801002000001080000"),
                ("cost63i_second_parent", "00000000000000403800000008000000")):
    old = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
           for r in rem_1405.get(h, [])}
    new = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
           for r in rem_after.get(h, [])}
    lost = {k: v for k, v in old.items() if k not in new}
    assert set(lost) <= cov4_hexes, (name, sorted(set(lost) - cov4_hexes))
    assert new == {k: v for k, v in old.items() if k not in lost}, name
    parents_after[name] = {"s5_hex": h, "rows": len(new),
                           "edge_cost": sum(new.values())}
    lost_detail[name] = lost
assert parents_after["second_candidate_s5"]["rows"] == 5 and \
    parents_after["second_candidate_s5"]["edge_cost"] == 364, \
    "pre-registered: second candidate S5 drops 6/439 -> 5/364"
assert parents_after["cost75e_parent2"]["rows"] == 65 and \
    parents_after["cost75e_parent2"]["edge_cost"] == 5316, \
    "pre-registered: the 67-row parent2 drops 67/5473 -> 65/5316"
assert lost_detail["second_candidate_s5"] == {CHILD: 75}
assert lost_detail["cost75e_parent2"] == {CHILD: 75, MIM10_HEX: 82}
print("per-parent rows at the new head: " + "; ".join(
    f"{k} {v['rows']}/{v['edge_cost']}" for k, v in parents_after.items()))

# ---------- 9. rankings at the new head ----------


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
assert as_tuples(class2[0:1]) == [("00000000000000801202000000200000", 2, 3,
                                   209)]
assert as_tuples(class2[1:2]) == [(P1_75E, 2, 5, 364)]
assert as_tuples([next(c for c in class2
                       if c["s5_hex"] == AUDIT_BLOCKED)]) == \
    [(AUDIT_BLOCKED, 3, 10, 698)]
assert as_tuples(class4[0:2]) == [("00000000020000003800000080000000", 4, 18,
                                  1460),
                                 ("00000000000000003800002000800000", 4, 60,
                                  4216)]

sha_recon, blen_recon = git_blob_sha(
    OUT / "class-frontier-reconciled-canonical1400-cost70g-"
    "recompute-20261116.json")

result = {
    "schema": "n11-class-frontier-cost75e-receipts-20261116-v1",
    "date": "2026-11-16",
    "baseline_record": {
        "reconciled_head_1405": "class-frontier-reconciled-canonical1400-"
                                "cost70g-recompute-20261116.json: head "
                                "1405/6443/509457/4713/373180 (commit "
                                f"ca0e8c42, git blob sha {sha_recon}, "
                                f"{blen_recon} bytes)",
        "rebase_facts": "class2-lane-rebase-facts-75e-76c-on-"
                        "canonical1405-20261116.json (git blob sha "
                        f"{REBASE_FACTS_BLOB}, commit d2c82ee2): the "
                        "cost-75e child genuinely remaining at 1405 with "
                        "exactly two open parents",
        "claim": "class2-lane-cost75e-inflight-20261116.json (commit "
                 "bc893758, superseded 1400 baseline): sweep completed "
                 "locally at the outage; raw batches + determinism rerun + "
                 "v15 crosscheck republished node-exact (commit 725f4b65), "
                 "the four WIN7-D10 certificates completed and published "
                 "(bit 37 was unfinished at the outage; bit 6 published as "
                 "part1of2/part2of2 with a receipt, commits dca46d09 / "
                 "5cf7f657 / a27d240d / beb6c605 / 0fd2b1f9), certificates "
                 "manifest blob "
                 f"{CERTS_MANIFEST_BLOB}",
    },
    "method": "runpy reproduction of the published reconciliation script "
              "(internally reproducing the cost-70g chain and the canonical "
              "1400 reconstruction byte-identically, re-asserting the three "
              "reconciliation output blobs and the rebase-facts blob), "
              "re-derivation of the sweep from the 10 blob-pinned raw batch "
              "JSONLs (75 candidates, WIN7-D10 bits 6/10/11/37, 71 "
              "REFUTED-D10, 0 capped, 108,292,517 nodes, determinism rerun "
              "batch5 node-exact, v15 crosscheck agreement), re-assertion of "
              "all four published certificates against the certificates "
              "manifest blob (root = child | 1<<bit, D4 canonical hex, md5 "
              "byte pins - bit 6 via the two published parts with per-part "
              "git blob shas and the receipt -, sorted-unique rows, BigInt "
              "union 0/0 and Bareiss sub-root verification records), root "
              "disjointness of the 4 roots against all 713 folded roots "
              "raw-hex and D4-canonically, the child asserted genuinely "
              "remaining at 1405 (both open parents hold the child row at "
              "edge cost 75, demand c1=0,c2=2,c4=0), then the 4 receipts "
              "folded on 1405 in publication order with pre-registered "
              "per-bit in-manifest marginals, the child orbit closed exactly "
              "once by the bit-6 receipt, a set-equality control and a "
              "reverse-order replay reproducing the identical final set and "
              "summary",
    "controls": {
        "reconciled_head_1405_reproduced": True,
        "reconciliation_blobs_byte_identical": True,
        "rebase_facts_blob_byte_identical": True,
        "sweep_rederived_from_raw_batches_blob_pinned": True,
        "determinism_rerun_batch5_node_exact": True,
        "v15_crosscheck_agrees": True,
        "certificates_manifest_blob_pinned": True,
        "certificates_md5_rows_bigint_bareiss_reasserted": True,
        "bit6_parts_receipt_blob_shas_verified": True,
        "root_disjointness_4_vs_713": True,
        "child_genuinely_remaining_at_1405": True,
        "child_orbit_closure": "closed by the bit-6 receipt, exactly once",
        "set_equality_after": "s_after == s_1405 | cov(4 cost-75e roots)",
        "reverse_order_replay_identical": True,
        "pre_registered_prediction_holds": "1407/6441/509300/4711/373023",
    },
    "cost75e_addition_on_reconciled1405": addition,
    "totals": {
        "receipts": 4,
        "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "zero_marginal_in_manifest": ["bit11", "bit37"],
        "child_closed_by_bit": child_closed_by,
        "second_in_manifest_marginal": {
            "hex": MIM10_HEX, "closed_by_bit": 10,
            "was_row_of": {"cost75e_parent2": 82, "cost70g_parent2": 82},
        },
        "certificate_rows": 203163,
        "certificate_bytes": 7352075,
        "certificate_sub_roots": 234,
        "certificate_extraction_nodes": 62175955,
        "sweep_nodes": 108292517,
    },
    "frontier_after_cost75e": {
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
                                       if c["s5_hex"] != AUDIT_BLOCKED), None),
        "next_class2": class2[1:4],
        "best_class4": class4[0] if class4 else None,
        "next_class4": class4[1:4],
    },
    "parents_after": parents_after,
    "lost_rows_per_parent": lost_detail,
    "coordination": {
        "cost75e_claim_retires": "class2-lane-cost75e-inflight-20261116.json "
                                 "is completed by this fold; the claim file "
                                 "records the fold and the re-based head",
        "cost76c_inflight_claim": "the cost-76c claim (child "
                                  "00000000010000809002000001000000) "
                                  "references the reconciled head 1405 and "
                                  "must re-base onto this 1407 head before "
                                  "folding",
        "cost76d_cost77e_parallel_claims": "the parallel cost-76d / cost-77e "
                                           "certificate lanes pin the 1405 "
                                           "head; if their folds land on "
                                           "1405, the resulting head must be "
                                           "reconciled with this 1407 head "
                                           "(root disjointness against these "
                                           "4 roots to be asserted by that "
                                           "reconciliation)",
        "second_candidate_worklist": "the second coverable class-2 candidate "
                                     "S5 drops to 5 rows/364; remaining rows "
                                     "at edges 76/76/77 plus the STERILE 64 "
                                     "and 71 rows; rows 75 (this fold) and "
                                     "the 76c child row are closed",
    },
    "interpretation_guard": "bookkeeping over published receipts; solved counts "
                            "measure manifest coverage, not the "
                            "game-theoretic value of any position; WIN7 "
                            "certificates prove a first-player win within "
                            "depth 10 from the individual 7-stone roots only; "
                            "REFUTED-D10 sweeps prove only absence of "
                            "WIN7-D10; STERILE rows are unclosable by "
                            "depth-10 WIN7 receipts, which is NOT a LOSS "
                            "proof; 11x11 empty board / two-stone root "
                            "{49,60} / S2 {59,60} / class 1 / class 2 / "
                            "class 4 remain UNKNOWN",
}
(OUT / "class-frontier-cost75e-receipts-recompute-20261116.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-cost75e-receipts-recompute-20261116.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in rem_after.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / ("class-frontier-s5-ranking-after-cost75e-receipts-"
             "20261116.csv")).open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits",
                "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / ("class-frontier-top-candidates-s6-after-cost75e-receipts-"
             "20261116.csv")).open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    coverable = [c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED]
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
print("written ranking + top-candidates CSVs (after-cost75e-receipts)")

for p in ("class-frontier-cost75e-receipts-recompute-20261116.json",
          "class-frontier-s5-ranking-after-cost75e-receipts-20261116.csv",
          "class-frontier-top-candidates-s6-after-cost75e-receipts-"
          "20261116.csv"):
    sha, blen = git_blob_sha(OUT / p)
    print(f"blob {p}: {sha} ({blen} bytes)")
