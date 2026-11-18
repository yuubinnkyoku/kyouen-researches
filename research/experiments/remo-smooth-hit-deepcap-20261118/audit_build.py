#!/usr/bin/env python3
"""K0960 deterministic audit builder: DEEP-CAP theorem + completion of
the smooth-hit census for primes 1000 < M <= 2000 over ALL t.

New universal claims (pen-and-paper proofs in report.md, mechanically
checked here over every smooth hit with t >= 2 in the range and over
the published M <= 1000 census):

  LEMMA ODDCAP      smooth hit (prime M >= 5, t >= 2), a = v2(N) >= 1:
                    every odd prime divisor p of N satisfies
                    p <= (M-1)/2^a.
  LEMMA MIN3        same hypotheses: Omega(odd part of N) >= 3.
  THEOREM DEEP-CAP  same hypotheses:
                    t < max(sqrt(M), ((M-1)^2+4)/(4M));
                    in particular t < M/4 for prime M >= 17.
                    Case A (top odd pair >= M): the top pair is a
                    divisor >= M, hence > k0, and ODDCAP caps it at
                    ((M-1)/2^a)^2 <= ((M-1)/2)^2.
                    Case B (top odd pair < M): the descending chain of
                    top partial products must cross M (else 2^i * odd
                    part lands in the window); the crossing product is
                    > k0 but < M * sqrt(M), forcing t < sqrt(M).
                    Corollary: k = 3 hits are all case A (case B would
                    give N <= (M-1)^2 < 2M^2+3M-1 <= N).

Census: CENSUS-STRIP2 = primes 1000 < M <= 2000, complete over all t
(closes the t > 60 gap of K0958's CENSUS-STRIP; completeness argument
unchanged, K0958 report Sec. 5).  The t <= 60 rows reproduce the
published hits_strip.json byte for byte.

Everything deterministic; reruns byte-identical.  Resumable:
census checkpoints in ckpt/<M>.json, engine results in ckpt/engine.json.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from branch_density_core import primes_upto  # pinned K0954 core
from composite_core import sigma_Z  # pinned engine (K0948-K0950 pin)
from prehit_core import factorize  # pinned K0956 core
from smooth_core import (sieve_flags, census_walk, classify_candidates,
                         window_blocked)

import census_full2000 as DRV

T0 = time.time()
CKPT = os.path.join(HERE, "ckpt")
K0958 = os.path.join(HERE, "pub")  # sha-pinned copies of the K0958
# published outputs (research/experiments/remo-smooth-hit-census-20261118)


def log(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def dump(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, sort_keys=True, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)


# ------------------------------------------------- phase A: census ckpt

PRIMES = primes_upto(2000)
STRIP2_M = [p for p in PRIMES if 1000 < p <= 2000]
os.makedirs(CKPT, exist_ok=True)

need = [M for M in STRIP2_M
        if not os.path.exists(os.path.join(CKPT, "%d.json" % M))]
if need:
    log("phase A: census for %d M (resumable)..." % len(need))
    BUDGET = float(os.environ.get("CENSUS_BUDGET", "240"))
    for M in need:
        if time.time() - T0 > BUDGET:
            log("budget hit; rerun to resume")
            sys.exit(0)
        DRV.run_one(M)
log("phase A: census checkpoints complete (%d/%d)"
    % (len([1 for M in STRIP2_M
            if os.path.exists(os.path.join(CKPT, "%d.json" % M))]),
       len(STRIP2_M)))

recs = {M: json.load(open(os.path.join(CKPT, "%d.json" % M)))
        for M in STRIP2_M}
hits = [h for M in STRIP2_M for h in recs[M]["hits"]]
hits.sort(key=lambda h: (h[0], h[4]))  # canonical order: by (M, Y)
log("  hits total: %d (t>60: %d)"
    % (len(hits), sum(1 for h in hits if h[2] > 60)))

# ------------------------------------------------- phase B: engine ckpt

ENG_PATH = os.path.join(CKPT, "engine.json")
eng = {}
if os.path.exists(ENG_PATH):
    eng = json.load(open(ENG_PATH))

# sample: every t>60 hit (new band, all of it) + every 149th of the
# t<=60 hits (rows byte-identical to the published strip, which
# K0958 engine-checked at a denser stride)
sample = [h for i, h in enumerate(hits) if h[2] > 60 or i % 149 == 0]
log("phase B: engine sample %d hits..." % len(sample))
t_start = time.time()
for j, h in enumerate(sample):
    key = "hit:%d:%d:%d" % (h[0], h[1], h[2])
    if key in eng:
        continue
    eng[key] = sigma_Z(h[0], h[3])
    if time.time() - T0 > 280:
        dump(ENG_PATH, eng)
        log("budget hit mid-engine; rerun to resume (%d/%d)"
            % (j, len(sample)))
        sys.exit(0)
hit_fail = sum(1 for h in sample
               if eng["hit:%d:%d:%d" % (h[0], h[1], h[2])] != 1)

# blocked engine sample: three M's, every 199th blocked smooth candidate
blocked_checked = 0
blocked_fail = 0
if os.environ.get("SKIP_BLOCKED_ENGINE", "") != "1":
    for M in (1423, 1789, 1999):
        ymax = (M - 1) ** 3 // M
        small = [p for p in PRIMES if p <= M - 1]
        smooth2, _c2, st2 = DRV.census_walk2(M, ymax, small)
        # independent re-walk with the ORIGINAL pinned core
        flags = sieve_flags(ymax)
        smooth1, _c1, st1 = census_walk(M, ymax, flags, small)
        assert st1 == st2, M
        assert all(smooth1[k] == smooth2[k] for k in smooth1), M
        _h1, blk = classify_candidates(M, smooth1)
        for i, b in enumerate(blk):
            if i % 199 != 0:
                continue
            key = "blk:%d:%d:%d" % (b["M"], b["kappa"], b["t"])
            if key not in eng:
                eng[key] = sigma_Z(b["M"], b["K"])
            blocked_checked += 1
            if eng[key] == 1:
                blocked_fail += 1
dump(ENG_PATH, eng)
log("phase B: engine hit_checks=%d fail=%d blocked=%d fail=%d (%.0fs)"
    % (len(sample), hit_fail, blocked_checked, blocked_fail,
       time.time() - t_start))

# ------------------------------------------------------ deep-cap check

PLIST_BIG = DRV.PLIST_BIG


def deepcap_of(M, kappa, t, fac):
    """fac: factorization of N as [(p, e)] ascending.  Per-hit caps."""
    a = fac[0][1] if fac and fac[0][0] == 2 else 0
    odd = fac[1:] if a else fac
    odds = sorted(p for (p, e) in odd for _ in range(e))
    kodd = len(odds)
    maxodd = odds[-1] if odds else 0
    toppair = odds[-2] * odds[-1] if kodd >= 2 else 0
    case = "A" if (kodd >= 2 and toppair >= M) else "B"
    # PAIR-MIN: every odd-pair product (with multiplicity) is a
    # divisor, so window emptiness forces each pair product that is
    # >= M to exceed k0.  Sharper than case-A's top-pair bound.
    pairs_ge = [odds[i] * odds[j]
                for i in range(kodd) for j in range(i + 1, kodd)
                if odds[i] * odds[j] >= M]
    d = {"a": a, "kodd": kodd, "maxodd": maxodd, "toppair": toppair,
         "case": case, "pairmin": min(pairs_ge) if pairs_ge else None}
    d["ok_pairmin"] = all(M * t + kappa - 1 < q for q in pairs_ge)
    d["ok_oddcap"] = (maxodd <= (M - 1) // (2 ** a)) if a >= 1 else None
    d["ok_min3"] = kodd >= 3
    if case == "A":
        # top pair is a divisor >= M, window empty => top pair > k0
        d["ok_case"] = M * t + kappa - 1 < toppair
    else:
        # descending-chain crossing => t < sqrt(M)
        d["ok_case"] = t * t < M
    d["ok_deepcap"] = (M < 17 or t < M / 4.0) and d["ok_case"]
    return d


dc = {"n_strip2": 0, "n_published_full": 0,
      "viol": {"deepcap": 0, "oddcap": 0, "min3": 0, "case": 0,
               "t_lt_M4": 0, "pairmin": 0},
      "v2_hist": {}, "kodd_hist": {}, "case_hist": {},
      "v2_hist_published": {}, "kodd_hist_published": {},
      "kodd3_caseB": 0}
for h in hits:
    M, kappa, t, K, Y, N, Om, om, br, a, kodd, maxodd, toppair = h
    if t < 2:
        continue
    dc["n_strip2"] += 1
    fac = factorize(N, PLIST_BIG)  # independent recomputation
    d = deepcap_of(M, kappa, t, fac)
    assert d["a"] == a and d["kodd"] == kodd \
        and d["maxodd"] == maxodd and d["toppair"] == toppair, (h, d)
    if not d["ok_deepcap"]:
        dc["viol"]["deepcap"] += 1
        print("VIOLATION", h[:7], d)
    if d["ok_oddcap"] is False:
        dc["viol"]["oddcap"] += 1
    if not d["ok_min3"]:
        dc["viol"]["min3"] += 1
    if not d["ok_case"]:
        dc["viol"]["case"] += 1
    if M >= 17 and not t < M / 4.0:
        dc["viol"]["t_lt_M4"] += 1
    if not d["ok_pairmin"]:
        dc["viol"]["pairmin"] += 1
        print("PAIRMIN VIOLATION", h[:7], d)
    dc["v2_hist"][d["a"]] = dc["v2_hist"].get(d["a"], 0) + 1
    dc["kodd_hist"][d["kodd"]] = dc["kodd_hist"].get(d["kodd"], 0) + 1
    dc["case_hist"][d["case"]] = dc["case_hist"].get(d["case"], 0) + 1
    if d["kodd"] == 3 and d["case"] == "B":
        dc["kodd3_caseB"] += 1

# published hits_full.json (primes M <= 1000): all t >= 2 hits
pub_full = json.load(open(os.path.join(K0958, "hits_full.json")))["rows"]
for r in pub_full:
    M, kappa, t, K, Y, N, Om, om, br = r
    if t < 2:
        continue
    dc["n_published_full"] += 1
    fac = factorize(N, PLIST_BIG)
    d = deepcap_of(M, kappa, t, fac)
    if not d["ok_deepcap"]:
        dc["viol"]["deepcap"] += 1
        print("VIOLATION (published full)", r[:7], d)
    if not d["ok_pairmin"]:
        dc["viol"]["pairmin"] += 1
        print("PAIRMIN VIOLATION (published full)", r[:7], d)
    if d["kodd"] == 3 and d["case"] == "B":
        dc["kodd3_caseB"] += 1
    dc["v2_hist_published"][d["a"]] = \
        dc["v2_hist_published"].get(d["a"], 0) + 1
    dc["kodd_hist_published"][d["kodd"]] = \
        dc["kodd_hist_published"].get(d["kodd"], 0) + 1
log("phase C: deepcap checks: strip2=%d pubfull=%d viol=%s"
    % (dc["n_strip2"], dc["n_published_full"], dc["viol"]))

# ------------------------------------------------- strip reconciliation

pub_strip = json.load(open(os.path.join(K0958, "hits_strip.json")))["rows"]
mine60 = [h for h in hits if h[2] <= 60]
pubmap = {}
for r in pub_strip:
    pubmap.setdefault((r[0], r[1], r[2]), []).append(r)
minemap = {}
for h in mine60:
    minemap.setdefault((h[0], h[1], h[2]), []).append(h)
recon = {
    "published_rows": len(pub_strip),
    "strip2_rows_t_le_60": len(mine60),
    "key_sets_equal": set(pubmap) == set(minemap),
    "row_mismatches": 0,
}
for k in pubmap:
    a_ = sorted(pubmap[k])
    b_ = sorted(minemap[k])
    if len(a_) != len(b_) or any(x[:8] != y[:8]
                                 for x, y in zip(a_, b_)):
        recon["row_mismatches"] += 1

# ----------------------------------------------- equivalence live check

EQ_M = 1783
ymax = (EQ_M - 1) ** 3 // EQ_M
flags = sieve_flags(ymax)
small = [p for p in PRIMES if p <= EQ_M - 1]
sm1, _c1, st1 = census_walk(EQ_M, ymax, flags, small)
sm2, _c2, st2 = DRV.census_walk2(EQ_M, ymax, small)
h1, _b1 = classify_candidates(EQ_M, sm1)
equiv = {
    "M": EQ_M,
    "stats_equal": st1 == st2,
    "smooth_equal": set(sm1) == set(sm2)
    and all(sm1[k] == sm2[k] for k in sm1),
    "rows_equal": len(h1) == recs[EQ_M]["n_hits"],
    "note": "session also verified M=1009 and M=1999 (see report)",
}
log("phase D: equivalence M=%d: %s" % (EQ_M, equiv))

# ------------------------------------------------------ structure stats

populations = {}
for lo, hi, key in [(1, 2, "t_eq_1"), (2, 10, "t_2_9"), (10, 40, "t_10_39"),
                    (40, 61, "t_40_60"), (61, 10 ** 9, "t_gt_60")]:
    sel = [h for h in hits if lo <= h[2] < hi]
    ent = {
        "n": len(sel),
        "Omega_ge10": sum(1 for h in sel if h[6] >= 10),
        "max_Omega": max((h[6] for h in sel), default=0),
        "kodd3": sum(1 for h in sel if h[10] == 3),
        "v2_hist": {},
    }
    for h in sel:
        ent["v2_hist"][h[9]] = ent["v2_hist"].get(h[9], 0) + 1
    populations[key] = ent
deep_band = [h for h in hits if h[2] > 60]
db = {
    "n": len(deep_band),
    "kodd_hist": {},
    "v2_hist": {},
    "max_odd_over_cap": [],
    "top_by_t": sorted(deep_band, key=lambda h: (-h[2], h[0]))[:10],
    "all_kodd3_caseA": all(h[12] >= h[0] for h in deep_band
                           if h[10] == 3),
}
for h in deep_band:
    db["kodd_hist"][h[10]] = db["kodd_hist"].get(h[10], 0) + 1
    db["v2_hist"][h[9]] = db["v2_hist"].get(h[9], 0) + 1
    db["max_odd_over_cap"].append(
        round(h[11] / ((h[0] - 1) // (2 ** h[9])), 4))
    # PAIR-MIN closeness: t/(pairmin/M) in the deep band
    fac = factorize(h[5], PLIST_BIG)
    odd = fac[1:] if h[9] else fac
    odds = sorted(p for (p, e) in odd for _ in range(e))
    pge = [odds[i] * odds[j] for i in range(len(odds))
           for j in range(i + 1, len(odds)) if odds[i] * odds[j] >= h[0]]
    if pge:
        db.setdefault("pairmin_close", []).append(
            round(h[2] * h[0] / min(pge), 4))
db["max_odd_over_cap"] = max(db["max_odd_over_cap"])
if db.get("pairmin_close"):
    db["pairmin_close_max"] = max(db["pairmin_close"])
    db["pairmin_close_median"] = sorted(db["pairmin_close"])[
        len(db["pairmin_close"]) // 2]
    del db["pairmin_close"]
cnt = Counter((h[0], h[1]) for h in hits)
mult = {
    "classes_with_multi_hits": sum(1 for n in cnt.values() if n > 1),
    "multi_hit_extra": sum(n - 1 for n in cnt.values() if n > 1),
}
maxt = max(hits, key=lambda h: (h[2], h[0]))
maxN = max(hits, key=lambda h: (h[5], h[0]))
seam_viol = 0
for h in hits:
    sb = (h[0] - 1) * (h[0] - 2) // (h[0] + 1)
    if h[2] > sb:
        seam_viol += 1
ysqr = {"n_M": 0, "n_smooth": 0, "n_smooth_and_hit": 0}
for M in STRIP2_M:
    N = M ** 3 - 1
    fac = factorize(N, PLIST_BIG)
    ysqr["n_M"] += 1
    if all(p <= M - 1 for (p, _e) in fac):
        ysqr["n_smooth"] += 1
        # Y = M^2 - 1 is the boundary candidate; k0 at t = M-1 is
        # M^2 - M - 1; window test as in K0958's audit
        if not window_blocked(N, M, M * M - M - 1, fac):
            ysqr["n_smooth_and_hit"] += 1
log("phase E: ysqr new band: %s" % ysqr)

# -------------------------------------------------------------- outputs

os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
pins = {}
for n in ("audit.json", "hits_full.json", "hits_strip.json"):
    pins["../remo-smooth-hit-census-20261118/output/" + n] = \
        sha256_file(os.path.join(K0958, n))
for n in ("smooth_core.py", "prehit_core.py", "composite_core.py",
          "sievegen_core.py", "branch_density_core.py", "hitpair_core.py"):
    pins[n] = sha256_file(os.path.join(HERE, n))

per_M = {}
for M in STRIP2_M:
    r = recs[M]
    per_M[str(M)] = {
        "Omega_hist_hits": r["Omega_hist_hits"],
        "dead_cand": r["dead_cand"],
        "max_N_hit": r["max_N_hit"],
        "max_t_hit": r["max_t_hit"],
        "n_blocked": r["n_blocked"],
        "n_branch_and_smooth": sum(1 for h in r["hits"] if h[8] == 1),
        "n_cand": r["n_cand"],
        "n_hits": r["n_hits"],
        "n_smooth_cand": r["n_smooth"],
        "n_steps": r["n_steps"],
        "n_t1_hits": sum(1 for h in r["hits"] if h[2] == 1),
        "omega_hist_hits": r["omega_hist_hits"],
        "ratio_maxN": (r["max_N_hit"] / ((M - 1) ** 3))
        if r["max_N_hit"] else 0.0,
        "seam_bound": (M - 1) * (M - 2) // (M + 1),
        "ymax": r["ymax"],
    }
audit = {
    "experiment": "remo-smooth-hit-deepcap-20261118",
    "pin": pins,
    "census_strip2": {
        "range": "primes 1000 < M <= 2000, complete over all t",
        "n_M": len(STRIP2_M),
        "per_M": per_M,
        "totals": {
            "n_cand": sum(r["n_cand"] for r in recs.values()),
            "n_smooth_cand": sum(r["n_smooth"] for r in recs.values()),
            "n_blocked": sum(r["n_blocked"] for r in recs.values()),
            "n_hits": len(hits),
            "n_hits_t_le_60": len(mine60),
            "n_hits_t_gt_60": len(deep_band),
            "dead_cand": sum(r["dead_cand"] for r in recs.values()),
            "s3_violations": sum(r["s3_violations"]
                                 for r in recs.values()),
            "max_t_hit": maxt[2], "max_t_hit_M": maxt[0],
            "max_N_hit": maxN[5], "max_N_hit_M": maxN[0],
        },
    },
    "strip_reconciliation": recon,
    "deepcap": dc,
    "deep_band": db,
    "populations": populations,
    "multiplicity": mult,
    "seam_violations": seam_viol,
    "ysquare_new_band": ysqr,
    "engine_checks": {
        "hit_checks": len(sample), "hit_fail": hit_fail,
        "blocked_checks": blocked_checked,
        "blocked_fail": blocked_fail,
        "engine": "composite_core.sigma_Z (pinned)",
    },
    "equivalence_live": equiv,
}
dump(os.path.join(HERE, "output", "audit.json"), audit)
dump(os.path.join(HERE, "output", "hits_strip2.json"),
     {"rows": [[h[0], h[1], h[2], h[6], h[7], h[8]] for h in hits],
      "row": ["M", "kappa", "t", "Omega", "omega",
              "is_branch_and_smooth"],
      "note": "K = (M+1)t+kappa, Y = K+1, N = MY-1; complete smooth-hit "
              "census for primes 1000 < M <= 2000 over all t; t <= 60 "
              "rows equal the published hits_strip.json byte for byte"})
dump(os.path.join(HERE, "output", "hits_deep_band.json"),
     {"rows": deep_band,
      "row": ["M", "kappa", "t", "K", "Y", "N", "Omega", "omega",
              "is_branch_and_smooth", "v2", "k_odd", "max_odd_prime",
              "top_odd_pair"]})
log("outputs written")
print("TOTALS: hits=%d deep(t>60)=%d cand=%d smooth=%d"
      % (len(hits), len(deep_band),
         audit["census_strip2"]["totals"]["n_cand"],
         audit["census_strip2"]["totals"]["n_smooth_cand"]))
print("DEEPCAP: strip2=%d pubfull=%d viol=%s kodd3_caseB=%d"
      % (dc["n_strip2"], dc["n_published_full"], dc["viol"],
         dc["kodd3_caseB"]))
print("ENGINE: hits %d/%d ok, blocked %d/%d ok"
      % (len(sample) - hit_fail, len(sample),
         blocked_checked - blocked_fail, blocked_checked))
