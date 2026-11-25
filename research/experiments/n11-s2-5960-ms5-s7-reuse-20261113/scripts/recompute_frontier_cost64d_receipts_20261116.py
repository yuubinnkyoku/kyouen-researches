#!/usr/bin/env python3
"""Fold the twenty-three cost-64d WIN7-D10 receipts on the cost-65j chain head
1419/174/6429/508474/4702/372388, producing the new canonical head
1435/174/6413/507337/4686/371251.

The cost-64d child 00000000000000403800000008002000 (stones [13,27,59,60,61,
70], edge cost 64, dual class-2 demand c1=0,c2=2,c4=0) is the cheapest unswept
row of the best own-closable class-2 target S5
00000000000000403800000008000000 (P, 24 rows / 1704) at head 1419, shared with
the second open class-2 parent 00000000000000003800000008002000 (42 rows /
2929).  Its 64 legal candidates are fully resolved by the published v16
sweep (commit f38be6d6): 23 WIN7-D10 (bits 0,1,2,11,16,30,32,43,53,66,69,75,
79,86,92,95,98,106,107,109,111,113,120), 41 REFUTED-D10, 0 capped,
64,291,757 candidate nodes excluding the eight 3402-node pilots; determinism
rerun batch5 node-exact in a fresh process; v15 crosscheck two-directional
(pilot 5949, anchors [2,66,87,92,113]).  All 23 WIN roots have published,
independently verifiable certificates (win23 manifest
class2-lane-cost64d-win23-certificates-20261116.json, git blob sha
244e4b618b4bed4de298f8e3179b0b569f85cf26; 861,439 rows / 69,769,470
extraction nodes / 1,193 sub-roots; BigInt union 0/0 + Bareiss all PASS;
commit 9f4684ad).

This script reproduces the cost-65j chain head 1419 (running the published
cost-65j fold script, which internally reproduces the whole reconciliation
chain, the cost-75e and cost-60c folds and the three cost-65j output blobs,
after the thirteen published reconstruct_tmp_* prerequisites), re-derives the
cost-64d sweep from the eight blob-pinned raw batch JSONLs, re-asserts the
published sweep-audit blob (whose fold_prep_marginals_at_1419 records the
per-receipt in-manifest marginals at the 1419 baseline) and the independent
third marginal-audit blob, re-asserts all twenty-three certificates
byte-for-byte (whole/parts git blob pins, join receipts, sorted-unique rows,
root mobility == legal_candidates.py, BigInt union 0/0 + Bareiss sub-root
double-verification records, manifest totals), runs the full 64-candidate
D4-orbit conflict census against the folded roots (zero overlaps), asserts
the 23 receipt roots are 23 distinct D4 orbits disjoint raw-hex and
D4-canonically from every folded root, asserts the child genuinely remaining
at 1419 (both open parents hold the child row at edge cost 64, dual class-2
demand), then folds the 23 receipts on 1419 in publication order (bits
ascending) with all per-receipt marginals pinned.

Pre-registered expectations: the child closes exactly once, by bit 0; nine
receipts are zero-marginal-in-manifest after the child closure (bits
1/11/43/53/66/69/79/98/111); total marginal 109 / marginal_in_manifest 16;
the 16 closed rows are exactly the sweep audit's union_closed_rows; the new
head is 1435/174/6413/507337/4686/371251 with the demand histogram losing
only c2=1,c4=0 (214->212) and c2=2,c4=0 (817->803) mass; the shared class-2
parent drops 42/2929 -> 31/2145, the target S5 24/1704 -> 18/1287, and the
eleven further open parents lose 1-2 rows each (30 parent-row incidences).

Interpretation guard: bookkeeping over published receipts; solved counts
measure manifest coverage, not the game-theoretic value of any position;
WIN7 certificates prove a first-player win within depth 10 from the
individual 7-stone roots only; REFUTED-D10 proves only absence of WIN7-D10
from that root and is never a LOSS proof; 11x11 empty board / two-stone
root {49,60} / S2 {59,60} / class 1 / class 2 / class 4 remain UNKNOWN.
"""
import csv
import hashlib
import json
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost64d-certificates"

CHILD = "00000000000000403800000008002000"
CHILD_V = int(CHILD, 16)
WIN_BITS = [0, 1, 2, 11, 16, 30, 32, 43, 53, 66, 69, 75, 79, 86, 92, 95,
            98, 106, 107, 109, 111, 113, 120]
ROOTS = {b: f"{CHILD_V | (1 << b):032x}" for b in WIN_BITS}
PARENT_P = "00000000000000403800000008000000"   # class-2 target S5 24/1704
PARENT_SH = "00000000000000003800000008002000"  # shared class-2 parent 42/2929
CLAIM_BLOB = "e3cf7378a08b156c5c0299c52e4ccbcd59de9236"  # v4 (fold complete)
SWEEP_AUDIT_BLOB = "8ebfb7213a0a16fb9792a075c4ead65d2d53f855"
MARGINAL_AUDIT_THIRD_BLOB = "734b7879d91a583dc7caf593204a20acdf737c91"
WIN23_MANIFEST_BLOB = "244e4b618b4bed4de298f8e3179b0b569f85cf26"
RAW_BLOBS = {
    "class2-lane-cost64d-raw-batch1-20261116.jsonl":
        "0f93456cfddb05a6fe3c1f236f84c5df245e4d4b",
    "class2-lane-cost64d-raw-batch2-20261116.jsonl":
        "c41d88f17c836a3517f6b61aba30a6abae958a1e",
    "class2-lane-cost64d-raw-batch3-20261116.jsonl":
        "d45d8cfa7b855db11b8a34e7700ba316e0914180",
    "class2-lane-cost64d-raw-batch4-20261116.jsonl":
        "bba937a0526e9ce16e096a378c72e15b9d8718f4",
    "class2-lane-cost64d-raw-batch5-20261116.jsonl":
        "12a379c4d1a36294a1daaee94a127ad0653f7314",
    "class2-lane-cost64d-raw-batch6-20261116.jsonl":
        "a0d86791e3846878022c4c33b8294f81f024593a",
    "class2-lane-cost64d-raw-batch7-20261116.jsonl":
        "6d34099b4103f84bb65941513551590319060afc",
    "class2-lane-cost64d-raw-batch8-20261116.jsonl":
        "ce86d0fb24fbbb63e39efbbc47c821965b9a4188",
}
BATCH_BITS = {
    1: [0, 1, 2, 3, 4, 5, 6, 8],
    2: [9, 10, 11, 16, 17, 21, 25, 29],
    3: [30, 32, 38, 42, 43, 44, 46, 53],
    4: [54, 66, 69, 74, 75, 76, 78, 79],
    5: [80, 83, 85, 86, 87, 88, 89, 92],
    6: [95, 96, 97, 98, 99, 100, 101, 102],
    7: [103, 105, 106, 107, 108, 109, 110, 111],
    8: [113, 114, 115, 116, 117, 118, 119, 120],
}
BATCH_BIT_NODES = {
    1: 10856729,
    2: 4759906,
    3: 9522168,
    4: 10356258,
    5: 6799604,
    6: 7633164,
    7: 7112686,
    8: 7251242,
}
SWEEP_NODES_TOTAL = 64291757            # excluding the eight pilots
PILOT_NODES = 3402
DET_BLOB = "cdee50ada96e585d186cb5401c56e7422ce8ff5a"
V15_BLOB = "ad5124538ee6b0dcc690ad34612094d0aa5613cd"
V15_ANCHORS = [2, 66, 87, 92, 113]
DET_BITS = [80, 83, 85, 86, 87, 88, 89, 92]
WIN23_TOTALS = {
    "published_certificates": 23, "rows": 861439,
    "extraction_nodes": 69769470, "sub_roots": 1193,
    "winner_states": 1220504, "loser_states": 362105,
    "terminal_count": 310638, "cert_bytes": 31086866,
}
# pinned per-receipt sequential (marginal, marginal_in_manifest) in
# publication order (bits ascending):
PINNED_MARGINAL = {0: 5, 1: 4, 2: 5, 11: 4, 16: 5, 30: 5, 32: 5, 43: 4,
                   53: 4, 66: 4, 69: 5, 75: 5, 79: 4, 86: 6, 92: 5, 95: 5,
                   98: 4, 106: 5, 107: 6, 109: 5, 111: 4, 113: 5, 120: 5}
PINNED_MIM = {0: 1, 1: 0, 2: 1, 11: 0, 16: 1, 30: 1, 32: 1, 43: 0, 53: 0,
              66: 0, 69: 0, 75: 1, 79: 0, 86: 2, 92: 1, 95: 1, 98: 0,
              106: 1, 107: 2, 109: 1, 111: 0, 113: 1, 120: 1}
PINNED_MIM_HEXES = {
    0: ["00000000000000403800000008002000"],
    2: ["00000000000000003800000008002004"],
    16: ["00000000000000003800000008012000"],
    30: ["00000000000000003800000009080000"],
    32: ["00000000000000403800000108000000"],
    75: ["00000000000000083800000008080000"],
    86: ["00000000000000c09002000000004000",
         "00000000000040003800000008080000"],
    92: ["00000000000000801212000000800000"],
    95: ["00000000000000c09002000800000000"],
    106: ["00000000000040809002000080000000"],
    107: ["00000000000000c09002000000800000",
          "00000000020000801202000080000000"],
    109: ["00000000000000c09002000000000002"],
    113: ["00000000000000801202080000800000"],
    120: ["00000000020000801202000000000400"],
}
# pinned per-parent (rows, edge_cost) before -> after for the 13 parents:
PINNED_PARENTS = {
    "00000000000000003800000008000004": ((66, 5451), (65, 5377)),
    "00000000000000003800000008002000": ((42, 2929), (31, 2145)),
    "00000000000000003800000008400000": ((43, 3197), (42, 3127)),
    "00000000000000003800000009000000": ((30, 2276), (29, 2203)),
    "00000000000000083800000008000000": ((50, 3750), (49, 3683)),
    "00000000000000403800000008000000": ((24, 1704), (18, 1287)),
    "00000000000000801202000000000200": ((65, 5316), (64, 5242)),
    "00000000000000801202000000000400": ((68, 5588), (67, 5514)),
    "00000000000000801202000000040000": ((74, 6113), (72, 5960)),
    "00000000000000801202000080000000": ((40, 3038), (38, 2901)),
    "00000000000000801202020000000000": ((49, 3360), (48, 3296)),
    "00000000000000801202080000000000": ((74, 6127), (73, 6052)),
    "00000000000000801212000000000000": ((68, 5376), (67, 5305)),
}
PINNED_AFTER = (1435, 174, 6413, 507337, 4686, 371251)
PINNED_HIST = {"c2=0,c4=1": 526, "c2=0,c4=2": 3013, "c2=0,c4=3": 12,
               "c2=1,c4=0": 212, "c2=1,c4=1": 54, "c2=1,c4=2": 9,
               "c2=2,c4=0": 803, "c2=2,c4=1": 5, "c2=2,c4=2": 52}
ZERO_MIM = [1, 11, 43, 53, 66, 69, 79, 98, 111]
UNION16 = [
    "00000000000000003800000008002004",
    "00000000000000003800000008012000",
    "00000000000000003800000009080000",
    "00000000000000083800000008080000",
    "00000000000000403800000008002000",
    "00000000000000403800000108000000",
    "00000000000000801202080000800000",
    "00000000000000801212000000800000",
    "00000000000000c09002000000000002",
    "00000000000000c09002000000004000",
    "00000000000000c09002000000800000",
    "00000000000000c09002000800000000",
    "00000000000040003800000008080000",
    "00000000000040809002000080000000",
    "00000000020000801202000000000400",
    "00000000020000801202000080000000",
]


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


_orig_write_text = Path.write_text


def _write_text_lf(self, data, encoding=None, errors=None, newline=None):
    with self.open("w", encoding=encoding or "utf-8", errors=errors,
                   newline="\n") as f:
        f.write(data)


Path.write_text = _write_text_lf

# ---------- 1. reproduce the cost-65j chain head 1419 ----------
ns65 = runpy.run_path(str(HERE / "scripts" /
                          "recompute_frontier_cost65j_receipts_"
                          "20261116.py"))
s_1419 = set(ns65["s_cur"])
st_1419 = ns65["st_after"]
rem_1419 = ns65["rem_after"]
dem_1419 = ns65["dem_after"]
covers = ns65["covers"]
manifest = ns65["manifest"]
classes = ns65["classes"]
summary_state = ns65["summary_state"]
canon = ns65["canon"]
folded_1410 = set(ns65["folded_1410"])           # 718 at head 1410
roots_65j = {int(h, 16) for h in ns65["ROOTS"].values()}  # 17 receipts
folded = folded_1410 | roots_65j
assert (st_1419["solved_s6_in_manifest"], st_1419["remaining_s5_orbits"],
        st_1419["unique_remaining_s6"], st_1419["sum_remaining_cost"],
        st_1419["s6_needed_by_open_classes"],
        st_1419["cost_needed_by_open_classes"]) == \
    (1419, 174, 6429, 508474, 4702, 372388), st_1419
assert len(folded_1410) == 718 and len(roots_65j) == 17
assert len(folded) == 734, len(folded)
print("CONTROL cost-65j chain head 1419/174/6429/508474/4702/372388 "
      "reproduced (the published cost-65j fold script re-asserts the whole "
      "chain, the cost-75e and cost-60c folds and its three output blobs); "
      "folded roots at 1419: 718 (head 1410) + the 17 cost-65j receipts = "
      "735 receipt roots, 734 distinct (the 65f bit-25 root is "
      "byte-identical to the already-folded cost-72b root)")

# ---------- 2. re-derive the sweep from the raw batches ----------
sha, blen = git_blob_sha(OUT / "class2-lane-cost64d-inflight-20261116.json")
assert sha == CLAIM_BLOB and blen == 11621, "claim v4 blob"
claim = json.loads((OUT / "class2-lane-cost64d-inflight-20261116.json")
                   .read_text())
assert claim["schema"] == "n11-class2-lane-cost64d-completed-20261116-v4"
assert claim["s6_child"] == CHILD and claim["candidate_count"] == 64
cand_bits = claim["legal_candidates"]
bit_recs = {}
pilots = []
for i in range(1, 9):
    name = f"class2-lane-cost64d-raw-batch{i}-20261116.jsonl"
    p = OUT / name
    sha, blen = git_blob_sha(p)
    assert sha == RAW_BLOBS[name], name
    lines = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    for rec in lines:
        if "control" in rec:
            pilots.append(rec["nodes"])
            assert rec["loss"] is False and rec["capped"] is False, rec
        else:
            assert rec["bit"] not in bit_recs, "each bit exactly once"
            bit_recs[rec["bit"]] = rec
    assert sorted(r["bit"] for r in lines if "bit" in r) == BATCH_BITS[i], i
    assert sum(r["nodes"] for r in lines if "bit" in r) == \
        BATCH_BIT_NODES[i], i
assert pilots == [PILOT_NODES] * 8, pilots
assert sorted(bit_recs) == cand_bits
win_bits = sorted(b for b, r in bit_recs.items() if r["loss"] is True)
refuted = sorted(b for b, r in bit_recs.items()
                 if r["loss"] is False and r["capped"] is False)
capped = sorted(b for b, r in bit_recs.items() if r["capped"] is True)
assert win_bits == WIN_BITS, win_bits
assert refuted == claim["results"]["refuted_d10_bits"]
assert len(refuted) == 41 and capped == []
assert sum(r["nodes"] for r in bit_recs.values()) == SWEEP_NODES_TOTAL
assert all(r["terminalStoneRange"] == [13, 17] for r in bit_recs.values())
assert all(r["andclose"] is True for r in bit_recs.values())
# determinism rerun batch5 node-exact
sha, _ = git_blob_sha(OUT / "class2-lane-cost64d-determinism-rerun-"
                      "batch5-20261116.jsonl")
assert sha == DET_BLOB, "determinism blob"
det = [json.loads(x) for x in
       (OUT / "class2-lane-cost64d-determinism-rerun-batch5-20261116.jsonl")
       .read_text().splitlines() if x.strip()]
det_bits = {r["bit"]: r for r in det if "bit" in r}
assert sorted(det_bits) == DET_BITS
assert next(r for r in det if "control" in r)["nodes"] == PILOT_NODES
for b, r in det_bits.items():
    o = bit_recs[b]
    assert (r["loss"], r["nodes"], r["capped"],
            r["terminalStoneRange"]) == \
        (o["loss"], o["nodes"], o["capped"], o["terminalStoneRange"]), b
# v15 crosscheck two-directional
sha, _ = git_blob_sha(OUT / "class2-lane-cost64d-v15-crosscheck-20261116.jsonl")
assert sha == V15_BLOB, "v15 crosscheck blob"
v15 = [json.loads(x) for x in
       (OUT / "class2-lane-cost64d-v15-crosscheck-20261116.jsonl")
       .read_text().splitlines() if x.strip()]
v15_bits = {r["bit"]: r for r in v15 if "bit" in r}
assert sorted(v15_bits) == V15_ANCHORS
assert next(r for r in v15 if "control" in r)["nodes"] == 5949
assert all(v15_bits[b]["loss"] is True
           for b in V15_ANCHORS if b in win_bits)
assert all(v15_bits[b]["loss"] is False
           for b in V15_ANCHORS if b not in win_bits)
print(f"CONTROL cost-64d sweep re-derived from the 8 blob-pinned raw "
      f"batches: 64 candidates, 23 WIN7-D10 bits {win_bits}, 41 "
      f"REFUTED-D10, 0 capped, {SWEEP_NODES_TOTAL} nodes + 8 pilots x "
      f"{PILOT_NODES}; terminal [13,17] and andclose all; determinism "
      f"rerun batch5 node-exact; v15 crosscheck agrees two-directionally "
      f"(pilot 5949, anchors {V15_ANCHORS})")

# ---------- 3. re-assert the published sweep audit + fold-prep marginals --
sha, blen = git_blob_sha(OUT / "class2-lane-cost64d-raw-sweep-audit-"
                         "20261116.json")
assert sha == SWEEP_AUDIT_BLOB and blen == 11369, "sweep audit blob"
audit = json.loads((OUT / "class2-lane-cost64d-raw-sweep-audit-20261116.json")
                   .read_text())
assert audit["sweep_aggregate"]["win7_d10_bits"] == win_bits
assert audit["sweep_aggregate"]["refuted_d10_bits"] == refuted
assert audit["sweep_aggregate"]["capped_bits"] == []
fp = audit["fold_prep_marginals_at_1419"]
assert fp["projected_head_after_fold"] == 1435
assert fp["union_closed_rows_count"] == 16
assert sorted(fp["union_closed_rows"]) == UNION16
mim_base = {}
for r in fp["receipts"]:
    mim_base[r["bit"]] = [int(h, 16)
                          for h in r["marginal_in_manifest_1419"]]
assert sorted(mim_base) == WIN_BITS
for b in WIN_BITS:
    cov = covers(CHILD_V | (1 << b))
    marg_m = (cov - s_1419) & manifest
    assert sorted(marg_m) == sorted(mim_base[b]), b
    assert CHILD_V in cov, b
union_base = set()
for b in WIN_BITS:
    union_base |= set(mim_base[b])
assert len(union_base) == 16 and CHILD_V in union_base
# independent third marginal audit (blob-pinned)
sha, blen = git_blob_sha(OUT / "class2-lane-cost64d-marginal-audit-third-"
                         "20261116.json")
assert sha == MARGINAL_AUDIT_THIRD_BLOB and blen == 7543, \
    "third marginal audit blob"
third = json.loads((OUT / "class2-lane-cost64d-marginal-audit-third-"
                    "20261116.json").read_text())
assert third["mismatches"] == []
assert third["per_root_marginals_match_published_audit"] is True
assert third["new_marginals"]["unique_rows"] == 16
assert third["new_marginals"]["parent_row_incidences"] == 30
assert third["new_marginals"]["projected_head"] == 1435
assert sorted(e["s6_canonical_hex"] for e in third["newly_closed_rows"]) \
    == UNION16
third_rows = {e["bit"]: [int(h, 16) for h in e["marginal_rows"]]
              for e in third["per_root"]}
for b in WIN_BITS:
    assert sorted(third_rows[b]) == sorted(mim_base[b]), b
print("CONTROL published fold-prep re-asserted: the sweep audit's "
      "fold_prep_marginals_at_1419 and the independent third marginal "
      "audit agree exactly with the re-derived per-receipt in-manifest "
      "marginals on the 1419 baseline; union 16 rows; projected head 1435")

# ---------- 4. re-assert all twenty-three published certificates ----------
sys.path.insert(0, str(HERE / "scripts"))
from legal_candidates import legal_candidates  # noqa: E402

sha, blen = git_blob_sha(OUT / "class2-lane-cost64d-win23-certificates-"
                         "20261116.json")
assert sha == WIN23_MANIFEST_BLOB and blen == 42974, "win23 manifest blob"
wman = json.loads((OUT / "class2-lane-cost64d-win23-certificates-"
                   "20261116.json").read_text())
assert wman["target"]["s6_child_hex"] == CHILD
certs = {}
for e in wman["certificates"]:
    bit = e["bit"]
    assert bit in WIN_BITS
    root_v = int(e["root_hex"], 16)
    assert root_v == CHILD_V | (1 << bit), bit
    assert e["verdict"] == "WIN7" and e["child_hex"] == CHILD
    assert e["d4_canonical_hex"] == f"{canon(root_v):032x}", bit
    assert e["root_mobility_matches_legal_candidates_py"] is True, bit
    stones, moves = legal_candidates(e["root_hex"])
    assert len(moves) == e["sub_roots"], bit
    pc = e["published_cert"]
    if pc["path"] is None:
        p1 = CERTS / f"bit{bit}-root-{ROOTS[bit]}.cert.part1of2"
        p2 = CERTS / f"bit{bit}-root-{ROOTS[bit]}.cert.part2of2"
        data = p1.read_bytes() + p2.read_bytes()
        assert len(data) == pc["whole_bytes"], bit
        for part, ppath in zip(pc["parts"], (p1, p2)):
            assert part["path"].endswith(ppath.name), bit
            assert len(ppath.read_bytes()) == part["bytes"], bit
            psha, _ = git_blob_sha(ppath)
            assert psha == part["git_blob_sha"], ppath.name
        rcpt = json.loads((CERTS / f"bit{bit}-root-{ROOTS[bit]}"
                           ".cert-receipt.json").read_text())
        assert rcpt["whole_md5"] == pc["whole_md5"] and \
            rcpt["whole_sha256"] == pc["whole_sha256"] and \
            rcpt["whole_bytes"] == pc["whole_bytes"] and \
            rcpt["joined_equals_whole"] is True, bit
        cert_md5 = pc["whole_md5"]
    else:
        data = (CERTS / f"bit{bit}-root-{ROOTS[bit]}.cert").read_bytes()
        assert pc["path"].endswith(f"bit{bit}-root-{ROOTS[bit]}.cert"), bit
        assert len(data) == pc["bytes"], bit
        psha, _ = git_blob_sha(CERTS / f"bit{bit}-root-{ROOTS[bit]}.cert")
        assert psha == pc["git_blob_sha"], bit
        cert_md5 = pc["md5"]
    assert hashlib.md5(data).hexdigest() == cert_md5, bit
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
    bv = e["bigint_verify"]
    assert bv["union_missing"] == 0 and bv["union_extra"] == 0, bit
    assert bv["subroots_passed"] == e["sub_roots"], bit
    assert bv["winner_states"] == e["winner_states"] and \
        bv["loser_states"] == e["loser_states"] and \
        bv["terminal_count"] == e["terminal_count"], bit
    br = e["bareiss_verify"]
    assert br["subroots_verified"] == e["sub_roots"] and \
        br["all_subroots_pass"] is True, bit
    assert e["fbt_drops"] == 0 and e["fatal"] is None, bit
    assert e["terminal_range"] == [13, 17], bit
    certs[bit] = e
assert wman["totals"] == WIN23_TOTALS, wman["totals"]
assert len(certs) == 23
print("CONTROL all 23 win23 certificates re-asserted byte-for-byte: "
      "manifest blob pinned, root = child | 1<<bit, D4 canonical, whole / "
      "part1of2+part2of2 git blob pins with join receipts, md5 byte pins, "
      "sorted-unique rows, root mobility == legal_candidates.py, BigInt "
      "union 0/0 and Bareiss sub-roots all PASS; totals 861,439 rows / "
      "69,769,470 extraction nodes / 1,193 sub-roots")

# ---------- 5. conflict census vs the folded roots at 1419 ----------
folded_d4 = {canon(r) for r in folded}
census = []
for b in cand_bits:
    if canon(CHILD_V | (1 << b)) in folded_d4:
        census.append((b, "WIN7" if bit_recs[b]["loss"] is True
                       else "REFUTED"))
assert census == [], census
raw_hits = sorted(b for b in WIN_BITS
                  if (CHILD_V | (1 << b)) in folded)
d4_hits = sorted(b for b in WIN_BITS
                 if canon(CHILD_V | (1 << b)) in folded_d4)
assert raw_hits == [] and d4_hits == []
assert len({canon(CHILD_V | (1 << b)) for b in WIN_BITS}) == 23
print("CONTROL conflict census: all 64 candidate D4 orbits are disjoint "
      "from the 734 distinct folded roots at 1419 - zero overlaps, zero "
      "WIN/LOSS conflicts; the 23 receipt roots are 23 distinct D4 "
      "orbits, disjoint raw-hex and D4-canonically from every folded "
      "root")

# ---------- 6. the child genuinely remains open at 1419 ----------
assert CHILD_V in manifest and CHILD_V not in s_1419
for h, exp_rows, exp_cost in ((PARENT_P, 24, 1704),
                              (PARENT_SH, 42, 2929)):
    rows = rem_1419.get(h, [])
    assert classes.get(h, 0) == 2, h
    assert len(rows) == exp_rows and \
        sum(int(r["s6_s7_edge_cost"]) for r in rows) == exp_cost, h
    ch = [r for r in rows if int(r["s6_hex"], 16) == CHILD_V]
    assert len(ch) == 1 and int(ch[0]["s6_s7_edge_cost"]) == 64, h
d = dem_1419.get(CHILD)
assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 0), d
print("CONTROL the child genuinely remains at head 1419: both open class-2 "
      "parents hold the child row (P 24/1704, shared 42/2929) at edge cost "
      "64, dual demand c1=0,c2=2,c4=0")

# ---------- 7. fold the 23 receipts on 1419 in publication order ---------
s_cur = set(s_1419)
addition = []
zero_mim = []
child_closed_by = None
for bit in WIN_BITS:
    root_v = CHILD_V | (1 << bit)
    cov = covers(root_v)
    assert CHILD_V in cov, "every receipt covers the child via its stone"
    marg = cov - s_cur
    marg_m = marg & manifest
    if CHILD_V in marg_m:
        assert child_closed_by is None, "the child must close exactly once"
        child_closed_by = bit
    rec = {
        "bit": bit,
        "root_hex": ROOTS[bit],
        "d4_canonical_hex": f"{canon(root_v):032x}",
        "source": "cost-64d raw batches 1-8 (v16, commit f38be6d6)",
        "certified": True,
        "sweep_nodes": bit_recs[bit]["nodes"],
        "covers": len(cov),
        "marginal": len(marg),
        "marginal_in_manifest": len(marg_m),
        "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
        "marginal_non_manifest_hexes":
            sorted(f"{k:032x}" for k in marg - marg_m),
        "rows": certs[bit]["rows"],
        "md5": (certs[bit]["published_cert"]["md5"]
                if certs[bit]["published_cert"]["path"] is not None
                else certs[bit]["published_cert"]["whole_md5"]),
        "sub_roots_pass": certs[bit]["sub_roots"],
        "extraction_nodes": certs[bit]["extraction_nodes"],
        "terminal_count": certs[bit]["terminal_count"],
    }
    addition.append(rec)
    if not marg_m:
        zero_mim.append(bit)
    assert (len(marg), len(marg_m)) == (PINNED_MARGINAL[bit],
                                        PINNED_MIM[bit]), bit
    if marg_m:
        assert sorted(f"{k:032x}" for k in marg_m) == \
            PINNED_MIM_HEXES[bit], bit
    s_cur |= marg
assert child_closed_by == 0, child_closed_by
assert zero_mim == ZERO_MIM, zero_mim
cov_all = set()
for bit in WIN_BITS:
    cov_all |= covers(CHILD_V | (1 << bit))
assert s_cur == s_1419 | cov_all, \
    "set-equality: s_after == s_1419 UNION covers(23 roots)"
total_marg = sum(a["marginal"] for a in addition)
total_mim = sum(a["marginal_in_manifest"] for a in addition)
assert (total_marg, total_mim) == (109, 16)
st_after, rem_after, uniq_after, dem_after = summary_state(s_cur)
assert (st_after["solved_s6_in_manifest"], st_after["remaining_s5_orbits"],
        st_after["unique_remaining_s6"], st_after["sum_remaining_cost"],
        st_after["s6_needed_by_open_classes"],
        st_after["cost_needed_by_open_classes"]) == PINNED_AFTER, st_after
assert st_after["solved_s6_in_manifest"] == 1419 + total_mim
assert st_after["hist"] == PINNED_HIST, st_after["hist"]
print("AFTER cost-64d fold:", json.dumps(st_after, indent=1))
print(f"total marginal={total_marg} marginal_in_manifest={total_mim}; "
      f"zero-mim receipts: {zero_mim}; child closed by bit: "
      f"{child_closed_by}")

# ---------- 8. per-parent rows at the new head ----------
parents_after = {}
lost_detail = {}
cov_hexes = {f"{k:032x}" for k in cov_all}
for h in sorted(PINNED_PARENTS):
    old_exp, new_exp = PINNED_PARENTS[h]
    old = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1419[h]}
    new = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_after[h]}
    lost = {k: v for k, v in old.items() if k not in new}
    assert set(lost) <= cov_hexes, (h, sorted(set(lost) - cov_hexes))
    assert new == {k: v for k, v in old.items() if k not in lost}, h
    assert (len(old), sum(old.values())) == old_exp, h
    assert (len(new), sum(new.values())) == new_exp, h
    parents_after[h] = {"s5_hex": h, "rows": len(new),
                        "edge_cost": sum(new.values()),
                        "rows_before": len(old),
                        "edge_cost_before": sum(old.values())}
    lost_detail[h] = lost
assert sum(len(v) for v in lost_detail.values()) == 30, \
    "30 parent-row incidences"
closed_hexes = {f"{k:032x}" for k in union_base}
for h, lost in lost_detail.items():
    assert set(lost) <= closed_hexes, h
print("per-parent rows at the new head (touched parents): " + "; ".join(
    f"{k} {v['rows_before']}/{v['edge_cost_before']} -> "
    f"{v['rows']}/{v['edge_cost']}" for k, v in parents_after.items()))

# ---------- 9. the 16 rows actually closed; demand invariants ----------
s_hex = {f"{k:032x}" for k in s_cur}
for row_hex in UNION16:
    assert row_hex in s_hex, (row_hex, "must be closed by the fold")
    dd = dem_1419.get(row_hex)
    assert dd["c2"] > 0 and dd["c4"] == 0 and dd["c1"] == 0, (row_hex, dd)
assert CHILD in s_hex
assert int(f"{CHILD_V:032x}", 16) == CHILD_V

# ---------- 10. rankings at the new head ----------


def best(rem, bit_):
    return sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"])
                                        for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit_),
        key=lambda r: (r["remaining_s6_orbits"], r["remaining_s7_edge_cost"],
                       r["s5_hex"]))


class2 = best(rem_after, 2)
class4 = best(rem_after, 4)
class1 = best(rem_after, 1)
AUDIT_BLOCKED = "00000000000000809082000000000000"
coverable = [c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED]
print("best class-4:", class4[0] if class4 else None)
print("best class-1:", class1[0] if class1 else None)
print("best coverable class-2:", coverable[0] if coverable else None,
      "second:", coverable[1] if len(coverable) > 1 else None)
print("audit-blocked:", next((c for c in class2
                             if c["s5_hex"] == AUDIT_BLOCKED), None))

result = {
    "schema": "n11-class-frontier-cost64d-receipts-20261116-v1",
    "date": "2026-11-16",
    "baseline_record": {
        "cost65j_head_1419": "1419/174/6429/508474/4702/372388 "
                            "(reproduced byte-identically by runpy of the "
                            "published cost-65j fold script)",
        "claim": "class2-lane-cost64d-inflight-20261116.json (v4, git blob "
                 f"sha {CLAIM_BLOB}; supersedes the v3 win23-certificate "
                 "claim, all v1/v2/v3 fields preserved)",
        "sweep": "8 raw batch JSONLs (v16), all blob-pinned; 64 "
                 "candidates, 23 WIN7-D10, 41 REFUTED-D10, 0 capped, "
                 f"{SWEEP_NODES_TOTAL} nodes + 8 pilots x {PILOT_NODES}; "
                 "determinism rerun batch5 node-exact; v15 crosscheck "
                 "two-directional",
        "sweep_audit": "class2-lane-cost64d-raw-sweep-audit-20261116.json "
                       f"(git blob sha {SWEEP_AUDIT_BLOB})",
        "marginal_audit_third":
            "class2-lane-cost64d-marginal-audit-third-20261116.json "
            f"(git blob sha {MARGINAL_AUDIT_THIRD_BLOB})",
    },
    "method": "runpy reproduction of the published cost-65j fold script "
              "(whole-chain head 1419), re-derivation of the cost-64d "
              "sweep from the 8 blob-pinned raw batches, re-assertion of "
              "the sweep audit and the independent third marginal audit "
              "(per-receipt in-manifest marginals on the 1419 baseline), "
              "re-assertion of all 23 win23 certificates byte-for-byte "
              "(whole/parts blob pins, join receipts, sorted-unique rows, "
              "root mobility == legal_candidates.py, BigInt union 0/0 + "
              "Bareiss records), 64-candidate-orbit conflict census vs the "
              "folded roots (zero overlaps), the child-remaining fact "
              "asserted on both open parents, then the 23 receipts folded "
              "in publication order with per-receipt marginals pinned and "
              "a set-equality control",
    "cost64d_additions_on_cost65j_1419": addition,
    "totals": {
        "receipts": 23,
        "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "child_closed_by_bit": child_closed_by,
        "zero_mim_receipts": zero_mim,
        "conflict_census_overlaps": census,
        "folded_roots_at_1419": {"receipt_roots": 735,
                                 "distinct_roots": 734},
        "rows_closed_hexes": UNION16,
        "sweep_nodes_excluding_pilots": SWEEP_NODES_TOTAL,
    },
    "frontier_after_cost64d": {
        "solved_s6_in_manifest": st_after["solved_s6_in_manifest"],
        "remaining_s5_orbits": st_after["remaining_s5_orbits"],
        "unique_remaining_s6": st_after["unique_remaining_s6"],
        "sum_remaining_cost": st_after["sum_remaining_cost"],
        "s6_needed_by_open_classes": st_after["s6_needed_by_open_classes"],
        "cost_needed_by_open_classes":
            st_after["cost_needed_by_open_classes"],
        "demand_histogram_open_only": st_after["hist"],
        "best_class2": class2[0] if class2 else None,
        "best_class4": class4[0] if class4 else None,
        "best_coverable_class2": coverable[0] if coverable else None,
        "second_coverable_class2": coverable[1] if len(coverable) > 1
                                    else None,
    },
    "parents_after": parents_after,
    "lost_rows_per_parent": lost_detail,
    "interpretation_guard": "bookkeeping over published receipts; solved "
                            "counts measure manifest coverage, not the "
                            "game-theoretic value of any position; WIN7 "
                            "certificates prove a first-player win within "
                            "depth 10 from the individual 7-stone roots "
                            "only; REFUTED-D10 proves only absence of "
                            "WIN7-D10 from that root and is never a LOSS "
                            "proof; 11x11 empty board / two-stone root "
                            "{49,60} / S2 {59,60} / class 1 / class 2 / "
                            "class 4 remain UNKNOWN",
}
(OUT / "class-frontier-cost64d-receipts-recompute-20261116.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-cost64d-receipts-recompute-20261116.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"])
                                    for r in rows)}
     for k, rows in rem_after.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                  r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / ("class-frontier-s5-ranking-after-cost64d-receipts-"
             "20261116.csv")).open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits",
                "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / ("class-frontier-top-candidates-s6-after-cost64d-receipts-"
             "20261116.csv")).open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    for label, cand in (("best class-4 blocker-candidate S5",
                         class4[0] if class4 else None),
                        ("best class-1 blocker-candidate S5",
                         class1[0] if class1 else None),
                        ("best class-2 blocker-candidate S5 "
                         "(receipt-unclosable, audit-blocked)",
                         next((c for c in class2
                               if c["s5_hex"] == AUDIT_BLOCKED), None)),
                        ("best coverable class-2 blocker-candidate S5",
                         coverable[0] if coverable else None),
                        ("second coverable class-2 candidate S5",
                         coverable[1] if len(coverable) > 1 else None)):
        if cand is None:
            continue
        rows = rem_after.get(cand["s5_hex"], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} "
                    f"classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} "
                    f"cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
        for row in sorted(rows, key=lambda r: int(r["s6_s7_edge_cost"])):
            dd = dem_after.get(row["s6_hex"],
                               {"c1": -1, "c2": -1, "c4": -1})
            w.writerow((cand["s5_hex"], row["s6_hex"],
                        row["s6_s7_edge_cost"],
                        f"c1={dd['c1']},c2={dd['c2']},c4={dd['c4']}"))
print("written ranking + top-candidates CSVs (after-cost64d-receipts)")

for p in ("class-frontier-cost64d-receipts-recompute-20261116.json",
          "class-frontier-s5-ranking-after-cost64d-receipts-20261116.csv",
          "class-frontier-top-candidates-s6-after-cost64d-receipts-"
          "20261116.csv",
          "class2-lane-cost64d-inflight-20261116.json",
          "class2-lane-cost64d-win23-certificates-20261116.json"):
    sha, blen = git_blob_sha(OUT / p)
    print(f"blob {p}: {sha} ({blen} bytes)")
