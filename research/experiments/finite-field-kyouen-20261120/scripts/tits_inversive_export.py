"""Build the Suzuki-Tits inversive plane of order 8 and export its circles.

The Tits ovoid of PG(3,8) (q = 2^3, sigma = 2^2 = 4) has the classical form

    O = {(1, x^sigma + x y + y^(sigma+2), x, y) : x, y in F_8} u {(0:1:0:0)},

verified by the earlier exponent search (f = x^4 + xy + y^6 works, the quadric
f = x^2+xy+y^2 is the elliptic-quadric case).  The inversive plane carries the
3-(65,9,1) design whose circles are the plane sections with 9 points; this script
writes those circles in the arc_census.txt format so that the arc census (and
hence the maximum arc size) can be computed for this NON-Miquelian plane, which
the literature has not studied.

Run:  python tits_inversive_export.py --q 8 --out ../output/circles_tits_q8.txt
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_prime_power import FiniteField, factorize, find_irreducible  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=8)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    q = args.q
    p, m = factorize(q)[0]
    F = FiniteField(p, m, find_irreducible(p, m))
    elems = list(F.elements())
    one = F.pow(elems[0], 0)
    zero = F.sub(one, one)
    mul, add = F.mul, F.add

    def normalise(v):
        if all(F.is_zero(x) for x in v):
            return None
        inv = None
        for x in v:
            if not F.is_zero(x):
                inv = F.div(one, x)
                break
        return tuple(mul(inv, x) for x in v)

    # Tits ovoid
    sigma = 2 ** (m // 2 + 1)          # e = (m-1)/2, sigma = 2^(e+1)
    ovoid = set()
    for x in elems:
        for y in elems:
            f = add(add(F.pow(x, sigma), mul(x, y)), F.pow(y, sigma + 2))
            ovoid.add((one, f, x, y))
    ovoid.add((zero, one, zero, zero))
    assert len(ovoid) == q * q + 1, len(ovoid)
    print(f"q={q}, sigma={sigma}: Tits ovoid with {len(ovoid)} points")

    pts = sorted(ovoid)
    index = {v: i for i, v in enumerate(pts)}

    # check it is an ovoid: every line has at most 2 points
    n_lines = 0
    bad = 0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            cnt = 0
            for lam in elems:
                nv = normalise(tuple(add(pts[i][k], mul(lam, pts[j][k])) for k in range(4)))
                if nv is not None and nv in ovoid:
                    cnt += 1
            if cnt > 2:
                bad += 1
                if bad == 1:
                    print("line with >2 points of the ovoid:", pts[i], pts[j], cnt)
    print(f"ovoid check: {bad} bad lines")

    # plane sections with q+1 = 9 points are the circles
    all_pts = []
    seen = set()
    for v in itertools.product(elems, repeat=4):
        nv = normalise(v)
        if nv is None or nv in seen:
            continue
        seen.add(nv)
        all_pts.append(nv)

    circles = []
    for a in all_pts:
        block = []
        for v in ovoid:
            s = zero
            for k in range(4):
                s = add(s, mul(a[k], v[k]))
            if F.is_zero(s):
                block.append(index[v])
        if len(block) == q + 1:
            circles.append(sorted(block))
    circles = sorted(set(tuple(b) for b in circles))
    print(f"plane sections of size {q+1}: {len(circles)} circles "
          f"(expected {q * (q * q + 1)})")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        fh.write(f"{q * q + 1} {len(circles)}\n")
        for b in circles:
            fh.write(f"{len(b)} " + " ".join(str(i) for i in b) + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
