"""Sanity check of 'hyperbolic <=> det M is a square' for q odd (used in K1252).

Random quadrics of PG(3,q) (q odd) are classified twice: by counting their
F_q-points (hyperbolic (q+1)^2, elliptic q^2+1, others degenerate) and by
testing whether det M is a square (after normalising the symmetric matrix so
that the off-diagonal entries are a_ij/2).  The two classifications must agree
on every non-degenerate sample.

Run:  python quadric_type_check.py --q 7 9 11 13 --samples 400
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_prime_power import FiniteField, factorize, find_irreducible  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--samples", type=int, default=400)
    args = ap.parse_args()

    for q in args.q:
        p, e = factorize(q)[0]
        F = FiniteField(p, e, find_irreducible(p, e))
        elems = list(F.elements())
        one = F.pow(elems[0], 0)
        zero = F.sub(one, one)
        mul, add = F.mul, F.add
        half = F.div(one, add(one, one))
        squares = {mul(x, x) for x in elems}
        # projective points
        seen = set()
        pts = []
        for a in elems:
            for b in elems:
                for c in elems:
                    for d in elems:
                        if F.is_zero(a) and F.is_zero(b) and F.is_zero(c) and F.is_zero(d):
                            continue
                        v = (a, b, c, d)
                        inv = None
                        for x in v:
                            if not F.is_zero(x):
                                inv = F.div(one, x)
                                break
                        v = tuple(mul(inv, x) for x in v)
                        if v in seen:
                            continue
                        seen.add(v)
                        pts.append(v)
        rng = random.Random(20261123 + q)
        agree = 0
        checked = 0
        mismatch = 0
        for _ in range(args.samples):
            a = [[zero] * 4 for _ in range(4)]
            for i in range(4):
                for j in range(i, 4):
                    v = rng.choice(elems)
                    a[i][j] = v
                    a[j][i] = v
            def Q(pt):
                # the quadratic form is sum_{i <= j} a_ij x_i x_j
                acc = zero
                for i in range(4):
                    for j in range(i, 4):
                        if not F.is_zero(a[i][j]):
                            acc = add(acc, mul(a[i][j], mul(pt[i], pt[j])))
                return acc
            cnt = sum(1 for pt in pts if F.is_zero(Q(pt)))
            # symmetric matrix with halved off-diagonals, for the determinant
            M = [[zero] * 4 for _ in range(4)]
            for i in range(4):
                for j in range(4):
                    M[i][j] = a[i][j] if i == j else mul(a[i][j], half)
            # determinant
            A = [row[:] for row in M]
            det = one
            ok = True
            for c in range(4):
                piv = next((i for i in range(c, 4) if not F.is_zero(A[i][c])), None)
                if piv is None:
                    ok = False
                    break
                if piv != c:
                    A[c], A[piv] = A[piv], A[c]
                    det = F.neg(det)
                det = mul(det, A[c][c])
                inv = F.div(one, A[c][c])
                A[c] = [mul(inv, x) for x in A[c]]
                for i in range(4):
                    if i != c and not F.is_zero(A[i][c]):
                        f = A[i][c]
                        A[i] = [F.sub(A[i][k], mul(f, A[c][k])) for k in range(4)]
            if not ok:
                continue
            checked += 1
            if cnt not in (q * q + 1, (q + 1) * (q + 1)):
                print(f"q={q}: unexpected non-degenerate point count {cnt}")
                continue
            hyperbolic = cnt == (q + 1) * (q + 1)
            det_square = det in squares
            if hyperbolic == det_square:
                agree += 1
            else:
                mismatch += 1
                print(f"q={q}: MISMATCH hyperbolic={hyperbolic} det_square={det_square}")
        print(f"q={q}: {checked} non-degenerate samples, {agree} agree, {mismatch} mismatch",
              flush=True)


if __name__ == "__main__":
    main()
