#!/usr/bin/env python3
"""K0963 sweep part 2: complete kodd=5 band search for 2000 < M <= MMAX.

For every prime M in (2000, MMAX] this sweeps the COMPLETE candidate
band for kodd=5 hits with t >= 4:

    t in [4, T5(M)],  T5(M) = max(t52, t27)  (a=1 worst case),
    t52 = (isqrt((M-1)^5 // (8(M+1)^2)) + 1) // M     (CAP-52),
    t27 = ((M-1)^3 // (108 (M+1)) + 1) // M           (CAP-27).

By the K0963 caps, a kodd=5 smooth hit with t > T5(M) is impossible, so
the band [4, T5] is complete for kodd=5.  Candidates are prime Y in
[(M+1)*4+1, (M+1)*T5+M-1] (plus Y = M^2), the HIT-ARITH census classes
(K0950/K0958: every smooth hit of prime M has Y prime or Y = M^2).

Method: sieve-walk.  For each small prime p <= M-1, walk the AP
Y = M^{-1} mod p inside the band and divide p-powers out of the
cofactor N = M*Y-1.  Cofactor 1 at the end  <=>  (M-1)-smooth.

Completeness claim produced (if no kodd=5 hit found):
    no kodd=5 smooth hit with t >= 4 exists for M <= MMAX.
kodd >= 6 rows found in band are recorded as evidence only (the
r >= 6 caps are proven only for cases PS / LG-PF, LG-OPEN is open).

Checkpointed: state in output/sweep_state.json, budget in seconds,
re-run to continue.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

sys.path.insert(0, ".")
from kodd5_core import (Regime, primes_upto, is_prime, divisors, band_tmax,
                        k5_config, cap_check)

STATE = "output/sweep_state.json"


def sieve_flags(n: int) -> bytearray:
    b = bytearray(b"\x01") * (n + 1)
    b[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n) + 1):
        if b[p]:
            b[p * p:n + 1:p] = b"\x00" * (((n - p * p) // p) + 1)
    return b


def band(M: int):
    T = band_tmax(M)
    ylo = (M + 1) * 4 + 1
    yhi = (M + 1) * T + M - 1
    return T, ylo, yhi


def sweep_M(M: int, prime_flags: bytearray, small_primes: list[int]) -> dict:
    T, ylo, yhi = band(M)
    co = {}
    for Y in range(ylo, yhi + 1):
        if prime_flags[Y]:
            co[Y] = M * Y - 1
    # small-prime AP walk
    for p in small_primes:
        if p > M - 1:
            break
        minv = pow(M, -1, p)
        y0 = ylo + ((minv - ylo) % p)
        for Y in range(y0, yhi + 1, p):
            c = co.get(Y)
            if c is not None:
                while c % p == 0:
                    c //= p
                co[Y] = c
    out = {"M": M, "T": T, "n_cand": len(co), "smooth": 0,
           "hits": [], "blocked": 0, "ysqr": None}
    for Y, c in co.items():
        if c != 1:
            continue
        out["smooth"] += 1
        kap = (Y - 1) % (M + 1)
        if kap > M - 2:
            continue
        t = (Y - 1 - kap) // (M + 1)
        reg = Regime(M, kap, t)
        facs, left = reg.factor(small_primes)
        if left != 1:
            continue  # cannot happen (cofactor check already)
        divs = divisors(facs)
        odd = sorted(p for p, e in facs if p > 2 for _ in range(e))
        kd = len(odd)
        row = {"M": M, "kap": kap, "t": t, "Y": Y, "N": reg.N,
               "a": reg.a, "kodd": kd, "odd": odd}
        if all(not (reg.M <= d <= reg.k0) for d in divs):
            if kd == 5:
                cfg = k5_config(reg, odd)
                row["config"] = cfg["config"]
                row["route"] = cfg["route"]
                row["cap"] = cap_check(reg, cfg["route"])["holds"]
            out["hits"].append(row)
        else:
            out["blocked"] += 1
    # Y = M^2 candidate (t = M-1): only relevant if within band
    if 4 <= M - 1 <= T:
        reg = Regime(M, 0, M - 1)  # Y = (M+1)(M-1)+1 = M^2
        assert reg.Y == M * M
        facs, left = reg.factor(small_primes)
        if left == 1:
            divs = divisors(facs)
            odd = sorted(p for p, e in facs if p > 2 for _ in range(e))
            if all(not (reg.M <= d <= reg.k0) for d in divs):
                out["ysqr"] = {"M": M, "t": M - 1, "N": reg.N,
                               "kodd": len(odd), "odd": odd}
    return out


def main():
    mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 240.0
    t0 = time.time()

    if os.path.exists(STATE):
        st = json.load(open(STATE))
    else:
        Ms = [p for p in primes_upto(mmax) if p > 2000]
        st = {"mmax": mmax, "Ms": Ms, "next": 0, "results": [],
              "n_hits": 0, "n_k5": 0, "n_k6plus": 0}
    if st["mmax"] != mmax:
        Ms = [p for p in primes_upto(mmax) if p > 2000]
        done = {r["M"] for r in st["results"]}
        st["mmax"] = mmax
        st["Ms"] = [M for M in Ms if M not in done]
        st["next"] = 0

    # global prime sieve up to max Yhi
    ymax = 0
    for M in st["Ms"]:
        T, _, yhi = band(M)
        ymax = max(ymax, yhi)
    ymax = max(ymax, (mmax + 1) * band_tmax(mmax) + mmax)
    prime_flags = sieve_flags(ymax)
    small_primes = primes_upto(mmax)

    while st["next"] < len(st["Ms"]) and time.time() - t0 < budget:
        M = st["Ms"][st["next"]]
        r = sweep_M(M, prime_flags, small_primes)
        st["results"].append(r)
        st["n_hits"] += len(r["hits"])
        st["n_k5"] += sum(1 for h in r["hits"] if h["kodd"] == 5)
        st["n_k6plus"] += sum(1 for h in r["hits"] if h["kodd"] >= 6)
        st["next"] += 1
        if r["hits"]:
            print("M=%d T=%d hits=%s" % (M, r["T"], json.dumps(r["hits"])),
                  flush=True)
        # checkpoint every M
        tmp = STATE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(st, f)
        os.replace(tmp, STATE)

    left = len(st["Ms"]) - st["next"]
    print(json.dumps({
        "mmax": st["mmax"], "done": st["next"], "left": left,
        "n_hits": st["n_hits"], "n_k5": st["n_k5"],
        "n_k6plus": st["n_k6plus"],
        "runtime_s": round(time.time() - t0, 1)}, indent=1))
    if left == 0:
        # final: collect all kodd>=5 rows and per-kodd max t
        rows = [h for r in st["results"] for h in r["hits"]]
        kd_hist = {}
        tmax = {}
        for h in rows:
            kd_hist[h["kodd"]] = kd_hist.get(h["kodd"], 0) + 1
            tmax[h["kodd"]] = max(tmax.get(h["kodd"], 0), h["t"])
        ysqr = [r["ysqr"] for r in st["results"] if r["ysqr"]]
        print("COMPLETE mmax=%d: rows=%d kd_hist=%s tmax=%s ysqr=%s"
              % (st["mmax"], len(rows), kd_hist, tmax, json.dumps(ysqr)))


if __name__ == "__main__":
    main()
