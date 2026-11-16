#!/usr/bin/env python3
"""v17 full-row re-checks of the cost-64d and cost-64g sweeps (2026-11-17).

Third step of the past-lane v17 re-check queue opened by the 2026-11-17
fbt-saturation log (research/log/2026-11-17-n11-class2-lane-cost76c-
fbt-saturation-defect-v17-repair-and-resweep.md): saturated v15/v16 searches
are unreliable in both verdict directions, so REFUTED-D10 verdicts of
possibly-saturated rows must be re-swept with the fbt-repaired v17 engine
before being reused as planning evidence.

cost-64d: head-1419 best own-closable class-2 child
00000000000000403800000008002000 (64 candidates, 23 WIN7-D10 bits with
dual-verified certificates via win23 manifest 244e4b61, 41 REFUTED-D10,
0 capped, total 64,291,757 nodes; folded at c7a849e0 onto head 1419->1435).
cost-64g: head-1438 census cheapest open row
00000000000100003800000008080000 (59 swept bits after 5 transfers, 1 WIN7-D10
bit 89 with a dual-verified certificate, 58 REFUTED-D10, 0 capped, total
33,505,865 nodes; folded at f14f8bdb onto head 1438->1441).

Both rows are re-executed here from scratch with the fbt-repaired engine
class4_child1_runner_v17.ts (blob c132cc64) using the published batch
partitions (8 batches each), depth 10, cap 1e9 (both published rows report
0 capped bits and max per-bit 3,457,163 / 3,672,017 nodes, so the cap never
binds), --andclose 1, pilot_d6 control per batch invocation, and compared
field-by-field against the published v16 raw batches 1-8.

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
    "64d": {
        "child": "00000000000000403800000008002000",
        "batches": {
            1: [0, 1, 2, 3, 4, 5, 6, 8],
            2: [9, 10, 11, 16, 17, 21, 25, 29],
            3: [30, 32, 38, 42, 43, 44, 46, 53],
            4: [54, 66, 69, 74, 75, 76, 78, 79],
            5: [80, 83, 85, 86, 87, 88, 89, 92],
            6: [95, 96, 97, 98, 99, 100, 101, 102],
            7: [103, 105, 106, 107, 108, 109, 110, 111],
            8: [113, 114, 115, 116, 117, 118, 119, 120],
        },
        "raw_blobs": {
            1: "0f93456cfddb05a6fe3c1f236f84c5df245e4d4b",
            2: "c41d88f17c836a3517f6b61aba30a6abae958a1e",
            3: "d45d8cfa7b855db11b8a34e7700ba316e0914180",
            4: "bba937a0526e9ce16e096a378c72e15b9d8718f4",
            5: "12a379c4d1a36294a1daaee94a127ad0653f7314",
            6: "a0d86791e3846878022c4c33b8294f81f024593a",
            7: "6d34099b4103f84bb65941513551590319060afc",
            8: "ce86d0fb24fbbb63e39efbbc47c821965b9a4188",
        },
        "published": {"win_bits": [0, 1, 2, 11, 16, 30, 32, 43, 53, 66, 69, 75,
                                    79, 86, 92, 95, 98, 106, 107, 109, 111, 113, 120],
                      "total_nodes": 64291757,
                      "sweep_commit": "f38be6d6", "fold_commit": "c7a849e0"},
    },
    "64g": {
        "child": "00000000000100003800000008080000",
        "batches": {
            1: [1, 2, 4, 6, 7, 8, 9, 11],
            2: [15, 16, 20, 21, 22, 24, 25, 33],
            3: [34, 38, 42, 43, 44, 45, 52, 54],
            4: [66, 67, 68, 70, 71, 73, 75, 76],
            5: [78, 79, 81, 86, 88, 89, 90, 94],
            6: [97, 98, 99, 100, 101, 102, 103, 105],
            7: [106, 107, 108, 109, 110, 112, 113, 114],
            8: [117, 118, 120],
        },
        "raw_blobs": {
            1: "873807ad7015ee8865b00b93d73ea23a92d2140d",
            2: "e9b0b41bbf9b4602a1d89bf8be0e930db2a4d0ee",
            3: "f22888df77cb35d2ac371e6857f8c3b3b15c3084",
            4: "a8ba871fbfe981ad22d0292738734ee080a66a08",
            5: "07809fd4cd15e9c341528a24b33a70d95167e267",
            6: "13088f70b66e5e2506bd9f9ad3b5b680012a85bb",
            7: "fcc2786d8431a5fd2ce417c91d9589736a029dbb",
            8: "1f2ea9d81a5ede641f33a4fa6dd1a96dde15fd6e",
        },
        "published": {"win_bits": [89], "total_nodes": 33505865,
                      "sweep_commit": "2a0b46a2", "fold_commit": "f14f8bdb"},
    },
}
ENGINE_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
FIELDS = ("loss", "nodes", "capped", "terminalStoneRange", "andclose")


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
        mismatch = []
        flips = []
        total_v16 = 0
        total_v17 = 0
        per_bit = []
        win_bits_v17 = []
        pilots_ok = True
        for i in range(1, 9):
            raw = OUT / f"class2-lane-cost{row}-raw-batch{i}-20261116.jsonl"
            v17 = OUT / f"class2-lane-cost{row}-v17-recheck-batch{i}-20261117.jsonl"
            check(f"{row}_raw_batch{i}_blob_sha1_matches_main",
                  git_blob_sha1(raw) == spec["raw_blobs"][i])
            p16, pp = load(raw)
            p17, p17p = load(v17)
            check(f"{row}_batch{i}_bit_set_identity",
                  sorted(p16) == spec["batches"][i] == sorted(p17),
                  f"v16={sorted(p16)} v17={sorted(p17)}")
            if pp != {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}:
                pilots_ok = False
                mismatch.append(("pilot_v16", i, pp))
            if p17p != {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}:
                pilots_ok = False
                mismatch.append(("pilot_v17", i, p17p))
            for b in spec["batches"][i]:
                a, c = p16[b], p17[b]
                total_v16 += a["nodes"]
                total_v17 += c["nodes"]
                if c["loss"] is True:
                    win_bits_v17.append(b)
                for k in FIELDS:
                    if a[k] != c[k]:
                        mismatch.append((i, b, k, a[k], c[k]))
                if a["loss"] != c["loss"]:
                    flips.append({"bit": b, "v16_loss": a["loss"], "v16_nodes": a["nodes"],
                                  "v17_loss": c["loss"], "v17_nodes": c["nodes"]})
                per_bit.append({"batch": i, "bit": b, "v17_loss": c["loss"],
                                "v17_nodes": c["nodes"], "v16_nodes": a["nodes"]})
        check(f"{row}_all_8_pilots_identity_3402", pilots_ok)
        check(f"{row}_all_bits_field_identical", len(mismatch) == 0,
              f"mismatches={mismatch}")
        check(f"{row}_nodes_total_identity", total_v16 == total_v17 == spec["published"]["total_nodes"],
              f"v16={total_v16} v17={total_v17} published={spec['published']['total_nodes']}")
        check(f"{row}_win_bits_unchanged",
              sorted(win_bits_v17) == spec["published"]["win_bits"],
              f"v17={sorted(win_bits_v17)} published={spec['published']['win_bits']}")
        check(f"{row}_verdict_flips_zero", len(flips) == 0, f"flips={flips}")
        row_results[row] = {
            "child": spec["child"],
            "checked_bits": len(per_bit),
            "field_identical_bits": len(per_bit) - sum(1 for m in mismatch if len(m) == 5),
            "mismatches": mismatch,
            "verdict_flips": flips,
            "win_bits_v17": sorted(win_bits_v17),
            "total_nodes_v16": total_v16,
            "total_nodes_v17": total_v17,
            "published_evidence": spec["published"],
            "per_bit": per_bit,
        }

    result = {
        "schema": "n11-class2-lane-cost64d64g-v17-full-row-rechecks-20261117-v1",
        "date": "2026-11-17",
        "method": ("fbt-repaired v17 engine (class4_child1_runner_v17.ts, blob "
                   "c132cc64) re-executed all swept bits of both rows from "
                   "scratch with the published batch partitions, depth 10, "
                   "cap 1e9 (published rows are 0-capped with max per-bit "
                   "3,457,163 / 3,672,017 nodes so the cap never binds), "
                   "--andclose 1, fresh engine state per candidate, pilot_d6 "
                   "control per batch; compared field-by-field against the "
                   "published v16 raw batches 1-8"),
        "engine_blob_sha1": ENGINE_BLOB,
        "rows": row_results,
        "checks": checks,
        "all_checks_pass": ok,
        "interpretation_guard": ("bookkeeping verification only; WIN7-D10 proves "
            "a first-player win within depth 10 from the individual 7-stone "
            "roots only; REFUTED-D10 is not a LOSS proof; unsaturated row "
            "identity is engine-consistency evidence, not a game resolution; "
            "11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} "
            "and classes 1/2/4 remain UNKNOWN"),
    }
    dest = OUT / "class2-lane-cost64d64g-v17-full-row-rechecks-20261117.json"
    with open(dest, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("checks:", len(checks), "all pass:", ok)
    for row in ROWS:
        r = row_results[row]
        print(row, "bits", r["checked_bits"], "total16", r["total_nodes_v16"],
              "total17", r["total_nodes_v17"], "wins", r["win_bits_v17"],
              "mismatches", len(r["mismatches"]))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
