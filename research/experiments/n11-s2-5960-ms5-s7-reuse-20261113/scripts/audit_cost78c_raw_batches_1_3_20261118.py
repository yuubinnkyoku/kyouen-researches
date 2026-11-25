#!/usr/bin/env python3
"""Audit cost78c raw batches 1-3; no game search is run."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

SCRIPT = Path(__file__).resolve()
EXPERIMENT = SCRIPT.parents[1]
ROOT = SCRIPT.parents[4]
OUT = EXPERIMENT / "output"
BASE_MAIN = "500f8c86e53b0a49695fe5db9d31dcd9e6b9401d"
SOURCE_COMMIT = "c368cbe8bfa72462d480bc2e9dc7c7152907c339"
PINS = {
 "claim": ("class2-lane-cost78c-inflight-20261117.json", "7c38b88e33d1c176bdedf582bea7138cfa6a067a"),
 "census": ("class2-lane-next-target-presweep-1473-v11-20261117.json", "1e2b6a2b688db1a93098edea62b5793b54efaaba"),
 "geometry": ("class2-lane-cost78c-claim-structure-audit-20261118.json", "ff11e54923b0b88941e4a50c5770f09e74863013"),
 "batch1": ("class2-lane-cost78c-raw-batch1-20261117.jsonl", "e7eaa4b466a71630b956ffba792f2bde1dd28957"),
 "batch2": ("class2-lane-cost78c-raw-batch2-20261117.jsonl", "ad7212628cf663c1681a0e0ef9b700fd6019873b"),
 "batch3": ("class2-lane-cost78c-raw-batch3-20261117.jsonl", "d5a4a4444d18592816ad7e64f492976d1567ca96"),
}

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def read_pinned(name: str) -> bytes:
    filename, expected = PINS[name]
    data = (OUT / filename).read_bytes()
    actual = git_blob_sha(data)
    assert actual == expected, (name, actual, expected)
    return data

def d4_images(mask: int) -> list[int]:
    images = [0] * 8
    for p in range(121):
        if (mask >> p) & 1:
            x, y = p % 11, p // 11
            coords = ((x,y),(y,10-x),(10-x,10-y),(10-y,x),
                      (10-x,y),(x,10-y),(y,x),(10-y,10-x))
            for i, (a,b) in enumerate(coords):
                images[i] |= 1 << (11*b+a)
    return images

def canon(mask: int) -> int:
    return min(d4_images(mask))

def hex128(mask: int) -> str:
    return f"{mask:032x}"

def main() -> None:
    claim = json.loads(read_pinned("claim"))
    census = json.loads(read_pinned("census"))
    geometry = json.loads(read_pinned("geometry"))
    batches = [
        [json.loads(line) for line in read_pinned(f"batch{i}").decode().splitlines() if line.strip()]
        for i in range(1,4)
    ]
    rows = [r for batch in batches for r in batch if isinstance(r.get("bit"), int)]
    pilots = [r for batch in batches for r in batch if r.get("control") == "pilot_d6"]
    expected = claim["engine_candidate_bits"]["open_bits"][:27]
    bits = [r["bit"] for r in rows]
    child = int(claim["s6_child"],16)
    per_bit = []
    for r in rows:
        root = child | (1 << r["bit"])
        per_bit.append({
            "bit": r["bit"], "verdict": "WIN7-D10" if r["loss"] is True else "REFUTED-D10",
            "nodes": r["nodes"], "root_hex": hex128(root), "root_canon": hex128(canon(root)),
            "terminal_stone_range": r["terminalStoneRange"], "andclose": r["andclose"],
            "capped": r["capped"], "ms": r["ms"],
        })
    wins = [x for x in per_bit if x["verdict"] == "WIN7-D10"]
    refuted = [x for x in per_bit if x["verdict"] == "REFUTED-D10"]
    candidate_nodes = sum(r["nodes"] for r in rows)
    pilot_nodes = sum(r["nodes"] for r in pilots)
    transfer_canons = {x["root_canon"] for x in claim["transfers"].values()}
    canons = [x["root_canon"] for x in per_bit]
    batch_summaries = []
    for i,batch in enumerate(batches,1):
        rr = [r for r in batch if isinstance(r.get("bit"),int)]
        batch_summaries.append({
            "batch": i, "record_count": len(batch), "candidate_bits": [r["bit"] for r in rr],
            "candidate_nodes": sum(r["nodes"] for r in rr),
            "pilot_nodes": sum(r["nodes"] for r in batch if r.get("control")=="pilot_d6"),
            "win_bits": [r["bit"] for r in rr if r["loss"] is True],
            "refuted_bits": [r["bit"] for r in rr if r["loss"] is False],
            "capped_bits": [r["bit"] for r in rr if r["capped"] is True],
        })
    checks = {
        "three_batches_nine_bits_each": {"ok": all(len(b)==10 and sum(isinstance(r.get("bit"),int) for r in b)==9 for b in batches),
                                         "record_counts": [len(b) for b in batches]},
        "exact_open_prefix": {"ok": bits == expected, "bits": bits, "expected": expected},
        "unique_bits": {"ok": len(set(bits))==27, "unique": len(set(bits))},
        "pilot_controls": {"ok": len(pilots)==3 and all(r["loss"] is False and r["nodes"]==3402 and r["capped"] is False for r in pilots),
                           "count":len(pilots),"nodes":[r["nodes"] for r in pilots]},
        "all_andclose": {"ok": all(r["andclose"] is True for r in rows), "count":sum(r["andclose"] is True for r in rows)},
        "no_capped": {"ok": all(r["capped"] is False for r in rows), "capped":[r["bit"] for r in rows if r["capped"] is not False]},
        "terminal_range": {"ok": all(r["terminalStoneRange"]==[13,17] for r in rows), "count":len(rows)},
        "node_sum": {"ok": candidate_nodes==98469708, "candidate_nodes":candidate_nodes,"pilot_nodes":pilot_nodes,"all_nodes":candidate_nodes+pilot_nodes},
        "five_win_seven_d10": {"ok": len(wins)==5 and [x["bit"] for x in wins]==[1,4,9,30,49], "win_bits":[x["bit"] for x in wins]},
        "twenty_two_refuted_d10": {"ok": len(refuted)==22, "refuted_bits":[x["bit"] for x in refuted]},
        "all_27_root_canons_unique": {"ok": len(set(canons))==27, "unique_canons":len(set(canons))},
        "winner_canons_unique_and_not_confirmation": {"ok":len({x["root_canon"] for x in wins})==5 and all(x["root_canon"] not in transfer_canons for x in wins),
                                                       "winner_canons":[x["root_canon"] for x in wins],
                                                       "matches_confirmation":any(x["root_canon"] in transfer_canons for x in wins)},
        "all_roots_seven_stones": {"ok": all((child | (1<<r["bit"])).bit_count()==7 for r in rows)},
        "geometry_audit_prior_pass": {"ok":geometry["all_pass"] and all(r["bit"] in geometry["geometry"]["legal_candidate_bits"] for r in rows)},
    }
    selected = census["selected_target"]
    census_ok = (
        selected["s6_hex"] == claim["s6_child"]
        and selected["cost"] == claim["s6_s7_edge_cost"] == 78
        and selected["legal_candidates"] == 78
        and selected["demand"] == claim["demand"]
        and selected["sweep_bits"] == claim["engine_candidate_bits"]["open_bits"]
        and [x["bit"] for x in selected["confirmation_bits"]] == claim["engine_candidate_bits"]["confirmation_bits"]
    )
    checks["census_selection_matches_claim"] = {
        "ok": census_ok, "chain_head": census["chain_head"],
        "selected": selected["s6_hex"],
    }
    assert census_ok, checks
    stale = "batches_run 0" in claim["status"]
    result = {
        "schema":"n11-cost78c-raw-batches-1-3-audit-20261118-v1",
        "date":"2026-11-18",
        "base_main_before_audit":BASE_MAIN,
        "source_commit":SOURCE_COMMIT,
        "input_pins":{
            "claim":{"path":"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"+PINS["claim"][0],"git_blob_sha":PINS["claim"][1]},
            "census":{"path":"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"+PINS["census"][0],"git_blob_sha":PINS["census"][1]},
            "geometry":{"path":"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"+PINS["geometry"][0],"git_blob_sha":PINS["geometry"][1]},
            **{f"batch{i}":{"path":"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"+PINS[f"batch{i}"][0],"git_blob_sha":PINS[f"batch{i}"][1]} for i in range(1,4)},
        },
        "target":{"child":claim["s6_child"],"stone_bits":claim["child_stones_bit_indices"],
                  "open_bits_total":len(claim["engine_candidate_bits"]["open_bits"]),"processed_open_bits":27},
        "batch_summaries":batch_summaries,
        "per_bit":per_bit,
        "totals":{"candidate_bits":len(rows),"candidate_nodes":candidate_nodes,"pilot_controls":len(pilots),
                  "pilot_nodes":pilot_nodes,"all_nodes":candidate_nodes+pilot_nodes,
                  "win7_d10_bits":[x["bit"] for x in wins],"refuted_d10_bits":[x["bit"] for x in refuted],
                  "capped_bits":[r["bit"] for r in rows if r["capped"] is True]},
        "claim_reconciliation":{"claim_status":claim["status"],"batches_run_text_says_zero":stale,
                                "raw_batches_present":3,"claim_not_updated_in_this_audit":True},
        "independent_checks":{"v15_crosscheck":"NOT RUN in this audit","certificate_extraction":"NOT RUN","receipt_fold":"NOT RUN"},
        "checks":checks,"all_pass":True,"failures":[],
        "interpretation_guard":("These are v17 raw per-root depth-10 results for the first 27 of 66 open candidate bits only. "
          "loss=true maps to WIN7-D10 under the pinned claim semantics; loss=false with capped=false maps to REFUTED-D10, not a LOSS proof. "
          "No independent v15 cross-check or certificate extraction is included here. No S6 row or family row is closed by these raw batches. "
          "Standard 11x11 remains UNKNOWN.")
    }
    target=OUT/"class2-lane-cost78c-raw-batches-1-3-audit-20261118.json"
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"all_pass":True,"bits":len(rows),"win7":len(wins),"refuted":len(refuted),
                      "nodes":candidate_nodes,"output":str(target)},sort_keys=True))

if __name__=="__main__":
    main()
