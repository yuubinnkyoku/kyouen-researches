#!/usr/bin/env python3
# claim v2 updater for class2-lane cost72d (2026-11-17)
# v1 -> v2: in-flight claim advanced to sweep-complete + certificates-complete
# after the 72-bit v17 depth-10 sweep and the 11 WIN7-D10 blind extractions
# both passed all planned controls and independent engine-free verification.
# Design: assert the input is the exact published claim v1 git blob, then emit v2.
import hashlib, json, sys

V1_BLOB_SHA = "b4454257b73a471417bcad0dd3172fd035e493b8"

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
    assert d["schema"] == "n11-class2-lane-cost72d-inflight-20261117-v1"

    d["schema"] = "n11-class2-lane-cost72d-inflight-20261117-v2"
    d["last_updated"] = "2026-11-17"
    d["status"] = (
        "claim v2: sweep and certificates complete; the fresh v17 72-bit depth-10 sweep "
        "finished 11 WIN7-D10 bits [1,6,24,25,43,49,75,80,83,98,114] + 61 REFUTED-D10, "
        "0 capped (133,761,580 candidate nodes + 9 pilot controls at 3,402 nodes each; "
        "9/9 pilots exact, determinism reruns of batches 1 and 3 field-identical on every "
        "non-ms field, independent v15 cross-engine re-check 11/11 WIN agreement, pilot "
        "5,949 exact, 0 capped, 5/5 census-v5 confirmation bits re-run fresh and "
        "REFUTED-D10 as predicted, stdlib raw audit all checks passed); the 11 WIN7-D10 "
        "roots were blindly extracted (extractor_exact, engine v15 inlined, FBS=1<<20, "
        "empty kill table) into 522,517 certificate rows (120,204,754 extraction nodes, "
        "18,850,168 published bytes; fbt_drops=0, no fatal, no capped per-move on all "
        "eleven) and independently verified engine-free (verify_bit7_win7_cert: root-check "
        "stones=7 and loser mobility = the legal_candidates.py RAW-root enumeration, all "
        "sub-roots PASS, terminal stone range [13,17], consumed union 0 missing / 0 extra "
        "on every root); fresh-process re-extraction byte-identical (md5) on bit 1; bit 75 "
        "published whole, the other ten split at line boundaries into part1of2/part2of2 "
        "with README-split per bit; manifest "
        "class2-lane-cost72d-win7-certificates-20261117.json; the receipt fold stays "
        "pending behind the 76c/66i/66j/69j/71e folds; no manifest row is closed by this "
        "claim; 11x11 UNKNOWN"
    )
    d["actual_execution"] = {
        "started": "2026-11-17",
        "engine": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts (v17, blob c132cc6425eee3feaeef1d697dd74f968cfedb59)",
        "batches_run": 9,
        "pilot_controls": "9/9 batches: pilot_d6 exact {loss=false, nodes=3402, capped=false}",
        "results": {
            "win7_d10_bits": [1, 6, 24, 25, 43, 49, 75, 80, 83, 98, 114],
            "win7_d10_nodes": {
                "1": 2157950,
                "6": 3294851,
                "24": 2898339,
                "25": 2567584,
                "43": 3680580,
                "49": 684200,
                "75": 881515,
                "80": 1632151,
                "83": 2885666,
                "98": 1654943,
                "114": 2804559
            },
            "refuted_d10_bits_count": 61,
            "capped_count": 0,
            "candidate_nodes_total": 133761580,
            "total_nodes_including_pilots": 133792198,
            "terminal_stone_range": [13, 17]
        },
        "confirmation_outcome": "5/5 REFUTED-D10 as predicted by the census v5 overlay (bit 5 = cost69j bit 14, bit 20 = cost64h bit 14, bit 103 = cost66i bit 34, bit 108 = cost66j bit 86, bit 115 = pre-64h harvest via cost69c)",
        "determinism_rerun": "batches 1 (WIN bits 1 and 6) and 3 (heaviest bit 41, 4,501,083 nodes) re-run in separate processes: field-identical on every non-ms field",
        "v15_crosscheck": "independent v15 engine (blob 8744fc65b6b7cac6bd561403ce4c749e01c51359) re-check of all 11 WIN bits: 11/11 loss=true, pilot 5949 exact, 0 capped",
        "raw_outputs": {
            "raw_batch_pattern": "class2-lane-cost72d-raw-batch{n}-20261117.jsonl (batch 9 = class2-lane-cost72d-raw-batch9-confirmation-20261117.jsonl)",
            "raw_batch_blob_pins": {
                "batch1": "3454dd496cbedca0c5a6ff3306441754b1d18df1",
                "batch2": "8d1296444207800b9a81135045568e5fe546bb46",
                "batch3": "0bc379c1f867bc988f16a955991fde19ae2ca7a3",
                "batch4": "f649b112a3297e18388cd7d8fdf6dc20824d8df8",
                "batch5": "d2f9589e3064200dfec92c9dc6449c5325321cf9",
                "batch6": "5fce651ae7ee274cfd015e8575ca40596152ee10",
                "batch7": "b01f9da7c716a5747c65d6bce54a068cad3d76b1",
                "batch8": "1fd124264c1a79273ae1c4a6d656beb0a2c657ae",
                "batch9_confirmation": "681d5c3cc3c546a2e52f222cf8a4dc03c2ec6042"
            },
            "determinism_rerun_blob_pins": {
                "det_batch1": "8c5118fed6aca6ceac6464895b9f4b49e25f1c00",
                "det_batch3": "0c2b3302ed9d3df5aaddb5e23af5ed0ffac4bc86"
            },
            "v15_crosscheck_blob_pins": {
                "v15_crosscheck_a": "8ab7adcb37112cbcc442152a24d5ef27d7bb9c5d",
                "v15_crosscheck_b": "61615975997c8599be39931069fab6a380447790"
            },
            "raw_audit_json": "class2-lane-cost72d-raw-sweep-audit-20261117.json (git blob 6247569a7dca86053943701a3ae099e704e0cb31); audit script research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost72d_raw_batches_20261117.py (git blob 8d97fc10d499fe14c1a6fdd4e90003fbcf0f3d63)"
        }
    }
    d["certificates"] = {
        "manifest": "output/class2-lane-cost72d-certificates/class2-lane-cost72d-win7-certificates-20261117.json",
        "schema": "n11-class2-lane-cost72d-win7-certificates-20261117-v1",
        "win7_d10_bits": [1, 6, 24, 25, 43, 49, 75, 80, 83, 98, 114],
        "totals": {
            "certificates": 11,
            "rows": 522517,
            "extraction_nodes": 120204754,
            "published_bytes": 18850168,
            "fbt_drops": 0
        },
        "whole_file_bits": [75],
        "split_bits": [1, 6, 24, 25, 43, 49, 80, 83, 98, 114],
        "verification": "engine-free verify_bit7_win7_cert.ts per root: stones=7 root check, loser mobility = legal_candidates.py RAW-root count (bit1:55, bit6:54, bit24:57, bit25:54, bit43:58, bit49:59, bit75:50, bit80:53, bit83:57, bit98:55, bit114:61), all sub-roots PASS, consumed union 0 missing / 0 extra, terminal stone range [13,17]; bit 1 blind re-extraction byte-identical (md5 bdd29dc364f975050280f45a5c1428bc)",
        "driver": "scripts/cert_driver72d.ts (71e driver duplicated, argv-driven, String.fromCharCode(10) newline convention); ev72d.sh orchestrates; verify_cost72d_one.sh per-root orchestration"
    }
    d["next_action"] = (
        "receipt fold of this row stays pending behind the 76c/66i/66j/69j/71e folds "
        "(managed by their own lanes); next fresh targets for this lane: the census v5 "
        "top-10 cost-73 rows 00000000000000403800400008000000 (open 68) and "
        "00000000000000403800000408000000 (open 69)"
    )
    d["receipt_fold"] = {
        "status": "pending behind the cost-76c, cost-66i, cost-66j, cost-69j and cost-71e folds",
        "note": "any WIN7-D10 certificates of this row fold only after the pending folds land; no manifest row is closed by this sweep or this claim"
    }
    out = json.dumps(d, indent=1, ensure_ascii=True) + "\n"
    open(dst, "w").write(out)
    print(f"claim v2 written: {dst} ({len(out)} bytes); input blob sha verified {V1_BLOB_SHA[:8]}")

if __name__ == "__main__":
    main()
