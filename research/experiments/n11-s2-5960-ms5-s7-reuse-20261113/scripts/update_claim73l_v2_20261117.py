#!/usr/bin/env python3
# claim v2 updater for class2-lane cost73l (2026-11-17)
# v1 -> v2: in-flight claim advanced to sweep-complete. This is the FIRST
# execution of this child: the raw batch JSONLs published with this claim
# are the claiming session's own execution outputs (no sandbox reset, no
# concurrent-session overlap). All planned controls passed (see the raw
# sweep audit class2-lane-cost73l-raw-sweep-audit-20261117.json).
# Certificates: pending (32 new WIN roots; the 2 WIN transfers 106/110 are
# covered by the published cost73j bit 118 / cost73k bit 98 certificates).
import hashlib, json, sys, pathlib

V1_BLOB_SHA = "fa13a0ada22e3de95c06e9a3101ce6d2a738f5b1"
CENSUS_V8_JSON_BLOB = "2542914e02db14a8426a1a16ef1c2cfcd9817375"

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
    assert d["schema"] == "n11-class2-lane-cost73l-inflight-20261117-v1"

    audit_blob = git_blob_sha((raw_dir /
        "class2-lane-cost73l-raw-sweep-audit-20261117.json").read_bytes())

    d["schema"] = "n11-class2-lane-cost73l-inflight-20261117-v2"
    d["last_updated"] = "2026-11-17"
    d["status"] = (
        "claim v2: sweep complete; the fresh v17 73-bit depth-10 sweep of the "
        "head-1473 census v8 rank-1 row finished 34 WIN7-D10 bits [1,2,3,4,6,8,"
        "9,18,21,23,25,28,29,32,34,41,42,44,47,53,54,61,62,64,66,80,95,105,106,"
        "110,112,113,116,119] (32 sweep WIN + 2 confirmation WIN transfers) + 39 "
        "REFUTED-D10, 0 capped (133,895,305 candidate nodes + 9 pilot controls "
        "at 3,402 nodes each; 9/9 pilots exact, determinism reruns of batches 1 "
        "and 4 (batch 4 holds the heaviest search bit 47, 6,045,349 nodes) "
        "field-identical on every non-ms field, independent v15 cross-engine "
        "re-check 34/34 WIN agreement via a/b/c/d, 4/4 pilots 5,949 exact, 0 "
        "capped; 7/7 census-v8 confirmation bits matching the predicted "
        "verdicts (2 WIN7-D10: bit 106 = cost73j bit 118, bit 110 = cost73k "
        "bit 98, both covered by published certificates; 5 REFUTED-D10: bit 65 "
        "= cost69j bit 118, bit 86 = cost72d bit 118, bit 90 = cost76c bit 48, "
        "bit 94 = cost73i bit 118, bit 97 = pre-64h harvest, identified in the "
        "raw sweep audit as cost64d bit 118, the only canon match among the "
        "published pre-64h raw batches); every transfer canon-equality "
        "independently re-derived with the D4 canon function of the published "
        "census v8 script (canon(source_child|source_bit) == claim root_canon "
        "== canon(this child|bit), 7/7, none raw-identical); provenance: first "
        "execution, the claiming session's own raw files published with this "
        "claim (no sandbox reset, no concurrent-session overlap for this "
        "child); stdlib raw audit all checks passed "
        "(class2-lane-cost73l-raw-sweep-audit-20261117.json); the 32 sweep "
        "WIN7-D10 roots go to blind certificate extraction and independent "
        "engine-free verification before publication (certificates pending, "
        "this claim does not publish them); the receipt fold stays pending "
        "behind the 66i/66j/69j/71e/72d/73i/73j/73k folds; no manifest row is "
        "closed by this claim; 11x11 UNKNOWN"
    )
    d["actual_execution"] = {
        "started": "2026-11-17",
        "engine": ("class4_child1_runner_v17.ts (v17, blob "
                   "c132cc6425eee3feaeef1d697dd74f968cfedb59), depth 10, cap "
                   "1e9 per bit, andclose 1, fresh engine state per candidate "
                   "bit"),
        "provenance": ("first execution; the raw batch JSONLs are this "
                       "session's own outputs, driven by scripts/"
                       "ev73l_batches_20261117.sh (same batch plan shape as "
                       "the cost73k run: 7x9 + 1x3 open bits + 1 confirmation "
                       "batch of 7 bits)"),
        "batches_run": 9,
        "pilot_controls": "9/9 batches: pilot_d6 exact {loss=false, nodes=3402, capped=false}",
        "results": {
            "win7_d10_bits": [1, 2, 3, 4, 6, 8, 9, 18, 21, 23, 25, 28, 29,
                              32, 34, 41, 42, 44, 47, 53, 54, 61, 62, 64,
                              66, 80, 95, 105, 106, 110, 112, 113, 116,
                              119],
            "win7_d10_nodes": {
                "1": 2205897, "2": 1714291, "3": 3336703, "4": 3034054,
                "6": 3715414, "8": 1743796, "9": 4189085, "18": 5377746,
                "21": 1588780, "23": 1717767, "25": 3298277, "28": 1010177,
                "29": 1255982, "32": 2329525, "34": 1826586, "41": 595652,
                "42": 2306573, "44": 2076710, "47": 6045349, "53": 1537745,
                "54": 1694242, "61": 496186, "62": 1319548, "64": 5253067,
                "66": 3145583, "80": 1154372, "95": 2171732, "105": 4406737,
                "106": 1234240, "110": 1432126, "112": 4669745,
                "113": 1283055, "116": 5113596, "119": 2083072
            },
            "refuted_d10_bits": [0, 7, 10, 14, 17, 19, 24, 26, 30, 33, 35,
                                45, 58, 65, 68, 76, 78, 79, 81, 85, 86, 87,
                                89, 90, 91, 92, 94, 96, 97, 98, 100, 101,
                                102, 107, 109, 111, 114, 117, 120],
            "refuted_d10_bits_count": 39,
            "capped_count": 0,
            "candidate_nodes_total": 133895305,
            "total_nodes_including_pilots": 133925923,
            "terminal_stone_range": [13, 17],
            "terminal_stone_range_exceptions": {
                "91": [13, 15],
                "note": "early refutation at 13-15 stones (24,376 nodes); see the raw sweep audit"
            },
            "heaviest_bit": 47,
            "heaviest_bit_nodes": 6045349
        },
        "confirmation_outcome": ("7/7 as predicted by the head-1473 census v8 "
                                 "eleven-map/harvest overlay (2 WIN7-D10: bit "
                                 "106 = cost73j bit 118, bit 110 = cost73k "
                                 "bit 98, both covered by the published "
                                 "certificates; 5 REFUTED-D10: bit 65 = "
                                 "cost69j bit 118, bit 86 = cost72d bit 118, "
                                 "bit 90 = cost76c bit 48, bit 94 = cost73i "
                                 "bit 118, bit 97 = pre-64h harvest, "
                                 "identified as cost64d bit 118 in the raw "
                                 "sweep audit); all 7 transfers canon-equal "
                                 "only (independent D4 canon re-derivation, "
                                 "verdict-level agreement, node counts differ "
                                 "by labeling, none raw-identical)"),
        "determinism_rerun": ("batches 1 (WIN bits 1, 2, 3, 4, 6, 8, 9 and "
                              "REFUTED bit 0; heaviest bit 9, 4,189,085 "
                              "nodes) and 4 (WIN bits 42, 44, 47, 53, 54, "
                              "61, 62 and REFUTED bits 45, 58; heaviest "
                              "search bit 47, 6,045,349 nodes) re-run in "
                              "separate processes: field-identical on every "
                              "non-ms field"),
        "v15_crosscheck": ("independent v15 engine (blob "
                           "8744fc65b6b7cac6bd561403ce4c749e01c51359) "
                           "re-check of all 34 WIN bits (a/b/c/d chunks of "
                           "9+9+8+8): 34/34 loss=true, 4/4 pilots 5949 "
                           "exact, 0 capped; v15 node total recorded in the "
                           "raw sweep audit"),
        "raw_outputs": ("see raw_batch_blob_pins in this claim; the raw batch "
                       "JSONLs, the two determinism rerun JSONLs and the "
                       "four v15 crosscheck JSONLs are published alongside "
                       "this claim v2"),
        "raw_batch_blob_pins": {},
        "raw_audit_json": ("class2-lane-cost73l-raw-sweep-audit-20261117.json "
                           "(git blob " + audit_blob + "); audit script "
                           "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
                           "scripts/audit_cost73l_raw_batches_20261117.py"),
    }
    for key, fname in (
            ("batch1", "class2-lane-cost73l-raw-batch1-20261117.jsonl"),
            ("batch2", "class2-lane-cost73l-raw-batch2-20261117.jsonl"),
            ("batch3", "class2-lane-cost73l-raw-batch3-20261117.jsonl"),
            ("batch4", "class2-lane-cost73l-raw-batch4-20261117.jsonl"),
            ("batch5", "class2-lane-cost73l-raw-batch5-20261117.jsonl"),
            ("batch6", "class2-lane-cost73l-raw-batch6-20261117.jsonl"),
            ("batch7", "class2-lane-cost73l-raw-batch7-20261117.jsonl"),
            ("batch8", "class2-lane-cost73l-raw-batch8-20261117.jsonl"),
            ("batch9", "class2-lane-cost73l-raw-batch9-confirmation-20261117.jsonl"),
            ("det_batch1", "class2-lane-cost73l-det-batch1-20261117.jsonl"),
            ("det_batch4", "class2-lane-cost73l-det-batch4-20261117.jsonl"),
            ("v15_a", "class2-lane-cost73l-v15-crosscheck-a-20261117.jsonl"),
            ("v15_b", "class2-lane-cost73l-v15-crosscheck-b-20261117.jsonl"),
            ("v15_c", "class2-lane-cost73l-v15-crosscheck-c-20261117.jsonl"),
            ("v15_d", "class2-lane-cost73l-v15-crosscheck-d-20261117.jsonl")):
        d["actual_execution"]["raw_batch_blob_pins"][key] = \
            git_blob_sha((raw_dir / fname).read_bytes())
    d["actual_execution"]["raw_batch_blob_pins"]["audit_json"] = audit_blob
    d["actual_execution"]["raw_batch_blob_pins"]["audit_script"] = \
        git_blob_sha(pathlib.Path(__file__).with_name(
            "audit_cost73l_raw_batches_20261117.py").read_bytes())
    d["actual_execution"]["raw_batch_blob_pins"]["batch_driver"] = \
        git_blob_sha(pathlib.Path(__file__).with_name(
            "ev73l_batches_20261117.sh").read_bytes())
    d["actual_execution"]["raw_batch_blob_pins"]["census_v8_json"] = \
        CENSUS_V8_JSON_BLOB
    d["actual_execution"]["raw_batch_blob_pins"]["claim_v1"] = V1_BLOB_SHA
    d["actual_execution"]["raw_batch_blob_pins"]["update_script"] = \
        git_blob_sha(pathlib.Path(__file__).read_bytes())
    d["certificates"] = {
        "status": ("pending: blind extraction of the 32 sweep WIN7-D10 roots "
                   "(per-bit fresh MS=1<<23 extraction prescription, "
                   "engine v15 inlined, extractor_exact, empty kill table as "
                   "in the 69j/71e/72d/73j/73k lanes) with independent "
                   "engine-free BigInt verification before publication; the "
                   "2 confirmation WIN roots (bits 106, 110) are already "
                   "certified by the published cost73j bit 118 and cost73k "
                   "bit 98 certificates; not published by this claim v2"),
    }
    d["next_action"] = (
        "blind certificate extraction + independent verification of the 32 "
        "sweep WIN7-D10 roots, published as certificate files with a "
        "certificate manifest; then the receipt fold of this row stays "
        "pending behind the 66i/66j/69j/71e/72d/73i/73j/73k folds"
    )
    d["receipt_fold"] = {
        "status": ("pending behind the cost-66i, cost-66j, cost-69j, cost-71e, "
                   "cost-72d, cost-73i, cost-73j and cost-73k folds"),
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
