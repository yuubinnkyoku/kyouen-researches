#!/usr/bin/env python3
"""K0964 audit: independent full verification of every mode-B row.

Independence: the Node engine found rows by AP sieve-walk; this audit
re-derives everything by plain trial division with a fresh prime list
and re-checks every published predicate with exact integer arithmetic.

Checks per kodd=4 row (and core checks shared with k5p/k3deep rows):
  structure: M prime in (2000,10000], live kappa, t in band (part 1:
    t<=T36 all-kappa / part 2: kap==0, T36<t<=T12)
  Y=(M+1)t+kap+1 prime, N=MY-1, k0=Mt+kap-1, identity N=(M+1)k0+2M-kap
  a=v2(N)>=1 matches, kap even (parity)
  independent factorization -> odd multiset, kodd, (M-1)-smooth
  window empty (all divisors vs [M,k0])
  TWO-ZONE (K0961 T1), EFFECTIVE-WINDOW (K0961 T3)
  K4-A (p3p4>=M), K4 dichotomy (T7), branch alpha/beta/gamma
  branch caps: alpha (Mt-1)^2*2^{3a}<(M-1)^3;
               gamma weak M*t<=isqrt-free floor((M-1)/2^a)^2;
               gamma sharp kap>=1: t*2^{2a}*p1^2<=M-2;
               gamma sharp kap==0: t*2^{2a}*p1<=M-2
  conj(i) violation status: t >= isqrt(M)+1
kodd=5 rows additionally: published kodd5_core config/route + cap_check
  + K5-CAP band check t<=T5(M).
kodd>=6 rows: k6plus_case label + conj(ii) status (t<=3).
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.join(_HERE, "..", "remo-kodd5-cap-20261118")):
    if os.path.isdir(_p):
        sys.path.insert(0, _p)
from kodd5_core import (Regime, is_prime, primes_upto, band_tmax,
                        k5_config, cap_check, k6plus_case, divisors)

HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.join(HERE, "audit_progress.json")


def audit_core(r: dict, bnd: dict, small_primes: list) -> dict:
    M, t, kap = r["M"], r["t"], r["kap"]
    ok = {}
    ok["M_prime"] = is_prime(M)
    ok["M_range"] = 2000 < M <= 10000
    ok["kap_live"] = 0 <= kap <= M - 2 and (t, kap) != (1, 0) and t >= 2
    ok["band"] = (t <= bnd["T36"] if r["part"] == 1 else
                  (kap == 0 and bnd["T36"] < t <= bnd["T12"]))
    Y = (M + 1) * t + kap + 1
    ok["Y"] = Y == r["Y"] and is_prime(Y)
    N = M * Y - 1
    ok["N"] = N == r["N"]
    k0 = M * t + kap - 1
    ok["k0"] = k0 == r["k0"]
    ok["identity"] = N == (M + 1) * k0 + 2 * M - kap
    a = (N & -N).bit_length() - 1
    ok["a"] = a == r["a"] and a >= 1
    ok["parity_kap_even"] = kap % 2 == 0
    # independent factorization by trial division
    facs = []
    m = N
    for p in small_primes:
        if p > M - 1 or m == 1:
            break
        if m % p == 0:
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            facs.append((p, e))
    ok["smooth"] = m == 1
    odd = sorted(p for p, e in facs if p > 2 for _ in range(e))
    ok["kodd_multiset"] = odd == r["odd"]
    ok["kodd"] = len(odd) == r.get("kodd", len(odd))
    divs = divisors(facs)
    ok["window_empty"] = all(not (M <= d <= k0) for d in divs)
    # TWO-ZONE: odd divisor q <= M-1 => 2^a q <= M-1
    ok["two_zone"] = all(((d & 1) == 1 and d <= M - 1) is False or
                         (1 << a) * d <= M - 1 for d in divs)
    # EFFECTIVE-WINDOW: no divisor in [M, XBAR), XBAR=(M+1)k0/(M-1)
    xb_lo, xb_hi = (M + 1) * k0, M - 1
    ok["eff_window"] = all(not (d >= M and d * xb_hi < xb_lo) for d in divs)
    return {"ok": ok, "a": a, "odd": odd, "facs": facs, "k0": k0, "Y": Y}


def k4_branch_checks(M, t, kap, a, odd, k0) -> dict:
    p1, p2, p3, p4 = odd
    ok = {}
    ok["k4A_top_pair"] = p3 * p4 >= M
    ok["dich1"] = not (p2 * p3 >= M and p1 * p4 >= M)
    ok["dich2"] = not (p1 * p3 >= M and p2 * p4 >= M)
    if p2 * p3 >= M:
        branch = "gamma"
    elif p1 * p4 >= M:
        branch = "alpha"
    else:
        branch = "beta"
    ok["beta_empty"] = branch != "beta"
    if branch == "alpha":
        # t < ((M-1)^{3/2}/2^{3a/2}+1)/M  <=> (Mt-1)^2*2^{3a} < (M-1)^3
        ok["cap_alpha"] = (M * t - 1) ** 2 * (1 << (3 * a)) < (M - 1) ** 3
    if branch == "gamma":
        q = (M - 1) // (1 << a)
        ok["cap_gamma_weak"] = M * t <= q * q
        if kap >= 1:
            ok["cap_gamma_sharp"] = t * (1 << (2 * a)) * p1 * p1 <= M - 2
        else:
            ok["cap_gamma_sharp0"] = t * (1 << (2 * a)) * p1 <= M - 2
    return {"ok": ok, "branch": branch}


def main() -> None:
    t0 = time.time()
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 240.0
    bounds = {b["M"]: b for b in json.load(open("bounds_bandB.json"))}
    small_primes = primes_upto(10000)

    prog = {"k4": 0, "k5p": 0, "k3d": 0, "done": False,
            "bad": [], "stats": {}, "k4_rows_n": None}
    if os.path.exists(PROG):
        prog = json.load(open(PROG))
    else:
        # file sizes first
        prog["k4_rows_n"] = sum(1 for _ in open("modeB/rows_k4.jsonl"))
        prog["k5p_rows_n"] = sum(1 for _ in open("modeB/rows_k5p.jsonl"))
        prog["k3d_rows_n"] = sum(1 for _ in open("modeB/rows_k3deep.jsonl"))
        json.dump(prog, open(PROG, "w"))

    def fail(kind, r, msg):
        prog["bad"].append({"kind": kind, "row": r, "msg": msg})
        if len(prog["bad"]) > 50:
            raise SystemExit("too many failures: " + msg)

    # ---- kodd=4 rows ----
    st = prog.setdefault("k4_stats", {"n": 0, "branch": {}, "viol": 0,
                                      "viol_rows": [], "kap0": 0,
                                      "sat_hist": {}, "a_hist": {},
                                      "p1_hist": {}, "min_M_per_t": {},
                                      "max_t": 0})
    with open("modeB/rows_k4.jsonl") as f:
        for i, line in enumerate(f):
            if i < prog["k4"]:
                continue
            if i > prog["k4"] and time.time() - t0 > budget:
                break
            prog["k4"] = i + 1
            r = json.loads(line)
            bnd = bounds[r["M"]]
            c = audit_core(r, bnd, small_primes)
            for k, v in c["ok"].items():
                if not v:
                    fail("k4", r, k)
            if len(c["odd"]) != 4:
                fail("k4", r, "kodd!=4")
                continue
            br = k4_branch_checks(r["M"], r["t"], r["kap"], c["a"],
                                  c["odd"], c["k0"])
            for k, v in br["ok"].items():
                if not v:
                    fail("k4", r, k)
            st["n"] += 1
            st["branch"][br["branch"]] = st["branch"].get(br["branch"], 0) + 1
            st["a_hist"][str(c["a"])] = st["a_hist"].get(str(c["a"]), 0) + 1
            st["p1_hist"][str(c["odd"][0])] = st["p1_hist"].get(str(c["odd"][0]), 0) + 1
            if r["kap"] == 0:
                st["kap0"] += 1
            viol = r["t"] >= math.isqrt(r["M"]) + 1
            if viol:
                st["viol"] += 1
                st["viol_rows"].append({k: r[k] for k in
                    ("M", "t", "kap", "Y", "N", "a", "k0", "odd", "part")})
                if br["branch"] != "gamma":
                    fail("k4", r, "violation-not-gamma")
                if r["kap"] < 1:
                    fail("k4", r, "violation-kap0")
            if r["t"] > st["max_t"]:
                st["max_t"] = r["t"]
            mmt = st["min_M_per_t"]
            if r["t"] not in mmt or r["M"] < mmt[r["t"]]["M"]:
                mmt[r["t"]] = {"M": r["M"], "kap": r["kap"]}
            # gamma sharp saturation (kap>=1)
            if br["branch"] == "gamma" and r["kap"] >= 1:
                sat = r["t"] * (1 << (2 * c["a"])) * c["odd"][0] ** 2 / (r["M"] - 2)
                b = min(int(sat * 10), 10)
                st["sat_hist"][str(b)] = st["sat_hist"].get(str(b), 0) + 1

    # ---- kodd=5 / >=6 rows ----
    st5 = prog.setdefault("k5p_stats", {"n5": 0, "n6p": 0, "t_over_T5": 0,
                                        "t_le3_ge6": 0, "over_t5_rows": [],
                                        "k5_t_hist": {}, "a_hist": {},
                                        "k6_cases": {}, "conj2_bad": []})
    with open("modeB/rows_k5p.jsonl") as f:
        for i, line in enumerate(f):
            if i < prog["k5p"]:
                continue
            if i > prog["k5p"] and time.time() - t0 > budget:
                break
            prog["k5p"] = i + 1
            r = json.loads(line)
            bnd = bounds[r["M"]]
            c = audit_core(r, bnd, small_primes)
            for k, v in c["ok"].items():
                if not v:
                    fail("k5p", r, k)
            if len(c["odd"]) != r["kodd"]:
                fail("k5p", r, "kodd-mismatch")
                continue
            if r["kodd"] == 5:
                st5["n5"] += 1
                reg = Regime(r["M"], r["kap"], r["t"])
                cfg = k5_config(reg, c["odd"])
                cp = cap_check(reg, cfg["route"])
                if not cp["holds"]:
                    fail("k5p", r, "cap-fails-" + cfg["route"])
                T5 = band_tmax(r["M"])
                if r["t"] > T5:
                    st5["t_over_T5"] += 1
                    st5["over_t5_rows"].append(r)
                st5["k5_t_hist"][str(r["t"])] = st5["k5_t_hist"].get(str(r["t"]), 0) + 1
                st5["a_hist"][str(c["a"])] = st5["a_hist"].get(str(c["a"]), 0) + 1
            else:
                st5["n6p"] += 1
                reg = Regime(r["M"], r["kap"], r["t"])
                lab = k6plus_case(reg, c["odd"])["case"]
                st5["k6_cases"][lab] = st5["k6_cases"].get(lab, 0) + 1
                if r["t"] <= 3:
                    st5["t_le3_ge6"] += 1
                else:
                    st5["conj2_bad"].append(r)

    # ---- kodd=3 deep rows (full verification) ----
    st3 = prog.setdefault("k3d_stats", {"n": 0, "viol_tmax": 0,
                                        "tmax_row": None, "deep_ok": 0})
    with open("modeB/rows_k3deep.jsonl") as f:
        for i, line in enumerate(f):
            if i < prog["k3d"]:
                continue
            if i > prog["k3d"] and time.time() - t0 > budget:
                break
            prog["k3d"] = i + 1
            r = json.loads(line)
            bnd = bounds[r["M"]]
            if r["t"] < bnd["csqrt"]:
                fail("k3d", r, "not-deep")
            c = audit_core(r, bnd, small_primes)
            for k, v in c["ok"].items():
                if not v:
                    fail("k3d", r, k)
            if len(c["odd"]) != 3:
                fail("k3d", r, "kodd!=3")
                continue
            st3["n"] += 1
            if r["t"] > st3["viol_tmax"]:
                st3["viol_tmax"] = r["t"]
                st3["tmax_row"] = {k: r[k] for k in ("M", "t", "kap", "N", "a", "odd")}

    done_k4 = prog["k4"] >= prog["k4_rows_n"]
    done_5p = prog["k5p"] >= prog["k5p_rows_n"]
    done_3d = prog["k3d"] >= prog["k3d_rows_n"]
    prog["done"] = done_k4 and done_5p and done_3d
    json.dump(prog, open(PROG, "w"))
    print(json.dumps({
        "k4_done": f"{prog['k4']}/{prog['k4_rows_n']}",
        "k5p_done": f"{prog['k5p']}/{prog['k5p_rows_n']}",
        "k3d_done": f"{prog['k3d']}/{prog['k3d_rows_n']}",
        "done": prog["done"], "bad": len(prog["bad"]),
        "k4_stats": st, "k5p_stats": st5, "k3d_stats": st3,
        "runtime_s": round(time.time() - t0, 1)}, indent=1))
    if prog["bad"]:
        print("FIRST FAILURES:", json.dumps(prog["bad"][:5], indent=1))


if __name__ == "__main__":
    main()
