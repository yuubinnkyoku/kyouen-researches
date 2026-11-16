#!/usr/bin/env python3
"""v17 full-row re-check of the cost-64f sweep (2026-11-17).

Fourth row of the past-lane v17 re-check queue opened by the 2026-11-17
fbt-saturation defect log: possibly-saturated v16 rows must be re-swept
with the fbt-repaired v17 engine before their REFUTED-D10 verdicts are
reused as planning evidence.

cost-64f: head-1438 row 0000000000000080120a000000800000
(59 swept bits after 5 D4 transfers, 3 WIN7-D10 bits 39/72/107 with
published dual-verified certificates (win3 manifest), 56 REFUTED-D10,
0 capped, total 54,905,391 nodes, heaviest bit 40 at 2,994,208 nodes).

The row is re-executed here from scratch with the fbt-repaired engine
class4_child1_runner_v17.ts (blob c132cc64) using the published batch
partition (8 batches), depth 10, cap 1e9 (published row is 0-capped with
max per-bit 2,994,208 nodes so the cap never binds), --andclose 1, fresh
engine state per candidate, pilot_d6 control per batch, and compared
field-by-field against the published v16 raw batches 1-8. A second full
independent execution (byte-comparison excluding wall-clock ms) anchors
two-run determinism when RUN2 is present.

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
RUN2 = HERE / "o64f-rerun"  # second independent execution (local; optional)

ENGINE_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
CHILD = "0000000000000080120a000000800000"
BATCHES = {
    1: [0, 1, 4, 6, 8, 9, 10, 11],
    2: [14, 18, 22, 26, 31, 32, 33, 39],
    3: [40, 42, 43, 52, 53, 54, 56, 58],
    4: [61, 66, 67, 72, 75, 76, 77, 79],
    5: [85, 86, 87, 88, 90, 94, 95, 96],
    6: [97, 98, 99, 102, 103, 105, 106, 107],
    7: [108, 110, 111, 112, 113, 114, 116, 117],
    8: [118, 119, 120],
}
RAW_BLOBS = {
    1: "e33817e9457ab509789e0092492b6d1640936abc",
    2: "6dd3db9b4456366c0e2adc8c4a6d34cefe22eeec",
    3: "44ad9e809bea1a70c9587304669b055ad4c542df",
    4: "1b62bb8a217f20cb13b7897fb14456255ab48bfb",
    5: "5a89767ccc9fe04ff205a9107aa7e949193efa26",
    6: "c598100ffe3ebe93170ebac5f8b96ec7af4d7b68",
    7: "0d5ed3ad125a247574754a79790e62b2a83913c3",
    8: "6b29c18220595fa47efbcea7aabfdd105f98f2a9",
}
WIN_BITS = [39, 72, 107]
TOTAL_NODES = 54905391
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


def strip_ms(recs):
    return {b: {k: v for k, v in r.items() if k != "ms"} for b, r in recs.items()}


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

    r16 = {}
    r17 = {}
    pilots = []
    mismatch = []
    flips = []
    total_v16 = 0
    total_v17 = 0
    per_bit = []
    for i in range(1, 9):
        raw = OUT / f"class2-lane-cost64f-raw-batch{i}-20261116.jsonl"
        v17 = OUT / f"class2-lane-cost64f-v17-recheck-batch{i}-20261117.jsonl"
        check(f"raw_batch{i}_blob_sha1_matches_main",
              git_blob_sha1(raw) == RAW_BLOBS[i])
        p16, pp = load(raw)
        p17, p17p = load(v17)
        check(f"batch{i}_bit_set_identity",
              sorted(p16) == BATCHES[i] == sorted(p17),
              f"v16={sorted(p16)} v17={sorted(p17)}")
        if pp != {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}:
            mismatch.append(("pilot_v16", i, pp))
        if p17p != {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}:
            mismatch.append(("pilot_v17", i, p17p))
        pilots.append({"batch": i, "v16": pp, "v17": p17p})
        for b in BATCHES[i]:
            a, c = p16[b], p17[b]
            r16[b] = a
            r17[b] = c
            total_v16 += a["nodes"]
            total_v17 += c["nodes"]
            for k in FIELDS:
                if a[k] != c[k]:
                    mismatch.append((i, b, k, a[k], c[k]))
            if a["loss"] != c["loss"]:
                flips.append({"bit": b, "v16_loss": a["loss"], "v16_nodes": a["nodes"],
                              "v17_loss": c["loss"], "v17_nodes": c["nodes"]})
            per_bit.append({"batch": i, "bit": b, "v17_loss": c["loss"],
                            "v17_nodes": c["nodes"], "v16_nodes": a["nodes"]})

    check("all_8_pilots_identity_3402",
          all(p["v16"] == p["v17"] == {"control": "pilot_d6", "loss": False,
                                       "nodes": 3402, "capped": False} for p in pilots))
    check("all_bits_field_identical", len(mismatch) == 0, f"mismatches={mismatch}")
    check("nodes_total_identity",
          total_v16 == total_v17 == TOTAL_NODES,
          f"v16={total_v16} v17={total_v17} published={TOTAL_NODES}")
    win_bits_v17 = sorted(b for b in r17 if r17[b]["loss"])
    check("win_bits_unchanged", win_bits_v17 == WIN_BITS,
          f"v17={win_bits_v17} published={WIN_BITS}")
    check("verdict_flips_zero", len(flips) == 0, f"flips={flips}")

    determinism = {"status": "skipped", "detail": f"RUN2 dir absent: {RUN2}"}
    if RUN2.is_dir():
        r2 = {}
        d_ok = True
        d_detail = []
        for i in range(1, 9):
            p2, p2p = load(RUN2 / f"v17-batch{i}.jsonl")
            for b in BATCHES[i]:
                r2[b] = p2[b]
            if p2p != {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}:
                d_ok = False
                d_detail.append(("pilot", i, p2p))
        for b in sorted(r17):
            if {k: v for k, v in r17[b].items() if k != "ms"} != \
               {k: v for k, v in r2[b].items() if k != "ms"}:
                d_ok = False
                d_detail.append((b, r17[b], r2[b]))
        determinism = {"status": "pass" if d_ok else "fail",
                       "detail": "two full independent executions agree on every bit and pilot (ms excluded)" if d_ok else str(d_detail[:5])}
        check("determinism_second_run_identical", d_ok)

    result = {
        "schema": "n11-class2-lane-cost64f-v17-full-row-recheck-20261117-v1",
        "date": "2026-11-17",
        "method": ("fbt-repaired v17 engine (class4_child1_runner_v17.ts, blob "
                   "c132cc64) re-executed all 59 swept bits of the row from "
                   "scratch with the published batch partition (8 batches), "
                   "depth 10, cap 1e9 (published row is 0-capped with max "
                   "per-bit 2,994,208 nodes so the cap never binds), "
                   "--andclose 1, fresh engine state per candidate, pilot_d6 "
                   "control per batch; compared field-by-field against the "
                   "published v16 raw batches 1-8; second independent full "
                   "execution anchors two-run determinism"),
        "child": CHILD,
        "engine_blob_sha1": ENGINE_BLOB,
        "checked_bits": len(per_bit),
        "mismatches": mismatch,
        "verdict_flips": flips,
        "win_bits_v17": win_bits_v17,
        "total_nodes_v16": total_v16,
        "total_nodes_v17": total_v17,
        "published_win_bits": WIN_BITS,
        "published_total_nodes": TOTAL_NODES,
        "determinism_rerun": determinism,
        "per_bit": per_bit,
        "checks": checks,
        "all_checks_pass": ok,
        "interpretation_guard": ("bookkeeping verification only; WIN7-D10 proves "
            "a first-player win within depth 10 from the individual 7-stone "
            "roots only; REFUTED-D10 is not a LOSS proof; row identity is "
            "engine-consistency evidence, not a game resolution; 11x11 empty "
            "board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes "
            "1/2/4 remain UNKNOWN"),
    }
    dest = OUT / "class2-lane-cost64f-v17-full-row-recheck-20261117.json"
    with open(dest, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("checks:", len(checks), "all pass:", ok)
    print("bits", len(per_bit), "total16", total_v16, "total17", total_v17,
          "wins", win_bits_v17, "mismatches", len(mismatch), "determ", determinism["status"])
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
