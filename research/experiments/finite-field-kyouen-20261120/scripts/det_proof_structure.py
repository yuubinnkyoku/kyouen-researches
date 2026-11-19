"""Structural lemmas for the D(n) upper bound  |Delta| <= a^2 * floor(a^2/2).

Notation.  a = n-1, Q = [0,a]^2 (the lattice square), and for four lattice
points p1,p2,p3,p4 in Q

    Delta(p1,p2,p3,p4) = det[[x_i, y_i, x_i^2+y_i^2, 1]] .

Expanding along the last row r = (x, y, x^2+y^2, 1) gives

    Delta(x,y) = alpha*x + beta*y + gamma*(x^2+y^2) + delta          (L)

with

    alpha = -M_1,  beta = M_2,  gamma = -M_3,  delta = M_4,

where M_j is the 3x3 minor of the first three rows with column j deleted.
In particular

    gamma = -det[[x_i,y_i,1]] = -2 * signed area(p1,p2,p3),
    delta =  det[[x_i,y_i,x_i^2+y_i^2]] = Delta(0,0).

Consequences verified here
--------------------------
(S1) L has no xy term, hence is a *radial* quadratic:
         L(x,y) = gamma * ( (x-h)^2 + (y-k)^2 ) + c0,
     with (h,k) = (-alpha/(2 gamma), -beta/(2 gamma)) the circumcentre and
     c0 = delta - gamma (h^2+k^2).  (For gamma = 0, L is affine.)

(S2) Therefore, over the *continuum* square Q, |L| is maximised either at a
     corner of Q or at the point of Q closest to (h,k).

(S3) Over the *lattice* points of Q, |L| is maximised either at a corner of Q
     or at the lattice point of Q closest to (h,k).

(S4) The "maximum is attained on the boundary" statement in DET_MAX_TRIPLE.md
     is FALSE for |Delta|: for the corner triple (0,0),(a,0),(0,a) the function
     is L = a^2 (a(x+y) - x^2 - y^2), whose absolute value is maximal at the
     centre (a/2,a/2) with value a^4/2, not on the boundary.  This script
     exhibits that counterexample explicitly.

(S5) Consequently the correct decomposition of D(a) is
         D(a) = max( A(a), B(a) )
     where
         A(a) = max over triples of max over the 4 corners of |L(c)|
              = max over triples of |det[[x_i,y_i,x_i^2+y_i^2]]|
                (corner case; by the dihedral symmetry of Q all four corners
                 give the same maximum),
         B(a) = max over triples of |L(P*)|,  P* = lattice point of Q closest
                to the circumcentre (h,k).

This script verifies (S1)-(S5) numerically and computes D(a), A(a), B(a)
exactly for a range of a.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


# --------------------------------------------------------------------------
# exact linear algebra
# --------------------------------------------------------------------------
def det3(m) -> int:
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def det4(rows) -> int:
    total = 0
    for i in range(4):
        minor = [rows[j][:3] for j in range(4) if j != i]
        total += (1 if i % 2 == 0 else -1) * det3(minor)
    return total


def lifted(p):
    x, y = p
    return (x, y, x * x + y * y, 1)


def coeffs(p1, p2, p3):
    """(alpha, beta, gamma, delta) with Delta(x,y) = a x + b y + c(x^2+y^2) + d."""
    rows = [lifted(p1), lifted(p2), lifted(p3)]
    coef = []
    for j in range(4):
        minor = [[rows[r][c] for c in range(4) if c != j] for r in range(3)]
        coef.append((1 if (3 + j) % 2 == 0 else -1) * det3(minor))
    return tuple(coef)


def eval_L(coef, x, y):
    alpha, beta, gamma, delta = coef
    return alpha * x + beta * y + gamma * (x * x + y * y) + delta


# --------------------------------------------------------------------------
# nearest lattice point of Q to a rational point
# --------------------------------------------------------------------------
def clamp_int(v: Fraction, a: int) -> int:
    """Nearest integer in [0,a] to the rational v (ties broken either way)."""
    n = round(v)          # Fraction.__round__ -> int, ties to even
    if n < 0:
        return 0
    if n > a:
        return a
    return n


def nearest_lattice(h: Fraction, k: Fraction, a: int):
    return clamp_int(h, a), clamp_int(k, a)


# --------------------------------------------------------------------------
# (S1) radial structure
# --------------------------------------------------------------------------
def check_radial(trials) -> bool:
    """L(x,y) = gamma*((x-h)^2+(y-k)^2) + c0 with h,k rational."""
    for (p1, p2, p3) in trials:
        alpha, beta, gamma, delta = coeffs(p1, p2, p3)
        if gamma == 0:
            continue
        h = Fraction(-alpha, 2 * gamma)
        k = Fraction(-beta, 2 * gamma)
        c0 = delta - gamma * (h * h + k * k)
        for (x, y) in [(0, 0), (1, 0), (0, 1), (3, 2), (5, 5)]:
            lhs = eval_L((alpha, beta, gamma, delta), x, y)
            rhs = gamma * ((x - h) ** 2 + (y - k) ** 2) + c0
            if lhs != rhs:
                return False
    return True


# --------------------------------------------------------------------------
# (S2)/(S3) max over the square / over the lattice points
# --------------------------------------------------------------------------
def max_over_lattice_exact(coef, a: int):
    """Exact max of |L| over the lattice points of Q, plus the argmax."""
    alpha, beta, gamma, delta = coef
    best, arg = -1, None
    for x in range(a + 1):
        for y in range(a + 1):
            v = abs(eval_L(coef, x, y))
            if v > best:
                best, arg = v, (x, y)
    return best, arg


def max_over_lattice_formula(coef, a: int):
    """max(|L| at the 4 corners, |L| at the lattice point closest to (h,k))."""
    alpha, beta, gamma, delta = coef
    corners = [(0, 0), (a, 0), (0, a), (a, a)]
    best, arg = -1, None
    for c in corners:
        v = abs(eval_L(coef, *c))
        if v > best:
            best, arg = v, c
    if gamma != 0:
        h = Fraction(-alpha, 2 * gamma)
        k = Fraction(-beta, 2 * gamma)
        ps = nearest_lattice(h, k, a)
        v = abs(eval_L(coef, *ps))
        if v > best:
            best, arg = v, ps
    return best, arg


def max_over_continuum_formula(coef, a: int):
    """max(|L| at the 4 corners, |L| at the point of Q closest to (h,k))."""
    alpha, beta, gamma, delta = coef
    corners = [(0, 0), (a, 0), (0, a), (a, a)]
    best, arg = -1, None
    for c in corners:
        v = abs(eval_L(coef, *c))
        if v > best:
            best, arg = v, c
    if gamma != 0:
        h = Fraction(-alpha, 2 * gamma)
        k = Fraction(-beta, 2 * gamma)
        hc = min(max(h, Fraction(0)), Fraction(a))
        kc = min(max(k, Fraction(0)), Fraction(a))
        v = abs(gamma * ((hc - h) ** 2 + (kc - k) ** 2)
                + delta - gamma * (h * h + k * k))
        if v > best:
            best, arg = v, (hc, kc)
    return best, arg


# --------------------------------------------------------------------------
# decomposition of D(a)
# --------------------------------------------------------------------------
def analyse(a: int, verbose: bool = False):
    pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
    corners = [(0, 0), (a, 0), (0, a), (a, a)]
    D = 0
    A = 0
    B = 0
    argD = argA = argB = None
    for tri in itertools.combinations(pts, 3):
        coef = coeffs(*tri)
        # corner part
        cbest, carg = -1, None
        for c in corners:
            v = abs(eval_L(coef, *c))
            if v > cbest:
                cbest, carg = v, c
        if cbest > A:
            A, argA = cbest, (tri, carg)
        # nearest-lattice part
        alpha, beta, gamma, delta = coef
        nbest = -1
        if gamma != 0:
            h = Fraction(-alpha, 2 * gamma)
            k = Fraction(-beta, 2 * gamma)
            ps = nearest_lattice(h, k, a)
            nbest = abs(eval_L(coef, *ps))
        if nbest > B:
            B, argB = nbest, (tri, None)
        m = max(cbest, nbest)
        if m > D:
            D, argD = m, (tri, carg if cbest >= nbest else "nearest")
    return {
        "a": a,
        "D": D,
        "A_corner": A,
        "B_nearest": B,
        "formula": a * a * ((a * a) // 2),
        "match": D == a * a * ((a * a) // 2),
        "argD": argD,
        "argA": argA,
        "argB": argB,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=list(range(1, 13)))
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    print("=" * 78)
    print("(S1) radial structure  L = gamma*((x-h)^2+(y-k)^2) + c0")
    a0 = 6
    pts0 = [(x, y) for y in range(a0 + 1) for x in range(a0 + 1)]
    trials = list(itertools.combinations(pts0, 3))
    print(f"    triples tested (a={a0}): {len(trials)}   radial: {check_radial(trials)}")

    print()
    print("=" * 78)
    print("(S2)/(S3) max over lattice points = max(corners, nearest lattice point)")
    ok_lat = ok_cont = True
    for a in range(1, 8):
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        for tri in itertools.combinations(pts, 3):
            coef = coeffs(*tri)
            b1, _ = max_over_lattice_exact(coef, a)
            b2, _ = max_over_lattice_formula(coef, a)
            if b1 != b2:
                ok_lat = False
                print(f"    LATTICE MISMATCH a={a} tri={tri} {b1} vs {b2}")
            # continuum: compare with a dense rational grid
            b3, _ = max_over_continuum_formula(coef, a)
            grid = 0
            N = 24
            for i in range(N + 1):
                for j in range(N + 1):
                    x = Fraction(i * a, N)
                    y = Fraction(j * a, N)
                    v = abs(eval_L(coef, x, y))
                    if v > grid:
                        grid = v
            if grid > b3:
                ok_cont = False
                print(f"    CONTINUUM MISMATCH a={a} tri={tri} grid={grid} formula={b3}")
    print(f"    lattice formula correct for a<=7:  {ok_lat}")
    print(f"    continuum formula correct for a<=7: {ok_cont}")

    print()
    print("=" * 78)
    print("(S4) counterexample to 'max is attained on the boundary'")
    a = 6
    coef = coeffs((0, 0), (a, 0), (0, a))
    print(f"    triple (0,0),(a,0),(0,a), a={a}:  coefficients {coef}")
    print(f"    L(x,y) = {coef[2]}*(x^2+y^2) + {coef[0]}*x + {coef[1]}*y + {coef[3]}")
    print(f"    L(0,0)={eval_L(coef,0,0)}  L(a,0)={eval_L(coef,a,0)}  "
          f"L(0,a)={eval_L(coef,0,a)}  L(a,a)={eval_L(coef,a,a)}")
    print(f"    L(a/2,a/2) = {eval_L(coef, Fraction(a,2), Fraction(a,2))}  "
          f"= a^4/2 = {Fraction(a**4,2)}")
    print(f"    -> |L| is maximal at the CENTRE, not on the boundary.")

    print()
    print("=" * 78)
    print("(S5) exact decomposition  D(a) = max(A(a), B(a))")
    print(f"{'a':>3} {'D(a)':>12} {'A corner':>12} {'B nearest':>12} "
          f"{'a^2*floor(a^2/2)':>18}  match")
    report = []
    for a in args.a:
        r = analyse(a)
        report.append(r)
        print(f"{a:>3} {r['D']:>12} {r['A_corner']:>12} {r['B_nearest']:>12} "
              f"{r['formula']:>18}  {'OK' if r['match'] else 'MISMATCH'}")
        print(f"      argmax D: triple={r['argD'][0]} at {r['argD'][1]}")
        print(f"      argmax A: triple={r['argA'][0]} at {r['argA'][1]}")
        if r['argB'][0] is not None:
            print(f"      argmax B: triple={r['argB'][0]}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False,
                                       default=str), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
