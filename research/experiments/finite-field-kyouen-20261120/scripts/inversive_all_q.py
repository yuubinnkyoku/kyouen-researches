"""Inversive planes of prime-power order, including characteristic 2.

The construction in inversive_prime_power.py uses F_{q^2} = F_q[u]/(u^2 - d),
which requires q odd (a non-square d must exist).  For q = 2^e this fails.

General construction used here:

    F_{q^2} = F_p[t]/(f)   with f irreducible of degree 2e over F_p,
    F_q     = { x in F_{q^2} : x^q = x }        (the fixed field of Frobenius)

Then the inversive plane of order q is

    points  = P^1(F_{q^2})
    circles = images of P^1(F_q) under PGL(2, F_{q^2})

This works for every prime power q, odd or even.

Note on q = 2: the inversive plane of order 2 has 5 points and 5 circles of
size 3, so no 4 points can ever be concyclic -- the game is trivial (every
point is always playable).  It is included for completeness.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from inversive_prime_power import (
    FiniteField,
    factorize,
    find_irreducible,
    is_prime,
)


def build_field(q: int) -> tuple[FiniteField, list]:
    """Return (F_{q^2}, list of F_q elements embedded in it)."""
    fac = factorize(q)
    if len(fac) != 1:
        raise ValueError(f"q={q} is not a prime power")
    p, e = fac[0]
    F = FiniteField(p, 2 * e, find_irreducible(p, 2 * e))
    sub = [x for x in F.elements() if F.pow(x, q) == x]
    if len(sub) != q:
        raise AssertionError(f"subfield has {len(sub)} elements, expected {q}")
    return F, sub


def projective_line(F: FiniteField):
    out = set()
    for b in F.elements():
        if F.is_zero(b):
            continue
        for a in F.elements():
            out.add(F.div(a, b))
    return sorted(out) + [None]


def mobius(F: FiniteField, z, t0, t1, t2):
    if z is None:
        return t2
    if F.is_zero(z):
        return t0
    if z == F.one:
        return t1
    den_d = F.sub(t0, t1)
    if F.is_zero(den_d):
        raise ZeroDivisionError("degenerate triple")
    d = F.div(F.sub(t1, t2), den_d)
    b = F.mul(t0, d)
    num = F.add(F.mul(t2, z), b)
    den = F.add(z, d)
    if F.is_zero(den):
        return None
    return F.div(num, den)


def circles_of_inversive_plane(F: FiniteField, sub, points):
    # sub already holds elements of F (the fixed field of Frobenius)
    base = list(sub) + [None]
    circles = set()
    for t0 in points:
        if t0 is None:
            continue
        for t1 in points:
            if t1 is None or t1 == t0:
                continue
            for t2 in points:
                if t2 is None or t2 == t0 or t2 == t1:
                    continue
                img = frozenset(mobius(F, z, t0, t1, t2) for z in base)
                if len(img) == len(sub) + 1:
                    circles.add(img)
    return circles


def verify_design(points, circles) -> dict:
    n = len(points)
    idx = {p: i for i, p in enumerate(points)}
    blocks = [frozenset(idx[p] for p in c) for c in circles]
    triple_count = Counter()
    for b in blocks:
        for tri in itertools.combinations(sorted(b), 3):
            triple_count[tri] += 1
    all_triples = set(itertools.combinations(range(n), 3))
    covered = set(triple_count)
    return {
        "points": n,
        "circles": len(blocks),
        "circle_sizes": dict(sorted(Counter(len(b) for b in blocks).items())),
        "triples_total": len(all_triples),
        "triples_covered": len(covered),
        "triples_missing": len(all_triples - covered),
        "max_triple_multiplicity": max(triple_count.values()) if triple_count else 0,
        "is_3_design": covered == all_triples and all(v == 1 for v in triple_count.values()),
    }


def build_inversive_plane(q: int):
    F, sub = build_field(q)
    points = projective_line(F)
    circles = circles_of_inversive_plane(F, sub, points)
    return points, circles


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[2, 3, 4, 5, 7, 8, 9])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        try:
            points, circles = build_inversive_plane(q)
        except Exception as exc:  # noqa: BLE001
            print(f"q={q}: FAILED ({type(exc).__name__}: {exc})", flush=True)
            rows.append({"q": q, "error": f"{type(exc).__name__}: {exc}"})
            continue
        design = verify_design(points, circles)
        rows.append({"q": q, **design})
        print(f"q={q}: points={design['points']} (expect {q*q+1})  "
              f"circles={design['circles']} (expect {q*(q*q+1)})  "
              f"sizes={design['circle_sizes']}  3-design={design['is_3_design']}",
              flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
