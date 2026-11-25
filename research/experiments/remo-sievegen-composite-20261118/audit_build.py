#!/usr/bin/env python3
"""Audit builder for K0937 (SIEVE-COMPOSITE-GEN / INV-TRACK). Runs every
check of sievegen_verify.run_checks() twice in-process, asserts the two
runs are identical, and writes output/sievegen_audit.json (deterministic:
no timestamps, sort_keys).

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

import sievegen_verify as V  # noqa: E402


def main():
    r1 = V.run_checks()
    r2 = V.run_checks()
    same = json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)

    def chk(name):
        return r1["checks"][name]

    audit = {
        "all_ok": bool(r1["all_ok"] and r2["all_ok"] and same),
        "runs_identical": bool(same),
        "region": {"tracker_hi": V.MBIG, "fresh_hi": V.M_FRESH,
                   "t1_grid_w_hi": V.T1_WHI, "deathfast_w_hi": V.DF_WHI,
                   "n_bound_tracker": 2 * V.MBIG + 3,
                   "n_bound_fresh": 2 * V.M_FRESH + 3},
        "checks": {
            "pin": {"ok": chk("PIN")["ok"],
                    "uv_sha256_8": chk("PIN")["uv_sha256"],
                    "p_sha256_8": chk("PIN")["p_sha256"]},
            "redrecon": {"ok": chk("REDRECON")["ok"],
                         "count": chk("REDRECON")["count"],
                         "mismatches": chk("REDRECON")["mismatches"]},
            "t1map": {"ok": chk("T1MAP")["ok"],
                      "inv_relevant_grids":
                          chk("T1MAP")["inv_relevant_grids"],
                      "window_grids": chk("T1MAP")["window_grids"],
                      "collapse_grids": chk("T1MAP")["collapse_grids"],
                      "noninv_t1_map_deviations":
                          chk("T1MAP")["noninv_t1_map_deviations"],
                      "fail_count": chk("T1MAP")["fail_count"]},
            "t2reg": {"ok": chk("T2REG")["ok"],
                      "count": chk("T2REG")["count"],
                      "fail_count": chk("T2REG")["fail_count"]},
            "deathfast": {"ok": chk("DEATHFAST")["ok"],
                          "count": chk("DEATHFAST")["count"],
                          "fail_count": chk("DEATHFAST")["fail_count"]},
            "invgen": {"ok": chk("INVGEN")["ok"],
                       "games": chk("INVGEN")["count"],
                       "died": chk("INVGEN")["died"],
                       "endgame_exits": chk("INVGEN")["endgame_exits"],
                       "inv_steps": chk("INVGEN")["inv_steps"],
                       "max_death_stretch": chk("INVGEN")["max_death_stretch"],
                       "max_spf": chk("INVGEN")["max_spf"],
                       "fail_count": chk("INVGEN")["fail_count"]},
            "freshpin": {"ok": chk("FRESHPIN")["ok"],
                         "count": chk("FRESHPIN")["count"],
                         "mismatches": chk("FRESHPIN")["mismatches"]},
            "canon": {"ok": chk("CANON")["ok"],
                      "stretch_entries_checked": chk("CANON")["count"],
                      "fail_count": chk("CANON")["fail_count"]},
            "trk": {"ok": chk("TRK")["ok"],
                    "games_checked": chk("TRK")["count"],
                    "fail_count": chk("TRK")["fail_count"]},
            "sieveobsgen": {"ok": chk("SIEVEOBSGEN")["ok"],
                            "games": chk("SIEVEOBSGEN")["count"],
                            "composite_games":
                                chk("SIEVEOBSGEN")["composite_games"],
                            "fail_count": chk("SIEVEOBSGEN")["fail_count"]},
            "sv7reg": {"ok": chk("SV7REG")["ok"],
                       "count": chk("SV7REG")["count"],
                       "fail_count": chk("SV7REG")["fail_count"]},
            "twincomp": {"ok": chk("TWINCOMP")["ok"],
                         "count": chk("TWINCOMP")["count"],
                         "law1_composites":
                             chk("TWINCOMP")["law1_composites"],
                         "law2_composites":
                             chk("TWINCOMP")["law2_composites"],
                         "law1_violations":
                             chk("TWINCOMP")["law1_violations"],
                         "law2_violations":
                             chk("TWINCOMP")["law2_violations"],
                         "prime_obs_law1": chk("TWINCOMP")["prime_obs_law1"],
                         "prime_obs_law2": chk("TWINCOMP")["prime_obs_law2"]},
        },
        "first_fails": {k: v.get("fails", [])[:5]
                        for k, v in r1["checks"].items()
                        if v.get("fail_count", 0) > 0},
    }
    out = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=1)
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    path = os.path.join(HERE, "output", "sievegen_audit.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out + "\n")
    print(json.dumps({"all_ok": audit["all_ok"],
                      "sha256": hashlib.sha256(out.encode()).hexdigest()},
                     sort_keys=True))
    sys.exit(0 if audit["all_ok"] else 1)


if __name__ == "__main__":
    main()
