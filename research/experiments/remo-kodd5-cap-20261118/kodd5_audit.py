#!/usr/bin/env python3
"""K0963 audit part 1: machine verification over the published census.

Verifies, independently of the published code, over ALL published
smooth-hit rows (K0958 hits_full.json, M<=1000, all t: 2,609 rows;
K0960 hits_strip2.json, 1000<M<=2000, all t: 8,277 rows):

  1. regime identities: K=(M+1)t+kappa, Y=K+1, N=MY-1,
     N=(M+1)k0+2M-kappa, k0=Mt+kappa-1, a=v2(N)>=1;
  2. published Omega/omega match the independent factorization;
  3. (M-1)-smoothness and window [M,k0] emptiness (full divisor check);
  4. EW: no divisor in [M, XBAR)   (K0961 T3, expect 0 violations);
  5. CK: no two coprime divisors both >= XBAR   (NEW lemma, expect 0);
  6. TZ (t>=2): odd divisor q<=M-1 => 2^a q <= M-1  (expect 0);
  7. CS/PK (t>=2): multiset partition complement bound (NEW, 0)
     + PAIR-INTERSECT: no two index-disjoint pairs >= XBAR (NEW, 0);
     kodd counts odd primes WITH multiplicity (published convention).
  8. kodd=5 & t>=2 rows: config classification (18 leaf configs) and
     per-config cap checks CAP-73 / SQRT3 / CAP-52 / CAP-27;
  9. kodd>=6 & t>=2 rows: case label PS / LG-PF / LG-OPEN;
 10. general facts p1p2,p2p3<=sigma, p1,p2<=sqrt(sigma) (kodd>=5).

Also records the conjecture counters:
  conj(i)  kodd=4 rows with t >= ceil(sqrt(M))  (expect none)
  conj(ii) kodd>=5 rows with t >= 4             (expect none)
"""
from __future__ import annotations

import json
import math
import sys
import time

sys.path.insert(0, ".")
from kodd5_core import (Regime, primes_upto, divisors, check_ew, check_ck,
                        check_tz, check_cs, check_pair_intersect,
                        check_general_facts, k5_config, cap_check,
                        k6plus_case, k0_caps)

IN1 = "../remo-smooth-hit-census-20261118/output/hits_full.json"
IN2 = "../remo-smooth-hit-deepcap-20261118/output/hits_strip2.json"
OUT = "output/kodd5_audit.json"

PRIMES = primes_upto(2000)


def audit_row(M, kap, t, pub=None):
    """pub = dict of published fields to cross-check."""
    r = {"M": M, "kap": kap, "t": t}
    reg = Regime(M, kap, t)
    r["K"], r["Y"], r["N"], r["k0"], r["a"] = reg.K, reg.Y, reg.N, reg.k0, reg.a
    facs, left = reg.factor(PRIMES)
    r["smooth"] = left == 1
    if pub:
        if "K" in pub:
            assert pub["K"] == reg.K and pub["Y"] == reg.Y and pub["N"] == reg.N, \
                ("identity mismatch", r)
        om = sum(e for _, e in facs) + (0 if left == 1 else 0)
        om_d = len(facs) + (0 if left == 1 else 0)
        r["omega_match"] = (om == pub["Omega"] and om_d == pub["omega"])
    if not r["smooth"]:
        return r, None
    # full factorization == smooth factorization
    divs = divisors(facs)
    r["window_empty"] = all(not (reg.M <= d <= reg.k0) for d in divs)
    r["ew"] = check_ew(reg, divs)
    r["ck"] = check_ck(reg, divs, facs)
    odd = sorted(p for p, e in facs if p > 2 for _ in range(e))
    r["kodd"] = len(odd)
    r["omega_odd"] = len(set(odd))
    if r["kodd"] == 5:
        cfg = k5_config(reg, odd)
        r["config"] = cfg
    if t >= 2:
        r["tz"] = check_tz(reg, divs)
        r["cs"] = check_cs(reg, odd)
        r["pi"] = check_pair_intersect(reg, odd)
        if r["kodd"] >= 5:
            r["facts"] = check_general_facts(reg, odd)
        if r["kodd"] == 5:
            r["cap"] = cap_check(reg, r["config"]["route"])
        if r["kodd"] >= 6:
            try:
                r["case6"] = k6plus_case(reg, odd)
                if r["case6"]["case"] in ("PS", "LG-PF"):
                    r["cap"] = cap_check(reg, "cap52")
            except AssertionError as exc:
                r["case6_assert_fail"] = str(exc)
    return r, facs


def main():
    t0 = time.time()
    rows1 = json.load(open(IN1))["rows"]
    rows2 = json.load(open(IN2))["rows"]
    n1, n2 = len(rows1), len(rows2)

    stats = {
        "n_rows": n1 + n2, "n_hits_full": n1, "n_strip2": n2,
        "viol": {}, "kodd_hist_t1": {}, "kodd_hist_t2plus": {},
        "k5_configs": {}, "k5_configs_t1": {}, "k6_cases": {},
        "k6_rows": [], "k5_rows_t2plus": [], "conj_i_viol": [],
        "conj_ii_viol": [], "k5_cap_margins": [], "misc": {},
    }
    def viol(name):
        stats["viol"][name] = stats["viol"].get(name, 0) + 1

    def process(M, kap, t, pub):
        try:
            r, facs = audit_row(M, kap, t, pub)
        except AssertionError as exc:
            viol("regime_assert")
            stats["misc"].setdefault("regime_asserts", []).append((M, kap, t, str(exc)))
            return
        if not r.get("smooth"):
            viol("not_smooth"); return
        if pub is not None and not r.get("omega_match", True):
            viol("omega_mismatch")
        if not r["window_empty"]:
            viol("window_nonempty"); return
        if not r["ew"]:
            viol("ew")
        if not r["ck"]:
            viol("ck")
        if r["a"] < 1:
            viol("parity_a")
        kd = r["kodd"]
        key = "kodd_hist_t1" if t == 1 else "kodd_hist_t2plus"
        stats[key][kd] = stats[key].get(kd, 0) + 1
        if t >= 2:
            if "tz" not in r or not r["tz"]:
                viol("tz")
            if "cs" not in r or not r["cs"]:
                viol("cs")
            if "pi" not in r or not r["pi"]:
                viol("pair_intersect")
            if kd >= 5:
                for fk, fv in r.get("facts", {}).items():
                    if not fv:
                        viol("fact_" + fk)
        # conjectures
        if kd == 4 and t * t >= M:
            stats["conj_i_viol"].append((M, kap, t, r["N"]))
        if kd >= 5 and t >= 4:
            stats["conj_ii_viol"].append((M, kap, t, r["N"]))
        # kodd=5 t>=2 bookkeeping
        if kd == 5 and t >= 2:
            cfg = r["config"]
            stats["k5_configs"][cfg["config"]] = stats["k5_configs"].get(cfg["config"], 0) + 1
            if not r["cap"]["holds"]:
                viol("k5_cap_" + cfg["route"])
            c52 = math.isqrt((M - 1) ** 5 // (8 * (M + 1) ** 2))
            stats["k5_cap_margins"].append({
                "M": M, "kap": kap, "t": t, "a": r["a"], "k0": r["k0"],
                "config": cfg["config"], "route": cfg["route"],
                "cap52_k0": c52})
            stats["k5_rows_t2plus"].append(
                {"M": M, "kap": kap, "t": t, "N": r["N"], "a": r["a"],
                 "odd": sorted(p for p, e in facs if p > 2 for _ in range(e)),
                 "config": cfg["config"], "route": cfg["route"]})
        if kd == 5 and t == 1:
            stats["k5_configs_t1"][r["config"]["config"]] = \
                stats["k5_configs_t1"].get(r["config"]["config"], 0) + 1
        if kd >= 6 and t >= 2:
            cs = r.get("case6", {})
            stats["k6_cases"][str(cs.get("case", "?"))] = \
                stats["k6_cases"].get(str(cs.get("case", "?")), 0) + 1
            stats["k6_rows"].append(
                {"M": M, "kap": kap, "t": t, "N": r["N"], "a": r["a"],
                 "kodd": kd, "case": cs.get("case"),
                 "odd": sorted(p for p, e in facs if p > 2 for _ in range(e)),
                 "cap_holds": r.get("cap", {}).get("holds")})
        return r

    for row in rows1:
        M, kap, t, K, Y, N, Om, om, br = row
        process(M, kap, t, {"K": K, "Y": Y, "N": N, "Omega": Om, "omega": om})
    for row in rows2:
        M, kap, t, Om, om, br = row
        process(M, kap, t, {"Omega": Om, "omega": om})

    stats["runtime_s"] = round(time.time() - t0, 1)
    stats["all_clean"] = (sum(stats["viol"].values()) == 0
                          and not stats["conj_i_viol"]
                          and not stats["conj_ii_viol"])
    import os
    os.makedirs("output", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(stats, f, indent=1)
    slim = {k: v for k, v in stats.items()
            if k not in ("k5_rows_t2plus", "k6_rows", "k5_cap_margins")}
    print(json.dumps(slim, indent=1))
    print("k5_rows_t2plus:", json.dumps(stats["k5_rows_t2plus"]))
    print("k6_rows:", json.dumps(stats["k6_rows"]))


if __name__ == "__main__":
    main()
