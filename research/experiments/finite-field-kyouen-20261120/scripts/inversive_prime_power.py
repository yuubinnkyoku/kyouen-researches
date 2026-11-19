"""Inversive planes of prime-power order: q = 4, 8, 9, ...

The existing inversive_plane.py only handles prime q, because it builds
F_{q^2} as F_q[t]/(t^2 - d) with d a non-residue mod q, which needs q prime.

For prime powers q = p^e we need F_q itself as F_p[t]/(f(t)) for an irreducible
f of degree e, and then F_{q^2} = F_q[u]/(u^2 - d) with d a non-residue in F_q.

This module provides:

  * a general finite field F_{p^e} with elements as tuples of e coefficients,
  * irreducibility testing and a search for an irreducible polynomial,
  * the quadratic extension F_{q^2},
  * the inversive plane of order q as P^1(F_{q^2}) with circles = images of
    P^1(F_q) under PGL(2, F_{q^2}),
  * verification of the 3-(q^2+1, q+1, 1) design axioms.

Everything is exact integer arithmetic.
"""

from __future__ import annotations

import itertools
from collections import Counter


# ---------------------------------------------------------------- F_p


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def factorize(n: int) -> list[tuple[int, int]]:
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            out.append((d, e))
        d += 1
    if n > 1:
        out.append((n, 1))
    return out


# ---------------------------------------------------------------- F_{p^e}


class FiniteField:
    """F_{p^e} = F_p[t]/(f(t)).  Elements are coefficient tuples of length e."""

    def __init__(self, p: int, e: int, f: tuple[int, ...] | None = None) -> None:
        if not is_prime(p):
            raise ValueError(f"{p} is not prime")
        self.p = p
        self.e = e
        self.q = p ** e
        if f is None:
            f = find_irreducible(p, e)
        if len(f) != e + 1 or f[-1] != 1:
            raise ValueError("f must be monic of degree e")
        self.f = f  # f[0] + f[1] t + ... + t^e
        self.zero = tuple([0] * e)
        self.one = tuple([1] + [0] * (e - 1))

    # -- polynomial helpers over F_p -------------------------------------

    def _poly_mulmod(self, a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
        p, e, f = self.p, self.e, self.f
        prod = [0] * (2 * e - 1)
        for i, ai in enumerate(a):
            if ai == 0:
                continue
            for j, bj in enumerate(b):
                if bj == 0:
                    continue
                prod[i + j] = (prod[i + j] + ai * bj) % p
        # reduce by f: t^e = -(f[0] + f[1] t + ... + f[e-1] t^{e-1})
        for k in range(2 * e - 2, e - 1, -1):
            c = prod[k]
            if c == 0:
                continue
            prod[k] = 0
            for j in range(e):
                prod[k - e + j] = (prod[k - e + j] - c * f[j]) % p
        return tuple(prod[:e])

    def add(self, a, b):
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def sub(self, a, b):
        return tuple((x - y) % self.p for x, y in zip(a, b))

    def neg(self, a):
        return tuple((-x) % self.p for x in a)

    def mul(self, a, b):
        return self._poly_mulmod(a, b)

    def is_zero(self, a) -> bool:
        return all(x == 0 for x in a)

    def elements(self):
        return list(itertools.product(range(self.p), repeat=self.e))

    def pow(self, a, n: int):
        result = self.one
        base = a
        while n:
            if n & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            n >>= 1
        return result

    def inv(self, a):
        if self.is_zero(a):
            raise ZeroDivisionError
        # a^(q-2) = a^{-1} in a field
        return self.pow(a, self.q - 2)

    def div(self, a, b):
        return self.mul(a, self.inv(b))

    def is_square(self, a) -> bool:
        if self.is_zero(a):
            return True
        return self.pow(a, (self.q - 1) // 2) == self.one


def poly_eval(coeffs: tuple[int, ...], x: int, p: int) -> int:
    v = 0
    for c in reversed(coeffs):
        v = (v * x + c) % p
    return v


def is_irreducible(f: tuple[int, ...], p: int) -> bool:
    """Irreducibility over F_p by checking for roots and small factors.

    For degree <= 3 this is exact: a polynomial of degree 2 or 3 over a field is
    irreducible iff it has no root.  For higher degree we fall back to a
    trial-division check against all monic polynomials of degree <= deg/2.
    """
    d = len(f) - 1
    if d == 1:
        return True
    if d <= 3:
        return all(poly_eval(f, x, p) != 0 for x in range(p))
    # general: trial division by monic polys of degree 1..d//2
    for k in range(1, d // 2 + 1):
        for g in itertools.product(range(p), repeat=k):
            g = tuple(g) + (1,)
            if _poly_divides(g, f, p):
                return False
    return True


def _poly_divides(g: tuple[int, ...], f: tuple[int, ...], p: int) -> bool:
    """True iff g divides f over F_p (g monic)."""
    rem = list(f)
    dg = len(g) - 1
    for i in range(len(rem) - 1, dg - 1, -1):
        c = rem[i] % p
        if c == 0:
            continue
        for j in range(dg + 1):
            rem[i - dg + j] = (rem[i - dg + j] - c * g[j]) % p
    return all(x % p == 0 for x in rem[:dg])


def find_irreducible(p: int, e: int) -> tuple[int, ...]:
    if e == 1:
        return (0, 1)
    for coeffs in itertools.product(range(p), repeat=e):
        f = tuple(coeffs) + (1,)
        if is_irreducible(f, p):
            return f
    raise ValueError(f"no irreducible of degree {e} over F_{p}")


# ---------------------------------------------------------------- F_{q^2}


class QuadraticExtension:
    """F_{q^2} = F_q[u]/(u^2 - d), d a non-square in F_q."""

    def __init__(self, base: FiniteField) -> None:
        self.base = base
        self.d = None
        for cand in base.elements():
            if base.is_zero(cand):
                continue
            if not base.is_square(cand):
                self.d = cand
                break
        if self.d is None:
            raise ValueError("no non-square found (q must be odd)")
        self.zero = (base.zero, base.zero)
        self.one = (base.one, base.zero)

    def add(self, x, y):
        b = self.base
        return (b.add(x[0], y[0]), b.add(x[1], y[1]))

    def sub(self, x, y):
        b = self.base
        return (b.sub(x[0], y[0]), b.sub(x[1], y[1]))

    def mul(self, x, y):
        b = self.base
        a1, b1 = x
        a2, b2 = y
        return (b.add(b.mul(a1, a2), b.mul(b.mul(b1, b2), self.d)),
                b.add(b.mul(a1, b2), b.mul(b1, a2)))

    def inv(self, x):
        b = self.base
        a, c = x
        norm = b.sub(b.mul(a, a), b.mul(b.mul(c, c), self.d))
        if b.is_zero(norm):
            raise ZeroDivisionError
        ninv = b.inv(norm)
        return (b.mul(a, ninv), b.neg(b.mul(c, ninv)))

    def div(self, x, y):
        return self.mul(x, self.inv(y))

    def is_zero(self, x) -> bool:
        return self.base.is_zero(x[0]) and self.base.is_zero(x[1])

    def elements(self):
        return [(a, c) for a in self.base.elements() for c in self.base.elements()]


# ---------------------------------------------------------------- P^1


def projective_line(F: QuadraticExtension):
    """P^1(F_{q^2}) as affine coordinates a/b plus the point at infinity."""
    out = set()
    for b in F.elements():
        if F.is_zero(b):
            continue
        for a in F.elements():
            out.add(F.div(a, b))
    return sorted(out) + [None]


def mobius(F: QuadraticExtension, z, t0, t1, t2):
    """Unique Mobius map with 0 -> t0, 1 -> t1, infinity -> t2, evaluated at z."""
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


def circles_of_inversive_plane(F: QuadraticExtension, points):
    """Images of P^1(F_q) under PGL(2, F_{q^2})."""
    base = [(x, F.base.zero) for x in F.base.elements()] + [None]
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
                if len(img) == F.base.q + 1:
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
    """Return (points, circles) for the inversive plane of order q (prime power)."""
    fac = factorize(q)
    if len(fac) != 1:
        raise ValueError(f"q={q} is not a prime power")
    p, e = fac[0]
    base = FiniteField(p, e)
    F = QuadraticExtension(base)
    points = projective_line(F)
    circles = circles_of_inversive_plane(F, points)
    return points, circles


def main() -> None:
    import argparse
    import json
    from pathlib import Path

    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7, 8, 9])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        try:
            points, circles = build_inversive_plane(q)
        except Exception as exc:  # noqa: BLE001
            print(f"q={q}: FAILED ({exc})", flush=True)
            rows.append({"q": q, "error": str(exc)})
            continue
        design = verify_design(points, circles)
        row = {"q": q, **design}
        rows.append(row)
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
