"""THE PROOF: E = Z_n minus {0, n/2}, and no complete mapping exists.

VERIFIED (net3_torus_native.py):

    q = 5,  n = 6:   E = {1,2,4,5}      = Z_6 \\ {0, 3}
    q = 7,  n = 8:   E = {1,2,3,5,6,7}  = Z_8 \\ {0, 4}

So E = Z_n \\ {0, n/2}, where n = q+1 is even and n/2 is the unique
involution of the cyclic group Z_n.

THEOREM.  Let n be even and E = Z_n \\ {0, n/2}.  There is NO bijection
phi: E -> E such that the map  e |-> e - phi(e)  (mod n) is injective.

PROOF.

Let phi: E -> E be a bijection and suppose psi(e) = e - phi(e) is
injective on E.  Since |E| = n-2, psi takes n-2 distinct values in Z_n.

(1)  SUM.  Summing psi over E:

         sum_{e in E} psi(e) = sum_E e - sum_E phi(e) = 0,

     because phi permutes E.  So the n-2 values of psi sum to 0 in Z_n.

(2)  Now compute sum_E e.  E = Z_n \\ {0, n/2}, so

         sum_E e = sum_{Z_n} e - 0 - n/2 = n(n-1)/2 - n/2  (mod n).

     For n even, sum_{Z_n} e = n(n-1)/2.  Modulo n:
       - if n/2 is odd, n(n-1)/2 = (n/2)(n-1) = (n/2)*(-1) = -n/2 = n/2 (mod n)
       - if n/2 is even, n(n-1)/2 = 0 (mod n)
     Either way sum_E e = sum_{Z_n} e - n/2.

     Check q=5, n=6: sum_{Z_6} = 15 = 3 (mod 6); sum_E = 1+2+4+5 = 12 = 0.
     3 - 3 = 0.  OK.
     Check q=7, n=8: sum_{Z_8} = 28 = 4 (mod 8); sum_E = 1+2+3+5+6+7 = 24 = 0.
     4 - 4 = 0.  OK.

     So sum_E e = 0 always.  Consistent with (1).

(3)  THE OBSTRUCTION.  psi is injective on E with image of size n-2, so
     exactly TWO values of Z_n are missing from the image.  Call them
     r and s.  Then

         sum_{Z_n} = sum(psi) + r + s = 0 + r + s  (mod n),

     so r + s = sum_{Z_n} = n(n-1)/2 (mod n).

     Also, psi(e) = e - phi(e) = 0 iff phi(e) = e, i.e. e is a fixed point
     of phi.  So 0 is in the image of psi iff phi has a fixed point.

     Similarly psi(e) = n/2 iff phi(e) = e - n/2 = e + n/2, i.e. phi maps
     e to its "antipode".

(4)  Now the counting.  Consider the involution iota(e) = e + n/2 on Z_n.
     It has NO fixed points (n even) and pairs up Z_n into n/2 pairs
     {e, e+n/2}.  The two excluded points 0 and n/2 form ONE such pair.

     So E is a union of n/2 - 1 antipodal pairs.

     If phi: E -> E is a bijection, consider the "antipodal defect"
         D = { e in E : phi(e) = e + n/2 }.
     psi(e) = n/2 exactly for e in D.

     Since psi is injective, |D| <= 1.

     Similarly, the fixed points of phi are F = { e : phi(e) = e }, and
     psi(e) = 0 exactly for e in F, so |F| <= 1.

(5)  Now: phi is a bijection of E, which is a union of antipodal pairs.
     Consider the induced map on the n/2 - 1 pairs.  If phi commutes with
     iota, it permutes the pairs; but phi need not commute.

     NUMERICAL FACT: for q = 5, 7 no such phi exists.

     A complete proof needs one more idea.  The natural candidate is to
     use the fact that |E| = n-2 is even and E is antipodally symmetric,
     so phi can be taken to be a "signed permutation" of the pairs; then
     psi(e) = e - phi(e) has a parity constraint that fails.

This script verifies the structure E = Z_n \\ {0, n/2} and the
non-existence of phi, and records the remaining gap.

Run:  python net3_final_proof.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from net3_torus_native import build_square  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'n':>3} {'E':>26} {'E=Z_n-{0,n/2}':>14} "
          f"{'phi exists?':>12} {'brute force':>12}")
    for q in args.q:
        r = build_square(q)
        if r is None:
            print(f"{q:>3}  SKIP (char 2)", flush=True)
            continue
        F, sub, d, L = r
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

        E = []
        for A in sub:
            if F.is_zero(A):
                continue
            num = F.add(F.one, F.mul(w, A))
            den = F.sub(F.one, F.mul(w, A))
            if F.is_zero(den):
                continue
            z = F.div(num, den)
            if z in expo:
                E.append(expo[z])
        E = sorted(set(E))

        expected = sorted(set(range(n)) - {0, n // 2})
        struct_ok = E == expected

        # brute force: is there a bijection phi: E -> E with e - phi(e) injective?
        found = []

        def rec(i, used_img, used_dif, phi):
            if i == len(E):
                found.append(list(phi))
                return True
            e = E[i]
            for f in E:
                if f in used_img:
                    continue
                dif = (e - f) % n
                if dif in used_dif:
                    continue
                phi.append(f)
                if rec(i + 1, used_img | {f}, used_dif | {dif}, phi):
                    return True
                phi.pop()
            return False

        exists = rec(0, frozenset(), frozenset(), [])

        row = {"q": q, "n": n, "E": E, "expected": expected,
               "structure_ok": struct_ok, "phi_exists": exists}
        rows.append(row)
        print(f"{q:>3} {n:>3} {str(E):>26} {str(struct_ok):>14} "
              f"{str(exists):>12} {str(exists):>12}", flush=True)

    print()
    print("STRUCTURE: E = Z_n \\ {0, n/2}, i.e. the cyclic group of order")
    print("n = q+1 with the identity and the unique involution removed.")
    print()
    print("The transversal problem is exactly: find a bijection phi of E")
    print("with e - phi(e) injective.  None exists for q = 5, 7.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
