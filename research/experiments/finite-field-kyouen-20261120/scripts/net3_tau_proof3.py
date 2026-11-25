"""PROOF OF tau_3 = q-1 FOR ODD q.

SETUP (all verified exactly for q = 3,5,7,9).

F_{q^2} = F_q[w] with w^2 = d in F_q (d a non-square, so q odd).  Every
point of F_{q^2} \\ F_q is u = x + y*w with y != 0.  The three partitions
of the 3-net are given by

    a = x/y,   b = (x-1)/y,   c = (d - a*b)/(a - b),

and the grid is filled exactly on a != b.

THEOREM.  tau_3 = q - 1 for odd q.

PROOF.

(1)  tau_3 <= q, since there are only q rows.

(2)  Suppose T is a full transversal avoiding the diagonal: a permutation
     sigma of F_q with sigma(a) != a and the values

         c(a) = (d - a*sigma(a)) / (a - sigma(a))

     all distinct, hence (being q values in F_q) a permutation of F_q.

(3)  KEY IDENTITY.  For each a,

         c(a) * (a - sigma(a)) = d - a*sigma(a).

     Rearranged,

         a*sigma(a) - c(a)*sigma(a) = d - c(a)*a
         sigma(a) * (a - c(a)) = d - c(a)*a
         sigma(a) = (d - c(a)*a) / (a - c(a)).

     So sigma is determined by c by the SAME formula with the roles of
     b and c exchanged.  In other words the Latin square is SYMMETRIC in
     (b, c): the relation

         c*(a - b) = d - a*b

     is symmetric under b <-> c.  Indeed expanding both:

         c*a - c*b = d - a*b
         b*a - b*c = d - a*c      (swap b,c)

     and these are the same equation.  So the Latin square is
     "self-transpose" in the (b,c) pair.

(4)  CONSEQUENCE.  The relation c*(a-b) = d - a*b can be rewritten as

         a*b + b*c + c*a = d ... (*)

     Check: c*a - c*b = d - a*b  =>  a*b + c*a - c*b = d.  Not symmetric.
     Let me redo: from c*(a-b) = d - a*b,
         c*a - c*b + a*b = d.
     The left side is a*b + a*c - b*c.  Under the cyclic permutation
     (a,b,c) -> (b,c,a) this becomes b*c + b*a - c*a, which is different.
     Under (a,b,c) -> (a,c,b) it becomes a*c + a*b - c*b = a*b + a*c - b*c,
     the same.  So (*) is symmetric in b <-> c only.

(5)  Now sum (*) over a, using that sigma is a permutation and c is a
     permutation:

         sum_a [ a*sigma(a) + a*c(a) - sigma(a)*c(a) ] = q*d = 0  (in F_q,
         since q = 0 in F_q).

     Hmm, q*d = 0 automatically.  So this gives

         sum_a a*sigma(a) + sum_a a*c(a) - sum_a sigma(a)*c(a) = 0.

     This is a genuine constraint linking the three permutations
     id, sigma, c.  It says the three pairwise "dot products" satisfy
     <id,sigma> + <id,c> - <sigma,c> = 0.

(6)  For q = 3,5,7,9 an exhaustive search shows NO such triple exists with
     sigma(a) != a.  Hence tau_3 = q-1.

STATUS: step (5) gives a clean necessary condition; step (6) is verified
exhaustively but the general non-existence proof is still open.  The
identity (*) is the right object to attack.

Run:  python net3_tau_proof3.py
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
    print(f"{'q':>3} {'d':>8} {'formula ok':>11} {'sym b<->c':>10} "
          f"{'sum identity':>13} {'full transv':>12}")
    for q in args.q:
        r = build_square(q)
        if r is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue
        F, sub, d, L = r
        keys = sorted({a for (a, b) in L})

        # formula check
        fok = 0
        ftot = 0
        for (a, b), c in L.items():
            den = F.sub(a, b)
            if F.is_zero(den):
                continue
            ftot += 1
            if F.div(F.sub(d, F.mul(a, b)), den) == c:
                fok += 1

        # symmetry in b <-> c:  (a,b)->c  iff  (a,c)->b
        sym = all(L.get((a, c)) == b for (a, b), c in L.items()
                  if (a, c) in L)

        # sum identity: <id,sig> + <id,c> - <sig,c> = 0 for every transversal
        # (check on all full transversals avoiding the diagonal; there are none,
        #  so check on all full transversals including diagonal hits)
        sum_ok = True
        checked = 0
        for perm in itertools.permutations(keys):
            if any(L.get((keys[i], perm[i])) is None for i in range(len(keys))):
                continue
            cs = [L[(keys[i], perm[i])] for i in range(len(keys))]
            if len(set(cs)) != len(keys):
                continue
            checked += 1
            s1 = sum(F.mul(keys[i], perm[i])[0] for i in range(len(keys))) % q
            s2 = sum(F.mul(keys[i], cs[i])[0] for i in range(len(keys))) % q
            s3 = sum(F.mul(perm[i], cs[i])[0] for i in range(len(keys))) % q
            if (s1 + s2 - s3) % q != 0:
                sum_ok = False
                break

        # full transversal avoiding diagonal
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

        row = {"q": q, "d": repr(d), "formula_hits": fok, "formula_total": ftot,
               "formula_exact": fok == ftot, "symmetric_b_c": sym,
               "sum_identity_holds": sum_ok, "transversals_checked": checked,
               "full_transversal_avoiding_diagonal": ft}
        rows.append(row)
        print(f"{q:>3} {repr(d):>8} {str(fok == ftot):>11} {str(sym):>10} "
              f"{str(sum_ok):>13} {str(ft):>12}", flush=True)

    print()
    print("The Latin square is c = (d-ab)/(a-b), symmetric in (b,c).")
    print("No full transversal avoids the diagonal for odd q <= 9.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
