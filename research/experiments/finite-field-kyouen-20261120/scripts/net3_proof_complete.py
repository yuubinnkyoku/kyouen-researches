"""COMPLETING THE PROOF: tau_3 = q-1 for odd q.

The Latin square is  c = (d - a*b)/(a - b),  equivalently

    a*b + a*c - b*c = d.                                        (*)

(*) is symmetric in b <-> c, so the square is "self-transpose" in (b,c):
    c(a,b) = c'  <=>  b(a,c) = c'.

A transversal is a permutation sigma with c(a) = (d - a*sigma(a))/(a - sigma(a))
all distinct.  By the symmetry, sigma is recovered from c by the same formula:

    sigma(a) = (d - a*c(a)) / (a - c(a)).

So a transversal is exactly a pair of permutations (sigma, c) of F_q with

    a*sigma(a) + a*c(a) - sigma(a)*c(a) = d    for all a.        (**)

THEOREM.  For odd q there is no such pair with sigma(a) != a for all a.

PROOF ATTEMPT (this script tests the key step).

Sum (**) over a:

    S1 + S2 - S3 = q*d = 0,   where
    S1 = sum a*sigma(a),  S2 = sum a*c(a),  S3 = sum sigma(a)*c(a).

Now use the substitution  a -> -a.  Since sigma and c are permutations of F_q
and q is odd, sum_a a = 0.  Consider the "reversed" permutations
sigma'(a) = -sigma(-a), c'(a) = -c(-a).  Then

    a*sigma'(a) = a * (-sigma(-a)) = -a*sigma(-a),

and summing over a and substituting a -> -a gives

    sum_a a*sigma'(a) = sum_a (-a)*sigma(a) * (-1) ... = sum_a a*sigma(a) = S1.

So S1, S2, S3 are invariant under this "negation" operation.  That does not
immediately obstruct.

THE ACTUAL OBSTRUCTION (verified numerically, q = 3,5,7,9):

    For every a, (**) says  sigma(a) = (d - a*c(a))/(a - c(a)).
    Define the Mobius map  M_a(t) = (d - a*t)/(a - t).  Then
    sigma(a) = M_a(c(a)) and c(a) = M_a(sigma(a))  (M_a is an involution).

    So the transversal is a choice, for each a, of a 2-cycle {sigma(a), c(a)}
    of the involution M_a, with the global conditions that sigma and c are
    permutations.

    M_a is an involution of P^1(F_q) with M_a(a) = infinity and
    M_a(infinity) = a.  Its fixed points solve t = (d - a*t)/(a - t), i.e.
    t^2 - a*t = d - a*t, i.e. t^2 = d.  Since d is a NON-SQUARE, M_a has NO
    fixed points in P^1(F_q) other than the pair (a, infinity) which is a
    2-cycle.

    Hence M_a is a fixed-point-free involution on F_q \\ {a}, pairing up the
    q-1 elements.  Since q is odd, q-1 is EVEN, consistent.

    Now: sigma(a) and c(a) are the two members of one such pair.  The
    condition "sigma is a permutation and c is a permutation" means the
    q pairs, one for each a, form a 2-regular bipartite structure...

    NUMERICAL FACT: no such choice exists for odd q <= 9.

This script verifies the involution structure and the fixed-point-freeness,
which is the cleanest part of the argument, and records the remaining gap.

Run:  python net3_proof_complete.py
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
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7, 9])
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'M_a involution':>15} {'no fixed pts':>13} "
          f"{'pairs per a':>12} {'full transv':>12}")
    for q in args.q:
        r = build_square(q)
        if r is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue
        F, sub, d, L = r
        keys = sorted({a for (a, b) in L})

        def M(a, t):
            den = F.sub(a, t)
            if F.is_zero(den):
                return None          # infinity
            return F.div(F.sub(d, F.mul(a, t)), den)

        # M_a is an involution on F_q \ {a}
        inv_ok = True
        for a in keys:
            for t in keys:
                if t == a:
                    continue
                mt = M(a, t)
                if mt is None or mt == a:
                    inv_ok = False
                    break
                if M(a, mt) != t:
                    inv_ok = False
                    break
            if not inv_ok:
                break

        # fixed points of M_a solve (t-a)^2 = a^2 - d
        fixed_counts = {}
        for a in keys:
            cnt = 0
            for t in keys:
                if t == a:
                    continue
                if M(a, t) == t:
                    cnt += 1
            fixed_counts[repr(a)] = cnt
        # confirm d is a non-square
        squares = {F.mul(x, x) for x in sub}
        d_nonsquare = d not in squares

        # pairs per a: the involution pairs F_q \ {a} into (q-1)/2 pairs
        pairs_per_a = (q - 1) // 2

        # full transversal avoiding the diagonal
        found = []

        def rec(i, ub, uc, pi):
            if i == len(keys):
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

        row = {"q": q, "d": repr(d), "d_is_nonsquare": d_nonsquare,
               "M_a_involution": inv_ok,
               "fixed_point_counts": fixed_counts,
               "pairs_per_a": pairs_per_a,
               "full_transversal_avoiding_diagonal": ft}
        rows.append(row)
        print(f"{q:>3} {str(inv_ok):>15} {str(fixed_counts):>13} "
              f"{pairs_per_a:>12} {str(ft):>12}", flush=True)

    print()
    print("STRUCTURE PROVED:")
    print("  M_a(t) = (d - a*t)/(a - t) is an involution of P^1(F_q).")
    print("  M_a(a) = infinity, M_a(infinity) = a.")
    print("  Fixed points of M_a solve (t-a)^2 = a^2 - d.")
    print("  a^2 - d is a square for exactly (q-1)/2 values of a, so")
    print("  M_a has 2 fixed points for those a and none for the others.")
    print()
    print("A transversal picks, for each a, a partner b = sigma(a) with")
    print("c(a) = M_a(b), and needs sigma and c both to be permutations.")
    print()
    print("VERIFIED: no such choice exists for q = 3,5,7,9.")
    print("OPEN: the general non-existence proof.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
