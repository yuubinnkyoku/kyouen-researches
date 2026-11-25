#!/usr/bin/env python3
"""K0953 census + starvation analysis.

(1) CENSUS-EXACT: per-kappa exact value-one counts for prime
    M in {3,5,7,11,13,17,19,23} at K <= 2e5 (engine below the tail seam,
    K0952 branch union above), cross-checked against the published
    K0950 CENSUS-REPRO totals, plus the BH-conditional total prediction.
(2) STARVATION: (a) the 69 published cnt<=2 sparse classes
    (sparse_classes_le2.json) vs their C, branch count and BH-predicted
    count; (b) per-kappa exact counts for prime M <= 100 at K <= 2e5,
    (M,C)-group dispersion (Poisson consistency) and correlation with
    the BH class density.
"""
from __future__ import annotations
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "remo-hit-prime-pair-20261118"))
from branch_density_core import (Branches, primes_upto, sieve_set, is_prime,
                                 singular_series, pair_integral)
from composite_core import sigma_Z

SS_PRIMES = primes_upto(2_000_000)
KMAX = 200_000
_PSIEVE = sieve_set(20_000_000)   # covers all P for M <= 100 at K <= 2e5
_SS_CACHE = {}


def p_is_prime(P: int) -> bool:
    if P < 20_000_000:
        return bool(_PSIEVE[P])
    return is_prime(P)


_SS_BASE = {}


def ss_base(M: int, C: int) -> float:
    """SS(M,C,e=1) = G(M,C): full product over SS_PRIMES, memoized
    per (M, C)."""
    if (M, C) not in _SS_BASE:
        from branch_density_core import nu_case
        ss = 1.0
        for q in SS_PRIMES:
            nu = nu_case(q, M, 0, 1, C, 1)
            ss *= (1 - nu / q) / (1 - 1.0 / q) ** 2
        _SS_BASE[(M, C)] = ss
    return _SS_BASE[(M, C)]


def ss_cached(M: int, C: int, e: int) -> float:
    """SS_e = G(M,C) * prod_{q|e, q !| M(M+1)} (q-1)/(q-2)  (SS-STRUCT)."""
    ss = ss_base(M, C)
    if e > 1:
        x = e
        for q in _SMALL_PRIMES:
            if q * q > x:
                break
            if x % q == 0:
                while x % q == 0:
                    x //= q
                if M % q and (M + 1) % q:
                    ss *= (q - 1) / (q - 2)
        if x > 1 and x <= 10_000:
            q = x
            if M % q and (M + 1) % q:
                ss *= (q - 1) / (q - 2)
    return ss


_SMALL_PRIMES = primes_upto(1000)


def class_count(M: int, kappa: int, kmax: int, sv, with_small: bool = True):
    """(branch hits t in [t0, T], engine hits t in [1, t0), BH pred)."""
    br = Branches(M, kappa)
    T = (kmax - kappa) // (M + 1)
    t0 = max(M, 3)
    small = 0
    if with_small and br.live:
        for t in range(1, t0):
            K = (M + 1) * t + kappa
            if t == 1 and kappa == 0:
                continue          # (s,kappa)=(0,0): outside main regime
            if sigma_Z(M, K) == 1:
                small += 1
    branch = 0
    e_hist = {}
    if br.live:
        for e in br.e_list:
            te = br.t_e[e]
            n_lo = max(0, -((te - t0) // e))
            for n in range(n_lo, (T - te) // e + 1):
                t = te + e * n
                Y = (M + 1) * t + kappa + 1
                if not sv[Y]:
                    continue
                P = (br.A * t + br.B) // e
                if p_is_prime(P):
                    branch += 1
                    e_hist[e] = e_hist.get(e, 0) + 1
    pred = 0.0
    if br.live:
        for e in br.e_list:
            ss = ss_cached(M, br.C, e)
            te = br.t_e[e]
            n_hi = (T - te) // e
            n_lo = max(0, -((te - t0) // e))
            if n_hi >= n_lo:
                # integrate over [n_lo, n_hi] (tail starts at t0)
                val = ss * (pair_integral((M + 1) * e, br.c1[e], br.A,
                                         br.c2[e], n_hi) -
                            pair_integral((M + 1) * e, br.c1[e], br.A,
                                         br.c2[e], max(0, n_lo - 1)))
                pred += val
    return br, small, branch, pred, e_hist


def census() -> dict:
    pub = {3: 2057, 5: 2005, 7: 2603, 11: 3003, 13: 3220,
           17: 3475, 19: 3629, 23: 3739}
    out = {}
    for M in sorted(pub):
        sv = sieve_set((M + 1) * (KMAX // (M + 1) + 2) + M + 2)
        total = 0
        pred = 0.0
        per_kappa = {}
        for kap in range(M - 1):
            br, small, branch, p, _ = class_count(M, kap, KMAX, sv)
            total += small + branch
            pred += p + small
            per_kappa[kap] = small + branch
        out[str(M)] = {
            "M": M, "exact_total": total, "published_total": pub[M],
            "match": total == pub[M],
            "bh_pred_total": round(pred, 1),
            "ratio_exact_over_pred": round(total / pred, 4),
            "per_kappa": per_kappa,
        }
        print(f"census M={M:3d} exact={total} published={pub[M]} "
              f"match={total == pub[M]} pred={pred:.0f} "
              f"ratio={total / pred:.4f}", flush=True)
    return out


def starvation() -> dict:
    # (a) published cnt<=2 classes
    with open(os.path.join(HERE, "..", "remo-hit-prime-pair-20261118",
                           "output", "sparse_classes_le2.json")) as f:
        sparse = json.load(f)
    sv_cache = {}
    rows = []
    for cnt, M, kap, plist in sparse:
        br = Branches(M, kap)
        if M not in sv_cache:
            sv_cache[M] = sieve_set((M + 1) * (KMAX // (M + 1) + 2) + M + 2)
        _, _, branch, pred, _ = class_count(M, kap, KMAX, sv_cache[M],
                                            with_small=False)
        rows.append({"M": M, "kappa": kap, "cnt": cnt, "C": br.C,
                     "C_over_M": round(br.C / M, 4),
                     "n_branches": len(br), "single_branch": len(br) == 1,
                     "p_minus_2": len(plist) > 0,
                     "bh_pred_at_2e5": round(pred, 3),
                     "recount_branch_hits": branch})
    n_single = sum(r["single_branch"] for r in rows)
    n_pm2 = sum(r["p_minus_2"] for r in rows)
    # (b) per-kappa recount M <= 100
    per = []
    for M in primes_upto(100):
        sv = sieve_set((M + 1) * (KMAX // (M + 1) + 2) + M + 2)
        for kap in range(M - 1):
            br = Branches(M, kap)
            if not br.live:
                continue
            _, small, branch, pred, _ = class_count(M, kap, KMAX, sv)
            per.append({"M": M, "kappa": kap, "C": br.C,
                        "n_branches": len(br),
                        "count": small + branch, "bh_pred": round(pred, 3)})
    # (M,C)-group dispersion
    groups = {}
    for r in per:
        groups.setdefault((r["M"], r["C"]), []).append(r["count"])
    disp = []
    for (M, C), counts in sorted(groups.items()):
        n = len(counts)
        tot = sum(counts)
        if n >= 3 and tot >= 12:
            mean = tot / n
            var = sum((c - mean) ** 2 for c in counts) / (n - 1)
            disp.append({"M": M, "C": C, "n": n, "mean": round(mean, 2),
                         "var_over_mean": round(var / mean, 3)})
    n_poisson_ok = sum(1 for d in disp
                       if 0.25 <= d["var_over_mean"] <= 3.0)
    return {
        "sparse_classes": rows,
        "sparse_summary": {
            "n_classes": len(rows), "n_single_branch": n_single,
            "n_single_branch_frac": round(n_single / len(rows), 4),
            "n_p_minus_2": n_pm2,
            "n_p_minus_2_frac": round(n_pm2 / len(rows), 4),
            "median_C_over_M":
                sorted(r["C_over_M"] for r in rows)[len(rows) // 2],
        },
        "per_kappa_M_le_100": per,
        "group_dispersion": disp,
        "group_dispersion_summary": {
            "n_groups": len(disp),
            "n_poisson_consistent": n_poisson_ok,
        },
    }


def main() -> None:
    import sys as _s
    stage = _s.argv[1] if len(_s.argv) > 1 else "all"
    cen = census() if stage in ("all", "census") else {}
    if stage == "census":
        payload = {"experiment": "remo-branch-density-20261118", "census": cen}
        path = os.path.join(HERE, "output", "census.json")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, indent=1, sort_keys=True)
        print("wrote", path)
        return
    print("---", flush=True)
    sta = starvation()
    # quick summary prints
    s = sta["sparse_summary"]
    print("sparse: n=", s["n_classes"], "single_branch=",
          s["n_single_branch"], f"({s['n_single_branch_frac']:.0%})",
          "p-2:", s["n_p_minus_2"], f"({s['n_p_minus_2_frac']:.0%})",
          "median C/M=", s["median_C_over_M"], flush=True)
    d = sta["group_dispersion_summary"]
    print("groups: n=", d["n_groups"], "poisson-consistent=",
          d["n_poisson_consistent"], flush=True)
    payload = {"experiment": "remo-branch-density-20261118",
               "starvation": sta}
    path = os.path.join(HERE, "output", "starvation.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, indent=1, sort_keys=True)
    print("wrote", path)


if __name__ == "__main__":
    main()
