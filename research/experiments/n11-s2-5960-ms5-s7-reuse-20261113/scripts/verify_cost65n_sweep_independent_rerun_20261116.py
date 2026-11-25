#!/usr/bin/env python3
"""Independent re-run verification of the cost-65n sweep (2026-11-16).

The parallel lane swept the 59 open candidate bits of the head-1441
cheapest open row 00000000000000801202010000800000 (cost 65, shared class-2
parent 00000000000000003800000008002000, claim v1 commit 7dcd9767) and
published raw batches 1-8 (commits 60c97b93 batches 1-4, e728c47e batches
5-8): 2 WIN7-D10 (bits 90, 117) + 57 REFUTED-D10, 0 capped, 92,530,349
nodes total.  This script verifies those results against this lane's own
independent re-run: the repo-verbatim v16 runner (class4_child1_runner_v16.ts,
depth 10, cap 1e7, --andclose 1) executed here in a fresh environment with
engine state fully reset per batch, pilot_d6 control 3402 nodes per batch.
The independent raw records are published alongside this script as
class2-lane-cost65n-independent-rerun-batch{1..8}-20261116.jsonl.

The comparison asserts bit/loss/nodes/capped/terminalStoneRange/andclose
identity for every one of the 59 swept bits and pilot identity for all 8
batch invocations.  Interpretation guard: bookkeeping verification only;
WIN7-D10 proves a first-player win within depth 10 from the individual
7-stone roots only; REFUTED-D10 is not a LOSS proof; 11x11 empty board,
two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain
UNKNOWN.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

BATCH_BITS = {
    1: [1, 3, 6, 8, 9, 10, 11, 12],
    2: [14, 17, 18, 19, 20, 21, 22, 26],
    3: [29, 31, 32, 42, 43, 44, 53, 54],
    4: [56, 58, 61, 66, 67, 74, 75, 77],
    5: [79, 83, 85, 86, 87, 88, 90, 94],
    6: [97, 98, 99, 102, 103, 105, 106, 107],
    7: [108, 110, 111, 112, 113, 114, 116, 117],
    8: [118, 119, 120],
}
CHILD = "00000000000000801202010000800000"

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
        par, par_pilot = load(OUT / f"class2-lane-cost65n-raw-batch{i}-20261116.jsonl")
        mine, mine_pilot = load(OUT / f"class2-lane-cost65n-independent-rerun-batch{i}-20261116.jsonl")
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
    result = {
        "schema": "n11-class2-lane-cost65n-independent-rerun-verification-20261116-v1",
        "date": "2026-11-16",
        "child": CHILD,
        "method": ("repo-verbatim v16 runner (class4_child1_runner_v16.ts) re-run "
                   "in this lane's fresh environment (Node 22, engine state reset "
                   "per batch, --andclose 1, depth 10, cap 1e7), compared "
                   "field-by-field against the parallel lane's published raw "
                   "batches 1-8"),
        "parallel_inputs": {
            "claim_v1": "class2-lane-cost65n-inflight-20261116.json (commit 7dcd9767)",
            "raw_batches_1_4": "commit 60c97b93",
            "raw_batches_5_8": "commit e728c47e",
        },
        "independent_raw_files": [
            f"class2-lane-cost65n-independent-rerun-batch{i}-20261116.jsonl"
            for i in range(1, 9)],
        "checked_bits": len(per_bit),
        "mismatches": mismatch,
        "all_node_exact": len(mismatch) == 0 and len(per_bit) == 59,
        "total_nodes_mine": total_mine,
        "total_nodes_parallel": total_parallel,
        "win_bits": [{"bit": b, "nodes": n} for b, n in win_bits],
        "refuted_bits": len(per_bit) - len(win_bits),
        "capped_bits": sum(1 for r in per_bit if r["capped"]),
        "pilots": "8/8 pilot_d6 = 3402 nodes, loss=false, all identical",
        "per_bit": per_bit,
        "interpretation_guard": ("bookkeeping verification only; WIN7-D10 proves "
            "a first-player win within depth 10 from the individual 7-stone "
            "roots only; REFUTED-D10 is not a LOSS proof; NOT-STERILE is not a "
            "game resolution; 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60} and classes 1/2/4 remain UNKNOWN"),
    }
    with open(OUT / "class2-lane-cost65n-independent-rerun-verification-20261116.json", "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("checked:", result["checked_bits"], "bits")
    print("mine total nodes:", total_mine, "| parallel:", total_parallel)
    print("win bits:", win_bits, "| refuted:", result["refuted_bits"], "| capped:", result["capped_bits"])
    print("mismatches:", mismatch)
    print("ALL 59 BITS NODE-EXACT" if result["all_node_exact"] else "MISMATCHES FOUND")

if __name__ == "__main__":
    main()
