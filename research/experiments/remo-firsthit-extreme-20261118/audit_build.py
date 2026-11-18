#!/usr/bin/env python3
"""K0959 deterministic audit builder: first-hit extreme-value
decomposition for primes M <= 2000 (all finite observations).

Reads (pinned by sha256):
  ../remo-prehit-mechanism-20261118/output/audit.json (K0956, F_by_M)
  ../remo-prehit-mechanism-20261118/output/firsthit_rows.json (K0956)

Output: output/audit.json (byte-identical on rerun).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from composite_core import sigma_Z  # pinned engine
from extr_core import (power_fit, through_origin_fit, median,
                       spearman)

HERE = os.path.dirname(os.path.abspath(__file__))
K0956 = os.path.join(HERE, "..", "remo-prehit-mechanism-20261118",
                     "output")
T0 = time.time()


def log(m):
    print("[%5.1fs] %s" % (time.time() - T0, m), flush=True)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


pins = {
    "audit.json": sha256_file(os.path.join(K0956, "audit.json")),
    "firsthit_rows.json": sha256_file(
        os.path.join(K0956, "firsthit_rows.json")),
}
k = json.load(open(os.path.join(K0956, "audit.json")))
rows = json.load(open(os.path.join(K0956, "firsthit_rows.json")))
fbm = k["firsthit"]["F_by_M"]  # 303 rows
log("loaded K0956 outputs (303 F rows, %d class rows)" % len(rows))

A = {"experiment": "remo-firsthit-extreme-20261118", "pin": pins}

# ------------------------------------------------ 1. F identity checks

ident = {"n": 0, "identity_fail": 0, "type_branch": 0,
         "kappa_even": 0, "monotone_violations": 0, "max_F": 0,
         "n_Ft2": 0}
prev = None
for r in fbm:
    M = r["M"]
    ident["n"] += 1
    if r["F"] != (M + 1) * r["F_t"] + r["F_kappa"]:
        ident["identity_fail"] += 1
    if r["F_type"] == "branch":
        ident["type_branch"] += 1
    if r["F_kappa"] % 2 == 0:
        ident["kappa_even"] += 1
    if prev is not None and r["F"] < prev:
        ident["monotone_violations"] += 1
    prev = r["F"]
    ident["max_F"] = max(ident["max_F"], r["F"])
    if r["F_t"] == 2:
        ident["n_Ft2"] += 1
A["identity"] = ident
log("identity checks done")

# ---------------------------------------- 2. flattening surrogate table

grids = {
    "M_le_199": [r for r in fbm if r["M"] <= 199],
    "M_le_2000": [r for r in fbm],
    "200_to_2000": [r for r in fbm if 200 <= r["M"] <= 2000],
}
fits = {}
for gname, g in grids.items():
    xs = [r["M"] for r in g]
    ys = [r["F"] for r in g]
    a, beta, r2 = power_fit(xs, ys)
    entry = {"n": len(g), "alpha": round(a, 4),
             "beta": round(beta, 4), "r2": round(r2, 4)}
    # surrogate recovery: power-fit the pure surrogate M ln^d M
    entry["surrogate_beta"] = {}
    for d in (1.0, 1.5, 1.8, 2.0):
        _a, b2, _r = power_fit(
            xs, [x * math.log(x) ** d for x in xs])
        entry["surrogate_beta"]["ln^%.1f" % d] = round(b2, 4)
    # one-parameter log-law fits through origin
    entry["law_fits"] = {}
    # log-space slope-1 law fits: log F = log alpha + log(M ln^d M)
    entry["loglaw_fits"] = {}
    for d in (1.0, 1.5, 1.8, 2.0):
        ll = [math.log(x * math.log(x) ** d) for x in xs]
        ly = [math.log(y) for y in ys]
        ml = sum(ll) / len(ll)
        my2 = sum(ly) / len(ly)
        alpha = math.exp(my2 - ml)
        ssr = sum((v - (math.log(alpha) + l)) ** 2
                  for v, l in zip(ly, ll))
        sst = sum((v - my2) ** 2 for v in ly)
        entry["loglaw_fits"]["M_ln^%.1f" % d] = {
            "alpha": round(alpha, 4), "r2": round(1.0 - ssr / sst, 4)}
    for d in (1.0, 1.5, 1.8, 2.0):
        law = (lambda x, d=d: x * math.log(x) ** d)
        alpha, r2l = through_origin_fit(xs, ys, law)
        entry["law_fits"]["M_ln^%.1f" % d] = {
            "alpha": round(alpha, 4), "r2": round(r2l, 4)}
    fits[gname] = entry
A["fits"] = fits
log("fits done: %s" % json.dumps(fits))

# ---------------------------------------------- 3. bucket medians

buckets = [(2, 50), (50, 100), (100, 200), (200, 500),
           (500, 1000), (1000, 2001)]
bm = {}
for lo, hi in buckets:
    sel = [r for r in fbm if lo <= r["M"] < hi]
    v1 = [r["F_t"] / math.log(r["M"]) ** 2 for r in sel]
    v2 = [r["F"] / (r["M"] * math.log(r["M"])) for r in sel]
    bm["%d_%d" % (lo, hi)] = {
        "n": len(sel),
        "median_Ft_over_ln2": round(median(v1), 4),
        "median_F_over_MlnM": round(median(v2), 4),
    }
A["bucket_medians"] = bm
log("bucket medians: %s" % json.dumps(bm))

# ------------------------------------- 4. worst-class structure

Cs = [r["F_C"] for r in fbm]
chist = {}
for c in Cs:
    chist[str(c)] = chist.get(str(c), 0) + 1
A["worst_class"] = {
    "C_hist": chist,
    "C_is_half": sum(1 for r in fbm
                     if r["F_C"] == (r["M"] + 1) // 2
                     or r["F_C"] == (r["M"] + 1) / 2),
    "kappa_over_M": {
        "median": round(median([r["F_kappa"] / r["M"] for r in fbm]), 4),
        "max": round(max(r["F_kappa"] / r["M"] for r in fbm), 4),
        "zero_count": sum(1 for r in fbm if r["F_kappa"] == 0),
    },
    "Ft2_M": [r["M"] for r in fbm if r["F_t"] == 2],
}
log("worst-class structure done")

# ------------------------------- 5. BH worst-class identification

by_M = {}
for r in rows:
    by_M.setdefault(r["M"], []).append(r)
bhw = {"n_M": 0, "argmax_agree": 0, "worst_norm_rank": [],
       "top3_overlap": [], "spearman_pooled": None,
       "spearman_top_decile": None}
all_t = []
all_s = []
top_t = []
top_s = []
for M, rs in sorted(by_M.items()):
    if len(rs) < 3:
        continue
    bhw["n_M"] += 1
    rs2 = sorted(rs, key=lambda r: (-r["t_first"], r["kappa"]))
    obs_worst = rs2[0]
    rs3 = sorted(rs, key=lambda r: (-r["t_star"], r["kappa"]))
    if rs3[0]["kappa"] == obs_worst["kappa"]:
        bhw["argmax_agree"] += 1
    n = len(rs)
    rank = next(i for i, r in enumerate(rs3)
                if r["kappa"] == obs_worst["kappa"])
    bhw["worst_norm_rank"].append(rank / (n - 1))
    o3 = {r["kappa"] for r in rs2[:3]}
    s3 = {r["kappa"] for r in rs3[:3]}
    bhw["top3_overlap"].append(len(o3 & s3))
    ts = [r["t_first"] for r in rs]
    ss = [r["t_star"] for r in rs]
    all_t.extend(ts)
    all_s.extend(ss)
    # top decile per M (largest classes only)
    k10 = max(3, n // 10)
    idx = sorted(range(n), key=lambda i: -ts[i])[:k10]
    top_t.extend(ts[i] for i in idx)
    top_s.extend(ss[i] for i in idx)
bhw["worst_norm_rank_median"] = round(
    median(bhw["worst_norm_rank"]), 4)
bhw["worst_norm_rank_mean"] = round(
    sum(bhw["worst_norm_rank"]) / len(bhw["worst_norm_rank"]), 4)
bhw["top3_overlap_mean"] = round(
    sum(bhw["top3_overlap"]) / len(bhw["top3_overlap"]), 4)
bhw["spearman_pooled"] = round(spearman(all_t, all_s), 4)
bhw["spearman_top_decile"] = round(spearman(top_t, top_s), 4)
bhw.pop("worst_norm_rank", None)
bhw.pop("top3_overlap", None)
A["bh_worst"] = bhw
log("BH worst-class: %s" % json.dumps(bhw))

# --------------------------- 6. extreme-value amplification (M<=199)

ev = {"n_M": 0, "rows": []}
nl = {r["M"]: r["n_live"] for r in fbm}
for M, rs in sorted(by_M.items()):
    ts = [r["t_first"] for r in rs]
    if len(ts) < 5:
        continue
    tstar = max(ts)
    med = median(ts)
    # iid-exponential baseline: max/median ~ ln(2n)/ln 2
    base = math.log(2 * len(ts)) / math.log(2)
    ev["rows"].append({
        "M": M, "n": len(ts), "t_max": tstar,
        "t_median": med, "amp": round(tstar / med, 4),
        "baseline": round(base, 4),
        "excess": round(tstar / med / base, 4),
    })
ev["n_M"] = len(ev["rows"])
ev["median_excess"] = round(median([r["excess"] for r in ev["rows"]]), 4)
ev["mean_excess"] = round(
    sum(r["excess"] for r in ev["rows"]) / len(ev["rows"]), 4)
A["extreme_value"] = ev
log("extreme-value done (n_M=%d, median excess %.3f)"
    % (ev["n_M"], ev["median_excess"]))

# ------------------------------------- 7. engine anchor on F rows

eng = {"n": 0, "fail": 0}
for r in fbm:
    eng["n"] += 1
    if sigma_Z(r["M"], r["F"]) != 1:
        eng["fail"] += 1
A["engine_F_anchor"] = eng
log("engine F anchor: %d checks, %d failures" % (eng["n"], eng["fail"]))

os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
with open(os.path.join(HERE, "output", "audit.json"), "w") as f:
    json.dump(A, f, sort_keys=True, separators=(",", ":"))
    f.write("\n")
log("output written")
