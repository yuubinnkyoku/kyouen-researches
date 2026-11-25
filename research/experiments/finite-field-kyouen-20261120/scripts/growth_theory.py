"""Theoretical upper bound for K on a 3-(v, s, 1) design.

For the inversive plane of order q: v = q^2+1 points, s = q+1 points per circle,
b = q(q^2+1) circles, and every triple lies on exactly one circle.

A safe set S has |S cap C| <= 3 for every circle C.

TRIPLE COUNTING (the standard bound):
    Each triple of S lies on exactly one circle, and that circle holds at most
    3 points of S.  So distinct triples of S lie on distinct circles:
        C(k,3) <= b = q(q^2+1) ~ q^3
    giving k = O(q).

But the observed K is much smaller (~q^{1/3}).  Why?

The triple bound is weak because it only uses "each triple has its own circle".
The real constraint is stronger: the circles through the triples of S must be
DISTINCT AND COMPATIBLE.  In particular, if two triples share two points, their
circles share those two points, and two distinct circles meet in at most 2
points -- so that is allowed.  But if two triples share ONE point, their circles
meet in that point and possibly others.

Let us look for a stronger counting argument.

PAIR-BASED COUNTING:
    For each pair {p,q} of S, the circles through p and q form a pencil.  In the
    inversive plane, the number of circles through two given points is q-1
    (the circles through p and q correspond to the q-1 remaining "directions").
    Each such circle can hold at most 3 points of S, so at most one more point
    of S.  Hence the pairs of S are "spread out" over the pencils.

    Counting: sum over circles C of C(|S cap C|, 2) = (number of circles through
    a pair) * C(k,2) = (q-1) * C(k,2).
    Since |S cap C| <= 3, C(|S cap C|,2) <= 3, so
        (q-1) C(k,2) <= 3b = 3q(q^2+1)
        C(k,2) <= 3q(q^2+1)/(q-1) ~ 3q^2
        k <= sqrt(6) q ~ 2.45 q.
    Still linear in q, not q^{1/3}.

So the elementary counting bounds give k = O(q), but the observed K is O(q^{1/3}).
The gap is large.  This suggests the true bound is NOT captured by simple
counting, and the observed small K may be a small-q phenomenon.

Let me test: is K really growing like q^{1/3}, or is the fit misleading?
With only 5 data points (q=3,4,5,7,8) and K in {5,5,6,6,7}, the fit is very
unreliable.  A linear fit K ~ a + b*q would also fit.

This script compares fits and computes what the counting bounds predict.
"""

from __future__ import annotations

import argparse
import json
import math
from math import comb
from pathlib import Path


INVERSIVE = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    qs = sorted(INVERSIVE)
    ks = [INVERSIVE[q] for q in qs]

    print("data:", dict(zip(qs, ks)))
    print()

    # fit 1: K = c * q^alpha  (log-log)
    xs = [math.log(q) for q in qs]
    ys = [math.log(k) for k in ks]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    alpha = (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
             / sum((x - mx) ** 2 for x in xs))
    c1 = math.exp(my - alpha * mx)
    r1 = sum((y - (math.log(c1) + alpha * x)) ** 2 for x, y in zip(xs, ys))

    # fit 2: K = a + b*q  (linear)
    mq, mk = sum(qs) / n, sum(ks) / n
    b2 = (sum((q - mq) * (k - mk) for q, k in zip(qs, ks))
          / sum((q - mq) ** 2 for q in qs))
    a2 = mk - b2 * mq
    r2 = sum((k - (a2 + b2 * q)) ** 2 for q, k in zip(qs, ks))

    # fit 3: K = a + b*log(q)
    ml = sum(xs) / n
    b3 = (sum((x - ml) * (k - mk) for x, k in zip(xs, ks))
          / sum((x - ml) ** 2 for x in xs))
    a3 = mk - b3 * ml
    r3 = sum((k - (a3 + b3 * x)) ** 2 for x, k in zip(xs, ks))

    print(f"fit K = c*q^alpha : c={c1:.3f}, alpha={alpha:.3f}, SSE={r1:.4f}")
    print(f"fit K = a + b*q   : a={a2:.3f}, b={b2:.4f}, SSE={r2:.4f}")
    print(f"fit K = a + b*log q: a={a3:.3f}, b={b3:.3f}, SSE={r3:.4f}")
    print()

    # counting bounds
    print("counting bounds vs observed:")
    print(f"{'q':>3} {'observed':>9} {'triple':>8} {'pair':>8}")
    rows = []
    for q in qs:
        b = q * (q * q + 1)
        # triple bound
        kt = 3
        while comb(kt + 1, 3) <= b:
            kt += 1
        # pair bound: (q-1)*C(k,2) <= 3b
        kp = 2
        while (q - 1) * comb(kp + 1, 2) <= 3 * b:
            kp += 1
        rows.append({"q": q, "observed": INVERSIVE[q], "triple_bound": kt,
                     "pair_bound": kp})
        print(f"{q:>3} {INVERSIVE[q]:>9} {kt:>8} {kp:>8}")

    print()
    print("CONCLUSION: the elementary counting bounds give k = O(q),")
    print("but the observed K is 5..7 for q up to 8.  The 'q^0.33' fit is")
    print("based on 5 points with K in {5,5,6,6,7} and is NOT reliable.")
    print("A linear fit K ~ a + b*q fits comparably well.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "fits": {
                "power": {"c": c1, "alpha": alpha, "sse": r1},
                "linear": {"a": a2, "b": b2, "sse": r2},
                "log": {"a": a3, "b": b3, "sse": r3},
            },
            "bounds": rows,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
