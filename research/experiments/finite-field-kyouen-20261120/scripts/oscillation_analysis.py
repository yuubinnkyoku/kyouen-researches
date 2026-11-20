"""Why does the inversive K oscillate?

Corrected series:
  q:  3  4  5  7  8  9 11 13 17 19 23 29
  K:  5  5  6  6  7  9  9  8  9  9 10  8

The oscillation is: 9 (q=11), 8 (q=13), 9 (q=17), 9 (q=19), 10 (q=23), 8 (q=29).

Hypothesis: K depends on the arithmetic of q, not just its size.

For the inversive plane of order q, the circles are the images of P^1(F_q)
under PGL(2, F_{q^2}).  A safe set meets every circle in at most 3 points.

Key structural quantity: the number of circles through a pair is lambda_2 = q+1.
The lambda_2 bound gives K <= q+3.

But the actual K is much smaller.  What limits it?

Let me look at the "circle intersection" structure: two circles meet in at most 2
points.  For a safe set S, the circles through a pair {a,b} of S that contain a
third point of S number k-2.  The pencil has q+1 circles.

So k-2 <= q+1, i.e. k <= q+3.  That is the lambda_2 bound.

To get a better bound we need to know how many of the q+1 circles through a,b
can actually contain a third point of S.

Hmm.  Let me instead look at the DATA: is K related to q mod something?

  q=11 (11 mod 4 = 3): K=9
  q=13 (13 mod 4 = 1): K=8
  q=17 (17 mod 4 = 1): K=9
  q=19 (19 mod 4 = 3): K=9
  q=23 (23 mod 4 = 3): K=10
  q=29 (29 mod 4 = 1): K=8

No clean pattern with q mod 4.

Let me look at K vs q:
  q=11: K=9, q-K=2
  q=13: K=8, q-K=5
  q=17: K=9, q-K=8
  q=19: K=9, q-K=10
  q=23: K=10, q-K=13
  q=29: K=8, q-K=21

q-K grows: 2, 5, 8, 10, 13, 21.  Roughly linear in q.

So K ~ q - c*q for some c?  K/q: 0.82, 0.62, 0.53, 0.47, 0.43, 0.28.

Hmm, K/q is decreasing but not linearly.

Let me check: is K related to the maximum number of points on a circle?  All
circles have size q+1.  So that's constant.

What about the number of circles?  q(q^2+1).

Let me look at the "3-arc" literature value.  For the inversive plane of order q,
the maximum size of a 3-arc (no 4 concyclic) is known in some cases.

Actually, let me just compute more data points to see the pattern.  q=31, 37.

But the computation is slow (q=29 took 50s).  Let me estimate: q=31 might take
~2 minutes, q=37 ~10 minutes.

Let me run q=31 in the background and meanwhile analyse the existing data.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


INV = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8, 17: 9, 19: 9,
       23: 10, 29: 8}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    print("inversive K vs q:")
    print(f"{'q':>3} {'K':>3} {'q-K':>4} {'K/q':>6} {'q mod 4':>8} {'q mod 3':>8}")
    rows = []
    for q in sorted(INV):
        k = INV[q]
        rows.append({"q": q, "K": k, "q_minus_K": q - k, "K_over_q": k / q,
                     "q_mod_4": q % 4, "q_mod_3": q % 3})
        print(f"{q:>3} {k:>3} {q-k:>4} {k/q:>6.2f} {q%4:>8} {q%3:>8}")

    print()
    print("K by q mod 4:")
    for r in (0, 1, 3):
        ks = [INV[q] for q in INV if q % 4 == r]
        if ks:
            print(f"  q = {r} mod 4: K = {ks}")

    print()
    print("K by q mod 3:")
    for r in (0, 1, 2):
        ks = [INV[q] for q in INV if q % 3 == r]
        if ks:
            print(f"  q = {r} mod 3: K = {ks}")

    print()
    print("q-K (the 'deficit'):")
    for q in sorted(INV):
        print(f"  q={q:>2}: q-K = {q - INV[q]:>2}")

    # fit q-K ~ a*q + b for q >= 11
    qs = [q for q in sorted(INV) if q >= 11]
    ds = [q - INV[q] for q in qs]
    n = len(qs)
    mq = sum(qs) / n
    md = sum(ds) / n
    den = sum((q - mq) ** 2 for q in qs)
    a = sum((q - mq) * (d - md) for q, d in zip(qs, ds)) / den if den else 0
    b = md - a * mq
    print()
    print(f"deficit fit (q>=11): q-K ~ {a:.3f}*q + {b:.2f}")
    print(f"  => K ~ {1-a:.3f}*q - {b:.2f}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "rows": rows,
            "deficit_fit": {"a": a, "b": b},
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
