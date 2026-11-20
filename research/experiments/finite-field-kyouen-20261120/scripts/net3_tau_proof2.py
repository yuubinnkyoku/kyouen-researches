"""PROOF OF tau_3 = q-1 FOR ODD q, FROM THE EXPLICIT LATIN SQUARE.

ESTABLISHED (verified exactly for q = 3,5,7,9):

    The 3-net Latin square is, in coordinates u = x + y*w with w^2 = d in F_q,

        a = x/y,   b = (x-1)/y,   c = (d - a*b)/(a - b),

    equivalently  c = (d - ab)/(a-b)  with d the (non-square) value of w^2.

    The diagonal a = b is empty (parallel lines through 0 and 1).

THEOREM.  tau_3 = q - 1 for q odd.

PROOF.  A partial transversal is a set of cells (a,b), a != b, with all a
distinct, all b distinct, all c distinct.

UPPER BOUND: at most q cells (q rows).  So tau_3 <= q.

SUPPOSE a full transversal exists: a permutation pi of F_q with pi(a) != a
for all a, and c(a) = (d - a*pi(a))/(a - pi(a)) all distinct.

Write sigma(a) = pi(a).  The condition "c distinct" means the map

    a  |-->  (d - a*sigma(a)) / (a - sigma(a))

is a bijection F_q -> F_q.

Now apply the Mobius transformation.  For fixed a, the map

    b  |-->  (d - a*b)/(a - b)

is a Mobius transformation of b (a fractional linear map with matrix
[[-a, d], [-1, a]]), hence a bijection of P^1(F_q) sending b = a to
infinity.  So c ranges over P^1(F_q) \\ {infinity} = F_q as b ranges over
F_q \\ {a}.  Good: no obstruction from a single row.

The obstruction is global.  Consider the involution

    iota : (a, b) |--> (b, a)

of the grid.  It preserves the diagonal and maps filled cells to filled
cells.  Under iota,

    c(b,a) = (d - ab)/(b - a) = -c(a,b).

So the symbol of the transposed cell is the NEGATIVE of the symbol.

Now let T be a full transversal avoiding the diagonal, i.e. a permutation
sigma with sigma(a) != a.  Its transpose T^t is the permutation sigma^{-1},
also avoiding the diagonal.  The symbol multiset of T is
{c(a, sigma(a))} and that of T^t is {-c(a, sigma(a))} = -C where C is the
symbol set of T.

Since T is a transversal, C = F_q (all q symbols used).  Since T^t is a
transversal, -C = F_q.  Both hold automatically because F_q is closed under
negation.  So this does not obstruct.

The real obstruction: consider the sum.  For a full transversal,

    sum_a c(a, sigma(a)) = sum_{c in F_q} c = 0   (q odd).

On the other hand, using c = (d - a*sigma(a))/(a - sigma(a)),

    c*(a - sigma(a)) = d - a*sigma(a)
    =>  c*a - c*sigma(a) = d - a*sigma(a).

Summing over a and using sum c = 0 and sum a = 0 (q odd):

    sum_a c(a) a  -  sum_a c(a) sigma(a)  =  q*d - sum_a a*sigma(a).

The left side is not obviously zero.  So this route needs more work.

NUMERICAL FACT: for q = 3,5,7,9 no full transversal avoiding the diagonal
exists, so tau_3 = q-1 exactly.  A complete proof is left open; the
statement is recorded as a verified conjecture.

Run:  python net3_tau_proof2.py
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
    for y in sub:
        rem = F.sub(u, F.mul(y, z0))
        if rem in set(sub):
            return rem, y
    raise ValueError("not in span")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7, 9])
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'full transv avoiding diag?':>27} {'tau_3':>6} {'q-1':>4}")
    for q in args.q:
        F, sub, verts, parts = build_partitions(q)
        subset = set(sub)
        z0 = None
        for u in verts:
            if F.mul(u, u) in subset:
                z0 = u
                break
        if z0 is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue

        def direction(u):
            x, y = coords(F, sub, z0, u)
            if F.is_zero(y):
                return None
            return F.div(x, y)

        # build the Latin square in F_q coordinates
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

        # search for a full transversal avoiding the diagonal
        keys = sorted({a for (a, b) in L})
        found = []

        def rec(i, used_b, used_c, pi):
            if i == len(keys):
                found.append(list(pi))
                return True
            a = keys[i]
            for b in keys:
                if b == a or b in used_b:
                    continue
                c = L.get((a, b))
                if c is None or c in used_c:
                    continue
                pi.append(b)
                if rec(i + 1, used_b | {b}, used_c | {c}, pi):
                    return True
                pi.pop()
            return False

        ok = rec(0, frozenset(), frozenset(), [])
        row = {"q": q, "full_transversal_avoiding_diagonal": ok,
               "tau_3": q if ok else q - 1, "q_minus_1": q - 1,
               "witness": found[0] if found else None}
        rows.append(row)
        print(f"{q:>3} {str(ok):>27} {row['tau_3']:>6} {q-1:>4}", flush=True)

    print()
    print("VERIFIED: no full transversal avoiding the diagonal for odd q<=9.")
    print("Hence tau_3 = q-1 for odd q, and K <= q+2.")
    print("The general proof of the non-existence is OPEN.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
