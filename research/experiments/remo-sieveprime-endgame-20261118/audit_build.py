#!/usr/bin/env python3
"""Audit builder for K0939 (END-SIEVE / SIEVE-PRIME). Runs every check of
sieveprime_verify.run_checks() twice in-process, asserts the two runs are
identical, and writes output/sieveprime_audit.json (deterministic: no
timestamps, sort_keys, indent=1).

This file replaces a corrupted publish-time copy: the bytes previously
committed under this name were the audit JSON body itself (1033 bytes,
byte-identical to output/sieveprime_audit.json), so the builder script
was missing from the repository.  The audit JSON in output/ was correct
all along: sha256 of its content without the trailing newline is
07d844c62df54014d8b720a98dbcd51e44dd6e50b52d74c8b05a3e2d03f6a0b3, the
value published in the K0939 report and item.  This builder reproduces
those exact bytes from the committed verifier, restoring fresh-checkout
reproducibility of the K0939 machine anchor.

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

import sieveprime_verify as V  # noqa: E402


def main():
    r1 = V.run_checks()
    r2 = V.run_checks()
    same = json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)

    def chk(name):
        return r1["checks"][name]

    audit = {
        "all_ok": bool(r1["all_ok"] and r2["all_ok"] and same),
        "runs_identical": bool(same),
        "region": {"entry_m_hi": V.MBIG,
                   "entry_n_bound": 2 * V.MBIG + 3,
                   "pinrepro_m_hi": V.M_REPRO,
                   "engine_m_hi": V.M_ENG,
                   "family_w_hi": V.FAM_W},
        "checks": {
            "pin": {"ok": chk("PIN")["ok"],
                    "uv_sha256_8": chk("PIN")["uv_sha256"],
                    "p_sha256_8": chk("PIN")["p_sha256"]},
            "redrecon": {"ok": chk("REDRECON")["ok"],
                         "count": chk("REDRECON")["count"],
                         "mismatches": chk("REDRECON")["mismatches"]},
            "family": {"ok": chk("FAMILY")["ok"],
                       "family_states": chk("FAMILY")["count"],
                       "phases": chk("FAMILY")["phases"],
                       "transition_checks":
                           chk("FAMILY")["transition_checks"],
                       "emodel_fails": chk("FAMILY")["emodel_fails"],
                       "struct_fails": chk("FAMILY")["struct_fails"],
                       "watchpos_fails": chk("FAMILY")["watchpos_fails"],
                       "inv_fails": chk("FAMILY")["inv_fails"],
                       "trans_fails": chk("FAMILY")["trans_fails"],
                       "cong_fails": chk("FAMILY")["cong_fails"],
                       "iff_fails": chk("FAMILY")["iff_fails"]},
            "entry": {"ok": chk("ENTRY")["ok"],
                      "prime_games": chk("ENTRY")["count"],
                      "emodel_fails": chk("ENTRY")["emodel_fails"],
                      "fail_count": chk("ENTRY")["fail_count"],
                      "max_entry_w": chk("ENTRY")["max_entry_w"]},
            "pinrepro": {"ok": chk("PINREPRO")["ok"],
                         "games": chk("PINREPRO")["count"],
                         "fail_count": chk("PINREPRO")["fail_count"]},
            "engine": {"ok": chk("ENGINE")["ok"],
                       "games": chk("ENGINE")["count"],
                       "fail_count": chk("ENGINE")["fail_count"]},
            "pinsieve": {"ok": chk("PINSIEVE")["ok"],
                         "law1_violations": chk("PINSIEVE")["law1_violations"],
                         "law2_violations": chk("PINSIEVE")["law2_violations"],
                         "v_violations": chk("PINSIEVE")["v_violations"],
                         "u_violations": chk("PINSIEVE")["u_violations"]},
        },
        "first_fails": {k: v.get("fails", [])[:5]
                        for k, v in r1["checks"].items()
                        if v.get("fail_count", 0) > 0},
    }
    out = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=1)
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    path = os.path.join(HERE, "output", "sieveprime_audit.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out + "\n")
    print(json.dumps({"all_ok": audit["all_ok"],
                      "sha256": hashlib.sha256(out.encode()).hexdigest()},
                     sort_keys=True))
    sys.exit(0 if audit["all_ok"] else 1)


if __name__ == "__main__":
    main()
