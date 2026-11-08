"""Check committed audit-receipt coverage; this does not replay DRAT proofs."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PRIME = 2647
CHECKER_SHA256 = "34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b"
BASE = "research/experiments/parabola-p2207-no-equality-witness-20261107"
RECEIPTS = BASE + "/output/drat_audit_full_2647_34249932790a9e9d.json"
CHECKER = BASE + "/drat_check_incremental.cpp"


def validate(data):
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    require(PRIME > 2 and PRIME % 2 == 1 and
            all(PRIME % d for d in range(2, math.isqrt(PRIME) + 1)), "not an odd prime")
    require(data.get("p") == PRIME and data.get("h") == 1323, "wrong prime or h")
    require(data.get("checker_source_sha256") == CHECKER_SHA256, "wrong checker source")
    rows = data.get("records")
    require(isinstance(rows, list) and len(rows) == 1323, "wrong record count")
    require(all(type(r.get("d")) is int for r in rows), "invalid d")
    require({r["d"] for r in rows} == set(range(1, 1324)), "incomplete or duplicate d")
    for r in rows:
        require(r.get("verified") is True, "unverified record")
        require(r.get("solver") == "UNSAT", "solver not UNSAT")
        require(r.get("checker_rc") == 0 and r.get("checker_out") == "VERIFIED", "checker failed")
        require(type(r.get("proof_lines")) is int and r["proof_lines"] > 0, "empty proof")
    return rows


def negative_controls(data):
    mutations = [
        ("missing", lambda x: x["records"].pop()),
        ("duplicate", lambda x: x["records"][-1].update(d=x["records"][0]["d"])),
        ("out-of-range", lambda x: x["records"][0].update(d=0)),
        ("wrong-prime", lambda x: x.update(p=2531)),
        ("wrong-source", lambda x: x.update(checker_source_sha256="0" * 64)),
        ("not-verified", lambda x: x["records"][0].update(verified=False)),
        ("nonzero-exit", lambda x: x["records"][0].update(checker_rc=1)),
        ("wrong-checker-output", lambda x: x["records"][0].update(checker_out="UNKNOWN")),
        ("unknown-solver", lambda x: x["records"][0].update(solver="UNKNOWN")),
        ("empty-proof", lambda x: x["records"][0].update(proof_lines=0)),
    ]
    rejected = []
    for name, mutate in mutations:
        forged = copy.deepcopy(data)
        mutate(forged)
        try:
            validate(forged)
        except ValueError:
            rejected.append(name)
        else:
            raise RuntimeError(f"accepted forged receipts: {name}")
    return rejected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--revision", default="b52faa12")
    args = ap.parse_args()
    revision = subprocess.check_output(
        ["git", "rev-parse", "--verify", args.revision + "^{commit}"], cwd=ROOT, text=True
    ).strip()
    raw = subprocess.check_output(["git", "show", revision + ":" + RECEIPTS], cwd=ROOT)
    source = subprocess.check_output(["git", "show", revision + ":" + CHECKER], cwd=ROOT)
    if hashlib.sha256(source).hexdigest() != CHECKER_SHA256:
        raise ValueError("committed checker source differs")
    data = json.loads(raw)
    rows = validate(data)
    result = {
        "input_commit": revision, "receipt_path": RECEIPTS,
        "receipt_sha256": hashlib.sha256(raw).hexdigest(),
        "checker_source_sha256": CHECKER_SHA256,
        "prime": PRIME, "odd_prime_by_trial_division": True,
        "h": 1323, "verified": len(rows), "failures": 0,
        "unique_complete_d_range": [1, 1323],
        "proof_lines_total": sum(r["proof_lines"] for r in rows),
        "proof_lines_min": min(r["proof_lines"] for r in rows),
        "proof_lines_max": max(r["proof_lines"] for r in rows),
        "check_seconds_min": min(r["check_seconds"] for r in rows),
        "check_seconds_max": max(r["check_seconds"] for r in rows),
        "rejected_negative_controls": negative_controls(data),
        "scope": "Receipt consistency only; no DRAT replay, encoding proof, or Lean verification.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
