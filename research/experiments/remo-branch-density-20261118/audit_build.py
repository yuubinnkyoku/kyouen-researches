#!/usr/bin/env python3
"""K0953 audit build: cold, deterministic battery over every machine
claim of this experiment.  Writes output/branch_density_audit.json
(byte-identical across cold reruns; run twice and compare sha256).

Checks:
  BRANCH-EXACT     engine sigma_Z vs K0952 branch union on
                  M in primes<=13, all live kappa, t in [t0,120].
  ALL-ADM         O(1) fixed-prime-divisor scan (obstructed) for all
                  admissible branches of all live classes, primes M<=199,
                  q<=1000; plus nu_pair full-scan cross-check on a
                  fixed subset (seeded LCG, no RNG dependency).
  OBSTRUCT-VALIDATE  obstructed(q) == (nu_pair(q)==q) on the subset.
  SS-FORM         nu_case closed form == nu_pair brute force,
                  q<=1000, all branches of M<=60 live classes;
                  singular_series vs census ss_cached on spot classes.
  SS-ANCHORS      SS_2 = 3.960971..., SS_3 = 5.281295... (K0950).
  U_M-ANCHORS     M=3 exact 3658 @1e5, 25860 @1e6, M=2 2025 @66666,
                  7751 @333333 (K0950/K0952 published counts, with the
                  kappa=0, t=1 special-hit caveat), BH ratio band.
  CENSUS-ANCHORS  per-M exact totals == published CENSUS-REPRO (8/8).
  STARVATION/FIRSTHIT  digests of the stage outputs + headline stats.
"""
from __future__ import annotations
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "remo-hit-prime-pair-20261118"))
from branch_density_core import (Branches, primes_upto, is_prime,
                                 nu_pair, nu_case, obstructed,
                                 singular_series, sieve_set)
from composite_core import sigma_Z
from census_starvation import ss_cached, ss_base

OUT = os.path.join(HERE, "output", "branch_density_audit.json")
Q_MAX = 1000
Q_SMALL = 1000


def _lcg(n: int, mod: int) -> list[int]:
    """Deterministic pseudo-sample: first n draws of x = 48271*x % (2^31-1)."""
    xs = []
    x = 20261118
    for _ in range(n):
        x = 48271 * x % 2147483647
        xs.append(x % mod)
    return xs


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def branch_exact() -> dict:
    """All kappa (live and dead), M in primes<=13, t in [t0,120]:
    engine sigma_Z(M,(M+1)t+kappa)==1 must equal the branch-union hit
    predicate (which is FALSE for every dead class in this window)."""
    states = hits = mismatches = 0
    for M in primes_upto(13):
        t0 = max(M, 3)
        for kap in range(M - 1):
            br = Branches(M, kap)
            for t in range(t0, 121):
                states += 1
                eng = sigma_Z(M, (M + 1) * t + kap) == 1
                brh = False
                for e in br.e_list:
                    if (t - br.t_e[e]) % e:
                        continue
                    Y = (M + 1) * t + kap + 1
                    P = (br.A * t + br.B) // e
                    if is_prime(Y) and P * e == br.A * t + br.B \
                            and is_prime(P):
                        brh = True
                        break
                if eng != brh:
                    mismatches += 1
                if eng:
                    hits += 1
    return {"states": states, "hits": hits, "mismatches": mismatches}


def all_adm() -> dict:
    prs = [q for q in primes_upto(Q_MAX)]
    n_classes = n_branches = 0
    violations = 0
    subset = []          # (M, kappa, e) sampled for nu_pair cross-check
    for M in primes_upto(199):
        for kap in range(M - 1):
            if math.gcd(kap + 1, M + 1) != 1:
                continue
            n_classes += 1
            br = Branches(M, kap)
            for e in br.e_list:
                n_branches += 1
                a1, c1 = (M + 1) * e, br.c1[e]
                a2, c2 = br.A, br.c2[e]
                for q in prs:
                    if obstructed(q, a1, c1, a2, c2):
                        violations += 1
                subset.append((M, kap, e))
    # seeded subset of 1200 branches for the O(q) cross-check
    idx = _lcg(1200, len(subset))
    seen = set()
    n_nu_checks = n_obst_mismatch = 0
    for i in idx:
        if i in seen:
            continue
        seen.add(i)
        M, kap, e = subset[i]
        br = Branches(M, kap)
        a1, c1 = (M + 1) * e, br.c1[e]
        a2, c2 = br.A, br.c2[e]
        for q in primes_upto(200):
            n_nu_checks += 1
            if obstructed(q, a1, c1, a2, c2) != (nu_pair(q, a1, c1,
                                                        a2, c2) == q):
                n_obst_mismatch += 1
    return {"live_classes": n_classes, "branches": n_branches,
            "q_max": Q_MAX, "fixed_divisor_violations": violations,
            "nu_pair_cross_checks": n_nu_checks,
            "nu_pair_vs_obstructed_mismatches": n_obst_mismatch}


def ss_form() -> dict:
    n_branches = mismatches = 0
    for M in primes_upto(60):
        for kap in range(M - 1):
            if math.gcd(kap + 1, M + 1) != 1:
                continue
            br = Branches(M, kap)
            for e in br.e_list:
                n_branches += 1
                a1, c1 = (M + 1) * e, br.c1[e]
                a2, c2 = br.A, br.c2[e]
                for q in primes_upto(Q_SMALL):
                    if nu_case(q, M, kap, e, br.C, br.A) != \
                            nu_pair(q, a1, c1, a2, c2):
                        mismatches += 1
    # spot numeric: singular_series (nu_case product, actual kappa)
    # vs census ss_cached (SS-STRUCT closed form, kappa only via C)
    spots = 0
    spot_max_rel = 0.0
    prs = primes_upto(200000)
    for (M, kap) in ((7, 0), (7, 2), (13, 10), (31, 0), (31, 30),
                     (61, 0), (97, 0), (199, 0)):
        br = Branches(M, kap)
        for e in br.e_list:
            v1 = singular_series(br, e, prs)
            v2 = ss_cached(M, br.C, e)
            rel = abs(v1 - v2) / v2
            spot_max_rel = max(spot_max_rel, rel)
            spots += 1
    return {"branches": n_branches, "q_max": Q_SMALL,
            "nu_case_vs_nu_pair_mismatches": mismatches,
            "spot_ss_checks": spots, "spot_max_rel_diff": spot_max_rel}


def ss_anchors() -> dict:
    prs = primes_upto(2_000_000)
    ss2 = singular_series(Branches(2, 0), 1, prs)
    ss3 = singular_series(Branches(3, 0), 1, prs)
    return {"SS2": round(ss2, 6), "SS3": round(ss3, 6),
            "SS2_published": 3.960971, "SS3_published": 5.281295}


def um_anchors() -> dict:
    d = json.load(open(os.path.join(HERE, "output", "um_sweep.json")))
    rows = {}
    for r in d["um_sweep"]:
        key = (r["M"], r["U"])
        if key in rows:
            assert rows[key]["exact_total"] == r["exact_total"]
        rows[key] = r
    checks = []
    # K0950/K0952 published U_M counts; the M=2 machine counts include
    # the special (s,kappa)=(0,0) hit at t=1 that the census-style
    # convention excludes, hence anchor = published + 1 there.
    for M, U, want, note in ((3, 100000, 3658, "published 3658"),
                             (3, 1000000, 25860, "published 25860"),
                             (2, 66666, 2025, "published 2024 +1 special"),
                             (2, 333333, 7751, "published 7750 +1 special")):
        r = rows[(M, U)]
        checks.append({"M": M, "U": U, "exact": r["exact_total"],
                       "anchor": want, "note": note,
                       "match": r["exact_total"] == want})
    ratios = [r["ratio_exact_over_pred"] for r in d["um_sweep"]]
    return {"anchor_checks": checks,
            "n_sweep_rows": len(d["um_sweep"]),
            "n_seam_states": sum(r["seam_states"] for r in d["um_sweep"]),
            "n_seam_mismatch": sum(r["seam_mismatch"] for r in d["um_sweep"]),
            "bh_ratio_min": round(min(ratios), 4),
            "bh_ratio_max": round(max(ratios), 4),
            "bh_ratio_in_095_1025":
                all(0.95 <= x <= 1.025 for x in ratios)}


def census_anchors() -> dict:
    d = json.load(open(os.path.join(HERE, "output", "census.json")))
    rows = list(d["census"].values())
    return {"n_M": len(rows),
            "all_match": all(r["match"] for r in rows),
            "totals": {r["M"]: [r["exact_total"], r["published_total"]]
                       for r in rows},
            "ratio_min": round(min(r["ratio_exact_over_pred"]
                                   for r in rows), 4),
            "ratio_max": round(max(r["ratio_exact_over_pred"]
                                   for r in rows), 4)}


def stage_digests() -> dict:
    out = {}
    for name in ("um_sweep.json", "census.json", "starvation.json",
                 "firsthit_pred.json"):
        p = os.path.join(HERE, "output", name)
        out[name] = sha256_file(p) if os.path.exists(p) else None
    st = json.load(open(os.path.join(HERE, "output", "starvation.json")))
    fh = json.load(open(os.path.join(HERE, "output",
                                     "firsthit_pred.json")))
    rows = fh["rows"]
    out["firsthit_headline"] = {
        "n_classes": len(rows),
        "n_pre_tail_first_hits": sum(r["pre_tail"] for r in rows),
        "n_t_hat_finite": sum(r["t_hat"] is not None for r in rows),
    }
    ss = st["starvation"]["sparse_summary"]
    out["starvation_headline"] = ss
    return out


def main() -> None:
    audit = {
        "experiment": "remo-branch-density-20261118",
        "branch_exact": branch_exact(),
        "all_adm": all_adm(),
        "ss_form": ss_form(),
        "ss_anchors": ss_anchors(),
        "um_anchors": um_anchors(),
        "census_anchors": census_anchors(),
        "stage_digests": stage_digests(),
    }
    ok = (audit["branch_exact"]["mismatches"] == 0
          and audit["all_adm"]["fixed_divisor_violations"] == 0
          and audit["all_adm"]["nu_pair_vs_obstructed_mismatches"] == 0
          and audit["ss_form"]["nu_case_vs_nu_pair_mismatches"] == 0
          and audit["ss_form"]["spot_max_rel_diff"] <= 1e-4
          and audit["ss_anchors"]["SS2"] == audit["ss_anchors"]["SS2_published"]
          and audit["ss_anchors"]["SS3"] == audit["ss_anchors"]["SS3_published"]
          and all(c["match"] for c in audit["um_anchors"]["anchor_checks"])
          and audit["um_anchors"]["n_seam_mismatch"] == 0
          and audit["census_anchors"]["all_match"]
          and audit["um_anchors"]["bh_ratio_in_095_1025"])
    audit["all_ok"] = ok
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(audit, f, indent=1, sort_keys=True)
    print("wrote", OUT, "all_ok =", ok)


if __name__ == "__main__":
    main()
