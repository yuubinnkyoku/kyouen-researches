#!/usr/bin/env python3
# claim v2 updater for class2-lane cost73j (2026-11-17)
# v1 -> v2: in-flight claim advanced to sweep-complete after the fresh
# 73-bit v17 depth-10 sweep (66 open + 7 confirmation bits) passed all
# planned controls (9/9 pilots exact, determinism reruns, v15 cross-engine
# 16/16 WIN agreement, 7/7 confirmation transfers REFUTED-D10 as predicted)
# and the stdlib raw audit passed all checks. Certificates: pending.
# Design: assert the input is the exact published claim v1 git blob, then emit v2.
import hashlib, json, sys

V1_BLOB_SHA = "d52005e662d39779d34ee5b1ae59f25a57f545a9"

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def main() -> None:
    src = sys.argv[1]  # claim v1 json
    dst = sys.argv[2]  # claim v2 json output
    raw = open(src, "rb").read()
    sha = git_blob_sha(raw)
    if sha != V1_BLOB_SHA:
        sys.exit(f"FATAL: input is not the published claim v1 blob (got {sha})")
    d = json.loads(raw.decode("utf-8"))
    assert d["schema"] == "n11-class2-lane-cost73j-inflight-20261117-v1"

    d["schema"] = "n11-class2-lane-cost73j-inflight-20261117-v2"
    d["last_updated"] = "2026-11-17"
    d["status"] = (
        "claim v2: sweep complete; the fresh v17 73-bit depth-10 sweep of the census v6 "
        "rank-1 row finished 16 WIN7-D10 bits [0,1,6,29,44,49,52,69,74,82,87,91,98,100,"
        "110,118] + 57 REFUTED-D10, 0 capped (168,445,380 candidate nodes + 9 pilot "
        "controls at 3,402 nodes each; 9/9 pilots exact, determinism reruns of batches 1 "
        "and 6 field-identical on every non-ms field, independent v15 cross-engine "
        "re-check 16/16 WIN agreement, pilot 5,949 exact, 0 capped, 7/7 census-v6 "
        "confirmation bits re-run fresh and REFUTED-D10 as predicted (4 raw-identical "
        "+ 3 canon-equal transfer sources, all source pins verified against their "
        "published audits / the pinned census v4 script), stdlib raw audit all checks "
        "passed); the 16 WIN7-D10 roots go to blind certificate extraction and "
        "independent engine-free verification before publication (certificates pending, "
        "this claim does not publish them); the receipt fold stays pending behind the "
        "76c/66i/66j/69j/71e/72d/73i folds; no manifest row is closed by this claim; "
        "11x11 UNKNOWN"
    )
    d["actual_execution"] = {
        "started": "2026-11-17",
        "engine": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts (v17, blob c132cc6425eee3feaeef1d697dd74f968cfedb59)",
        "batches_run": 9,
        "pilot_controls": "9/9 batches: pilot_d6 exact {loss=false, nodes=3402, capped=false}",
        "results": {
            "win7_d10_bits": [0, 1, 6, 29, 44, 49, 52, 69, 74, 82, 87, 91,
                              98, 100, 110, 118],
            "win7_d10_nodes": {
                "0": 2017323, "1": 3423188, "6": 2120524, "29": 4630877,
                "44": 2543589, "49": 886240, "52": 3844019, "69": 1070978,
                "74": 2555074, "82": 588415, "87": 3696441, "91": 1693102,
                "98": 8801472, "100": 1919973, "110": 3283518,
                "118": 1564528
            },
            "refuted_d10_bits_count": 57,
            "capped_count": 0,
            "candidate_nodes_total": 168445380,
            "total_nodes_including_pilots": 168476098,
            "terminal_stone_range": [13, 17]
        },
        "confirmation_outcome": ("7/7 REFUTED-D10 as predicted by the census v6 "
                                 "nine-map overlay (bit 5 = cost69j bit 34, bit 14 = "
                                 "cost72d bit 34, bit 20 = cost64h bit 34, bit 46 = "
                                 "cost73i bit 34, bit 97 = cost71e bit 106, bit 103 = "
                                 "cost66i bit 14, bit 108 = cost66j bit 106); bits "
                                 "5/14/20/46 are raw-identical to their transfer "
                                 "sources (identical node counts), bits 97/103/108 "
                                 "are canon-equal only"),
        "determinism_rerun": ("batches 1 (WIN bits 0, 1, 6 and the heaviest search "
                              "bit 3, 11,476,946 nodes) and 6 (heaviest WIN bit 98, "
                              "8,801,472 nodes) re-run in separate processes: "
                              "field-identical on every non-ms field"),
        "v15_crosscheck": ("independent v15 engine (blob "
                           "8744fc65b6b7cac6bd561403ce4c749e01c51359) re-check of "
                           "all 16 WIN bits: 16/16 loss=true, pilot 5949 exact, "
                           "0 capped"),
        "raw_outputs": "see raw_batch_blob_pins in this claim; the raw batch JSONLs, "
                       "the two determinism rerun JSONLs and the two v15 crosscheck "
                       "JSONLs are published alongside this claim v2",
    }
    d["certificates"] = {
        "status": "pending: blind extraction of the 16 WIN7-D10 roots (engine v15 "
                   "inlined, extractor_exact, empty kill table as in the 69j/71e/72d "
                   "lanes) with independent engine-free verification before "
                   "publication; not published by this claim v2",
        "planned_driver": "cert_driver73j.ts (71e/72d driver duplicated, argv-driven, "
                          "String.fromCharCode(10) newline convention)"
    }
    d["next_action"] = (
        "blind certificate extraction + independent verification of the 16 WIN7-D10 "
        "roots, published as certificate files (part1of2/part2of2 splits for large "
        "bits, one file per push) with a certificate manifest; then the receipt fold "
        "of this row stays pending behind the 76c/66i/66j/69j/71e/72d/73i folds"
    )
    d["receipt_fold"] = {
        "status": "pending behind the cost-76c, cost-66i, cost-66j, cost-69j, cost-71e, cost-72d and cost-73i folds",
        "note": "any WIN7-D10 certificates of this row fold only after the pending folds land; no manifest row is closed by this sweep or this claim"
    }
    out = json.dumps(d, indent=1, ensure_ascii=True) + "\n"
    open(dst, "w").write(out)
    print(f"claim v2 written: {dst} ({len(out)} bytes); input blob sha verified {V1_BLOB_SHA[:8]}")

if __name__ == "__main__":
    main()
