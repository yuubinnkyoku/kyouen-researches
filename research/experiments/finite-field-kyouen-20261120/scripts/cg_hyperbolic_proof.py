"""Verify the substitution chain that proves every non-degenerate char-2 member is hyperbolic.

Claim: for q = 2^m and Q = H + rho*L0 + tau*L1 with H = X0X3+X1X2, L0 = X0X1+X2^2,
L1 = X1^2+X2X3, rho*tau != 1, there is a linear substitution (explicit below)
carrying Q to Y0*Y3 + tau*X1^2 + (1+rho*tau)*X1*X2 + rho*X2^2, and the binary
form tau*X1^2 + (1+rho*tau)*X1*X2 + rho*X2^2 is equivalent to X1*X2 because
Tr(tau*rho/(1+tau*rho)^2) = Tr(u + u^2) = 0.

This script checks both steps numerically over F_8 and F_16.

Run:  python cg_hyperbolic_proof.py --q 8 16
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_prime_power import FiniteField, factorize, find_irreducible  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    args = ap.parse_args()

    for q in args.q:
        p, m = factorize(q)[0]
        assert p == 2
        F = FiniteField(p, m, find_irreducible(p, m))
        elems = list(F.elements())
        one = F.pow(elems[0], 0)
        zero = F.sub(one, one)
        mul, add = F.mul, F.add

        def trace(x):
            acc = zero
            cur = x
            for _ in range(m):
                acc = add(acc, cur)
                cur = mul(cur, cur)
            return acc

        def Qf(rho, tau, X):
            x0, x1, x2, x3 = X
            acc = add(mul(x0, x3), mul(x1, x2))                      # H
            acc = add(acc, mul(rho, add(mul(x0, x1), mul(x2, x2))))  # rho L0
            acc = add(acc, mul(tau, add(mul(x1, x1), mul(x2, x3))))  # tau L1
            return acc

        def M_apply(rho, tau, y):
            """the substitution chain of the proof, written out explicitly"""
            y0, y1, y2, y3 = y
            # step 2: X0 = Y0 + tau*X2
            X0 = add(y0, mul(tau, y2))
            X1 = y1
            X2 = y2
            # step 3 applied first in the derivation: Y3 = Y3' + tau^2 X2 + tau Y0
            Y3 = add(add(y3, mul(mul(tau, tau), y2)), mul(tau, y0))
            # step 1: X3 = Y3 + rho*X1 + tau*X0   (with X0 already substituted)
            X3 = add(add(Y3, mul(rho, X1)), mul(tau, X0))
            return (X0, X1, X2, X3)

        ok = 0
        bad = 0
        binary_ok = 0
        binary_bad = 0
        trials = 0
        for rho in elems:
            for tau in elems:
                if mul(rho, tau) == one:      # degenerate member
                    continue
                trials += 1
                # step (a): Q(M y) == y0*y3 + tau*y1^2 + (1+rho tau) y1 y2 + rho y2^2
                good = True
                for y in itertools.product(elems, repeat=4):
                    lhs = Qf(rho, tau, M_apply(rho, tau, y))
                    y0, y1, y2, y3 = y
                    rhs = add(mul(y0, y3),
                              add(mul(tau, mul(y1, y1)),
                                  add(mul(add(one, mul(rho, tau)), mul(y1, y2)),
                                      mul(rho, mul(y2, y2)))))
                    if lhs != rhs:
                        good = False
                        break
                if good:
                    ok += 1
                else:
                    bad += 1
                    if bad <= 3:
                        print(f"q={q}: chain mismatch at rho={rho} tau={tau}")
                # step (b): the trace condition for the binary form
                x = mul(tau, rho)
                denom = mul(add(one, x), add(one, x))
                t = trace(mul(x, F.div(one, denom))) if not F.is_zero(denom) else None
                if t is not None and F.is_zero(t):
                    binary_ok += 1
                else:
                    binary_bad += 1
                    print(f"q={q}: trace condition fails at rho={rho} tau={tau}")
        print(f"q={q}: {trials} non-degenerate members; chain verified {ok}, failed {bad}; "
              f"trace condition holds {binary_ok}, fails {binary_bad}", flush=True)


if __name__ == "__main__":
    main()
