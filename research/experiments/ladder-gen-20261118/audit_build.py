#!/usr/bin/env python3
"""Audit builder for K0934 (LAD-GEN). Runs every check of
ladder_gen_verify.run_checks() twice in-process, asserts the two runs are
identical, and writes output/ladder_gen_audit.json (deterministic: no
timestamps, sort_keys, fixed float formatting).

Run from the experiment directory:
    python3 audit_build.py
Exit status 0 iff both runs pass all checks and agree byte-for-byte.
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ladder_gen_verify as V  # noqa: E402


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
                     "games": r1["counts"].get("LG1", 0),
                     "cold_blocks_checked": r1["counts"].get("LG2", 0),
                     "breaking_checked": r1["counts"].get("LG3", 0),
                     "end_states_checked": r1["counts"].get("LG4", 0),
                     "elim_sets_checked": r1["counts"].get("LG5", 0),
                     "watched_checked": r1["counts"].get("LG5w", 0)},
            "regressions": {
                "lad_h0_h0_cases": r1["counts"].get("LG6", 0),
                "s4_table_cases": r1["counts"].get("LG7", 0)},
            "handoff": {"stretch2_games": r1["counts"].get("LG8", 0),
                        "stretch2_blocks_checked": r1["counts"].get("LG8b", 0),
                        "w_max": V.W_HANDOFF, "n_max": V.N_HANDOFF},
        },
        "first_fails": r1["fails"][:10],
    }
    out = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=1)
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    path = os.path.join(HERE, "output", "ladder_gen_audit.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out + "\n")
    print(json.dumps({"all_ok": audit["all_ok"],
                      "sha256": hashlib.sha256(out.encode()).hexdigest()},
                     sort_keys=True))
    sys.exit(0 if audit["all_ok"] else 1)


if __name__ == "__main__":
    main()
