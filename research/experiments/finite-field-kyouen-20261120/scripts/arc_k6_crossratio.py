"""THE (C,T) CONFIGURATION TYPE IS THE CROSS-RATIO ORBIT.

At q=7 the (C,T) pairs split into two classes of sizes 14,700 and 9,800.
Since there are b = 350 circles and C(q+1,4) = C(8,4) = 70 four-subsets per
circle, the per-circle split is

    14700 / 350 = 42
     9800 / 350 = 28

So the 70 four-subsets of a circle fall into two PGL(2,q)-orbits of sizes
42 and 28.

THE EXPLANATION.  A circle is a copy of P^1(F_q).  The group PGL(2,q) acts
on P^1(F_q) 3-transitively, so it acts on 4-subsets, and the ORBIT of a
4-subset is its "configuration type".  The invariant is the CROSS-RATIO
class: normalise three of the four points to 0, 1, infinity; the fourth
lands at some t, and the orbit is determined by the set

    { t, 1/t, 1-t, 1/(1-t), t/(t-1), (t-1)/t }

(the six values obtained by permuting the four points).

For q=5: P^1(F_5) has 6 points, C(6,4) = 15 four-subsets, and they form a
SINGLE orbit -- hence one type, hence uniform N_j.

For q=7: P^1(F_7) has 8 points, C(8,4) = 70 four-subsets, forming TWO
orbits of sizes 42 and 28.

This script verifies the orbit structure directly.

Run:  python arc_k6_crossratio.py --q 5 7
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_prime_power import FiniteField, factorize  # noqa: E402


def p1(q: int):
    """P^1(F_q) as a list, with None for infinity."""
    fac = factorize(q)
    p, e = fac[0]
    F = FiniteField(p, e)
    return F, list(F.elements()) + [None]


def mobius_orbits_on_4subsets(q: int):
    """Orbits of PGL(2,q) on 4-subsets of P^1(F_q)."""
    F, pts = p1(q)
    idx = {repr(x): i for i, x in enumerate(pts)}
    n = len(pts)

    # generate PGL(2,q) as the group of Mobius maps; act on 4-subsets
    # Instead of building the whole group, use the cross-ratio invariant:
    # two 4-subsets are equivalent iff their cross-ratio sets coincide.
    def cross_ratio_set(quad):
        """The set of 6 cross-ratio values (as a frozenset of reprs)."""
        vals = set()
        for perm in itertools.permutations(quad):
            z1, z2, z3, z4 = perm
            # (z1,z2;z3,z4) = (z1-z3)(z2-z4) / ((z1-z4)(z2-z3))
            def sub(a, b):
                if a is None and b is None:
                    return F.zero
                if a is None:
                    return None
                if b is None:
                    return a
                return F.sub(a, b)

            def mul(a, b):
                if a is None or b is None:
                    return None
                return F.mul(a, b)

            def div(a, b):
                if b is None:
                    return F.zero
                if a is None:
                    return None
                if F.is_zero(b):
                    return None
                return F.div(a, b)

            t = div(mul(sub(z1, z3), sub(z2, z4)),
                    mul(sub(z1, z4), sub(z2, z3)))
            vals.add(repr(t))
        return frozenset(vals)

    orbits = Counter()
    for quad in itertools.combinations(range(n), 4):
        cr = cross_ratio_set([pts[i] for i in quad])
        orbits[cr] += 1
    return n, orbits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        n, orbits = mobius_orbits_on_4subsets(q)
        sizes = sorted(orbits.values(), reverse=True)
        row = {"q": q, "p1_size": n, "four_subsets": sum(sizes),
               "num_orbits": len(orbits), "orbit_sizes": sizes}
        rows.append(row)
        print(f"q={q}: |P^1(F_q)| = {n}, C(n,4) = {sum(sizes)}", flush=True)
        print(f"  PGL(2,q)-orbits on 4-subsets: {len(orbits)}", flush=True)
        print(f"  orbit sizes: {sizes}", flush=True)
        for cr, cnt in sorted(orbits.items(), key=lambda x: -x[1]):
            print(f"    size {cnt}: cross-ratio set {sorted(cr)}", flush=True)

    print()
    print("The orbit sizes must match the observed (C,T) class sizes:")
    print("  q=5: 1 orbit  -> uniform N_j          (observed: 1 class)")
    print("  q=7: 2 orbits -> two N_j classes      (observed: 42 and 28)")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
