#!/usr/bin/env python3
# Cross-lane agreement check for the cost73k fresh v17 depth-10 sweep
# (2026-11-17). Compares the claiming lane's published raw batch JSONLs
# (this repository) against the concurrent-session sweep record published
# at commit 8803a3b0 (git blob 0cba988e2a65e9195b0a0e6a3168a518e27079fb),
# per the record's next_action.
#
# Both sessions ran the same deterministic engine (class4_child1_runner_v17,
# blob c132cc6425eee3feaeef1d697dd74f968cfedb59, depth 10, cap 1e9 per bit,
# andclose 1, fresh engine state per candidate bit) over the same 73
# candidate bits of child 00000000000000801206000000000400, with different
# batch groupings. Fresh runs are node-deterministic, so every per-bit
# (loss, nodes, capped) triple must agree.
#
# Usage:
#   python3 check_cost73k_cross_lane_agreement_20261117.py <record.json> <output_dir>
# The record bytes are verified against the pinned blob before use.
import hashlib, json, sys, pathlib

RECORD_BLOB = "0cba988e2a65e9195b0a0e6a3168a518e27079fb"
CHILD = "00000000000000801206000000000400"
ENGINE_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
CLAIM_V2_SCHEMA = "n11-class2-lane-cost73k-inflight-20261117-v2"
RAW_BATCHES = [
    "class2-lane-cost73k-raw-batch1-20261117.jsonl",
    "class2-lane-cost73k-raw-batch2-20261117.jsonl",
    "class2-lane-cost73k-raw-batch3-20261117.jsonl",
    "class2-lane-cost73k-raw-batch4-20261117.jsonl",
    "class2-lane-cost73k-raw-batch5-20261117.jsonl",
    "class2-lane-cost73k-raw-batch6-20261117.jsonl",
    "class2-lane-cost73k-raw-batch7-20261117.jsonl",
    "class2-lane-cost73k-raw-batch8-20261117.jsonl",
    "class2-lane-cost73k-raw-batch9-confirmation-20261117.jsonl",
]

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def main() -> None:
    record_path = pathlib.Path(sys.argv[1])
    out_dir = pathlib.Path(sys.argv[2])
    rb = record_path.read_bytes()
    rec_sha = git_blob_sha(rb)
    assert rec_sha == RECORD_BLOB, f"record blob mismatch: {rec_sha}"
    rec = json.loads(rb.decode("utf-8"))
    assert rec["schema"] == "n11-class2-lane-cost73k-concurrent-session-sweep-record-20261117-v1"
    assert rec["sweep_execution"]["child"] == CHILD
    assert rec["sweep_execution"]["engine"].startswith("class4_child1_runner_v17.ts")
    assert ENGINE_BLOB in rec["sweep_execution"]["engine"]

    # Rebuild the claiming lane's per-bit table from the raw batch JSONLs.
    mine, pilots = {}, 0
    batch_of = {}
    for i, fname in enumerate(RAW_BATCHES, start=1):
        for line in (out_dir / fname).read_text().splitlines():
            r = json.loads(line)
            if r.get("control"):
                assert r["control"] == "pilot_d6" and r["nodes"] == 3402 \
                    and r["loss"] is False and r["capped"] is False, (fname, r)
                pilots += 1
                continue
            bit = r["bit"]
            assert bit not in mine, f"duplicate bit {bit}"
            mine[bit] = {"loss": r["loss"], "nodes": r["nodes"], "capped": r["capped"]}
            batch_of[bit] = i
    assert pilots == 9, pilots
    assert len(mine) == 73, len(mine)

    theirs = {int(k): v for k, v in rec["verdicts"]["per_bit"].items()}
    assert len(theirs) == 73, len(theirs)
    assert set(mine) == set(theirs), \
        (sorted(set(mine) ^ set(theirs)))

    mismatches = []
    for bit in sorted(mine):
        a, b = mine[bit], theirs[bit]
        if (a["loss"], a["nodes"], a["capped"]) != (b["loss"], b["nodes"], b["capped"]):
            mismatches.append(bit)
    assert not mismatches, f"per-bit mismatches: {mismatches}"

    my_win = sorted(b for b in mine if mine[b]["loss"])
    my_refuted = sorted(b for b in mine if not mine[b]["loss"])
    assert my_win == sorted(rec["verdicts"]["win7_d10_bits"]), "win set mismatch"
    assert my_refuted == sorted(rec["verdicts"]["refuted_d10_bits"]), "refuted set mismatch"
    assert len(my_win) == 25 and len(my_refuted) == 48

    my_win_nodes = {str(b): mine[b]["nodes"] for b in my_win}
    assert my_win_nodes == rec["verdicts"]["win7_d10_nodes"], "win node dict mismatch"

    node_sum = sum(mine[b]["nodes"] for b in mine)
    assert node_sum == rec["sweep_execution"]["candidate_nodes_total"] == 128861941, node_sum
    assert node_sum + 9 * 3402 == rec["sweep_execution"]["total_nodes_including_pilots"] == 128892559

    # Batch grouping intentionally differs between the sessions; record it.
    # The claiming lane ran 66 open bits (7x9 + 1x3) + 7 confirmation bits,
    # the concurrent session 67 open bits (7x9 + 1x4) + 6 confirmation bits,
    # so most bits sit in a different batch index; only the per-bit engine
    # results are part of the determinism claim, not the grouping.
    their_batch = {b: v["batch"] for b, v in theirs.items()}
    diff_bits = sorted(b for b in mine if their_batch[b] != batch_of[b])
    # sanity: every batch index in both groupings is a known 1..9 batch
    assert all(1 <= v <= 9 for v in batch_of.values()), "bad batch index (mine)"
    assert all(1 <= v <= 9 for v in their_batch.values()), "bad batch index (theirs)"
    # bit 14: mine ran as a confirmation bit (batch 9), theirs as an open bit
    # (batch 1); bits 23/26/34/53/55/107 ran as confirmation bits in both
    assert batch_of[14] == 9 and their_batch[14] == 1
    for b in (23, 26, 34, 53, 55, 107):
        assert batch_of[b] == 9 and their_batch[b] == 9, b

    # Confirmation bits: 7/7 fresh outcomes already recorded in the record;
    # the claiming lane's raw batches agree bit-exactly with them.
    conf = rec["confirmation_agreement"]["census_v7_claim_predictions"]
    assert set(int(k) for k in conf) == {14, 23, 26, 34, 53, 55, 107}
    for k, verdict in conf.items():
        b = int(k)
        got_win = mine[b]["loss"]
        assert (verdict == "WIN7-D10") == got_win, (b, verdict)

    theirs_by_batch = {}
    for b in theirs:
        theirs_by_batch.setdefault(theirs[b]["batch"], []).append(b)

    out = {
        "schema": "n11-class2-lane-cost73k-cross-lane-agreement-20261117-v1",
        "status": ("PASS: the claiming lane's published raw batch JSONLs agree with the "
                   "concurrent-session sweep record on every per-bit verdict, node count "
                   "and capped flag (73/73), on the 25 WIN7-D10 / 48 REFUTED-D10 "
                   "partition, on the per-WIN node table, on the node sums and on the "
                   "7/7 census-v7 confirmation outcomes"),
        "compared": {
            "claiming_lane_raw_batches": RAW_BATCHES,
            "claiming_lane_claim": ("class2-lane-cost73k-inflight-20261117.json claim v2 "
                                    "(schema " + CLAIM_V2_SCHEMA + ")"),
            "concurrent_session_record": ("class2-lane-cost73k-concurrent-session-sweep-"
                                         "record-20261117.json, git blob " + RECORD_BLOB +
                                         ", commit 8803a3b0"),
            "engine_common": ("class4_child1_runner_v17.ts, git blob " + ENGINE_BLOB +
                              ", depth 10, cap 1e9 per bit, andclose 1, fresh engine "
                              "state per candidate bit; both sessions ran fresh "
                              "executions from source, no shared cache or state"),
        },
        "agreement": {
            "per_bit_triples_loss_nodes_capped": "73/73 identical",
            "win7_d10_bits": my_win,
            "win7_d10_count": 25,
            "refuted_d10_bits": my_refuted,
            "refuted_d10_count": 48,
            "capped_count": 0,
            "win_node_table_identical": True,
            "candidate_nodes_total": node_sum,
            "total_nodes_including_pilots": node_sum + 9 * 3402,
            "pilot_controls": "9/9 batches on the claiming lane, pilot_d6 exact 3402; the "
                              "record states 9/9 as well",
            "confirmation_bits_census_v7": {str(b): ("WIN7-D10" if mine[b]["loss"] else
                                                      "REFUTED-D10")
                                            for b in (14, 23, 26, 34, 53, 55, 107)},
            "confirmation_agreement": "7/7",
        },
        "batch_grouping_difference": {
            "note": ("the two sessions grouped the same 73 bits into batches "
                      "differently; batch grouping is not part of the engine "
                      "determinism claim, and the differing bits are listed "
                      "explicitly"),
            "claiming_lane_batches": {str(i): sorted(b for b in mine if batch_of[b] == i)
                                      for i in range(1, 10)},
            "concurrent_session_batches": "see batch_grouping_counts below",
            "bits_assigned_differently": diff_bits,
            "batch_grouping_counts": {
                "claiming_lane": {str(i): sum(1 for b in mine if batch_of[b] == i)
                                  for i in range(1, 10)},
                "concurrent_session": {str(i): sum(1 for b in theirs if their_batch[b] == i)
                                      for i in range(1, 10)},
            },
        },
        "scope_guard": ("this agreement shows two independent fresh executions of the "
                        "same deterministic engine produced identical per-bit results; "
                        "it is not an independent re-derivation of the verdicts and "
                        "closes no manifest row; WIN7-D10 proves a first-player win "
                        "within depth 10 from each individual 7-stone root only; "
                        "REFUTED-D10 is not a LOSS proof; the receipt fold stays "
                        "pending; 11x11 remains UNKNOWN"),
    }
    out["batch_grouping_difference"]["concurrent_session_batches"] = {
        str(k): sorted(v) for k, v in theirs_by_batch.items()}

    dst = out_dir / "class2-lane-cost73k-cross-lane-agreement-20261117.json"
    text = json.dumps(out, indent=1, ensure_ascii=True) + "\n"
    dst.write_text(text)
    print(f"agreement JSON written: {dst} ({len(text)} bytes)")
    print("blob:", git_blob_sha(text.encode()))

if __name__ == "__main__":
    main()
