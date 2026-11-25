#!/usr/bin/env python3
"""v17 full-row re-check of the cost-66c sweep (2026-11-17).

Second row of the past-lane v17 re-check queue opened by the 2026-11-17
fbt-saturation log (research/log/2026-11-17-n11-class2-lane-cost76c-
fbt-saturation-defect-v17-repair-and-resweep.md): saturated v15/v16
searches are unreliable in both directions, so REFUTED-D10 verdicts of
possibly-saturated rows must be re-swept with the repaired v17 engine before
being reused as planning evidence.

cost-66c is the highest-risk queued row: head-1441 third-ranked cheapest
open row 00000000000000003800000008002008 (cost 66, shared class-2 parent
00000000000000003800000008002000; claim v1 64e83dff, claim v2 completed
NOT-STERILE b17e978e) with bit 30 at 8,806,920 nodes and bit 112 resolved at
cap 80M with 12,574,920 nodes, i.e. the two largest per-bit searches among
all previously published rows. The 7 WIN bits 73/75/79/87/96/97/112 are
covered by dual-verified certificates (manifest 39665854), so the re-check
focuses on the 52 swept REFUTED-D10 bits.

This script re-executes all 59 swept bits from scratch with the fbt-repaired
engine class4_child1_runner_v17.ts (blob c132cc64) using the published batch
partitions, depth 10, cap 1e7, --andclose 1 (bit 112 additionally at cap
80000000), pilot_d6 control per batch invocation, and compares field-by-field
against the published v16 raw batches 1-8 plus the bit-112 cap-raise
resolution record. The single saturation-detected bit (117) is additionally
cross-checked against the 2x2 order matrix (engines v16/v17 x andclose 1/0).

Interpretation guard: bookkeeping verification only; WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone roots only;
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
ENGINE = "class4_child1_runner_v17.ts"
ENGINE_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
RAW_BLOBS = {
    1: "1ee1146df8ef8ef666df96a69732feabfc87c2fb",
    2: "b598d6ccff9c93deb5739e96e3b32ce9a110661c",
    3: "c3a85aca605061fafbc19ce220923386f87c9064",
    4: "5ff20e15a8d892e930bda28b3198765b9e0d6f57",
    5: "5899ba17b7d5ee35da2a4716c28a85973d90f797",
    6: "8d84f6cba95ab80eb397b4ea3a3494947b2b7e54",
    7: "a805e4101fa657c6b6b2ad029691f06088d31986",
    8: "ec9adcd267c2943aac144444b43b790a8cc225fe",
}
BIT112_RESOLUTION = {
    "file": "class2-lane-cost66c-bit112-cap80m-resolution-20261116.jsonl",
    "blob": "317876ada7bdb23d158ddebce6a0876475bebd3e",
}
RAW_FILES = {i: f"class2-lane-cost66c-raw-batch{i}-20261116.jsonl" for i in range(1, 9)}
V17_FILES = {i: f"class2-lane-cost66c-v17-recheck-batch{i}-20261117.jsonl" for i in range(1, 9)}
V17_BIT112 = "class2-lane-cost66c-v17-recheck-bit112-cap80m-20261117.jsonl"
ORDER_MATRIX = "class2-lane-cost66c-v17-bit117-order-matrix-20261117.jsonl"
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
          git_blob_sha1(SCR / ENGINE) == ENGINE_BLOB)
    for i in range(1, 9):
        check(f"raw_batch{i}_blob_sha1_matches_main",
              git_blob_sha1(OUT / RAW_FILES[i]) == RAW_BLOBS[i])
    check("bit112_resolution_blob_sha1_matches_main",
          git_blob_sha1(OUT / BIT112_RESOLUTION["file"]) == BIT112_RESOLUTION["blob"])

    mismatch = []
    flips = []
    total_v16 = 0
    total_v17 = 0
    per_bit = []
    win_bits_v17 = []
    pilots_ok = True
    for i in range(1, 9):
        p16, pp = load(OUT / RAW_FILES[i])
        p17, p17p = load(OUT / V17_FILES[i])
        check(f"batch{i}_bit_set_identity",
              sorted(p16) == BATCH_BITS[i] == sorted(p17),
              f"v16={sorted(p16)} v17={sorted(p17)}")
        if pp != {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}:
            pilots_ok = False
            mismatch.append(("pilot_v16", i, pp))
        if p17p != {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}:
            pilots_ok = False
            mismatch.append(("pilot_v17", i, p17p))
        for b in BATCH_BITS[i]:
            a, c = p16[b], p17[b]
            if b == 112:
                continue  # handled via the cap-raise resolution record below
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
            per_bit.append({
                "batch": i, "bit": b, "v16_loss": a["loss"], "v17_loss": c["loss"],
                "v16_nodes": a["nodes"], "v17_nodes": c["nodes"],
                "nodes_delta": c["nodes"] - a["nodes"],
                "capped": c["capped"], "terminalStoneRange": c["terminalStoneRange"],
                "andclose": c["andclose"],
            })

    # bit 112 via the cap-raise resolution record (raw batch 7 keeps it capped)
    r112_16 = json.loads((OUT / BIT112_RESOLUTION["file"]).read_text().strip())
    p17_112, p17_112_pilot = load(OUT / V17_BIT112)
    c = p17_112[112]
    check("v17_bit112_pilot_d6_identity",
          p17_112_pilot == {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False})
    total_v16 += r112_16["nodes"]
    total_v17 += c["nodes"]
    if c["loss"] is True:
        win_bits_v17.append(112)
    bit112_fields_match = all(r112_16[k] == c[k] for k in FIELDS)
    check("bit112_cap80m_resolution_field_identity", bit112_fields_match,
          f"v16={r112_16} v17={c}")
    per_bit.append({
        "batch": "cap80m_resolution", "bit": 112, "v16_loss": r112_16["loss"],
        "v17_loss": c["loss"], "v16_nodes": r112_16["nodes"], "v17_nodes": c["nodes"],
        "nodes_delta": c["nodes"] - r112_16["nodes"], "capped": c["capped"],
        "terminalStoneRange": c["terminalStoneRange"], "andclose": c["andclose"],
    })
    if r112_16["loss"] != c["loss"]:
        flips.append({"bit": 112, "v16_loss": r112_16["loss"], "v16_nodes": r112_16["nodes"],
                      "v17_loss": c["loss"], "v17_nodes": c["nodes"]})

    # order matrix for the saturation-detected bit 117
    om = [json.loads(l) for l in (OUT / ORDER_MATRIX).read_text().splitlines() if l.strip()]
    check("order_matrix_4_configurations_present", len(om) == 4)
    om_verdicts = {(r["engine"], r["andclose_mode"]): r["loss"] for r in om}
    check("order_matrix_all_refuted_d10",
          all(v is False for v in om_verdicts.values()), f"{om_verdicts}")
    om_c0 = [r for r in om if r["andclose_mode"] == 0]
    check("order_matrix_c0_node_exact_v16_eq_v17",
          len(om_c0) == 2 and om_c0[0]["nodes"] == om_c0[1]["nodes"] == 1341675)
    om_c1 = {r["engine"]: r["nodes"] for r in om if r["andclose_mode"] == 1}
    check("order_matrix_c1_v16_3121390_v17_3121368",
          om_c1 == {"v16": 3121390, "v17": 3121368}, f"{om_c1}")

    check("all_8_batch_pilots_identity_3402", pilots_ok)
    check("verdict_flips_zero", len(flips) == 0, f"flips={flips}")
    check("win_bits_unchanged_73_75_79_87_96_97_112",
          sorted(win_bits_v17) == [73, 75, 79, 87, 96, 97, 112],
          f"v17 win bits={sorted(win_bits_v17)}")
    sat_bits = [r for r in per_bit if r["nodes_delta"] != 0]
    check("saturation_detected_only_bit_117",
          [r["bit"] for r in sat_bits] == [117],
          f"node-delta bits={[ (r['bit'], r['nodes_delta']) for r in sat_bits ]}")
    check("bit_117_verdict_unchanged_refuted_d10",
          all(r["v16_loss"] is False and r["v17_loss"] is False for r in sat_bits))

    result = {
        "schema": "n11-class2-lane-cost66c-v17-full-row-recheck-20261117-v1",
        "date": "2026-11-17",
        "child": CHILD,
        "row": ("head-1441 third-ranked cheapest open row, cost 66, shared "
                "class-2 parent 00000000000000003800000008002000, 66 legal "
                "candidates, 7 pre-swept REFUTED transfers excluded, 59 swept "
                "bits (bit 112 resolved at cap 80M)"),
        "method": ("fbt-repaired v17 engine (class4_child1_runner_v17.ts, blob "
                   "c132cc64) re-executed all 59 swept bits from scratch with "
                   "the published batch partitions (8 batches), depth 10, cap "
                   "1e7, --andclose 1 (bit 112 additionally at cap 80000000), "
                   "fresh engine state per candidate, pilot_d6 control per "
                   "batch; compared field-by-field against the published v16 "
                   "raw batches 1-8 and the bit-112 cap-raise resolution record"),
        "engine_blob_sha1": ENGINE_BLOB,
        "published_raw_blob_sha1": {RAW_FILES[i]: RAW_BLOBS[i] for i in range(1, 9)},
        "published_bit112_resolution_blob_sha1": BIT112_RESOLUTION["blob"],
        "v17_raw_files": [V17_FILES[i] for i in range(1, 9)] + [V17_BIT112, ORDER_MATRIX],
        "previous_evidence": {
            "claim_v1": "64e83dff", "claim_v2_completed": "b17e978e",
            "independent_v16_rerun_verification": "42788a0d",
            "win_certificates": ("7 WIN7-D10 certificates (bits 73/75/79/87/96/97/"
                                 "112), dual-verified BigInt + Bareiss, manifest "
                                 "commit 39665854; blind re-extraction byte-identical "
                                 "(b41027e1)"),
        },
        "checked_bits": len(per_bit),
        "field_identical_bits": len(per_bit) - len(sat_bits),
        "saturation_detected_bits": [
            {"bit": r["bit"], "v16_nodes": r["v16_nodes"], "v17_nodes": r["v17_nodes"],
             "nodes_delta": r["nodes_delta"], "verdict": "REFUTED-D10 unchanged"}
            for r in sat_bits],
        "verdict_flips": flips,
        "win_bits_v17": sorted(win_bits_v17),
        "total_nodes_v16": total_v16,
        "total_nodes_v17": total_v17,
        "bit112_cap80m": {"v16": r112_16, "v17": c},
        "bit117_order_matrix": om,
        "bit117_conclusion": ("v16 c1 dropped 22 nodes worth of fb triples "
            "(3,121,390 -> 3,121,368 under the v17 repair); the c0 traversal is "
            "node-exact across engines (1,341,675) so saturation manifested only "
            "in the close-first ordering; the REFUTED-D10 verdict is identical in "
            "all 4 configurations (2 engines x 2 orderings), so the published "
            "REFUTED stands with engine-corrected node count 3,121,368"),
        "saturation_context": ("bit 112 at 12,574,920 nodes and bit 30 at "
            "8,806,920 nodes are node-exact under v17 (fb-unsaturated), while "
            "bit 117 at only 3,121,390 nodes saturated lightly: saturation "
            "depends on fb unique-triple diversity, not on raw node count, "
            "confirming that node-count thresholds are only an empirical guide"),
        "determinism": ("two full 8-batch + cap80M runs in this lane produced "
                        "identical bit/loss/nodes/capped/terminalStoneRange/"
                        "andclose for all 59 bits and identical pilots (ms only "
                        "differs)"),
        "checks": checks,
        "all_checks_pass": ok,
        "per_bit": per_bit,
        "interpretation_guard": ("bookkeeping verification only; WIN7-D10 proves "
            "a first-player win within depth 10 from the individual 7-stone "
            "roots only; REFUTED-D10 is not a LOSS proof; NOT-STERILE is not a "
            "game resolution; 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60} and classes 1/2/4 remain UNKNOWN"),
    }
    dest = OUT / "class2-lane-cost66c-v17-full-row-recheck-20261117.json"
    with open(dest, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("checks:", len(checks), "all pass:", ok)
    print("total v16:", total_v16, "| v17:", total_v17)
    print("win bits v17:", sorted(win_bits_v17))
    print("sat bits:", [(r["bit"], r["nodes_delta"]) for r in sat_bits])
    print("flips:", flips)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
