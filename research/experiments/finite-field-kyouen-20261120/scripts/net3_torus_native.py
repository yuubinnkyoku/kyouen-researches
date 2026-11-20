"""THE TORUS GROUP LAW IN ITS NATIVE HOME F_{q^2}.

The law  u *_d v = (u + v)/(1 + d*u*v)  is the group law of the norm-1
torus, but it is only a PARTIAL operation on F_q (and on F_q u {infinity}).
The reason: the parametrisation

    u |-> ((1 + d*u^2)/(1 - d*u^2), 2u/(1 - d*u^2))

has poles, and the group is really

    T_d = { z in F_{q^2} : z^{q+1} = 1 },   |T_d| = q + 1.

The correct statement is in terms of z in T_d, not u in F_q.

THE CLEAN FORM.  Work in F_{q^2} = F_q[w], w^2 = d.  Every z in T_d is
z = X + Y*w with X^2 - d*Y^2 = 1.  The map

    z = X + Y*w  |->  u = Y/(1 + X)

is a bijection T_d \\ {-1} -> F_q, with -1 corresponding to u = infinity.

So F_q is "T_d minus two points" (-1 and the point at infinity of the
u-parametrisation), which matches |F_q| = q = (q+1) - 1.

Now: the relation A = S *_d T with A, S, T in F_q^* means, in T_d,

    z_A = z_S * z_T

where z_A, z_S, z_T are the corresponding torus elements.  The set
{ z_A : A in F_q^* } is a subset of T_d of size q-1.

This script computes that subset and its structure in T_d, which is the
correct setting for the proof.

Run:  python net3_torus_native.py
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
    print(f"{'q':>3} {'|T_d|':>6} {'|E|':>5} {'E in Z_n':>30} {'E = Z_n - ?':>14}")
    for q in args.q:
        r = build_square(q)
        if r is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue
        F, sub, d, L = r
        n = q + 1

        # T_d = { z in F_{q^2} : z^{q+1} = 1 }.  Build it.
        # F is F_p[t]/(f) of degree 2e; enumerate all elements and filter.
        all_el = list(F.elements())
        T = [z for z in all_el if F.pow(z, n) == F.one]
        assert len(T) == n, f"|T_d| = {len(T)}, expected {n}"

        # find a generator
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
        if gen is None:
            print(f"{q:>3}  T_d not cyclic?!", flush=True)
            continue

        # exponent of each torus element
        expo = {}
        x = F.one
        for e in range(n):
            expo[x] = e
            x = F.mul(x, gen)

        # map A in F_q^* to its torus element z_A = (1 + w*A)/(1 - w*A)
        # (the standard parametrisation with u = A)
        w = None
        for cand in all_el:
            if F.mul(cand, cand) == d and cand not in set(sub):
                w = cand
                break
        if w is None:
            print(f"{q:>3}  no w with w^2 = d", flush=True)
            continue

        E = []
        for A in sub:
            if F.is_zero(A):
                continue
            num = F.add(F.one, F.mul(w, A))
            den = F.sub(F.one, F.mul(w, A))
            if F.is_zero(den):
                continue
            z = F.div(num, den)
            if z not in expo:
                print(f"{q:>3}  z not in T_d for A={A}", flush=True)
                continue
            E.append(expo[z])
        E = sorted(set(E))

        missing = sorted(set(range(n)) - set(E))
        row = {"q": q, "n": n, "torus_order": len(T), "E": E,
               "missing_exponents": missing}
        rows.append(row)
        print(f"{q:>3} {len(T):>6} {len(E):>5} {str(E):>30} "
              f"{str(missing):>14}", flush=True)

    print()
    print("E is the exponent set of F_q^* inside the cyclic group T_d of")
    print("order q+1.  In exponent coordinates the transversal condition is")
    print("    tau = alpha - sigma_  (mod q+1),")
    print("a complete-mapping problem on the subset E of Z_{q+1}.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
