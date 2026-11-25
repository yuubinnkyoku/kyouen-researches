#!/usr/bin/env python3
# claim v2 updater for class2-lane cost73k (2026-11-17)
# v1 -> v2: in-flight claim advanced to sweep-complete. The original claiming
# session's local raw files were lost to a sandbox reset before publication,
# so the published raw batch JSONLs are a fresh regeneration (a third
# independent execution of the same pinned engine source, see the batch
# driver scripts/ev73k_batches_20261117.sh). The regeneration passed every
# planned control and matches the concurrent-session sweep record per-bit
# (73/73) and a third session's record-level consistency audit (PASS).
# Certificates: pending.
import hashlib, json, sys, pathlib

V1_BLOB_SHA = "a24d3557ef23a279cc08c2d578e420f676f28f05"
RECORD_BLOB = "0cba988e2a65e9195b0a0e6a3168a518e27079fb"
RECORD_AUDIT_BLOB = "f1de8b915595ccf697f79d1e8e3398665aeebe2c"
CENSUS_V7_BLOB = "68246f3263fe6cbb49ffafa866f73b49cf3c2ebb"

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def main() -> None:
    src = sys.argv[1]  # claim v1 json (published blob)
    dst = sys.argv[2]  # claim v2 json output
    raw_dir = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else pathlib.Path(src).parent
    raw = pathlib.Path(src).read_bytes()
    sha = git_blob_sha(raw)
    if sha != V1_BLOB_SHA:
        sys.exit(f"FATAL: input is not the published claim v1 blob (got {sha})")
    d = json.loads(raw.decode("utf-8"))
    assert d["schema"] == "n11-class2-lane-cost73k-inflight-20261117-v1"

    audit_blob = git_blob_sha((raw_dir /
        "class2-lane-cost73k-raw-sweep-audit-20261117.json").read_bytes())
    agree_blob = git_blob_sha((raw_dir /
        "class2-lane-cost73k-cross-lane-agreement-20261117.json").read_bytes())

    d["schema"] = "n11-class2-lane-cost73k-inflight-20261117-v2"
    d["last_updated"] = "2026-11-17"
    d["status"] = (
        "claim v2: sweep complete; the fresh v17 73-bit depth-10 sweep of the census v7 "
        "rank-1 row finished 25 WIN7-D10 bits [0,7,11,14,15,26,35,39,41,44,55,58,62,73,"
        "76,87,89,94,95,97,98,103,105,112,117] (22 sweep WIN + 3 confirmation WIN) + 48 "
        "REFUTED-D10, 0 capped (128,861,941 candidate nodes + 9 pilot controls at 3,402 "
        "nodes each; 9/9 pilots exact, determinism reruns of batches 1 and 7 "
        "field-identical on every non-ms field, independent v15 cross-engine re-check "
        "25/25 WIN agreement via a/b/c (22 sweep WIN bits) + d (3 confirmation WIN "
        "bits), 4/4 pilots 5,949 exact, 0 capped, v15 node total 116,892,833, 7/7 "
        "census-v7 confirmation bits matching the predicted verdicts (3 WIN7-D10: bit 14 "
        "= cost73j bit 110, bit 26 = cost73i bit 110, bit 55 = cost69j bit 110; 4 "
        "REFUTED-D10: bit 23 = 64d bit 110 pre-64h harvest, bit 34 = cost72d bit 110, "
        "bit 53 = cost66i bit 10 raw-identical (identical absolute root hex and node "
        "count 39,808), bit 107 = cost71e bit 110; six sources verified against their "
        "published raw/audit files, see the raw sweep audit); provenance: the original "
        "claiming session's local raw files were lost to a sandbox reset before "
        "publication, so the raw batch JSONLs published with this claim are a fresh "
        "regeneration from the pinned engine source (a third independent execution, "
        "driver scripts/ev73k_batches_20261117.sh); a concurrent session had "
        "independently run the same 73-bit fresh v17 sweep (concurrent-session sweep "
        "record, git blob 0cba988e2a65e9195b0a0e6a3168a518e27079fb, commit 8803a3b0, "
        "different batch grouping) and the cross-lane agreement check found the "
        "published raw batches identical to that record on every per-bit verdict, node "
        "count and capped flag (73/73, class2-lane-cost73k-cross-lane-agreement-"
        "20261117.json), with a third-session record-level consistency audit PASS (git "
        "blob f1de8b915595ccf697f79d1e8e3398665aeebe2c, commit 0274a2ef); stdlib raw "
        "audit all checks passed (class2-lane-cost73k-raw-sweep-audit-20261117.json); "
        "the 22 sweep WIN7-D10 roots go to blind certificate extraction and "
        "independent engine-free verification before publication (certificates pending, "
        "this claim does not publish them; the 3 confirmation WIN roots are already "
        "covered by the published 73j/73i/69j certificates); the receipt fold stays "
        "pending behind the 76c/66i/66j/69j/71e/72d/73i folds; no manifest row is "
        "closed by this claim; 11x11 UNKNOWN"
    )
    d["actual_execution"] = {
        "started": "2026-11-17",
        "engine": ("class4_child1_runner_v17.ts (v17, blob "
                   "c132cc6425eee3feaeef1d697dd74f968cfedb59), depth 10, cap 1e9 per "
                   "bit, andclose 1, fresh engine state per candidate bit"),
        "provenance": ("the original claiming session completed the sweep (execution A) "
                       "but its local raw files were lost to a sandbox reset before "
                       "publication; a concurrent session independently ran the same "
                       "sweep (execution B, published per-bit record, commit 8803a3b0); "
                       "the raw files published with this claim are a fresh "
                       "regeneration (execution C) driven by scripts/"
                       "ev73k_batches_20261117.sh from the pinned engine source; "
                       "executions A, B and C agree on every per-bit non-ms field "
                       "(C vs B verified 73/73 in the published cross-lane agreement "
                       "check)"),
        "batches_run": 9,
        "pilot_controls": "9/9 batches: pilot_d6 exact {loss=false, nodes=3402, capped=false}",
        "results": {
            "win7_d10_bits": [0, 7, 11, 14, 15, 26, 35, 39, 41, 44, 55, 58,
                              62, 73, 76, 87, 89, 94, 95, 97, 98, 103, 105,
                              112, 117],
            "win7_d10_nodes": {
                "0": 2105074, "7": 3010263, "11": 1066114, "14": 2316193,
                "15": 3718618, "26": 4563004, "35": 2901076, "39": 591964,
                "41": 839318, "44": 1743886, "55": 2207258, "58": 1872967,
                "62": 654959, "73": 2742442, "76": 1860230, "87": 2732579,
                "89": 1245153, "94": 1225545, "95": 2429062, "97": 1726126,
                "98": 2145334, "103": 2450696, "105": 1703526, "112": 2273492,
                "117": 2731534
            },
            "refuted_d10_bits_count": 48,
            "capped_count": 0,
            "candidate_nodes_total": 128861941,
            "total_nodes_including_pilots": 128892559,
            "terminal_stone_range": [13, 17]
        },
        "confirmation_outcome": ("7/7 as predicted by the census v7 ten-map "
                                 "overlay (3 WIN7-D10: bit 14 = cost73j bit "
                                 "110, bit 26 = cost73i bit 110, bit 55 = "
                                 "cost69j bit 110; 4 REFUTED-D10: bit 23 = "
                                 "64d bit 110 pre-64h harvest, bit 34 = "
                                 "cost72d bit 110, bit 53 = cost66i bit 10 "
                                 "(raw-identical, identical node count 39,808), "
                                 "bit 107 = cost71e bit 110); the other six "
                                 "transfer sources are canon-equal only "
                                 "(verdict-level agreement, node counts may "
                                 "differ by labeling)"),
        "determinism_rerun": ("batches 1 (WIN bits 0, 7, 11, 15 and the "
                              "heaviest search bit 6, 4,683,949 nodes) and 7 "
                              "(WIN bits 103, 105, 112 and the heaviest search "
                              "bit 111, 7,826,307 nodes) re-run in separate "
                              "processes: field-identical on every non-ms "
                              "field"),
        "v15_crosscheck": ("independent v15 engine (blob "
                           "8744fc65b6b7cac6bd561403ce4c749e01c51359) re-check of "
                           "all 25 WIN bits (a/b/c: the 22 sweep WIN bits split "
                           "8+7+7; d: the 3 confirmation WIN bits): 25/25 loss=true, "
                           "4/4 pilots 5949 exact, 0 capped, node total 116,892,833 "
                           "(equal to the concurrent-session record's v15 total)"),
        "cross_session_agreement": {
            "concurrent_session_record": ("class2-lane-cost73k-concurrent-session-sweep-"
                                          "record-20261117.json, git blob "
                                          "0cba988e2a65e9195b0a0e6a3168a518e27079fb, "
                                          "commit 8803a3b0: a concurrent session ran the "
                                          "same full 73-bit fresh v17 depth-10 sweep "
                                          "independently (different batch grouping: "
                                          "7x9 + 4 open bits + 6 confirmation bits; "
                                          "bit 14 run as an open bit) before noticing "
                                          "the concurrent claim overlap, and preserved "
                                          "the per-bit summary record without raw "
                                          "files, leaving this claim as canonical"),
            "agreement_check": ("class2-lane-cost73k-cross-lane-agreement-20261117.json "
                               "(git blob " + agree_blob + "): the published raw "
                               "batches are identical to the record on every per-bit "
                               "(loss, nodes, capped) triple (73/73), on the 25 "
                               "WIN7-D10 / 48 REFUTED-D10 partition, on the per-WIN "
                               "node table, on the node sums (128,861,941 candidates "
                               "/ 128,892,559 with pilots) and on the 7/7 census-v7 "
                               "confirmation outcomes; the batch groupings differ on "
                               "8 bits [14,15,31,52,73,89,101,116], which is grouping "
                               "only and not part of the determinism claim"),
            "agreement_check_script": ("scripts/check_cost73k_cross_lane_agreement_"
                                      "20261117.py (published alongside this claim)"),
            "record_level_consistency_audit": ("a third session independently re-derived "
                                               "the candidate geometry with a separate "
                                               "BigInt implementation and re-aggregated "
                                               "the published per-bit record: PASS "
                                               "(class2-lane-cost73k-concurrent-record-"
                                               "consistency-audit-20261117.json, git "
                                               "blob " + RECORD_AUDIT_BLOB + ", commit "
                                               "0274a2ef)"),
            "scope": ("cross-session determinism evidence for the same deterministic "
                      "engine from source; not an independent re-derivation of the "
                      "verdicts and closes no manifest row"),
        },
        "raw_outputs": ("see raw_batch_blob_pins in this claim; the raw batch "
                        "JSONLs, the two determinism rerun JSONLs and the "
                        "four v15 crosscheck JSONLs are published alongside "
                        "this claim v2"),
        "raw_batch_blob_pins": {},
        "raw_audit_json": ("class2-lane-cost73k-raw-sweep-audit-20261117.json "
                           "(git blob " + audit_blob + "); audit script "
                           "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
                           "scripts/audit_cost73k_raw_batches_20261117.py"),
    }
    for key, fname in (
            ("batch1", "class2-lane-cost73k-raw-batch1-20261117.jsonl"),
            ("batch2", "class2-lane-cost73k-raw-batch2-20261117.jsonl"),
            ("batch3", "class2-lane-cost73k-raw-batch3-20261117.jsonl"),
            ("batch4", "class2-lane-cost73k-raw-batch4-20261117.jsonl"),
            ("batch5", "class2-lane-cost73k-raw-batch5-20261117.jsonl"),
            ("batch6", "class2-lane-cost73k-raw-batch6-20261117.jsonl"),
            ("batch7", "class2-lane-cost73k-raw-batch7-20261117.jsonl"),
            ("batch8", "class2-lane-cost73k-raw-batch8-20261117.jsonl"),
            ("batch9", "class2-lane-cost73k-raw-batch9-confirmation-20261117.jsonl"),
            ("det_batch1", "class2-lane-cost73k-det-batch1-20261117.jsonl"),
            ("det_batch7", "class2-lane-cost73k-det-batch7-20261117.jsonl"),
            ("v15_a", "class2-lane-cost73k-v15-crosscheck-a-20261117.jsonl"),
            ("v15_b", "class2-lane-cost73k-v15-crosscheck-b-20261117.jsonl"),
            ("v15_c", "class2-lane-cost73k-v15-crosscheck-c-20261117.jsonl"),
            ("v15_d", "class2-lane-cost73k-v15-crosscheck-d-20261117.jsonl")):
        d["actual_execution"]["raw_batch_blob_pins"][key] = \
            git_blob_sha((raw_dir / fname).read_bytes())
    d["actual_execution"]["raw_batch_blob_pins"]["audit_json"] = audit_blob
    d["actual_execution"]["raw_batch_blob_pins"]["audit_script"] = \
        git_blob_sha(pathlib.Path(__file__).with_name(
            "audit_cost73k_raw_batches_20261117.py").read_bytes())
    d["actual_execution"]["raw_batch_blob_pins"]["agreement_json"] = agree_blob
    d["actual_execution"]["raw_batch_blob_pins"]["agreement_script"] = \
        git_blob_sha(pathlib.Path(__file__).with_name(
            "check_cost73k_cross_lane_agreement_20261117.py").read_bytes())
    d["actual_execution"]["raw_batch_blob_pins"]["batch_driver"] = \
        git_blob_sha(pathlib.Path(__file__).with_name(
            "ev73k_batches_20261117.sh").read_bytes())
    d["actual_execution"]["raw_batch_blob_pins"]["claim_v1"] = V1_BLOB_SHA
    d["actual_execution"]["raw_batch_blob_pins"]["update_script"] = \
        git_blob_sha(pathlib.Path(__file__).read_bytes())
    d["certificates"] = {
        "status": ("pending: blind extraction of the 22 sweep WIN7-D10 roots "
                   "(engine v15 inlined, extractor_exact, empty kill table as "
                   "in the 69j/71e/72d/73j lanes) with independent engine-free "
                   "verification before publication; the 3 confirmation WIN "
                   "roots (bits 14, 26, 55) are already certified by the "
                   "published cost73j bit 110, cost73i bit 110 and cost69j "
                   "bit 110 certificates; not published by this claim v2"),
        "planned_driver": ("cert_driver73k.ts (73j driver duplicated, "
                           "argv-driven, String.fromCharCode(10) newline "
                           "convention)")
    }
    d["next_action"] = (
        "blind certificate extraction + independent verification of the 22 sweep "
        "WIN7-D10 roots, published as certificate files (whole files under the "
        "size threshold, part1of2/part2of2 splits otherwise, one file per push) "
        "with a certificate manifest; then the receipt fold of this row stays "
        "pending behind the 76c/66i/66j/69j/71e/72d/73i folds"
    )
    d["receipt_fold"] = {
        "status": ("pending behind the cost-76c, cost-66i, cost-66j, cost-69j, "
                   "cost-71e, cost-72d and cost-73i folds"),
        "note": ("any WIN7-D10 certificates of this row fold only after the "
                 "pending folds land; no manifest row is closed by this sweep "
                 "or this claim")
    }
    out = json.dumps(d, indent=1, ensure_ascii=True) + "\n"
    pathlib.Path(dst).write_text(out)
    print(f"claim v2 written: {dst} ({len(out)} bytes); input blob sha verified "
          f"{V1_BLOB_SHA[:8]}")

if __name__ == "__main__":
    main()
