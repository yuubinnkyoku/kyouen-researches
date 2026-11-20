"""FAMILY C AND D IN THE CYCLIC PICTURE: a concrete conjecture.

We have the exact dictionary for the F_q part:

    a in F_q  <-->  alpha = alpha(1/a) in Z_{q+1},  a bijection,
    cell (a,b) with symbol c  <-->  gamma = alpha - beta  (mod q+1).

So the 3-net is the addition table of Z_n, n = q+1.

Now T lives in F_{q^2} \\ F_q, NOT in F_q.  So T-points do not have an
alpha coordinate from this dictionary.  But there IS a natural coordinate:
every z in F_{q^2} \\ F_q determines a unique F_q-line through 0 (its P_0
class) and a unique F_q-line through 1 (its P_1 class).  Those are exactly
the (a, b) pair, and the symbol c is the P_inf class.

So a T-point IS a cell (a,b) of the Latin square, i.e. a pair
(alpha, beta) in Z_n x Z_n with alpha != beta.  And the symbol is
gamma = alpha - beta.

THEREFORE: T is a set of cells of the cyclic Latin square, and

    family B  =  no two cells share a row, a column, or a symbol
              =  T is a partial transversal.

    family C  =  no three cells lie on a circle through an anchor.
    family D  =  no four cells are concyclic.

THE CONJECTURE.  In the (alpha, beta) coordinates, a circle through the
anchor 0 is a set of cells satisfying a LINEAR equation.  Let me test:

    is "cells (alpha_i, beta_i) lie on a circle through 0"
    equivalent to "alpha_i + beta_i = const" or "alpha_i - beta_i = const"
    or some other linear condition?

This script tests all linear conditions of the form
    p*alpha + q*beta = const   (mod n)
for small p, q, against the actual concyclicity data.

Run:  python net3_family_cd_linear.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from crossratio_graph import concyclic  # noqa: E402
from inversive_all_q import build_field, build_inversive_plane  # noqa: E402
from net3_transversal import build_partitions  # noqa: E402


def coords(F, sub, z0, u):
    ss = set(sub)
    for y in sub:
        rem = F.sub(u, F.mul(y, z0))
        if rem in ss:
            return rem, y
    raise ValueError("not in span")


def setup(q):
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

    # cells: (a,b) -> (alpha, beta, gamma)
    cells = {}
    for u in verts:
        a = direction(u)
        b = direction(F.sub(u, F.one))
        dnm = F.sub(F.one, u)
        if F.is_zero(dnm):
            continue
        c = direction(F.div(u, dnm))
        if a is None or b is None or c is None:
            continue
        aa, ab, ac = alpha(a), alpha(b), alpha(c)
        if aa is None or ab is None or ac is None:
            continue
        cells[(a, b)] = (aa, ab, ac, u)

    return F, sub, d, n, cells, alpha


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        s = setup(q)
        if s is None:
            print(f"q={q}: SKIP (char 2)", flush=True)
            continue
        F, sub, d, n, cells, alpha = s

        # For each anchor, group cells by "which circle through the anchor
        # contains the corresponding T-point".  A T-point is u; the anchor
        # is 0, 1, or infinity.  Two T-points u, u' are on a common circle
        # through the anchor iff concyclic(anchor, u, u', x) for some x...
        # Actually family C is about TRIPLES.  Let me instead test the
        # simpler pairwise question: for a FIXED anchor a, is the relation
        # "u, u' on a common circle through a" linear in (alpha, beta)?

        anchors = {"0": F.zero, "1": F.one, "inf": None}
        results = {}
        for name, a in anchors.items():
            # collect pairs (u, u') on a common circle through a
            pts = list(cells.values())
            # For each pair, test whether SOME circle through a contains both
            points, circles = build_inversive_plane(q)
            idx = {p: i for i, p in enumerate(points)}
            circ = [frozenset(idx[p] for p in c) for c in circles]
            a_idx = idx[a]

            def share_circle_through_a(u, v):
                for cs in circ:
                    if a_idx in cs and idx[u] in cs and idx[v] in cs:
                        return True
                return False

            # test linear conditions p*alpha + q*beta = const
            best = None
            for p in range(n):
                for qq in range(n):
                    if p == 0 and qq == 0:
                        continue
                    # for each pair, does "same value of p*alpha+qq*beta"
                    # match "share a circle through a"?
                    agree = 0
                    tot = 0
                    for i in range(len(pts)):
                        for j in range(i + 1, len(pts)):
                            ai, bi, _, ui = pts[i]
                            aj, bj, _, uj = pts[j]
                            lin = ((p * ai + qq * bi) % n
                                   == (p * aj + qq * bj) % n)
                            geo = share_circle_through_a(ui, uj)
                            tot += 1
                            if lin == geo:
                                agree += 1
                    if best is None or agree > best[1]:
                        best = ((p, qq), agree, tot)
            results[name] = {"best_pq": best[0], "agree": best[1],
                             "total": best[2],
                             "rate": round(best[1] / best[2], 4) if best[2] else None}

        row = {"q": q, "n": n, "anchors": results}
        rows.append(row)
        print(f"q={q} (n={n}):", flush=True)
        for name, r in results.items():
            print(f"  anchor {name}: best (p,q)={r['best_pq']} "
                  f"agreement {r['agree']}/{r['total']} = {r['rate']}",
                  flush=True)

    print()
    print("If any anchor reaches agreement 1.0, family C is a LINEAR condition")
    print("in the cyclic coordinates, and the whole game becomes a linear")
    print("algebra problem over Z_{q+1}.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
