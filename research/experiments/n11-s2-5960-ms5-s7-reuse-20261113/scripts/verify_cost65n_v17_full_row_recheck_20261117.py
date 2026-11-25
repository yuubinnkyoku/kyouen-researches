#!/usr/bin/env python3
"""v17 full-row re-check of the cost-65n sweep (2026-11-17).

The 2026-11-17 fbt-saturation log (research/log/2026-11-17-
n11-class2-lane-cost76c-fbt-saturation-defect-v17-repair-and-resweep.md)
found that the v15/v16 fbtOR fb cache silently drops circle-blocking mask
updates once the fb table saturates (>= ~1.16e5 unique triples), which
flipped verdicts on saturated searches (cost76c bit 113 WIN -> REFUTED) and
left past REFUTED-D10 verdicts of possibly-saturated rows unusable as
planning evidence until re-swept with the repaired v17 engine. The log
explicitly queues cost-65n among the rows to re-check before its verdicts
are reused.

This script performs that re-check for cost-65n: the head-1441 cheapest open
row 00000000000000801202010000800000 (cost 65, shared class-2 parent
00000000000000003800000008002000; parallel-lane sweep commits 60c97b93
batches 1-4 and e728c47e batches 5-8, claim v2 6e85762f; independent v16
rerun verification 0c237017 already reproduced all 59 bits node-exact with
the *buggy* v16). All 59 swept bits are re-executed here from scratch with
the fbt-repaired engine class4_child1_runner_v17.ts (blob c132cc64) using
the published batch partitions, depth 10, cap 1e7, --andclose 1, pilot_d6
control 3402 per batch invocation.

The comparison asserts bit-set identity per batch, pilot identity for all 8
batch invocations, and bit/loss/nodes/capped/terminalStoneRange/andclose
identity for every one of the 59 swept bits, plus the nodes total.
Interpretation guard: bookkeeping verification only; WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone roots only
(bits 90/117 are additionally covered by dual-verified certificates);
REFUTED-D10 is not a LOSS proof; NOT-STERILE is not a game resolution;
11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes
1/2/4 remain UNKNOWN.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SCR = HERE / "scripts"

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
ENGINE = "class4_child1_runner_v17.ts"
ENGINE_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
RAW_BLOBS = {
    1: "8361a5be1cfa801947ba1e9ec48601f188f7cf6e",
    2: "4e2bbc51baeb4a65aadb3e9ece6868a9494f2eb4",
    3: "c613f71462a82f74e0ed0923c9b5996966b9ef01",
    4: "35b53b20b05d1e725aafe7980572e8d1d034d4bb",
    5: "c4f810a23f0081ccaa97a5d88f3a79c908fa11c6",
    6: "32545b321511f19b75688871d9960ea09efa3e04",
    7: "fe5a98c31115e8885385399200b47cec2adadb20",
    8: "278e69ba3854b57d2e8a032bd6770352d3a18261",
}
V17_FILES = {
    i: f"class2-lane-cost65n-v17-recheck-batch{i}-20261117.jsonl" for i in range(1, 9)
}
RAW_FILES = {
    i: f"class2-lane-cost65n-raw-batch{i}-20261116.jsonl" for i in range(1, 9)
}
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
        checks.append({"check": name, "pass": bool(cond), "detail": detail if detail else ("" if cond else "FAILED")})
        if not cond:
            ok = False

    check("engine_blob_sha1_matches_pinned_c132cc64",
          git_blob_sha1(SCR / ENGINE) == ENGINE_BLOB)
    for i in range(1, 9):
        check(f"raw_batch{i}_blob_sha1_matches_main", git_blob_sha1(OUT / RAW_FILES[i]) == RAW_BLOBS[i])

    mismatch = []
    total_v16 = 0
    total_v17 = 0
    per_bit = []
    win_bits = []
    pilots_ok = True
    for i in range(1, 9):
        p16, pp = load(OUT / RAW_FILES[i])
        p17, p17p = load(OUT / V17_FILES[i])
        check(f"batch{i}_bit_set_identity", sorted(p16) == BATCH_BITS[i] == sorted(p17),
              f"v16={sorted(p16)} v17={sorted(p17)}")
        if pp != {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}:
            pilots_ok = False
            mismatch.append(("pilot_v16", i, pp))
        if p17p != {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}:
            pilots_ok = False
            mismatch.append(("pilot_v17", i, p17p))
        for b in BATCH_BITS[i]:
            a, c = p16[b], p17[b]
            total_v16 += a["nodes"]
            total_v17 += c["nodes"]
            if c["loss"] is True:
                win_bits.append(b)
            for k in FIELDS:
                if a[k] != c[k]:
                    mismatch.append((i, b, k, a[k], c[k]))
            per_bit.append({
                "batch": i, "bit": b, "loss": c["loss"], "nodes": c["nodes"],
                "capped": c["capped"], "terminalStoneRange": c["terminalStoneRange"],
                "andclose": c["andclose"], "v16_nodes": a["nodes"],
            })
    check("all_8_pilot_d6_identity_3402", pilots_ok)
    check("all_59_bits_field_identical_v17_vs_v16", len(mismatch) == 0,
          f"mismatches={mismatch}")
    check("nodes_total_identity", total_v16 == total_v17,
          f"v16={total_v16} v17={total_v17}")
    check("win_bits_unchanged_90_117", win_bits == [90, 117], f"v17 win bits={win_bits}")
    check("no_capped_bits", all(not r["capped"] for r in per_bit))
    max_bit = max(per_bit, key=lambda r: r["nodes"])

    result = {
        "schema": "n11-class2-lane-cost65n-v17-full-row-recheck-20261117-v1",
        "date": "2026-11-17",
        "child": CHILD,
        "row": ("head-1441 cheapest open row, cost 65, shared class-2 parent "
                "00000000000000003800000008002000, 65 legal candidates, "
                "6 pre-swept REFUTED transfers excluded, 59 swept bits"),
        "method": ("fbt-repaired v17 engine (class4_child1_runner_v17.ts, blob "
                   "c132cc64, probe-exhaustion fallback: compute-and-apply "
                   "without caching) re-executed all 59 swept bits from scratch "
                   "with the published batch partitions (8 batches), depth 10, "
                   "cap 1e7, --andclose 1, fresh engine state per candidate, "
                   "pilot_d6 control per batch; compared field-by-field against "
                   "the parallel lane's published v16 raw batches 1-8"),
        "engine_blob_sha1": ENGINE_BLOB,
        "published_raw_blob_sha1": {RAW_FILES[i]: RAW_BLOBS[i] for i in range(1, 9)},
        "v17_raw_files": [V17_FILES[i] for i in range(1, 9)],
        "previous_evidence": {
            "sweep_commits": {"batches_1_4": "60c97b93", "batches_5_8": "e728c47e",
                              "claim_v2": "6e85762f"},
            "independent_v16_rerun_verification": "0c237017 (59/59 node-exact, buggy v16)",
            "win_certificates": ("bits 90/117 dual-verified (BigInt + Bareiss), "
                                 "blind re-extraction byte-identical (e01093dc)"),
        },
        "checked_bits": len(per_bit),
        "all_field_identical": len(mismatch) == 0,
        "mismatches": mismatch,
        "total_nodes_v16": total_v16,
        "total_nodes_v17": total_v17,
        "win_bits_v17": win_bits,
        "refuted_bits_v17": len(per_bit) - len(win_bits),
        "capped_bits": 0,
        "max_nodes_bit": {"bit": max_bit["bit"], "nodes": max_bit["nodes"]},
        "saturation_conclusion": ("all 59 bits reproduce the published v16 "
            "records exactly (nodes included), so the whole row is "
            "fb-unsaturated under the v17 probe-exhaustion fallback; the "
            "measured unsaturation ceiling rises from 3.5M (cost64h/64e) to "
            "5,654,046 nodes/bit (bit 26; bit 9 at 5,075,917 also unsaturated)"),
        "determinism": ("two full 8-batch runs in this lane produced identical "
                        "bit/loss/nodes/capped/terminalStoneRange/andclose for "
                        "all 59 bits and identical pilots (ms differs only)"),
        "checks": checks,
        "all_checks_pass": ok,
        "per_bit": per_bit,
        "interpretation_guard": ("bookkeeping verification only; WIN7-D10 proves "
            "a first-player win within depth 10 from the individual 7-stone "
            "roots only; REFUTED-D10 is not a LOSS proof; unsaturated row "
            "identity is engine-consistency evidence, not a game resolution; "
            "11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} "
            "and classes 1/2/4 remain UNKNOWN"),
    }
    dest = OUT / "class2-lane-cost65n-v17-full-row-recheck-20261117.json"
    with open(dest, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("checks:", len(checks), "all pass:", ok)
    print("total v16:", total_v16, "| v17:", total_v17)
    print("win bits:", win_bits, "| mismatches:", mismatch)
    print("max nodes bit:", max_bit["bit"], max_bit["nodes"])
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
