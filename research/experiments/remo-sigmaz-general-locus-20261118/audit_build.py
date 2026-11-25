#!/usr/bin/env python3
"""K0946 audit builder.

Runs `node sigma_locus_core.js audit` (deterministic), cross-checks the
JS results against the PINNED K0941 Python core (composite_core.py,
sha256-verified against the committed copy) element by element, and
writes output/sigma_locus_audit.json.

Deterministic: no clock, no randomness. Run it twice and byte-compare
output/sigma_locus_audit.json to check determinism.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from composite_core import sigma_E, sigma_Z  # pinned K0941 core

CORE_SHAS = {
    "sievegen_core.py":
        "a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e4714c50bbc68bef1843499",
    "composite_core.py":
        "3990d67ff3a89f480bd92ae784a9efa763d76264e2b8e4a2d1752507a4740f40",
}


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    # 1. COREPIN
    corepin = {}
    for name, expect in CORE_SHAS.items():
        got = sha256(os.path.join(HERE, name))
        corepin[name] = {"sha256": got, "match": got == expect}
    if not all(v["match"] for v in corepin.values()):
        print("COREPIN FAILED", corepin, file=sys.stderr)
        sys.exit(1)

    # 2. JS audit (single run; determinism checked by running audit_build twice)
    out = subprocess.run(["node", os.path.join(HERE, "sigma_locus_core.js"), "audit"],
                          capture_output=True, text=True, check=True)
    rep = json.loads(out.stdout.strip().splitlines()[-1])

    py = {}

    # 3. zgrid: element-wise pinned sigma_Z vs JS naive port, M 1..12, K 2..1200
    zf = 0; zn = 0
    for m in range(1, 13):
        js = rep["zgrid_py"][str(m)]
        for i, K in enumerate(range(2, 1201)):
            zn += 1
            if sigma_Z(m, K) != js[i]:
                zf += 1
    py["zgrid_pinned_vs_js"] = {"states": zn, "fails": zf}

    # 4. egrid: element-wise pinned sigma_E vs JS naive port, P 0..8, k 2..40, all alpha
    ef = 0; en = 0
    for P in range(0, 9):
        byp = rep["egrid_py"][str(P)]
        for j, k in enumerate(range(2, 41)):
            vals = byp[j]
            for alpha in range(0, k + 1):
                en += 1
                if sigma_E(P, alpha, k - alpha) != vals[alpha]:
                    ef += 1
    py["egrid_pinned_vs_js"] = {"states": en, "fails": ef}

    # 5. classify re-verify with the pinned core (M in {2,3,5,7}, K <= 6000)
    cl = {}
    for M in (2, 3, 5, 7):
        g = M + 1
        hits = 0; silent = 0; mismatch = 0
        for K in range(M + 1, 6001):
            if sigma_Z(M, K) != 1:
                continue
            hits += 1
            if fast_hit_mismatch(M, K, g):
                mismatch += 1
            else:
                silent += 1
        cl[str(M)] = {"hits": hits, "silent_confirmed": silent, "mismatch": mismatch}
    py["classify_pinned"] = cl

    # 6. hits_small: full hit-set comparison, all M 1..40, K 2..1200
    hf = 0; hn = 0
    for M in range(1, 41):
        js_hits = set(rep["hits_small"][str(M)])
        py_hits = set(K for K in range(2, 1201) if sigma_Z(M, K) == 1)
        hn += len(js_hits) + len(py_hits)
        if js_hits != py_hits:
            hf += 1
    py["hits_small_pinned_vs_js"] = {"M_values": 40, "set_mismatches": hf}

    # 7. excl1 reduced form with the pinned core
    xf = 0; xn = 0
    for M in range(2, 17):
        for s in range(0, 21):
            xn += 1
            if sigma_E(M + 1, M * (s + 2) - 1, 0) == 0:
                xf += 1
    py["excl1_pinned"] = {"states": xn, "zeros": xf}

    all_ok = (
        all(v["fails"] == 0 for v in rep["cross"].values())
        and all(v["cascade"] == 0 and v["naive_mismatch"] == 0
                and v["run_identity_fail"] == 0
                for v in rep["classify"].values())
        and rep["excl1"]["zeros"] == 0
        and zf == 0 and ef == 0
        and all(v["mismatch"] == 0 and v["hits"] > 0 for v in cl.values())
        and hf == 0
        and xf == 0
    )

    audit = {
        "all_ok": all_ok,
        "corepin": corepin,
        "js_audit": rep,
        "py_checks": py,
    }
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    dst = os.path.join(HERE, "output", "sigma_locus_audit.json")
    with open(dst, "w") as f:
        json.dump(audit, f, sort_keys=True, separators=(",", ":"))
        f.write("\n")
    print("wrote", dst, "all_ok=", all_ok)


def fast_hit_mismatch(M, K, g):
    """Pinned-core replication of the JS classify silent test."""
    kappa = K % g
    s = (K - M - 1) // g
    if (K - M - 1) - s * g != kappa:
        return True
    return sigma_E(M, kappa, M * (s + 1)) != kappa + 1


if __name__ == "__main__":
    main()
