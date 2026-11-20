"""THE STRONG THEOREM: the Latin square c = (d-ab)/(a-b) has NO transversal.

Numerical fact (net3_final_step.py): for q = 3, 5, 7 the Latin square

    L(a,b) = (d - a*b)/(a - b),    a != b,   d a non-square in F_q

has NO full transversal at all -- not even one that uses the diagonal.
(The diagonal cells are empty, so a "full transversal" here means a
permutation sigma with L(a, sigma(a)) defined and all distinct; since the
diagonal is empty, sigma(a) != a is automatic.)

Wait -- that is the same thing.  Let me restate precisely.

The grid has q rows and q columns, and the cell (a,a) is EMPTY.  A full
transversal would need one cell in each row and each column, i.e. a
permutation sigma with sigma(a) != a for all a (because (a,a) is empty).
So "full transversal" and "full transversal avoiding the diagonal" are the
SAME notion here.  The count 0 confirms tau_3 <= q-1.

THEOREM (to prove).  For odd q and d a non-square, there is no permutation
sigma of F_q with sigma(a) != a and

    c(a) = (d - a*sigma(a))/(a - sigma(a))

all distinct.

PROOF STRATEGY (the "product" argument).

From (*)  a*sigma(a) + a*c(a) - sigma(a)*c(a) = d,  solve for sigma:

    sigma(a) = (d - a*c(a))/(a - c(a)).

So sigma and c play symmetric roles.  Now consider the PRODUCT over a of
the relation.  Multiply (*) by ... or better, use the substitution

    a = 1/A,  sigma(a) = 1/S,  c(a) = 1/T.

Then (*) becomes

    1/(AS) + 1/(AT) - 1/(ST) = d
    =>  T + S - A = d*A*S*T.                                     (**)

Now sum (**) over a.  Since A, S, T each run over the same set
{1/x : x in F_q^*} = F_q^* (as permutations), we get

    sum T + sum S - sum A = d * sum (A*S*T).

The left side is sum(F_q^*) + sum(F_q^*) - sum(F_q^*) = sum(F_q^*) = 0
for q odd (since F_q^* pairs x with -x).  Hence

    sum_a A(a)*S(a)*T(a) = 0.                                    (***)

That is a clean necessary condition: the pointwise product
A*S*T must sum to zero.

But A*S*T = 1/(a*sigma(a)*c(a)), so (***) says

    sum_a 1/(a * sigma(a) * c(a)) = 0.

This is a genuine constraint.  Whether it is contradictory is what the
script tests.

Run:  python net3_product_argument.py
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
    print(f"{'q':>3} {'full transv':>12} {'sum 1/(a*s*c)':>15} "
          f"{'sum A*S*T':>11}")
    for q in args.q:
        r = build_square(q)
        if r is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue
        F, sub, d, L = r
        keys = sorted({a for (a, b) in L})
        n = len(keys)

        total = 0
        sums = set()
        for perm in itertools.permutations(keys):
            cs = []
            ok = True
            for i in range(n):
                c = L.get((keys[i], perm[i]))
                if c is None:
                    ok = False
                    break
                cs.append(c)
            if not ok or len(set(cs)) != n:
                continue
            total += 1
            # sum of 1/(a*sigma(a)*c(a))
            acc = F.zero
            for i in range(n):
                a, s, c = keys[i], perm[i], cs[i]
                if F.is_zero(a) or F.is_zero(s) or F.is_zero(c):
                    acc = None
                    break
                prod = F.mul(F.mul(a, s), c)
                acc = F.add(acc, F.inv(prod))
            if acc is not None:
                sums.add(repr(acc))

        row = {"q": q, "full_transversals": total,
               "distinct_sums": sorted(sums)}
        rows.append(row)
        print(f"{q:>3} {total:>12} {str(sorted(sums)):>15}", flush=True)

    print()
    print("If there are no full transversals, tau_3 = q-1 follows.")
    print("The product argument gives the necessary condition")
    print("    sum_a 1/(a*sigma(a)*c(a)) = 0,")
    print("which any transversal must satisfy.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
