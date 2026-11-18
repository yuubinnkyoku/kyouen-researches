#!/usr/bin/env python3
"""K0960 driver: complete the smooth-hit census for primes
1000 < M <= 2000 over ALL t (closing the t > 60 gap of K0958's
CENSUS-STRIP), with checkpointed per-M progress.

Semantics are identical to smooth_core.census_walk (same candidate
set: prime Y in [M+2, ymax], kappa = (Y-1) mod (M+1) in [0, M-2],
(t,kappa) != (1,0); same sieve-walk; same n_cand/n_steps/dead_cand
counting).  The only change is that candidates are enumerated from a
precomputed prime list instead of scanning every Y (pure speed).

ymax = (M-1)^3 // M   (complete over all t, census completeness as in
K0958 report Sec. 5).

Checkpoint protocol: for each M the driver appends one JSON line
per_M/<M>.json into the checkpoint dir before returning; on restart,
M's whose checkpoint exists are skipped.  Everything deterministic.
"""
from __future__ import annotations

import bisect
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from branch_density_core import primes_upto  # pinned K0954 core
from composite_core import sigma_Z  # pinned engine
from prehit_core import factorize, divisors_of, dstar, branch_divisor
from smooth_core import sieve_flags, window_blocked

T0 = time.time()
CKPT = os.path.join(HERE, "ckpt")
os.makedirs(CKPT, exist_ok=True)


def log(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)


# ---------------------------------------------------------------- setup

PRIMES = primes_upto(2000)
YMAX_GLOBAL = (1999 - 1) ** 3 // 1999  # largest ymax over the range
log("global ymax = %d; sieving flags..." % YMAX_GLOBAL)
YFLAGS = sieve_flags(YMAX_GLOBAL)
ALL_PRIMES = [i for i in range(2, YMAX_GLOBAL + 1) if YFLAGS[i]]
log("prime list up to %d: %d primes" % (YMAX_GLOBAL, len(ALL_PRIMES)))
PLIST_BIG = primes_upto(32000)  # hits are (M-1)-smooth; M-1 <= 1999


# --------------------------------------------------- optimized walk


def census_walk2(M, ymax, small):
    Mp1 = M + 1
    cand = {}
    n_cand = 0
    lo = bisect.bisect_left(ALL_PRIMES, M + 2)
    hi = bisect.bisect_right(ALL_PRIMES, ymax)
    for Y in ALL_PRIMES[lo:hi]:
        kap = (Y - 1) % Mp1
        if kap > M - 2:
            continue
        if kap == 0 and (Y - 1) // Mp1 == 1:
            continue  # special state (t,kappa) = (1,0)
        cand[Y] = [M * Y - 1, []]
        n_cand += 1
    dead = 0
    get = cand.get
    for Y in cand:
        kap = (Y - 1) % Mp1
        if math.gcd(kap + 1, Mp1) != 1:
            dead += 1
    n_steps = 0
    for p in small:
        r = pow(M, -1, p)
        start = r + ((M + 2 - r + p - 1) // p) * p
        for Y in range(start, ymax + 1, p):
            v = get(Y)
            if v is None:
                continue
            n_steps += 1
            lv, fac = v
            e = 0
            while lv % p == 0:
                lv //= p
                e += 1
            if e:
                fac.append([p, e])
                v[0] = lv
    smooth = {Y: v for Y, v in cand.items() if v[0] == 1}
    stats = {"n_cand": n_cand, "n_steps": n_steps, "dead_cand": dead}
    return smooth, cand, stats


def classify(M, smooth):
    """Same rows as smooth_core.classify_candidates + deep-cap fields."""
    Mp1 = M + 1
    hits = []
    blocked = 0
    s3_viol = 0
    max_t = 0
    max_N = 0
    Om_h = {}
    om_h = {}
    for Y in sorted(smooth):
        v = smooth[Y]
        fac = [(p, e) for (p, e) in v[1]]
        kap = (Y - 1) % Mp1
        t = (Y - 1 - kap) // Mp1
        K = Mp1 * t + kap
        N = M * Y - 1
        k0 = M * t + kap - 1
        Om = sum(e for (_p, e) in fac)
        blk = window_blocked(N, M, k0, fac)
        if blk:
            blocked += 1
            if Om <= 3:
                s3_viol += 1
            continue
        # hit: deep-cap structure fields
        a = 0
        if fac and fac[0][0] == 2:
            a = fac[0][1]
        odd = fac[1:] if a else fac
        k_odd = sum(e for (_p, e) in odd)
        odd_sorted = sorted([p for (p, e) in odd for _ in range(e)])
        top_pair = odd_sorted[-2] * odd_sorted[-1] if k_odd >= 2 else 0
        max_odd = odd_sorted[-1] if odd_sorted else 0
        row = [M, kap, t, K, Y, N, Om, len(fac),
               0,  # is_branch_and_smooth (filled below; 0 = smooth-only)
               a, k_odd, max_odd, top_pair]
        # branch type via K0956 helpers
        C = math.gcd(Mp1, kap + 2)
        divs = divisors_of(fac)
        d = branch_divisor(N, M, C, divs)
        row[8] = 1 if d else 0
        hits.append(row)
        Om_h[Om] = Om_h.get(Om, 0) + 1
        om_h[len(fac)] = om_h.get(len(fac), 0) + 1
        if t > max_t:
            max_t = t
        if N > max_N:
            max_N = N
    return hits, blocked, s3_viol, max_t, max_N, Om_h, om_h


# ---------------------------------------------------------------- run

strip2_M = [p for p in PRIMES if 1000 < p <= 2000]


def run_one(M):
    """Census + classify for one prime M; writes ckpt/<M>.json."""
    ymax = (M - 1) ** 3 // M
    small = [p for p in PRIMES if p <= M - 1]
    smooth, _cand, st = census_walk2(M, ymax, small)
    hits, blocked, s3_viol, max_t, max_N, Om_h, om_h = classify(M, smooth)
    rec = {
        "M": M, "ymax": ymax,
        "n_cand": st["n_cand"], "n_steps": st["n_steps"],
        "dead_cand": st["dead_cand"], "n_smooth": len(smooth),
        "n_blocked": blocked, "s3_violations": s3_viol,
        "n_hits": len(hits), "max_t_hit": max_t, "max_N_hit": max_N,
        "Omega_hist_hits": Om_h, "omega_hist_hits": om_h,
        "hits": hits,
    }
    tmp = os.path.join(CKPT, "%d.tmp" % M)
    with open(tmp, "w") as f:
        json.dump(rec, f, sort_keys=True, separators=(",", ":"))
    os.replace(tmp, os.path.join(CKPT, "%d.json" % M))
    log("M=%d ymax=%d cand=%d smooth=%d hits=%d blocked=%d "
        "maxt=%d s3v=%d dead=%d"
        % (M, ymax, st["n_cand"], len(smooth), len(hits), blocked,
           max_t, s3_viol, st["dead_cand"]))


if __name__ == "__main__":
    todo = [M for M in strip2_M
            if not os.path.exists(os.path.join(CKPT, "%d.json" % M))]
    log("M range: %d primes, todo: %d" % (len(strip2_M), len(todo)))

    BUDGET = float(os.environ.get("CENSUS_BUDGET", "240"))
    for M in todo:
        if time.time() - T0 > BUDGET:
            log("budget reached; stopping cleanly (resume by rerun)")
            break
        run_one(M)

    done = sorted(int(f.split(".")[0]) for f in os.listdir(CKPT)
                  if f.endswith(".json"))
    log("checkpoints complete: %d/%d" % (len(done), len(strip2_M)))
    if len(done) == len(strip2_M):
        log("ALL DONE")
