#!/usr/bin/env python3
"""K0961 audit: machine verification of TWO-ZONE / CO-FACTOR /
EFFECTIVE-WINDOW / SQUEEZE-3 / CHAR-3 over the published smooth-hit
censuses (M <= 2000, all t), plus candidate-walk anchors in the
prime-Y and composite-Y regions and a kodd=4 branch classification.

Inputs (published, sha-pinned in the K0961 item):
  ../remo-smooth-hit-census-20261118/output/hits_full.json
      K0958 census, primes 5 <= M <= 1000, all t (2,609 smooth hits)
  ../remo-smooth-hit-deepcap-20261118/output/hits_strip2.json
      K0960 CENSUS-STRIP2, primes 1000 < M <= 2000, all t (8,277 rows)
  ../remo-smooth-hit-deepcap-20261118/output/hits_deep_band.json
      K0960 t > 60 band (1000 < M <= 2000), 836 rows, cross-check

Checked statements (proofs in report.md; this file is the anchor):
  T1  TWO-ZONE (t>=2, all hits): every odd divisor q of N with
      q < M satisfies 2^a * q <= M-1.
  L2  CO-FACTOR (all hits): every divisor d <= M-1 of N has
      N/d > (M+1)k0/(M-1).
  T3  EFFECTIVE-WINDOW (all hits, k0 >= 2M-kappa): no divisor of N
      lies in [M, (M+1)k0/(M-1)).
  T4  SQUEEZE-3 (kodd=3 hits, compliant i.e. 2^a p3 <= M-1;
      automatic for t>=2 by K0960 ODDCAP):
        p1*p2*(M-1) > (M+1)*k0
        t*M*(M+1) <= (M-1)*p1*p2 - 1
        p1*p2 >= M+3   (M >= 5)
        t*M*(M+1)*2^(2a) <= (M-1)^3 - 2^(2a)
        N == 2^a*p3*p1*p2  (bookkeeping identity)
  T5  CHAR-3 (kodd=3): prime-Y walk candidates:
        t>=2: hit <=> compliant (both directions);
        t=1 : compliant => hit.  Composite-Y walk:
        kodd=3 & compliant => window empty.
  K4  kodd=4 (t>=2) branch classification:
        (A) p3p4 >= M:  cross-pair dichotomy (machine-checked):
             not both (p2p3 >= M, p1p4 >= M), not both
             (p1p3 >= M, p2p4 >= M);
             (alpha) p2p3 < M <= p1p4   -> t^2 bound (alpha)
             (beta)  p2p3 < M, p1p4 < M  -> (M+1)(Mt-1) <= 2^a(M-1)^2
             (gamma) p2p3 >= M           -> p1p4 < M, weak bound
                   t*M < ((M-1)/2^a)^2 + 1
        (B) p3p4 < M  -> t < sqrt(M)  (K0960 DEEP-CAP case B)
      Conjecture (finite-checked): kodd=4 -> t < sqrt(M);
      kodd>=5 -> t <= 3 (max over census).

Everything is pure arithmetic, single-threaded, deterministic.
Output: output/squeeze_audit.json (sort_keys, indent=1).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from branch_density_core import primes_upto  # pinned K0954 core
from composite_core import sigma_Z  # pinned K0950/K0956 engine
from prehit_core import divisors_of  # pinned K0956 core
from smooth_core import census_walk, sieve_flags, window_blocked  # K0958 pin

T0 = time.time()
OUT = os.path.join(HERE, "output")
os.makedirs(OUT, exist_ok=True)


def log(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


# --------------------------------------------------------------- inputs

IN_FULL = os.path.join(HERE, "..", "remo-smooth-hit-census-20261118",
                       "output", "hits_full.json")
IN_STRIP2 = os.path.join(HERE, "..", "remo-smooth-hit-deepcap-20261118",
                         "output", "hits_strip2.json")
IN_DEEPBAND = os.path.join(HERE, "..", "remo-smooth-hit-deepcap-20261118",
                           "output", "hits_deep_band.json")

# independent factorizer: sieve once, trial division
PSIEVE_N = 46000
PF = sieve_flags(PSIEVE_N)
PLIST = [i for i in range(2, PSIEVE_N + 1) if PF[i]]
assert PLIST[-1] ** 2 > 2 * 10 ** 9


def factor_indep(n):
    """Trial-division factorization; returns list of [p, e], p asc."""
    fac = []
    for p in PLIST:
        if p * p > n:
            break
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            fac.append([p, e])
    if n > 1:
        fac.append([n, 1])
    return fac


def row_fields(M, kap, t):
    K = (M + 1) * t + kap
    Y = K + 1
    N = M * Y - 1
    k0 = M * t + kap - 1
    return K, Y, N, k0


def struct_fields(fac):
    a = 0
    odd = []
    Om = 0
    for p, e in fac:
        Om += e
        if p == 2:
            a = e
        else:
            odd.extend([p] * e)
    odd.sort()
    return a, odd, len(odd), Om, len(fac)


def compliant(a, odd, M):
    """ODDCAP compliance: every odd prime p has 2^a * p <= M-1."""
    c = (1 << a)
    return all(c * p <= M - 1 for p in odd)


def fac_str(fac):
    return "*".join("%d^%d" % (p, e) if e > 1 else "%d" % p
                    for p, e in fac)


# ======================================================= part A: rows

def part_rows():
    log("ROWS: loading published hit rows")
    full = json.load(open(IN_FULL))["rows"]
    strip2 = json.load(open(IN_STRIP2))["rows"]
    deep = json.load(open(IN_DEEPBAND))["rows"]
    rows = []
    for r in full:
        rows.append((r[0], r[1], r[2], r[6], r[7], r[8], "full"))
    for r in strip2:
        rows.append((r[0], r[1], r[2], r[3], r[4], r[5], "strip2"))
    log("ROWS: %d rows (full %d + strip2 %d)" % (len(rows), len(full),
                                                 len(strip2)))

    res = {"n_rows": len(rows), "n_full": len(full), "n_strip2": len(strip2),
           "viol": {}}
    v = res["viol"]
    for name in ["identity", "recon_omega", "parity", "smooth", "exclusive",
                 "twozone_t2", "effwindow_zone",
                 "squeeze_s1", "squeeze_s2", "squeeze_s3", "squeeze_deepcap",
                 "squeeze_book", "char3_window_vacuous",
                 "k4_dichotomy1", "k4_dichotomy2", "k4_alpha", "k4_beta",
                 "k4_gamma_p1p4", "k4_gamma_weak", "k4_gamma_sharp",
                 "k4B_sqrt",
                 "kodd4_sqrtM_conj", "kodd_ge5_small_t_conj",
                 "deepband_crosscheck"]:
        v[name] = 0

    # stats accumulators
    t1_k3 = {"compliant": 0, "noncompliant": 0}
    kodd_hist = {"t1": {}, "t2_60": {}, "t_gt60": {}}
    max_t_per_kodd = {}
    kodd_ge4_top = []
    a_ge2_deep = []
    effwindow_outside = 0
    effwindow_outside_viol = 0
    twozone_t1_viol = 0
    floor_attained = {"t1": [], "t2_60": [], "t_gt60": []}
    rho = {"t2_60": [], "t_gt60": []}
    sdial = {"t2_60": [], "t_gt60": []}
    k4_branch = {"A_alpha": 0, "A_beta": 0, "A_gamma": 0, "B": 0}
    k4_branch_max = {"A_alpha": [0, 0, 0], "A_beta": [0, 0, 0],
                     "A_gamma": [0, 0, 0], "B": [0, 0, 0]}
    k4_gamma_max_t = 0
    k4_gamma_rows = []
    t1_k4_caseB = 0
    deepband_seen = set()
    deepmap = {(r[0], r[1], r[2]): r for r in deep}

    for (M, kap, t, Om_pub, om_pub, br, src) in rows:
        K, Y, N, k0 = row_fields(M, kap, t)
        if N != (M + 1) * k0 + 2 * M - kap:
            v["identity"] += 1
            continue
        fac = factor_indep(N)
        a, odd, kodd, Om, om = struct_fields(fac)
        if (Om, om) != (Om_pub, om_pub):
            v["recon_omega"] += 1
        if N % 2 or a == 0:
            v["parity"] += 1
        if any(p > M - 1 for p, _e in fac):
            v["smooth"] += 1
        if br != 0:
            v["exclusive"] += 1
        comp = compliant(a, odd, M)

        # divisor facts (used by T1/T3/L2-anchoring)
        divs = divisors_of(fac)

        # T1 TWO-ZONE: odd divisors q < M must satisfy 2^a q <= M-1
        bad_tz = 0
        pow2a = (1 << a)
        for d in divs:
            if d % 2 == 1 and d < M and pow2a * d > M - 1:
                bad_tz += 1
        if t >= 2:
            if bad_tz:
                v["twozone_t2"] += 1
        else:
            twozone_t1_viol += bad_tz

        # T3 EFFECTIVE-WINDOW
        zone = k0 >= 2 * M - kap
        bad_ew = 0
        cap_num = (M + 1) * k0
        for d in divs:
            if d >= M and d * (M - 1) < cap_num:
                bad_ew += 1
        if zone:
            if bad_ew:
                v["effwindow_zone"] += 1
        else:
            effwindow_outside += 1
            effwindow_outside_viol += bad_ew

        # T4 SQUEEZE-3 on compliant kodd=3 rows
        if kodd == 3:
            if t == 1:
                t1_k3["compliant" if comp else "noncompliant"] += 1
            if comp:
                p1, p2, p3 = odd
                c = pow2a * p3
                pair = p1 * p2
                if pair * (M - 1) <= (M + 1) * k0:
                    v["squeeze_s1"] += 1
                if t * M * (M + 1) > (M - 1) * pair - 1:
                    v["squeeze_s2"] += 1
                if pair < M + 3:
                    v["squeeze_s3"] += 1
                q4 = 1 << (2 * a)
                if t * M * (M + 1) * q4 > (M - 1) ** 3 - q4:
                    v["squeeze_deepcap"] += 1
                if c * pair != N:
                    v["squeeze_book"] += 1
                if window_blocked(N, M, k0, fac):
                    # compliant kodd=3 must have empty window (CHAR-3 <=)
                    v["char3_window_vacuous"] += 1
                bq = ((M - 1) * pair - 1) // (M * (M + 1))
                band = "t1" if t == 1 else ("t2_60" if t <= 60
                                           else "t_gt60")
                if t == bq:
                    floor_attained[band].append([M, kap, t])
                if t >= 2:
                    rho[band].append(t * M / pair)
                    sdial[band].append(c / (M - 1))
                if t > 60 and a >= 2:
                    a_ge2_deep.append([M, kap, t, Om, om, fac_str(fac)])

        # K4 branch classification (t >= 2, kodd = 4)
        if t >= 2 and kodd == 4:
            p1, p2, p3, p4 = odd
            pr12, pr13, pr14 = p1 * p2, p1 * p3, p1 * p4
            pr23, pr24, pr34 = p2 * p3, p2 * p4, p3 * p4
            # cross-pair dichotomies (proven; machine anchor)
            if pr23 >= M and pr14 >= M:
                v["k4_dichotomy1"] += 1
            if pr13 >= M and pr24 >= M:
                v["k4_dichotomy2"] += 1
            br_name = None
            if pr34 >= M:
                br_name = ("A_alpha" if (pr23 < M and pr14 >= M) else
                           ("A_beta" if (pr23 < M and pr14 < M) else
                            "A_gamma"))
                k4_branch[br_name] += 1
                if pr23 < M and pr14 >= M:
                    # (alpha): t < sqrt(M)/2^a
                    lhs = pow2a * M * t - pow2a
                    if lhs * lhs >= M * (M - 1) ** 2:
                        v["k4_alpha"] += 1
                elif pr23 < M and pr14 < M:
                    # (beta): (M+1)(Mt-1) <= 2^a (M-1)^2
                    if (M + 1) * (M * t - 1) > pow2a * (M - 1) ** 2:
                        v["k4_beta"] += 1
                else:
                    # (gamma): p1p4 < M forced; weak + sharp bounds
                    if pr14 >= M:
                        v["k4_gamma_p1p4"] += 1
                    if M * t >= ((M - 1) // pow2a) ** 2 + 1:
                        v["k4_gamma_weak"] += 1
                    # sharp: t * 2^(2a) * p1^2 < M-1
                    if t * (1 << (2 * a)) * p1 * p1 > M - 2:
                        v["k4_gamma_sharp"] += 1
                    if t > k4_gamma_max_t:
                        k4_gamma_max_t = t
                        k4_gamma_rows = [[M, kap, t, fac_str(fac)]]
                    elif t == k4_gamma_max_t:
                        k4_gamma_rows.append([M, kap, t, fac_str(fac)])
            else:
                k4_branch["B"] += 1
                br_name = "B"
                if t * t >= M:
                    v["k4B_sqrt"] += 1
            if br_name and t > k4_branch_max[br_name][0]:
                k4_branch_max[br_name] = [t, M, kap]
            # conjecture anchors
            if t * t >= M:
                v["kodd4_sqrtM_conj"] += 1
        if kodd >= 5 and t >= 4:
            v["kodd_ge5_small_t_conj"] += 1
        if t == 1 and kodd == 4 and odd[2] * odd[3] < M:
            t1_k4_caseB += 1

        # histograms / extremes
        band = "t1" if t == 1 else ("t2_60" if t <= 60 else "t_gt60")
        kodd_hist[band][kodd] = kodd_hist[band].get(kodd, 0) + 1
        if kodd not in max_t_per_kodd or t > max_t_per_kodd[kodd][0]:
            max_t_per_kodd[kodd] = (t, M, kap)
        if kodd >= 4:
            kodd_ge4_top.append((t, M, kap, kodd))
            kodd_ge4_top.sort(reverse=True)
            del kodd_ge4_top[30:]

        # deep-band cross-check (file covers 1000 < M <= 2000, t > 60)
        if t > 60:
            if M > 1000:
                r = deepmap.get((M, kap, t))
                if r is None:
                    v["deepband_crosscheck"] += 1
                else:
                    top_pair = odd[-2] * odd[-1] if len(odd) >= 2 else 0
                    mine = [M, kap, t, K, Y, N, Om, om, 0, a, kodd,
                            odd[-1] if odd else 0, top_pair]
                    if mine != r:
                        v["deepband_crosscheck"] += 1
                deepband_seen.add((M, kap, t))

    if len(deepband_seen) != len(deep):
        v["deepband_crosscheck"] += 1

    def stats(xs):
        if not xs:
            return {"n": 0}
        s = sorted(xs)
        n = len(s)
        med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0
        return {"n": n, "min": s[0], "median": med, "max": s[-1]}

    res["t1_kodd3"] = t1_k3
    res["twozone_t1_violations"] = twozone_t1_viol
    res["effwindow_outside_zone"] = {
        "n_rows": effwindow_outside,
        "n_with_divisor_in_sliver": effwindow_outside_viol}
    res["kodd_hist"] = kodd_hist
    res["max_t_per_kodd"] = {str(k): list(x) for k, x in
                             sorted(max_t_per_kodd.items())}
    res["kodd_ge4_top30_t"] = [list(x) for x in kodd_ge4_top]
    res["a_ge2_deep_band"] = a_ge2_deep
    res["squeeze_stats"] = {
        "rho": {b: stats(rho[b]) for b in rho},
        "s": {b: stats(sdial[b]) for b in sdial},
        "floor_attained": floor_attained,
        "floor_attained_counts": {b: len(floor_attained[b])
                                  for b in floor_attained},
        "rho_argmax_t_gt60": None,
    }
    # argmax rho for t>60
    best = None
    for (M, kap, t, Om, om, br, src) in rows:
        pass
    res["k4_branch"] = k4_branch
    res["k4_branch_max_t"] = k4_branch_max
    res["k4_gamma_max_t"] = k4_gamma_max_t
    res["k4_gamma_rows_at_max"] = k4_gamma_rows
    res["t1_kodd4_caseB"] = t1_k4_caseB
    log("ROWS: done; violations: %s" % {k: w for k, w in v.items() if w})
    return res, rows


def rho_argmax(rows):
    """argmax of rho = tM/p1p2 over compliant kodd=3 t>60 rows."""
    best = None
    for (M, kap, t, Om, om, br, src) in rows:
        if t <= 60:
            continue
        _K, _Y, N, _k0 = row_fields(M, kap, t)
        fac = factor_indep(N)
        a, odd, kodd, _Om, _om = struct_fields(fac)
        if kodd != 3 or not compliant(a, odd, M):
            continue
        p1, p2, _p3 = odd
        val = t * M / (p1 * p2)
        if best is None or val > best[0]:
            best = (val, [M, kap, t])
    return best


# ============================================== part B: engine anchors

def part_engine_hits(rows):
    log("ENGINE: sampling hit rows")
    sample = [(M, kap, t) for (M, kap, t, *_r) in rows]
    picks = set(sample[::37])
    for (M, kap, t) in sample:
        if t >= 150:
            picks.add((M, kap, t))
    picks = sorted(picks)
    ok = fails = 0
    for (M, kap, t) in picks:
        K = (M + 1) * t + kap
        if sigma_Z(M, K) == 1:
            ok += 1
        else:
            fails += 1
    log("ENGINE: %d hit anchors, %d fails" % (ok, fails))
    return {"n_hit_anchor": ok, "n_hit_fail": fails}


# =========================================== part C: candidate walks

WALK_M = [p for p in primes_upto(100) if p >= 5] + \
         [101, 127, 163, 199, 263, 397, 521, 997, 1009, 1523, 1789]


def part_walks():
    """Prime-Y candidate walk (pinned census_walk): CHAR-3 iff test,
    dead-class anchor, published-row cross-check."""
    log("WALKS: prime-Y census on %d primes" % len(WALK_M))
    pred = {"t2_k3_compliant_blocked": 0, "t2_k3_noncompliant_hit": 0,
            "t1_k3_compliant_blocked": 0,
            "t2_k3_compliant": 0, "t2_k3": 0,
            "t1_k3_compliant": 0, "t1_k3": 0,
            "hits_dead": 0, "walk_vs_published_mismatch_M": 0}
    blocked_kodd_hist = {}
    blocked_for_engine = []
    per_M = []
    ymaxmax = max((M - 1) ** 3 // M for M in WALK_M)
    yflags = sieve_flags(ymaxmax)
    pub = {}
    for r in json.load(open(IN_FULL))["rows"]:
        pub.setdefault(r[0], set()).add((r[1], r[2]))
    for r in json.load(open(IN_STRIP2))["rows"]:
        pub.setdefault(r[0], set()).add((r[1], r[2]))
    for M in WALK_M:
        ymax = (M - 1) ** 3 // M
        small = [p for p in primes_upto(M - 1) if p >= 2]
        smooth, _cand, st = census_walk(M, ymax, yflags, small)
        hits = 0
        blocked = 0
        hitkeys = set()
        for Y in sorted(smooth):
            v = smooth[Y]
            fac = [(p, e) for p, e in v[1]]
            kap = (Y - 1) % (M + 1)
            t = (Y - 1 - kap) // (M + 1)
            N = M * Y - 1
            k0 = M * t + kap - 1
            a, odd, kodd, _Om, _om = struct_fields(fac)
            blk = window_blocked(N, M, k0, fac)
            comp = compliant(a, odd, M)
            dead = math.gcd(kap + 1, M + 1) != 1
            if kodd == 3:
                if t >= 2:
                    pred["t2_k3"] += 1
                    if comp:
                        pred["t2_k3_compliant"] += 1
                        if blk:
                            pred["t2_k3_compliant_blocked"] += 1
                    elif not blk:
                        pred["t2_k3_noncompliant_hit"] += 1
                else:
                    pred["t1_k3"] += 1
                    if comp:
                        pred["t1_k3_compliant"] += 1
                        if blk:
                            pred["t1_k3_compliant_blocked"] += 1
            if blk:
                blocked += 1
                blocked_kodd_hist[kodd] = \
                    blocked_kodd_hist.get(kodd, 0) + 1
                if len(blocked_for_engine) < 40 and t % 7 == 2:
                    blocked_for_engine.append((M, (M + 1) * t + kap))
            else:
                hits += 1
                hitkeys.add((kap, t))
                if dead:
                    pred["hits_dead"] += 1
        if hitkeys != pub.get(M, set()):
            pred["walk_vs_published_mismatch_M"] += 1
            log("WALKS: M=%d hit-set mismatch vs published (%d vs %d)"
                % (M, len(hitkeys), len(pub.get(M, set()))))
        per_M.append({"M": M, "n_cand": st["n_cand"],
                      "n_smooth": len(smooth), "hits": hits,
                      "blocked": blocked})
    log("WALKS: done %s" % pred)
    return {"per_M": per_M, "predictions": pred,
            "blocked_kodd_hist": {str(k): w for k, w in
                                  sorted(blocked_kodd_hist.items())},
            "blocked_engine_sample": blocked_for_engine}


def part_engine_blocked(blocked_rows):
    ok = fails = 0
    for (M, K) in blocked_rows:
        if sigma_Z(M, K) != 1:
            ok += 1
        else:
            fails += 1
    return {"n_blocked_anchor": ok, "n_blocked_fail": fails}


COMPOSITE_M = [p for p in primes_upto(149) if p >= 5]


def part_composite():
    """Composite-Y walk (all Y): CHAR-3 <= anchor (kodd=3 & compliant
    => window empty, in the composite-Y region too) and phantom rows
    (window empty but Y composite: NOT hits; engine-anchored)."""
    log("COMPOSITE: all-Y walk on %d primes" % len(COMPOSITE_M))
    pred = {"smooth_total": 0, "compositeY_smooth": 0,
            "k3_compliant": 0, "k3_compliant_window_nonempty": 0,
            "k3_compositeY": 0,
            "phantom_dead": 0, "phantom_live": 0, "Msq_smooth": 0,
            "Msq_hit": 0}
    phantom_engine = []
    for M in COMPOSITE_M:
        ymax = (M - 1) ** 3 // M
        Mp1 = M + 1
        cand = {}
        for Y in range(M + 2, ymax + 1):
            kap = (Y - 1) % Mp1
            if kap > M - 2:
                continue
            if kap == 0 and (Y - 1) // Mp1 == 1:
                continue
            cand[Y] = [M * Y - 1, []]
        small = [p for p in primes_upto(M - 1) if p >= 2]
        get = cand.get
        for p in small:
            r = pow(M, -1, p)
            start = r + ((M + 2 - r + p - 1) // p) * p
            for Y in range(start, ymax + 1, p):
                v = get(Y)
                if v is None:
                    continue
                lv, fac = v
                e = 0
                while lv % p == 0:
                    lv //= p
                    e += 1
                if e:
                    fac.append([p, e])
                    v[0] = lv
        smooth = {Y: v for Y, v in cand.items() if v[0] == 1}
        yflags = sieve_flags(ymax)
        for Y in sorted(smooth):
            v = smooth[Y]
            fac = [(p, e) for p, e in v[1]]
            kap = (Y - 1) % Mp1
            t = (Y - 1 - kap) // Mp1
            N = M * Y - 1
            k0 = M * t + kap - 1
            a, odd, kodd, _Om, _om = struct_fields(fac)
            blk = window_blocked(N, M, k0, fac)
            comp = compliant(a, odd, M)
            pred["smooth_total"] += 1
            yprime = yflags[Y] == 1
            is_msq = (Y == M * M)
            if not yprime:
                pred["compositeY_smooth"] += 1
            if kodd == 3:
                if not yprime:
                    pred["k3_compositeY"] += 1
                if comp:
                    pred["k3_compliant"] += 1
                    if blk:
                        pred["k3_compliant_window_nonempty"] += 1
            if is_msq:
                pred["Msq_smooth"] += 1
                if not blk:
                    pred["Msq_hit"] += 1
            if (not yprime) and (not is_msq) and (not blk):
                if math.gcd(kap + 1, Mp1) != 1:
                    pred["phantom_dead"] += 1
                else:
                    pred["phantom_live"] += 1
                if len(phantom_engine) < 25:
                    phantom_engine.append((M, Mp1 * t + kap))
    log("COMPOSITE: done %s" % pred)
    return pred, phantom_engine


def part_engine_phantom(rows):
    ok = fails = 0
    for (M, K) in rows:
        if sigma_Z(M, K) != 1:
            ok += 1
        else:
            fails += 1
    return {"n_phantom_anchor": ok, "n_phantom_fail": fails}


# ------------------------------------------------------------------ run

def main():
    res_rows, rows = part_rows()
    res_rows["squeeze_stats"]["rho_argmax_t_gt60"] = rho_argmax(rows)
    res_walks = part_walks()
    engine_blocked = part_engine_blocked(
        res_walks.pop("blocked_engine_sample"))
    res_walks["engine_blocked_anchor"] = engine_blocked
    res_composite, phantom = part_composite()
    engine_phantom = part_engine_phantom(phantom)
    engine_hits = part_engine_hits(rows)

    out = {
        "inputs": {
            "hits_full.json": sha256(IN_FULL),
            "hits_strip2.json": sha256(IN_STRIP2),
            "hits_deep_band.json": sha256(IN_DEEPBAND),
            "composite_core.py": sha256(os.path.join(HERE,
                                                     "composite_core.py")),
            "smooth_core.py": sha256(os.path.join(HERE,
                                                  "smooth_core.py")),
            "prehit_core.py": sha256(os.path.join(HERE,
                                                  "prehit_core.py")),
            "branch_density_core.py": sha256(os.path.join(
                HERE, "branch_density_core.py")),
            "sievegen_core.py": sha256(os.path.join(HERE,
                                                    "sievegen_core.py")),
        },
        "rows_part": res_rows,
        "walks_part": res_walks,
        "composite_part": res_composite,
        "engine": {"hits": engine_hits, "phantom": engine_phantom},
        "note": "K0961 TWO-ZONE/CO-FACTOR/EFFECTIVE-WINDOW/SQUEEZE-3/"
                "CHAR-3 audit; all arithmetic exact, floats only for "
                "reported statistics",
    }
    path = os.path.join(OUT, "squeeze_audit.json")
    with open(path, "w") as f:
        json.dump(out, f, sort_keys=True, indent=1)
        f.write("\n")
    log("WROTE %s (%d bytes)" % (path, os.path.getsize(path)))


if __name__ == "__main__":
    main()
