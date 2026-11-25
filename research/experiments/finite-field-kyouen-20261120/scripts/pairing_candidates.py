"""Test whether the second player's win at q=7 has a pairing strategy.

A *pairing strategy* for the second player is a fixed-point-free involution pi
of the point set such that: whenever the position S is a pi-invariant safe set
and p is a legal move, the reply pi(p) is also legal, i.e. S + p + pi(p) is
again safe.  If such a pi exists the second player wins by always answering
pi(p), and the q=7 anomaly gets a constructive explanation.

All automorphisms of the Miquelian plane M(q) are Moebius maps (composed with a
field automorphism), so up to conjugacy the only fixed-point-free involutions
are  z -> c/z  with c a non-square in F_{q^2}.  Hence testing one such c
settles the existence question.

This script writes the pairing for a given q as a plain list, so the C checker
(pairing_check.c) can test it on the enumerated safe sets.

Run:  python pairing_candidates.py --q 7 --out ../output/pairing_q7.txt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from inversive_fast import build_circles  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "output"


def find_nonsquare(F):
    one = F.pow(F.elements()[0], 0)
    for x in F.elements():
        if F.is_zero(x) or x == one:
            continue
        # x is a non-square iff x^((|F|-1)/2) != 1
        n = len(F.elements()) - 1
        if F.pow(x, n // 2) != one:
            return x
    raise AssertionError("no non-square found")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    q = args.q

    points, blocks = build_circles(q, check_orbit_size=True)
    F, sub = build_field(q)
    elems = list(F.elements())
    # identical point order to what build_circles uses: F.elements() then infinity
    assert points[:len(elems)] == elems and points[-1] is None
    c = find_nonsquare(F)
    one = F.pow(c, 0)

    pairing = []
    for p in points:
        if p is None:
            pairing.append(elems.index(F.sub(one, one)))      # infinity -> 0
        elif F.is_zero(p):
            pairing.append(len(points) - 1)                    # 0 -> infinity
        else:
            pairing.append(elems.index(F.mul(c, F.div(one, p))))

    # sanity: pi is an involution without fixed points
    n = len(points)
    assert all(pairing[pairing[i]] == i for i in range(n)), "not an involution"
    assert all(pairing[i] != i for i in range(n)), "has fixed points"
    print(f"q={q}: non-square c={c}, fixed-point-free involution on {n} points")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8") as fh:
            fh.write(f"{n}\n")
            for i in range(n):
                fh.write(f"{pairing[i]}\n")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
