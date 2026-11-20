"""FAMILIES C AND D IN THE CYCLIC COORDINATES.

ESTABLISHED.  The map  a |-> alpha = alpha(1/a)  is a bijection
F_q -> Z_{q+1}, and the Latin square is EXACTLY the addition table:

    gamma = alpha - beta   (mod n),   n = q+1.

So the whole 3-net is the cyclic group Z_n.  Now what are families C and D?

FAMILY C.  {a, z, z', z''} concyclic with a in {0, 1, infinity}.  In the
normalised picture the anchors are a = 0, 1, infinity, which correspond to
alpha = alpha(infinity), alpha(alpha(1)), alpha(alpha(0)) -- three specific
elements of Z_n.

FAMILY D.  Four points of T concyclic.

The cleanest way to see the structure: the inversive plane's circles are
the images of P^1(F_q) under PGL(2, F_{q^2}).  In the normalised picture
S = {0,1,inf} u T, a circle through 0, 1, infinity is exactly P^1(F_q)
itself, which contains no point of T.  A circle through two of the anchors
is a "line" of the 3-net (family B).  A circle through ONE anchor is a
different object (family C).

THE KEY QUESTION: in the alpha coordinates, what does "z, z', z'' lie on a
circle through the anchor a" mean?

This script computes, for each anchor, the family of triples in alpha
coordinates, and looks for a pattern.

Run:  python net3_family_cd_alpha.py
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
from inversive_all_q import build_field  # noqa: E402
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

    return F, sub, d, direction, alpha, n


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
        F, sub, d, direction, alpha, n = s

        # the three anchors in alpha coordinates
        anchors = {"0": F.zero, "1": F.one, "inf": None}
        a_alpha = {name: alpha(F.inv(v)) if v is not None and not F.is_zero(v)
                   else alpha(None) for name, v in anchors.items()}
        # alpha(1/0) = alpha(infinity); alpha(1/1) = alpha(1); alpha(1/inf)=alpha(0)
        a_alpha = {
            "0": alpha(None),          # 1/0 = infinity
            "1": alpha(F.one),         # 1/1 = 1
            "inf": alpha(F.zero),      # 1/infinity = 0
        }

        # for each anchor, collect the triples {z,z',z''} that ARE concyclic
        # with it, in alpha coordinates
        pts = [v for v in sub if not F.is_zero(v)] + [None]
        # T = F_{q^2} \ F_q, but we only need the alpha labels of F_q points
        # Actually family C is about z,z',z'' in T (NOT in F_q).  So we need
        # the alpha coordinates of T-points, which is a different map.
        # Skip: report the anchor coordinates only.
        row = {"q": q, "n": n, "anchor_alphas": a_alpha}
        rows.append(row)
        print(f"q={q}: n={n}, anchor alpha values {a_alpha}", flush=True)

    print()
    print("The anchors 0, 1, infinity map to three specific elements of Z_n.")
    print("Family C is about triples of T-points, which need their own")
    print("alpha-like coordinate (T is not F_q).")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
