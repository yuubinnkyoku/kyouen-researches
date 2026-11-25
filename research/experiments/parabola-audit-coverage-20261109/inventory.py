"""Inventory immutable DRAT receipts; never launch a solver or replay a proof."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = "research/experiments/parabola-p2207-no-equality-witness-20261107"
SOURCE_SHA = "34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b"
REVISION = "87e28af3c927d640bde3fbc8a20238efc30bccb8"
TARGETS = {2531: set(range(1, 1242, 20)), 3251: set(range(1, 1602, 25))}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ranges(values):
    output = []
    for value in sorted(values):
        if output and output[-1][1] + 1 == value:
            output[-1][1] = value
        else:
            output.append([value, value])
    return output


def classify(data, p):
    h = (p-1)//2
    require(p > 2 and p % 2 and all(p % n for n in range(2, math.isqrt(p)+1)), "not an odd prime")
    require(type(data.get("p")) is int and data["p"] == p, "wrong prime")
    require(type(data.get("h")) is int and data["h"] == h, "wrong h")
    require(data.get("checker_source_sha256") == SOURCE_SHA, "wrong checker source")
    rows = data.get("records")
    require(isinstance(rows, list), "missing records")
    seen, verified, unverified = set(), set(), set()
    for row in rows:
        require(isinstance(row, dict), "record is not an object")
        d = row.get("d")
        require(type(d) is int and 1 <= d <= h, "invalid d")
        require(d not in seen, "duplicate d")
        seen.add(d)
        require(type(row.get("verified")) is bool, "verified is not Boolean")
        if row["verified"]:
            require(row.get("solver") == "UNSAT", "verified non-UNSAT")
            require(type(row.get("checker_rc")) is int and row["checker_rc"] == 0, "checker exit")
            require(row.get("checker_out") == "VERIFIED", "checker output")
            require(type(row.get("proof_lines")) is int and row["proof_lines"] > 0, "empty proof")
            verified.add(d)
        else:
            unverified.add(d)
    universe = set(range(1, h+1))
    target = TARGETS.get(p)
    return {"p": p, "h": h, "records": len(rows), "verified": len(verified),
            "unverified_d": sorted(unverified), "verified_d_ranges": ranges(verified),
            "missing_verified_count": len(universe-verified),
            "missing_verified_d_ranges": ranges(universe-verified),
            "full_verified_coverage": verified == universe,
            "planned_sample": None if target is None else {
                "target_count": len(target), "verified_target_count": len(target & verified),
                "missing_target_d": sorted(target-verified),
                "complete": target <= verified}}


def negative_controls(data):
    tests = [
        ("wrong-prime", lambda x: x.update(p=2531)),
        ("wrong-h", lambda x: x.update(h=1322)),
        ("old-or-wrong-source", lambda x: x.update(checker_source_sha256="0"*64)),
        ("duplicate-d", lambda x: x["records"].append(copy.deepcopy(x["records"][0]))),
        ("outside-d", lambda x: x["records"][0].update(d=1324)),
        ("Boolean-d", lambda x: x["records"][0].update(d=True)),
        ("non-Boolean-verified", lambda x: x["records"][0].update(verified=1)),
        ("unknown-solver", lambda x: x["records"][0].update(solver="UNKNOWN")),
        ("failed-checker", lambda x: x["records"][0].update(checker_rc=1)),
        ("wrong-checker-output", lambda x: x["records"][0].update(checker_out="NOT VERIFIED")),
        ("empty-proof", lambda x: x["records"][0].update(proof_lines=0)),
    ]
    passed = []
    for name, mutate in tests:
        changed = copy.deepcopy(data)
        mutate(changed)
        try:
            classify(changed, 2647)
        except ValueError:
            passed.append(name)
        else:
            raise AssertionError(f"accepted forged receipt: {name}")
    changed = copy.deepcopy(data)
    changed["records"].pop(0)
    result = classify(changed, 2647)
    assert not result["full_verified_coverage"] and result["missing_verified_count"] == 1
    passed.append("missing-record-stays-partial")
    changed = copy.deepcopy(data)
    changed["records"][0].update(verified=False, solver="UNKNOWN", checker_rc=1)
    result = classify(changed, 2647)
    assert not result["full_verified_coverage"] and result["verified"] == 1322
    passed.append("unverified-record-stays-partial")
    return passed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--revision", default=REVISION)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    revision = subprocess.check_output(["git", "rev-parse", "--verify", args.revision+"^{commit}"],
                                       cwd=ROOT, text=True).strip()
    def committed(path):
        return subprocess.check_output(["git", "show", revision+":"+path], cwd=ROOT)
    require(hashlib.sha256(committed(BASE+"/drat_check_incremental.cpp")).hexdigest() == SOURCE_SHA,
            "committed source differs from receipt source hash")
    results, full_data = [], None
    for p in (2207, 2531, 2647, 3251):
        path = BASE+f"/output/drat_audit_full_{p}_{SOURCE_SHA[:16]}.json"
        raw = committed(path)
        data = json.loads(raw)
        result = classify(data, p)
        result.update(receipt_path=path, receipt_sha256=hashlib.sha256(raw).hexdigest())
        results.append(result)
        if p == 2647:
            full_data = data
    report = {"input_commit": revision, "checker_source_sha256": SOURCE_SHA,
              "inventories": results, "passed_controls": negative_controls(full_data),
              "scope": "Receipt consistency and coverage only; no DRAT replay, geometric proof, or general checker soundness proof."}
    encoded = json.dumps(report, indent=2)+"\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8", newline="\n")
    print(encoded, end="")


if __name__ == "__main__":
    main()
