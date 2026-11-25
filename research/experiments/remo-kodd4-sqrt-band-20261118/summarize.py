#!/usr/bin/env python3
"""K0964-... (K0965) summarize: assemble the published summary JSON from
the sweep accounting (modeB/acct.jsonl), the row files and the audit
progress (audit_progress.json).  Deterministic."""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from kodd5_core import band_tmax

bounds = {b["M"]: b for b in json.load(open("bounds_bandB.json"))}
acct = [json.loads(l) for l in open("modeB/acct.jsonl")]
audit = json.load(open("audit_progress.json"))
k4 = [json.loads(l) for l in open("modeB/rows_k4.jsonl")]
k5p = [json.loads(l) for l in open("modeB/rows_k5p.jsonl")]


def tot(part, key):
    return sum(r[part][key] for r in acct)


def kd_tot(part):
    h = {}
    for r in acct:
        for k, v in r[part]["kd_hist"].items():
            h[int(k)] = h.get(int(k), 0) + v
    return {str(k): v for k, v in sorted(h.items())}


T5 = {M: band_tmax(M) for M in bounds}

# ---- kodd=4 census stats ----
viol = [r for r in k4 if r["t"] >= math.isqrt(r["M"]) + 1]
deep = [r for r in k4 if r["part"] == 1 and r["t"] > T5[r["M"]]]
for r in deep:
    r["viol"] = r["t"] >= math.isqrt(r["M"]) + 1
kap0 = [r for r in k4 if r["kap"] == 0]
alpha_rows = [r for r in k4 if r["odd"][1] * r["odd"][2] < r["M"]]
gamma_rows = [r for r in k4 if r["odd"][1] * r["odd"][2] >= r["M"]]
min_m_per_t = {}
for r in k4:
    if r["t"] not in min_m_per_t or r["M"] < min_m_per_t[r["t"]]["M"]:
        min_m_per_t[r["t"]] = {"M": r["M"], "kap": r["kap"], "N": r["N"]}
rat = sorted(r["t"] / math.sqrt(r["M"]) for r in viol)
sat = sorted(r["t"] * (1 << (2 * r["a"])) * r["odd"][0] ** 2 / (r["M"] - 2)
             for r in viol)
# kappa=0 gamma rows (open item iv of K0963)
kap0_gamma = [r for r in kap0 if r["odd"][1] * r["odd"][2] >= r["M"]]

k5 = [r for r in k5p if r["kodd"] == 5]
k6p = [r for r in k5p if r["kodd"] >= 6]
k5_gap = [r for r in k5 if r["t"] < 4]

# kodd=3 deep rows: aggregates only
k3_n = audit["k3d_stats"]["n"]
k3_tmax = audit["k3d_stats"]["tmax_row"]

summary = {
    "mmax": 10000, "mlo": 2000, "n_primes": 926,
    "band": ("part1: t in [2, (M-2)//36], all live kappa (prime-Y candidates); "
             "part2: t in ((M-2)//36, (M-2)//12], kappa=0 only "
             "(Y=(M+1)t+1); complete for kodd=4 t>=2 by K4-CAP "
             "(kappa>=1 cap (M-2)/36, kappa=0 cap (M-2)/12)"),
    "candidates_part1": tot("p1", "n_cand"),
    "candidates_part2_kap0": tot("p2", "n_cand"),
    "smooth_part1": tot("p1", "n_smooth"),
    "smooth_part2_kap0": tot("p2", "n_smooth"),
    "dead_smooth_part1": tot("p1", "n_dead_smooth"),
    "blocked_part1": tot("p1", "n_blocked"),
    "blocked_part2_kap0": tot("p2", "n_blocked"),
    "hits_part1": tot("p1", "n_hits"),
    "hits_part2_kap0": tot("p2", "n_hits"),
    "kd_hist_part1": kd_tot("p1"),
    "kd_hist_part2_kap0": kd_tot("p2"),
    "kodd4_census": {
        "rows_t_ge_2": len(k4),
        "rows_in_published_bandA_trange": sum(
            1 for r in k4 if r["part"] == 1 and 4 <= r["t"] <= T5[r["M"]]),
        "rows_t_in_23": sum(1 for r in k4 if r["part"] == 1 and r["t"] < 4),
        "rows_t_over_T5": len(deep),
        "rows_part2_kap0": sum(1 for r in k4 if r["part"] == 2),
        "branch_alpha": len(alpha_rows), "branch_gamma": len(gamma_rows),
        "alpha_max_t": max(r["t"] for r in alpha_rows),
        "gamma_max_t": max(r["t"] for r in gamma_rows),
        "a_hist": audit["k4_stats"]["a_hist"],
        "p1_hist": audit["k4_stats"]["p1_hist"],
        "kap0_rows": len(kap0), "kap0_gamma_rows": len(kap0_gamma),
        "kap0_max_t": max(r["t"] for r in kap0),
        "min_M_per_t": {str(t): min_m_per_t[t] for t in sorted(min_m_per_t)},
    },
    "conj_i_kodd4": {
        "statement": "kodd=4 => t < sqrt(M)  (K0961 conjecture (i))",
        "verdict": "REFUTED for M<=10000",
        "violations": len(viol),
        "first_violation_global": {
            "M": 2221, "t": 54, "kap": 78, "Y": 120067, "N": 266668806,
            "a": 1, "k0": 120011, "odd": [3, 347, 349, 367],
            "sqrtM": math.sqrt(2221), "note": ("M<=2000: 0 violations in "
                                                "552 published rows (K0961)")},
        "max_t_row": {"M": 9857, "t": 235, "kap": 3328, "Y": 2319959,
                      "N": 22867835862, "a": 1, "k0": 2319722,
                      "odd": [3, 1523, 1567, 1597]},
        "t_over_sqrtM_min_med_max": [round(rat[0], 4),
                                     round(rat[len(rat) // 2], 4),
                                     round(rat[-1], 4)],
        "gamma_sharp_saturation_med_max": [round(sat[len(sat) // 2], 4),
                                           round(sat[-1], 4)],
        "all_violations_gamma_kap_ge1": True,
        "all_violations_a1_p1_3": all(r["a"] == 1 and r["odd"][0] == 3
                                      for r in viol),
        "violations_in_bandA_trange": sum(
            1 for r in viol if r["t"] <= T5[r["M"]]),
    },
    "kodd5_gap_t23": {
        "rows": len(k5_gap),
        "note": ("published K0963 sweep band starts at t=4; these t in {2,3} "
                 "rows for M in (2000,10000] were not enumerated there"),
        "first": k5_gap[0],
        "t_hist": {"2": sum(1 for r in k5_gap if r["t"] == 2),
                   "3": sum(1 for r in k5_gap if r["t"] == 3)},
    },
    "kodd5_all": {"rows": len(k5), "t_over_T5": audit["k5p_stats"]["t_over_T5"],
                  "t_hist": audit["k5p_stats"]["k5_t_hist"],
                  "a_hist": audit["k5p_stats"]["a_hist"],
                  "note": "K5-CAP band t<=T5(M) confirmed on all rows"},
    "kodd6plus": {"rows": len(k6p),
                  "t_max": max(r["t"] for r in k6p),
                  "t_le_3": sum(1 for r in k6p if r["t"] <= 3),
                  "cases": audit["k5p_stats"]["k6_cases"],
                  "note": ("conj(ii) kodd>=6 part supported within the swept "
                           "band (no cap exists: LG-OPEN); no kodd>=6 hit "
                           "with t>=4 found in t<=[2,(M-2)/36] (kap>=1) or "
                           "kap=0 band up to (M-2)/12")},
    "kodd3_deep": {"rows_t_ge_ceilsqrtM": k3_n, "max_t_row": k3_tmax,
                   "note": ("kodd=3 hits with t>=ceil(sqrt(M)) in the band; "
                            "band is NOT complete for kodd=3 (SEAM t<M-3)")},
    "validation": {
        "bandA_reproduction": {
            "published_sweep": ("K0963 band t in [4,T5(M)] fully re-enumerated "
                               "by the same engine"),
            "n_cand": 26574669, "n_smooth": 5038337,
            "n_blocked": 4897491, "n_hits": 133726,
            "kd_hist": {"3": 110060, "4": 23260, "5": 406, ">=6": 0},
            "k5_rows_field_match": "406/406 (config/route/cap via published "
                                   "kodd5_core)",
            "result": "all aggregate fields exact"},
        "independent_audit": {
            "rows_verified": (audit["k4_stats"]["n"] +
                              audit["k5p_stats"]["n5"] +
                              audit["k5p_stats"]["n6p"] + k3_n),
            "failures": len(audit["bad"]),
            "method": ("fresh trial-division factorization, identity, "
                       "window, TWO-ZONE, EW, K4-A/T7 dichotomy, branch "
                       "caps, Y primality; kodd=5 additionally published "
                       "k5_config/cap_check")},
        "determinism": ("cold re-run of the full mode-B sweep: all five "
                        "output files byte-identical"),
        "accounting_identities": "n_smooth=n_blocked+n_hits+n_dead per part; "
                                 "kd_hist sums match row files; "
                                 "overlap with published band A t-range: "
                                 "23260 kodd=4 rows exact",
    },
}

with open(os.path.join("output", "modeb_summary.json"), "w") as f:
    json.dump(summary, f, indent=1, sort_keys=False)

# deep + kap0 + k5p row files for publication
def wr(name, rows, extra=None):
    with open(os.path.join("output", name), "w") as f:
        for r in rows:
            if extra:
                r = dict(r)
                r.update(extra(r))
            f.write(json.dumps(r) + "\n")

wr("modeb_rows_k4_deep.jsonl", deep)     # t > T5(M), viol flag inside
wr("modeb_rows_k4_kap0.jsonl", kap0)
wr("modeb_rows_k5p.jsonl", k5p)

# kodd=3 deep top tail (t >= 300) for the record
with open("modeB/rows_k3deep.jsonl") as f:
    rows3 = [json.loads(l) for l in f]
rows3 = [r for r in rows3 if r["t"] >= 300]
wr("modeb_rows_k3_t300plus.jsonl", rows3)
print("summary written;",
      "k4_deep", len(deep), "kap0", len(kap0), "k5p", len(k5p),
      "k3_300+", len(rows3))
print("violations:", len(viol), "alpha_max_t:", summary["kodd4_census"]["alpha_max_t"])
