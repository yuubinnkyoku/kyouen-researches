#!/usr/bin/env python3
"""Fold the single cost-64g WIN7-D10 receipt (bit 89, root
00000000020100003800000008080000) into the published cost-64f chain head
1438/174/6410/507143/4683/371057 (2026-11-16).

Same protocol as recompute_frontier_cost64f_receipts_20261116.py:

1. runpy-reproduce the whole published cost-64f fold chain (every published
   assert re-run, head 1438) and re-assert its five output blobs;
2. re-derive the cost-64g sweep from the 8 blob-pinned raw batches plus the
   2 determinism reruns, the v15 crosscheck and the completed claim v2
   (NOT-STERILE: 1 WIN7-D10 bit 89 + 58 REFUTED-D10 swept + 5 transferred);
3. re-assert the published head-1438 pre-sweep census v3 bit table
   (open 59 == swept set, 5 transferred root canons, family data);
4. re-assert the published bit-89 certificate byte-for-byte (whole cert
   blob pin, md5/sha256 re-hash, BigInt/Bareiss verify records, root
   mobility == legal_candidates.py) and the published raw-sweep audit;
5. conflict census: all 64 candidate D4 orbits disjoint from the 760 folded
   roots (746 D4 canons) at head 1438;
6. assert the child genuinely remains open at head 1438 on both direct open
   class-2 parents (shared 30/2081, second 50/3631, edge cost 64,
   dual demand c1=0,c2=2,c4=0);
7. fold the receipt in publication order with per-receipt marginals and a
   set-equality control; emit the new canonical head, per-parent deltas,
   closed-row demand invariants, rankings, the fold record for the claim
   update (v3, all v2 fields preserved, v2 restorable byte-identically)
   and the three chain outputs.

Pre-registered expectations (recorded from the first derivation run, then
pinned): the receipt covers 7 S6 boards, 6 marginal on the 1438 baseline,
3 of them in the manifest - the child 00000000000100003800000008080000
plus 00000000000000801202010000080000 and
00000000020000801002010000080000; the child closes exactly once, by bit
89; the demand histogram loses exactly c2=0,c4=2 (3012->3011), c2=2,c4=0
(802->801) and c2=2,c4=2 (51->50) mass; the five affected open parents
(00000000000000003800000008002000, 00000000000000003800001000800000,
00000000000000801202000000080000, 00000000000000801202010000000000,
00000000020000003800000000080000) lose 7 parent-row incidences and 465
edge cost in total; the new canonical head is
1441/174/6407/506945/4680/370859.

Bookkeeping over published receipts only; solved counts measure manifest
coverage, not the game-theoretic value of any position; WIN7 certificates
prove a first-player win within depth 10 from the individual 7-stone roots
only; REFUTED-D10 is never a LOSS proof; the 11x11 empty board remains
UNKNOWN.
"""
import csv
import hashlib
import json
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SCRIPTS = HERE / "scripts"

CHILD = "00000000000100003800000008080000"
CHILD_V = int(CHILD, 16)
WIN_BITS = [89]
ROOTS = {b: f"{CHILD_V | (1 << b):032x}" for b in WIN_BITS}
ROOT_V = CHILD_V | (1 << 89)
PARENT_SH = "00000000000000003800000008002000"   # shared class-2 parent 30/2081
PARENT_2 = "00000000000000801202010000000000"    # second class-2 parent 50/3631
TRANSFERRED_BITS = [5, 29, 104, 111, 119]
SWEEP_NODES_TOTAL = 33505865
PILOT_NODES = 3402
V15_PILOT_NODES = 5949
V15_ANCHORS = [1, 43, 89, 118]
WIN_BIT_NODES = 690457
WIN_BIT_V15_NODES = 1760287
CERT_ROWS = 30373
CERT_EXTRACTION_NODES = 1278418
CERT_SUBROOTS = 45
CERT_BYTES = 1096891
HEAD_1438 = (1438, 174, 6410, 507143, 4683, 371057)
# pre-registered fold expectations (recorded from the first derivation run,
# then pinned; every value below is re-derived and asserted on every run)
PINNED_AFTER = (1441, 174, 6407, 506945, 4680, 370859)
PINNED_MARG = 6
PINNED_MIM = 3
PINNED_MIM_HEXES = ["00000000000000801202010000080000",
                    "00000000000100003800000008080000",
                    "00000000020000801002010000080000"]
PINNED_HIST = {"c2=0,c4=1": 526, "c2=0,c4=2": 3011, "c2=0,c4=3": 12,
               "c2=1,c4=0": 212, "c2=1,c4=1": 54, "c2=1,c4=2": 9,
               "c2=2,c4=0": 801, "c2=2,c4=1": 5, "c2=2,c4=2": 50}
PINNED_PARENTS = {
    "00000000000000003800000008002000": ((30, 2081), (29, 2017)),
    "00000000000000003800001000800000": ((66, 4719), (64, 4585)),
    "00000000000000801202000000080000": ((67, 5135), (66, 5066)),
    "00000000000000801202010000000000": ((50, 3631), (48, 3498)),
    "00000000020000003800000000080000": ((60, 4288), (59, 4223)),
}
PINNED_INCIDENCES = 7
PINNED_COST_DELTA = 465
CLAIM_V2_SCHEMA = "n11-class2-lane-cost64g-completed-20261116-v2"
CLAIM_V3_SCHEMA = "n11-class2-lane-cost64g-fold-complete-20261116-v3"
INDEP_RERUN_COMMIT = "1b0bd2cf7822feb9e272a3f90e0e70a34fa3a809"

# pinned input blobs (all landed on main before this fold)
FOLD64F_SCRIPT_BLOB = "522069ffbbd9fd3c6aeb168bce76b3b21a996f5c"
FOLD64F_JSON_BLOB = "e11f31f303d0f3ab1b6d124403867e9f4ecdbebf"
FOLD64F_RANKING_BLOB = "5d08ef277600481e18bcdbdf68cbf2f9b48a11e3"
FOLD64F_TOPCSV_BLOB = "838d98a3b2e68d28e546dc0a2597c2f7b5277e7c"
CLAIM64F_BLOB = "b43303e88f04949cb037fafaf7d898885af6eada"
WIN3_MANIFEST_BLOB = "29aedffcfe7e4f7d110671c26177d9ff9cbb085d"
PRESWEEP_V3_BLOB = "47174799e620da94abb4297b39edb079ce8b5936"
PRESWEEP_ROWS_BLOB = "89b11c4c85565f6e8a657211b354570de17e5d03"
CLAIM_V2_BLOB = "c899b52d8793c7272d16f36529cb1f690a93a312"
AUDIT_BLOB = "fc45acbd9d19ad662393d36ffdd36ff58215b5a7"
WIN1_MANIFEST_BLOB = "e30be681e5293071c128046bbabf6f4f84983f93"
CERT_BLOB = "1d2cc167b2212c2df6cb85c99f91d244cba4be55"
BIGINT_VERIFY_BLOB = "b8fb47dfd62b52add01d03b02d95a4403ccad6c6"
BAREISS_VERIFY_BLOB = "3b40d928642a07fc0444c1ca1ea09fe9171bcb0a"
CERT_SUMMARY_BLOB = "67dc529b081f7048f414c176a7b7c87332214094"
RAW_BLOBS = {
    1: "873807ad7015ee8865b00b93d73ea23a92d2140d",
    2: "e9b0b41bbf9b4602a1d89bf8be0e930db2a4d0ee",
    3: "f22888df77cb35d2ac371e6857f8c3b3b15c3084",
    4: "a8ba871fbfe981ad22d0292738734ee080a66a08",
    5: "07809fd4cd15e9c341528a24b33a70d95167e267",
    6: "13088f70b66e5e2506bd9f9ad3b5b680012a85bb",
    7: "fcc2786d8431a5fd2ce417c91d9589736a029dbb",
    8: "1f2ea9d81a5ede641f33a4fa6dd1a96dde15fd6e",
}
DET_BLOBS = {
    3: "f6266ff40b7b3101b9bec6c03bc50e215f33780d",
    5: "56998e7f86e4303dc4d4c248d0321cd37519da49",
}
V15_BLOB = "8f65eb1e78805f7f55dfa3bd0bba7060acc759a6"


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


def load_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]


def main():
    # ---------- 1. reproduce the cost-64f chain head 1438 -------------------
    ns64f = runpy.run_path(str(SCRIPTS /
                               "recompute_frontier_cost64f_receipts_"
                               "20261116.py"))
    sha, _ = git_blob_sha(SCRIPTS / "recompute_frontier_cost64f_receipts_"
                         "20261116.py")
    assert sha == FOLD64F_SCRIPT_BLOB, sha
    st_1438 = ns64f["st_after"]
    assert (st_1438["solved_s6_in_manifest"], st_1438["remaining_s5_orbits"],
            st_1438["unique_remaining_s6"], st_1438["sum_remaining_cost"],
            st_1438["s6_needed_by_open_classes"],
            st_1438["cost_needed_by_open_classes"]) == HEAD_1438, st_1438
    for fname, blob in (("class-frontier-cost64f-receipts-recompute-"
                         "20261116.json", FOLD64F_JSON_BLOB),
                        ("class-frontier-s5-ranking-after-cost64f-"
                         "receipts-20261116.csv", FOLD64F_RANKING_BLOB),
                        ("class-frontier-top-candidates-s6-after-cost64f-"
                         "receipts-20261116.csv", FOLD64F_TOPCSV_BLOB),
                        ("class2-lane-cost64f-inflight-20261116.json",
                         CLAIM64F_BLOB),
                        ("class2-lane-cost64f-win3-certificates-20261116.json",
                         WIN3_MANIFEST_BLOB)):
        sha, _ = git_blob_sha(OUT / fname)
        assert sha == blob, (fname, sha)
    s_1438 = ns64f["s_cur"]
    rem_1438 = ns64f["rem_after"]
    dem_1438 = ns64f["dem_after"]
    manifest = ns64f["manifest"]
    classes = ns64f["classes"]
    canon = ns64f["canon"]
    covers = ns64f["covers"]
    summary_state = ns64f["summary_state"]
    legal_candidates = ns64f["legal_candidates"]
    folded = set(ns64f["folded"])                     # 757 ints at head 1435
    assert len(folded) == 757
    addition_64f = ns64f["addition"]
    assert [a["bit"] for a in addition_64f] == [39, 72, 107]
    for a in addition_64f:                            # the 3 cost-64f roots
        folded.add(int(a["root_hex"], 16))
    assert len(folded) == 760
    folded_d4 = {canon(r) for r in folded}
    assert len(folded_d4) == 746, len(folded_d4)
    hist_1438 = st_1438["hist"]
    assert hist_1438["c2=2,c4=0"] == 802, hist_1438
    print("CONTROL cost-64f chain head 1438/174/6410/507143/4683/371057 "
          "reproduced (runpy of the published cost-64f fold script, git blob "
          f"{FOLD64F_SCRIPT_BLOB}; every published assert re-run); its five "
          "output blobs byte-identical; folded roots 760 / 746 D4 canons")

    # ---------- 2. re-derive the cost-64g sweep from the raw batches ---------
    bit_recs = {}
    batch_nodes = {}
    for n in sorted(RAW_BLOBS):
        p = OUT / f"class2-lane-cost64g-raw-batch{n}-20261116.jsonl"
        sha, _ = git_blob_sha(p)
        assert sha == RAW_BLOBS[n], (n, sha)
        rows = load_jsonl(p)
        ctrl = [r for r in rows if "control" in r]
        cand = [r for r in rows if "bit" in r]
        assert len(ctrl) == 1 and ctrl[0]["control"] == "pilot_d6"
        assert ctrl[0]["nodes"] == PILOT_NODES
        assert ctrl[0]["loss"] is False and ctrl[0]["capped"] is False
        bits = [r["bit"] for r in cand]
        assert len(bits) == len(set(bits)), n
        for r in cand:
            assert r["bit"] not in bit_recs, r["bit"]
            assert r["capped"] is False and r["andclose"] is True
            assert r["terminalStoneRange"] == [13, 17]
            bit_recs[r["bit"]] = r
        batch_nodes[n] = sum(r["nodes"] for r in cand)
    assert len(bit_recs) == 59
    assert sum(batch_nodes.values()) == SWEEP_NODES_TOTAL, batch_nodes
    win_bits = sorted(b for b, r in bit_recs.items() if r["loss"])
    refuted_swept = sorted(b for b, r in bit_recs.items() if not r["loss"])
    assert win_bits == WIN_BITS, win_bits
    assert len(refuted_swept) == 58
    assert bit_recs[89]["nodes"] == WIN_BIT_NODES, bit_recs[89]
    for n, blob in DET_BLOBS.items():
        p = OUT / f"class2-lane-cost64g-v16-determinism-rerun-batch{n}-" \
                  f"20261116.jsonl"
        sha, _ = git_blob_sha(p)
        assert sha == blob, (n, sha)
        det = load_jsonl(p)
        assert len(det) == 9
        dctl = [r for r in det if "control" in r]
        assert len(dctl) == 1 and dctl[0]["nodes"] == PILOT_NODES
        det_bits = {r["bit"]: (r["loss"], r["nodes"], r["capped"],
                               tuple(r["terminalStoneRange"]))
                    for r in det if "bit" in r}
        raw_bits = {r["bit"]: (r["loss"], r["nodes"], r["capped"],
                               tuple(r["terminalStoneRange"]))
                    for r in load_jsonl(OUT / f"class2-lane-cost64g-raw-"
                                        f"batch{n}-20261116.jsonl")
                    if "bit" in r}
        assert det_bits == raw_bits, n
    p = OUT / "class2-lane-cost64g-v15-crosscheck-20261116.jsonl"
    sha, _ = git_blob_sha(p)
    assert sha == V15_BLOB, sha
    v15 = load_jsonl(p)
    v15p = [r for r in v15 if "control" in r]
    assert len(v15p) == 1 and v15p[0]["nodes"] == V15_PILOT_NODES
    v15_bits = {r["bit"]: r for r in v15 if "bit" in r}
    assert sorted(v15_bits) == V15_ANCHORS, sorted(v15_bits)
    for b in V15_ANCHORS:
        assert v15_bits[b]["loss"] is bit_recs[b]["loss"], b
        assert v15_bits[b]["capped"] is False
    assert v15_bits[89]["loss"] is True
    assert v15_bits[89]["nodes"] == WIN_BIT_V15_NODES

    # ---------- 2b. the completed claim v2 (v3-restorable) -------------------
    claim_path = OUT / "class2-lane-cost64g-inflight-20261116.json"
    claim = json.loads(claim_path.read_text())
    v2_fields = None
    if claim["schema"] == CLAIM_V3_SCHEMA:
        # rerun on a folded claim: restore v2 byte-identically, then re-fold
        fld = claim["fold"]
        v2_fields = fld["v2_fields"]
        restored = {k: v for k, v in claim.items() if k != "fold"}
        restored["schema"] = CLAIM_V2_SCHEMA
        restored["status"] = v2_fields["status"]
        restored["supersedes"] = v2_fields["supersedes"]
        restored["results"]["fold"] = v2_fields["results_fold"]
        raw = json.dumps(restored, indent=1, ensure_ascii=False) + "\n"
        sha = hashlib.sha1(b"blob %d\0" % len(raw.encode()) +
                           raw.encode()).hexdigest()
        assert sha == CLAIM_V2_BLOB, "v3 -> v2 restore is not byte-identical"
        claim = restored
    assert claim["schema"] == CLAIM_V2_SCHEMA, claim["schema"]
    sha, blen = git_blob_sha(claim_path)
    if v2_fields is None:
        assert sha == CLAIM_V2_BLOB and blen == 12446, (sha, blen)
    res = claim["results"]
    assert claim["s6_child"] == CHILD and claim["candidate_count"] == 64
    assert claim["legal_candidates"] == sorted(list(bit_recs)
                                               + TRANSFERRED_BITS)
    assert res["win7_d10_bits"] == WIN_BITS and res["win7_d10_count"] == 1
    assert res["refuted_d10_bits_swept_v16"] == refuted_swept
    assert res["refuted_d10_bits_transferred"] == TRANSFERRED_BITS
    assert res["refuted_d10_count"] == 63 and res["capped_count"] == 0
    assert res["candidate_nodes_excluding_pilots"] == SWEEP_NODES_TOTAL
    for n in sorted(RAW_BLOBS):
        assert res["batch_bit_lists"][str(n)] == \
            [r["bit"] for r in load_jsonl(OUT / f"class2-lane-cost64g-raw-"
                                          f"batch{n}-20261116.jsonl")
             if "bit" in r], n
    assert claim["open_candidates_to_sweep"] == sorted(bit_recs)
    print(f"CONTROL cost-64g sweep re-derived from the 8 blob-pinned raw "
          f"batches: 1 WIN7-D10 (bit 89, {WIN_BIT_NODES} nodes) + 58 "
          f"REFUTED-D10 swept + 5 transferred = 64/64, 0 capped, "
          f"{SWEEP_NODES_TOTAL} nodes; determinism reruns batch3/batch5 "
          f"node-exact; v15 crosscheck anchors {V15_ANCHORS} two-directional "
          f"(bit 89 WIN at {WIN_BIT_V15_NODES} v15 nodes)")

    # ---------- 3. re-assert the published head-1438 census v3 -------------
    for fname, blob in (("class2-lane-next-target-presweep-1438-20261116.json",
                         PRESWEEP_V3_BLOB),
                        ("class2-lane-next-target-rows-1438-20261116.csv",
                         PRESWEEP_ROWS_BLOB)):
        sha, _ = git_blob_sha(OUT / fname)
        assert sha == blob, (fname, sha)
    presweep = json.loads((OUT / "class2-lane-next-target-presweep-"
                           "1438-20261116.json").read_text())
    assert presweep["schema"] == "n11-class2-lane-next-target-presweep-" \
        "1438-20261116-v1"
    assert presweep["chain_head"] == "1438/174/6410/507143/4683/371057"
    assert presweep["receipt_roots"] == {"count": 760, "distinct_canons": 746}
    bt = presweep["cheapest_row_bit_tables"][CHILD]
    assert len(bt) == 64
    census_open = sorted(e["bit"] for e in bt if e["status"] == "open")
    census_tr = {e["bit"]: e["root_canon"] for e in bt
                 if e["status"] == "harvested_refuted"}
    assert sorted(census_tr) == TRANSFERRED_BITS
    assert census_open == sorted(bit_recs), "census v3 open set == swept set"
    for e in bt:
        assert canon(CHILD_V | (1 << e["bit"])) == int(e["root_canon"], 16), \
            e["bit"]
    fam = presweep["family_census"][PARENT_SH]
    assert len(fam["rows"]) == 30 and \
        sum(r["cost"] for r in fam["rows"]) == 2081
    fch = [r for r in fam["rows"] if r["s6_hex"] == CHILD]
    assert len(fch) == 1
    fch = fch[0]
    assert fch["cost"] == 64 and fch["demand"] == {"c1": 0, "c2": 2, "c4": 0}
    assert fch["census"] == {"receipt_win": 0, "harvested_win": 0,
                             "harvested_refuted": 5, "open": 59}
    assert fch["open_after_census"] == 59
    print("CONTROL published head-1438 census v3 re-asserted: open 59 == "
          "swept set, 5 transferred root canons re-derived, shared family "
          "30/2081 with the child row at cost 64, demand c1=0,c2=2,c4=0")

    # ---------- 4. re-assert the published bit-89 certificate ----------------
    cert_dir = OUT / "class2-lane-cost64g-certificates"
    cert_name = "bit89-root-00000000020100003800000008080000"
    cert_path = cert_dir / f"{cert_name}.cert"
    sha, blen = git_blob_sha(cert_path)
    assert sha == CERT_BLOB and blen == CERT_BYTES, (sha, blen)
    for suffix, blob in ((".bigint-verify.json", BIGINT_VERIFY_BLOB),
                         ("-bareiss-verify.json", BAREISS_VERIFY_BLOB),
                         (".cert.part1of1.summary.json", CERT_SUMMARY_BLOB)):
        sha, _ = git_blob_sha(cert_dir / f"{cert_name}{suffix}")
        assert sha == blob, (suffix, sha)
    sha, blen = git_blob_sha(OUT / "class2-lane-cost64g-win1-certificates-"
                          "20261116.json")
    assert sha == WIN1_MANIFEST_BLOB and blen == 3701, (sha, blen)
    wman = json.loads((OUT / "class2-lane-cost64g-win1-certificates-"
                      "20261116.json").read_text())
    assert len(wman["certificates"]) == 1
    cert = wman["certificates"][0]
    assert cert["bit"] == 89 and cert["root_hex"] == ROOTS[89]
    assert cert["child_hex"] == CHILD and cert["verdict"] == "WIN7"
    assert cert["d4_canonical_hex"] == f"{canon(ROOT_V):032x}"
    assert cert["root_mobility_matches_legal_candidates_py"] is True
    assert cert["rows"] == CERT_ROWS
    assert cert["extraction_nodes"] == CERT_EXTRACTION_NODES
    assert cert["sub_roots"] == CERT_SUBROOTS
    assert cert["fbt_drops"] == 0 and cert["fatal"] is None
    assert cert["terminal_range"] == [13, 17]
    assert cert["winner_states"] == 44932 and cert["loser_states"] == 14916
    assert cert["terminal_count"] == 9172
    pc = cert["published_cert"]
    assert pc["bytes"] == CERT_BYTES and pc["git_blob_sha"] == CERT_BLOB
    assert pc["md5"] == hashlib.md5(cert_path.read_bytes()).hexdigest()
    assert pc["sha256"] == hashlib.sha256(
        cert_path.read_bytes()).hexdigest()
    assert wman["totals"] == {"published_certificates": 1, "rows": CERT_ROWS,
                              "extraction_nodes": CERT_EXTRACTION_NODES,
                              "sub_roots": CERT_SUBROOTS,
                              "winner_states": 44932, "loser_states": 14916,
                              "terminal_count": 9172, "cert_bytes":
                              CERT_BYTES}
    lines = cert_path.read_text().splitlines()
    assert len(lines) == CERT_ROWS + 2
    assert lines[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                        "second_to_move_LOSS")
    assert lines[1] == f"root {ROOTS[89]}"
    row_hexes = []
    for line in lines[2:]:
        parts = line.split(" ")
        assert len(parts) == 2 and len(parts[0]) == 32
        row_hexes.append(parts[0])
        int(parts[0], 16)
        int(parts[1])
    assert len(row_hexes) == CERT_ROWS
    assert row_hexes == sorted(set(row_hexes)), "cert rows sorted-unique"
    bj = json.loads((cert_dir / f"{cert_name}.bigint-verify.json")
                    .read_text())["bigint_record"]
    assert bj["union_missing"] == 0 and bj["union_extra"] == 0
    assert bj["subroots_passed"] == CERT_SUBROOTS
    assert bj["strategy_rows"] == CERT_ROWS and bj["rows_sorted_unique"] is True
    assert bj["consumed_winner_rows"] == CERT_ROWS
    assert bj["root_stones"] == 7 and bj["root_mobility"] == CERT_SUBROOTS
    assert bj["root_safe"] is True
    assert bj["winner_states"] == 44932 and bj["loser_states"] == 14916
    assert bj["terminal_count"] == 9172 and bj["terminal_range"] == [13, 17]
    br = json.loads((cert_dir / f"{cert_name}-bareiss-verify.json")
                    .read_text())
    assert br["all_subroots_pass"] is True
    assert br["subroots_verified"] == CERT_SUBROOTS and br["rows"] == CERT_ROWS
    assert br["terminal_count"] == 9172 and br["terminal_range"] == [13, 17]
    assert br["root_check"] == {"stones": 7, "loserMobility": 45}
    assert br["winner_states_seen_across_subroots"] == 69020
    summ = json.loads((cert_dir / f"{cert_name}.cert.part1of1.summary.json")
                      .read_text())
    assert summ["child"] == CHILD and summ["bit"] == 89
    assert summ["nMoves"] == CERT_SUBROOTS and summ["nRows"] == CERT_ROWS
    assert summ["fbt_drops"] == 0
    assert all(v["ok"] for v in summ["perMove"].values())
    assert not any(v["capped"] for v in summ["perMove"].values())
    assert sum(v["nodes"] for v in summ["perMove"].values()) == \
        CERT_EXTRACTION_NODES
    stones, moves = legal_candidates(ROOTS[89])
    assert len(stones) == 7 and len(moves) == CERT_SUBROOTS
    assert sorted(moves) == sorted(summ["moves"]) == sorted(br["subroot_moves"])
    assert cert["bigint_verify"] == {"union_missing": 0, "union_extra": 0,
                                     "subroots_passed": 45,
                                     "winner_states": 44932,
                                     "loser_states": 14916,
                                     "terminal_count": 9172}
    assert cert["bareiss_verify"]["all_subroots_pass"] is True

    # ---------- 4b. re-assert the published raw-sweep audit -----------------
    sha, blen = git_blob_sha(OUT / "class2-lane-cost64g-sweep-audit-"
                          "20261116.json")
    assert sha == AUDIT_BLOB and blen == 5511, (sha, blen)
    audit = json.loads((OUT / "class2-lane-cost64g-sweep-audit-20261116.json")
                       .read_text())
    assert audit["child"] == CHILD and audit["child_stones"] == \
        [19, 27, 59, 60, 61, 80]
    assert audit["claim_schema_crosscheck"] == CLAIM_V2_SCHEMA
    cc = audit["census_crosscheck"]
    assert cc["census_bit_table_open_59"] and cc["census_transferred_5"]
    assert cc["family_shared_30_2081"]
    d4s = audit["d4_orbit_collision_scan"]
    assert d4s["candidate_canons_distinct"] == 64
    assert d4s["intra_sweep_collisions"] == 0
    assert d4s["win_canon"] == f"{canon(ROOT_V):032x}"
    sa = audit["sweep_aggregate"]
    assert sa["win7_d10_bits"] == WIN_BITS and sa["win7_d10_count"] == 1
    assert sa["swept_candidates"] == 59 and sa["capped"] == 0
    assert sa["refuted_d10_swept"] == 58 and \
        sa["refuted_d10_transferred"] == 5 and sa["pilots_3402"] == 8
    assert sa["total_candidate_nodes"] == SWEEP_NODES_TOTAL
    assert [b["batch"] for b in sa["batches"]] == sorted(RAW_BLOBS)
    for brec in sa["batches"]:
        n = brec["batch"]
        assert brec["candidate_bits"] == \
            [r["bit"] for r in load_jsonl(OUT / f"class2-lane-cost64g-raw-"
                f"batch{n}-20261116.jsonl") if "bit" in r], n
        assert brec["pilot_nodes"] == PILOT_NODES
        assert brec["nodes"] == batch_nodes[n], n
    assert sa["heaviest_bits_nodes"]["43"] == max(
        r["nodes"] for r in bit_recs.values())
    for b in TRANSFERRED_BITS:
        tr = audit["transfers"][str(b)]
        assert tr["root"] == f"{CHILD_V | (1 << b):032x}", b
        assert tr["d4_canon"] == f"{canon(CHILD_V | (1 << b)):032x}", b
    v15a = audit["v15_crosscheck"]
    assert v15a["pilot_nodes"] == V15_PILOT_NODES and \
        v15a["anchors"] == V15_ANCHORS
    assert v15a["two_directional_agreement"] is True
    assert v15a["win_bit_89_v15_nodes"] == WIN_BIT_V15_NODES
    assert sorted(audit["independent_enumeration"]["legal_candidates"]) == \
        sorted(list(bit_recs) + TRANSFERRED_BITS)
    lp = audit["lift_parents"]
    assert lp["shared_parent"] == {"hex": PARENT_SH,
                                   "d4_canon": PARENT_SH,
                                   "rows_at_head_1438": 30,
                                   "edge_cost_at_head_1438": 2081,
                                   "matches_census_family": True}
    assert lp["second_parent"] == {"hex": PARENT_2, "d4_canon": PARENT_2,
                                   "rows_at_head_1438": 50,
                                   "edge_cost_at_head_1438": 3631}
    print("CONTROL the published bit-89 certificate re-asserted "
          "byte-for-byte: whole cert blob pin + md5/sha256 re-hash, 30,373 "
          "sorted-unique rows, BigInt union 0/0 + Bareiss 45/45 records, "
          "root mobility == legal_candidates.py; raw-sweep audit crosscheck "
          "(batches, transfers, lift parents 30/2081 + 50/3631) PASS")

    # ---------- 5. conflict census vs the folded roots at 1438 -------------
    census_overlaps = []
    for b in sorted(bit_recs) + TRANSFERRED_BITS:
        if canon(CHILD_V | (1 << b)) in folded_d4:
            census_overlaps.append(b)
    assert census_overlaps == [], census_overlaps
    assert ROOT_V not in folded and canon(ROOT_V) not in folded_d4
    assert len({canon(CHILD_V | (1 << b))
                for b in sorted(bit_recs) + TRANSFERRED_BITS}) == 64
    print("CONTROL conflict census: all 64 candidate D4 orbits are disjoint "
          "from the 760 folded roots (746 D4 canons) at 1438 - zero "
          "overlaps, zero WIN/LOSS conflicts")

    # ---------- 6. the child genuinely remains open at 1438 -----------------
    assert CHILD_V in manifest and CHILD_V not in s_1438
    for h, exp_rows, exp_cost in ((PARENT_SH, 30, 2081),
                                  (PARENT_2, 50, 3631)):
        rows = rem_1438.get(h, [])
        assert classes.get(h, 0) == 2, h
        assert len(rows) == exp_rows and \
            sum(int(r["s6_s7_edge_cost"]) for r in rows) == exp_cost, h
        ch = [r for r in rows if int(r["s6_hex"], 16) == CHILD_V]
        assert len(ch) == 1 and int(ch[0]["s6_s7_edge_cost"]) == 64, h
    d = dem_1438.get(CHILD)
    assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 0), d
    print("CONTROL the child genuinely remains at head 1438: both direct "
          "open class-2 parents hold the child row (shared 30/2081, second "
          "50/3631) at edge cost 64, dual demand c1=0,c2=2,c4=0")

    # ---------- 7. fold the single receipt on 1438 ---------------------------
    s_cur = set(s_1438)
    addition = []
    child_closed_by = None
    for bit in WIN_BITS:
        root_v = CHILD_V | (1 << bit)
        cov = covers(root_v)
        assert CHILD_V in cov, "the receipt must cover the child via its stone"
        marg = cov - s_cur
        marg_m = marg & manifest
        if CHILD_V in marg_m:
            assert child_closed_by is None
            child_closed_by = bit
        rec = {
            "bit": bit,
            "root_hex": ROOTS[bit],
            "d4_canonical_hex": f"{canon(root_v):032x}",
            "source": ("cost-64g raw batches 1-8 (v16) + the published "
                       "head-1438 presweep v3 transfer census"),
            "certified": True,
            "sweep_nodes": bit_recs[bit]["nodes"],
            "covers": len(cov),
            "marginal": len(marg),
            "marginal_in_manifest": len(marg_m),
            "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
            "marginal_non_manifest_hexes":
                sorted(f"{k:032x}" for k in marg - marg_m),
            "rows": cert["rows"],
            "md5": cert["published_cert"]["md5"],
            "sub_roots_pass": cert["sub_roots"],
            "extraction_nodes": cert["extraction_nodes"],
            "terminal_count": cert["terminal_count"],
        }
        addition.append(rec)
        assert (len(marg), len(marg_m)) == (PINNED_MARG, PINNED_MIM), bit
        assert sorted(f"{k:032x}" for k in marg_m) == PINNED_MIM_HEXES, bit
        s_cur |= marg
    assert child_closed_by == 89, child_closed_by
    cov_all = set()
    for bit in WIN_BITS:
        cov_all |= covers(CHILD_V | (1 << bit))
    assert s_cur == s_1438 | cov_all, \
        "set-equality: s_after == s_1438 UNION covers(1 root)"
    total_marg = sum(a["marginal"] for a in addition)
    total_mim = sum(a["marginal_in_manifest"] for a in addition)
    assert (total_marg, total_mim) == (PINNED_MARG, PINNED_MIM)
    st_after, rem_after, uniq_after, dem_after = summary_state(s_cur)
    assert (st_after["solved_s6_in_manifest"], st_after["remaining_s5_orbits"],
            st_after["unique_remaining_s6"], st_after["sum_remaining_cost"],
            st_after["s6_needed_by_open_classes"],
            st_after["cost_needed_by_open_classes"]) == PINNED_AFTER, st_after
    assert st_after["solved_s6_in_manifest"] == 1438 + total_mim
    assert st_after["hist"] == PINNED_HIST, st_after["hist"]
    print("AFTER cost-64g fold:", json.dumps(st_after, indent=1))
    print(f"total marginal={total_marg} marginal_in_manifest={total_mim}; "
          f"child closed by bit: {child_closed_by}")

    # ---------- 8. per-parent rows at the new head --------------------------
    cov_hexes = {f"{k:032x}" for k in cov_all}
    union_base = set()
    for a in addition:
        union_base |= {int(h, 16) for h in a["marginal_manifest_hexes"]}
    parents_after = {}
    lost_detail = {}
    for h in sorted(rem_1438):
        old = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1438[h]}
        new = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_after[h]}
        lost = {k: v for k, v in old.items() if k not in new}
        if not lost:
            assert new == old, h
            continue
        assert set(lost) <= cov_hexes, (h, sorted(set(lost) - cov_hexes))
        assert new == {k: v for k, v in old.items() if k not in lost}, h
        parents_after[h] = {"s5_hex": h, "classes": classes.get(h, 0),
                            "rows": len(new),
                            "edge_cost": sum(new.values()),
                            "rows_before": len(old),
                            "edge_cost_before": sum(old.values())}
        lost_detail[h] = lost
    incidences = sum(len(v) for v in lost_detail.values())
    cost_delta = sum(sum(v.values()) for v in lost_detail.values())
    assert incidences == PINNED_INCIDENCES, incidences
    assert cost_delta == PINNED_COST_DELTA, cost_delta
    assert sorted(parents_after) == sorted(PINNED_PARENTS), \
        sorted(parents_after)
    for h, pa in parents_after.items():
        old_exp, new_exp = PINNED_PARENTS[h]
        assert (pa["rows_before"], pa["edge_cost_before"]) == old_exp, h
        assert (pa["rows"], pa["edge_cost"]) == new_exp, h
    closed_hexes = {f"{k:032x}" for k in union_base}
    for h, lost in lost_detail.items():
        assert set(lost) <= closed_hexes, h
    print("per-parent rows at the new head (touched parents): " + "; ".join(
        f"{k} {v['rows_before']}/{v['edge_cost_before']} -> "
        f"{v['rows']}/{v['edge_cost']}" for k, v in parents_after.items()))
    print(f"parent-row incidences {incidences}, parent edge cost delta "
          f"{cost_delta}")

    # ---------- 9. the rows actually closed; demand invariants --------------
    s_hex = {f"{k:032x}" for k in s_cur}
    for a in addition:
        for row_hex in a["marginal_manifest_hexes"]:
            assert row_hex in s_hex, row_hex
            dd = dem_1438.get(row_hex)
            assert dd["c1"] == 0 and (dd["c2"] + dd["c4"]) > 0, (row_hex, dd)
    assert CHILD in s_hex
    dd = dem_1438[CHILD]
    assert (dd["c1"], dd["c2"], dd["c4"]) == (0, 2, 0), dd

    # ---------- 10. rankings at the new head ---------------------------------
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
        "schema": "n11-class-frontier-cost64g-receipts-20261116-v1",
        "date": "2026-11-16",
        "baseline_record": {
            "cost64f_head_1438": "1438/174/6410/507143/4683/371057 "
                                "(reproduced byte-identically by runpy of "
                                "the published cost-64f fold script, git "
                                "blob sha " + FOLD64F_SCRIPT_BLOB + "; all "
                                "published asserts re-run, five output blobs "
                                "re-asserted)",
            "claim": "class2-lane-cost64g-inflight-20261116.json (v2 "
                     "completed NOT-STERILE, git blob sha " + CLAIM_V2_BLOB +
                     "; supersedes the v1 in-flight claim blob "
                     "895b0cfc09ff042b2ca0626f9d535ac7ddc0c5aa; all v1 "
                     "fields preserved)",
            "sweep": "8 raw batch JSONLs (v16), all blob-pinned; 64 "
                     "candidates = 1 WIN7-D10 (bit 89) + 58 REFUTED-D10 "
                     "swept + 5 REFUTED-D10 transferred (D4-canonical "
                     "identity, published head-1438 presweep v3), 0 capped, "
                     "33505865 nodes + 8 pilots x 3402; determinism reruns "
                     "batch3/batch5 node-exact; v15 crosscheck "
                     "two-directional (anchors 1/43/89/118, the WIN bit 89 "
                     "at 1760287 v15 nodes); independently re-verified "
                     "node-exact 59/59 by the parallel-rerun verification "
                     "commit " + INDEP_RERUN_COMMIT,
            "presweep_v3": "class2-lane-next-target-presweep-1438-20261116."
                           f"json (git blob sha {PRESWEEP_V3_BLOB}; rows CSV "
                           f"git blob sha {PRESWEEP_ROWS_BLOB})",
            "certificate": "class2-lane-cost64g-win1-certificates-20261116."
                           f"json (git blob sha {WIN1_MANIFEST_BLOB}) + the "
                           "whole cert bit89-root-000000000201000038000000"
                           f"08080000.cert (git blob sha {CERT_BLOB}, "
                           "1096891 bytes, under the split threshold; "
                           "BigInt union 0/0 + Bareiss 45/45 records "
                           "blob-pinned)",
            "raw_sweep_audit": "class2-lane-cost64g-sweep-audit-20261116."
                              f"json (git blob sha {AUDIT_BLOB})",
        },
        "method": "runpy reproduction of the published cost-64f fold script "
                  "(whole-chain head 1438), re-derivation of the cost-64g "
                  "sweep from the 8 blob-pinned raw batches plus the 5 "
                  "blob-pinned pre-sweep transferred REFUTED verdicts, "
                  "re-assertion of the published bit-89 certificate "
                  "byte-for-byte (whole-cert blob pin, md5/sha256 re-hash, "
                  "sorted-unique rows, root mobility == legal_candidates.py, "
                  "BigInt union 0/0 + Bareiss records), 64-candidate-orbit "
                  "conflict census vs the folded roots (zero overlaps), the "
                  "child-remaining fact asserted on both direct open "
                  "parents, then the single receipt folded with per-receipt "
                  "marginals and a set-equality control",
        "cost64g_additions_on_cost64f_1438": addition,
        "totals": {
            "receipts": 1,
            "total_marginal": total_marg,
            "total_marginal_in_manifest": total_mim,
            "child_closed_by_bit": child_closed_by,
            "transferred_refuted_bits": TRANSFERRED_BITS,
            "conflict_census_overlaps": census_overlaps,
            "folded_roots_at_1438": {"receipt_roots": 760,
                                     "distinct_roots": 760,
                                     "distinct_d4_canons": 746},
            "rows_closed_hexes": addition[0]["marginal_manifest_hexes"],
            "sweep_nodes_excluding_pilots": SWEEP_NODES_TOTAL,
            "parent_row_incidences": incidences,
            "parent_edge_cost_delta": cost_delta,
        },
        "frontier_after_cost64g": {
            "solved_s6_in_manifest": st_after["solved_s6_in_manifest"],
            "remaining_s5_orbits": st_after["remaining_s5_orbits"],
            "unique_remaining_s6": st_after["unique_remaining_s6"],
            "sum_remaining_cost": st_after["sum_remaining_cost"],
            "s6_needed_by_open_classes":
                st_after["s6_needed_by_open_classes"],
            "cost_needed_by_open_classes":
                st_after["cost_needed_by_open_classes"],
            "demand_histogram_open_only": st_after["hist"],
            "best_class2": class2[0] if class2 else None,
            "best_class4": class4[0] if class4 else None,
            "best_class1": class1[0] if class1 else None,
            "best_coverable_class2": coverable[0] if coverable else None,
            "second_coverable_class2": coverable[1] if len(coverable) > 1
                                        else None,
        },
        "parents_after": parents_after,
        "lost_rows_per_parent": lost_detail,
        "interpretation_guard": "bookkeeping over published receipts; solved "
                                "counts measure manifest coverage, not the "
                                "game-theoretic value of any position; WIN7 "
                                "certificates prove a first-player win "
                                "within depth 10 from the individual "
                                "7-stone roots only; REFUTED-D10 proves only "
                                "absence of WIN7-D10 from that root and is "
                                "never a LOSS proof; 11x11 empty board / "
                                "two-stone roots {49,60} and {59,60} / S2 "
                                "{59,60} / class 1 / class 2 / class 4 "
                                "remain UNKNOWN",
    }
    (OUT / "class-frontier-cost64g-receipts-recompute-20261116.json"
     ).write_text(json.dumps(result, indent=1) + "\n")
    print("written class-frontier-cost64g-receipts-recompute-20261116.json")

    ranking = sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"])
                                        for r in rows)}
         for k, rows in rem_after.items()),
        key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                       r["remaining_s7_edge_cost"], r["s5_hex"]))
    with (OUT / ("class-frontier-s5-ranking-after-cost64g-receipts-"
                 "20261116.csv")).open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(("s5_hex", "classes", "remaining_s6_orbits",
                    "remaining_s7_edge_cost"))
        for r in ranking:
            w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                        r["remaining_s7_edge_cost"]))

    with (OUT / ("class-frontier-top-candidates-s6-after-cost64g-"
                 "receipts-20261116.csv")).open("w", newline="") as f:
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
    print("written ranking + top-candidates CSVs (after-cost64g-receipts)")

    # ---------- 11. claim v3: add the fold record ---------------------------
    fold_json_sha, _ = git_blob_sha(
        OUT / "class-frontier-cost64g-receipts-recompute-20261116.json")
    head_after = (f"{st_after['solved_s6_in_manifest']}/"
                  f"{st_after['remaining_s5_orbits']}/"
                  f"{st_after['unique_remaining_s6']}/"
                  f"{st_after['sum_remaining_cost']}/"
                  f"{st_after['s6_needed_by_open_classes']}/"
                  f"{st_after['cost_needed_by_open_classes']}")
    if v2_fields is None:
        v2_fields = {"status": claim["status"],
                     "supersedes": claim["supersedes"],
                     "results_fold": claim["results"]["fold"]}
    claim3 = {k: v for k, v in claim.items()}
    claim3["schema"] = CLAIM_V3_SCHEMA
    claim3["status"] = (
        "FOLD COMPLETE on 2026-11-16 by the long-term lane session: the "
        "single WIN7-D10 receipt (bit 89, root "
        "00000000020100003800000008080000) is folded on the reproduced "
        "head-1438 chain (runpy of the published cost-64f fold script, all "
        "asserts re-run) - the child row closes in the manifest exactly "
        "once (child closed by bit 89) and every open parent holding it "
        "loses the row; new canonical head " + head_after + "; conflict "
        "census vs the 760 folded roots (746 D4 canons) at 1438: zero "
        "overlaps, zero WIN/LOSS conflicts; all v1/v2 fields preserved "
        "(v2 restorable byte-identically from the fold record); 11x11 "
        "empty board, two-stone roots {49,60} and {59,60}, S2 {59,60}, "
        "and classes 1/2/4 all remain UNKNOWN")
    claim3["supersedes"] = (
        "v2 (completed NOT-STERILE claim, git blob sha " + CLAIM_V2_BLOB +
        ", all fields preserved) which superseded v1 (in-flight claim, "
        "commit 14bb1385baa9db17f8988d38e18757e2816ab885, git blob sha "
        "895b0cfc09ff042b2ca0626f9d535ac7ddc0c5aa)")
    claim3["results"]["fold"] = (
        "complete: the receipt is folded by "
        "recompute_frontier_cost64g_receipts_20261116.py; new canonical "
        "head " + head_after)
    claim3["fold"] = {
        "schema": "n11-class2-lane-cost64g-fold-20261116-v1",
        "fold_json": ("class-frontier-cost64g-receipts-recompute-"
                      "20261116.json (git blob sha " + fold_json_sha + ")"),
        "head_before": "1438/174/6410/507143/4683/371057",
        "head_after": head_after,
        "receipts": 1,
        "win_bit": 89,
        "root_hex": ROOTS[89],
        "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "child_closed_by_bit": child_closed_by,
        "parent_row_incidences": incidences,
        "parent_edge_cost_delta": cost_delta,
        "parents_after": parents_after,
        "v2_fields": v2_fields,
    }
    claim_path.write_text(json.dumps(claim3, indent=1, ensure_ascii=False)
                          + "\n")

    for p in ("class-frontier-cost64g-receipts-recompute-20261116.json",
              "class-frontier-s5-ranking-after-cost64g-receipts-20261116.csv",
              "class-frontier-top-candidates-s6-after-cost64g-"
              "receipts-20261116.csv",
              "class2-lane-cost64g-inflight-20261116.json"):
        sha, blen = git_blob_sha(OUT / p)
        print(f"blob {p}: {sha} ({blen} bytes)")


if __name__ == "__main__":
    main()
