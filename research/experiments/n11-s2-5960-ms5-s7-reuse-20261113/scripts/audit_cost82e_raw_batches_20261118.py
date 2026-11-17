#!/usr/bin/env python3
"""Audit of the cost82e raw sweep batches (class2-lane-cost82e-raw-batch{1..8}-20261118.jsonl).

Checks (mirroring the cost79c/79d/79e/80e/80f/81/82d raw-batches audits, plus
the det re-run check that earlier censuses performed, kept here because this
sweep is published as a labelled cross-version revalidation of a historical
STERILE row rather than as a census-re-ranked closure attempt):
  * every batch file starts with the pilot_d6 control line: loss=false,
    nodes=3402, capped=false (the v17 control);
  * the per-bit records cover exactly the planned batch bits, in order,
    with andclose=true, capped=false and a terminal stone range within [13,17];
  * verdict semantics: loss=true => WIN7-D10, loss=false and not capped =>
    REFUTED-D10;
  * the nineteen confirmation bits come out REFUTED-D10 exactly as predicted
    by the census v19 overlay (0 conflicts);
  * per-bit root canon = D4 canon(child | 1<<bit), recorded for every bit and
    checked against the census v19 transfer root canons for the confirmation
    bits (census v19 blob a0c6abaf0df163eddc35f8b8dc0f8c0eb4268fe6, claim v1
    blob 5f9f3d95b6c83ea68665978129c7f9c3ae7d2b74);
  * node sums per batch and overall;
  * the det rerun chunks (det-batch1, det-batch7) are field-identical to the
    corresponding raw batches on every non-ms field;
  * the independent v15 crosscheck chunk (pilot_d6 = 5949) agrees 19/19
    loss=false with the confirmation batch.
No engine run is performed here: this is an audit of the already-produced raw
JSONL batch files, read byte-for-byte.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

CHILD = int("00000000020000003800000090000000", 16)
BATCHES = {
    "1": [0, 2, 3, 4, 6, 7, 8, 10, 12],
    "2": [14, 16, 17, 18, 19, 21, 29, 33, 34],
    "3": [36, 38, 39, 42, 43, 44, 49, 50, 53],
    "4": [54, 66, 67, 69, 70, 71, 72, 76, 77],
    "5": [78, 80, 81, 82, 83, 84, 86, 87, 91],
    "6": [92, 94, 95, 99, 101, 102, 103, 104, 106],
    "7": [108, 110, 112, 113, 114, 116, 117, 118, 120],
    "8": [5, 11, 15, 30, 32, 35, 41, 45, 46, 74, 75, 79, 85, 88, 90, 93, 105, 109, 115],
}
OPEN_BITS = sorted(sum((v for k, v in BATCHES.items() if k != "8"), []))
CONFIRMATION_BITS = BATCHES["8"]
CONFIRMATION_PREDICTED = {b: "REFUTED-D10" for b in CONFIRMATION_BITS}
CONFIRMATION_ROOT_CANONS = {
    5: "00000000020000003800000090000020",
    11: "00000000020000003800000090000800",
    15: "00000000020000003800000090008000",
    30: "000000000200000038000000d0000000",
    32: "00000000020000003800000190000000",
    35: "00000000020000003800000890000000",
    41: "00000000020000003800020090000000",
    45: "00000000020000003800200090000000",
    46: "00000000020000003800400090000000",
    74: "00000000020004003800000090000000",
    75: "00000000020008003800000090000000",
    79: "00000000020080003800000090000000",
    85: "00000000022000003800000090000000",
    88: "00000000030000003800000090000000",
    90: "00000000060000003800000090000000",
    93: "00000000120000003800000088000000",
    105: "00000000120000003800000080008000",
    109: "00000000120000003800000080000800",
    115: "00000000120000003800000080000020",
}
DET_BATCHES = {"1": "class2-lane-cost82e-det-batch1-20261118.jsonl",
               "7": "class2-lane-cost82e-det-batch7-20261118.jsonl"}
V15_CROSSCHECK = "class2-lane-cost82e-v15-crosscheck-a-20261118.jsonl"


def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
                      (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x))
            for i, (a, b) in enumerate(coords):
                result[i] |= 1 << (11 * b + a)
    return result


IMG = [images(1 << p) for p in range(121)]


def canon(mask):
    best = None
    for r in range(8):
        v = 0
        for p in range(121):
            if mask >> p & 1:
                v |= IMG[p][r]
        if best is None or v < best:
            best = v
    return best


def verdict_of(rec):
    if rec["loss"]:
        return "WIN7-D10"
    if rec["capped"]:
        return "CAPPED"
    return "REFUTED-D10"


def main():
    per_batch = {}
    per_bit = {}
    total_nodes = 0
    pilot_ok = 0
    checks = []
    all_bits = sorted(OPEN_BITS + CONFIRMATION_BITS)
    assert len(all_bits) == 82 and len(set(all_bits)) == 82
    for nb, bits in sorted(BATCHES.items(), key=lambda kv: int(kv[0])):
        suffix = "-confirmation" if nb == "8" else ""
        fn = OUT / ("class2-lane-cost82e-raw-batch%s%s-20261118.jsonl" % (nb, suffix))
        raw = fn.read_bytes()
        lines = [json.loads(l) for l in raw.decode().splitlines() if l]
        assert lines[0].get("control") == "pilot_d6", "batch %s: first line is not the pilot control" % nb
        ctl = lines[0]
        assert ctl["loss"] is False and ctl["nodes"] == 3402 and ctl["capped"] is False, \
            "batch %s: pilot control mismatch %r" % (nb, ctl)
        pilot_ok += 1
        recs = lines[1:]
        got = [r["bit"] for r in recs]
        assert got == bits, "batch %s: bit list mismatch: %r vs plan %r" % (nb, got, bits)
        bnodes = 0
        for r in recs:
            assert r["capped"] is False, "batch %s bit %s: capped" % (nb, r["bit"])
            assert r["andclose"] is True, "batch %s bit %s: andclose" % (nb, r["bit"])
            tsr = r["terminalStoneRange"]
            assert tsr[0] >= 13 and tsr[1] <= 17, "batch %s bit %s: terminal range %r" % (nb, r["bit"], tsr)
            assert r["bit"] not in per_bit, "duplicate bit %s" % r["bit"]
            root_canon = format(canon(CHILD | (1 << r["bit"])), "032x")
            v = verdict_of(r)
            if r["bit"] in CONFIRMATION_BITS:
                assert root_canon == CONFIRMATION_ROOT_CANONS[r["bit"]], \
                    "confirmation bit %s: root canon %s != census v19 transfer %s" % (
                        r["bit"], root_canon, CONFIRMATION_ROOT_CANONS[r["bit"]])
            per_bit[r["bit"]] = {
                "batch": int(nb), "verdict": v, "nodes": r["nodes"],
                "ms": r["ms"], "root_canon": root_canon,
                "terminal_stone_range": tsr,
            }
            bnodes += r["nodes"]
        per_batch[nb] = {"bits": bits, "pilot_nodes": 3402, "candidate_nodes": bnodes,
                         "file_sha1": hashlib.sha1(raw).hexdigest(), "file_bytes": len(raw)}
        total_nodes += bnodes
        checks.append("batch %s: pilot 3402 + %d bits, %d candidate nodes" % (nb, len(bits), bnodes))

    # det rerun check: field-identical on every non-ms field
    det_files = {}
    for nb, fn in sorted(DET_BATCHES.items()):
        raw = (OUT / fn).read_bytes()
        lines = [json.loads(l) for l in raw.decode().splitlines() if l]
        assert lines[0].get("control") == "pilot_d6" and lines[0]["nodes"] == 3402, \
            "det batch %s: pilot mismatch" % nb
        recs = {r["bit"]: r for r in lines[1:]}
        assert sorted(recs) == BATCHES[nb], "det batch %s: bit list mismatch" % nb
        for b, r in recs.items():
            o = per_bit[b]
            assert r["loss"] is False and r["capped"] is False and r["andclose"] is True, (nb, b)
            assert r["nodes"] == o["nodes"], ("det nodes", nb, b)
            assert r["terminalStoneRange"] == o["terminal_stone_range"], ("det tsr", nb, b)
        det_files[nb] = {"file": fn, "file_sha1": hashlib.sha1(raw).hexdigest(),
                         "file_bytes": len(raw)}
        checks.append("det batch %s: field-identical on every non-ms field (%d bits)" % (nb, len(recs)))

    v15fn = OUT / V15_CROSSCHECK
    v15raw = v15fn.read_bytes()
    v15lines = [json.loads(l) for l in v15raw.decode().splitlines() if l]
    assert v15lines[0].get("control") == "pilot_d6" and v15lines[0]["nodes"] == 5949, \
        "v15 crosscheck pilot mismatch"
    v15recs = {r["bit"]: r for r in v15lines[1:]}
    assert sorted(v15recs) == sorted(CONFIRMATION_BITS), "v15 crosscheck bit list mismatch"
    v15_agree = 0
    for b in CONFIRMATION_BITS:
        assert v15recs[b]["loss"] is False and v15recs[b]["capped"] is False, b
        if per_bit[b]["verdict"] == "REFUTED-D10" and v15recs[b]["loss"] is False:
            v15_agree += 1
        else:
            raise AssertionError("v15 crosscheck verdict disagreement on bit %s" % b)
    assert v15_agree == len(CONFIRMATION_BITS), "v15 cross-engine agreement %d/%d" % (v15_agree, len(CONFIRMATION_BITS))

    win_bits = sorted(b for b, r in per_bit.items() if r["verdict"] == "WIN7-D10")
    refuted_bits = sorted(b for b, r in per_bit.items() if r["verdict"] == "REFUTED-D10")
    capped_bits = sorted(b for b, r in per_bit.items() if r["verdict"] == "CAPPED")
    conf_outcome = {b: per_bit[b]["verdict"] for b in CONFIRMATION_BITS}
    conf_ok = all(conf_outcome[b] == CONFIRMATION_PREDICTED[b] for b in CONFIRMATION_BITS)

    result = {
        "schema": "n11-class2-lane-cost82e-raw-batches-1-8-audit-20261118-v1",
        "date": "2026-11-18",
        "child": format(CHILD, "032x"),
        "engine": "class4_child1_runner_v17.ts (git blob c132cc6425eee3feaeef1d697dd74f968cfedb59), depth 10, cap 1e9 per bit, andclose 1",
        "batches": per_batch,
        "pilot_controls_pass": "%d/8" % pilot_ok,
        "determinism_rerun": {
            "files": det_files,
            "result": "field-identical on every non-ms field (batches 1 and 7)",
        },
        "per_bit": {str(b): per_bit[b] for b in sorted(per_bit)},
        "win7_d10_bits": win_bits,
        "refuted_d10_bits": refuted_bits,
        "capped_bits": capped_bits,
        "counts": {"win7_d10": len(win_bits), "refuted_d10": len(refuted_bits),
                   "capped": len(capped_bits), "total_bits": len(per_bit)},
        "confirmation_bits": [str(b) for b in CONFIRMATION_BITS],
        "confirmation_outcome": {str(k): v for k, v in conf_outcome.items()},
        "confirmation_prediction_match": "19/19 REFUTED-D10 as predicted by the census v19 overlay (0 conflicts)" if conf_ok else "MISMATCH",
        "confirmation_root_canons_match_census_v19_transfers": conf_ok,
        "v15_crosscheck": {
            "file": V15_CROSSCHECK,
            "pilot_nodes": 5949,
            "agreement": "19/19 loss=false (0 conflicts)",
            "file_sha1": hashlib.sha1(v15raw).hexdigest(),
        },
        "root_canon_rule": "per-bit root_canon == D4 canon(child | 1<<bit), recomputed independently in this audit",
        "total_candidate_nodes": total_nodes,
        "open_bits_total": len(OPEN_BITS),
        "checks_log": checks,
        "verdict_semantics": "loss=true => WIN7-D10 (certificate rebuild target); loss=false && !capped => REFUTED-D10, no first-player win within depth 10 from this root (NOT a LOSS proof); verdicts are per 7-stone root only",
        "unknown_status": "11x11 empty board: UNKNOWN. This sweep proves only WIN7-D10/REFUTED-D10 verdicts for the 82 seven-stone roots of this child and closes no family row by itself; the 11x11 empty board, the two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN regardless of this sweep's outcome",
    }
    out_path = OUT / "class2-lane-cost82e-raw-batches-1-8-audit-20261118.json"
    out_path.write_text(json.dumps(result, indent=1, sort_keys=False, ensure_ascii=True) + "\n")
    print("wrote %s" % out_path)
    print("win bits:", win_bits)
    print("refuted:", len(refuted_bits), "capped:", len(capped_bits))
    print("confirmation:", conf_outcome)
    print("total candidate nodes:", total_nodes)


if __name__ == "__main__":
    main()
