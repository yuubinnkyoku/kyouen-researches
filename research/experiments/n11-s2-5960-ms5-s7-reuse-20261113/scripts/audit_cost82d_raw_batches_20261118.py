#!/usr/bin/env python3
"""Audit of the cost82d raw sweep batches (class2-lane-cost82d-raw-batch{1..9}-20261118.jsonl).

Checks (mirroring the cost79c/79d/79e/80e/80f/81 raw-batches audits):
  * every batch file starts with the pilot_d6 control line: loss=false,
    nodes=3402, capped=false (the v17 control);
  * the per-bit records cover exactly the planned batch bits, in order,
    with andclose=true, capped=false and a terminal stone range within [13,17];
  * verdict semantics: loss=true => WIN7-D10, loss=false and not capped =>
    REFUTED-D10;
  * the seventeen confirmation bits come out REFUTED-D10 exactly as predicted
    by the census v18 overlay (0 conflicts);
  * per-bit root canon = D4 canon(child | 1<<bit), recorded for every bit and
    checked against the census v18 transfer root canons for the confirmation
    bits (census v18 blob 11306824f2363d5002559d4d1535d91a61509929, claim v1
    blob 1f4484edb58728d6266581c2818d744805fcaaf8);
  * node sums per batch and overall;
  * the independent v15 crosscheck chunk (pilot_d6 = 5949) agrees 17/17
    loss=false with the confirmation batch.
No engine run is performed here: this is an audit of the already-produced raw
JSONL batch files, read byte-for-byte.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

CHILD = int("00000000020000003800000080000800", 16)
BATCHES = {
    "1": [2, 3, 4, 6, 7, 8, 10, 14, 16],
    "2": [17, 18, 19, 26, 28, 29, 33, 34, 36],
    "3": [37, 38, 39, 40, 42, 43, 44, 49, 50],
    "4": [51, 53, 54, 66, 67, 69, 70, 71, 72],
    "5": [76, 77, 78, 81, 82, 83, 84, 86, 87],
    "6": [91, 92, 94, 95, 99, 101, 102, 103, 104],
    "7": [106, 108, 109, 110, 112, 113, 114, 116, 117],
    "8": [118, 120],
    "9": [5, 15, 27, 30, 32, 35, 41, 45, 46, 74, 75, 79, 85, 90, 93, 105, 115],
}
OPEN_BITS = sorted(sum((v for k, v in BATCHES.items() if k != "9"), []))
CONFIRMATION_BITS = BATCHES["9"]
CONFIRMATION_PREDICTED = {b: "REFUTED-D10" for b in CONFIRMATION_BITS}
CONFIRMATION_ROOT_CANONS = {
    5: "00000000020000003800000080000820",
    15: "00000000020000003800000080008800",
    27: "00000000020000003800000088000800",
    30: "000000000200000038000000c0000800",
    32: "00000000020000003800000180000800",
    35: "00000000020000003800000880000800",
    41: "00000000020000003800020080000800",
    45: "00000000020000003800200080000800",
    46: "00000000020000003800400080000800",
    74: "00000000020004003800000080000800",
    75: "00000000020008003800000080000800",
    79: "00000000020080003800000080000800",
    85: "00000000022000003800000080000800",
    90: "00000000060000003800000080000800",
    93: "00000000220000003800000080000800",
    105: "0000000a000000003800000000820000",
    115: "0000000a000000003800000000800020",
}

V15_CROSSCHECK = "class2-lane-cost82d-v15-crosscheck-a-20261118.jsonl"


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
        suffix = "-confirmation" if nb == "9" else ""
        fn = OUT / ("class2-lane-cost82d-raw-batch%s%s-20261118.jsonl" % (nb, suffix))
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
                    "confirmation bit %s: root canon %s != census v18 transfer %s" % (
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
        "schema": "n11-class2-lane-cost82d-raw-batches-1-9-audit-20261118-v1",
        "date": "2026-11-18",
        "child": format(CHILD, "032x"),
        "engine": "class4_child1_runner_v17.ts (git blob c132cc6425eee3feaeef1d697dd74f968cfedb59), depth 10, cap 1e9 per bit, andclose 1",
        "batches": per_batch,
        "pilot_controls_pass": "%d/9" % pilot_ok,
        "per_bit": {str(b): per_bit[b] for b in sorted(per_bit)},
        "win7_d10_bits": win_bits,
        "refuted_d10_bits": refuted_bits,
        "capped_bits": capped_bits,
        "counts": {"win7_d10": len(win_bits), "refuted_d10": len(refuted_bits),
                   "capped": len(capped_bits), "total_bits": len(per_bit)},
        "confirmation_bits": [str(b) for b in CONFIRMATION_BITS],
        "confirmation_outcome": {str(k): v for k, v in conf_outcome.items()},
        "confirmation_prediction_match": "17/17 REFUTED-D10 as predicted by the census v18 overlay (0 conflicts)" if conf_ok else "MISMATCH",
        "confirmation_root_canons_match_census_v18_transfers": conf_ok,
        "v15_crosscheck": {
            "file": V15_CROSSCHECK,
            "pilot_nodes": 5949,
            "agreement": "17/17 loss=false (0 conflicts)",
            "file_sha1": hashlib.sha1(v15raw).hexdigest(),
        },
        "root_canon_rule": "per-bit root_canon == D4 canon(child | 1<<bit), recomputed independently in this audit",
        "total_candidate_nodes": total_nodes,
        "open_bits_total": len(OPEN_BITS),
        "checks_log": checks,
        "verdict_semantics": "loss=true => WIN7-D10 (certificate rebuild target); loss=false && !capped => REFUTED-D10, no first-player win within depth 10 from this root (NOT a LOSS proof); verdicts are per 7-stone root only",
        "unknown_status": "11x11 empty board: UNKNOWN. This sweep proves only WIN7-D10/REFUTED-D10 verdicts for the 82 seven-stone roots of this child and closes no family row by itself; the 11x11 empty board, the two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN regardless of this sweep's outcome",
    }
    out_path = OUT / "class2-lane-cost82d-raw-batches-1-9-audit-20261118.json"
    out_path.write_text(json.dumps(result, indent=1, sort_keys=False, ensure_ascii=True) + "\n")
    print("wrote %s" % out_path)
    print("win bits:", win_bits)
    print("refuted:", len(refuted_bits), "capped:", len(capped_bits))
    print("confirmation:", conf_outcome)
    print("total candidate nodes:", total_nodes)


if __name__ == "__main__":
    main()