"""Build the Suzuki-Tits inversive plane of order q = 2^(2e+1) for a given q.

The Tits ovoid in PG(3,q) has the classical form

    O = {(1, x^sigma + x y + y^(sigma+2), x, y) : x, y in F_q} u {(0:1:0:0)},
    sigma = 2^(e+1),   q = 2^(2e+1),

which the q=8 exponent search confirmed (K1254).  The circles are the plane
sections of size q+1; this script builds them and writes them in the
arc_census.txt format so searches and censuses can run on the non-Miquelian
board.

Checks: |O| = q^2+1, the number of circles = q(q^2+1), and the pair-incidence
count (every pair on (v-2)/(k-2) = q+1 circles for a 3-design).

Run:  python tits_build.py --q 32 --out ../output/circles_tits_q32.txt
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_prime_power import FiniteField, factorize, find_irreducible  # noqa: E402


def tits_ovoid(q: int):
    p, m = factorize(q)[0]
    assert p == 2 and m % 2 == 1 and m >= 3, "Tits ovoids exist for q = 2^(2e+1)"
    F = FiniteField(p, m, find_irreducible(p, m))
    elems = list(F.elements())
    one = F.pow(elems[0], 0)
    zero = F.sub(one, one)
    mul, add = F.mul, F.add
    sigma = 2 ** ((m - 1) // 2 + 1)
    ovoid = []
    seen = set()
    for x in elems:
        for y in elems:
            f = add(add(F.pow(x, sigma), mul(x, y)), F.pow(y, sigma + 2))
            v = (one, f, x, y)
            if v not in seen:
                seen.add(v)
                ovoid.append(v)
    ovoid.append((zero, one, zero, zero))
    return F, elems, ovoid, sigma


def build(q: int):
    F, elems, ovoid, sigma = tits_ovoid(q)
    one = F.pow(elems[0], 0)
    zero = F.sub(one, one)
    mul, add = F.mul, F.add
    index = {v: i for i, v in enumerate(ovoid)}
    n = len(ovoid)

    # projective points of PG(3,q) as normalised tuples (to parametrise planes)
    seen = set()
    pts = []
    for v in itertools.product(elems, repeat=4):
        if all(F.is_zero(x) for x in v):
            continue
        inv = None
        for x in v:
            if not F.is_zero(x):
                inv = F.div(one, x)
                break
        nv = tuple(mul(inv, x) for x in v)
        if nv in seen:
            continue
        seen.add(nv)
        pts.append(nv)

    circles = set()
    for a in pts:
        block = []
        for v in ovoid:
            s = zero
            for k in range(4):
                s = add(s, mul(a[k], v[k]))
            if F.is_zero(s):
                block.append(index[v])
        if len(block) == q + 1:
            circles.add(tuple(sorted(block)))
    circles = sorted(circles)
    return q, n, ovoid, circles


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    q, n, ovoid, circles = build(args.q)
    print(f"q={args.q}: Tits ovoid with {n} points, {len(circles)} circles "
          f"(expected {q * (q * q + 1)})")

    # pair incidence check: for a 3-design each pair lies on (v-2)/(k-2) circles
    from collections import Counter
    pair_count = Counter()
    for blk in circles:
        for pr in itertools.combinations(blk, 2):
            pair_count[pr] += 1
    expected = (n - 2) // (q - 1)
    vals = set(pair_count.values())
    print(f"pairs covered: {len(pair_count)} of {n * (n - 1) // 2}; "
          f"multiplicities {sorted(vals)} (3-design expects all {expected})")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        fh.write(f"{n} {len(circles)}\n")
        for b in circles:
            fh.write(f"{len(b)} " + " ".join(str(i) for i in b) + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
