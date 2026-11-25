#!/usr/bin/env python3
"""Independent agreement verification of the published cost-64h v15
REFUTED cross-engine check (5 raw JSONL shards a-e + verification record,
commit ae7e583709, 2026-11-16T13:57:39Z) against a fully independent
re-derivation in this fresh environment.

The published record cross-checks the 41 REFUTED-D10 bits of the cost-64h
sweep with the independent v15 engine and additionally re-runs two WIN
control bits (4 and 120) node-exactly against the earlier published v15
win crosscheck. This second-implementation lane re-derives everything
from the byte-pinned shards and the published v16 raw batches:

  1. blob-verify the 5 shard files and the verification record against
     the main directory listing (pins below);
  2. re-derive the 41-bit REFUTED set from the published v16 raw batches
     (8 shards, blob-pinned in the published claim v2);
  3. check the shard contents: 41 REFUTED bits each loss=false uncapped
     andclose=true terminal range 13-17, 2 WIN controls loss=true,
     5/5 pilot_d6 records at exactly 5949 nodes, no duplicate bits,
     bit set = 41 REFUTED + {4, 120};
  4. WIN controls node-exact against the published v15 win crosscheck
     (bit4: 3,555,878 / bit120: 4,836,378);
  5. cross-check every field of the published verification record
     (8/8 checks true, 41/41 per-bit verdict+node agreement,
     refuted node sum 57,767,631, total incl. controls 66,159,887).

Bookkeeping verification only; no engine search was run and no verdict
was created. REFUTED-D10 is not a LOSS proof; WIN7 certificates prove a
first-player win within depth 10 from the individual 7-stone roots only;
the 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and
classes 1/2/4 remain UNKNOWN.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
sys.path.insert(0, str(HERE / "scripts"))
from fold_projection_head1450_tool_20261116 import git_blob_sha  # noqa: E402

SHARDS = {s: f"class2-lane-cost64h-v15-refuted-crosscheck-{s}-20261116.jsonl"
          for s in "abcde"}
PINS = {
    **SHARDS,
    "class2-lane-cost64h-v15-refuted-crosscheck-verification-20261116.json":
        "cc410c888fe38cb109daf4ceabc45022d89838c1",
}
SHARD_BLOBS = {
    "a": "311ba6c95750e4b589464725b59bd75181342b43",
    "b": "2b54730ecd78c48d63f00768babeae77682a2dd6",
    "c": "e1a48b96de4a0db79780e1172617e6e57bdc313b",
    "d": "b06433e3bb61df65ed773ca60356c81d042d2381",
    "e": "de33012ee9bd96eabaa8662d5c9fd7cadb393093",
}
V15_WIN_CROSSCHECK = "class2-lane-cost64h-v15-crosscheck-20261116.jsonl"
V15_WIN_BLOB = "0d32c2a0f5411d455f5b1503bc37c95c58f0b155"
CLAIM_JSON = "class2-lane-cost64h-inflight-20261116.json"
CLAIM_BLOB = "68e4878094b78eaf0a465033d0289a6db5d94861"
WIN_CONTROLS = [4, 120]
CONTROL_NODES = {4: 3555878, 120: 4836378}
REFUTED_NODE_SUM = 57767631
TOTAL_NODE_SUM = 66159887


def load_jsonl(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def main():
    checks = {}
    # ---- 1. blob pins -----------------------------------------------------
    for s, blob in SHARD_BLOBS.items():
        assert git_blob_sha((OUT / SHARDS[s]).read_bytes()) == blob, s
    vpath = ("class2-lane-cost64h-v15-refuted-crosscheck-verification"
             "-20261116.json")
    assert git_blob_sha((OUT / vpath).read_bytes()) == PINS[vpath]
    pins_verified = len(SHARD_BLOBS) + 1
    checks["C1_blob_pins"] = pins_verified
    claim = json.loads((OUT / CLAIM_JSON).read_text())
    assert git_blob_sha((OUT / CLAIM_JSON).read_bytes()) == CLAIM_BLOB
    raw_pins = {p.rsplit("/", 1)[-1]: s
                for p, s in claim["published_artifacts"]["raw_batches"]}
    assert git_blob_sha((OUT / V15_WIN_CROSSCHECK).read_bytes()) == V15_WIN_BLOB
    for name, blob in raw_pins.items():
        assert git_blob_sha((OUT / name).read_bytes()) == blob, name
    checks["C2_claim_and_raw_batch_pins"] = len(raw_pins) + 2

    # ---- 2. re-derive the 41-bit REFUTED set from the v16 raw batches ----
    ref_v16 = {}
    for name in sorted(raw_pins):
        if "raw-batch" not in name:
            continue
        for d in load_jsonl(OUT / name):
            if "control" not in d:
                assert d["bit"] not in ref_v16
                ref_v16[d["bit"]] = d
    refuted_bits = sorted(b for b, r in ref_v16.items() if r["loss"] is False)
    assert len(refuted_bits) == 41
    assert sorted(b for b, r in ref_v16.items() if r["loss"] is True) == \
        [4, 6, 8, 33, 38, 42, 44, 49, 68, 74, 76, 77, 78, 79, 83, 89, 91,
         101, 109, 113, 114, 116, 120]
    checks["C3_v16_refuted_set"] = refuted_bits

    # ---- 3. shard contents ----------------------------------------------
    recs, pilots = [], 0
    for s in "abcde":
        for d in load_jsonl(OUT / SHARDS[s]):
            if "control" in d:
                assert d == {"control": "pilot_d6", "loss": False,
                            "nodes": 5949, "capped": False}, d
                pilots += 1
            else:
                recs.append(d)
    assert pilots == 5
    by_bit = {}
    for r in recs:
        assert r["bit"] not in by_bit
        by_bit[r["bit"]] = r
    assert sorted(by_bit) == sorted(refuted_bits + WIN_CONTROLS)
    for b in refuted_bits:
        r = by_bit[b]
        assert r["loss"] is False and r["capped"] is False
        assert r["andclose"] is True
        assert r["terminalStoneRange"] == [13, 17]
    ref_node_sum = sum(by_bit[b]["nodes"] for b in refuted_bits)
    assert ref_node_sum == REFUTED_NODE_SUM
    assert sum(r["nodes"] for r in recs) == TOTAL_NODE_SUM
    checks["C4_shard_contents"] = {
        "refuted": 41, "win_controls": 2, "pilots": pilots,
        "refuted_node_sum": ref_node_sum,
        "total_node_sum_incl_controls": TOTAL_NODE_SUM}

    # ---- 4. WIN controls node-exact vs the published v15 win crosscheck ---
    v15win = {d["bit"]: d for d in load_jsonl(OUT / V15_WIN_CROSSCHECK)
              if "control" not in d}
    for b in WIN_CONTROLS:
        r = by_bit[b]
        assert r["loss"] is True and r["capped"] is False
        assert r["andclose"] is True
        assert r["terminalStoneRange"] == [13, 17]
        assert r["nodes"] == v15win[b]["nodes"] == CONTROL_NODES[b]
    checks["C5_win_controls_node_exact"] = {
        str(b): by_bit[b]["nodes"] for b in WIN_CONTROLS}

    # ---- 5. cross-check the published verification record ----------------
    v = json.loads((OUT / vpath).read_text())
    for k, val in v["checks"].items():
        assert val is True, (k, val)
    assert sorted(v["refuted_bits"]) == refuted_bits
    assert v["win_control_bits"] == WIN_CONTROLS
    assert v["v15_refuted_node_sum"] == ref_node_sum
    assert v["claim_v2_blob"] == CLAIM_BLOB
    assert len(v["per_bit"]) == 41
    for pb in v["per_bit"]:
        b = pb["bit"]
        assert pb["verdict_agreement"] is True
        assert pb["v15"]["loss"] == by_bit[b]["loss"] is False
        assert pb["v15"]["capped"] == by_bit[b]["capped"] is False
        assert pb["v15"]["nodes"] == by_bit[b]["nodes"]
        assert pb["v16_published"]["loss"] == ref_v16[b]["loss"] is False
        assert pb["v16_published"]["capped"] == ref_v16[b]["capped"] is False
        assert pb["v16_published"]["nodes"] == ref_v16[b]["nodes"]
    for b in WIN_CONTROLS:
        c = v["win_control_detail"][str(b)]
        assert c["loss"] is True and c["capped"] is False
        assert c["node_exact_vs_published_v15"] is True
        assert c["published_nodes"] == c["rerun_nodes"] == CONTROL_NODES[b]
    checks["C6_published_record_crosscheck"] = len(v["checks"])
    print(f"CONTROL {pins_verified} shard/record pins + "
          f"{len(raw_pins) + 2} claim/batch pins blob-verified; "
          "41/41 REFUTED verdict+node agreement, win controls node-exact")

    result = {
        "schema": "n11-class2-lane-cost64h-v15-refuted-crosscheck-"
                  "independent-agreement-20261116-v1",
        "date": "2026-11-16",
        "role": ("second-implementation agreement check of the published "
                 "v15 REFUTED cross-engine check (commit ae7e583709): this "
                 "lane re-derived the 41-bit REFUTED set from the published "
                 "v16 raw batches and verified the 5 shards, the 2 WIN "
                 "controls and every field of the published verification "
                 "record in a fresh environment"),
        "published_record": {
            "verification_json": vpath,
            "git_blob_sha": PINS[vpath],
            "git_commit": "ae7e58370929edb0c9a31e4d0570ce933127b797",
            "shard_blob_shas": SHARD_BLOBS},
        "rederivation": {
            "refuted_bits_41": refuted_bits,
            "win_control_bits": WIN_CONTROLS,
            "pilots": pilots,
            "refuted_node_sum": ref_node_sum,
            "total_node_sum_incl_controls": TOTAL_NODE_SUM,
            "win_control_nodes": {str(b): CONTROL_NODES[b]
                                  for b in WIN_CONTROLS}},
        "checks": checks,
        "interpretation_guard": ("bookkeeping verification only; no engine "
                                 "search was run and no verdict was "
                                 "created; REFUTED-D10 is not a LOSS proof; "
                                 "WIN7 certificates prove a first-player "
                                 "win within depth 10 from the individual "
                                 "7-stone roots only; the 11x11 empty "
                                 "board, two-stone roots {49,60} and "
                                 "{59,60}, S2 {59,60} and classes 1/2/4 "
                                 "all remain UNKNOWN"),
    }
    out_path = OUT / ("class2-lane-cost64h-v15-refuted-crosscheck-"
                      "independent-agreement-20261116.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote", out_path.name, "blob",
          git_blob_sha(out_path.read_bytes())[:12])
    print("ALL CONTROLS PASS")


if __name__ == "__main__":
    main()
