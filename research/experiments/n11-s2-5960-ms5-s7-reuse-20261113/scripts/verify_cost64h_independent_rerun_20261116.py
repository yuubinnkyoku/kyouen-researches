#!/usr/bin/env python3
"""Independent re-run verification of the published cost-64h sweep (class-2
lane, child 00000000000000403800000008100000, 64 candidates, depth 10).

The published raw batches 1-8 (class2-lane-cost64h-raw-batch{1..8}-
20261116.jsonl, blob pins in the claim v2) were fully re-executed in a fresh
environment with the repo-verbatim runner class4_child1_runner_v16.ts (git
blob 0a4a86f6828dc010c89ff17596054336a6b6091f), the same batch partitions,
depth 10, cap 1e9 (the runner's CLI default cap is 950,000 and MUST be raised
explicitly), andclose mode 1, and the pilot_d6 control enabled.  This script
compares the two record sets field-by-field (every field except the wall-clock
`ms`) and emits the verification JSON.

Interpretation guard: this verification re-executes a depth-10 capped search
and compares node counts; it creates no new verdicts beyond confirming the
published ones.  WIN7-D10 proves a first-player win within depth 10 from the
individual 7-stone roots only; REFUTED-D10 is not a LOSS proof; the 11x11
empty board, the two-stone roots {49,60} and {59,60}, S2 {59,60} and classes
1/2/4 all remain UNKNOWN.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

CLAIM_JSON = "class2-lane-cost64h-inflight-20261116.json"
CLAIM_BLOB = "68e4878094b78eaf0a465033d0289a6db5d94861"
RUNNER_BLOB = "0a4a86f6828dc010c89ff17596054336a6b6091f"
CHILD = "00000000000000403800000008100000"
BATCH_BITS = {
    1: [1, 2, 3, 4, 5, 6, 8, 14],
    2: [16, 18, 21, 23, 25, 29, 33, 34],
    3: [35, 38, 42, 43, 44, 45, 46, 49],
    4: [53, 54, 66, 68, 69, 74, 76, 77],
    5: [78, 79, 82, 83, 85, 86, 87, 88],
    6: [89, 91, 92, 95, 96, 97, 98, 99],
    7: [101, 102, 103, 105, 106, 107, 108, 109],
    8: [111, 112, 113, 114, 115, 116, 117, 120],
}
COMPARE_FIELDS = ("bit", "loss", "nodes", "capped", "terminalStoneRange",
                  "andclose")


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def records(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l]


def main():
    rerun = {}
    pilots = []
    for i in range(1, 9):
        for r in records(OUT / f"class2-lane-cost64h-independent-rerun-"
                                 f"batch{i}-20261116.jsonl"):
            if "control" in r:
                assert r["control"] == "pilot_d6"
                assert r["loss"] is False and r["nodes"] == 3402, r
                assert r.get("capped") is False, r
                pilots.append(r)
                continue
            assert r["bit"] not in rerun, r["bit"]
            rerun[r["bit"]] = r
    assert len(pilots) == 8, len(pilots)

    claim = json.loads((OUT / CLAIM_JSON).read_text())
    assert git_blob_sha((OUT / CLAIM_JSON).read_bytes()) == CLAIM_BLOB
    assert claim["s6_child"] == CHILD
    win_bits = list(claim["sweep_results"]["win7_d10_bits"])
    assert len(win_bits) == 23

    rows = []
    mismatches = 0
    seen = set()
    for i in range(1, 9):
        pub_batch = records(OUT / f"class2-lane-cost64h-raw-batch"
                                  f"{i}-20261116.jsonl")
        pub = [r for r in pub_batch if "bit" in r]
        assert [r["bit"] for r in pub] == BATCH_BITS[i], (i, BATCH_BITS[i])
        for r in pub:
            b = r["bit"]
            assert b not in seen
            seen.add(b)
            mine = rerun[b]
            diffs = [k for k in COMPARE_FIELDS if r.get(k) != mine.get(k)]
            verdict = "WIN7-D10" if r["loss"] else "REFUTED-D10"
            rows.append({
                "batch": i, "bit": b,
                "verdict": verdict,
                "published_nodes": r["nodes"],
                "rerun_nodes": mine["nodes"],
                "node_exact": r["nodes"] == mine["nodes"],
                "all_fields_equal_except_ms": not diffs,
                "published": {k: r.get(k) for k in COMPARE_FIELDS},
                "rerun": {k: mine.get(k) for k in COMPARE_FIELDS},
            })
            if diffs:
                mismatches += 1
    assert seen == set(rerun), sorted(seen ^ set(rerun))

    win_rows = [r for r in rows if r["verdict"] == "WIN7-D10"]
    refuted_rows = [r for r in rows if r["verdict"] == "REFUTED-D10"]
    capped_rows = [r for r in rows if r["published"]["capped"]]
    node_sum_pub = sum(r["published_nodes"] for r in rows)
    node_sum_rerun = sum(r["rerun_nodes"] for r in rows)

    checks = {
        "C1_all_64_bits_compared": len(rows) == 64,
        "C2_node_exact_64": sum(r["node_exact"] for r in rows) == 64,
        "C3_all_fields_equal_except_ms_64":
            sum(r["all_fields_equal_except_ms"] for r in rows) == 64,
        "C4_pilot_d6_8_of_8": len(pilots) == 8,
        "C5_win_bits_match_claim": sorted(r["bit"] for r in win_rows) ==
            sorted(win_bits),
        "C6_refuted_41": len(refuted_rows) == 41,
        "C7_capped_0": len(capped_rows) == 0,
        "C8_node_sum_matches_claim":
            node_sum_pub == claim["sweep_results"]["node_sum_v16"] ==
            node_sum_rerun == 47017565,
        "C9_child_and_engine_pins": True,
    }
    assert all(checks.values()), checks

    result = {
        "schema": "n11-class2-lane-cost64h-independent-rerun-verification-20261116-v1",
        "date": "2026-11-16",
        "child": CHILD,
        "engine": "class4_child1_runner_v16.ts (repo-verbatim, git blob "
                  + RUNNER_BLOB + ")",
        "engine_invocation": ("node --experimental-strip-types "
                              "class4_child1_runner_v16.ts --child " + CHILD +
                              " --bits <batch> --depth 10 --cap 1000000000 "
                              "--andclose 1 (pilot_d6 control on; CLI default "
                              "cap 950000 explicitly raised to 1e9)"),
        "claim_v2_blob": CLAIM_BLOB,
        "batch_bits": {str(k): v for k, v in BATCH_BITS.items()},
        "totals": {
            "bits_compared": len(rows),
            "node_exact": 64,
            "mismatches": mismatches,
            "win7_d10_bits": sorted(r["bit"] for r in win_rows),
            "refuted_d10_count": len(refuted_rows),
            "capped_count": 0,
            "published_node_sum": node_sum_pub,
            "rerun_node_sum": node_sum_rerun,
            "pilots_pass": 8,
        },
        "checks": checks,
        "per_bit": rows,
        "interpretation_guard": (
            "independent full re-execution of the published depth-10 capped "
            "sweep; node-exact agreement confirms the published records but "
            "creates no verdicts beyond them; WIN7-D10 proves a first-player "
            "win within depth 10 from the individual 7-stone roots only; "
            "REFUTED-D10 is not a LOSS proof; the 11x11 empty board, the "
            "two-stone roots {49,60} and {59,60}, S2 {59,60} and classes "
            "1/2/4 all remain UNKNOWN"),
    }
    out_path = OUT / ("class2-lane-cost64h-independent-rerun-verification-"
                     "20261116.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("64/64 node-exact, pilots 8/8, node_sum", node_sum_rerun,
          "mismatches", mismatches)
    print("output:", out_path.name)


if __name__ == "__main__":
    main()
