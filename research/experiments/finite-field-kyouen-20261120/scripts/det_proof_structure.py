"""Exact decomposition of D(a) = max |Delta| over the lattice square.

Mathematical content
====================

Let a = n-1, Q = [0,a]^2, and for four points p1,p2,p3,p4 in Q

    Delta(p1,p2,p3,p4) = det[[x_i, y_i, x_i^2+y_i^2, 1]] .

Expanding along the last row r = (x, y, x^2+y^2, 1):

    Delta(x,y) = alpha*x + beta*y + gamma*(x^2+y^2) + delta          (L)

with, for the triple (p1,p2,p3),

    alpha = -M_1,  beta = M_2,  gamma = -M_3,  delta = M_4,

M_j being the 3x3 minor of the three rows with column j deleted.  In particular

    gamma = -det[[x_i,y_i,1]]  = -2 * signed area(p1,p2,p3),
    delta =  det[[x_i,y_i,x_i^2+y_i^2]] = Delta(p1,p2,p3,(0,0)).

Because (L) has no xy term it is a *radial* quadratic:

    L(x,y) = gamma * ( (x-h)^2 + (y-k)^2 ) + c0,
    (h,k) = (-alpha/(2 gamma), -beta/(2 gamma)) = circumcentre,
    c0    = delta - (alpha^2+beta^2)/(4 gamma).

Hence, writing d(P) = |P-(h,k)|^2, the function |L| = |gamma| * |d - R^2| is a
function of d alone, monotone on each side of d = R^2.  Therefore

  * over the CONTINUUM square Q,  max |L| = max( |L| at the 4 corners,
                                                 |L| at the point of Q nearest (h,k) );
  * over the LATTICE points of Q, max |L| = max( |L| at the 4 corners,
                                                 |L| at the lattice point of Q
                                                      nearest (h,k) ).

Consequently

    D(a) = max( A(a), B(a) ),

    A(a) = max over triples of |Delta(triple, corner)|   (corner branch),
    B(a) = max over triples of |L(nearest lattice point)| (interior branch).

This script computes A(a), B(a), D(a) exactly (integer arithmetic) and also the
continuous relaxation max, for a range of a.  It also verifies the coefficient
formula against the direct 4x4 determinant.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np


# --------------------------------------------------------------------------
# exact coefficient formula, checked against the direct determinant
# --------------------------------------------------------------------------
def det3(m) -> int:
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def det4(rows) -> int:
    """Expansion along the last column (index 3): sign (-1)^(i+3)."""
    total = 0
    for i in range(4):
        minor = [rows[j][:3] for j in range(4) if j != i]
        total += (1 if (i + 3) % 2 == 0 else -1) * det3(minor)
    return total


def lifted(p):
    x, y = p
    return (x, y, x * x + y * y, 1)


def coeffs(p1, p2, p3):
    rows = [lifted(p1), lifted(p2), lifted(p3)]
    out = []
    for j in range(4):
        minor = [[rows[r][c] for c in range(4) if c != j] for r in range(3)]
        out.append((1 if (3 + j) % 2 == 0 else -1) * det3(minor))
    return tuple(out)


def verify_coeffs(a: int) -> bool:
    pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
    for tri in itertools.combinations(pts, 3):
        al, be, ga, de = coeffs(*tri)
        for p4 in pts:
            if p4 in tri:
                continue
            x, y = p4
            pred = al * x + be * y + ga * (x * x + y * y) + de
            direct = det4([lifted(p) for p in tri] + [lifted(p4)])
            if pred != direct:
                return False
    return True


# --------------------------------------------------------------------------
# exact analysis of one a
# --------------------------------------------------------------------------
def analyse(a: int, want_continuous: bool = True):
    xs = np.arange(a + 1, dtype=np.int64)
    Xg, Yg = np.meshgrid(xs, xs, indexing="ij")
    X = Xg.ravel()
    Y = Yg.ravel()
    S = X * X + Y * Y
    n = X.size
    corners = [(0, 0), (a, 0), (0, a), (a, a)]

    A_max = 0
    A_arg = None
    B_max = 0
    B_arg = None
    C_max = 0.0
    C_arg = None

    for i in range(n):
        x1 = int(X[i]); y1 = int(Y[i]); s1 = int(S[i])
        for j in range(i + 1, n):
            x2 = int(X[j]); y2 = int(Y[j]); s2 = int(S[j])

            # gamma, alpha, beta, delta are affine in (X, Y, S) for fixed p1,p2
            gx = -(y1 - y2); gy = (x1 - x2); g0 = -(x1 * y2 - y1 * x2)
            ay = -(s1 - s2); as_ = (y1 - y2); a0 = -(y1 * s2 - s1 * y2)
            bx = (s1 - s2); bs = -(x1 - x2); b0 = (x1 * s2 - s1 * x2)
            dx = (y1 * s2 - s1 * y2); dy = -(x1 * s2 - s1 * x2); ds = (x1 * y2 - y1 * x2)

            gamma = gx * X + gy * Y + g0
            alpha = ay * Y + as_ * S + a0
            beta = bx * X + bs * S + b0
            delta = dx * X + dy * Y + ds * S

            # ---- corner branch (exact) ----
            for (cx, cy) in corners:
                v = np.abs(alpha * cx + beta * cy + gamma * (cx * cx + cy * cy) + delta)
                k = int(np.argmax(v))
                m = int(v[k])
                if m > A_max:
                    A_max = m
                    A_arg = ((i, j, k), (cx, cy))

            nz = gamma != 0
            if not nz.any():
                continue

            gf = gamma.astype(np.float64)
            hf = -alpha.astype(np.float64) / (2.0 * gf)
            kf = -beta.astype(np.float64) / (2.0 * gf)

            # ---- interior branch, lattice: nearest lattice point (exact) ----
            nx0 = np.clip(np.rint(hf), 0, a).astype(np.int64)
            ny0 = np.clip(np.rint(kf), 0, a).astype(np.int64)
            best = np.zeros(n, dtype=np.int64)
            for ox in (-1, 0, 1):
                for oy in (-1, 0, 1):
                    px = np.clip(nx0 + ox, 0, a)
                    py = np.clip(ny0 + oy, 0, a)
                    v = np.abs(alpha * px + beta * py + gamma * (px * px + py * py) + delta)
                    v = np.where(nz, v, 0)
                    best = np.maximum(best, v)
            k = int(np.argmax(best))
            m = int(best[k])
            if m > B_max:
                B_max = m
                B_arg = ((i, j, k), (int(nx0[k]), int(ny0[k])))

            # ---- continuous relaxation (float, for exploration) ----
            if want_continuous:
                hc = np.clip(hf, 0.0, float(a))
                kc = np.clip(kf, 0.0, float(a))
                v = np.abs(gamma.astype(np.float64) * (hc * hc + kc * kc)
                           + alpha.astype(np.float64) * hc
                           + beta.astype(np.float64) * kc
                           + delta.astype(np.float64))
                v = np.where(nz, v, 0.0)
                k = int(np.argmax(v))
                if float(v[k]) > C_max:
                    C_max = float(v[k])
                    C_arg = ((i, j, k), (float(hc[k]), float(kc[k])))

    D = max(A_max, B_max)
    return {
        "a": a,
        "A_corner": A_max,
        "A_arg": A_arg,
        "B_nearest": B_max,
        "B_arg": B_arg,
        "D_lattice": D,
        "formula": a * a * ((a * a) // 2),
        "match": D == a * a * ((a * a) // 2),
        "D_continuous_float": C_max,
        "C_arg": C_arg,
        "continuous_target_a4_over_2": Fraction(a ** 4, 2),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=list(range(1, 13)))
    ap.add_argument("--verify-a", type=int, default=4)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    print("=" * 84)
    print("(0) coefficient formula  Delta(x,y) = alpha x + beta y + gamma(x^2+y^2) + delta")
    ok = verify_coeffs(args.verify_a)
    print(f"    verified against the direct 4x4 determinant for a={args.verify_a}: {ok}")

    print()
    print("=" * 84)
    print("(1) exact decomposition  D(a) = max( A(a), B(a) )")
    print(f"{'a':>3} {'A corner':>11} {'B nearest':>11} {'D lattice':>11} "
          f"{'a^2*floor(a^2/2)':>17} {'ok':>4} {'cont.max':>12} {'a^4/2':>10}")
    report = []
    for a in args.a:
        r = analyse(a)
        report.append(r)
        print(f"{a:>3} {r['A_corner']:>11} {r['B_nearest']:>11} {r['D_lattice']:>11} "
              f"{r['formula']:>17} {'OK' if r['match'] else 'FAIL':>4} "
              f"{r['D_continuous_float']:>12.3f} {float(r['continuous_target_a4_over_2']):>10.1f}")
        print(f"      argmax A: {r['A_arg']}")
        print(f"      argmax B: {r['B_arg']}")
        print(f"      argmax cont: {r['C_arg']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
