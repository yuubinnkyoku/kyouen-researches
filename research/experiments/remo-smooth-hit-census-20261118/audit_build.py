#!/usr/bin/env python3
"""K0958 deterministic audit builder: complete smooth-hit census.

CENSUS-FULL : primes 5 <= M <= 1000, complete over all t.
CENSUS-STRIP: primes 1000 < M <= 2000, complete within t <= 60.

Outputs (byte-identical on rerun; no timestamps in the JSON):
  output/audit.json          aggregates + checks + pins
  output/hits_full.json      compact hit rows, CENSUS-FULL
  output/hits_strip.json    compact hit rows, CENSUS-STRIP
  output/firstclass_M199.json per-class first hits, primes M <= 199

Inputs pinned by sha256 (see audit.json pin section):
  ../remo-prehit-mechanism-20261118/output/audit.json (K0956)
  ../remo-prehit-mechanism-20261118/output/firsthit_rows.json (K0956)
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from branch_density_core import primes_upto  # pinned K0954 core
from composite_core import sigma_Z  # pinned engine (K0948-K0950 pin)
from prehit_core import factorize, scan_first_hit  # pinned K0956 core
from smooth_core import (sieve_flags, census_walk, classify_candidates,
                         enrich_hits)

HERE = os.path.dirname(os.path.abspath(__file__))
K0956 = os.path.join(HERE, "..", "remo-prehit-mechanism-20261118",
                     "output")

T0 = time.time()


def log(msg: str) -> None:
    print("[%6.1fs] %s" % (time.time() - T0, msg), flush=True)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def dump(path: str, obj) -> None:
    with open(path, "w") as f:
        json.dump(obj, f, sort_keys=True, separators=(",", ":"))
        f.write("\n")


# ----------------------------------------------------------------- inputs

PIN_NAMES = {
    "audit.json": os.path.join(K0956, "audit.json"),
    "firsthit_rows.json": os.path.join(K0956, "firsthit_rows.json"),
}
pins = {n: sha256_file(p) for n, p in PIN_NAMES.items()}
k0956 = json.load(open(PIN_NAMES["audit.json"]))
firsthit_rows = json.load(open(PIN_NAMES["firsthit_rows.json"]))
log("loaded pinned K0956 outputs")

PRIMES = primes_upto(2000)
PLIST_BIG = primes_upto(32000)  # sqrt((M-1)^3) <= ~31623 for M <= 2000
YFLAGS = sieve_flags(1000000)   # covers (M-1)^3/M for M <= 1000
assert (997 - 1) ** 3 // 997 < 1000000  # largest ymax in FULL

# ----------------------------------------------------------- census run


def run_census(M_list, strip: bool):
    per_M = {}
    hits_all = []
    s3_viol = 0
    dead_total = 0
    omega_hist_hits = {}
    omega_hist_blocked = {}
    Omega_hist_hits = {}
    Omega_hist_blocked = {}
    max_Omega_hit = 0
    max_Omega_blocked = 0
    hits_Omega_ge5 = []
    for M in M_list:
        if strip:
            ymax = 61 * (M + 1)  # t <= 60 complete
        else:
            ymax = (M - 1) ** 3 // M
        small = [p for p in PRIMES if p <= M - 1]
        smooth, cand, st = census_walk(M, ymax, YFLAGS, small)
        hits, blocked = classify_candidates(M, smooth)
        enrich_hits(M, hits, PLIST_BIG)
        dead_total += st["dead_cand"]
        seam_bound = (M - 1) * (M - 2) // (M + 1)
        n_hit_classes = len({h["kappa"] for h in hits})
        max_t = max((h["t"] for h in hits), default=0)
        max_N = max((h["N"] for h in hits), default=0)
        Om_h = {}
        Om_b = {}
        om_h = {}
        for h in hits:
            Om_h[h["Omega"]] = Om_h.get(h["Omega"], 0) + 1
            om_h[h["omega"]] = om_h.get(h["omega"], 0) + 1
            omega_hist_hits[h["omega"]] = \
                omega_hist_hits.get(h["omega"], 0) + 1
            Omega_hist_hits[h["Omega"]] = \
                Omega_hist_hits.get(h["Omega"], 0) + 1
            if h["Omega"] > max_Omega_hit:
                max_Omega_hit = h["Omega"]
            if h["Omega"] >= 5:
                hits_Omega_ge5.append(h)
            assert h["t"] <= seam_bound or h["t"] == 1, (M, h)
        for b in blocked:
            Om_b[b["Omega"]] = Om_b.get(b["Omega"], 0) + 1
            omega_hist_blocked[b["omega"]] = \
                omega_hist_blocked.get(b["omega"], 0) + 1
            Omega_hist_blocked[b["Omega"]] = \
                Omega_hist_blocked.get(b["Omega"], 0) + 1
            if b["Omega"] > max_Omega_blocked:
                max_Omega_blocked = b["Omega"]
            if b["Omega"] <= 3:
                s3_viol += 1  # Lemma S3' violation (must be 0)
        per_M[str(M)] = {
            "Omega_hist_blocked": Om_b,
            "Omega_hist_hits": Om_h,
            "dead_cand": st["dead_cand"],
            "max_N_hit": max_N,
            "max_t_hit": max_t,
            "n_blocked": len(blocked),
            "n_branch_and_smooth": sum(1 for h in hits
                                       if h["type"] == "branch"),
            "n_cand": st["n_cand"],
            "n_hit_classes": n_hit_classes,
            "n_hits": len(hits),
            "n_smooth_cand": len(smooth),
            "n_smooth_only": sum(1 for h in hits
                                 if h["type"] == "smooth-only"),
            "n_steps": st["n_steps"],
            "n_t1_hits": sum(1 for h in hits if h["t"] == 1),
            "omega_hist_hits": om_h,
            "ratio_maxN": (max_N / ((M - 1) ** 3)) if max_N else 0.0,
            "seam_bound": seam_bound,
            "ymax": ymax,
        }
        hits_all.extend(hits)
    return {
        "per_M": per_M, "hits": hits_all, "s3_violations": s3_viol,
        "dead_cand": dead_total,
        "omega_hist_hits": omega_hist_hits,
        "omega_hist_blocked": omega_hist_blocked,
        "Omega_hist_hits": Omega_hist_hits,
        "Omega_hist_blocked": Omega_hist_blocked,
        "max_Omega_hit": max_Omega_hit,
        "max_Omega_blocked": max_Omega_blocked,
        "hits_Omega_ge5": hits_Omega_ge5,
    }


full_M = [p for p in PRIMES if 5 <= p <= 1000]
strip_M = [p for p in PRIMES if 1000 < p <= 2000]
log("CENSUS-FULL over %d primes..." % len(full_M))
FULL = run_census(full_M, strip=False)
log("  hits=%d blocked=%d s3viol=%d dead=%d maxOmegaHit=%d maxOmegaBlk=%d"
    % (len(FULL["hits"]), sum(v["n_blocked"] for v in FULL["per_M"].values()),
       FULL["s3_violations"], FULL["dead_cand"], FULL["max_Omega_hit"],
       FULL["max_Omega_blocked"]))
log("CENSUS-STRIP over %d primes (t <= 60)..." % len(strip_M))
STRIP = run_census(strip_M, strip=True)
log("  hits=%d blocked=%d"
    % (len(STRIP["hits"]), sum(v["n_blocked"] for v in STRIP["per_M"].values())))

# ------------------------------------------------ FIRST-CLASS M <= 199


log("FIRST-CLASS recompute (per-class first hits, M <= 199)...")
firstclass = []
for M in [p for p in PRIMES if 2 <= p <= 199]:
    t_cap = int(7 * math.log(M + 1) ** 2 + 100)
    for kap in range(0, M - 1):
        if math.gcd(kap + 1, M + 1) != 1:
            continue
        r = scan_first_hit(M, kap, t_cap, YFLAGS, 1000000, PLIST_BIG)
        assert r is not None, (M, kap)
        firstclass.append({"M": M, "kappa": kap, "t_first": r[0],
                           "K_first": r[1], "type_first": r[2]})
log("  %d live classes" % len(firstclass))

# ---------------------------------------------------------- crosschecks

log("crosschecks vs published K0956 outputs...")
cc = {}
# (1) published 29 smooth-only states (M <= 199, t in [2, M-2])
pub_states = []
for _m, v in k0956["smooth_law"]["per_M"].items():
    pub_states.extend(v["states"])
pub_set = {(s["M"], s["kappa"], s["t"]) for s in pub_states}
mine_full = FULL["hits"]
mine_199 = [h for h in mine_full if h["M"] <= 199
            and 2 <= h["t"] <= h["M"] - 2]
mine_set = {(h["M"], h["kappa"], h["t"]) for h in mine_199}
cc["pub29_match"] = {
    "n_published": len(pub_states),
    "n_census": len(mine_set),
    "exact_match": pub_set == mine_set,
    "field_mismatch": sum(
        1 for s in pub_states
        for h in mine_199
        if (h["M"], h["kappa"], h["t"]) == (s["M"], s["kappa"], s["t"])
        and (h["K"] != s["K"] or h["N"] != s["N"] or h["C"] != s["C"])),
}
# (2) T1-CHANNEL: t=1 smooth hits count (97 for M <= 199)
cc["t1_smooth"] = {
    "published_n_t1_hits": k0956["t1_channel"]["n_t1_hits"],
    "census_n_t1_hits_M_le_199": sum(
        1 for h in mine_full if h["M"] <= 199 and h["t"] == 1),
    "published_smooth_t1": 97,
    "census_smooth_t1_M_le_199": sum(
        1 for h in mine_full if h["M"] <= 199 and h["t"] == 1),
}
# (3) firsthit_rows smooth-type rows: (M, K) must be census hits
fr_smooth = [r for r in firsthit_rows if r["type"] == "smooth"]
hit_keys = {(h["M"], h["K"]): h for h in mine_full if h["M"] <= 199}
bad = 0
for r in fr_smooth:
    h = hit_keys.get((r["M"], r["K_first"]))
    if h is None or h["t"] != r["t_first"]:
        bad += 1
cc["firsthit_rows_smooth"] = {
    "n_rows": len(fr_smooth), "n_mismatch": bad}
# (4) n_smooth_first (F_by_M) vs census hit-class counts
fbm = k0956["firsthit"]["F_by_M"]
nsf = {r["M"]: r["n_smooth_first"] for r in fbm}
viol_full = []
for M in full_M:
    if FULL["per_M"][str(M)]["n_hit_classes"] < nsf.get(M, 0):
        viol_full.append(M)
strip_ge = []
for M in strip_M:
    ok = STRIP["per_M"][str(M)]["n_hit_classes"] >= nsf.get(M, 0)
    strip_ge.append({"M": M, "ge": ok,
                     "n_strip_hit_classes": STRIP["per_M"][str(M)]["n_hit_classes"],
                     "n_smooth_first_pub": nsf.get(M, 0)})
cc["n_smooth_first_vs_census"] = {
    "full_range_violations": viol_full,
    "strip_shortfall": [s for s in strip_ge if not s["ge"]],
    "n_strip_M": len(strip_M),
}
# (5) per-class first-hit type counts vs F_by_M (M <= 199)
nsf_199 = {}
nbf_199 = {}
for r in firstclass:
    if r["type_first"] == "smooth":
        nsf_199[r["M"]] = nsf_199.get(r["M"], 0) + 1
    else:
        nbf_199[r["M"]] = nbf_199.get(r["M"], 0) + 1
mm = []
for M in sorted({r["M"] for r in firstclass}):
    if nsf_199.get(M, 0) != nsf.get(M, 0):
        mm.append(M)
cc["firstclass_type_counts_vs_pub"] = {
    "mismatch_M": mm, "n_M": len({r["M"] for r in firstclass}),
    "total_smooth_first_recomputed": sum(nsf_199.values())}
# (6) row-level: my recompute vs published firsthit_rows.json
pub_rows = {(r["M"], r["kappa"]): r for r in firsthit_rows}
row_mm = 0
for r in firstclass:
    p = pub_rows.get((r["M"], r["kappa"]))
    if p is None or p["t_first"] != r["t_first"] or \
            p["K_first"] != r["K_first"] or p["type"] != r["type_first"]:
        row_mm += 1
cc["firstclass_rows_vs_pub"] = {
    "n_rows_pub": len(pub_rows), "n_rows_recomputed": len(firstclass),
    "n_mismatch": row_mm}

# ------------------------------------------------------- engine checks

log("engine checks (sampled)...")
eng = {"hit_checks": 0, "hit_fail": 0, "blocked_checks": 0,
       "blocked_fail": 0}
all_hits = [(h, "full") for h in FULL["hits"]] + \
    [(h, "strip") for h in STRIP["hits"]]
for i, (h, tag) in enumerate(all_hits):
    take = h["M"] <= 199 or (tag == "full" and i % 29 == 0) or \
        (tag == "strip" and i % 97 == 0)
    if not take:
        continue
    eng["hit_checks"] += 1
    if sigma_Z(h["M"], h["K"]) != 1:
        eng["hit_fail"] += 1
all_blocked_n = sum(v["n_blocked"] for v in FULL["per_M"].values()) + \
    sum(v["n_blocked"] for v in STRIP["per_M"].values())
# deterministic blocked sample: re-walk cheaply is costly; instead sample
# from stored blocked Omega>=5 rows and a stride over per-M blocked lists
# is not stored -> use hits-independent check: verify blocked rows we kept
for h in FULL["hits_Omega_ge5"] + STRIP["hits_Omega_ge5"]:
    pass  # these are hits, already checked if sampled
log("  hit_checks=%d fail=%d" % (eng["hit_checks"], eng["hit_fail"]))

# blocked engine sample: rerun classification for a few M and check
blocked_checked = 0
blocked_fail = 0
for M in [127, 199, 499, 997]:
    ymax = (M - 1) ** 3 // M
    small = [p for p in PRIMES if p <= M - 1]
    smooth, _c, _s = census_walk(M, ymax, YFLAGS, small)
    hits, blocked = classify_candidates(M, smooth)
    for j, b in enumerate(blocked):
        if j % 97 != 0:
            continue
        blocked_checked += 1
        if sigma_Z(b["M"], b["K"]) == 1:
            blocked_fail += 1
eng["blocked_checks"] = blocked_checked
eng["blocked_fail"] = blocked_fail
log("  blocked_checks=%d fail=%d" % (blocked_checked, blocked_fail))

# -------------------------------------------------------------- outputs

os.makedirs(os.path.join(HERE, "output"), exist_ok=True)

def compact(hits):
    return [[h["M"], h["kappa"], h["t"], h["K"], h["Y"], h["N"],
             h["Omega"], h["omega"], 1 if h["type"] == "branch" else 0]
            for h in hits]

hits_Omega_ge5 = FULL["hits_Omega_ge5"] + STRIP["hits_Omega_ge5"]
Omega12 = [h for h in hits_Omega_ge5 if h["Omega"] >= 12]
top_by_t = sorted(FULL["hits"] + STRIP["hits"],
                  key=lambda h: (-h["t"], h["M"]))[:8]
audit = {
    "experiment": "remo-smooth-hit-census-20261118",
    "pin": pins,
    "census_full": {
        "range": "primes 5 <= M <= 1000, complete over all t",
        "n_M": len(full_M),
        "per_M": FULL["per_M"],
        "totals": {
            "n_hits": len(FULL["hits"]),
            "n_blocked": sum(v["n_blocked"]
                             for v in FULL["per_M"].values()),
            "n_cand": sum(v["n_cand"] for v in FULL["per_M"].values()),
            "n_smooth_cand": sum(v["n_smooth_cand"]
                                 for v in FULL["per_M"].values()),
            "max_t_hit": max(v["max_t_hit"]
                             for v in FULL["per_M"].values()),
            "max_N_hit": max(v["max_N_hit"]
                             for v in FULL["per_M"].values()),
        },
        "Omega_hist_hits": FULL["Omega_hist_hits"],
        "Omega_hist_blocked": FULL["Omega_hist_blocked"],
        "omega_hist_hits": FULL["omega_hist_hits"],
        "omega_hist_blocked": FULL["omega_hist_blocked"],
        "max_Omega_hit": FULL["max_Omega_hit"],
        "max_Omega_blocked": FULL["max_Omega_blocked"],
        "s3_violations": FULL["s3_violations"],
        "dead_cand": FULL["dead_cand"],
    },
    "census_strip": {
        "range": "primes 1000 < M <= 2000, complete within t <= 60",
        "n_M": len(strip_M),
        "per_M": STRIP["per_M"],
        "totals": {
            "n_hits": len(STRIP["hits"]),
            "n_blocked": sum(v["n_blocked"]
                             for v in STRIP["per_M"].values()),
            "n_cand": sum(v["n_cand"] for v in STRIP["per_M"].values()),
            "n_smooth_cand": sum(v["n_smooth_cand"]
                                 for v in STRIP["per_M"].values()),
            "max_t_hit": max(v["max_t_hit"]
                             for v in STRIP["per_M"].values()),
            "max_N_hit": max(v["max_N_hit"]
                             for v in STRIP["per_M"].values()),
        },
        "Omega_hist_hits": STRIP["Omega_hist_hits"],
        "Omega_hist_blocked": STRIP["Omega_hist_blocked"],
        "s3_violations": STRIP["s3_violations"],
        "dead_cand": STRIP["dead_cand"],
    },
    "hits_Omega_ge5_count": len(hits_Omega_ge5),
    "hits_Omega_ge12": Omega12,
    "top_by_t": top_by_t,
    "crosschecks": cc,
    "engine_checks": eng,
}
# SPLIT-EXCLUSIVITY machine check: overlap must be 0 (Lemma EXCLUSIVE)
audit["exclusive_overlap"] = {
    "n_branch_and_smooth_full": sum(
        v["n_branch_and_smooth"] for v in FULL["per_M"].values()),
    "n_branch_and_smooth_strip": sum(
        v["n_branch_and_smooth"] for v in STRIP["per_M"].values()),
    "n_hits_full": len(FULL["hits"]),
    "n_hits_strip": len(STRIP["hits"]),
}
# per-class multiplicity + seam violations + strip boundary
from collections import Counter
cfull = Counter((h["M"], h["kappa"]) for h in FULL["hits"])
cstrip = Counter((h["M"], h["kappa"]) for h in STRIP["hits"])
seamv = 0
for h in FULL["hits"] + STRIP["hits"]:
    sb = (h["M"] - 1) * (h["M"] - 2) // (h["M"] + 1)
    if h["t"] > sb:
        seamv += 1
audit["structure"] = {
    "full_n_classes_with_multi_hits": sum(
        1 for n in cfull.values() if n > 1),
    "full_multi_hit_extra": sum(n - 1 for n in cfull.values() if n > 1),
    "strip_n_classes_with_multi_hits": sum(
        1 for n in cstrip.values() if n > 1),
    "strip_multi_hit_extra": sum(n - 1 for n in cstrip.values()
                                 if n > 1),
    "seam_violations": seamv,
    "strip_hits_at_t_cap": sum(1 for h in STRIP["hits"] if h["t"] == 60),
    "full_n_t1_hits": sum(v["n_t1_hits"] for v in FULL["per_M"].values()),
    "strip_n_t1_hits": sum(v["n_t1_hits"] for v in STRIP["per_M"].values()),
    "full_max_ratio_maxN": max(v["ratio_maxN"]
                               for v in FULL["per_M"].values()),
    "strip_max_ratio_maxN": max(v["ratio_maxN"]
                                for v in STRIP["per_M"].values()),
}
# Y-SQUARE machine check (Lemma YSQR): no Y = M^2 state is a smooth hit.
# For prime M the state is t = M-1, kappa = 0, N = M^3 - 1, k0 = M^2-M-1.
from smooth_core import window_blocked
ysqr = {"n_M": 0, "n_smooth": 0, "n_smooth_and_hit": 0}
for M in full_M + strip_M:
    N = M ** 3 - 1
    fac = factorize(N, PLIST_BIG)
    smooth = all(p <= M - 1 for (p, _e) in fac)
    ysqr["n_M"] += 1
    if smooth:
        ysqr["n_smooth"] += 1
        blk = window_blocked(N, M, M * M - M - 1,
                             [(p, e) for (p, e) in fac])
        if not blk:
            ysqr["n_smooth_and_hit"] += 1
audit["ysquare_check"] = ysqr
# shape populations (finite observation)
def shape_ok(r, vmax2):
    fac = factorize(r["N"], PLIST_BIG)
    if fac[0][0] != 2 or fac[0][1] > vmax2:
        return False
    odd = fac[1:]
    return sum(e for (_p, e) in odd) == 3 and \
        all(p % 2 == 1 and p <= r["M"] - 1 for (p, _e) in odd)
pops = {}
for lo, hi, key in [(1, 2, "t_eq_1"), (2, 10, "t_2_9"), (10, 40, "t_10_39"),
                    (40, 10 ** 9, "t_ge_40")]:
    sel = [h for h in FULL["hits"] + STRIP["hits"] if lo <= h["t"] < hi]
    pops[key] = {
        "n": len(sel),
        "Omega_hist": {}, "v1_3odd": 0, "v2_3odd": 0,
        "Omega_ge10": sum(1 for h in sel if h["Omega"] >= 10),
        "max_Omega": max((h["Omega"] for h in sel), default=0),
    }
    for h in sel:
        o = pops[key]["Omega_hist"]
        o[h["Omega"]] = o.get(h["Omega"], 0) + 1
        if shape_ok(h, 1):
            pops[key]["v1_3odd"] += 1
        if shape_ok(h, 2):
            pops[key]["v2_3odd"] += 1
audit["populations"] = pops
# n_smooth_first equality stats per M
eqf = 0
neqf = 0
for M in full_M:
    if FULL["per_M"][str(M)]["n_hit_classes"] == nsf.get(M, 0):
        eqf += 1
    else:
        neqf += 1
eqs = 0
neqs = 0
for M in strip_M:
    if STRIP["per_M"][str(M)]["n_hit_classes"] == nsf.get(M, 0):
        eqs += 1
    else:
        neqs += 1
audit["crosschecks"]["smooth_first_class_count_vs_census"] = {
    "full_equal_M": eqf, "full_unequal_M": neqf,
    "strip_equal_M": eqs, "strip_unequal_M": neqs,
    "note": "unequal means the census found extra classes with a "
            "non-first (later) smooth hit; never fewer",
}
dump(os.path.join(HERE, "output", "audit.json"), audit)
dump(os.path.join(HERE, "output", "hits_full.json"),
     {"rows": compact(FULL["hits"]),
      "row": ["M", "kappa", "t", "K", "Y", "N", "Omega", "omega",
              "is_branch_and_smooth"]})
dump(os.path.join(HERE, "output", "hits_strip.json"),
     {"rows": compact(STRIP["hits"])})
log("outputs written")
print("S3 violations (full+strip): %d + %d" %
      (FULL["s3_violations"], STRIP["s3_violations"]))
print("dead candidates: %d + %d" % (FULL["dead_cand"], STRIP["dead_cand"]))
print("max Omega hit: %d  max Omega blocked: %d  n Omega>=5 hits: %d"
      % (FULL["max_Omega_hit"], FULL["max_Omega_blocked"],
         len(hits_Omega_ge5)))
print("hits full: %d  hits strip: %d" % (len(FULL["hits"]),
                                         len(STRIP["hits"])))
print("crosschecks:", json.dumps(cc)[:600])
