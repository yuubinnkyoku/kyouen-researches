"""The inversive-plane game: the faithful finite analogue of the cocircular game.

The AG(2,q) board of ff_kyouen.py has a defect: over F_q the form x^2+y^2 is
isotropic exactly when q = 1 mod 4, so the "circles" degenerate into line pairs
and the game changes character with q mod 4.

The standard finite analogue of "circles in the Euclidean plane" is the
**inversive plane** (Mobius plane) of order q: a 3-(q^2+1, q+1, 1) design whose
blocks are called circles.  Every three points lie on exactly one circle and
every circle has exactly q+1 points -- the exact finite counterpart of
"three points determine a circle".

Classical model (projective line over F_{q^2}):

    points  = P^1(F_{q^2})                     (q^2 + 1 of them)
    circles = images of P^1(F_q) under PGL(2, F_{q^2})

This model exists for every prime power q, so the q mod 4 dichotomy disappears.
The game: players alternately occupy points; a move completing 4 points on a
common circle loses (complete-call rule, K0001).

This script builds the design, verifies the 3-design axioms, and reports the
game-theoretic invariants for small q.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path


# ---------------------------------------------------------------- F_{q^2}


class GF:
    """F_p[t]/(t^2 - d), d a non-residue mod p.  Elements are (a, b) = a + b t."""

    def __init__(self, p: int, d: int) -> None:
        self.p = p
        self.d = d % p
        if any((i * i) % p == self.d for i in range(p)):
            raise ValueError(f"d={d} is a square mod {p}")
        self.zero = (0, 0)
        self.one = (1, 0)

    def add(self, x, y):
        return ((x[0] + y[0]) % self.p, (x[1] + y[1]) % self.p)

    def sub(self, x, y):
        return ((x[0] - y[0]) % self.p, (x[1] - y[1]) % self.p)

    def mul(self, x, y):
        a, b = x
        c, e = y
        return ((a * c + b * e * self.d) % self.p, (a * e + b * c) % self.p)

    def inv(self, x):
        a, b = x
        norm = (a * a - b * b * self.d) % self.p
        if norm == 0:
            raise ZeroDivisionError
        ninv = pow(norm, -1, self.p)
        return ((a * ninv) % self.p, (-b * ninv) % self.p)

    def div(self, x, y):
        return self.mul(x, self.inv(y))

    def elements(self):
        return [(a, b) for a in range(self.p) for b in range(self.p)]


def find_non_residue(p: int) -> int:
    for d in range(2, p):
        if not any((i * i) % p == d for i in range(p)):
            return d
    raise ValueError(f"no non-residue mod {p}")


# ---------------------------------------------------------------- P^1(F_{q^2})


def projective_line(F: GF):
    """P^1(F_{q^2}) as affine coordinates a/b plus the point at infinity."""
    out = set()
    for b in F.elements():
        if b == F.zero:
            continue
        for a in F.elements():
            out.add(F.div(a, b))
    return sorted(out) + [None]


def mobius(F: GF, z, t0, t1, t2):
    """The unique Mobius map with 0 -> t0, 1 -> t1, infinity -> t2, at z."""
    if z is None:
        return t2
    if z == F.zero:
        return t0
    if z == F.one:
        return t1
    # f(z) = (a z + b)/(c z + d) with a/c = t2; take c = 1, a = t2.
    # f(0) = b/d = t0  =>  b = t0 d
    # f(1) = (t2 + t0 d)/(1 + d) = t1  =>  d (t0 - t1) = t1 - t2
    den_d = F.sub(t0, t1)
    if den_d == F.zero:
        raise ZeroDivisionError("degenerate triple")
    d = F.div(F.sub(t1, t2), den_d)
    b = F.mul(t0, d)
    num = F.add(F.mul(t2, z), b)
    den = F.add(z, d)
    if den == F.zero:
        return None
    return F.div(num, den)


def circles_of_inversive_plane(F: GF, points):
    """Images of P^1(F_q) under PGL(2, F_{q^2})."""
    base = [(x, 0) for x in range(F.p)] + [None]
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
                if len(img) == F.p + 1:
                    circles.add(img)
    return circles


def verify_design(points, circles) -> dict:
    """Check the 3-(q^2+1, q+1, 1) axioms."""
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


def game_invariants(points, circles) -> dict:
    """Safe-set census and Grundy values for the complete-call game."""
    n = len(points)
    idx = {p: i for i, p in enumerate(points)}
    blocks = [sorted(idx[p] for p in c) for c in circles]
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)

    def can_add(i: int, pmask: int) -> bool:
        for bi in through[i]:
            cnt = 0
            for j in blocks[bi]:
                if pmask >> j & 1:
                    cnt += 1
                    if cnt >= 3:
                        return False
        return True

    # enumerate safe sets by size
    by_size: dict[int, list[int]] = {}
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        by_size.setdefault(pmask.bit_count(), []).append(pmask)
        for i in range(start, n):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask):
                stack.append((i + 1, pmask | (1 << i)))

    g: dict[int, int] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            reach = set()
            for i in range(n):
                if pmask >> i & 1:
                    continue
                if can_add(i, pmask):
                    reach.add(g[pmask | (1 << i)])
            m = 0
            while m in reach:
                m += 1
            g[pmask] = m

    layer = {k: len(v) for k, v in sorted(by_size.items())}
    min_maximal = None
    for size in sorted(by_size):
        for pmask in by_size[size]:
            if all(pmask >> i & 1 or not can_add(i, pmask) for i in range(n)):
                min_maximal = size
                break
        if min_maximal is not None:
            break

    gdist = Counter(g.values())
    first = Counter(g[1 << i] for i in range(n))
    return {
        "safe_sets": sum(layer.values()),
        "layer_sizes": layer,
        "max_safe_size": max(layer),
        "min_maximal_size": min_maximal,
        "empty_grundy": g[0],
        "empty_outcome": "P(second-player-win)" if g[0] == 0 else "N(first-player-win)",
        "grundy_distribution": dict(sorted(gdist.items())),
        "max_grundy": max(gdist),
        "first_move_grundy_distribution": dict(sorted(first.items())),
        "first_moves_winning": sum(c for v, c in first.items() if v == 0),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5])
    ap.add_argument("--game", action="store_true", help="also compute Grundy values")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        d = find_non_residue(q)
        F = GF(q, d)
        points = projective_line(F)
        circles = circles_of_inversive_plane(F, points)
        design = verify_design(points, circles)
        row = {"q": q, "field": f"F_{q}[t]/(t^2-{d})", **design}
        if args.game:
            row.update(game_invariants(points, circles))
        rows.append(row)
        print(
            f"q={q}: points={design['points']} (expect {q*q+1})  "
            f"circles={design['circles']} (expect {q*(q*q+1)})  "
            f"sizes={design['circle_sizes']}  "
            f"3-design={design['is_3_design']}  "
            f"missing_triples={design['triples_missing']}",
            flush=True,
        )
        if args.game:
            print(
                f"     safe={row['safe_sets']} K={row['max_safe_size']} "
                f"s={row['min_maximal_size']} g(empty)={row['empty_grundy']} "
                f"gdist={row['grundy_distribution']}",
                flush=True,
            )

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
