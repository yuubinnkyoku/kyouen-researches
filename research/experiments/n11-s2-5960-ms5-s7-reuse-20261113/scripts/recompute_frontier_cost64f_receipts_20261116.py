#!/usr/bin/env python3
"""Fold the three cost-64f WIN7-D10 receipts on the cost-64d chain head
1435/174/6413/507337/4686/371251, producing the new canonical head
1438/174/6410/507143/4683/371057.

The cost-64f child 0000000000000080120a000000800000 (stones [23,49,51,57,60,
71], edge cost 64, dual class-2 demand c1=0,c2=2,c4=0) is the cheapest
not-fully-determined row of the head-1435 v2 census, held by both of its
direct open class-2 parents 00000000000000003800000008002000 (shared, 31
rows / 2145) and 0000000000000080120a000000000000 (43 rows / 3167).  Its 64
legal candidates are fully resolved by the published v16 sweep: 3 WIN7-D10
(bits 39, 72, 107), 56 REFUTED-D10 swept, 5 REFUTED-D10 transferred pre-sweep
by D4-canonical identity (bits 21, 35, 55, 64, 109), 0 capped, 54,905,391
candidate nodes excluding the eight 3402-node pilots; determinism rerun
batch2 node-exact in a fresh process; v15 crosscheck two-directional (pilot
5949, anchors [0, 32, 39, 118]).  All 3 WIN roots have published,
independently verifiable certificates (win3 manifest
class2-lane-cost64f-win3-certificates-20261116.json, git blob sha
29aedffcfe7e4f7d110671c26177d9ff9cbb085d; 116,367 rows / 9,709,419
extraction nodes / 142 sub-roots; BigInt union 0/0 + Bareiss all PASS).

This script reproduces the cost-64d chain head 1435 (running the published
cost-64d fold script, which internally reproduces the whole reconciliation
chain, the cost-75e, cost-60c and cost-65j folds and the five cost-64d
output blobs, after the thirteen published reconstruct_tmp_* prerequisites),
re-derives the cost-64f sweep from the eight blob-pinned raw batch JSONLs
(plus the five blob-pinned pre-sweep transferred REFUTED verdicts from the
published head-1435 v2 presweep bit table), re-asserts the published
parent-and-marginal audit blob (whose receipt_marginals_in_order records the
sequential per-receipt in-manifest marginals in publication order on the
1435 baseline and whose
projected_head_after_cost64f_fold pre-registers the new head), re-asserts
all three certificates byte-for-byte (whole/parts git blob pins, join
receipts, sorted-unique rows, root mobility == legal_candidates.py, BigInt
union 0/0 + Bareiss sub-root double-verification records, manifest totals),
runs the full 64-candidate D4-orbit conflict census against the folded roots
at 1435 (zero overlaps), asserts the 3 receipt roots are 3 distinct D4
orbits disjoint raw-hex and D4-canonically from every folded root, asserts
the child genuinely remaining at 1435 (both open parents hold the child row
at edge cost 64, dual class-2 demand), then folds the 3 receipts on 1435 in
publication order (bits ascending) with all per-receipt marginals pinned.

Pre-registered expectations: the child closes exactly once, by bit 39; one
receipt is zero-marginal-in-manifest (bit 72); total marginal 15 /
marginal_in_manifest 3; the 3 closed rows are the child, 00000000000000a090
02000000002000 and 00000000020002801002000000080000; the new head is
1438/174/6410/507143/4683/371057 with the demand histogram losing exactly
c2=0,c4=2 (3013->3012), c2=2,c4=0 (803->802) and c2=2,c4=2 (52->51) mass;
the five affected open parents lose 7 parent-row incidences and 455 edge
cost in total.

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
CERTS = OUT / "class2-lane-cost64f-certificates"

CHILD = "0000000000000080120a000000800000"
CHILD_V = int(CHILD, 16)
WIN_BITS = [39, 72, 107]
TRANSFERRED_BITS = [21, 35, 55, 64, 109]
ROOTS = {b: f"{CHILD_V | (1 << b):032x}" for b in WIN_BITS}
PARENT_SH = "00000000000000003800000008002000"   # shared class-2 parent 31/2145
PARENT_2 = "0000000000000080120a000000000000"    # second class-2 parent 43/3167
CLAIM_BLOB = "b43303e88f04949cb037fafaf7d898885af6eada"  # v5 (fold complete)
WIN3_MANIFEST_BLOB = "29aedffcfe7e4f7d110671c26177d9ff9cbb085d"
AUDIT_BLOB = "d9f5f377b9503f034cb7e9220b0d84d716bde87d"
PRESWEEP_V2_BLOB = "59d42a6b1d8db4dbc498872576283e0130a0c390"
RAW_BLOBS = {
    "class2-lane-cost64f-raw-batch1-20261116.jsonl":
        "e33817e9457ab509789e0092492b6d1640936abc",
    "class2-lane-cost64f-raw-batch2-20261116.jsonl":
        "6dd3db9b4456366c0e2adc8c4a6d34cefe22eeec",
    "class2-lane-cost64f-raw-batch3-20261116.jsonl":
        "44ad9e809bea1a70c9587304669b055ad4c542df",
    "class2-lane-cost64f-raw-batch4-20261116.jsonl":
        "1b62bb8a217f20cb13b7897fb14456255ab48bfb",
    "class2-lane-cost64f-raw-batch5-20261116.jsonl":
        "5a89767ccc9fe04ff205a9107aa7e949193efa26",
    "class2-lane-cost64f-raw-batch6-20261116.jsonl":
        "c598100ffe3ebe93170ebac5f8b96ec7af4d7b68",
    "class2-lane-cost64f-raw-batch7-20261116.jsonl":
        "0d5ed3ad125a247574754a79790e62b2a83913c3",
    "class2-lane-cost64f-raw-batch8-20261116.jsonl":
        "6b29c18220595fa47efbcea7aabfdd105f98f2a9",
}
BATCH_BITS = {
    1: [0, 1, 4, 6, 8, 9, 10, 11],
    2: [14, 18, 22, 26, 31, 32, 33, 39],
    3: [40, 42, 43, 52, 53, 54, 56, 58],
    4: [61, 66, 67, 72, 75, 76, 77, 79],
    5: [85, 86, 87, 88, 90, 94, 95, 96],
    6: [97, 98, 99, 102, 103, 105, 106, 107],
    7: [108, 110, 111, 112, 113, 114, 116, 117],
    8: [118, 119, 120],
}
BATCH_BIT_NODES = {
    1: 8328271,
    2: 9012852,
    3: 8836552,
    4: 6833000,
    5: 4518376,
    6: 7699783,
    7: 7479466,
    8: 2197091,
}
SWEEP_NODES_TOTAL = 54905391            # excluding the eight pilots
PILOT_NODES = 3402
DET_BLOB = "018cec32d3959b3e7a20a2a37359fb77c61432b1"
V15_BLOB = "a3d687e708d09b44be69964ffc3dee7369f90141"
V15_ANCHORS = [0, 32, 39, 118]
V15_PILOT_NODES = 5949
DET_BITS = [14, 18, 22, 26, 31, 32, 33, 39]
WIN3_TOTALS = {
    "published_certificates": 3, "rows": 116367,
    "extraction_nodes": 9709419, "sub_roots": 142,
    "winner_states": 161762, "loser_states": 49341,
    "terminal_count": 38570, "cert_bytes": 4197505,
}
# pinned per-receipt sequential (marginal, marginal_in_manifest) in
# publication order (bits ascending):
PINNED_MARGINAL = {39: 6, 72: 4, 107: 5}
PINNED_MIM = {39: 1, 72: 0, 107: 2}
PINNED_MIM_HEXES = {
    39: ["0000000000000080120a000000800000"],
    107: ["00000000000000a09002000000002000",
          "00000000020002801002000000080000"],
}
# pinned per-parent (rows, edge_cost) before -> after for the 5 parents:
PINNED_PARENTS = {
    "00000000000000003800000008002000": ((31, 2145), (30, 2081)),
    "00000000000000003800002080000000": ((78, 5837), (76, 5707)),
    "00000000000000801202000000080000": ((68, 5202), (67, 5135)),
    "0000000000000080120a000000000000": ((43, 3167), (41, 3036)),
    "00000000020000003800000000080000": ((61, 4351), (60, 4288)),
}
PINNED_AFTER = (1438, 174, 6410, 507143, 4683, 371057)
PINNED_HIST = {"c2=0,c4=1": 526, "c2=0,c4=2": 3012, "c2=0,c4=3": 12,
               "c2=1,c4=0": 212, "c2=1,c4=1": 54, "c2=1,c4=2": 9,
               "c2=2,c4=0": 802, "c2=2,c4=1": 5, "c2=2,c4=2": 51}
ZERO_MIM = [72]
UNION3 = [
    "0000000000000080120a000000800000",
    "00000000000000a09002000000002000",
    "00000000020002801002000000080000",
]
OPEN_PARENT_INcidences = {"0000000000000080120a000000800000": 2,
                         "00000000000000a09002000000002000": 3,
                         "00000000020002801002000000080000": 2}


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


_orig_write_text = Path.write_text


def _write_text_lf(self, data, encoding=None, errors=None, newline=None):
    with self.open("w", encoding=encoding or "utf-8", errors=errors,
                   newline="\n") as f:
        f.write(data)


Path.write_text = _write_text_lf

# ---------- 1. reproduce the cost-64d chain head 1435 ----------
ns64 = runpy.run_path(str(HERE / "scripts" /
                          "recompute_frontier_cost64d_receipts_"
                          "20261116.py"))
s_1435 = set(ns64["s_cur"])
st_1435 = ns64["st_after"]
rem_1435 = ns64["rem_after"]
dem_1435 = ns64["dem_after"]
covers = ns64["covers"]
manifest = ns64["manifest"]
classes = ns64["classes"]
summary_state = ns64["summary_state"]
canon = ns64["canon"]
folded_1419 = set(ns64["folded"])                    # 734 at head 1419
roots_64d = {int(a["root_hex"], 16) for a in ns64["addition"]}
assert (st_1435["solved_s6_in_manifest"], st_1435["remaining_s5_orbits"],
        st_1435["unique_remaining_s6"], st_1435["sum_remaining_cost"],
        st_1435["s6_needed_by_open_classes"],
        st_1435["cost_needed_by_open_classes"]) == \
    (1435, 174, 6413, 507337, 4686, 371251), st_1435
assert len(folded_1419) == 734 and len(roots_64d) == 23
folded = folded_1419 | roots_64d
assert len(folded) == 757, len(folded)
assert len({canon(r) for r in folded}) == 743
print("CONTROL cost-64d chain head 1435/174/6413/507337/4686/371251 "
      "reproduced (the published cost-64d fold script re-asserts the whole "
      "chain, the cost-65j / cost-60c / cost-75e folds and its five output "
      "blobs); folded roots at 1435: 734 (head 1419) + the 23 cost-64d "
      "receipt roots = 757 receipt roots, 743 distinct D4 canons")

# ---------- 2. re-derive the sweep from the raw batches ----------
sha, blen = git_blob_sha(OUT / "class2-lane-cost64f-inflight-20261116.json")
assert sha == CLAIM_BLOB and blen == 21680, "claim v5 blob"
claim = json.loads((OUT / "class2-lane-cost64f-inflight-20261116.json")
                  .read_text())
assert claim["schema"] == "n11-class2-lane-cost64f-completed-20261116-v5"
assert claim["s6_child"] == CHILD and claim["candidate_count"] == 64
cand_bits = claim["legal_candidates"]
bit_recs = {}
pilots = []
for i in range(1, 9):
    name = f"class2-lane-cost64f-raw-batch{i}-20261116.jsonl"
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
assert sorted(bit_recs) == sorted(set(cand_bits) - set(TRANSFERRED_BITS))
assert len(bit_recs) == 59
win_bits = sorted(b for b, r in bit_recs.items() if r["loss"] is True)
refuted_swept = sorted(b for b, r in bit_recs.items()
                       if r["loss"] is False and r["capped"] is False)
capped = sorted(b for b, r in bit_recs.items() if r["capped"] is True)
assert win_bits == WIN_BITS, win_bits
assert refuted_swept == claim["results"]["refuted_d10_bits_swept_v16"]
assert TRANSFERRED_BITS == claim["results"]["refuted_d10_bits_transferred"]
assert len(refuted_swept) == 56 and len(TRANSFERRED_BITS) == 5 and capped == []
assert len(win_bits) + len(refuted_swept) + len(TRANSFERRED_BITS) == 64
cr = claim["results"]
assert (cr["win7_d10_count"], cr["refuted_d10_count"],
        cr["refuted_d10_count_swept_v16"],
        cr["refuted_d10_count_transferred"], cr["determined_d10_count"],
        cr["capped_count"]) == (3, 61, 56, 5, 64, 0)
assert cr["count_identity"] == (
    "candidate_count = win7_d10_count + refuted_d10_count + capped_count; "
    "refuted_d10_count = swept_refuted_v16 + transferred_refuted")
assert sum(r["nodes"] for r in bit_recs.values()) == SWEEP_NODES_TOTAL
assert all(r["terminalStoneRange"] == [13, 17] for r in bit_recs.values())
assert all(r["andclose"] is True for r in bit_recs.values())
# determinism rerun batch2 node-exact
sha, _ = git_blob_sha(OUT / "class2-lane-cost64f-v16-determinism-rerun-"
                      "batch2-20261116.jsonl")
assert sha == DET_BLOB, "determinism blob"
det = [json.loads(x) for x in
       (OUT / "class2-lane-cost64f-v16-determinism-rerun-batch2-"
        "20261116.jsonl").read_text().splitlines() if x.strip()]
det_bits = {r["bit"]: r for r in det if "bit" in r}
assert sorted(det_bits) == DET_BITS
assert next(r for r in det if "control" in r)["nodes"] == PILOT_NODES
for b, r in det_bits.items():
    o = bit_recs[b]
    assert (r["loss"], r["nodes"], r["capped"],
            r["terminalStoneRange"]) == \
        (o["loss"], o["nodes"], o["capped"], o["terminalStoneRange"]), b
# v15 crosscheck two-directional
sha, _ = git_blob_sha(OUT / "class2-lane-cost64f-v15-crosscheck-20261116.jsonl")
assert sha == V15_BLOB, "v15 crosscheck blob"
v15 = [json.loads(x) for x in
       (OUT / "class2-lane-cost64f-v15-crosscheck-20261116.jsonl")
       .read_text().splitlines() if x.strip()]
v15_bits = {r["bit"]: r for r in v15 if "bit" in r}
assert sorted(v15_bits) == V15_ANCHORS
assert next(r for r in v15 if "control" in r)["nodes"] == V15_PILOT_NODES
assert all(v15_bits[b]["loss"] is True for b in V15_ANCHORS if b in win_bits)
assert all(v15_bits[b]["loss"] is False
           for b in V15_ANCHORS if b not in win_bits)
print(f"CONTROL cost-64f sweep re-derived from the 8 blob-pinned raw "
      f"batches plus the 5 blob-pinned pre-sweep transferred REFUTED "
      f"verdicts: 64 candidates, 3 WIN7-D10 bits {win_bits}, 56 REFUTED-D10 "
      f"swept + 5 transferred {TRANSFERRED_BITS}, 0 capped, "
      f"{SWEEP_NODES_TOTAL} nodes + 8 pilots x {PILOT_NODES}; terminal "
      f"[13,17] and andclose all; determinism rerun batch2 node-exact; v15 "
      f"crosscheck agrees two-directionally (pilot {V15_PILOT_NODES}, "
      f"anchors {V15_ANCHORS})")

# ---------- 2b. re-assert the published head-1435 v2 presweep table ------
sha, blen = git_blob_sha(OUT / "class2-lane-next-target-presweep-1435-v2-"
                         "20261116.json")
assert sha == PRESWEEP_V2_BLOB and blen == 138253, "presweep v2 blob"
presweep = json.loads((OUT / "class2-lane-next-target-presweep-1435-v2-"
                       "20261116.json").read_text())
assert presweep["receipt_roots"] == {"count": 757, "distinct_canons": 743}
assert presweep["harvest"]["conflicts"] == 0
tab = presweep["cheapest_row_bit_tables"][CHILD]
assert len(tab) == 64 and sorted(e["bit"] for e in tab) == cand_bits
tmap = {e["bit"]: e for e in tab}
for b in cand_bits:
    assert tmap[b]["root_canon"] == f"{canon(CHILD_V | (1 << b)):032x}", b
assert sorted(e["bit"] for e in tab
              if e["status"] == "harvested_refuted") == TRANSFERRED_BITS
assert sorted(e["bit"] for e in tab
              if e["status"] == "open") == sorted(bit_recs)
assert len({e["root_canon"] for e in tab}) == 64
assert tmap[39]["status"] == "open" and tmap[72]["status"] == "open" \
    and tmap[107]["status"] == "open"
print("CONTROL published head-1435 v2 presweep bit table re-asserted: all "
      "64 candidate D4 canons match the re-derived root canons exactly, "
      "the 5 transferred bits were harvested_refuted pre-sweep and the 59 "
      "swept bits were open; 757 receipt roots / 743 distinct canons; "
      "harvest conflicts 0")

# ---------- 3. re-assert the published parent-and-marginal audit ---------
sha, blen = git_blob_sha(OUT / "class2-lane-cost64f-parent-and-marginal-"
                         "audit-20261116.json")
assert sha == AUDIT_BLOB and blen == 11888, "parent-and-marginal audit blob"
audit = json.loads((OUT / "class2-lane-cost64f-parent-and-marginal-"
                    "audit-20261116.json").read_text())
assert audit["canonical_head_before_fold"] == \
    "1435/174/6413/507337/4686/371251"
assert audit["target_row"] == CHILD
assert audit["prior_receipt_and_verdict_census"]["prior_receipt_roots"] == \
    {"count": 757, "distinct_canons": 743}
assert audit["new_marginal_row_count"] == 3
assert audit["unique_row_cost_delta"] == 194
assert audit["parent_row_incidences"] == 7
assert audit["parent_edge_cost_delta"] == 455
assert audit["affected_parent_count"] == 5
assert all(v is True for v in audit["checks"].values()), audit["checks"]
assert sorted(e["s6_hex"] for e in audit["new_marginal_rows"]) == UNION3
rmio = audit["receipt_marginals_in_order"]
assert [e["bit"] for e in rmio] == WIN_BITS
mim_base = {}
for e in rmio:
    b = e["bit"]
    assert e["root_hex"] == ROOTS[b], b
    assert e["root_d4_canonical_hex"] == f"{canon(CHILD_V | (1 << b)):032x}", b
    assert e["prior_corpus_status"] == "open", b
    mim_base[b] = [int(h, 16) for h in e["marginal_rows_in_receipt_order"]]
    assert e["marginal_count"] == len(mim_base[b]) == PINNED_MIM[b], b
# the audit's per-receipt marginals are sequential in publication order
# (every receipt covers the child via its stone, so the baseline marginals
# of bits 72/107 also contain the child until bit 39 closes it):
s_tmp = set(s_1435)
for b in WIN_BITS:
    cov = covers(CHILD_V | (1 << b))
    marg_m = (cov - s_tmp) & manifest
    assert sorted(marg_m) == sorted(mim_base[b]), b
    assert CHILD_V in cov, b
    s_tmp |= cov - s_tmp
union_base = set()
for b in WIN_BITS:
    union_base |= set(mim_base[b])
assert len(union_base) == 3 and CHILD_V in union_base
for e in audit["new_marginal_rows"]:
    incid = OPEN_PARENT_INcidences[e["s6_hex"]]
    assert e["open_s5_parent_incidences"] == incid, e["s6_hex"]
    hold = [h for h, rows in rem_1435.items()
            if any(int(r["s6_hex"], 16) == int(e["s6_hex"], 16)
                   for r in rows)]
    assert len(hold) == incid, (e["s6_hex"], hold)
    assert sorted(hold) == sorted(p["s5_hex"]
                                  for p in e["direct_s5_parents"]), \
        e["s6_hex"]
    dd = dem_1435.get(e["s6_hex"])
    assert (dd["c1"], dd["c2"], dd["c4"]) == \
        (e["c1"], e["c2"], e["c4"]), e["s6_hex"]
    for p in e["direct_s5_parents"]:
        rows = rem_1435[p["s5_hex"]]
        assert (len(rows), sum(int(r["s6_s7_edge_cost"]) for r in rows)) == \
            (p["remaining_s6_orbits_head1435"],
             p["remaining_s7_edge_cost_head1435"]), p["s5_hex"]
        assert classes.get(p["s5_hex"], 0) == p["classes_mask"], p["s5_hex"]
proj = audit["projected_head_after_cost64f_fold"]
assert (proj["solved_s6_in_manifest"], proj["remaining_s5_orbits"],
        proj["unique_remaining_s6"], proj["sum_remaining_cost"],
        proj["s6_needed_by_open_classes"],
        proj["cost_needed_by_open_classes"]) == PINNED_AFTER, proj
assert proj["demand_histogram_open_only"] == PINNED_HIST, proj
print("CONTROL published parent-and-marginal audit re-asserted: the "
      "sequential receipt_marginals_in_order (1/0/2), the 3 new rows with "
      "their 7 open-parent incidences across 5 parents, the head-1435 per-parent "
      "rows/costs and the projected head 1438/174/6410/507143/4683/371057 "
      "with its histogram all agree with the re-derived values on the 1435 "
      "baseline")

# ---------- 4. re-assert all three published certificates ---------------
sys.path.insert(0, str(HERE / "scripts"))
from legal_candidates import legal_candidates  # noqa: E402

sha, blen = git_blob_sha(OUT / "class2-lane-cost64f-win3-certificates-"
                         "20261116.json")
assert sha == WIN3_MANIFEST_BLOB and blen == 9137, "win3 manifest blob"
wman = json.loads((OUT / "class2-lane-cost64f-win3-certificates-"
                   "20261116.json").read_text())
assert wman["schema"] == "n11-class2-lane-cost64f-win3-certificates-20261116-v2"
assert wman["target"]["s6_child_hex"] == CHILD
assert sorted(wman["target"]["direct_s5_parents"][0].keys()) == \
    sorted(["s5_hex", "classes_mask", "remaining_s6_orbits_head1435",
            "remaining_s7_edge_cost_head1435"])
assert sorted(p["s5_hex"] for p in wman["target"]["direct_s5_parents"]) == \
    [PARENT_SH, PARENT_2]
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
assert wman["totals"] == WIN3_TOTALS, wman["totals"]
assert len(certs) == 3
print("CONTROL all 3 win3 certificates re-asserted byte-for-byte: manifest "
      "blob pinned, root = child | 1<<bit, D4 canonical, whole / "
      "part1of2+part2of2 git blob pins with join receipts, md5 byte pins, "
      "sorted-unique rows, root mobility == legal_candidates.py, BigInt "
      "union 0/0 and Bareiss sub-roots all PASS; totals 116,367 rows / "
      "9,709,419 extraction nodes / 142 sub-roots")

# ---------- 5. conflict census vs the folded roots at 1435 --------------
folded_d4 = {canon(r) for r in folded}
census = []
for b in cand_bits:
    if canon(CHILD_V | (1 << b)) in folded_d4:
        census.append((b, "WIN7" if bit_recs.get(b, {}).get("loss") is True
                       else "REFUTED"))
assert census == [], census
raw_hits = sorted(b for b in WIN_BITS
                  if (CHILD_V | (1 << b)) in folded)
d4_hits = sorted(b for b in WIN_BITS
                 if canon(CHILD_V | (1 << b)) in folded_d4)
assert raw_hits == [] and d4_hits == []
assert len({canon(CHILD_V | (1 << b)) for b in WIN_BITS}) == 3
assert tmap[39]["root_canon"] not in folded_d4
assert tmap[72]["root_canon"] not in folded_d4
assert tmap[107]["root_canon"] not in folded_d4
print("CONTROL conflict census: all 64 candidate D4 orbits are disjoint "
      "from the 757 distinct folded roots (743 D4 canons) at 1435 - zero "
      "overlaps, zero WIN/LOSS conflicts; the 3 receipt roots are 3 "
      "distinct D4 orbits, disjoint raw-hex and D4-canonically from every "
      "folded root")

# ---------- 6. the child genuinely remains open at 1435 ------------------
assert CHILD_V in manifest and CHILD_V not in s_1435
for h, exp_rows, exp_cost in ((PARENT_SH, 31, 2145),
                              (PARENT_2, 43, 3167)):
    rows = rem_1435.get(h, [])
    assert classes.get(h, 0) == 2, h
    assert len(rows) == exp_rows and \
        sum(int(r["s6_s7_edge_cost"]) for r in rows) == exp_cost, h
    ch = [r for r in rows if int(r["s6_hex"], 16) == CHILD_V]
    assert len(ch) == 1 and int(ch[0]["s6_s7_edge_cost"]) == 64, h
d = dem_1435.get(CHILD)
assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 0), d
print("CONTROL the child genuinely remains at head 1435: both direct open "
      "class-2 parents hold the child row (shared 31/2145, second 43/3167) "
      "at edge cost 64, dual demand c1=0,c2=2,c4=0")

# ---------- 7. fold the 3 receipts on 1435 in publication order ----------
s_cur = set(s_1435)
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
        "source": ("cost-64f raw batches 1-8 (v16) + the published "
                   "head-1435 v2 presweep transfer census"),
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
assert child_closed_by == 39, child_closed_by
assert zero_mim == ZERO_MIM, zero_mim
cov_all = set()
for bit in WIN_BITS:
    cov_all |= covers(CHILD_V | (1 << bit))
assert s_cur == s_1435 | cov_all, \
    "set-equality: s_after == s_1435 UNION covers(3 roots)"
total_marg = sum(a["marginal"] for a in addition)
total_mim = sum(a["marginal_in_manifest"] for a in addition)
assert (total_marg, total_mim) == (15, 3)
st_after, rem_after, uniq_after, dem_after = summary_state(s_cur)
assert (st_after["solved_s6_in_manifest"], st_after["remaining_s5_orbits"],
        st_after["unique_remaining_s6"], st_after["sum_remaining_cost"],
        st_after["s6_needed_by_open_classes"],
        st_after["cost_needed_by_open_classes"]) == PINNED_AFTER, st_after
assert st_after["solved_s6_in_manifest"] == 1435 + total_mim
assert st_after["hist"] == PINNED_HIST, st_after["hist"]
print("AFTER cost-64f fold:", json.dumps(st_after, indent=1))
print(f"total marginal={total_marg} marginal_in_manifest={total_mim}; "
      f"zero-mim receipts: {zero_mim}; child closed by bit: "
      f"{child_closed_by}")

# ---------- 8. per-parent rows at the new head --------------------------
parents_after = {}
lost_detail = {}
cov_hexes = {f"{k:032x}" for k in cov_all}
for h in sorted(PINNED_PARENTS):
    old_exp, new_exp = PINNED_PARENTS[h]
    old = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1435[h]}
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
assert sum(len(v) for v in lost_detail.values()) == 7, \
    "7 parent-row incidences"
assert sum(sum(v.values()) for v in lost_detail.values()) == 455
closed_hexes = {f"{k:032x}" for k in union_base}
for h, lost in lost_detail.items():
    assert set(lost) <= closed_hexes, h
# cross-check against the published audit's affected_parent_deltas
audit_par = {e["s5_hex"]: e for e in audit["affected_parent_deltas"]}
assert sorted(audit_par) == sorted(PINNED_PARENTS)
for h, e in audit_par.items():
    assert (e["before_rows"], e["before_parent_edge_cost"],
            e["lost_rows"], e["lost_parent_edge_cost"],
            e["after_rows"], e["after_parent_edge_cost"]) == \
        (PINNED_PARENTS[h][0][0], PINNED_PARENTS[h][0][1],
         len(lost_detail[h]), sum(lost_detail[h].values()),
         PINNED_PARENTS[h][1][0], PINNED_PARENTS[h][1][1]), h
    assert classes.get(h, 0) == e["classes_mask"], h
print("per-parent rows at the new head (touched parents): " + "; ".join(
    f"{k} {v['rows_before']}/{v['edge_cost_before']} -> "
    f"{v['rows']}/{v['edge_cost']}" for k, v in parents_after.items()))

# ---------- 9. the 3 rows actually closed; demand invariants -----------
s_hex = {f"{k:032x}" for k in s_cur}
for row_hex in UNION3:
    assert row_hex in s_hex, (row_hex, "must be closed by the fold")
    dd = dem_1435.get(row_hex)
    assert dd["c1"] == 0 and (dd["c2"] + dd["c4"]) > 0, (row_hex, dd)
assert CHILD in s_hex
assert int(f"{CHILD_V:032x}", 16) == CHILD_V
dd = dem_1435[CHILD]
assert (dd["c1"], dd["c2"], dd["c4"]) == (0, 2, 0), dd
dd = dem_1435["00000000000000a09002000000002000"]
assert (dd["c1"], dd["c2"], dd["c4"]) == (0, 2, 2), dd
dd = dem_1435["00000000020002801002000000080000"]
assert (dd["c1"], dd["c2"], dd["c4"]) == (0, 0, 2), dd

# ---------- 10. rankings at the new head -------------------------------


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
    "schema": "n11-class-frontier-cost64f-receipts-20261116-v1",
    "date": "2026-11-16",
    "baseline_record": {
        "cost64d_head_1435": "1435/174/6413/507337/4686/371251 "
                            "(reproduced byte-identically by runpy of the "
                            "published cost-64d fold script)",
        "claim": "class2-lane-cost64f-inflight-20261116.json (v5, git blob "
                 f"sha {CLAIM_BLOB}; supersedes the v4 counter-corrected "
                 "completed NOT-STERILE claim blob "
                 "b9d0f9fa714237ca5f7cfffcedc2d7917fee8eb3 (61 REFUTED-D10 "
                 "= 56 swept + 5 transferred) which superseded the v3 "
                 "parent-metadata-corrected claim blob "
                 "5159e0ac0ba9591e95ee6a9ab7a01aeb9e899f6e; all "
                 "v1/v2/v3/v4 fields preserved)",
        "sweep": "8 raw batch JSONLs (v16), all blob-pinned; 64 "
                 "candidates = 3 WIN7-D10 + 56 REFUTED-D10 swept + 5 "
                 "REFUTED-D10 transferred (D4-canonical identity, "
                 "published head-1435 v2 presweep), 0 capped, "
                 f"{SWEEP_NODES_TOTAL} nodes + 8 pilots x {PILOT_NODES}; "
                 "determinism rerun batch2 node-exact; v15 crosscheck "
                 "two-directional",
        "presweep_v2": "class2-lane-next-target-presweep-1435-v2-20261116."
                       f"json (git blob sha {PRESWEEP_V2_BLOB})",
        "parent_and_marginal_audit":
            "class2-lane-cost64f-parent-and-marginal-audit-20261116.json "
            f"(git blob sha {AUDIT_BLOB})",
    },
    "method": "runpy reproduction of the published cost-64d fold script "
              "(whole-chain head 1435), re-derivation of the cost-64f "
              "sweep from the 8 blob-pinned raw batches plus the 5 "
              "blob-pinned pre-sweep transferred REFUTED verdicts, "
              "re-assertion of the published parent-and-marginal audit "
              "(sequential per-receipt in-manifest marginals in "
              "publication order on the 1435 baseline), "
              "re-assertion of all 3 win3 certificates byte-for-byte "
              "(whole/parts blob pins, join receipts, sorted-unique rows, "
              "root mobility == legal_candidates.py, BigInt union 0/0 + "
              "Bareiss records), 64-candidate-orbit conflict census vs the "
              "folded roots (zero overlaps), the child-remaining fact "
              "asserted on both direct open parents, then the 3 receipts "
              "folded in publication order with per-receipt marginals "
              "pinned and a set-equality control",
    "cost64f_additions_on_cost64d_1435": addition,
    "totals": {
        "receipts": 3,
        "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "child_closed_by_bit": child_closed_by,
        "zero_mim_receipts": zero_mim,
        "transferred_refuted_bits": TRANSFERRED_BITS,
        "conflict_census_overlaps": census,
        "folded_roots_at_1435": {"receipt_roots": 757,
                                 "distinct_roots": 757,
                                 "distinct_d4_canons": 743},
        "rows_closed_hexes": UNION3,
        "sweep_nodes_excluding_pilots": SWEEP_NODES_TOTAL,
        "parent_row_incidences": 7,
        "parent_edge_cost_delta": 455,
    },
    "frontier_after_cost64f": {
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
(OUT / "class-frontier-cost64f-receipts-recompute-20261116.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-cost64f-receipts-recompute-20261116.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"])
                                    for r in rows)}
     for k, rows in rem_after.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / ("class-frontier-s5-ranking-after-cost64f-receipts-"
             "20261116.csv")).open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits",
                "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / ("class-frontier-top-candidates-s6-after-cost64f-receipts-"
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
print("written ranking + top-candidates CSVs (after-cost64f-receipts)")

for p in ("class-frontier-cost64f-receipts-recompute-20261116.json",
          "class-frontier-s5-ranking-after-cost64f-receipts-20261116.csv",
          "class-frontier-top-candidates-s6-after-cost64f-receipts-"
          "20261116.csv",
          "class2-lane-cost64f-inflight-20261116.json",
          "class2-lane-cost64f-win3-certificates-20261116.json"):
    sha, blen = git_blob_sha(OUT / p)
    print(f"blob {p}: {sha} ({blen} bytes)")
