"""Build the projective plane boards PG(2,q) for the blocking-set Kyouen game.

Points: canonical representatives of the 1-dimensional subspaces of F_q^3.
Lines: kernels of nonzero linear functionals, i.e. 2-dimensional subspaces.
The game rule is the usual Kyouen one: a position is safe if every line
meets it in at most 3 points.  Equivalently, the complement is a blocking set.

Supports q = 2, 3 (prime field) and q = 4 (GF(4) = {0,1,w,w+1}, w^2 = w+1).

Usage:
    python build_pg2.py --q 2 3 4
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


class PrimeField:
    def __init__(self, p: int):
        self.p = p
        self.elements = list(range(p))

    def add(self, a, b):
        return (a + b) % self.p

    def mul(self, a, b):
        return (a * b) % self.p

    def neg(self, a):
        return (-a) % self.p

    def inv(self, a):
        return pow(a, -1, self.p)

    def zero(self, a):
        return a == 0


class GF4:
    """GF(4) = F_2[w]/(w^2+w+1); element a + b w encoded as a | (b<<1)."""

    def __init__(self):
        self.elements = [0, 1, 2, 3]

    def add(self, a, b):
        return a ^ b

    def mul(self, a, b):
        a0, a1 = a & 1, (a >> 1) & 1
        b0, b1 = b & 1, (b >> 1) & 1
        # (a0+a1 w)(b0+b1 w) = a0b0 + (a0b1+a1b0) w + a1b1 w^2
        # w^2 = w + 1
        c0 = (a0 & b0) ^ (a1 & b1)
        c1 = (a0 & b1) ^ (a1 & b0) ^ (a1 & b1)
        return c0 | (c1 << 1)

    def neg(self, a):
        return a  # characteristic 2

    def inv(self, a):
        assert a != 0
        for b in self.elements:
            if self.mul(a, b) == 1:
                return b
        raise AssertionError

    def zero(self, a):
        return a == 0


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def make_field(q: int):
    if q == 4:
        return GF4()
    if _is_prime(q):
        return PrimeField(q)
    raise ValueError(f"q={q} not supported (prime or 4)")


def canon(F, v, q):
    for c in v:
        if not F.zero(c):
            ci = F.inv(c)
            return tuple(F.mul(x, ci) for x in v)
    raise ValueError("zero vector")


def build(q: int):
    F = make_field(q)
    vecs = [v for v in product(F.elements, repeat=3) if any(not F.zero(x) for x in v)]
    pts = sorted({canon(F, v, q) for v in vecs})
    index = {p: i for i, p in enumerate(pts)}
    assert len(pts) == q * q + q + 1, (q, len(pts))

    funcs = sorted({canon(F, f, q) for f in product(F.elements, repeat=3)
                    if any(not F.zero(x) for x in f)})
    lines = []
    for f in funcs:
        pts_on = [index[p] for p in pts
                  if F.zero(sum_field(F, [F.mul(a, b) for a, b in zip(f, p)]))]
        lines.append(tuple(sorted(pts_on)))
    lines = sorted(set(lines))
    assert len(lines) == q * q + q + 1, (q, len(lines))
    assert all(len(L) == q + 1 for L in lines)
    return len(pts), lines


def sum_field(F, xs):
    s = 0
    for x in xs:
        s = F.add(s, x)
    return s


def check(q: int, blocks: list[tuple[int, ...]]) -> dict:
    v = q * q + q + 1
    pair = {}
    for L in blocks:
        for a, b in combinations(L, 2):
            pair[(a, b)] = pair.get((a, b), 0) + 1
    assert len(pair) == v * (v - 1) // 2
    assert set(pair.values()) == {1}
    return {"v": v, "b": len(blocks), "k": q + 1,
            "pair_lambda": 1, "lines_ok": True}


def write_board(path: Path, n: int, blocks) -> None:
    with path.open("w", encoding="utf-8") as fh:
        fh.write(f"{n} {len(blocks)}\n")
        for B in blocks:
            fh.write(f"{len(B)} " + " ".join(map(str, B)) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {"experiment": "projective-blocking-kyouen-20261125", "boards": []}
    for q in args.q:
        n, blocks = build(q)
        info = check(q, blocks)
        write_board(OUT / f"board_pg2q{q}.txt", n, blocks)
        meta["boards"].append({"q": q, "name": f"PG(2,{q})", **info,
                               "board": f"output/board_pg2q{q}.txt"})
        print(f"PG(2,{q}): v={n} lines={len(blocks)} k={q+1}", flush=True)
    (OUT / "boards_meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
