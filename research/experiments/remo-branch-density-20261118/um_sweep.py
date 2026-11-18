#!/usr/bin/env python3
"""K0953 U_M sweep: exact value-one counts for the kappa=0 family
U_M = {u : sigma_Z(M,(M+1)u) = 1}, engine below the tail seam and the
K0952 branch union above it, plus the BH prediction
U_M(N) ~ sum_e SS_e * integral_0^{(N-t_e)/e} dn/(ln Y_e(n) ln P_e(n))
(conditional on Bateman-Horn for the branch pairs; ALL-ADM makes every
SS_e positive).  NO extra 1/e factor: the upper limit (N-t_e)/e already
carries the Jacobian dn = dt/e of the t-to-n change of variables
(report.md, U_M-DENSITY remark)."""
from __future__ import annotations
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from branch_density_core import (Branches, primes_upto, sieve_set, is_prime,
                                 singular_series, pair_integral)
from composite_core import sigma_Z

SS_PRIMES = primes_upto(2_000_000)


def um_exact(M: int, U: int) -> dict:
    """Count U_M up to u <= U and record seam agreement."""
    br = Branches(M, 0)
    assert br.live
    t0 = max(M, 3)
    # sieve Y = (M+1)u+1 for u in [t0, U]
    lo = t0
    hi = U
    ymax = (M + 1) * hi + 1
    sv = sieve_set(ymax)
    small = 0
    small_hits = []
    for u in range(1, t0):
        if sigma_Z(M, (M + 1) * u) == 1:
            small += 1
            small_hits.append(u)
    # seam check: engine vs branch on [t0, t0+40]
    seam_states = 0
    seam_mismatch = 0
    for u in range(t0, min(t0 + 40, hi) + 1):
        seam_states += 1
        Y = (M + 1) * u + 1
        eng = sigma_Z(M, (M + 1) * u) == 1
        brh = bool(sv[Y]) and any(
            (u - br.t_e[e]) % e == 0 and is_prime((br.A * u + br.B) // e)
            for e in br.e_list)
        if eng != brh:
            seam_mismatch += 1
    # exact branch count
    n_hits = 0
    e_hist = {}
    for e in br.e_list:
        te = br.t_e[e]
        n_lo = max(0, -((te - lo) // e))
        for n in range(n_lo, (hi - te) // e + 1):
            u = te + e * n
            Y = (M + 1) * u + 1
            if not sv[Y]:
                continue
            P = (br.A * u + br.B) // e
            if is_prime(P):
                n_hits += 1
                e_hist[e] = e_hist.get(e, 0) + 1
    # BH prediction
    pred = 0.0
    pred_by_e = {}
    for e in br.e_list:
        ss = singular_series(br, e, SS_PRIMES)
        te = br.t_e[e]
        n_hi = (hi - te) // e
        val = ss * pair_integral((M + 1) * e, br.c1[e], br.A,
                                 br.c2[e], n_hi)
        pred_by_e[e] = val
        pred += val
    total = small + n_hits
    return {
        "M": M, "U": U, "exact_total": total, "engine_small": small,
        "small_hits": small_hits, "branch_hits": n_hits,
        "branch_hist_by_e": {str(k): v for k, v in sorted(e_hist.items())},
        "n_branches": len(br.e_list), "C": br.C, "A": br.A, "B": br.B,
        "branches": [{"e": e, "t_e": br.t_e[e], "c1": br.c1[e],
                      "c2": br.c2[e],
                      "SS": round(singular_series(br, e, SS_PRIMES), 6)}
                     for e in br.e_list],
        "bh_pred": pred, "bh_pred_by_e":
            {str(k): round(v, 4) for k, v in pred_by_e.items()},
        "ratio_exact_over_pred": round(total / pred, 5) if pred else None,
        "seam_states": seam_states, "seam_mismatch": seam_mismatch,
    }


def main() -> None:
    jobs = [(2, 333_333), (2, 66_666), (2, 20_000), (2, 100_000),
            (3, 1_000_000), (3, 100_000), (3, 20_000), (3, 100_000),
            (5, 1_000_000), (5, 100_000), (5, 20_000),
            (7, 1_000_000), (7, 100_000), (7, 20_000),
            (11, 100_000), (11, 20_000),
            (13, 100_000), (13, 20_000),
            (17, 100_000), (19, 100_000), (23, 100_000),
            (29, 100_000), (31, 100_000)]
    out = []
    for M, U in jobs:
        rec = um_exact(M, U)
        out.append(rec)
        print(f"M={M:3d} U={U:8d} exact={rec['exact_total']:7d} "
              f"pred={rec['bh_pred']:9.2f} ratio={rec['ratio_exact_over_pred']}"
              f" seam_mm={rec['seam_mismatch']}", flush=True)
    path = os.path.join(HERE, "output", "um_sweep.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"experiment": "remo-branch-density-20261118",
                   "um_sweep": out}, f, indent=1, sort_keys=True)
    print("wrote", path)


if __name__ == "__main__":
    main()
