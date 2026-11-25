#!/usr/bin/env python3
"""K0953 first-hit analysis: observed per-class first hits
(pkill_tight_tier3.json, 46 primes M<=199, K<=1e7) vs the BH-conditional
TAIL first-hit prediction.

PRE-TAIL-FIRSTHIT (machine fact, this file): 1545/1546 live classes
have their first value-one hit strictly below the tail seam
t0 = max(M,3); the single exception is (M,kappa)=(43,20), first hit
exactly at the seam t=43.  Hence the published FIRSTHIT-GROWTH law
F(M) ~ 1.767 * M^1.509 is entirely a pre-tail phenomenon.

TAIL-FIRSTHIT-PRED (BH-conditional): for each live class, the smallest
t >= t0 with BH-expected tail hits >= 1, by bisection on ln t
(tail-only integral: the pre-tail region contributes nothing).
Output: predicted scale K_hat = (M+1) t_hat + kappa, per-M
F_hat(M) = max_kappa K_hat, regression vs observed F(M).
"""
from __future__ import annotations
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from branch_density_core import Branches, pair_integral
from census_starvation import ss_cached   # SS-STRUCT closed form + memo

TIER3 = os.path.join(HERE, "..", "remo-hit-prime-pair-20261118",
                     "output", "pkill_tight_tier3.json")
GROWTH = os.path.join(HERE, "..", "remo-hit-prime-pair-20261118",
                     "output", "firsthit_growth.json")
OUT = os.path.join(HERE, "output", "firsthit_pred.json")

NODES = 48
ITER = 14
T_HI = 10 ** 9


def expected_tail(br: "Branches", ss: dict, T: int, t0: int) -> float:
    tot = 0.0
    M1 = br.M + 1
    for e in br.e_list:
        te = br.t_e[e]
        n_hi = (T - te) // e
        n_lo = max(0, -((te - t0) // e))
        if n_hi < n_lo:
            continue
        if n_lo <= 1:
            val = pair_integral(M1 * e, br.c1[e], br.A, br.c2[e],
                                n_hi, NODES)
        else:
            a1, c1_, a2, c2_ = M1 * e, br.c1[e], br.A, br.c2[e]
            val = (pair_integral(a1, c1_, a2, c2_, n_hi, NODES)
                   - pair_integral(a1, c1_, a2, c2_, n_lo - 1, NODES))
        tot += ss[e] * val
    return tot


def tail_first_hit(br: "Branches", ss: dict, t0: int):
    if expected_tail(br, ss, T_HI, t0) < 1.0:
        return float("inf")
    lo, hi = float(t0), float(T_HI)
    for _ in range(ITER):
        mid = math.sqrt(lo * hi)
        if expected_tail(br, ss, int(mid), t0) >= 1.0:
            hi = mid
        else:
            lo = mid
    return math.sqrt(lo * hi)


def main() -> None:
    tier3 = json.load(open(TIER3))
    growth = json.load(open(GROWTH))
    f_obs = {r["M"]: r["F"] for r in growth["per_M"]}
    rows = []
    for ms in sorted(tier3, key=int):
        M = int(ms)
        t0 = max(M, 3)
        for ks, K_first in sorted(tier3[ms]["first"].items(),
                                  key=lambda kv: int(kv[0])):
            kappa = int(ks)
            br = Branches(M, kappa)
            ss = {e: ss_cached(M, br.C, e) for e in br.e_list}
            t_hat = tail_first_hit(br, ss, t0)
            t_first = (K_first - kappa) // (M + 1)
            rows.append({
                "M": M, "kappa": kappa, "C": br.C,
                "n_branches": len(br.e_list),
                "K_first": K_first, "t_first": t_first,
                "pre_tail": t_first < t0, "t0": t0,
                "t_hat": (None if math.isinf(t_hat) else round(t_hat, 3)),
                "K_hat": (None if math.isinf(t_hat)
                          else round((M + 1) * t_hat + kappa, 1)),
            })
        print(f"M={M} done ({len(rows)} rows)", flush=True)
    # per-M aggregation
    per_M = []
    for ms in sorted(tier3, key=int):
        M = int(ms)
        sub = [r for r in rows if r["M"] == M]
        khats = [r["K_hat"] for r in sub if r["K_hat"] is not None]
        per_M.append({
            "M": M, "F_obs": f_obs.get(M), "F_hat": (max(khats)
                                                     if khats else None),
            "n_classes": len(sub),
            "median_that_over_t0": round(
                sorted(r["t_hat"] / r["t0"] for r in sub
                       if r["t_hat"] is not None)[len(sub) // 2], 4)
            if khats else None,
        })
    json.dump({"rows": rows, "per_M": per_M,
               "params": {"nodes": NODES, "iter": ITER, "t_hi": T_HI}},
              open(OUT, "w"), indent=1)
    print("wrote", OUT, "rows:", len(rows))


if __name__ == "__main__":
    main()
