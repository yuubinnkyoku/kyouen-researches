"""Is the maximum arc at q=9 unique up to the automorphism group?

At q=9 the exact maximum arc size is K=9 and there are exactly 29,520 nine-arcs
(K1058, K1253).  This script takes one of them and walks its orbit under
PGammaL(2,q^2) = PGL(2,q^2) . Gal(F_{q^2}/F_p) using the generators

    z -> z+1,  z -> lambda*z,  z -> 1/z,  z -> z^p

If the orbit has all 29,520 arcs then the extremal arc is unique up to symmetry.

Run:  python max_arc_orbit.py --q 9 --arc 6,18,45,20,17,61,77,0,22
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from inversive_fast import build_circles  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--arc", type=str, required=True)
    ap.add_argument("--cap", type=int, default=200000)
    args = ap.parse_args()
    q = args.q
    arc0 = frozenset(int(x) for x in args.arc.split(","))

    F, sub = build_field(q)
    points, blocks = build_circles(q, check_orbit_size=True)
    idx = {p: i for i, p in enumerate(points)}
    elems = list(F.elements())
    one = F.pow(elems[0], 0)

    # a primitive element of F_{q^2}
    order = q * q - 1

    def order_of(x):
        cur = one
        for k in range(1, order + 1):
            cur = F.mul(cur, x)
            if cur == one:
                return k
        return None

    lam = None
    for x in elems:
        if F.is_zero(x) or x == one:
            continue
        if order_of(x) == order:
            lam = x
            break
    if lam is None:
        raise SystemExit("no primitive element")

    p = min(F.p for _ in [0]) if hasattr(F, "p") else None
    # field characteristic: derive from the field order
    n_field = len(elems)
    for cand in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        k = 1
        v = cand
        while v < n_field:
            v *= cand
        if v == n_field:
            p = cand
            break
    if p is None:
        raise SystemExit("cannot determine the characteristic")

    def apply(fn, arc):
        out = set()
        for i in arc:
            z = points[i]
            w = fn(z)
            if w is None:
                out.add(idx[None])
            else:
                out.add(idx[w])
        return frozenset(out)

    gens = [
        lambda z: None if z is None else F.add(z, one),
        lambda z: None if z is None else F.mul(lam, z),
        # z -> 1/z with infinity mapped to 0 (a genuine Moebius map)
        lambda z: (F.sub(one, one) if z is None else
                   (None if F.is_zero(z) else F.div(one, z))),
        lambda z: None if z is None else F.pow(z, p),
    ]

    seen = {arc0}
    frontier = [arc0]
    while frontier:
        nxt = []
        for arc in frontier:
            for g in gens:
                img = apply(g, arc)
                if len(img) != len(arc):
                    continue
                if img in seen:
                    continue
                seen.add(img)
                nxt.append(img)
                if len(seen) > args.cap:
                    print(f"q={q}: orbit exceeds cap {args.cap}")
                    return
        frontier = nxt
    print(f"q={q}: orbit size {len(seen)}  (total {len(arc0)}-arcs known: 29,520 at q=9)")
    print(f"  single orbit? {len(seen) == 29520}")


if __name__ == "__main__":
    main()
