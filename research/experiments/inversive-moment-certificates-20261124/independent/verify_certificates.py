#!/usr/bin/env python3
"""Independent exact-arithmetic checker for the inversive-plane moment certificates.

Written from scratch for the independent audit.  Only the Python standard
library is used (fractions.Fraction, math.comb, json, pathlib).

What is checked
---------------
(1) Symbolic expansion of
        P_s(r) = -(r-(s-3))(r-(s-2))(r-s)
    and
        Q(r)   = (r-1)(r-3)(r-4)
    in the binomial basis {1, r, C(r,2), C(r,3)}.  The expansion is done
    symbolically in s (for P_s) by finite differences, not by copying the
    claimed coefficients.  For P_s the result is compared with
        (s(s-3)(s-2), -(s-3)(3s-4), 2(3s-8), -6)
    as a polynomial identity in s; for Q with (-12, 12, -10, 6).

(2) The three closed-form moment identities, as exact polynomial identities:
        Y(2q+2, q)          = -4(q^2-5q-2)
        Y((s-2)q+1, q)      = -q*W(s,q),
            W(s,q)=q(s-1)(s-4)-s(s-2)(s-3)-2
        Y_blocking(2q-1, q) = -2(q-8)(q-1).

(3) Range checks over the claimed ranges, with counts:
      A: 6 <= q <= 200, n = 2q+2
      B: 9 <= q <= 200, 5 <= s <= q-1, n = (s-2)q+1
      C: 9 <= q <= 200, m = 2q-1
    In each case the certificate value is computed from the four moment
    sums (not merely from the closed form), compared with the closed form,
    and required to be negative.  W(s,q)>0 is checked independently.

(4) Sign of P_s on all integers 0..s (s=4..199) and of Q on all integers
    1..q+1 (q=9..200).  Also checks the sign pattern that makes the
    vanishing assumptions essential: P_s(r)<0 for r>s, Q(0)<0.

(5) The 3-design parameters: v=q^2+1, k=q+1, b=q(q^2+1),
    r_1=q(q+1), lambda_2=q+1, lambda_3=1 and the standard consistency
    identities between them.

The script exits 0 iff all checks pass.  Results are written to
output/verification.json (inside independent/).
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"

# --------------------------------------------------------------------------
# Sparse multivariate polynomials with Fraction coefficients.
# A monomial is a tuple of exponents; nvars fixes the length.
# --------------------------------------------------------------------------


class MPoly:
    __slots__ = ("n", "t")

    def __init__(self, n, terms=None):
        self.n = n
        self.t = {}
        if terms:
            for k, v in terms.items():
                v = Fraction(v)
                if v:
                    self.t[tuple(k)] = v

    @classmethod
    def zero(cls, n):
        return cls(n)

    @classmethod
    def one(cls, n):
        return cls(n, {(0,) * n: 1})

    @classmethod
    def const(cls, n, c):
        return cls(n, {(0,) * n: c})

    @classmethod
    def var(cls, n, i):
        e = [0] * n
        e[i] = 1
        return cls(n, {tuple(e): 1})

    def copy(self):
        return MPoly(self.n, dict(self.t))

    def is_zero(self):
        return not self.t

    def __bool__(self):
        return bool(self.t)

    def __add__(self, other):
        if isinstance(other, (int, Fraction)):
            other = MPoly.const(self.n, other)
        if self.n != other.n:
            raise ValueError("different number of variables")
        r = self.copy()
        for k, v in other.t.items():
            r.t[k] = r.t.get(k, Fraction(0)) + v
            if r.t[k] == 0:
                del r.t[k]
        return r

    __radd__ = __add__

    def __neg__(self):
        return MPoly(self.n, {k: -v for k, v in self.t.items()})

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        if isinstance(other, (int, Fraction)):
            return MPoly(self.n, {k: v * other for k, v in self.t.items()})
        if self.n != other.n:
            raise ValueError("different number of variables")
        r = {}
        for k1, v1 in self.t.items():
            for k2, v2 in other.t.items():
                k = tuple(a + b for a, b in zip(k1, k2))
                r[k] = r.get(k, Fraction(0)) + v1 * v2
        return MPoly(self.n, r)

    __rmul__ = __mul__

    def __pow__(self, e):
        if e < 0:
            raise ValueError("negative exponent")
        r = MPoly.one(self.n)
        b = self
        while e:
            if e & 1:
                r = r * b
            b = b * b
            e >>= 1
        return r

    def substitute(self, idx, value):
        """Substitute x_idx = value; returns a polynomial in nvars-1 vars."""
        if not (0 <= idx < self.n):
            raise IndexError(idx)
        value = Fraction(value)
        r = {}
        for k, v in self.t.items():
            c = v * (value ** k[idx])
            if c:
                k2 = k[:idx] + k[idx + 1:]
                r[k2] = r.get(k2, Fraction(0)) + c
        return MPoly(self.n - 1, r)

    def const_value(self):
        if self.n != 0:
            raise ValueError("not a constant polynomial")
        return self.t.get((), Fraction(0))

    def __eq__(self, other):
        if isinstance(other, (int, Fraction)):
            other = MPoly.const(self.n, other)
        return self.n == other.n and self.t == other.t

    def __repr__(self):
        if not self.t:
            return "0"
        return " + ".join(
            f"{v}*x^{k}" for k, v in sorted(self.t.items())
        )


def binom_poly(p: MPoly, k: int) -> MPoly:
    """C(p,k) = p(p-1)...(p-k+1)/k! as an exact polynomial."""
    r = MPoly.one(p.n)
    for i in range(k):
        r = r * (p - i)
    return r * Fraction(1, factorial(k))


# --------------------------------------------------------------------------
# Univariate integer polynomials (ascending coefficients).
# Used for the pointwise non-negativity checks.
# --------------------------------------------------------------------------


def upoly_from_roots(roots, sign=1):
    p = [1]
    for root in roots:
        q = [0] * (len(p) + 1)
        for i, c in enumerate(p):
            q[i + 1] += c
            q[i] -= c * root
        p = q
    return [sign * c for c in p]


def upoly_eval(p, x):
    v = 0
    for c in reversed(p):
        v = v * x + c
    return v


def upoly_to_binom(p):
    """Newton forward expansion p(r)=sum_k d_k C(r,k), d_k=Delta^k p(0)."""
    d = len(p) - 1
    cur = [upoly_eval(p, r) for r in range(d + 1)]
    out = []
    for _ in range(d + 1):
        out.append(cur[0])
        cur = [cur[i + 1] - cur[i] for i in range(len(cur) - 1)]
    return tuple(out)


# --------------------------------------------------------------------------
# Certificate coefficients and the moment functional.
# --------------------------------------------------------------------------


def coeffs_s(s):
    """Claimed coefficients of P_s in the {1,r,C(r,2),C(r,3)} basis."""
    return (
        s * (s - 3) * (s - 2),
        -(s - 3) * (3 * s - 4),
        2 * (3 * s - 8),
        -6,
    )


def coeffs_4():
    return coeffs_s(4)


def coeffs_Q():
    return (-12, 12, -10, 6)


def W(s, q):
    return q * (s - 1) * (s - 4) - s * (s - 2) * (s - 3) - 2


def Y_int(coeffs, n, q):
    """a0*b + a1*(n*r1) + a2*(C(n,2)*lambda2) + a3*C(n,3).

    Here b=q(q^2+1), r1=q(q+1), lambda2=q+1, lambda3=1.
    This is the RHS of the four moment identities, i.e. sum_r P(r) t_r.
    """
    a0, a1, a2, a3 = coeffs
    return (
        a0 * q * (q * q + 1)
        + a1 * n * q * (q + 1)
        + a2 * comb(n, 2) * (q + 1)
        + a3 * comb(n, 3)
    )


def Y_poly(coeffs, n_poly, q_poly):
    """The same functional with polynomial coefficients/arguments."""
    M0 = q_poly * (q_poly * q_poly + 1)
    M1 = n_poly * q_poly * (q_poly + 1)
    M2 = binom_poly(n_poly, 2) * (q_poly + 1)
    M3 = binom_poly(n_poly, 3)
    return coeffs[0] * M0 + coeffs[1] * M1 + coeffs[2] * M2 + coeffs[3] * M3


# --------------------------------------------------------------------------
# Main verification.
# --------------------------------------------------------------------------


def main():
    Q_MAX = 200
    S_MAX = Q_MAX - 1          # s <= q-1 with q <= Q_MAX
    results = {"experiment": "independent verification of moment certificates"}
    failures = []

    def check(cond, label, detail=None):
        if not cond:
            failures.append({"label": label, "detail": detail})
            print(f"FAIL: {label} {detail if detail is not None else ''}")
        return cond

    # ---- (1) symbolic coefficient expansion --------------------------------
    # P_s(r) = -(r-(s-3))(r-(s-2))(r-s), variables (r,s).
    r2 = MPoly.var(2, 0)
    s2 = MPoly.var(2, 1)
    P_sym = -((r2 - (s2 - 3)) * (r2 - (s2 - 2)) * (r2 - s2))
    vals = [P_sym.substitute(0, j) for j in range(4)]  # polys in s
    cur = vals
    diffs = []
    for _ in range(4):
        diffs.append(cur[0])
        cur = [cur[i + 1] - cur[i] for i in range(len(cur) - 1)]
    # diffs are polynomials in s only (nvars=1 after substituting r).
    s1 = MPoly.var(1, 0)
    claimed = (
        s1 * (s1 - 3) * (s1 - 2),
        -(s1 - 3) * (3 * s1 - 4),
        2 * (3 * s1 - 8),
        MPoly.const(1, -6),
    )
    symbolic_coeff_ok = all(
        check(diffs[k] == claimed[k], f"symbolic P_s coefficient a{k}")
        for k in range(4)
    )
    results["symbolic_P_coefficients"] = symbolic_coeff_ok
    results["symbolic_P_coefficients_vector"] = [
        str(x) for x in diffs
    ]

    # Q(r) = (r-1)(r-3)(r-4), univariate.
    r1 = MPoly.var(1, 0)
    Q_sym = (r1 - 1) * (r1 - 3) * (r1 - 4)
    qvals = [Q_sym.substitute(0, j) for j in range(4)]
    cur = qvals
    qdiffs = []
    for _ in range(4):
        qdiffs.append(cur[0])
        cur = [cur[i + 1] - cur[i] for i in range(len(cur) - 1)]
    qclaim = [MPoly.const(0, c) for c in coeffs_Q()]
    symbolic_Q_ok = all(
        check(qdiffs[k] == qclaim[k], f"symbolic Q coefficient a{k}")
        for k in range(4)
    )
    results["symbolic_Q_coefficients"] = symbolic_Q_ok
    results["symbolic_Q_coefficients_vector"] = [
        str(int(x.const_value())) for x in qdiffs
    ]

    # Per-s numerical expansion, as an independent second route.
    coeff_count = 0
    for s in range(4, S_MAX + 1):
        p = upoly_from_roots([s - 3, s - 2, s], -1)
        got = upoly_to_binom(p)
        check(got == coeffs_s(s), f"per-s coefficient expansion s={s}", (got, coeffs_s(s)))
        coeff_count += 1
    results["coefficient_expansions_checked"] = coeff_count

    # ---- (2) symbolic closed-form identities -------------------------------
    # Theorem A: s=4, n=2q+2.
    qA = MPoly.var(1, 0)
    YA = Y_poly(coeffs_4(), 2 * qA + 2, qA)
    A_identity_ok = check(
        YA == -4 * (qA * qA - 5 * qA - 2),
        "symbolic identity A: Y(2q+2,q) = -4(q^2-5q-2)",
        str(YA),
    )
    results["identity_A_symbolic"] = A_identity_ok

    # Theorem B: n=(s-2)q+1, general s.
    qB = MPoly.var(2, 0)
    sB = MPoly.var(2, 1)
    nB = (sB - 2) * qB + 1
    YB = Y_poly(
        (
            sB * (sB - 3) * (sB - 2),
            -(sB - 3) * (3 * sB - 4),
            2 * (3 * sB - 8),
            MPoly.const(2, -6),
        ),
        nB,
        qB,
    )
    WB = qB * (sB - 1) * (sB - 4) - sB * (sB - 2) * (sB - 3) - 2
    B_identity_ok = check(
        YB + qB * WB == 0,
        "symbolic identity B: Y((s-2)q+1,q) = -q*W(s,q)",
        str(YB + qB * WB),
    )
    results["identity_B_symbolic"] = B_identity_ok

    # Theorem C: m=2q-1.
    qC = MPoly.var(1, 0)
    YC = Y_poly(coeffs_Q(), 2 * qC - 1, qC)
    C_identity_ok = check(
        YC == -2 * (qC - 8) * (qC - 1),
        "symbolic identity C: Y_blocking(2q-1,q) = -2(q-8)(q-1)",
        str(YC),
    )
    results["identity_C_symbolic"] = C_identity_ok

    # ---- (3) pointwise non-negativity and range checks ---------------------
    p_nonneg = 0
    p_s_values = 0
    for s in range(4, S_MAX + 1):
        p = upoly_from_roots([s - 3, s - 2, s], -1)
        for rr in range(s + 1):
            v = upoly_eval(p, rr)
            check(v >= 0, f"P_{s}({rr}) >= 0", v)
            p_nonneg += 1
        # P_s(r) < 0 for r > s: this is why t_r=0 for r>s is needed.
        for rr in range(s + 1, Q_MAX + 2):
            v = upoly_eval(p, rr)
            check(v < 0, f"P_{s}({rr}) < 0 (r>s)", v)
            p_s_values += 1
    results["P_nonneg_point_checks"] = p_nonneg
    results["P_negative_outside_checks"] = p_s_values
    results["P_s_max_s"] = S_MAX

    qpoly = upoly_from_roots([1, 3, 4], +1)
    q_nonneg = 0
    for q in range(9, Q_MAX + 1):
        for rr in range(1, q + 2):
            v = upoly_eval(qpoly, rr)
            check(v >= 0, f"Q({rr}) >= 0 for q={q}", v)
            q_nonneg += 1
    check(upoly_eval(qpoly, 0) == -12, "Q(0) = -12 < 0")
    results["Q_nonneg_point_checks"] = q_nonneg
    results["Q_at_zero"] = upoly_eval(qpoly, 0)

    # Theorem A range.
    A_checks = 0
    for q in range(6, Q_MAX + 1):
        n = 2 * q + 2
        y = Y_int(coeffs_4(), n, q)
        check(y == -4 * (q * q - 5 * q - 2), f"A closed form q={q}", y)
        check(y < 0, f"A negativity q={q}", y)
        A_checks += 1
    results["theorem_A_checks"] = A_checks
    results["theorem_A_range"] = [6, Q_MAX]

    # Theorem B range.
    B_checks = 0
    W_checks = 0
    B_n_le_v = 0
    for q in range(9, Q_MAX + 1):
        for s in range(5, q):  # 5 <= s <= q-1
            n = (s - 2) * q + 1
            c = coeffs_s(s)
            y = Y_int(c, n, q)
            check(y == -q * W(s, q), f"B closed form q={q},s={s}", (y, -q * W(s, q)))
            check(y < 0, f"B negativity q={q},s={s}", y)
            check(W(s, q) > 0, f"B W>0 q={q},s={s}", W(s, q))
            check(n <= q * q + 1, f"B n<=v q={q},s={s}", (n, q * q + 1))
            B_checks += 1
            W_checks += 1
            if n <= q * q + 1:
                B_n_le_v += 1
    results["theorem_B_checks"] = B_checks
    results["theorem_B_W_checks"] = W_checks
    results["theorem_B_n_le_v"] = B_n_le_v
    results["theorem_B_range"] = "9<=q<=200, 5<=s<=q-1"

    # Theorem C range.
    C_checks = 0
    for q in range(9, Q_MAX + 1):
        m = 2 * q - 1
        y = Y_int(coeffs_Q(), m, q)
        check(y == -2 * (q - 8) * (q - 1), f"C closed form q={q}", y)
        check(y < 0, f"C negativity q={q}", y)
        check(m <= q * q + 1, f"C m<=v q={q}", (m, q * q + 1))
        C_checks += 1
    results["theorem_C_checks"] = C_checks
    results["theorem_C_range"] = [9, Q_MAX]

    # ---- (4) design parameters --------------------------------------------
    design_checks = 0
    design_ok = True
    for q in range(2, Q_MAX + 1):
        v = q * q + 1
        k = q + 1
        b = q * (q * q + 1)
        r1 = q * (q + 1)
        lam2 = q + 1
        lam3 = 1
        ok = (
            b * k == v * r1
            and r1 * (k - 1) == lam2 * (v - 1)
            and lam2 * (k - 2) == lam3 * (v - 2)
            and b * comb(k, 3) == comb(v, 3) * lam3
            and b == v * (v - 1) * (v - 2) // (k * (k - 1) * (k - 2))
        )
        if not check(ok, f"design parameters q={q}"):
            design_ok = False
        design_checks += 1
    results["design_parameter_checks"] = design_checks
    results["design_parameters_ok"] = design_ok

    # ---- summary -----------------------------------------------------------
    results["status"] = "PASS" if not failures else "FAIL"
    results["failures"] = failures
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "verification.json").write_text(
        json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(results, indent=1, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
