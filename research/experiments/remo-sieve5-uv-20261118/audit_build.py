#!/usr/bin/env python3
"""Deterministic audit builder for K0932 (SIEVE5-U/V, twin laws mod 30).

Runs the full check suite of sieve5_verify.py twice in-process and requires
identical results, then writes output/sieve5_uv_audit.json (no timestamps,
sort_keys, deterministic). Two cold invocations of this script must produce
byte-identical outputs.

Run from the experiment directory:
    python3 audit_build.py
Exit status 0 iff both runs agree and all checks pass.
"""

import hashlib
import json
import os
import sys

import sieve5_verify as sv

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output", "sieve5_uv_audit.json")


def main():
    res1, ok1 = sv.run_checks()
    res2, ok2 = sv.run_checks()
    if res1 != res2:
        print("NONDETERMINISTIC: two runs differ")
        sys.exit(2)
    if not (ok1 and ok2):
        print("CHECKS FAILED")
        sys.exit(1)

    def sha(path):
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    audit = {
        "experiment": "remo-sieve5-uv-20261118",
        "item": "K0932",
        "checks": res1,
        "all_ok": True,
        "m_fresh": sv.M_FRESH,
        "scripts_sha256": {
            "sieve5_verify.py": sha(os.path.join(HERE, "sieve5_verify.py")),
            "audit_build.py": sha(os.path.join(HERE, "audit_build.py")),
        },
        "pins": {
            "pc_uv8000.json": sv.PIN_UV_SHA,
            "pc_p8000.json": sv.PIN_P_SHA,
        },
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print("audit written:", OUT)
    print("runs identical: True ; all_ok: True")


if __name__ == "__main__":
    main()
