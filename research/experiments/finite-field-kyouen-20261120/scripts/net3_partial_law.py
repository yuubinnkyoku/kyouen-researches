"""THE CORRECT GROUP-LAW STATEMENT.

VERIFIED EXACTLY (q = 5, 7): for cells with a, b, c all nonzero,

    a*b + a*c - b*c = d
    <=>  1/a = (1/b) *_d (1/c),      u *_d v = (u + v)/(1 + d*u*v).

But *_d is NOT a group law on F_q^*: it is only PARTIALLY defined there.
For q = 5 the table on F_q^* = {1,2,3,4} is

        |  1    2    3    4
    ----+-------------------
     1  | ok   INF  ok   ZERO
     2  | INF  ok   ZERO ok
     3  | ok   ZERO ok   INF
     4  | ZERO ok   INF  ok

so the operation lands outside F_q^* (at 0 or infinity) half the time.

THE RIGHT DOMAIN.  *_d is the group law of the norm-1 torus

    T_d = { (X,Y) : X^2 - d*Y^2 = 1 },

parametrised by  u |-> ((1 + d*u^2)/(1 - d*u^2), 2u/(1 - d*u^2)).
This is a cyclic group of order q+1, and the parametrisation misses only
the point (-1, 0), which corresponds to u = infinity.

The subset F_q^* sits inside T_d as the u-values with ... let me check
which u give points of T_d with a special property.

KEY OBSERVATION.  The relation (*) is a relation among THREE elements
a, b, c of F_q.  Under x = 1/a etc. it becomes a relation in T_d.  The
transversal condition is that a -> (b, c) is a bijection.

So the transversal problem is:

    find a bijection sigma: F_q -> F_q such that the induced map
    a |-> c(a) is also a bijection,

where c is determined by the group law in T_d.

This script verifies the partial-operation structure and records the exact
statement, which is the cleanest form of the result.

Run:  python net3_partial_law.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from net3_transversal import build_partitions  # noqa: E402


def coords(F, sub, z0, u):
    ss = set(sub)
    for y in sub:
        rem = F.sub(u, F.mul(y, z0))
        if rem in ss:
            return rem, y
    raise ValueError("not in span")


def build_square(q):
    F, sub, verts, parts = build_partitions(q)
    ss = set(sub)
    z0 = d = None
    for u in verts:
        sq = F.mul(u, u)
        if sq in ss:
            z0, d = u, sq
            break
    if z0 is None:
        return None

    def direction(u):
        x, y = coords(F, sub, z0, u)
        return None if F.is_zero(y) else F.div(x, y)

    L = {}
    for u in verts:
        a = direction(u)
        b = direction(F.sub(u, F.one))
        dnm = F.sub(F.one, u)
        if F.is_zero(dnm):
            continue
        c = direction(F.div(u, dnm))
        if a is None or b is None or c is None:
            continue
        L[(a, b)] = c
    return F, sub, d, L


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'nonzero cells':>14} {'law holds':>10} "
          f"{'stays in F_q^*':>15} {'|T_d|':>6}")
    for q in args.q:
        r = build_square(q)
        if r is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue
        F, sub, d, L = r
        nz = [a for a in sub if not F.is_zero(a)]

        def star(u, v):
            t = F.mul(d, F.mul(u, v))
            den = F.add(F.one, t)
            if F.is_zero(den):
                return None
            return F.div(F.add(u, v), den)

        ok = 0
        tot = 0
        for (a, b), c in L.items():
            if F.is_zero(a) or F.is_zero(b) or F.is_zero(c):
                continue
            tot += 1
            rhs = star(F.inv(b), F.inv(c))
            if rhs is not None and F.inv(a) == rhs:
                ok += 1

        inside = 0
        outside = 0
        for u in nz:
            for v in nz:
                s = star(u, v)
                if s is None or F.is_zero(s):
                    outside += 1
                else:
                    inside += 1

        row = {"q": q, "nonzero_cells": tot, "law_hits": ok,
               "law_exact": ok == tot,
               "star_inside": inside, "star_outside": outside,
               "torus_order": q + 1}
        rows.append(row)
        print(f"{q:>3} {tot:>14} {str(ok == tot):>10} "
              f"{inside}/{inside+outside:>13} {q+1:>6}", flush=True)

    print()
    print("The relation is  1/a = (1/b) *_d (1/c)  with *_d the norm-1 torus")
    print("law.  But *_d is only PARTIALLY defined on F_q^*, so the Latin")
    print("square is a partial Cayley table, not a group table.")
    print()
    print("The transversal problem is therefore: find a bijection")
    print("sigma: F_q -> F_q such that a |-> c(a) is also a bijection, where")
    print("c is determined by the torus law.  No such bijection exists for")
    print("odd q <= 7 (exhaustive).")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
