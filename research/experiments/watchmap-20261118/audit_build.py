#!/usr/bin/env python3
"""Audit builder for K0935 (WATCH-MAP). Runs every check of
watchmap_verify.run_checks() twice in-process, asserts the two runs are
identical, and writes output/watchmap_audit.json (deterministic: no
timestamps, sort_keys).

Run from the experiment directory:
    python3 audit_build.py
Exit status 0 iff both runs pass all checks and agree.
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import watchmap_verify as V  # noqa: E402


def main():
    r1 = V.run_checks()
    r2 = V.run_checks()
    same = json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)
    audit = {
        "all_ok": bool(r1["all_ok"] and r2["all_ok"] and same),
        "runs_identical": bool(same),
        "fail_count": r1["fail_count"],
        "checks": {
            "grid": {"w_max": V.W_MAX, "n_max": V.N_MAX,
                     "watched_maps_checked": r1["counts"].get("WM1", 0),
                     "composition_checks": r1["counts"].get("WM2", 0)},
        },
        "first_fails": r1["fails"][:10],
    }
    out = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=1)
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    path = os.path.join(HERE, "output", "watchmap_audit.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out + "\n")
    print(json.dumps({"all_ok": audit["all_ok"],
                      "sha256": hashlib.sha256(out.encode()).hexdigest()},
                     sort_keys=True))
    sys.exit(0 if audit["all_ok"] else 1)


if __name__ == "__main__":
    main()
