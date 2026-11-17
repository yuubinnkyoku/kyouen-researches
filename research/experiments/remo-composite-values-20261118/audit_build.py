#!/usr/bin/env python3
"""Build output/composite_values_audit.json for K0941.

Runs run_checks() once in-process (detail record), then runs
composite_verify.py twice as fresh subprocesses (each of which
internally runs run_checks() twice and checks in-process
determinism) and requires byte-identical stdout and exit status 0
from both.  Writes the audit record (same schema as the K0939
audit) to output/composite_values_audit.json.

Run from the experiment directory:
    python3 audit_build.py
Exit status 0 iff everything passed and the audit file was written.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from composite_verify import run_checks  # noqa: E402

REGION = {
    "engine_m_hi": 600,
    "struct_m_hi": 1500,
    "death_fullrepro_p2obs_m_hi": 8000,
    "egame_k_hi": 50,
}


def main():
    res1 = run_checks()

    cold = []
    for _ in range(2):
        p = subprocess.run([sys.executable,
                            os.path.join(HERE, "composite_verify.py")],
                           capture_output=True)
        cold.append(p)
    cold_identical = (cold[0].returncode == 0 and
                      cold[1].returncode == 0 and
                      cold[0].stdout == cold[1].stdout)

    checks = {}
    first_fails = {}
    for name, v in res1["checks"].items():
        key = name.lower()
        entry = {"ok": bool(v["ok"])}
        for fld in ("count", "fail_count", "fails", "games",
                    "collapse_deaths", "u_p2_games", "v_p2_games",
                    "uv_sha256", "p_sha256"):
            if fld in v:
                entry[fld] = v[fld]
        checks[key] = entry
        if not v["ok"]:
            first_fails[key] = v.get("fails", [])[:3]

    audit = {
        "all_ok": bool(res1["all_ok"] and cold_identical),
        "checks": checks,
        "first_fails": first_fails,
        "region": REGION,
        "runs_identical": bool(cold_identical),
        "cold_runs_byte_identical": bool(cold_identical),
    }
    outdir = os.path.join(HERE, "output")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "composite_values_audit.json")
    with open(out, "w") as f:
        json.dump(audit, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps({"all_ok": audit["all_ok"],
                      "runs_identical": audit["runs_identical"],
                      "checks": {k: v["ok"] for k, v in
                                 audit["checks"].items()}},
                     sort_keys=True))
    sys.exit(0 if audit["all_ok"] else 1)


if __name__ == "__main__":
    main()
