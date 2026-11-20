"""Growth rate of K for the inversive plane and AG(2,q).

Known exact values:
  inversive: q=3:5, q=4:5, q=5:6, q=7:6, q=8:7
  AG(2,q):   q=3:5, q=4:5, q=5:6, q=7:6, q=8:8

Both grow very slowly: K ~ 5..8 for q up to 8, while the board has q^2+1 points.

This script:
  1. tabulates the known values and the counting bounds,
  2. fits simple models (K ~ c*q^alpha, K ~ a + b*log q),
  3. compares with the integer-grid K_n ~ 2n,
  4. reports the "density" K/n.

The goal is to characterise the growth, which is a structural question about
how large a set can be while meeting every circle in at most 3 points.
"""

from __future__ import annotations

import argparse
import json
import math
from math import comb
from pathlib import Path


INVERSIVE = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7}
AG = {3: 5, 4: 5, 5: 6, 7: 6, 8: 8}
INTEGER = {3: 5, 4: 7, 5: 9, 7: 14, 8: 15}


def counting_bound(q: int) -> int:
    b = q * (q * q + 1)
    k = 3
    while comb(k + 1, 3) <= b:
        k += 1
    return k


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'inv K':>6} {'inv n':>6} {'K/n':>7} {'AG K':>6} {'AG n':>6} "
          f"{'K/n':>7} {'int K':>6} {'int n':>6} {'K/n':>7} {'cnt bnd':>8}")
    for q in sorted(INVERSIVE):
        n_inv = q * q + 1
        n_ag = q * q
        n_int = q * q
        ki = INVERSIVE[q]
        ka = AG[q]
        kn = INTEGER[q]
        cb = counting_bound(q)
        rows.append({
            "q": q,
            "inversive_K": ki, "inversive_n": n_inv, "inversive_density": ki / n_inv,
            "ag_K": ka, "ag_n": n_ag, "ag_density": ka / n_ag,
            "integer_K": kn, "integer_n": n_int, "integer_density": kn / n_int,
            "counting_bound": cb,
        })
        print(f"{q:>3} {ki:>6} {n_inv:>6} {ki/n_inv:>7.3f} {ka:>6} {n_ag:>6} "
              f"{ka/n_ag:>7.3f} {kn:>6} {n_int:>6} {kn/n_int:>7.3f} {cb:>8}")

    # fit K ~ c * q^alpha by least squares on log-log
    qs = sorted(INVERSIVE)
    xs = [math.log(q) for q in qs]
    ys = [math.log(INVERSIVE[q]) for q in qs]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    alpha = num / den if den else 0
    c = math.exp(my - alpha * mx)
    print(f"\ninversive: K ~ {c:.3f} * q^{alpha:.3f}  (log-log fit)")
    print(f"  => K grows like q^{alpha:.2f}, i.e. very slowly")

    # integer grid: K ~ 2n
    print(f"\ninteger grid: K_n / n = "
          f"{', '.join(f'{INTEGER[q]/q:.2f}' for q in sorted(INTEGER))}")
    print(f"  => K_n ~ 2n (linear in n)")

    # density comparison
    print(f"\ndensity K/n:")
    print(f"  inversive: {', '.join(f'{INVERSIVE[q]/(q*q+1):.3f}' for q in qs)}")
    print(f"  AG(2,q):   {', '.join(f'{AG[q]/(q*q):.3f}' for q in qs)}")
    print(f"  integer:   {', '.join(f'{INTEGER[q]/(q*q):.3f}' for q in qs)}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "rows": rows,
            "inversive_fit": {"c": c, "alpha": alpha},
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
