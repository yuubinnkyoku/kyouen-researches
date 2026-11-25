"""Export the "general position" hypergraph of PG(3,q) in the arc_maxsearch format.

Background
----------
K1250 shows that an arc of the inversive plane of order q is exactly a set of
points of the elliptic quadric Q^-(3,q) with no four coplanar, and that such a
set is the column set of an MDS code [k,4,k-3].  Dropping the "on the quadric"
condition gives the classical object: a set of points of PG(3,q) in general
position (no four coplanar; this already forces no three collinear).  Its
maximum size is the maximum length M_4(q) of a 4-dimensional MDS code over F_q,
so searching it with the same tool measures how much the quadric costs.

For a set in general position a point p may be added to S iff no plane through
p already contains three points of S.  Planes therefore play exactly the role
that circles play for the inversive plane and arc_maxsearch.c can be reused
unchanged, with the planes of PG(3,q) as "blocks":

    points  = (q^4-1)/(q-1)                       projective points
    planes  = (q^4-1)/(q-1)                       (the dual points)
    block   = q^2+q+1 points, each point on q^2+q+1 planes, each pair on q+1

Run:  python pg3_planes.py --q 3 4 5 7 --export
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_prime_power import (  # noqa: E402
    FiniteField, factorize, find_irreducible, is_prime,
)

OUT = Path(__file__).resolve().parent.parent / "output"


# ---------------------------------------------------------------------------
# prime case: the field is Z/q, all arithmetic is integer arithmetic mod q
# ---------------------------------------------------------------------------

def build_prime(q: int):
    def normalise(v):
        for a in v:
            if a % q:
                inv = pow(a, -1, q)
                return tuple((inv * x) % q for x in v)
        raise ValueError("zero vector")

    pts, seen = [], set()
    for a in range(q):
        for b in range(q):
            for c in range(q):
                for d in range(q):
                    if a == b == c == d == 0:
                        continue
                    w = normalise((a, b, c, d))
                    if w not in seen:
                        seen.add(w)
                        pts.append(w)
    planes, seen_p, seen_n = [], set(), set()
    for a in range(q):
        for b in range(q):
            for c in range(q):
                for d in range(q):
                    if a == b == c == d == 0:
                        continue
                    y = normalise((a, b, c, d))
                    if y in seen_p:
                        continue
                    seen_p.add(y)
                    block = tuple(i for i, p in enumerate(pts)
                                  if sum(yk * pk for yk, pk in zip(y, p)) % q == 0)
                    assert len(block) == q * q + q + 1
                    planes.append(block)
    return pts, planes


# ---------------------------------------------------------------------------
# prime power case: generic field arithmetic
# ---------------------------------------------------------------------------

def build_prime_power(q: int):
    p, e = factorize(q)[0]
    F = FiniteField(p, e, find_irreducible(p, e))
    one = F.pow(F.elements()[0], 0)
    zero = F.sub(one, one)
    elems = list(F.elements())

    def normalise(v):
        for a in v:
            if not F.is_zero(a):
                inv = F.div(one, a)
                return tuple(F.mul(inv, x) for x in v)
        raise ValueError("zero vector")

    def dot(x, y):
        acc = zero
        for a, b in zip(x, y):
            acc = F.add(acc, F.mul(a, b))
        return acc

    pts, seen = [], set()
    for a in elems:
        for b in elems:
            for c in elems:
                for d in elems:
                    if all(F.is_zero(t) for t in (a, b, c, d)):
                        continue
                    w = normalise((a, b, c, d))
                    if w not in seen:
                        seen.add(w)
                        pts.append(w)
    planes, seen_p = [], set()
    for a in elems:
        for b in elems:
            for c in elems:
                for d in elems:
                    if all(F.is_zero(t) for t in (a, b, c, d)):
                        continue
                    y = normalise((a, b, c, d))
                    if y in seen_p:
                        continue
                    seen_p.add(y)
                    block = tuple(i for i, p in enumerate(pts) if F.is_zero(dot(y, p)))
                    planes.append(block)
    return pts, planes


def design_check(q: int, n: int, planes) -> dict:
    sizes = Counter(len(B) for B in planes)
    inc = Counter()
    for B in planes:
        for p in B:
            inc[p] += 1
    pair = Counter()
    for B in planes:
        for i in range(len(B)):
            for j in range(i + 1, len(B)):
                pair[(B[i], B[j])] += 1
    expected = q ** 3 + q ** 2 + q + 1
    return {
        "q": q, "n": n, "b": len(planes),
        "n_expected": expected, "b_expected": expected,
        "block_sizes": sorted(sizes), "size_expected": q * q + q + 1,
        "point_incidence": sorted(set(inc.values())),
        "incidence_expected": q * q + q + 1,
        "pair_multiplicity": sorted(set(pair.values())),
        "pair_expected": q + 1,
        "ok": (n == expected and len(planes) == expected
               and set(sizes) == {q * q + q + 1}
               and set(inc.values()) == {q * q + q + 1}
               and set(pair.values()) == {q + 1}),
    }


def write_blocks(path: Path, n: int, planes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write(f"{n} {len(planes)}\n")
        for B in planes:
            fh.write(f"{len(B)} " + " ".join(str(x) for x in B) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--export", action="store_true")
    args = ap.parse_args()

    ok_all = True
    for q in args.q:
        pts, planes = (build_prime(q) if is_prime(q) else build_prime_power(q))
        info = design_check(q, len(pts), planes)
        ok_all &= info["ok"]
        print(f"q={q}: n={info['n']} b={info['b']} sizes={info['block_sizes']} "
              f"inc={info['point_incidence']} pair={info['pair_multiplicity']} "
              f"-> {'OK' if info['ok'] else 'FAIL'}", flush=True)
        if args.export:
            path = OUT / f"pg3q{q}.txt"
            write_blocks(path, len(pts), planes)
            print(f"  wrote {path} ({path.stat().st_size} bytes)", flush=True)

    if not ok_all:
        raise SystemExit("PG(3,q) plane design check FAILED")


if __name__ == "__main__":
    main()
