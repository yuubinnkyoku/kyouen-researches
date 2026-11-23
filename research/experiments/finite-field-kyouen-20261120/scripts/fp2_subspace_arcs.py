"""For q = p^2, test every 2-dimensional F_p-subspace of F_{q^2} as an arc.

At q=9 the extremal 9-arc turns out to be (up to PGammaL) the graph of an
F_3-linear map, i.e. a 2-dimensional F_3-subspace of F_81 = F_{3^4}.  For q = p^2
that generalises naturally: F_{q^2} = F_{p^4} is a 4-dimensional F_p-space, and
every 2-dimensional F_p-subspace has exactly p^2 = q elements, so it is a
q-point subset of the inversive plane.  The question is whether some of them are
arcs -- if so, K(q) = q = p^2 attains the bound K <= q of K1252 for every odd
square order.

The number of such subspaces is the Gaussian binomial
[4 choose 2]_p = (p^2+1)(p^2+p+1), which is small: 130 at p=3, 806 at p=5,
2850 at p=7, 16226 at p=11.

Run:  python fp2_subspace_arcs.py --q 9 25 49
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from inversive_fast import build_circles  # noqa: E402
from inversive_prime_power import factorize  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    results = {}
    for q in args.q:
        fact = factorize(q)
        if len(fact) != 1 or fact[0][1] != 2:
            print(f"q={q}: not a square of a prime power, skipped")
            continue
        p, _ = fact[0]
        F, sub = build_field(q)
        elems = list(F.elements())
        index = {e: i for i, e in enumerate(elems)}
        points, blocks = build_circles(q, check_orbit_size=True)
        n = len(points)
        assert n == q * q + 1
        cmasks = []
        for B in blocks:
            mask = 0
            for pt in B:
                mask |= 1 << pt
            cmasks.append(mask)
        zero = tuple(0 for _ in elems[0])
        one = F.pow(elems[0], 0)

        def add_vec(a, b):
            return tuple((x + y) % p for x, y in zip(a, b))

        def scale(c, a):
            return tuple((c * x) % p for x in a)

        def rank2(v, w):
            # F_p-independence of two vectors over F_p: v not a multiple of w
            if all(x == 0 for x in v) or all(x == 0 for x in w):
                return False
            for c in range(p):
                if scale(c, w) == v:
                    return False
            return True

        seen = set()
        arcs = []
        count = 0
        vectors = [v for v in elems if v != zero]
        for v, w in itertools.combinations(vectors, 2):
            if not rank2(v, w):
                continue
            span = set()
            for a in range(p):
                for b in range(p):
                    span.add(add_vec(scale(a, v), scale(b, w)))
            key = frozenset(span)
            if key in seen:
                continue
            seen.add(key)
            count += 1
            mask = 0
            for e in span:
                mask |= 1 << index[e]
            if all(bin(mask & m).count("1") < 4 for m in cmasks):
                arcs.append(sorted(index[e] for e in span))
        print(f"q={q} (p={p}): {count} two-dimensional F_p-subspaces, "
              f"{len(arcs)} of them are arcs of size {q}", flush=True)
        results[q] = {"subspaces": count, "arcs": len(arcs), "examples": arcs[:3]}

    if args.out:
        import json
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
