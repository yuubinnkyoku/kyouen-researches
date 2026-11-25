"""THE FINAL STEP: why no full transversal avoids the diagonal for odd q.

We have, exactly:

    the Latin square is   c = (d - a*b)/(a - b),   equivalently
    a*b + a*c - b*c = d                                          (*)

and for fixed a the map b -> c is the involution

    M_a(t) = (d - a*t)/(a - t),   M_a(a) = infinity, M_a(infinity) = a.

A transversal is a permutation sigma with c(a) = M_a(sigma(a)) a permutation.

THE KEY REFORMULATION.  Put  s = sigma(a), t = c(a).  Then (*) reads

    a*s + a*t - s*t = d.

Solve for a:

    a(s + t) = d + s*t
    a = (d + s*t)/(s + t)          (s + t != 0)

So the relation is SYMMETRIC in all three of a, s, t:

    a*s + a*t - s*t = d     is symmetric under any permutation of (a,s,t)?

Check: swapping a and s gives s*a + s*t - a*t = d, which is
a*s + s*t - a*t.  Compare with a*s + a*t - s*t.  These differ.
So NOT fully symmetric.  But note

    a*s + a*t - s*t = d
    <=>  a*s + a*t = d + s*t
    <=>  a(s+t) = d + s*t

and cyclically

    s(a+t) = d + a*t
    t(a+s) = d + a*s

These are three DIFFERENT equations, so the relation is not symmetric.

HOWEVER: the relation can be written as

    1/a + 1/s + 1/t = ... let's see.  Divide (*) by a*s*t:

    1/t + 1/s - 1/a = d/(a*s*t).

Not clean.

BETTER: substitute a = 1/A, s = 1/S, t = 1/T (assuming none is 0):

    1/(AS) + 1/(AT) - 1/(ST) = d
    =>  T + S - A = d*A*S*T.

Still not symmetric.

THE CLEAN FORM.  Note that (*) is equivalent to

    (a - d/s)(s - t) = ... 

Let me instead use the substitution that makes it a group law.  Define

    Phi(x) = x + d/x        (for x != 0).

Then (*) says a*s + a*t - s*t = d.  Divide by s*t:

    a/t + a/s - 1 = d/(s*t).

Hmm.

NUMERICAL APPROACH.  Rather than force the algebra, let me test the
following clean conjecture, which would finish the proof:

CONJECTURE.  For odd q, every full transversal of the Latin square
c = (d-ab)/(a-b) (diagonal allowed) has at least one cell on the diagonal.

Equivalently: the number of full transversals avoiding the diagonal is 0.

This script counts full transversals and how many avoid the diagonal,
for q = 3,5,7, and checks the structure of the ones that exist.

Run:  python net3_final_step.py
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
    print(f"{'q':>3} {'full transv':>12} {'avoiding diag':>14} "
          f"{'diag hits hist':>16}")
    for q in args.q:
        r = build_square(q)
        if r is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue
        F, sub, d, L = r
        keys = sorted({a for (a, b) in L})
        n = len(keys)

        total = 0
        avoiding = 0
        hist = {}
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
            hits = sum(1 for i in range(n) if perm[i] == keys[i])
            hist[hits] = hist.get(hits, 0) + 1
            if hits == 0:
                avoiding += 1

        row = {"q": q, "full_transversals": total,
               "avoiding_diagonal": avoiding,
               "diagonal_hit_histogram": {str(k): v for k, v in sorted(hist.items())}}
        rows.append(row)
        print(f"{q:>3} {total:>12} {avoiding:>14} {str(sorted(hist.items())):>16}",
              flush=True)

    print()
    print("If 'avoiding diag' is 0 for all odd q, then tau_3 = q-1.")
    print("The histogram shows how many full transversals hit the diagonal")
    print("in exactly k places.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
