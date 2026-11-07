"""Audit the two-term asymptotic law kappa(r) = 2r ln r + r ln ln r + (1+ln2) r + o(r).

The kappa values used in the residual table are the exact certificates of the
companion experiment (``graph-star-subdivided-star-no-contact-double-root-20261107``);
several are recomputed here and the two new large values r = 3000, 10000 are
computed from scratch.  Floating point is used only to display ratios and to
propose candidate k; every verdict comes from an exact integer certificate
(``no_root_ok`` / ``roots_certified``).
"""
from __future__ import annotations

import json
import math
import sys
from decimal import Decimal, getcontext
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIBLING = HERE.parent / "graph-star-subdivided-star-no-contact-double-root-20261107"
sys.path.insert(0, str(SIBLING))
import verify_no_contact_double_root as base  # noqa: E402

OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
getcontext().prec = 60

CSTAR = 1.0 + math.log(2.0)


def k_candidate(r: int, c: float) -> int:
    """Odd k near 2r ln r + r ln ln r + c r (float proposal only)."""
    lr = math.log(r)
    llr = math.log(lr)
    k = int(2.0 * r * lr + r * llr + c * r)
    return k + 1 if k % 2 == 0 else k


def model(r: int) -> float:
    lr = math.log(r)
    return 2.0 * r * lr + r * math.log(lr) + CSTAR * r


def decimal_ln_m(k: int, r: int) -> Decimal:
    a = Decimal(r + 2) / Decimal(r + 1)
    return ((Decimal(k + 1) * a.ln()) + (Decimal(k) * Decimal(k).ln())
            - (Decimal(k + 1) * Decimal(k + 1).ln()))


def estimate_bounds(k: int, r: int) -> tuple[Decimal, Decimal]:
    m = Decimal(k + 1) / Decimal(r + 1)
    lower = m - Decimal(k + 1) / (2 * Decimal(r + 1) ** 2) - Decimal(k + 1).ln() - 1
    upper = m - Decimal(k + 1).ln() - 1 + Decimal(1) / (2 * Decimal(k))
    return lower, upper


def main() -> int:
    results: dict = {"exact_arithmetic_for_verdicts": True,
                     "c_star": CSTAR}

    kappa: dict[int, int] = {}
    prev = SIBLING / "output" / "no_contact_double_root.json"
    if prev.exists():
        data = json.loads(prev.read_text(encoding="utf-8"))
        kappa = {int(k): v for k, v in data["threshold_table"]["all_thresholds"].items()}

    # re-verify a sample of the imported table and add two new exact values
    sample = [2, 3, 17, 101, 503, 997]
    recheck = {}
    for r in sample:
        got = base.threshold(r)["threshold"]
        recheck[str(r)] = {"imported": kappa.get(r), "recomputed": got,
                           "agrees": kappa.get(r) == got}
        kappa[r] = got
    for r in (3000, 10000):
        kappa[r] = base.threshold(r)["threshold"]
    results["recheck_sample"] = recheck
    results["new_large_values"] = {"3000": kappa[3000], "10000": kappa[10000]}

    rows = []
    for r in sorted(kappa):
        if r < 4:
            continue
        k = kappa[r]
        pred = model(r)
        resid = k - pred
        rows.append({
            "r": r,
            "kappa": k,
            "ratio_kappa_over_r_ln_r": k / (r * math.log(r)),
            "predicted_2rlnr_plus_rlnlnr": pred,
            "residual": resid,
            "residual_over_r": resid / r,
        })
    results["residual_table"] = {
        "rows": len(rows),
        "residual_over_r_monotone_decreasing": all(
            rows[i]["residual_over_r"] >= rows[i + 1]["residual_over_r"] - 1e-12
            for i in range(len(rows) - 1)
        ),
        "samples": [rows[i] for i in (0, 1, 5, 20, 96, len(rows) - 6, len(rows) - 3,
                                      len(rows) - 2, len(rows) - 1)],
        "min_residual_over_r": min(x["residual_over_r"] for x in rows),
        "max_residual_over_r": max(x["residual_over_r"] for x in rows),
    }

    # spot checks: below the predicted threshold (rootless) and above it (two roots)
    spot = {}
    for r in (3000, 10000):
        low = k_candidate(r, 1.2)
        high = k_candidate(r, 2.5)
        spot[str(r)] = {
            "k_low": low,
            "k_low_rootless": base.no_root_ok(r, low),
            "k_high": high,
            "k_high_two_roots": base.roots_certified(r, high),
        }
    results["threshold_bracket"] = spot

    # numeric audit of the two-sided log estimate (not a proof)
    checks = []
    worst = Decimal(0)
    for r in (5, 10, 100, 1000, 10000):
        for c in (-1.0, 0.0, 1.0, 2.0):
            k = k_candidate(r, c)
            if k < 3:
                continue
            lnm = decimal_ln_m(k, r)
            lower, upper = estimate_bounds(k, r)
            gap = max(lower - lnm, lnm - upper)
            worst = max(worst, gap)
            checks.append({"r": r, "k": k,
                           "lnM_inside_bounds": lower < lnm < upper,
                           "max_gap": str(gap)})
    results["two_sided_estimate_audit"] = {
        "points": len(checks),
        "all_inside": all(x["lnM_inside_bounds"] for x in checks),
        "worst_gap": str(worst),
        "precision_digits": 60,
    }

    OUT.joinpath("kappa_asymptotic.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in results.items()
                      if k not in ("residual_table",) }, indent=2, ensure_ascii=False))
    print("residual summary:", json.dumps(
        {k: v for k, v in results["residual_table"].items() if k != "samples"},
        ensure_ascii=False))
    print("residual samples:")
    for x in results["residual_table"]["samples"]:
        print(f"  r={x['r']:>6} kappa={x['kappa']:>8} ratio={x['ratio_kappa_over_r_ln_r']:.4f}"
              f" residual/r={x['residual_over_r']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
