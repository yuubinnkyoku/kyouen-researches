"""Which q make the 3-cycle fixed points fall off the base circle?

The triple {0,1,2} is F_q-rational, so the S3 subgroup of PGL(2,q^2) that
permutes it is really PGL(2,q) (coefficients in F_q).  In particular the
3-cycle 0 -> 1 -> 2 -> 0 is a Moebius map over F_q, and its two fixed points
are the roots of a quadratic over F_q: either both lie in F_q (so they sit on
the base circle and are NOT four-point extensions of the triple), or they form a
conjugate pair in F_{q^2} \\ F_q (so they ARE extensions and give the exceptional
orbit of size 2 among the q^2-q extensions).

That orbit is exactly the orbit that carries a different Grundy value at q=5,
so the character of the discriminant is a cheap structural invariant that may
explain which q behave like q=5 and which like q=7.

Run:  python three_cycle_character.py --q 3 4 5 7 8 9 11 13 16 17 19 23 25 27 29 31 32
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402


def mat_mul(F, A, B):
    """Product of 2x2 matrices given as (a00, a01, a10, a11)."""
    a00, a01, a10, a11 = A
    b00, b01, b10, b11 = B
    return (
        F.add(F.mul(a00, b00), F.mul(a01, b10)),
        F.add(F.mul(a00, b01), F.mul(a01, b11)),
        F.add(F.mul(a10, b00), F.mul(a11, b10)),
        F.add(F.mul(a10, b01), F.mul(a11, b11)),
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    args = ap.parse_args()

    print(f"{'q':>4} {'disc square?':>13} {'fixed pts in F_q?':>18}  (character)")
    for q in args.q:
        F, sub = build_field(q)
        one = F.pow(sub[0], 0)
        zero = F.sub(one, one)
        # t = (0,1,2) and u = (1,2,0) as elements of F_q inside F_{q^2}
        t = sub[:3]
        u = [sub[1], sub[2], sub[0]]
        t0, t1, t2 = t
        u0, u1, u2 = u
        # phi_t matrix (rows may be scaled): [[(t1-t2), -t0(t1-t2)], [1, -t2]]
        n = F.sub(t1, t2)
        A = (n, F.neg(F.mul(t0, n)), one, F.neg(t2))
        # psi_u matrix: [[u2(u1-u0), u0(u2-u1)], [(u1-u0), (u2-u1)]]
        B = (F.mul(u2, F.sub(u1, u0)), F.mul(u0, F.sub(u2, u1)),
             F.sub(u1, u0), F.sub(u2, u1))
        a, b, c, d = mat_mul(F, B, A)      # f = psi_u o phi_t
        # fixed points: c z^2 + (d-a) z - b = 0, discriminant (d-a)^2 + 4bc
        four = F.add(F.add(one, one), F.add(one, one))
        disc = F.add(F.mul(F.sub(d, a), F.sub(d, a)), F.mul(four, F.mul(b, c)))
        # square test in F_q
        order = q - 1
        if F.is_zero(disc):
            square = True
        else:
            square = F.pow(disc, order // 2) == one
        inFq = square
        note = "on base circle" if inFq else "extensions (size-2 orbit)"
        print(f"{q:>4} {str(square):>13} {str(inFq):>18}  {note}")


if __name__ == "__main__":
    main()
