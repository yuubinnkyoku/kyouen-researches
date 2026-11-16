#!/usr/bin/env python3
"""v17 full-row re-checks of the cost-76d and cost-77e sweeps (2026-11-17).

Fifth step of the past-lane v17 re-check queue opened by the 2026-11-17
fbt-saturation defect log: possibly-saturated v16 rows must be re-swept
with the fbt-repaired v17 engine before their REFUTED-D10 verdicts are
reused as planning evidence.

cost-76d: head-1419-folded row child 00000000040000003800080008000000
(76 swept bits, 2 WIN7-D10 bits 19/49 with published dual-verified
certificates, 74 REFUTED-D10, 0 capped, published total 96,246,915
nodes, published heaviest bit 112 at 10,150,705 nodes).
cost-77e: head-1405-based row child 00000000040000809002000000004000
(77 swept bits, 2 WIN7-D10 bits 37/69 with published dual-verified
certificates, 75 REFUTED-D10, 0 capped, published total 116,019,458
nodes, published heaviest bit 33 at 11,599,283 nodes).

Both rows are the heaviest published class-2 sweeps re-checked so far.
Both are re-executed here from scratch with the fbt-repaired engine
class4_child1_runner_v17.ts (blob c132cc64) using the published batch
partitions (10 batches each), depth 10, cap 1e9 (both published rows are
0-capped so the cap never binds), --andclose 1, fresh engine state per
candidate, pilot_d6 control per batch, and compared field-by-field
against the published v16 raw batches 1-10. Second full independent
executions (byte-comparison excluding wall-clock ms) anchor two-run
determinism when the RUN2 directories are present.

Pass criteria: verdict flips 0, WIN bits unchanged, bit-set identity,
pilot identity, determinism pass. Node-count corrections (v16 -> v17)
are recorded as saturation findings, not failures.

77e child-hex incident: an earlier local 77e attempt was executed with
the mistyped child 00000000040000809092000000004000 (one hex digit);
its outputs were discarded before this re-check. The true child was
re-derived from the published sweep record
class2-lane-cost77e-sweep-20261116.json (s6_child field) and confirmed
by the published certificate root hexes (child|1<<bit).

Interpretation guard: bookkeeping verification only; WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone roots only;
REFUTED-D10 is not a LOSS proof; 11x11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain UNKNOWN.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SCR = HERE / "scripts"

ROWS = {
    "76d": {
        "child": "00000000040000003800080008000000",
        "batches": {
            1: [0, 1, 2, 3, 4, 5, 6, 7],
            2: [8, 9, 10, 11, 12, 15, 16, 17],
            3: [18, 19, 20, 21, 23, 24, 25, 29],
            4: [30, 31, 32, 35, 38, 41, 42, 44],
            5: [45, 46, 49, 52, 53, 66, 67, 68],
            6: [70, 71, 72, 73, 75, 76, 78, 80],
            7: [81, 83, 85, 86, 87, 88, 89, 92],
            8: [93, 94, 98, 99, 102, 103, 104, 105],
            9: [106, 107, 109, 110, 111, 112, 113, 116],
            10: [117, 118, 119, 120],
        },
        "raw_blobs": {
            1: "d3c9ae3690c7c74e2b85fb4a84e0b02bb0ee06fb",
            2: "9144839aefc28cf4fd78710b1c130c0a0fe80f16",
            3: "8dae0d02ceea0b80ba1ecb0f853778b7dc158c23",
            4: "3c1e4557b97cc7f5cb2eb51cb79a9b02254ff11f",
            5: "c0c152d58a16aa9377ef8f365508699e32c71c94",
            6: "dbf10a3064c52472fddfc204fa4f0c00eaf6772e",
            7: "57c0eda0ffd3023ef44862c83c2eb547c7e4c584",
            8: "f4862407930d5658987dc4bc1fe9766c204ecf0e",
            9: "bc32bed989265468841bb076ccfa6328e94514e3",
            10: "8855f2d6f3821c1cd7d7e33eed6d17a63ecac3ee",
        },
        "run2": HERE / "o76d-rerun",
        "published_win_bits": [19, 49],
        "published_total_nodes": 96246915,
    },
    "77e": {
        "child": "00000000040000809002000000004000",
        "batches": {
            1: [0, 1, 2, 3, 4, 6, 7, 8],
            2: [9, 10, 11, 15, 17, 18, 19, 20],
            3: [22, 23, 25, 28, 29, 30, 31, 32],
            4: [33, 34, 37, 41, 42, 43, 44, 45],
            5: [46, 47, 48, 53, 54, 56, 57, 59],
            6: [61, 62, 64, 65, 67, 68, 69, 70],
            7: [75, 76, 77, 78, 80, 85, 87, 88],
            8: [92, 94, 95, 96, 98, 99, 101, 103],
            9: [105, 106, 107, 108, 109, 110, 111, 112],
            10: [114, 116, 117, 119, 120],
        },
        "raw_blobs": {
            1: "2034e39709d598827d912074b15dc6a61df2d5ad",
            2: "cb883d07206e0f5ff4935ff4d36bbbf4addb7202",
            3: "a64d7a19456c11f79e473f9df08c785007867d75",
            4: "32d9d9582a848c0e65e91c56dfdab40de2fa74ee",
            5: "489f13e374f267fbc0a3a798e631e4fb543b4fc7",
            6: "5846d0470e43dc2ce49cecace0e6d628ff795765",
            7: "106ac2387f7d302dfcc5963abf26ca20174ec2bb",
            8: "3956be4dcc89009f07fd6e6ddb1eba8d186a8b54",
            9: "59df74f2902e8b45dadcef9ee451c27fbe3ff953",
            10: "d9f4fa3c5aa85fe9e408f45a88396d1edcb535c2",
        },
        "run2": HERE / "o77e-rerun",
        "published_win_bits": [37, 69],
        "published_total_nodes": 116019458,
    },
}
ENGINE_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
FIELDS = ("loss", "nodes", "capped", "terminalStoneRange", "andclose")
PILOT = {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}


def git_blob_sha1(path):
    data = Path(path).read_bytes()
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


def load(path):
    recs = {}
    pilot = None
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if "bit" in d:
            recs[d["bit"]] = d
        elif d.get("control") == "pilot_d6":
            pilot = d
    return recs, pilot


def norm(rec):
    return {k: v for k, v in rec.items() if k != "ms"}


def main():
    checks = []
    ok = True

    def check(name, cond, detail=None):
        nonlocal ok
        checks.append({"check": name, "pass": bool(cond),
                       "detail": detail if detail else ("" if cond else "FAILED")})
        if not cond:
            ok = False

    check("engine_blob_sha1_matches_pinned_c132cc64",
          git_blob_sha1(SCR / "class4_child1_runner_v17.ts") == ENGINE_BLOB)

    row_results = {}
    for row, spec in ROWS.items():
        mismatch_fields = []
        node_corrections = []
        flips = []
        total_v16 = 0
        total_v17 = 0
        win_bits_v17 = []
        per_bit = []
        pilots_ok = True
        for i in range(1, 11):
            raw = OUT / f"class2-lane-cost{row}-raw-batch{i}-20261116.jsonl"
            v17 = OUT / f"class2-lane-cost{row}-v17-recheck-batch{i}-20261117.jsonl"
            check(f"{row}_raw_batch{i}_blob_sha1_matches_main",
                  git_blob_sha1(raw) == spec["raw_blobs"][i])
            p16, pp = load(raw)
            p17, p17p = load(v17)
            check(f"{row}_batch{i}_bit_set_identity",
                  sorted(p16) == spec["batches"][i] == sorted(p17),
                  f"v16={sorted(p16)} v17={sorted(p17)}")
            if pp != PILOT or p17p != PILOT:
                pilots_ok = False
                mismatch_fields.append(("pilot", i, pp, p17p))
            for b in spec["batches"][i]:
                a, c = p16[b], p17[b]
                total_v16 += a["nodes"]
                total_v17 += c["nodes"]
                if c["loss"] is True:
                    win_bits_v17.append(b)
                for k in FIELDS:
                    if a[k] != c[k]:
                        mismatch_fields.append((i, b, k, a[k], c[k]))
                if a["nodes"] != c["nodes"]:
                    node_corrections.append({
                        "bit": b, "v16_nodes": a["nodes"], "v17_nodes": c["nodes"],
                        "delta": c["nodes"] - a["nodes"],
                        "verdict_unchanged": a["loss"] == c["loss"]})
                if a["loss"] != c["loss"]:
                    flips.append({"bit": b, "v16_loss": a["loss"], "v16_nodes": a["nodes"],
                                  "v17_loss": c["loss"], "v17_nodes": c["nodes"]})
                per_bit.append({"batch": i, "bit": b, "v17_loss": c["loss"],
                                "v17_nodes": c["nodes"], "v16_nodes": a["nodes"]})
        check(f"{row}_all_10_pilots_identity_3402", pilots_ok)
        check(f"{row}_terminal_range_andclose_only_fields_differ_as_nodes",
              all(m[2] == "nodes" for m in mismatch_fields if len(m) == 5),
              f"non-node field mismatches={[m for m in mismatch_fields if len(m) == 5 and m[2] != 'nodes']}")
        check(f"{row}_win_bits_unchanged",
              sorted(win_bits_v17) == spec["published_win_bits"],
              f"v17={sorted(win_bits_v17)} published={spec['published_win_bits']}")
        check(f"{row}_verdict_flips_zero", len(flips) == 0, f"flips={flips}")

        determinism = {"status": "skipped", "detail": f"RUN2 dir absent: {spec['run2']}"}
        if spec["run2"].is_dir():
            d_ok = True
            d_detail = []
            for i in range(1, 11):
                v17 = OUT / f"class2-lane-cost{row}-v17-recheck-batch{i}-20261117.jsonl"
                p1, p1p = load(v17)
                p2, p2p = load(spec["run2"] / f"v17-batch{i}.jsonl")
                if p1p != PILOT or p2p != PILOT:
                    d_ok = False
                    d_detail.append(("pilot", i, p1p, p2p))
                for b in spec["batches"][i]:
                    if norm(p1[b]) != norm(p2[b]):
                        d_ok = False
                        d_detail.append((b, p1[b], p2[b]))
            determinism = {"status": "pass" if d_ok else "fail",
                           "detail": "two full independent executions agree on every bit and pilot (ms excluded)" if d_ok else str(d_detail[:5])}
            check(f"{row}_determinism_second_run_identical", d_ok)
        row_results[row] = {
            "child": spec["child"],
            "checked_bits": len(per_bit),
            "node_corrections": node_corrections,
            "non_node_field_mismatches": [m for m in mismatch_fields if len(m) == 5 and m[2] != "nodes"],
            "verdict_flips": flips,
            "win_bits_v17": sorted(win_bits_v17),
            "total_nodes_v16": total_v16,
            "total_nodes_v17": total_v17,
            "published_win_bits": spec["published_win_bits"],
            "published_total_nodes": spec["published_total_nodes"],
            "per_bit": per_bit,
            "determinism_rerun": determinism,
        }

    result = {
        "schema": "n11-class2-lane-cost76d77e-v17-full-row-rechecks-20261117-v1",
        "date": "2026-11-17",
        "method": ("fbt-repaired v17 engine (class4_child1_runner_v17.ts, blob "
                   "c132cc64) re-executed all swept bits of both rows from "
                   "scratch with the published batch partitions (10 batches "
                   "each), depth 10, cap 1e9 (both published rows are 0-capped), "
                   "--andclose 1, fresh engine state per candidate, pilot_d6 "
                   "control per batch; compared field-by-field against the "
                   "published v16 raw batches 1-10; second independent full "
                   "executions anchor two-run determinism"),
        "engine_blob_sha1": ENGINE_BLOB,
        "rows": row_results,
        "checks": checks,
        "all_checks_pass": ok,
        "interpretation_guard": ("bookkeeping verification only; WIN7-D10 proves "
            "a first-player win within depth 10 from the individual 7-stone "
            "roots only; REFUTED-D10 is not a LOSS proof; node-count "
            "corrections are engine-consistency bookkeeping, not a game "
            "resolution; 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60} and classes 1/2/4 remain UNKNOWN"),
    }
    dest = OUT / f"class2-lane-cost76d77e-v17-full-row-rechecks-20261117.json"
    with open(dest, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("checks:", len(checks), "all pass:", ok)
    for row in ROWS:
        r = row_results[row]
        print(row, "bits", r["checked_bits"], "total16", r["total_nodes_v16"],
              "total17", r["total_nodes_v17"], "wins", r["win_bits_v17"],
              "corrections", len(r["node_corrections"]), "flips", len(r["verdict_flips"]))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
