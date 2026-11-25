"""FAMILY C AND D IN THE EXPONENT PICTURE.

We now have the exact dictionary:

    a in F_q  <-->  alpha = alpha(1/a) in Z_{q+1},   a bijection
    cell (a,b) with symbol c  <-->  alpha = beta + gamma  (mod q+1)

where beta = alpha(1/b), gamma = alpha(1/c).

So the Latin square is the ADDITION TABLE of Z_{q+1}, restricted to the
subset  E = alpha(P^1(F_q)) = Z_{q+1}  (all of it, since alpha is a
bijection!).  Wait -- alpha is a bijection onto ALL of Z_{q+1}, so the
"restriction" is vacuous.

That means the Latin square IS the full addition table of Z_{q+1}, with
the diagonal removed.  Let me verify this directly: is L(a,b) determined
by alpha(1/a) - alpha(1/b)?

If so, then:
  - family B (pairs) = "T is a partial transversal of the addition table
    of Z_{q+1} with the diagonal removed" = a partial transversal of the
    cyclic Latin square.
  - family C and D must be expressible in the same coordinates.

This script tests whether the square is EXACTLY the cyclic group table,
which would be the cleanest possible statement.

Run:  python net3_cyclic_table.py
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
    print(f"{'q':>3} {'n':>3} {'cells':>6} {'cyclic table?':>14} "
          f"{'diag = ?':>10}")
    for q in args.q:
        r = build_square(q)
        if r is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue
        F, sub, d, L = r
        n = q + 1

        all_el = list(F.elements())
        T = [z for z in all_el if F.pow(z, n) == F.one]
        gen = None
        for cand in T:
            if cand == F.one:
                continue
            x = cand
            k = 1
            while x != F.one and k <= n:
                x = F.mul(x, cand)
                k += 1
            if k == n:
                gen = cand
                break
        expo = {}
        x = F.one
        for e in range(n):
            expo[x] = e
            x = F.mul(x, gen)

        w = None
        for cand in all_el:
            if F.mul(cand, cand) == d and cand not in set(sub):
                w = cand
                break

        def alpha(A):
            if A is None:
                z = F.one
            else:
                num = F.add(A, w)
                den = F.sub(A, w)
                z = F.one if F.is_zero(den) else F.div(num, den)
            return expo.get(z)

        # test: gamma = alpha - beta (mod n) for every cell
        ok = 0
        tot = 0
        diag = set()
        for (a, b), c in L.items():
            aa, ab, ac = alpha(a), alpha(b), alpha(c)
            if aa is None or ab is None or ac is None:
                continue
            tot += 1
            if (aa - ab) % n == ac:
                ok += 1
            if a == b:
                diag.add((aa - ab) % n)

        row = {"q": q, "n": n, "cells": tot, "cyclic_hits": ok,
               "is_cyclic_table": ok == tot, "diagonal_values": sorted(diag)}
        rows.append(row)
        print(f"{q:>3} {n:>3} {tot:>6} {str(ok == tot):>14} "
              f"{str(sorted(diag)):>10}  ({ok}/{tot})", flush=True)

    print()
    print("If is_cyclic_table is True, the Latin square is EXACTLY the")
    print("addition table of Z_{q+1} (with the diagonal removed), and the")
    print("whole game is a problem about the cyclic group.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
