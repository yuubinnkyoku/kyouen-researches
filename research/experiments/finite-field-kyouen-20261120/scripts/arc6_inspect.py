"""Inspect arcs6 internals at even q."""

from __future__ import annotations

import sys
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_k6_pure import arcs6, N_xy, H  # noqa: E402


def main() -> None:
    for q in (4, 8, 16):
        val, detail = arcs6(q)
        n = q * q + 1
        b = q * (q * q + 1)
        s = q + 1
        print(f"=== q={q} ===")
        print(f"  n={n}, b={b}, s={s}")
        print(f"  C(n,6) = {comb(n, 6)}")
        print(f"  term6 = {detail['term6']}")
        print(f"  term5 = {detail['term5']}")
        print(f"  contrib = {detail['contrib']}")
        print(f"  result = {Fraction(val)}")
        print("  contrib breakdown:")
        for n2, cnt in N_xy(q).items():
            n1 = s - 2 * n2
            h0, h1, h2 = H(n2, n1, 0, 4), H(n2, n1, 1, 4), H(n2, n1, 2, 4)
            part = b * cnt * (h0 + Fraction(h1, 2) + Fraction(h2, 3))
            print(f"    n2={n2}, cnt={cnt}, n1={n1}, "
                  f"H=({h0},{h1},{h2}), part={part}")
        print()


if __name__ == "__main__":
    main()
