#!/usr/bin/env python3
"""Audit builder for K0936 (SIEVE7-U/V). Runs every check of
sieve7_verify.run_checks() twice in-process, asserts the two runs are
identical, and writes output/sieve7_uv_audit.json (deterministic: no
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

import sieve7_verify as V  # noqa: E402


def main():
    r1 = V.run_checks()
    r2 = V.run_checks()
    same = json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)

    def chk(name):
        return r1["checks"][name]

    audit = {
        "all_ok": bool(r1["all_ok"] and r2["all_ok"] and same),
        "runs_identical": bool(same),
        "region": {"edge_lo": 3, "edge_hi": V.M0 - 1,
                   "composition_lo": V.M0, "fresh_hi": V.M_FRESH,
                   "class_j_lo": 2, "class_j_hi": V.J_HI},
        "checks": {
            "pin": {"ok": chk("PIN")["ok"],
                    "uv_sha256_8": chk("PIN")["uv_sha256"],
                    "p_sha256_8": chk("PIN")["p_sha256"]},
            "redrecon": {"ok": chk("REDRECON")["ok"],
                         "count": chk("REDRECON")["count"],
                         "mismatches": chk("REDRECON")["mismatches"]},
            "freshpin": {"ok": chk("FRESHPIN")["ok"],
                         "count": chk("FRESHPIN")["count"],
                         "mismatches": chk("FRESHPIN")["mismatches"]},
            "canon": {"ok": chk("CANON")["ok"],
                      "stretch_entries_checked": chk("CANON")["count"],
                      "fail_count": chk("CANON")["fail_count"]},
            "trk": {"ok": chk("TRK")["ok"],
                    "games_checked": chk("TRK")["count"],
                    "fail_count": chk("TRK")["fail_count"]},
            "s3reg": {"ok": chk("S3REG")["ok"],
                      "count": chk("S3REG")["count"],
                      "fail_count": chk("S3REG")["fail_count"]},
            "k935tbl": {"ok": chk("K935TBL")["ok"],
                        "count": chk("K935TBL")["count"],
                        "fail_count": chk("K935TBL")["fail_count"]},
            "sv7edge": {"ok": chk("SV7EDGE")["ok"],
                        "domain_pairs": chk("SV7EDGE")["count"],
                        "stretch6_deaths": chk("SV7EDGE")["stretch6_deaths"],
                        "fail_count": chk("SV7EDGE")["fail_count"]},
            "sv7": {"ok": chk("SV7")["ok"],
                    "domain_pairs": chk("SV7")["count"],
                    "stretch6_deaths": chk("SV7")["stretch6_deaths"],
                    "stretch6_survivals": chk("SV7")["stretch6_survivals"],
                    "fail_count": chk("SV7")["fail_count"]},
            "class": {"ok": chk("CLASS")["ok"],
                      "rows": chk("CLASS")["count"],
                      "expected_rows": chk("CLASS")["expected_rows"],
                      "fail_count": chk("CLASS")["fail_count"],
                      "table": chk("CLASS")["rows"]},
            "twin210": {"ok": chk("TWIN210")["ok"],
                        "law1_classes": chk("TWIN210")["law1_classes"],
                        "law2_classes": chk("TWIN210")["law2_classes"],
                        "law1_new_classes": chk("TWIN210")["law1_new_classes"],
                        "law2_new_classes": chk("TWIN210")["law2_new_classes"],
                        "law1_violations":
                            chk("TWIN210")["law1_violations"],
                        "law2_violations":
                            chk("TWIN210")["law2_violations"]},
            "sieveobs": {"ok": chk("SIEVEOBS")["ok"],
                         "games": chk("SIEVEOBS")["count"],
                         "fail_count": chk("SIEVEOBS")["fail_count"],
                         "odd_pot_deaths":
                            chk("SIEVEOBS")["odd_pot_deaths"]},
        },
        "first_fails": {k: v.get("fails", [])[:5]
                        for k, v in r1["checks"].items()
                        if v.get("fail_count", 0) > 0},
    }
    out = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=1)
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    path = os.path.join(HERE, "output", "sieve7_uv_audit.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out + "\n")
    print(json.dumps({"all_ok": audit["all_ok"],
                      "sha256": hashlib.sha256(out.encode()).hexdigest()},
                     sort_keys=True))
    sys.exit(0 if audit["all_ok"] else 1)


if __name__ == "__main__":
    main()
