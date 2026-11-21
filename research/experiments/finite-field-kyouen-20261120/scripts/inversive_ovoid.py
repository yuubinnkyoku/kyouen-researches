"""FAST INVERSIVE PLANE VIA THE ELLIPTIC QUADRIC (OVOID) MODEL.

The PGL(2, F_{q^2}) construction used so far enumerates all triples of
points and applies Mobius maps: O(q^5) work, which is why q >= 9 is slow.

The classical EGGLIKE model is much faster:

    Q(x0,x1,x2,x3) = x0^2 + x0*x1 + a*x1^2 + x2^2 + x2*x3 + b*x3^2

with x^2 + x + a and x^2 + x + b irreducible over F_q.  The quadric
Q = 0 has q^2 + 1 points (an ELLIPTIC QUADRIC / ovoid) in PG(3,q), and the
inversive plane of order q is

    points  = the q^2 + 1 points of the ovoid
    circles = the plane sections of size q + 1

Each plane of PG(3,q) meets the ovoid in 0, 1, 2, or q+1 points; the
q+1-point sections are the circles.  Enumerating planes is O(q^3), and
testing a plane against the ovoid is O(q^2), so the total is O(q^5) in the
worst case but with a tiny constant -- in practice far faster than the
Mobius route because we never enumerate point triples.

This script builds the plane this way and verifies the 3-design axioms.

Run:  python inversive_ovoid.py --q 3 4 5 7 8 9 11 13
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_prime_power import FiniteField, factorize  # noqa: E402


def irreducible_quadratic_with_trace_one(F: FiniteField):
    """Find a such that x^2 + x + a is irreducible over F_q."""
    for a in F.elements():
        # x^2 + x + a irreducible  <=>  no root in F_q
        has_root = False
        for x in F.elements():
            v = F.add(F.add(F.mul(x, x), x), a)
            if F.is_zero(v):
                has_root = True
                break
        if not has_root:
            return a
    raise ValueError("no irreducible x^2+x+a found")


def build_ovoid(q: int):
    """Points of an elliptic quadric in PG(3,q), as normalised 4-tuples.

    General form:  Q = f(x0,x1) + g(x2,x3)  where f and g are irreducible
    binary quadratic forms.  For q odd we may take

        f = x0^2 - d*x1^2,   g = x2^2 - e*x3^2

    with d, e non-squares and d*e a non-square (so the quadric is elliptic).
    For q even we use  f = x0^2 + x0*x1 + a*x1^2  with x^2+x+a irreducible.
    """
    fac = factorize(q)
    if len(fac) != 1:
        raise ValueError(f"q={q} is not a prime power")
    p, e = fac[0]
    F = FiniteField(p, e)
    odd = (p != 2)

    if odd:
        # Standard normal form of an ELLIPTIC quadric in PG(3,q), q odd:
        #
        #     Q = x0^2 + x1^2 + x2^2 + d*x3^2        (d a non-square)
        #
        # This is the classic "x^2+y^2+z^2+d*w^2" form.  Its zero locus has
        # q^2 + 1 points and is an ovoid.
        squares = {F.mul(x, x) for x in F.elements()}
        nonsquares = [c for c in F.elements()
                      if not F.is_zero(c) and c not in squares]
        if not nonsquares:
            raise ValueError("no non-square")
        d = nonsquares[0]

        def Q(v):
            x0, x1, x2, x3 = v
            s = F.add(F.mul(x0, x0), F.mul(x1, x1))
            s = F.add(s, F.mul(x2, x2))
            s = F.add(s, F.mul(d, F.mul(x3, x3)))
            return s
        params = {"d": repr(d)}
    else:
        # characteristic 2: the ELLIPTIC quadric is
        #
        #     Q = x0*x1 + x2^2 + x2*x3 + a*x3^2,     Tr_{F_q/F_2}(a) = 1
        #
        # (The form x0^2 + x0*x1 + a*x1^2 + x2^2 + x2*x3 + b*x3^2 with both
        #  quadratics irreducible is HYPERBOLIC: it has q^2 + 2q + 1 points,
        #  not q^2 + 1.  That mistake was caught by the point count.)
        def trace(c):
            # absolute trace F_q -> F_2:  c + c^2 + c^4 + ... + c^(q/2)
            s = F.zero
            x = c
            k = 1
            while k < q:
                s = F.add(s, x)
                x = F.mul(x, x)
                k *= 2
            return s

        a = None
        for cand in F.elements():
            if not F.is_zero(trace(cand)):
                a = cand
                break
        if a is None:
            raise ValueError("no element of absolute trace 1")

        def Q(v):
            x0, x1, x2, x3 = v
            t = F.add(F.mul(x0, x1), F.mul(x2, x2))
            t = F.add(t, F.mul(x2, x3))
            t = F.add(t, F.mul(a, F.mul(x3, x3)))
            return t
        params = {"a": repr(a)}

    # enumerate projective points of PG(3,q) and keep those on Q = 0
    pts = set()
    for v in itertools.product(F.elements(), repeat=4):
        if all(F.is_zero(c) for c in v):
            continue
        for c in v:
            if not F.is_zero(c):
                inv = F.inv(c)
                pts.add(tuple(F.mul(x, inv) for x in v))
                break
    ovoid = sorted(v for v in pts if F.is_zero(Q(v)))
    return F, params, ovoid


def planes_of_pg3(q: int):
    """All planes of PG(3,q) as normalised coefficient 4-tuples."""
    fac = factorize(q)
    p, e = fac[0]
    F = FiniteField(p, e)
    out = set()
    for c in itertools.product(F.elements(), repeat=4):
        if all(F.is_zero(x) for x in c):
            continue
        for x in c:
            if not F.is_zero(x):
                inv = F.inv(x)
                out.add(tuple(F.mul(y, inv) for y in c))
                break
    return F, sorted(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7, 8])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        t0 = time.time()
        F, params, ovoid = build_ovoid(q)
        t1 = time.time()
        _, planes = planes_of_pg3(q)
        # circles = plane sections of size q+1
        circles = []
        for c in planes:
            sec = []
            for v in ovoid:
                s = F.zero
                for ci, vi in zip(c, v):
                    s = F.add(s, F.mul(ci, vi))
                if F.is_zero(s):
                    sec.append(v)
            if len(sec) == q + 1:
                circles.append(tuple(sorted(sec)))
        circles = sorted(set(circles))
        t2 = time.time()

        # verify the 3-design axioms
        n = len(ovoid)
        tri = Counter()
        for B in circles:
            for t in itertools.combinations(B, 3):
                tri[t] += 1
        expected = n * (n - 1) * (n - 2) // 6
        is_design = (len(tri) == expected and set(tri.values()) == {1})

        row = {"q": q, "params": params, "points": n,
               "expected_points": q * q + 1,
               "circles": len(circles),
               "expected_circles": q * (q * q + 1),
               "circle_sizes": sorted({len(c) for c in circles}),
               "is_3_design": is_design,
               "ovoid_seconds": round(t1 - t0, 2),
               "circles_seconds": round(t2 - t1, 2)}
        rows.append(row)
        print(f"q={q:>3}: points={n} (expect {q*q+1}), "
              f"circles={len(circles)} (expect {q*(q*q+1)}), "
              f"sizes={row['circle_sizes']}, 3-design={is_design}  "
              f"[{t1-t0:.1f}s + {t2-t1:.1f}s]", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
