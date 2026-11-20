"""THE DERIVED-DESIGN RECURSION, done correctly.

Let D be a 3-(v,s,1) design and S a safe set (every block meets S in <= 3).
Fix p in S.  The DERIVED design D_p has

    points = the v-1 points other than p
    blocks = { B \\ {p} : B a block through p },  each of size s-1

and is a 2-(v-1, s-1, 1) design, i.e. a LINEAR SPACE with all lines of size
s-1.

CLAIM.  S \\ {p} meets every line of D_p in at most 2 points.

PROOF.  A line of D_p is B \\ {p} for a block B through p.  If it contained
two points a,b of S\\{p}, then B contains p,a,b -- three points of S.  If it
contained a third c, then B would contain four points of S, contradicting
safety.  []

Hence, writing A_2(L) for the maximum 2-arc (no 3 collinear) of a linear
space L,

    K(D) <= 1 + A_2(D_p).                                    (DERIVATION BOUND)

Consequences:

  (a) A_2(L) <= 1 + lambda_2 for any linear space L (the lines through a
      fixed point a are lambda_2 in number and each carries at most one
      further point of a 2-arc).  So the derivation bound IMPLIES the
      lambda_2 bound K <= lambda_2 + 2.

  (b) The derivation bound is STRICTLY SHARPER whenever A_2(D_p) < lambda_2+1.

Classical derived designs:

    inversive plane of order q, derived at p  =  AG(2,q)
    Witt S(3,6,22), derived at p              =  PG(2,4)

IMPORTANT: AG(2,q) is built here by DERIVING the inversive plane, not by
mod-q arithmetic.  Mod-q arithmetic gives the TORUS Z_q^2, which coincides
with AG(2,q) only for prime q (see TORUS.md).

Run:  python derived_design_bound.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_inversive_plane  # noqa: E402


# ------------------------------------------------------------------ derive


def derive(points, blocks, p):
    """Derived design at point p: (n_points, lines) with p removed."""
    others = [x for x in points if x != p]
    idx = {x: i for i, x in enumerate(others)}
    lines = set()
    for B in blocks:
        if p in B:
            ln = tuple(sorted(idx[x] for x in B if x != p))
            if len(ln) >= 2:
                lines.add(ln)
    return len(others), sorted(lines)


# ------------------------------------------------------------------ PG(2,q)


def build_pg2q(q: int):
    def normalise(v):
        for c in v:
            if c % q != 0:
                inv = pow(c, -1, q)
                return tuple((x * inv) % q for x in v)
        return None

    pts = set()
    for x in range(q):
        for y in range(q):
            for z in range(q):
                if (x, y, z) != (0, 0, 0):
                    pts.add(normalise((x, y, z)))
    points = sorted(pts)
    idx = {p: i for i, p in enumerate(points)}
    lines = set()
    for a in range(q):
        for b in range(q):
            for c in range(q):
                if (a, b, c) == (0, 0, 0):
                    continue
                ln = tuple(sorted(
                    idx[p] for p in points
                    if (a * p[0] + b * p[1] + c * p[2]) % q == 0))
                if len(ln) == q + 1:
                    lines.add(ln)
    return len(points), sorted(lines)


# ------------------------------------------------------------------ max 2-arc


def max_2arc(n: int, lines, node_cap: int = 200_000_000):
    """Maximum set meeting every line in at most 2 points."""
    lines_of_point: list[list[int]] = [[] for _ in range(n)]
    for li, L in enumerate(lines):
        for p in L:
            lines_of_point[p].append(li)

    cnt = [0] * len(lines)
    chosen: list[int] = []
    best: list[list[int]] = [[]]
    state = {"nodes": 0}

    def rec(start: int) -> None:
        state["nodes"] += 1
        if state["nodes"] > node_cap:
            raise RuntimeError("node cap exceeded")
        if len(chosen) > len(best[0]):
            best[0] = chosen.copy()
        if len(chosen) + (n - start) <= len(best[0]):
            return
        for p in range(start, n):
            ok = True
            for li in lines_of_point[p]:
                if cnt[li] >= 2:
                    ok = False
                    break
            if not ok:
                continue
            for li in lines_of_point[p]:
                cnt[li] += 1
            chosen.append(p)
            rec(p + 1)
            chosen.pop()
            for li in lines_of_point[p]:
                cnt[li] -= 1

    rec(0)
    return best[0], state["nodes"]


# ------------------------------------------------------------------ main


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--node-cap", type=int, default=200_000_000)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7, 8, 9])
    args = ap.parse_args()

    INV_K = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8}

    rows = []
    print("=== inversive plane derived at p  =  AG(2,q) ===")
    print(f"{'q':>3} {'v':>5} {'lines':>6} {'A_2':>5} {'1+A_2':>6} "
          f"{'lam2+2':>7} {'K(inv)':>7} {'tight?':>7}")
    for q in args.q:
        points, circles = build_inversive_plane(q)
        n, lines = derive(points, circles, points[0])
        t0 = time.time()
        try:
            best, nodes = max_2arc(n, lines, node_cap=args.node_cap)
            a2, err = len(best), None
        except RuntimeError as exc:
            a2, best, nodes, err = None, None, -1, str(exc)
        dt = time.time() - t0
        lam2 = q + 1
        K = INV_K.get(q)
        bound = 1 + a2 if a2 is not None else None
        tight = (K == bound) if (K is not None and bound is not None) else None
        rows.append({
            "board": "AG(2,q) derived", "q": q, "v": n, "lines": len(lines),
            "A_2": a2, "derivation_bound": bound, "lambda2_bound": lam2 + 2,
            "K_inversive": K, "tight": tight, "witness": best,
            "nodes": nodes, "seconds": round(dt, 2), "error": err,
        })
        print(f"{q:>3} {n:>5} {len(lines):>6} {a2!s:>5} {bound!s:>6} "
              f"{lam2+2:>7} {K!s:>7} {tight!s:>7}  {dt:.1f}s"
              + (f"  ERROR {err}" if err else ""), flush=True)

    print()
    print("=== A_2(PG(2,q)) : max arc (classical) ===")
    print(f"{'q':>3} {'v':>5} {'A_2':>5} {'q+1':>5} {'q+2':>5} {'classical':>10}")
    for q in (2, 3, 4, 5, 7):
        n, lines = build_pg2q(q)
        t0 = time.time()
        try:
            best, nodes = max_2arc(n, lines, node_cap=args.node_cap)
            a2, err = len(best), None
        except RuntimeError as exc:
            a2, best, nodes, err = None, None, -1, str(exc)
        dt = time.time() - t0
        cls = q + 2 if q % 2 == 0 else q + 1
        rows.append({
            "board": "PG(2,q)", "q": q, "v": n, "A_2": a2, "classical": cls,
            "match": a2 == cls if a2 is not None else None,
            "witness": best, "nodes": nodes, "seconds": round(dt, 2),
            "error": err,
        })
        print(f"{q:>3} {n:>5} {a2!s:>5} {q+1:>5} {q+2:>5} {cls:>10}  {dt:.1f}s"
              + (f"  ERROR {err}" if err else ""), flush=True)

    print()
    print("DERIVATION BOUND:  K(D) <= 1 + A_2(D_p)")
    print("  Witt S(3,6,22) derived at p = PG(2,4): K <= 1 + 6 = 7, and K = 7.")
    print("  A_2(L) <= 1 + lambda_2 for any linear space, so the derivation")
    print("  bound implies K <= lambda_2 + 2.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
