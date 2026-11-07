"""Exact audit: the subdivided-star odd-k terminal polynomial has no contact double root.

Object
------
For integers r = q-3 >= 1 and odd k >= 3 put F_{k,r}(y) = y^k (y-a) + r - y with
a = (r+2)/(r+1).  The negative real roots of T_{k,r}(u) = u^{k+1} + (r+2) u^k
+ (r+1)^k u + r (r+1)^{k+1} correspond to y > 1 with F_{k,r}(y) = 0.

Claim (no contact double root): there is no (r, k odd >= 3, y in (1,a)) with
F = 0 and F' = 0.

Mechanism audited here
----------------------
Tangency implies the quadratic

    (Q)  k (r+1) y^2 - [ (k+1) r (r+1) + (k-1)(r+2) ] y + k r (r+2) = 0

whose discriminant is exactly

    D(r,k) = (Q0 k + P)^2 - 4 R,   Q0 = r^2-2, P = r^2+2r+2, R = r(r+1)(r+2).

If D is not a perfect square then (Q) is irreducible, so the conjugate of the
tangency point is also a root of the rational polynomial encoding F'=0; but F'
has exactly one positive zero.  Hence tangency forces D(r,k) to be a perfect
square.  For r >= 2 a perfect square D forces D = n^2 with (A-n)(A+n) = 4R,
A = Q0 k + P, hence A <= 2R + 1/2 and therefore k <= 2r+5 + (6r+8.5)/(r^2-2)
< 2r+9.  On the other hand M(2r+7) < r-a for r >= 4, where M(k) = max_{1<y<a}
(a-y) y^k, so min F > 0 for every odd k <= 2r+7 and no tangency is possible.

All comparisons below are exact integer / rational arithmetic; no floating
point is used for any verdict.  Floats appear only in the optional numeric
cross-check that is explicitly labelled as non-proof.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from math import isqrt
from pathlib import Path

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)


def q0(r: int) -> int:
    return r * r - 2


def p_of(r: int) -> int:
    return r * r + 2 * r + 2


def rr(r: int) -> int:
    return r * (r + 1) * (r + 2)


def disc_direct(r: int, k: int) -> int:
    """Discriminant of k(r+1)y^2 - [(k+1)r(r+1)+(k-1)(r+2)]y + kr(r+2)."""
    lead = k * (r + 1)
    mid = (k + 1) * r * (r + 1) + (k - 1) * (r + 2)
    const = k * r * (r + 2)
    return mid * mid - 4 * lead * const


def disc_formula(r: int, k: int) -> int:
    a = q0(r) * k + p_of(r)
    return a * a - 4 * rr(r)


def is_square(n: int) -> bool:
    if n < 0:
        return False
    s = isqrt(n)
    return s * s == n


# ---------------------------------------------------------------------------
# M(k) = max_{1<y<a} (a-y) y^k = a^{k+1} k^k / (k+1)^{k+1}
# ---------------------------------------------------------------------------

def no_root_ok(r: int, k: int) -> bool:
    """Exact sufficient certificate: M(k) < r-a, so F > 0 on (1,a)."""
    lhs = pow(r + 2, k + 1) * pow(k, k)
    rhs = (r * r - 2) * pow(r + 1, k) * pow(k + 1, k + 1)
    return lhs < rhs


def roots_certified(r: int, k: int) -> bool:
    """Exact certificate: F(y*) < 0 at y* = k a/(k+1), giving >= 2 roots."""
    lhs = pow(r + 2, k + 1) * pow(k, k)
    coef = r * (k + 1) * (r + 1) - k * (r + 2)
    rhs = coef * pow(r + 1, k) * pow(k + 1, k)
    return lhs > rhs


def ystar(r: int, k: int) -> Fraction:
    return Fraction(k * (r + 2), (k + 1) * (r + 1))


def a_of(r: int) -> Fraction:
    return Fraction(r + 2, r + 1)


def H_exact(r: int, k: int, y: Fraction) -> Fraction:
    return (a_of(r) - y) * y ** k


def Hprime_exact(r: int, k: int, y: Fraction) -> Fraction:
    return k * y ** (k - 1) * (a_of(r) - Fraction(k + 1, k) * y)


def F_exact(r: int, k: int, y: Fraction) -> Fraction:
    return y ** k * (y - a_of(r)) + r - y


def _numeric_minimizer(r: int, k: int) -> float:
    """Float location of the unique critical point of F in (y_*, a); search only."""
    a = (r + 2) / (r + 1)
    lo = k * a / (k + 1)
    hi = a
    for _ in range(200):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        f1 = m1 ** k * (m1 - a) + r - m1
        f2 = m2 ** k * (m2 - a) + r - m2
        if f1 < f2:
            hi = m2
        else:
            lo = m1
    return 0.5 * (lo + hi)


def tangent_no_root(r: int, k: int, y_t: Fraction | None = None) -> bool | None:
    """Exact certificate that F > 0 on (1,a).

    H is concave on [y_**,a), y_* > y_**, so F(y) >= L(y) there for the tangent
    line L of H at any rational y_t in (y_*,a); on (1,y_*], F >= F(y_*).  The
    certificate succeeds when F(y_*) > 0 and min(L(y_*), L(a)) > 0.
    """
    a = a_of(r)
    ys = ystar(r, k)
    if y_t is None:
        y_t = Fraction(_numeric_minimizer(r, k)).limit_denominator(10 ** 7)
    if not (ys < y_t < a):
        return False
    if not (r - ys - H_exact(r, k, ys) > 0):
        return False
    Ht = H_exact(r, k, y_t)
    Hpt = Hprime_exact(r, k, y_t)

    def lower(y: Fraction) -> Fraction:
        return r - y - (Ht + Hpt * (y - y_t))

    return min(lower(ys), lower(a)) > 0


def witness_two_roots(r: int, k: int) -> Fraction | None:
    """Exact rational witness y with F(y) < 0 (implies two distinct real roots)."""
    a = a_of(r)
    ys = ystar(r, k)
    yc = _numeric_minimizer(r, k)
    for den in (10 ** 3, 10 ** 5, 10 ** 7, 10 ** 9):
        cand = Fraction(round(yc * den), den)
        if ys < cand < a and F_exact(r, k, cand) < 0:
            return cand
    return None


def float_min_sign(r: int, k: int) -> int:
    """Float (non-proof) sign of min F, computed in log space to avoid overflow."""
    import math

    a = (r + 2) / (r + 1)
    y = _numeric_minimizer(r, k)
    if y <= 1 or y >= a:
        return 0
    head = r - y
    logE = k * math.log(y) + math.log(a - y)
    if head <= 0:
        return -1
    return 1 if math.log(head) > logE else -1


def twostep_cross_check(rmax: int) -> dict:
    """Independent float check: the exact verdicts agree with the numeric minimum sign."""
    bad = []
    checked = 0
    for r in range(2, rmax + 1):
        row = threshold(r)
        k = row["threshold"]
        if k is None:
            continue
        checked += 1
        if float_min_sign(r, k) >= 0 or float_min_sign(r, k - 2) <= 0:
            bad.append([r, k, float_min_sign(r, k - 2), float_min_sign(r, k)])
    return {"rows": checked, "disagreements": bad}


def check_quadratic_identity(max_r: int = 40, max_k: int = 21) -> dict:
    """Q(y) = (a-y)y - (r-y)((k+1)y-ka) and (r+1)^k F'(y) = G(y), as identities."""
    checked = 0
    for r in range(1, max_r + 1):
        a = a_of(r)
        for k in range(3, max_k + 1, 2):
            for y in (Fraction(1, 3), Fraction(1), Fraction(11, 10), Fraction(6, 5), Fraction(r + 1, r)):
                q = (k * y * y
                     - ((k + 1) * r + (k - 1) * a) * y
                     + k * a * r)
                lhs = (a - y) * y - (r - y) * ((k + 1) * y - k * a)
                if q != lhs:
                    raise AssertionError(f"quadratic identity r={r} k={k} y={y}")
                g = (r + 1) ** k * (y ** (k - 1) * ((k + 1) * y - k * a) - 1)
                g_expanded = (((r + 1) * y) ** (k - 1)
                              * ((k + 1) * (r + 1) * y - k * (r + 2))
                              - (r + 1) ** k)
                if g != g_expanded:
                    raise AssertionError(f"derivative identity r={r} k={k} y={y}")
                checked += 1
    return {"points_checked": checked}


def kappa_upper(r: int) -> int:
    """Explicit odd k with roots certified: 5(r+1)*ceil(log2(r+1)), made odd."""
    n = r.bit_length()          # = ceil(log2(r+1))
    k = 5 * (r + 1) * n
    return k + 1 if k % 2 == 0 else k


def kappa_lower(r: int) -> int:
    """Largest odd k <= r*floor(log2 r); every odd k <= it is certified rootless."""
    k = r * (r.bit_length() - 1)
    return k - 1 if k % 2 == 0 else k


def kappa_two_sided(rmax: int = 400) -> dict:
    """r*floor(log2 r)-1 < kappa(r) <= 5(r+1)ceil(log2(r+1))+1, exact at both ends."""
    violations = []
    rows = 0
    for r in range(4, rmax + 1):
        rows += 1
        ku = kappa_upper(r)
        kl = kappa_lower(r)
        if not roots_certified(r, ku):
            violations.append([r, ku, "upper not certified"])
        if not no_root_ok(r, kl):
            violations.append([r, kl, "lower witness fails"])
    return {
        "r_range": [4, rmax],
        "rows": rows,
        "violations": violations,
        "kappa_upper_1000": kappa_upper(1000),
        "kappa_lower_1000": kappa_lower(1000),
    }


def check_mechanism(max_r: int = 60, max_k: int = 51) -> dict:
    """D(r,k) formula agrees with the coefficient discriminant."""
    n = 0
    for r in range(1, max_r + 1):
        for k in range(3, max_k + 1, 2):
            if disc_direct(r, k) != disc_formula(r, k):
                raise AssertionError(f"disc mismatch r={r} k={k}")
            n += 1
    return {"pairs_checked": n}


def finite_cases() -> dict:
    """r=1,2,3: enumerate the odd k allowed by the bound and test D for squares."""
    rows = {}
    for r in (1, 2, 3):
        if r >= 2:
            bound = Fraction(2 * rr(r), q0(r)) + Fraction(1, 2 * q0(r)) - Fraction(p_of(r), q0(r))
        else:
            bound = None
        squares = []
        tested = []
        for k in range(3, 61, 2):
            if bound is not None and k > bound:
                break
            tested.append(k)
            if is_square(disc_formula(r, k)):
                squares.append(k)
        # for r=1 continue without the (positive) bound: D=(5-k)^2-24 has
        # (k-5-n)(k-5+n)=24, whose solutions are k in {10,12}; scan a wide odd range.
        if r == 1:
            for k in range(3, 2001, 2):
                if k in tested:
                    continue
                if is_square(disc_formula(r, k)):
                    squares.append(k)
        rows[r] = {
            "odd_k_tested": len(tested) + (0 if r != 1 else 1999 - len(tested)),
            "k_range_from_bound": [3, int(bound)] if bound is not None else "all odd <= 1999",
            "square_discriminants": squares,
        }
    return rows


def divisor_check(r: int) -> list[int]:
    """Tangency forces A = Q0 k + P to be a sum a + R/a over divisor pairs of R."""
    R, Q0, P = rr(r), q0(r), p_of(r)
    hits = []
    a = 1
    while a * a <= R:
        if R % a == 0:
            A = a + R // a
            if Q0 > 0 and (A - P) % Q0 == 0:
                k = (A - P) // Q0
                if k >= 3 and k % 2 == 1:
                    hits.append(k)
        a += 1
    return hits


def min_F_positive(r: int, k: int) -> bool:
    return no_root_ok(r, k)


def threshold(r: int, n_cap: int = 200_000) -> dict:
    """Smallest odd k with a certified negative value; the previous odd k must be certified positive.

    The verdicts are the exact integer certificates ``roots_certified`` /
    ``no_root_ok``.  A floating-point log estimate only proposes the candidate
    k, keeping the number of huge-integer comparisons small.
    """
    import math

    def dense(k: int) -> bool:          # certified two roots
        return roots_certified(r, k)

    def sparse(k: int) -> bool:         # certified no roots
        return no_root_ok(r, k)

    def dense_any(k: int) -> bool:
        return dense(k) or witness_two_roots(r, k) is not None

    def sparse_any(k: int) -> bool:
        return sparse(k) or bool(tangent_no_root(r, k))

    def logM(k: int) -> float:
        a = (r + 2) / (r + 1)
        return (k + 1) * math.log(a) + k * math.log(k) - (k + 1) * math.log(k + 1)

    def h(k: int) -> float:             # >0 proposes "two roots"
        a = (r + 2) / (r + 1)
        ystar = k * a / (k + 1)
        return logM(k) - math.log(r - ystar)

    lo, hi = 3.0, 3.0
    while h(hi) <= 0:
        lo = hi
        hi *= 2
        if hi > 2 * n_cap:
            return {"r": r, "q": r + 3, "threshold": None,
                    "status": "not certified below cap"}
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if h(mid) > 0:
            hi = mid
        else:
            lo = mid
    k = max(3, int(hi) | 1)
    while k > 3 and dense(k - 2):
        k -= 2
    while not dense(k):
        k += 2
    # the roots certificate could in principle miss the true boundary; only in
    # that case fall back to an explicit rational witness one step lower.
    if not sparse_any(k - 2) and witness_two_roots(r, k - 2) is not None:
        k -= 2
    if k == 3:
        return {"r": r, "q": r + 3, "threshold": 3,
                "previous_odd": None,
                "previous_odd_certified_rootless": None,
                "status": "threshold is the smallest odd k"}
    if sparse_any(k - 2):
        method = "M-bound" if sparse(k - 2) else "tangent-bound"
        return {"r": r, "q": r + 3, "threshold": k,
                "previous_odd": k - 2,
                "previous_odd_certified_rootless": True,
                "rootless_certificate": method,
                "status": "clean"}
    return {"r": r, "q": r + 3, "threshold": k,
            "previous_odd": k - 2,
            "previous_odd_certified_rootless": False,
            "status": "elementary criteria do not decide"}


def main() -> int:
    results: dict = {"exact_arithmetic": True}

    results["discriminant_identity"] = check_mechanism()
    results["quadratic_and_derivative_identity"] = check_quadratic_identity()

    # 1. r >= 4: M(2r+7) < r-a, exactly.
    bad = []
    scan = 4000
    for r in range(4, scan + 1):
        if not no_root_ok(r, 2 * r + 7):
            bad.append(r)
    results["m_bound"] = {
        "r_range": [4, scan],
        "checked": scan - 3,
        "violations": bad,
    }

    # 2. the elementary analytic bound (documented, not floating point):
    #    a^{k+1} <= exp((k+1)/(r+1)) and 34/(2r+8) < r-4/3 for r >= 4.
    results["analytic_bound_note"] = {
        "argument": "a^(k+1) <= exp((2r+8)/(r+1)) <= exp(16/5) < 34 and "
                    "34/(2r+8) <= 34/16 < r-4/3 for r >= 4",
        "rational_witness": "34/16 < 4 - 4/3",
        "inequality_holds": Fraction(34, 16) < Fraction(4) - Fraction(4, 3),
    }

    # 3. small r
    results["finite_cases_r1_r2_r3"] = finite_cases()

    # 4. independent divisor-sum characterisation (no square-root bound needed)
    hits = {}
    for r in range(1, 301):
        h = divisor_check(r)
        if h:
            hits[r] = h
    results["divisor_sum_hits_r1_r300"] = hits

    # 5. no square discriminant for r >= 4 in the allowed k window
    squares = []
    pairs = 0
    for r in range(4, 201):
        Q0 = q0(r)
        bound = Fraction(2 * rr(r) + 1, 2 * Q0) - Fraction(p_of(r), Q0)
        k = 3
        while k <= bound:
            pairs += 1
            if is_square(disc_formula(r, k)):
                squares.append([r, k])
            k += 2
    results["square_discriminants_r4_r200"] = {
        "pairs_checked": pairs,
        "found": squares,
    }

    # 6. threshold table
    table = []
    undecided = []
    rmax = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    for r in range(2, rmax + 1):
        row = threshold(r)
        table.append(row)
        if row["status"] != "clean":
            undecided.append(row)
    results["threshold_table"] = {
        "r_range": [2, rmax],
        "rows": len(table),
        "undecided": undecided,
        "monotone_nondecreasing": all(
            table[i]["threshold"] <= table[i + 1]["threshold"] for i in range(len(table) - 1)
        ),
        "certificate_mix": {
            m: sum(1 for x in table if x.get("rootless_certificate") == m)
            for m in ("M-bound", "tangent-bound")
        },
        "samples": table[:12] + table[-6:],
        "all_thresholds": {str(x["r"]): x["threshold"] for x in table},
    }

    results["kappa_two_sided"] = kappa_two_sided(400)
    results["float_cross_check"] = twostep_cross_check(rmax)

    OUT.joinpath("no_contact_double_root.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({k: v for k, v in results.items() if k != "threshold_table"}, indent=2, ensure_ascii=False))
    print("threshold rows:", len(table), "undecided:", len(undecided))
    print("monotone:", results["threshold_table"]["monotone_nondecreasing"])
    print("samples:", [(x["r"], x["threshold"]) for x in results["threshold_table"]["samples"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
