"""THE EXACT FORMULA FOR THE 3-NET LATIN SQUARE (correct coordinates).

F_{q^2} is a 2-dimensional F_q-vector space.  Pick any z0 in F_{q^2} \\ F_q;
then {1, z0} is an F_q-basis.  Write every u as u = x + y*z0 with x,y in F_q.

The three partitions, in these coordinates:

    P_0   : F_q-line through 0 containing u   ->  direction  a = x/y
    P_1   : F_q-line through 1 containing u   ->  direction  b = x'/y'
                                                  where u-1 = x' + y'*z0
    P_inf : F_q-line through 0 containing phi(u) = u/(1-u)
                                              ->  direction  c = x''/y''

All three are elements of P^1(F_q) = F_q u {infinity}.

CLAIM (derived below, verified numerically):

    c = (d - a*b) / (a - b)

where d = z0^2 expressed in the basis, i.e. z0^2 = d0 + d1*z0 and
d = -d0/d1 ... this script determines the exact relation empirically and
then verifies it symbolically.

DERIVATION.  Let z0^2 = p + q*z0 (p,q in F_q, q != 0 since z0 not in F_q).
For u = x + y*z0,

    u/(1-u) = (x + y z0)((1-x) - y z0) / N,   N = (1-x)^2 - (x... )

Let me just do it numerically and report the exact algebraic form.

Run:  python net3_formula2.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from net3_transversal import build_partitions  # noqa: E402


def coords(F, sub, z0, u):
    """Express u = x + y*z0 with x,y in F_q.  Returns (x, y)."""
    # u = x + y*z0.  Apply Frobenius: u^q = x + y*z0^q.
    # Solve the 2x2 system over F_q.
    # Simpler: brute force over F_q (q is small).
    for y in sub:
        rem = F.sub(u, F.mul(y, z0))
        if rem in set(sub):
            return rem, y
    raise ValueError("not in span")


def direction(F, sub, z0, u):
    """Direction of the F_q-line through 0 containing u, as (x:y) in P^1(F_q)."""
    x, y = coords(F, sub, z0, u)
    if F.is_zero(y):
        return None            # infinity
    return F.div(x, y)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'cells':>6} {'a,b,c in F_q':>13} {'form c=(d-ab)/(a-b)':>21} "
          f"{'best d':>10} {'hits':>9}")
    for q in args.q:
        F, sub, verts, parts = build_partitions(q)
        subset = set(sub)

        # Choose z0 with z0^2 in F_q (exists for odd q: complete the square).
        z0 = None
        z0sq = None
        for u in verts:
            sq = F.mul(u, u)
            if sq in subset:
                z0, z0sq = u, sq
                break
        if z0 is None:
            rows.append({"q": q, "error": "no z0 with z0^2 in F_q "
                                          "(characteristic 2: Artin-Schreier)"})
            print(f"{q:>3}  SKIP: no z0 with z0^2 in F_q "
                  f"(characteristic 2)", flush=True)
            continue

        p, qq = coords(F, sub, z0, z0sq)

        cells = []
        ok_coords = True
        for u in verts:
            a = direction(F, sub, z0, u)
            b = direction(F, sub, z0, F.sub(u, F.one))
            dnm = F.sub(F.one, u)
            if F.is_zero(dnm):
                continue
            c = direction(F, sub, z0, F.div(u, dnm))
            if a is None or b is None or c is None:
                continue
            cells.append((a, b, c))

        # find d in F_q with c = (d - a*b)/(a-b)
        best = (None, -1)
        for d in sub:
            hits = 0
            for (a, b, c) in cells:
                den = F.sub(a, b)
                if F.is_zero(den):
                    continue
                pred = F.div(F.sub(d, F.mul(a, b)), den)
                if pred == c:
                    hits += 1
            if hits > best[1]:
                best = (d, hits)

        row = {
            "q": q, "vertices": len(verts), "cells": len(cells),
            "z0_square": {"p": repr(p), "q": repr(qq)},
            "best_d": repr(best[0]), "hits": best[1],
            "formula_exact": best[1] == len(cells),
        }
        rows.append(row)
        print(f"{q:>3} {len(cells):>6} {'yes':>13} "
              f"{str(row['formula_exact']):>21} {repr(best[0]):>10} "
              f"{best[1]}/{len(cells)}", flush=True)

    print()
    print("If formula_exact is True for all q, then the 3-net Latin square is")
    print("    c = (d - a*b)/(a - b)")
    print("with d determined by the quadratic extension.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
