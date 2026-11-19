"""Continuous relaxation of the D(a) bound, and the key geometric lemma.

Findings from det_proof_structure.py (exact, a <= 12):

  * D(a) = max(A(a), B(a)) where A is the corner branch and B the
    nearest-lattice-point branch, and both equal a^2*floor(a^2/2).
  * The CONTINUOUS maximum of |Delta| over the square is exactly a^4/2,
    attained by three corners + the centre of the square.

Since a^2*floor(a^2/2) = a^4/2 for even a and (a^4-a^2)/2 for odd a, the
continuous statement

    (CT)   |Delta| <= a^4/2   for all four points in the continuum square Q

implies the claim for even a, and gives a^2/2 of slack for odd a.

This script
  (1) numerically maximises |Delta| over Q^4 (multi-start local optimisation)
      and reports the maximiser, confirming (CT) and its extremal family;
  (2) tests the KEY LEMMA used in the proof of (CT):
        for a triangle with vertices in Q and circumcentre c in Q,
        Area * R^2 <= a^4/4 ;
  (3) tests the corner branch over the continuum.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


def delta(p1, p2, p3, p4) -> float:
    rows = np.array([[p[0], p[1], p[0] ** 2 + p[1] ** 2, 1.0]
                     for p in (p1, p2, p3, p4)])
    return float(np.linalg.det(rows))


def delta_vec(v) -> float:
    pts = [(v[0], v[1]), (v[2], v[3]), (v[4], v[5]), (v[6], v[7])]
    return delta(*pts)


def circumcentre(p1, p2, p3):
    """Centre and squared radius of the circle through three points."""
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    d = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-14:
        return None, None
    a2 = ax * ax + ay * ay
    b2 = bx * bx + by * by
    c2 = cx * cx + cy * cy
    ux = (a2 * (by - cy) + b2 * (cy - ay) + c2 * (ay - by)) / d
    uy = (a2 * (cx - bx) + b2 * (ax - cx) + c2 * (bx - ax)) / d
    r2 = (ax - ux) ** 2 + (ay - uy) ** 2
    return (ux, uy), r2


def triangle_area(p1, p2, p3) -> float:
    return 0.5 * abs((p2[0] - p1[0]) * (p3[1] - p1[1])
                     - (p3[0] - p1[0]) * (p2[1] - p1[1]))


# --------------------------------------------------------------------------
# (1) maximise |Delta| over Q^4
# --------------------------------------------------------------------------
def maximise_delta(a: float, starts: int, seed: int):
    rng = np.random.default_rng(seed)
    best = 0.0
    best_v = None
    for _ in range(starts):
        v0 = rng.uniform(0.0, a, size=8)
        res = minimize(lambda v: -abs(delta_vec(v)), v0, method="Nelder-Mead",
                       options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000})
        val = abs(delta_vec(res.x))
        if val > best:
            best, best_v = val, res.x.copy()
    return best, best_v


# --------------------------------------------------------------------------
# (2) the key lemma: Area * R^2 <= a^4/4 for circumcentre in Q
# --------------------------------------------------------------------------
def check_key_lemma(a: float, samples: int, seed: int):
    rng = np.random.default_rng(seed)
    worst = 0.0
    worst_tri = None
    for _ in range(samples):
        tri = rng.uniform(0.0, a, size=(3, 2))
        c, r2 = circumcentre(*tri)
        if c is None:
            continue
        if not (0.0 <= c[0] <= a and 0.0 <= c[1] <= a):
            continue
        val = triangle_area(*tri) * r2
        if val > worst:
            worst, worst_tri = val, (tri.copy(), c, r2)
    return worst, worst_tri


def check_key_lemma_grid(a: float, n: int):
    """Deterministic scan over a grid of triples."""
    xs = np.linspace(0.0, a, n)
    worst = 0.0
    worst_tri = None
    pts = [(x, y) for x in xs for y in xs]
    for tri in itertools.combinations(pts, 3):
        c, r2 = circumcentre(*tri)
        if c is None:
            continue
        if not (0.0 <= c[0] <= a and 0.0 <= c[1] <= a):
            continue
        val = triangle_area(*tri) * r2
        if val > worst:
            worst, worst_tri = val, (tri, c, r2)
    return worst, worst_tri


# --------------------------------------------------------------------------
# (3) corner branch over the continuum
# --------------------------------------------------------------------------
def maximise_corner_branch(a: float, starts: int, seed: int):
    """max over p1,p2,p3 in Q of |Delta(p1,p2,p3,C)| for a corner C."""
    rng = np.random.default_rng(seed)
    best = 0.0
    best_v = None
    for _ in range(starts):
        v0 = rng.uniform(0.0, a, size=6)
        res = minimize(
            lambda v: -abs(delta((v[0], v[1]), (v[2], v[3]), (v[4], v[5]), (0.0, 0.0))),
            v0, method="Nelder-Mead",
            options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000})
        val = abs(delta((res.x[0], res.x[1]), (res.x[2], res.x[3]),
                        (res.x[4], res.x[5]), (0.0, 0.0)))
        if val > best:
            best, best_v = val, res.x.copy()
    return best, best_v


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=float, default=1.0)
    ap.add_argument("--starts", type=int, default=400)
    ap.add_argument("--samples", type=int, default=200000)
    ap.add_argument("--grid", type=int, default=9)
    ap.add_argument("--seed", type=int, default=20261120)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    a = args.a
    report = {"a": a}

    print("=" * 78)
    print(f"(1) maximise |Delta| over Q^4,  a = {a}   (target a^4/2 = {a**4/2:.6f})")
    best, v = maximise_delta(a, args.starts, args.seed)
    pts = [(v[0], v[1]), (v[2], v[3]), (v[4], v[5]), (v[6], v[7])]
    print(f"    max |Delta| found = {best:.9f}")
    print(f"    a^4/2             = {a**4/2:.9f}")
    print(f"    ratio             = {best/(a**4/2):.9f}")
    print("    maximiser:")
    for p in pts:
        print(f"      ({p[0]:.6f}, {p[1]:.6f})")
    report["max_delta"] = best
    report["target"] = a ** 4 / 2
    report["maximiser"] = [list(p) for p in pts]

    print()
    print("=" * 78)
    print(f"(2) KEY LEMMA  Area*R^2 <= a^4/4 = {a**4/4:.6f}  (circumcentre in Q)")
    w, tri = check_key_lemma(a, args.samples, args.seed + 1)
    print(f"    random sampling ({args.samples} triples): worst = {w:.9f}  "
          f"ratio to a^4/4 = {w/(a**4/4):.9f}")
    if tri is not None:
        print(f"      at triangle {np.round(tri[0],6).tolist()}  centre {np.round(tri[1],6).tolist()}")
    wg, trig = check_key_lemma_grid(a, args.grid)
    print(f"    grid scan ({args.grid}^2 points, all triples): worst = {wg:.9f}  "
          f"ratio = {wg/(a**4/4):.9f}")
    if trig is not None:
        print(f"      at triangle {np.round(trig[0],6).tolist()}  centre {np.round(trig[1],6).tolist()}")
    report["key_lemma_random_worst"] = w
    report["key_lemma_grid_worst"] = wg

    print()
    print("=" * 78)
    print(f"(3) corner branch over the continuum, a = {a}")
    cb, cv = maximise_corner_branch(a, args.starts, args.seed + 2)
    print(f"    max |Delta(p1,p2,p3,(0,0))| = {cb:.9f}   (a^4/2 = {a**4/2:.6f})")
    print(f"    at p1=({cv[0]:.6f},{cv[1]:.6f}) p2=({cv[2]:.6f},{cv[3]:.6f}) "
          f"p3=({cv[4]:.6f},{cv[5]:.6f})")
    report["corner_branch_max"] = cb

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
