#!/usr/bin/env python3
"""K0956 audit builder: the pre-tail mechanism of sigma_Z value-one hits.

Single deterministic run; writes audit.json, firsthit_rows.json and
firsthit_agg.json into the experiment directory.  All checks are
finite exhaustive enumerations or pinned-input recomputations; nothing
is claimed beyond what report.md proves or the JSON records.

Checks:
  PIN              sha256 of every pinned input and of prehit_core.py
  ENGINE-ANCHOR    engine value-one vs raw window predicate (small grid)
  GAP-GRID-A/B     engine vs HIT-GAP over wide (M, kappa, t) grids,
                   split by the k0 >= sqrt(N) regime
  SPLIT-GRID       every pre-tail hit (M <= 199 prime, live class,
                   2 <= t <= M-2) is BRANCH or satisfies the SMOOTH
                   bound N <= (M-1)^3 and (M-1)-smoothness
  FIRSTHIT         per-class first hits for primes M <= 2000;
                   0 mismatches vs tier3 (M <= 199) and firsthit_pred
  FIRSTHIT-PRED    corrected from-start BH prediction t* of first hits
                   (K0954 tail-only t_hat gave Spearman 0.095)
  RATE-PROFILE     per-t hit census for 6 profile M values
  SMOOTH-LAW       smooth-only hits: census + (M-1)^3 boundary check
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import prehit_core as pc
from branch_density_core import Branches, primes_upto, is_prime
from composite_core import sigma_Z

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)

PRIMES_SMALL = [p for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
                            41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
                            89, 97] if is_prime(p)]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def primes_between(lo, hi):
    return [p for p in primes_upto(hi) if p >= lo]


def spearman(xs, ys):
    """Rank correlation with average ranks for ties."""
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx)
                    * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


T0 = time.time()


def elog(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)


# =====================================================================
# PIN
# =====================================================================
elog("PIN")
pin = {}
for f in ["composite_core.py", "sievegen_core.py", "branch_density_core.py",
          "hitpair_core.py", "firsthit_pred.json", "pkill_tight_tier3.json",
          "prehit_core.py"]:
    pin[f] = sha256_file(f)

# =====================================================================
# shared sieves
# =====================================================================
M_MAX_FIRSTHIT = 2000
elog("sieves")
plist = primes_upto(46341)          # covers sqrt(N) for N <= 2^31
ycap = (M_MAX_FIRSTHIT + 1) * (7 * math.ceil(math.log(M_MAX_FIRSTHIT + 1) ** 2)
                               + 100) + M_MAX_FIRSTHIT + 2
yflags = pc.sieve_flags(int(ycap))
elog("ycap=%d" % ycap)

# =====================================================================
# ENGINE-ANCHOR + GAP-GRID-A/B: engine vs predicates
# =====================================================================
def grid_engine(Mlist, t_lo, t_hi, label):
    n_states = n_regime = n_hit = 0
    mism_gap = mism_raw = mism_regime = 0
    nonregime_states = []
    t0 = time.time()
    for M in Mlist:
        for kappa in range(0, M - 1):
            for t in range(t_lo, t_hi + 1):
                if (t, kappa) == (1, 0):
                    continue
                K = (M + 1) * t + kappa
                eng = (sigma_Z(M, K) == 1)
                Y = K + 1
                N = M * Y - 1
                k0 = M * t + kappa - 1
                y_ok = (Y == M * M) or (Y <= ycap and yflags[Y]) \
                    or (Y > ycap and is_prime(Y))
                fac = pc.factorize(N, plist) if y_ok else []
                divs = pc.divisors_of(fac)
                raw = y_ok and pc.window_empty(N, M, k0, divs)
                gap = pc.hit_gap_pred(M, kappa, t, N, divs, y_ok)
                n_states += 1
                if raw:
                    n_hit += 1
                if eng != raw:
                    mism_raw += 1
                if eng != gap:
                    mism_gap += 1
                regime = k0 * k0 >= N
                if regime:
                    n_regime += 1
                    if eng != gap:
                        mism_regime += 1
                else:
                    if len(nonregime_states) < 40:
                        nonregime_states.append(
                            {"M": M, "kappa": kappa, "t": t,
                             "engine_one": eng, "gap_rhs": gap})
    out = {"label": label, "n_states": n_states, "n_regime": n_regime,
           "n_engine_hits": n_hit, "mismatch_engine_vs_raw": mism_raw,
           "mismatch_engine_vs_hitgap_all": mism_gap,
           "mismatch_engine_vs_hitgap_regime": mism_regime,
           "nonregime_sample": nonregime_states,
           "seconds": round(time.time() - t0, 1)}
    elog("%s: states=%d regime=%d hits=%d mism_raw=%d mism_gap=%d "
         "mism_regime=%d (%.0fs)"
         % (label, n_states, n_regime, n_hit, mism_raw, mism_gap,
            mism_regime, time.time() - t0))
    return out


gridA = grid_engine([m for m in primes_between(2, 61)], 1, 50, "GAP-GRID-A")
gridB = grid_engine([m for m in primes_between(2, 23)], 51, 120, "GAP-GRID-B")

# =====================================================================
# SPLIT-GRID: classify all pre-tail hits, M <= 199 prime, live classes
# =====================================================================
elog("SPLIT-GRID")
split = {"violations": 0, "n_hits": 0, "n_branch": 0, "n_smooth_only": 0,
         "t1_branch": 0, "t1_smooth": 0,
         "nonlive_hits": [], "smooth_states": [], "seam_violations": 0,
         "t1_hits": 0}
M_list_199 = primes_between(2, 199)
profile_counts = {}   # M -> {t: [hits, branch, smooth]}
split_all_hits = {}  # M -> list of live-class hit dicts (t <= M-2)
for M in M_list_199:
    for kappa in range(0, M - 1):
        live = math.gcd(kappa + 1, M + 1) == 1
        t0k = 2 if kappa == 0 else 1
        for t in range(t0k, M - 1):
            r = pc.analyze_state(M, kappa, t, yflags, ycap, plist)
            if r is None:
                continue
            if not live:
                if len(split["nonlive_hits"]) < 60:
                    split["nonlive_hits"].append(
                        {"M": M, "kappa": kappa, "t": t, "K": r["K"],
                         "N": r["N"]})
                continue
            if t >= 2:
                split["n_hits"] += 1
                if r["type"] == "branch":
                    split["n_branch"] += 1
                else:
                    split["n_smooth_only"] += 1
                    if not (r["smooth"] and r["n_le_cube"]):
                        split["violations"] += 1
                    if r["t"] >= (M - 3 if M >= 7 else 3):
                        split["seam_violations"] += 1
                    split["smooth_states"].append(
                        {"M": M, "kappa": kappa, "t": t, "K": r["K"],
                         "Y": r["Y"], "N": r["N"], "C": r["C"],
                         "smooth": r["smooth"], "n_le_cube": r["n_le_cube"]})
            else:
                split["t1_hits"] += 1
                if r["type"] == "branch":
                    split["t1_branch"] += 1
                else:
                    split["t1_smooth"] += 1
            split_all_hits.setdefault(M, []).append(
                {"kappa": kappa, "t": t, "type": r["type"]})
            if M in (7, 13, 23, 53, 101, 199):
                prof = profile_counts.setdefault(M, {})
                e = prof.setdefault(t, [0, 0, 0])
                e[0] += 1
                e[1 if r["type"] == "branch" else 2] += 1
elog("SPLIT-GRID: hits(t>=2)=%d branch=%d smooth-only=%d viol=%d "
     "seam_viol=%d t1_hits=%d nonlive_hits=%d"
     % (split["n_hits"], split["n_branch"], split["n_smooth_only"],
        split["violations"], split["seam_violations"], split["t1_hits"],
        len(split["nonlive_hits"])))

# =====================================================================
# T1-CHANNEL: t=1 hits among Y(1)-prime live classes (M <= 199)
elog("T1-CHANNEL")
t1 = {"n_y1_prime_live_kge1": 0, "n_t1_hits": 0, "n_blocked": 0,
      "blocked_sample": []}
for M in primes_between(2, 199):
    for kappa in range(1, M - 1):
        if math.gcd(kappa + 1, M + 1) != 1:
            continue
        Y = M + kappa + 2
        if not ((Y <= ycap and yflags[Y]) or is_prime(Y)):
            continue
        t1["n_y1_prime_live_kge1"] += 1
        r = pc.analyze_state(M, kappa, 1, yflags, ycap, plist)
        if r is not None:
            t1["n_t1_hits"] += 1
        else:
            t1["n_blocked"] += 1
            if len(t1["blocked_sample"]) < 12:
                N = M * Y - 1
                divs = pc.divisors_of(pc.factorize(N, plist))
                win = [d for d in divs if M <= d <= M + kappa - 1]
                t1["blocked_sample"].append(
                    {"M": M, "kappa": kappa, "Y": Y, "N": N,
                     "window_divisors": win})
elog("T1-CHANNEL: Y1-prime=%d hits=%d blocked=%d"
     % (t1["n_y1_prime_live_kge1"], t1["n_t1_hits"], t1["n_blocked"]))

# =====================================================================
# FIRSTHIT: per-class first hits for primes M <= 2000
# =====================================================================
elog("FIRSTHIT scan M<=%d" % M_MAX_FIRSTHIT)
fh_rows = []       # full rows for M <= 199 (crosscheck + prediction)
fh_agg = []        # per-M aggregates for all M <= 2000
fh_all = []        # (M, kappa, t, K, type) compact for all M <= 2000
n_nohit = 0
t0 = time.time()
for M in primes_between(2, M_MAX_FIRSTHIT):
    t_cap = 7 * math.ceil(math.log(M + 1) ** 2) + 100
    rec = {"M": M, "n_live": 0, "n_branch_first": 0, "n_smooth_first": 0,
           "F": 0, "F_kappa": None, "F_t": None, "F_type": None,
           "F_C": None}
    for kappa in range(0, M - 1):
        if math.gcd(kappa + 1, M + 1) != 1:
            continue
        rec["n_live"] += 1
        r = pc.scan_first_hit(M, kappa, t_cap, yflags, ycap, plist)
        if r is None:
            n_nohit += 1
            fh_all.append((M, kappa, None, None, "none"))
            continue
        t, K, typ = r
        C = math.gcd(M + 1, kappa + 2)
        fh_all.append((M, kappa, t, K, typ))
        if typ == "branch":
            rec["n_branch_first"] += 1
        else:
            rec["n_smooth_first"] += 1
        if K > rec["F"]:
            rec["F"] = K
            rec["F_kappa"], rec["F_t"], rec["F_type"] = kappa, t, typ
            rec["F_C"] = C
        if M <= 199:
            fh_rows.append({"M": M, "kappa": kappa, "C": C,
                            "t_first": t, "K_first": K, "type": typ})
    fh_agg.append(rec)
elog("FIRSTHIT scan done (%.0fs), classes with no hit <= cap: %d"
     % (time.time() - t0, n_nohit))

# crosscheck vs tier3 + firsthit_pred
tier3 = json.load(open("pkill_tight_tier3.json"))
mism_t3 = mism_fh = mism_F = 0
for Ms in tier3:
    if Ms == "Kmax":
        continue
    M = int(Ms)
    rec = fh_agg[[r["M"] for r in fh_agg].index(M)]
    for ks, Kf in tier3[Ms]["first"].items():
        kappa = int(ks)
        row = [r for r in fh_rows if r["M"] == M and r["kappa"] == kappa]
        if not row or row[0]["K_first"] != Kf:
            mism_t3 += 1
    if rec["F"] != tier3[Ms]["max_first_K"]:
        mism_F += 1
fh_pred = json.load(open("firsthit_pred.json"))["rows"]
fh_lookup = {(r["M"], r["kappa"]): r for r in fh_rows}
for r in fh_pred:
    key = (r["M"], r["kappa"])
    if key not in fh_lookup:
        mism_fh += 1
    else:
        m = fh_lookup[key]
        if m["K_first"] != r["K_first"] or m["t_first"] != r["t_first"]:
            mism_fh += 1
elog("crosschecks: tier3 mismatch=%d F mismatch=%d firsthit_pred mismatch=%d"
     % (mism_t3, mism_F, mism_fh))

# =====================================================================
# FIRSTHIT-PRED: corrected from-start BH vs observed first hits
# =====================================================================
elog("FIRSTHIT-PRED (M <= 199)")
t0 = time.time()
pl_bh = primes_upto(1000)
pred_rows = []
for r in fh_rows:
    br = Branches(r["M"], r["kappa"])
    tstar = pc.first_hit_tstar(br, pl_bh, t_hi=10 ** 6)
    lam_tf = pc.bh_expected_from_start(br, r["t_first"], pl_bh)
    pred_rows.append({**r, "t_star": round(tstar, 4),
                      "lam_at_first": round(lam_tf, 4)})
elog("BH predictions done (%.0fs)" % (time.time() - t0))

# pooled and within-M Spearman
sp_pooled = spearman([r["t_star"] for r in pred_rows],
                     [r["t_first"] for r in pred_rows])
sp_within = {}
for M in sorted(set(r["M"] for r in pred_rows)):
    sub = [r for r in pred_rows if r["M"] == M]
    if len(sub) >= 3 and len(set(r["t_first"] for r in sub)) > 1:
        sp_within[str(M)] = round(
            spearman([r["t_star"] for r in sub],
                     [r["t_first"] for r in sub]), 4)
sp_within_mean = round(sum(sp_within.values()) / len(sp_within), 4)
lams = sorted(r["lam_at_first"] for r in pred_rows)
lam_med = lams[len(lams) // 2]
lam_mean = round(sum(lams) / len(lams), 4)
# first-hit distribution in corrected BH time (Poisson-race check)
l2 = sorted(r["lam_at_first"] for r in pred_rows if r["t_first"] >= 2)
race = {"n": len(l2), "median": round(l2[len(l2) // 2], 4),
        "mean": round(sum(l2) / len(l2), 4)}
for x in (0.25, 0.5, 1.0, 2.0):
    race["cdf_at_%s" % x] = round(
        sum(1 for v in l2 if v <= x) / len(l2), 4)
    race["exp_cdf_at_%s" % x] = round(1 - math.exp(-x), 4)

# calibration: observed fraction of classes hit by T vs BH-predicted
CAL_T = [2, 3, 5, 8, 12, 20, 30, 50, 80, 120]
cal_pooled = []
for T in CAL_T:
    lam_at_T = []
    for r in fh_rows:
        br = Branches(r["M"], r["kappa"])
        lam_at_T.append(pc.bh_expected_from_start(br, T, pl_bh))
    frac = sum(1 for r in pred_rows if r["t_first"] <= T) / len(pred_rows)
    mlam = sum(lam_at_T) / len(lam_at_T)
    mpred = sum(1 - math.exp(-x) for x in lam_at_T) / len(lam_at_T)
    cal_pooled.append({"T": T, "obs_frac": round(frac, 4),
                       "mean_lambda": round(mlam, 4),
                       "model_frac": round(mpred, 4)})
elog("calibration pooled: " + json.dumps(cal_pooled))

# K0954 tail-only baseline (pooled)
fh_pred_lookup = {(r["M"], r["kappa"]): r for r in fh_pred}
xs = [fh_pred_lookup[(r["M"], r["kappa"])]["t_hat"] for r in pred_rows]
ys = [r["t_first"] for r in pred_rows]
sp_old = spearman(xs, ys)
elog("Spearman pooled: new t*=%.4f  old t_hat=%.4f  within-M mean=%.4f"
     % (sp_pooled, sp_old, sp_within_mean))

# =====================================================================
# RATE-PROFILE: observed per-t counts vs BH cumulative (live classes)
# =====================================================================
elog("RATE-PROFILE")
rate_profile = {}
for M in (7, 13, 23, 53, 101, 199):
    prof = profile_counts[M]
    ts = sorted(prof)
    obs = [{"t": t, "hits": prof[t][0], "branch": prof[t][1],
            "smooth": prof[t][2]} for t in ts]
    # BH cumulative averaged over live classes at sample t points
    live_kappas = [k for k in range(M - 1)
                   if math.gcd(k + 1, M + 1) == 1]
    sample_ts = [t for t in range(1, min(M - 1, 30))]
    bh_cum = []
    for t in sample_ts:
        vals = []
        for k in live_kappas:
            br = Branches(M, k)
            vals.append(pc.bh_expected_from_start(br, t, pl_bh))
        obs_cum = sum(
            1 for r in split_all_hits.get(M, [])
            if r["kappa"] in live_kappas and r["t"] <= t
            and math.gcd(r["kappa"] + 1, M + 1) == 1)
        bh_cum.append({"t": t,
                       "bh_mean_cum": round(sum(vals) / len(vals), 4),
                       "obs_cum_per_class": round(
                           obs_cum / len(live_kappas), 4)})
    rate_profile[str(M)] = {"per_t": obs, "bh_cum": bh_cum}

# =====================================================================
# SMOOTH-LAW
# =====================================================================
smooth_by_M = {}
for s in split["smooth_states"]:
    smooth_by_M.setdefault(s["M"], []).append(s)
smooth_law = {"n_smooth_only_total": split["n_smooth_only"],
              "violations": split["violations"],
              "seam_violations": split["seam_violations"],
              "per_M": {}}
for M in sorted(smooth_by_M):
    ss = smooth_by_M[M]
    smooth_law["per_M"][str(M)] = {
        "n": len(ss),
        "max_t": max(s["t"] for s in ss),
        "states": sorted(ss, key=lambda s: s["t"])}
# smooth-first classes from FIRSTHIT (M <= 2000)
sf = [r for r in fh_all if r[4] == "smooth"]
smooth_law["n_smooth_first_classes_M_le_2000"] = len(sf)
smooth_law["smooth_first_by_M"] = {}
for (M, kappa, t, K, typ) in sf:
    smooth_law["smooth_first_by_M"].setdefault(str(M), 0)
    smooth_law["smooth_first_by_M"][str(M)] += 1
decades = [(2, 31), (31, 101), (101, 317), (317, 1009), (1009, 2001)]
dec_frac = []
for (lo, hi) in decades:
    ncl = sum(r["n_live"] for r in fh_agg if lo <= r["M"] < hi)
    nsm = sum(r["n_smooth_first"] for r in fh_agg if lo <= r["M"] < hi)
    dec_frac.append({"M_range": [lo, hi], "n_classes": ncl,
                     "n_smooth_first": nsm,
                     "frac": round(nsm / ncl, 4) if ncl else None})
smooth_law["smooth_first_frac_by_decade"] = dec_frac

# =====================================================================
# assemble + write
# =====================================================================
audit = {
    "experiment": "remo-prehit-mechanism-20261118",
    "pin": pin,
    "engine_anchor_and_grids": [gridA, gridB],
    "split_grid": {k: v for k, v in split.items()
                   if k != "smooth_states"},
    "t1_channel": t1,
    "firsthit": {
        "m_max": M_MAX_FIRSTHIT,
        "n_live_classes_total": sum(r["n_live"] for r in fh_agg),
        "n_no_hit_within_cap": n_nohit,
        "mismatch_vs_tier3_first": mism_t3,
        "mismatch_vs_tier3_F": mism_F,
        "mismatch_vs_firsthit_pred": mism_fh,
        "n_branch_first": sum(r["n_branch_first"] for r in fh_agg),
        "n_smooth_first": sum(r["n_smooth_first"] for r in fh_agg),
        "F_by_M": [{ "M": r["M"], "F": r["F"], "F_kappa": r["F_kappa"],
                     "F_t": r["F_t"], "F_type": r["F_type"],
                     "F_C": r["F_C"], "n_live": r["n_live"],
                     "n_branch_first": r["n_branch_first"],
                     "n_smooth_first": r["n_smooth_first"]}
                    for r in fh_agg],
    },
    "firsthit_pred": {
        "spearman_pooled_new_tstar": round(sp_pooled, 4),
        "spearman_pooled_old_t_hat": round(sp_old, 4),
        "spearman_within_M": sp_within,
        "spearman_within_M_mean": sp_within_mean,
        "lam_at_first_median": round(lam_med, 4),
        "lam_at_first_mean": lam_mean,
        "lam_at_first_p10": lams[len(lams) // 10],
        "lam_at_first_p90": lams[(9 * len(lams)) // 10],
        "calibration_pooled": cal_pooled,
        "poisson_race_t_first_ge2": race,
    },
    "rate_profile": rate_profile,
    "smooth_law": {k: v for k, v in smooth_law.items()
                   if k != "per_M"} | {"per_M": {
                       m: {"n": v["n"], "max_t": v["max_t"],
                           "states": v["states"]}
                       for m, v in smooth_law["per_M"].items()}},
}
with open(os.path.join(OUT, "audit.json"), "w") as f:
    json.dump(audit, f, indent=1, sort_keys=True)
with open(os.path.join(OUT, "firsthit_rows.json"), "w") as f:
    json.dump(pred_rows, f, indent=1, sort_keys=True)
elog("written audit.json, firsthit_rows.json")
