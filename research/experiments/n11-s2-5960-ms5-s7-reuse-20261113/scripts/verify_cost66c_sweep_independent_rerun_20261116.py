#!/usr/bin/env python3
"""Independent re-run verification of the cost-66c sweep (2026-11-16).

The parallel lane swept the 59 open candidate bits of the head-1441
third-ranked cheapest open row 00000000000000003800000008002008 (cost 66,
shared class-2 parent 00000000000000003800000008002000, claim v1 commit
64e83dff, claim v2 completed NOT-STERILE commit b17e978e) and published raw
batches 1-8 plus the bit-112 cap-raise resolution record: 7 WIN7-D10 (bits
73, 75, 79, 87, 96, 97, 112) + 52 swept REFUTED-D10 + 7 transferred
REFUTED-D10 = 66/66 candidates determined, 0 capped after the resolution
(bit 112 exceeded the 10000000-node protocol cap at 10000001 nodes in raw
batch 7 and was resolved at a raised cap of 80000000 as WIN7-D10 with
12574920 nodes), 84180263 total definitive swept nodes.  This script
verifies those results against this lane's own independent re-run: the
repo-verbatim v16 runner (class4_child1_runner_v16.ts, depth 10, cap 1e7,
--andclose 1, bit 112 additionally re-run at cap 80000000) executed here in
a fresh environment with engine state fully reset per candidate, pilot_d6
control 3402 nodes per batch invocation.  The independent raw records are
published alongside this script as
class2-lane-cost66c-independent-rerun-batch{1..8}-20261116.jsonl and
class2-lane-cost66c-independent-rerun-bit112-cap80m-20261116.jsonl.

The comparison asserts bit/loss/nodes/capped/terminalStoneRange/andclose
identity for every one of the 59 swept bits, pilot identity for all 8 batch
invocations, and full identity of the bit-112 cap-raise resolution record.
Interpretation guard: bookkeeping verification only; WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone roots only;
REFUTED-D10 is not a LOSS proof; NOT-STERILE is not a game resolution; 11x11
empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4
remain UNKNOWN.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

BATCH_BITS = {
    1: [1, 2, 9, 10, 12, 17, 21, 30],
    2: [32, 33, 34, 38, 42, 43, 44, 53],
    3: [54, 66, 67, 69, 71, 73, 74, 75],
    4: [76, 78, 79, 83, 85, 86, 87, 88],
    5: [89, 92, 93, 94, 95, 96, 97, 98],
    6: [99, 100, 101, 102, 103, 105, 106, 107],
    7: [108, 109, 110, 111, 112, 113, 114, 116],
    8: [117, 118, 120],
}
CHILD = "00000000000000003800000008002008"
WIN_ROOTS = {
    73: "00000000000002003800000008002008",
    75: "00000000000008003800000008002008",
    79: "00000000000080003800000008002008",
    87: "00000000008000003800000008002008",
    96: "00000001000000003800000008002008",
    97: "00000000002000003800000008002008",
    112: "00010000000000003800000008002008",
}

def load(path):
    recs = {}
    pilot = None
    for line in path.read_text().splitlines():
        d = json.loads(line)
        if "bit" in d:
            recs[d["bit"]] = d
        elif d.get("control") == "pilot_d6":
            pilot = d
    return recs, pilot

def main():
    mismatch = []
    total_mine = 0
    total_parallel = 0
    win_bits = []
    per_bit = []
    for i in range(1, 9):
        par, par_pilot = load(OUT / f"class2-lane-cost66c-raw-batch{i}-20261116.jsonl")
        mine, mine_pilot = load(OUT / f"class2-lane-cost66c-independent-rerun-batch{i}-20261116.jsonl")
        assert sorted(par) == BATCH_BITS[i], (i, sorted(par))
        assert sorted(mine) == BATCH_BITS[i], (i, sorted(mine))
        if par_pilot != {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}:
            mismatch.append(("pilot", i, "parallel", par_pilot))
        if par_pilot != mine_pilot:
            mismatch.append(("pilot", i, "mine", mine_pilot))
        for b in BATCH_BITS[i]:
            p, m = par[b], mine[b]
            total_mine += m["nodes"]
            total_parallel += p["nodes"]
            if m["loss"] is True:
                win_bits.append((b, m["nodes"]))
            for k in ("loss", "nodes", "capped", "terminalStoneRange", "andclose"):
                if p[k] != m[k]:
                    mismatch.append((i, b, k, p[k], m[k]))
            per_bit.append({
                "batch": i, "bit": b, "loss": m["loss"], "nodes": m["nodes"],
                "capped": m["capped"],
                "terminalStoneRange": m["terminalStoneRange"],
                "andclose": m["andclose"],
            })
    # bit-112 cap-raise resolution: single record published by the parallel lane
    par_res = json.loads((OUT / "class2-lane-cost66c-bit112-cap80m-resolution-20261116.jsonl").read_text().strip())
    mine_res_recs, mine_res_pilot = load(OUT / "class2-lane-cost66c-independent-rerun-bit112-cap80m-20261116.jsonl")
    mine_res = mine_res_recs[112]
    resolution_check = {}
    for k in ("loss", "nodes", "capped", "terminalStoneRange", "andclose"):
        resolution_check[k] = {"parallel": par_res[k], "mine": mine_res[k],
                                "agree": par_res[k] == mine_res[k]}
        if par_res[k] != mine_res[k]:
            mismatch.append(("resolution-bit112", k, par_res[k], mine_res[k]))
    raw_as_run_mine = total_mine
    raw_as_run_parallel = total_parallel
    definitive_mine = total_mine - 10000001 + mine_res["nodes"]
    definitive_parallel = 84180263
    result = {
        "schema": "n11-class2-lane-cost66c-independent-rerun-verification-20261116-v1",
        "date": "2026-11-16",
        "child": CHILD,
        "method": ("repo-verbatim v16 runner (class4_child1_runner_v16.ts) re-run "
                   "in this lane's fresh environment (Node 22, engine state reset "
                   "per candidate, --andclose 1, depth 10, cap 1e7; bit 112 "
                   "additionally re-run at cap 80000000), compared field-by-field "
                   "against the parallel lane's published raw batches 1-8 and the "
                   "bit-112 cap-raise resolution record"),
        "parallel_inputs": {
            "claim_v1": "class2-lane-cost66c-inflight-20261116.json (commit 64e83dff)",
            "claim_v2_completed": "commit b17e978e",
            "raw_batches_1_8_and_resolution": "commit b17e978e",
        },
        "independent_raw_files": [
            f"class2-lane-cost66c-independent-rerun-batch{i}-20261116.jsonl"
            for i in range(1, 9)] + [
            "class2-lane-cost66c-independent-rerun-bit112-cap80m-20261116.jsonl"],
        "checked_bits": len(per_bit),
        "mismatches": mismatch,
        "all_node_exact": len(mismatch) == 0 and len(per_bit) == 59,
        "total_nodes_mine_raw_as_run": raw_as_run_mine,
        "total_nodes_parallel_raw_as_run": raw_as_run_parallel,
        "total_definitive_nodes_mine": definitive_mine,
        "total_definitive_nodes_parallel_claim": definitive_parallel,
        "win_bits": [{"bit": b, "nodes": n, "root_hex": WIN_ROOTS[b]} for b, n in win_bits]
            + [{"bit": 112, "nodes": mine_res["nodes"], "root_hex": WIN_ROOTS[112]}],
        "refuted_swept_bits": len(per_bit) - len(win_bits) - 1,  # bit 112 counted once
        "capped_bits_in_raw": 1,
        "bit112_resolution_check": resolution_check,
        "pilots": "8/8 + 1 (resolution run) pilot_d6 = 3402 nodes, loss=false, all identical",
        "per_bit": per_bit,
        "interpretation_guard": ("bookkeeping verification only; WIN7-D10 proves "
            "a first-player win within depth 10 from the individual 7-stone "
            "roots only; REFUTED-D10 is not a LOSS proof; NOT-STERILE is not a "
            "game resolution; 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60} and classes 1/2/4 remain UNKNOWN"),
    }
    with open(OUT / "class2-lane-cost66c-independent-rerun-verification-20261116.json", "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("checked:", result["checked_bits"], "bits + bit-112 resolution")
    print("mismatches:", mismatch)
    print("raw-as-run mine:", raw_as_run_mine, "| parallel:", raw_as_run_parallel)
    print("definitive mine:", definitive_mine, "| parallel claim:", definitive_parallel)
    print("all_node_exact:", result["all_node_exact"])

if __name__ == "__main__":
    main()
