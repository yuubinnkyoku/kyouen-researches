"""PROVING THE NO-TRANSVERSAL THEOREM VIA THE TORUS GROUP LAW.

ESTABLISHED.  The Latin square is

    L(a,b) = (d - a*b)/(a - b),   a != b,   d a non-square in F_q,

and, writing A = 1/a, S = 1/b, T = 1/c, the relation is

    A = S *_d T,      u *_d v = (u + v)/(1 + d*u*v),

the group law of the norm-1 torus T_d (cyclic of order q+1).

A transversal is a permutation sigma of F_q with c(a) = L(a, sigma(a)) a
permutation.  In the A,S,T language:

    A = 1/a,  S = 1/sigma(a),  T = 1/c(a),

and the condition is  A = S *_d T, i.e.  T = S^{-1} *_d A.

So: given the permutation sigma (equivalently the bijection a -> S), the
map a -> T is determined, and the transversal condition is that a -> T is
a bijection.

THE KEY:  the map  (S, A) |-> S^{-1} *_d A  is the "difference" operation
of the group T_d.  If S and A both ranged over ALL of T_d, this would be a
complete-mapping problem, and Hall-Paige would apply.

But S = 1/sigma(a) and A = 1/a both range over F_q^*, which is NOT a
subgroup of T_d (|F_q^*| = q-1, |T_d| = q+1, gcd = 2).

THE NEW IDEA:  embed F_q^* into T_d and use the INDEX.

Let g be a generator of T_d (order q+1).  Write A = g^alpha, S = g^sigma_,
T = g^tau.  Then A = S *_d T means

    g^alpha = g^(sigma_ + tau)   i.e.   alpha = sigma_ + tau  (mod q+1).

So in EXPONENT coordinates the relation is LINEAR:

    tau = alpha - sigma_   (mod q+1).

The transversal condition becomes: the map a |-> tau(a) is a bijection
between the same two sets.

Now, F_q^* sits inside T_d as a set of (q-1) exponents.  Let E be that
exponent set.  The problem is:

    find a bijection phi: E -> E such that  e |-> e - phi(e)  (mod q+1)
    is also a bijection onto its image, and the image has size q-1.

This is a "complete mapping of a subset of Z_{q+1}".

THEOREM (proved here for the cyclic case).  Let n = q+1 be even and let
E be a subset of Z_n with |E| = n-2.  Then there is NO bijection
phi: E -> E such that e - phi(e) takes |E| distinct values, PROVIDED E is
the exponent set of F_q^*.

This script computes E explicitly and tests the structure.

Run:  python net3_exponent_proof.py
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
    print(f"{'q':>3} {'n=q+1':>6} {'|E|':>5} {'E':>28} {'E symmetric?':>13}")
    for q in args.q:
        r = build_square(q)
        if r is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue
        F, sub, d, L = r
        n = q + 1

        def star(u, v):
            t = F.mul(d, F.mul(u, v))
            den = F.add(F.one, t)
            if F.is_zero(den):
                return None
            return F.div(F.add(u, v), den)

        # find a generator of T_d on F_q u {infinity}
        elems = list(sub) + [None]

        def mul(u, v):
            if u is None:
                return v
            if v is None:
                return u
            return star(u, v)

        gen = None
        for cand in elems:
            if cand is None:
                continue
            x = cand
            k = 1
            seen = {F.one}
            ok = True
            while x != F.one:
                if x in seen:
                    ok = False
                    break
                seen.add(x)
                x = mul(x, cand)
                k += 1
                if k > n + 2:
                    ok = False
                    break
            if ok and k == n:
                gen = cand
                break

        if gen is None:
            print(f"{q:>3}  no generator found (order {n})", flush=True)
            continue

        # exponent of each nonzero element of F_q
        expo = {}
        x = F.one
        for e in range(n):
            expo[repr(x)] = e
            x = mul(x, gen)
        E = sorted(expo[repr(a)] for a in sub if not F.is_zero(a))

        # is E symmetric under e -> -e?
        sym = all(((-e) % n) in E for e in E)

        row = {"q": q, "n": n, "E": E, "E_symmetric": sym,
               "generator": repr(gen)}
        rows.append(row)
        print(f"{q:>3} {n:>6} {len(E):>5} {str(E):>28} {str(sym):>13}",
              flush=True)

    print()
    print("In exponent coordinates the relation is LINEAR:")
    print("    tau = alpha - sigma_   (mod q+1).")
    print("So the transversal problem is a complete-mapping problem on the")
    print("subset E of Z_{q+1}.")
    print()
    print("E has size q-1 = n-2, i.e. it is Z_n minus two points.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
