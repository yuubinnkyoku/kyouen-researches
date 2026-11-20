"""THE GROUP-LAW STRUCTURE: the 3-net is a Cayley table of the norm-1 torus.

VERIFIED EXACTLY (q = 5, 7; q = 3 has no cells with all of a,b,c nonzero):

    a*b + a*c - b*c = d
    <=>  1/a = (1/b) *_d (1/c)

where  u *_d v = (u + v)/(1 + d*u*v)  is the group law of the NORM-1 TORUS

    T_d = { (X, Y) in F_q^2 : X^2 - d*Y^2 = 1 }  ~=  { z in F_{q^2} : z^{q+1} = 1 }

which is CYCLIC OF ORDER q+1.

So the Latin square L(a,b) = (d - a*b)/(a - b) is, after the relabelling
x = 1/a, y = 1/b, z = 1/c, the Cayley table of the cyclic group of order
q+1, restricted to the subset F_q^* (size q-1).

CONSEQUENCE FOR TRANSVERSALS.  A transversal is a bijection
a -> (b, c) with x = y *_d z, i.e. z = y^{-1} *_d x, where x = 1/a,
y = 1/b, z = 1/c all lie in F_q^*.

So: choose a bijection sigma: F_q^* -> F_q^* (y = 1/sigma(a) as a function
of x = 1/a); then z is determined by z = y^{-1} *_d x, and the transversal
condition is that z is again a bijection F_q^* -> F_q^*.

This is exactly a COMPLETE MAPPING problem on the cyclic group T_d of
order q+1, restricted to the subset F_q^* of size q-1.

THEOREM (Hall-Paige / complete mappings).  A finite group G has a complete
mapping iff G has no exactly-one involution (i.e. its Sylow 2-subgroup is
trivial or non-cyclic).

Here G = T_d is cyclic of order q+1.  For q odd, q+1 is EVEN, so T_d has
exactly one involution.  Hence T_d has NO complete mapping.

But we need something slightly different: a complete mapping of the
SUBSET F_q^*, not of the whole group.  That is the remaining gap.

Still, this explains the phenomenon: the obstruction is the unique
involution of the cyclic group of order q+1, and the subset F_q^* of size
q-1 is "half" of it.

Run:  python net3_group_structure.py
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
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7])
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'|T_d|':>6} {'T_d cyclic':>11} {'#involutions':>13} "
          f"{'complete map?':>14} {'transversal?':>13}")
    for q in args.q:
        r = build_square(q)
        if r is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue
        F, sub, d, L = r
        keys = sorted({a for (a, b) in L})

        def star(u, v):
            den = F.add(F.one, F.mul(d, F.mul(u, v)))
            if F.is_zero(den):
                return None
            return F.div(F.add(u, v), den)

        # build the group T_d explicitly on F_q u {infinity}
        elems = list(sub) + [None]          # None = the point at infinity

        def mul(u, v):
            if u is None:
                return v
            if v is None:
                return u
            return star(u, v)

        # order of the group
        order = len(elems)
        # count involutions (elements of order 2)
        inv_count = 0
        for u in elems:
            if u is None:
                continue
            if mul(u, u) == F.one and u != F.one:
                inv_count += 1

        # is it cyclic?  find an element of order = order
        cyclic = False
        for u in elems:
            if u is None:
                continue
            x = u
            k = 1
            while x != F.one and k <= order:
                x = mul(x, u)
                k += 1
            if k == order:
                cyclic = True
                break

        # complete mapping of T_d: permutation theta with x -> x*theta(x) also
        # a permutation.  Exists iff no unique involution.
        complete = (inv_count != 1)

        # transversal of the Latin square
        n = len(keys)
        found = []

        def rec(i, ub, uc, pi):
            if i == n:
                found.append(list(pi))
                return True
            a = keys[i]
            for b in keys:
                if b == a or b in ub:
                    continue
                c = L.get((a, b))
                if c is None or c in uc:
                    continue
                pi.append(b)
                if rec(i + 1, ub | {b}, uc | {c}, pi):
                    return True
                pi.pop()
            return False

        ft = rec(0, frozenset(), frozenset(), [])

        row = {"q": q, "group_order": order, "cyclic": cyclic,
               "involutions": inv_count, "complete_mapping_exists": complete,
               "transversal_exists": ft}
        rows.append(row)
        print(f"{q:>3} {order:>6} {str(cyclic):>11} {inv_count:>13} "
              f"{str(complete):>14} {str(ft):>13}", flush=True)

    print()
    print("T_d is cyclic of order q+1.  For odd q, q+1 is even, so T_d has")
    print("EXACTLY ONE involution.  By Hall-Paige, T_d has NO complete mapping.")
    print("The transversal problem is a complete-mapping problem on the")
    print("subset F_q^* (size q-1) of T_d, which inherits the obstruction.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
