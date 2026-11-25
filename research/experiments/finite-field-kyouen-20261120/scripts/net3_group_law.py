"""ATTEMPTING THE GENERAL PROOF: no transversal for c = (d-ab)/(a-b).

We have the exact relation

    a*b + a*c - b*c = d                                          (*)

with a, b = sigma(a), c = c(a).  Both sigma and c are permutations of F_q.

REFORMULATION AS A GROUP LAW.  Solve (*) for c:

    c(a - b) = d - a*b
    c = (d - a*b)/(a - b).

Now make the substitution

    a = sqrt(d) * (1 + u)/(1 - u)          (a Mobius map, u in P^1(F_q))

where sqrt(d) does NOT exist in F_q (d is a non-square).  So this
substitution is not available over F_q.  Instead work in F_{q^2} = F_q[w],
w^2 = d, and put

    a = w * (1 + u)/(1 - u).

Then a is in F_{q^2}.  But our a's are in F_q, so u must satisfy
w*(1+u)/(1-u) in F_q, i.e. (1+u)/(1-u) in w^{-1} F_q = w F_q.

Hmm, this conjugation is exactly the standard "half-turn" trick.

SIMPLER: THE COMPOSITION ARGUMENT.

Since sigma and c are both permutations, so is their composition
tau = c o sigma^{-1}.  A permutation of F_q has a fixed point iff
... not necessarily.

But: consider the map  a |-> (sigma(a), c(a)).  This is a bijection
F_q -> F_q x F_q whose image is a transversal.  The relation (*) says the
image lies on the surface

    S_d = { (b,c) : a*b + a*c - b*c = d for some a }
        = { (b,c) : a = (d + b*c)/(b + c) is defined and in F_q }.

So the transversal is a bijection F_q -> F_q x F_q whose image is
contained in the graph of the "inverse" relation.

KEY: the relation (*) is equivalent to

    1/(a) ... no.

Let me use the substitution  x -> 1/x  properly.  Put A = 1/a, B = 1/b,
C = 1/c (all nonzero).  Then (*) becomes

    T + S - A = d*A*S*T     (with A=1/a, S=1/b, T=1/c)

i.e.

    A + ... let me redo.  a*b + a*c - b*c = d.  Divide by a*b*c:

    1/c + 1/b - 1/a = d/(a*b*c)

so with A = 1/a, B = 1/b, C = 1/c:

    C + B - A = d*A*B*C.                                        (**)

Now (**) is LINEAR in each of A, B, C separately.  Solve for A:

    A(d*B*C + 1) = B + C
    A = (B + C)/(1 + d*B*C).

THIS IS THE ADDITION LAW OF THE CONIC / THE GROUP OF NORM 1!

Indeed, the map  x |-> (1 + d*x^2)/(1 - d*x^2), ... let me check: the
standard parametrisation of the norm-1 torus is

    N(u) = (1 + d*u^2)/(1 - d*u^2) + w * (2u)/(1 - d*u^2)

and the group law on the conic  X^2 - d*Y^2 = 1 is

    u *_d v = (u + v)/(1 + d*u*v).

**THAT IS EXACTLY THE FORMULA FOR A.**  So (**) says

    A = B *_d C

where `*_d` is the group law of the norm-1 torus, i.e. the group
F_{q^2}^(1) = { z : z^{q+1} = 1 } of order q+1.

So the relation (*) is equivalent to

    1/a = (1/b) *_d (1/c)

in the cyclic group of order q+1.

NOW THE PROOF.  A transversal is a bijection a -> (b, c) with
1/a = (1/b) *_d (1/c).  Write x = 1/a, y = 1/b, z = 1/c, all in F_q^*.
The condition is x = y *_d z, i.e. z = y^{-1} *_d x.

So: given the permutation sigma (i.e. a -> b), c is DETERMINED, and the
condition that c is a permutation is a condition on sigma.

Concretely, the map  (y, x) |-> y^{-1} *_d x  must be a bijection when
x = 1/a and y = 1/sigma(a) both range over F_q^*.

This is a "complete mapping"-type condition on the group G = F_{q^2}^(1)
of order q+1, restricted to the subset F_q^* of order q-1.

Hmm, but F_q^* is not a subgroup of G (orders q-1 and q+1 are coprime-ish).
Actually gcd(q-1, q+1) = 2.

This is the crux.  Let me test the reformulation numerically.

Run:  python net3_group_law.py
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
    print(f"{'q':>3} {'cells':>6} {'1/a=(1/b)*_d(1/c)':>20} {'group order':>12}")
    for q in args.q:
        r = build_square(q)
        if r is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue
        F, sub, d, L = r
        keys = sorted({a for (a, b) in L})

        def star(u, v):
            """u *_d v = (u+v)/(1+d*u*v) on F_q."""
            den = F.add(F.one, F.mul(d, F.mul(u, v)))
            if F.is_zero(den):
                return None
            return F.div(F.add(u, v), den)

        ok = 0
        tot = 0
        for (a, b), c in L.items():
            if F.is_zero(a) or F.is_zero(b) or F.is_zero(c):
                continue
            tot += 1
            lhs = F.inv(a)
            rhs = star(F.inv(b), F.inv(c))
            if rhs is not None and lhs == rhs:
                ok += 1

        row = {"q": q, "cells": tot, "group_law_hits": ok,
               "group_law_exact": ok == tot,
               "norm1_group_order": q + 1}
        rows.append(row)
        print(f"{q:>3} {tot:>6} {str(ok == tot):>20} {q+1:>12}  ({ok}/{tot})",
              flush=True)

    print()
    print("If exact, the relation is  1/a = (1/b) *_d (1/c)  where *_d is the")
    print("group law of the norm-1 torus of order q+1:")
    print("    u *_d v = (u + v)/(1 + d*u*v).")
    print("So the Latin square is the Cayley table of a cyclic group of")
    print("order q+1, restricted to the subset F_q^* of size q-1.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
