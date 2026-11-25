#!/usr/bin/env python3
"""Fold the seventeen cost-65j WIN7-D10 receipts on the cost-60c chain head
1410/174/6438/509109/4711/373023 (corrected premise, v2).

The cost-65j child 00000000000000809102000080000000 (edge cost 65, dual
class-2 demand c1=0,c2=2,c4=0 at the after-cost-75c frontier that
motivated the sweep) is the cheapest child of the third class-2 target S5
00000000000000809102000000000000.  Its 65 legal candidates are fully
resolved by the published sweeps: 17 WIN7-D10 receipt roots (bits
4,15,18,20,21,23,25,28,66,79,91,101,109 from the cost-65f raw batches 1-7,
v15 engine, 2026-11-14, commits per the claim record; bits 112,116,118,119
from the cost-65j raw batch 8, v16 engine, commit 738e33e3), 48 REFUTED-D10
(43 from cost-65f batches, bit 113 by the published canonical identity
transfer of the K0863 theorem-applicability scan, commits 2d090b49 /
50c0f1c1, X1 re-verified by the second independent verification 7c99621f;
bits 111,114,117,120 from cost-65j batches 8-9), 0 capped.

DISCOVERY RECORDED BY THIS FOLD (v1 premise correction): the motivating
child is ALREADY SOLVED at head 1410.  It was closed exactly once, by the
cost-63a bit-97 WIN receipt root 00000002000000809102000800000000 (the
D4 orbit of the 65f bit-79 candidate) inside the warm-multiband2 /
unified-merge fold of 2026-11-15, whose marginal_in_manifest was exactly
one row = the child (blob-pinned published record re-asserted below).
Three further already-folded roots also cover the child: the cost-72b
receipts 00000000000000809102000082000000 (byte-identical to the 65f
bit-25 root) and 00000002000000809102000002000000 (orbit of 65f bit 91),
and the cost-69i receipt 00000002000000809102000000002000 (orbit of 65f
bit 101).  The 65f/65j sweep independently re-derived all four orbits as
WIN7-D10 — zero WIN/LOSS conflicts (census below).  The third class-2
target S5 itself has zero remaining rows at 1410.  The value of this fold
is therefore NOT closing the child (already closed) but closing the nine
still-remaining manifest rows covered by the 17 receipts, including the two
cost-64 rows 00000000000000003800000008002002 / 00000000000000003800000008
003000, with four fresh independently verifiable WIN7 certificates.

This script reproduces the cost-60c chain head 1410 (running the published
cost-60c fold script, which internally reproduces the whole reconciliation
chain and the cost-75e fold byte-identically and re-asserts the three
cost-60c output blobs), re-derives the 65f+65j sweep totals from the nine
blob-pinned raw batch JSONLs (65 candidates, 17 WIN7-D10, 48 REFUTED-D10
incl. the bit-113 transfer, 0 capped, 402,652,063 nodes incl. pilot
controls), re-asserts the published pre-fold cover map (blob-pinned: the 17
receipts' 7 one-stone-deletion canonical forms cover exactly 34 manifest
rows), re-asserts the four new cost-65j WIN7-D10 certificates published
with this fold (bits 112/116/118/119, md5 + git blob byte pins,
sorted-unique rows, BigInt union 0/0 and Bareiss sub-root double
verification records; the thirteen cost-65f receipts have no published
certificates and are folded on their blob-pinned published v15 raw sweep
records, marked certified:false), runs the full 65-candidate-orbit conflict
census against the 718 folded roots (exactly four orbit overlaps, all
WIN/WIN), asserts the child-already-closed fact against the blob-pinned
warm-multiband2 record, asserts the exact nine remaining covered rows and
the two cost-64 rows among them, then folds the 17 receipts on 1410 in
publication order (65f bits ascending, then 65j bits ascending) with all
per-receipt marginals pinned.

Interpretation guard: bookkeeping over published receipts; solved counts
measure manifest coverage, not the game-theoretic value of any position;
WIN7 certificates prove a first-player win within depth 10 from the
individual 7-stone roots only; REFUTED-D10 proves only absence of WIN7-D10
from that root; 11x11 empty board / two-stone root {49,60} / S2 {59,60} /
class 1 / class 2 / class 4 remain UNKNOWN.
"""
import csv
import hashlib
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost65j-certificates"

CHILD = "00000000000000809102000080000000"
CHILD_V = int(CHILD, 16)
WIN_BITS_65F = [4, 15, 18, 20, 21, 23, 25, 28, 66, 79, 91, 101, 109]
WIN_BITS_65J = [112, 116, 118, 119]
WIN_BITS = WIN_BITS_65F + WIN_BITS_65J
TRANSFERRED_BIT = 113
ROOTS = {b: f"{CHILD_V | (1 << b):032x}" for b in WIN_BITS}
PARENT_S5 = "00000000000000809102000000000000"   # third class-2 target S5
ROW64_BIT21 = "00000000000000003800000008002002"  # cost-64 row, 65f bit 21
ROW64_BIT20 = "00000000000000003800000008003000"  # cost-64 row, 65f bit 20
COVERMAP_BLOB = "d6d20e52c6b5af8f268222bfc9c87d6ac77c655d"
CLAIM_BLOB = "7a4c900710e3ddb34fb9e272e8e673815e13a4f3"  # v5
REUSE_AUDIT_BLOB = "1999d82b0f78dd9f69b6c81fbbe6bf3937d31a44"
MERGE2_BLOB = "0830cfc3746baa6ad5b542579dc9d657b61ac72a"  # warm-multiband2
MERGE_UNIFIED_BLOB = "a0789eedd5b81d1c9ea96220acfb487f38e70e08"
# the four already-folded cross-cover roots of the child (orbit -> root):
CLOSERS = {  # 65f/65j candidate bit -> (folded root hex, closing provenance)
    25: ("00000000000000809102000082000000",
         "cost-72b receipts (byte-identical to the 65f bit-25 root)"),
    79: ("00000002000000809102000800000000",
         "cost-63a bit-97 receipt, warm-multiband2/unified-merge fold "
         "2026-11-15 (this fold closed the child, marginal_in_manifest = "
         "exactly the child row)"),
    91: ("00000002000000809102000002000000",
         "cost-72b receipts"),
    101: ("00000002000000809102000000002000",
          "cost-69i receipts"),
}
# the nine still-remaining covered rows at 1410 (receipt bit -> row hex):
REMAINING9 = {
    4: "00000000000000043800000008002000",
    18: "00000000000000003800000408002000",
    20: "00000000000000003800000008003000",
    21: "00000000000000003800000008002002",
    28: "00000000000000003800400008002000",
    109: "00000000000000003800000008002200",
    112: "00000000010000003800000008080000",
    116: "00000000000000003800100008080000",
    118: "00000000000000003800000008480000",
}
# pinned per-receipt (marginal, marginal_in_manifest) in publication order:
PINNED_MARGINAL = {4: 5, 15: 4, 18: 5, 20: 5, 21: 5, 23: 4, 25: 0, 28: 5,
                   66: 4, 79: 0, 91: 0, 101: 0, 109: 5, 112: 5, 116: 5,
                   118: 5, 119: 4}
PINNED_MIM = {4: 1, 15: 0, 18: 1, 20: 1, 21: 1, 23: 0, 25: 0, 28: 1, 66: 0,
              79: 0, 91: 0, 101: 0, 109: 1, 112: 1, 116: 1, 118: 1, 119: 0}
# pinned new-head frontier after the fold (v2 pre-registration):
PINNED_AFTER = (1419, 174, 6429, 508474, 4702, 372388)
# pinned per-parent rows (before -> after) for the nine touched parents:
PINNED_PARENTS = {
    "00000000000000003800000008000002": ((41, 3095), (39, 2962)),
    "00000000000000003800000008001000": ((46, 3448), (45, 3384)),
    "00000000000000003800000008002000": ((51, 3564), (42, 2929)),
    "00000000000000003800000008400000": ((44, 3268), (43, 3197)),
    "00000000000000003800000408000000": ((56, 4624), (55, 4550)),
    "00000000000000003800100008000000": ((66, 5493), (65, 5417)),
    "00000000000000003800400008000000": ((56, 4444), (55, 4375)),
    "00000000000000043800000008000000": ((67, 5621), (66, 5547)),
    "00000000000000801202000000000100": ((60, 4939), (59, 4865)),
}
RAW_BLOBS = {
    "class2-lane-cost65f-raw-batch1-20261114.jsonl":
        "46ff5b200af04de19db8dd0ce1a57d180c70ba90",
    "class2-lane-cost65f-raw-batch2-20261114.jsonl":
        "cd3bfedbb07e7717ae4a5be44ff130dfd6c4a696",
    "class2-lane-cost65f-raw-batch3-20261114.jsonl":
        "1f3d6dc89b244f66858824ef99abe6ee2dd2de4e",
    "class2-lane-cost65f-raw-batch4-20261114.jsonl":
        "cfffbcdd472a65ca06860d691f2f8506f5315a98",
    "class2-lane-cost65f-raw-batch5-20261114.jsonl":
        "9d789a2906b471823a99aed33a2b3dc41c62e271",
    "class2-lane-cost65f-raw-batch6-20261114.jsonl":
        "2ae5fd9b57b35ff4660f7da4c13c2122e70cfb7a",
    "class2-lane-cost65f-raw-batch7-20261114.jsonl":
        "89b554a338845f7ef77f4497d97ccfa70d84c045",
    "class2-lane-cost65j-raw-batch8-20261116.jsonl":
        "963c9f80db41d8d0cce4bdde642917cf5695a210",
    "class2-lane-cost65j-raw-batch9-20261116.jsonl":
        "52cd7d8daf0d486d76694fa5e836583bd6bd669f",
}
BATCH_BIT_NODES = {
    "class2-lane-cost65f-raw-batch1-20261114.jsonl": 70778854,
    "class2-lane-cost65f-raw-batch2-20261114.jsonl": 76633276,
    "class2-lane-cost65f-raw-batch3-20261114.jsonl": 70718886,
    "class2-lane-cost65f-raw-batch4-20261114.jsonl": 36995447,
    "class2-lane-cost65f-raw-batch5-20261114.jsonl": 45653717,
    "class2-lane-cost65f-raw-batch6-20261114.jsonl": 36897448,
    "class2-lane-cost65f-raw-batch7-20261114.jsonl": 47202063,
    "class2-lane-cost65j-raw-batch8-20261116.jsonl": 15793993,
    "class2-lane-cost65j-raw-batch9-20261116.jsonl": 1929932,
}
SWEEP_NODES_TOTAL = 402652063  # incl. pilot controls (5949 x7 + 3402 x2)
WIN_NODES = 158472633
REFUTED_RUN_NODES = 244130983
CERTS_MANIFEST_BLOB = None  # pinned after assembly, before publication


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


_orig_write_text = Path.write_text


def _write_text_lf(self, data, encoding=None, errors=None, newline=None):
    with self.open("w", encoding=encoding or "utf-8", errors=errors,
                   newline="\n") as f:
        f.write(data)


Path.write_text = _write_text_lf

# ---------- 1. reproduce the cost-60c chain head 1410 ----------
ns60 = runpy.run_path(str(HERE / "scripts" /
                          "recompute_frontier_cost60c_receipts_"
                          "20261116.py"))
s_1410 = set(ns60["s_after"])
st_1410 = ns60["st_after"]
rem_1410 = ns60["rem_after"]
dem_1410 = ns60["dem_after"]
covers = ns60["covers"]
manifest = ns60["manifest"]
classes = ns60["classes"]
summary_state = ns60["summary_state"]
canon = ns60["canon"]
folded_1410 = set(ns60["folded"]) | {int(ns60["ROOT"], 16)}
assert (st_1410["solved_s6_in_manifest"], st_1410["remaining_s5_orbits"],
        st_1410["unique_remaining_s6"], st_1410["sum_remaining_cost"],
        st_1410["s6_needed_by_open_classes"],
        st_1410["cost_needed_by_open_classes"]) == \
    (1410, 174, 6438, 509109, 4711, 373023), st_1410
assert len(folded_1410) == 718, len(folded_1410)
print("CONTROL cost-60c chain head 1410/174/6438/509109/4711/373023 "
      "reproduced (the published cost-60c fold script re-asserts the whole "
      "chain, the cost-75e fold and its three output blobs); 718 folded "
      "roots (717 + the cost-60c root)")

# ---------- 2. re-derive the 65f+65j sweep from the raw batches ----------
bit_recs = {}
pilots = []
for i in range(1, 8):
    p = OUT / f"class2-lane-cost65f-raw-batch{i}-20261114.jsonl"
    sha, _ = git_blob_sha(p)
    assert sha == RAW_BLOBS[p.name], p.name
for name in list(RAW_BLOBS):
    p = OUT / name
    sha, _ = git_blob_sha(p)
    assert sha == RAW_BLOBS[name], name
    lines = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    pnodes = 0
    for rec in lines:
        if "control" in rec:
            pilots.append(rec["nodes"])
            assert rec["loss"] is False and rec["capped"] is False, rec
        else:
            assert rec["bit"] not in bit_recs, "each run bit exactly once"
            bit_recs[rec["bit"]] = rec
    assert sum(r["nodes"] for r in lines if "bit" in r) == \
        BATCH_BIT_NODES[name], name
assert sorted(pilots) == [3402, 3402] + [5949] * 7, pilots
assert len(bit_recs) == 64, len(bit_recs)
sha, _ = git_blob_sha(OUT / "class2-lane-cost65j-inflight-20261115.json")
assert sha == CLAIM_BLOB, "claim v5 blob"
claim = json.loads((OUT / "class2-lane-cost65j-inflight-20261115.json")
                   .read_text())
assert claim["s6_child"] == CHILD and claim["legal_candidates_total"] == 65
assert sorted(bit_recs) + [] == \
    sorted(set(claim["candidate_bits"]) - {TRANSFERRED_BIT})
win_bits = sorted(b for b, r in bit_recs.items() if r["loss"] is True)
refuted_run = sorted(b for b, r in bit_recs.items()
                     if r["loss"] is False and r["capped"] is False)
capped = sorted(b for b, r in bit_recs.items() if r["capped"] is True)
assert win_bits == WIN_BITS, win_bits
assert sorted(refuted_run + [TRANSFERRED_BIT]) == \
    sorted(claim["progress"]["refuted_bits"])
assert len(refuted_run) + 1 == 48 and capped == []
assert sum(r["nodes"] for r in bit_recs.values()) == \
    WIN_NODES + REFUTED_RUN_NODES
assert sum(r["nodes"] for b, r in bit_recs.items() if r["loss"] is True) == \
    WIN_NODES
assert all(r["terminalStoneRange"] == [13, 17] for r in bit_recs.values())
assert all(r["andclose"] is True for r in bit_recs.values())
assert sum(BATCH_BIT_NODES.values()) + sum(pilots) == SWEEP_NODES_TOTAL
assert TRANSFERRED_BIT not in bit_recs
print(f"CONTROL 65f+65j sweep re-derived from the 9 blob-pinned raw "
      f"batches: 65 candidates (64 run + bit {TRANSFERRED_BIT} transfer), "
      f"17 WIN7-D10 bits {win_bits}, 48 REFUTED-D10 (47 run + transfer), "
      f"0 capped, {SWEEP_NODES_TOTAL} nodes incl. pilots; terminal "
      f"[13,17] and andclose all; pilots 5949 x7 (v15) + 3402 x2 (v16)")

# ---------- 3. re-assert the published pre-fold cover map ----------
sha, blen = git_blob_sha(OUT / "class2-lane-cost65j-win-marginals-"
                         "20261116.json")
assert sha == COVERMAP_BLOB and blen == 12900, "cover map blob"
cmap = json.loads((OUT / "class2-lane-cost65j-win-marginals-20261116.json")
                  .read_text())
assert cmap["child"] == CHILD
assert sorted(int(b) for b in cmap["receipts"]) == WIN_BITS
cov_union = set()
manifest_hexes = {f"{k:032x}" for k in manifest}
for b in WIN_BITS:
    e = cmap["receipts"][str(b)]
    assert e["root_hex"] == ROOTS[b], b
    dels = {f"{canon(int(ROOTS[b], 16) ^ (1 << s)):032x}"
            for s in range(121) if (int(ROOTS[b], 16) >> s) & 1}
    assert set(e["in_manifest_deletions"]) == dels & manifest_hexes, b
    cov_union |= set(e["in_manifest_deletions"])
assert len(cov_union) == 34, len(cov_union)
assert CHILD in cov_union
assert cov_union == set(cmap["covered_manifest_rows_union"])
assert cmap["known_65f_covered_rows_check"][ROW64_BIT21] == \
    {"covered_by_65f_bit": 21, "verified": True}
assert cmap["known_65f_covered_rows_check"][ROW64_BIT20] == \
    {"covered_by_65f_bit": 20, "verified": True}
print("CONTROL pre-fold cover map re-asserted (blob-pinned): 17 receipts "
      "cover exactly 34 manifest rows by D4-canonical one-stone deletions; "
      "the child row and the two cost-64 rows (65f bits 21/20) included")

# ---------- 4. re-assert the four new cost-65j certificates ----------
sha, blen = git_blob_sha(OUT / "class2-lane-cost65j-win7-certificates-"
                         "20261116.json")
assert sha == "d4981d7e075d8b2bb2e032790cbb95555bdc2b84" and blen == 9804, \
    "certificates manifest blob"
cman = json.loads((OUT / "class2-lane-cost65j-win7-certificates-"
                   "20261116.json").read_text())
assert cman["target"]["s6_child_hex"] == CHILD
certs = {}
for bit in WIN_BITS_65J:
    e = next(c for c in cman["certificates"] if c["bit"] == bit)
    assert e["verdict"] == "WIN7" and e["child_hex"] == CHILD
    assert e["root_hex"] == ROOTS[bit]
    root_v = int(e["root_hex"], 16)
    assert root_v == CHILD_V | (1 << bit), bit
    assert e["d4_canonical_hex"] == f"{canon(root_v):032x}", bit
    assert e["root_mobility_matches_legal_candidates_py"] is True, bit
    pc = e["published_cert"]
    if pc["path"] is None:
        # split parts (all four bits): cat part1of2 part2of2 == whole
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
    else:
        data = (CERTS / f"bit{bit}-root-{ROOTS[bit]}.cert").read_bytes()
        assert pc["path"].endswith(f"bit{bit}-root-{ROOTS[bit]}.cert"), bit
        assert len(data) == pc["bytes"], bit
    assert hashlib.md5(data).hexdigest() == \
        (pc["md5"] if pc["path"] is not None else pc["whole_md5"]), bit
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
    assert bigint["bigint_record"]["union_missing"] == 0 and \
        bigint["bigint_record"]["union_extra"] == 0, bit
    assert bigint["bigint_record"]["subroots_passed"] == e["sub_roots"], bit
    assert bigint["bigint_record"]["terminal_range"] == [13, 17], bit
    bare = json.loads((CERTS / f"bit{bit}-root-{ROOTS[bit]}"
                       "-bareiss-verify.json").read_text())
    assert bare["subroots_verified"] == e["sub_roots"], bit
    assert bare["all_subroots_pass"] is True, bit
    certs[bit] = e
tot = cman["totals"]
assert (tot["published_certificates"], tot["rows"], tot["extraction_nodes"],
        tot["sub_roots"], tot["winner_states"], tot["loser_states"],
        tot["terminal_count"], tot["cert_bytes"]) == \
    (4, 232426, 36781305, 225, 313767, 93295, 79542, 8381377), tot
print("CONTROL the four new cost-65j certificates re-asserted: manifest "
      "blob pinned, root = child | 1<<bit, D4 canonical, md5 byte pins "
      "(all four bits via part1of2+part2of2 with per-part blob shas and "
      "receipts), sorted-unique rows, BigInt union 0/0 and Bareiss "
      "sub-roots; manifest totals 232,426 rows / 36,781,305 extraction "
      "nodes / 225 sub-roots")

# ---------- 4b. conflict census: all 65 candidate orbits vs 718 folded ----
folded_d4 = {canon(r) for r in folded_1410}
census = []
for b in claim["candidate_bits"]:
    if canon(CHILD_V | (1 << b)) in folded_d4:
        r = bit_recs.get(b)
        verdict = ("WIN7" if r["loss"] is True else
                   "REFUTED-transfer" if b == TRANSFERRED_BIT else "REFUTED")
        census.append((b, verdict))
assert census == [(25, "WIN7"), (79, "WIN7"), (91, "WIN7"),
                  (101, "WIN7")], census
print("CONTROL conflict census: exactly four of the 65 candidate orbits "
      "were already folded (bits 25/79/91/101); the 65f/65j sweep "
      "re-derived every one of them WIN7-D10 — zero WIN/LOSS conflicts "
      "against the 718 folded roots; the other 61 orbits are disjoint")

# ---------- 5. root overlap audit against the 718 folded roots ----------
new_roots = {int(ROOTS[b], 16) for b in WIN_BITS}
raw_hits = sorted(b for b in WIN_BITS if int(ROOTS[b], 16) in folded_1410)
d4_hits = sorted(b for b in WIN_BITS
                 if canon(int(ROOTS[b], 16)) in folded_d4)
assert raw_hits == [25], raw_hits
assert d4_hits == [25, 79, 91, 101], d4_hits
assert len({canon(int(ROOTS[b], 16)) for b in WIN_BITS}) == 17, \
    "the 17 receipts occupy 17 distinct D4 orbits"
print("CONTROL root overlap audit: of the 17 receipt roots exactly one is "
      "raw-hex identical to an already-folded root (bit 25, the cost-72b "
      "receipt) and four share D4 orbits with earlier folds (bits "
      "25/79/91/101, all cross-cover WIN receipts); the other 13 are "
      "disjoint from the 718 folded roots raw-hex and D4-canonically; "
      "17 distinct D4 orbits pairwise")

# ---------- 6. the child is already closed; the nine rows remain ----------
assert CHILD_V in manifest and CHILD_V in s_1410, \
    "the child is a manifest row already solved at head 1410"
# blob-pinned published record of the closing fold:
sha, blen = git_blob_sha(OUT / "class-frontier-warm-multiband2-recompute-"
                         "20261115.json")
assert sha == MERGE2_BLOB and blen == 13842, "warm-multiband2 blob"
merge2 = json.loads((OUT / "class-frontier-warm-multiband2-recompute-"
                    "20261115.json").read_text())
closing_rec = next(r for r in merge2["warm_multiband2_addition"]
                   if r.get("band") == "class2-lane-cost63a"
                   and r.get("bit") == 97)
assert closing_rec == {
    "band": "class2-lane-cost63a", "bit": 97,
    "root_hex": "00000002000000809102000800000000", "covers": 7,
    "marginal": 5, "marginal_in_manifest": 1,
    "marginal_manifest_hexes": [CHILD]}, closing_rec
sha, blen = git_blob_sha(OUT / "class-frontier-unified-merge-recompute-"
                         "20261115.json")
assert sha == MERGE_UNIFIED_BLOB and blen == 15534, "unified-merge blob"
for b, (root_hex, prov) in CLOSERS.items():
    rv = int(root_hex, 16)
    assert rv in folded_1410, b
    assert canon(rv) == canon(int(ROOTS[b], 16)), b
    assert CHILD_V in covers(rv), b
    assert bit_recs[b]["loss"] is True, b
assert int(ROOTS[25], 16) == int(CLOSERS[25][0], 16)
assert rem_1410.get(PARENT_S5, []) == [], \
    "the third class-2 target S5 is fully closed at head 1410"
# the exact nine still-remaining covered rows:
rem_rows = {}
for bstr, e in cmap["receipts"].items():
    for row_hex in e["in_manifest_deletions"]:
        rv = int(row_hex, 16)
        if rv not in s_1410:
            assert row_hex not in rem_rows, "each open row one receipt"
            rem_rows[row_hex] = int(bstr)
assert {v: k for k, v in rem_rows.items()} == REMAINING9, \
    sorted(rem_rows.items())
for row_hex in REMAINING9.values():
    rv = int(row_hex, 16)
    assert rv in manifest and rv not in s_1410
    d = dem_1410.get(row_hex)
    assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 0), (row_hex, d)
    pars = [h for h, rows in rem_1410.items()
            if row_hex in {r["s6_hex"] for r in rows}]
    assert len(pars) == 2 and all(classes.get(h, 0) == 2 for h in pars), \
        (row_hex, pars)
assert ROW64_BIT21 == REMAINING9[21] and ROW64_BIT20 == REMAINING9[20]
print("CONTROL the motivating child is already solved at 1410 (closed "
      "exactly once by the cost-63a bit-97 cross-cover receipt in the "
      "blob-pinned warm-multiband2/unified-merge fold, marginal = exactly "
      "the child row; three further folded cross-cover roots, all "
      "re-derived WIN7 by this sweep; the third class-2 target S5 has "
      "zero remaining rows at 1410); exactly nine of the 34 covered rows "
      "remain open, all dual class-2 demand c1=0,c2=2,c4=0, including "
      "the two cost-64 rows")

# ---------- 7. fold the 17 receipts on 1410 in publication order ----------
s_cur = set(s_1410)
addition = []
zero_mim = []
child_closed_by = None
for bit in WIN_BITS:
    root_v = int(ROOTS[bit], 16)
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
        "source": ("cost-65f raw batches 1-7 (v15)" if bit in WIN_BITS_65F
                   else "cost-65j raw batch 8 (v16)"),
        "certified": bit in WIN_BITS_65J,
        "sweep_nodes": bit_recs[bit]["nodes"],
        "covers": len(cov),
        "marginal": len(marg),
        "marginal_in_manifest": len(marg_m),
        "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
        "marginal_non_manifest_hexes":
            sorted(f"{k:032x}" for k in marg - marg_m),
    }
    if bit in WIN_BITS_65J:
        pc = certs[bit]["published_cert"]
        cert_md5 = pc["md5"] if pc["path"] is not None else pc["whole_md5"]
        rec.update({
            "rows": certs[bit]["rows"],
            "md5": cert_md5,
            "sub_roots_pass": certs[bit]["sub_roots"],
            "extraction_nodes": certs[bit]["extraction_nodes"],
            "terminal_count": certs[bit]["terminal_count"],
        })
    else:
        rec["certificate_status"] = (
            "no published certificate; verdict evidence = the blob-pinned "
            "v15 raw batch record + the corpus-wide raw-vs-audit node-sum "
            "consistency audit (commit f44f9f3a) + the canonical root "
            "verdict cache conflict-0 census (scan 2d090b49, second "
            "independent verification 7c99621f)")
    addition.append(rec)
    if not marg_m:
        zero_mim.append(bit)
    assert (len(marg), len(marg_m)) == (PINNED_MARGINAL[bit],
                                        PINNED_MIM[bit]), bit
    if marg_m:
        assert sorted(f"{k:032x}" for k in marg_m) == \
            [REMAINING9[bit]], bit
    s_cur |= marg
assert child_closed_by is None, \
    "the child is already solved at 1410 and must not close here"
cov_all = set()
for bit in WIN_BITS:
    cov_all |= covers(int(ROOTS[bit], 16))
assert s_cur == s_1410 | cov_all, \
    "set-equality: s_after == s_1410 UNION covers(17 roots)"
total_mim = sum(a["marginal_in_manifest"] for a in addition)
total_marg = sum(a["marginal"] for a in addition)
assert (total_marg, total_mim) == (61, 9)
assert zero_mim == [15, 23, 25, 66, 79, 91, 101, 119], zero_mim
st_after, rem_after, uniq_after, dem_after = summary_state(s_cur)
assert (st_after["solved_s6_in_manifest"], st_after["remaining_s5_orbits"],
        st_after["unique_remaining_s6"], st_after["sum_remaining_cost"],
        st_after["s6_needed_by_open_classes"],
        st_after["cost_needed_by_open_classes"]) == PINNED_AFTER, st_after
assert st_after["solved_s6_in_manifest"] == 1410 + total_mim
assert st_after["hist"] == {"c2=0,c4=1": 526, "c2=0,c4=2": 3013,
                            "c2=0,c4=3": 12, "c2=1,c4=0": 214,
                            "c2=1,c4=1": 54, "c2=1,c4=2": 9,
                            "c2=2,c4=0": 817, "c2=2,c4=1": 5,
                            "c2=2,c4=2": 52}, st_after["hist"]
print("AFTER cost-65j fold:", json.dumps(st_after, indent=1))
print(f"total marginal={total_marg} marginal_in_manifest={total_mim}; "
      f"zero-mim receipts: {zero_mim}; child closed by bit: "
      f"{child_closed_by} (already closed at 1410 by the cost-63a bit-97 "
      "cross-cover receipt)")

# ---------- 8. per-parent rows at the new head ----------
parents_after = {}
lost_detail = {}
cov_hexes = {f"{k:032x}" for k in cov_all}
for h in sorted(PINNED_PARENTS):
    old_exp, new_exp = PINNED_PARENTS[h]
    old = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1410[h]}
    new = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_after[h]}
    lost = {k: v for k, v in old.items() if k not in new}
    assert set(lost) <= cov_hexes, (h, sorted(set(lost) - cov_hexes))
    assert new == {k: v for k, v in old.items() if k not in lost}, h
    assert (len(old), sum(old.values())) == old_exp, (h, len(old),
                                                      sum(old.values()))
    assert (len(new), sum(new.values())) == new_exp, (h, len(new),
                                                     sum(new.values()))
    parents_after[h] = {"s5_hex": h, "rows": len(new),
                         "edge_cost": sum(new.values()),
                         "rows_before": len(old),
                         "edge_cost_before": sum(old.values())}
    lost_detail[h] = lost
assert sum(len(v) for v in lost_detail.values()) == 2 * total_mim, \
    "the nine rows are dual-parented: 18 parent-row incidences"
assert CHILD not in {r for v in lost_detail.values() for r in v}
print("per-parent rows at the new head (touched parents): " + "; ".join(
    f"{k} {v['rows_before']}/{v['edge_cost_before']} -> "
    f"{v['rows']}/{v['edge_cost']}" for k, v in parents_after.items()))

# ---------- 9. the nine rows actually closed; child already in s ----------
s_hex = {f"{k:032x}" for k in s_cur}
for row_hex in REMAINING9.values():
    assert row_hex in s_hex, (row_hex, "must be closed by the fold")
assert ROW64_BIT21 in s_hex and ROW64_BIT20 in s_hex
assert CHILD in s_hex, "the child was already solved at 1410"

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
AUDIT_BLOCKED = "00000000000000809082000000000000"
coverable = [c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED]
print("best class-4:", class4[0] if class4 else None)
print("best coverable class-2:", coverable[0] if coverable else None,
      "second:", coverable[1] if len(coverable) > 1 else None)
print("audit-blocked:", next((c for c in class2
                             if c["s5_hex"] == AUDIT_BLOCKED), None))

result = {
    "schema": "n11-class-frontier-cost65j-receipts-20261116-v2",
    "date": "2026-11-16",
    "baseline_record": {
        "cost60c_head_1410": "1410/174/6438/509109/4711/373023 "
                            "(reproduced byte-identically by runpy of the "
                            "published cost-60c fold script)",
        "claim": "class2-lane-cost65j-inflight-20261115.json (v5, git blob "
                 f"sha {CLAIM_BLOB}; supersedes the v4 sweep-complete "
                 "claim, all v4 fields preserved)",
        "sweep": "9 raw batch JSONLs (7 x cost-65f v15, 2 x cost-65j v16), "
                 "all blob-pinned; 65 candidates, 17 WIN7-D10, 48 "
                 "REFUTED-D10 (incl. the bit-113 canonical transfer), 0 "
                 f"capped, {SWEEP_NODES_TOTAL} nodes incl. pilots",
        "cover_map": "class2-lane-cost65j-win-marginals-20261116.json "
                     f"(git blob sha {COVERMAP_BLOB})",
        "premise_correction": "the motivating child "
                              "00000000000000809102000080000000 is "
                              "ALREADY SOLVED at head 1410: closed "
                              "exactly once by the cost-63a bit-97 "
                              "cross-cover receipt "
                              "00000002000000809102000800000000 in the "
                              "warm-multiband2/unified-merge fold "
                              "(2026-11-15, marginal = exactly the child "
                              "row, blob-pinned record); three further "
                              "folded roots cover it (cost-72b roots "
                              "00000000000000809102000082000000 = the 65f "
                              "bit-25 root byte-identical and "
                              "00000002000000809102000002000000, cost-69i "
                              "root 00000002000000809102000000002000); "
                              "the sweep re-derived all four orbits "
                              "WIN7 — zero conflicts; the third class-2 "
                              "target S5 00000000000000809102000000000000 "
                              "has zero remaining rows at 1410; the "
                              "fold's value is the nine still-remaining "
                              "covered rows, not the child",
    },
    "method": "runpy reproduction of the published cost-60c fold script, "
              "re-derivation of the 65f+65j sweep from the 9 blob-pinned "
              "raw batches, re-assertion of the published pre-fold cover "
              "map (34 covered manifest rows), re-assertion of the four "
              "new WIN7-D10 certificates (BigInt union 0/0 + Bareiss "
              "double verification), 65-candidate-orbit conflict census "
              "vs the 718 folded roots (exactly four overlaps, all "
              "WIN/WIN), the child-already-closed fact asserted against "
              "the blob-pinned warm-multiband2 record, the exact nine "
              "remaining covered rows pinned, then the 17 receipts folded "
              "in publication order with per-receipt marginals pinned and "
              "a set-equality control",
    "certificates_note": "the four cost-65j receipts (bits 112/116/118/119) "
                         "carry published WIN7-D10 certificates; the "
                         "thirteen cost-65f receipts (v15, 2026-11-14) "
                         "have no published certificates and are folded on "
                         "their blob-pinned raw sweep records — "
                         "certificate extraction for them remains optional "
                         "follow-up work",
    "cost65j_additions_on_cost60c_1410": addition,
    "totals": {
        "receipts": 17,
        "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "child_closed_by_bit": child_closed_by,
        "child_already_closed_by": "cost-63a bit-97 cross-cover receipt "
                                    "(warm-multiband2/unified-merge fold "
                                    "2026-11-15)",
        "conflict_census_overlaps": {"bits": [25, 79, 91, 101],
                                      "verdicts": "all WIN7, 0 conflicts"},
        "remaining_covered_rows_at_1410": 9,
        "zero_mim_receipts": zero_mim,
        "covered_manifest_rows_union_before_fold": 34,
        "sweep_nodes_total_incl_pilots": SWEEP_NODES_TOTAL,
    },
    "frontier_after_cost65j": {
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
                            "only; REFUTED-D10 sweeps prove only absence "
                            "of WIN7-D10; 11x11 empty board / two-stone "
                            "root {49,60} / S2 {59,60} / class 1 / class 2 "
                            "/ class 4 remain UNKNOWN",
}
(OUT / "class-frontier-cost65j-receipts-recompute-20261116.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-cost65j-receipts-recompute-20261116.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in rem_after.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                  r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / ("class-frontier-s5-ranking-after-cost65j-receipts-"
             "20261116.csv")).open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits",
                "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / ("class-frontier-top-candidates-s6-after-cost65j-receipts-"
             "20261116.csv")).open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    for label, cand in (("best class-4 blocker-candidate S5",
                         class4[0] if class4 else None),
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
            dd = dem_after.get(row["s6_hex"], {"c1": -1, "c2": -1, "c4": -1})
            w.writerow((cand["s5_hex"], row["s6_hex"],
                        row["s6_s7_edge_cost"],
                        f"c1={dd['c1']},c2={dd['c2']},c4={dd['c4']}"))
print("written ranking + top-candidates CSVs (after-cost65j-receipts)")

for p in ("class-frontier-cost65j-receipts-recompute-20261116.json",
          "class-frontier-s5-ranking-after-cost65j-receipts-20261116.csv",
          "class-frontier-top-candidates-s6-after-cost65j-receipts-"
          "20261116.csv",
          "class2-lane-cost65j-win7-certificates-20261116.json"):
    sha, blen = git_blob_sha(OUT / p)
    print(f"blob {p}: {sha} ({blen} bytes)")
