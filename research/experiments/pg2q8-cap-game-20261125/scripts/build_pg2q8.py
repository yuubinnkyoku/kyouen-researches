"""Build PG(2,8) from GF(8) = GF(2)[x]/(x^3+x+1).

Points: canonical nonzero vectors of GF(8)^3 (first nonzero coordinate 1).
Lines: 2D GF(8)-subspaces: for each pair p,q the 9 projective points
{canon(a p + b q) : (a,b) != (0,0)}.

Usage:
    python build_pg2q8.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def gmul(a: int, b: int) -> int:
    r = 0
    for i in range(3):
        if (b >> i) & 1:
            r ^= a << i
    for bit in (5, 4, 3):
        if (r >> bit) & 1:
            r ^= 0b1011 << (bit - 3)
    return r & 7


def ginv(a: int) -> int:
    for y in range(1, 8):
        if gmul(a, y) == 1:
            return y
    raise ValueError(a)


def canon(v: tuple[int, int, int]):
    for x in v:
        if x:
            inv = ginv(x)
            return tuple(gmul(inv, z) for z in v)
    return None


def main() -> None:
    vecs = [(a, b, c) for a in range(8) for b in range(8) for c in range(8)
            if (a, b, c) != (0, 0, 0)]
    pts = sorted({canon(v) for v in vecs})
    idx = {p: i for i, p in enumerate(pts)}
    assert len(pts) == 73, len(pts)
    lines = set()
    for i, p in enumerate(pts):
        for q in pts[i + 1:]:
            L = {idx[canon(tuple(gmul(a, p[k]) ^ gmul(b, q[k]) for k in range(3)))]
                 for a in range(8) for b in range(8) if (a, b) != (0, 0)}
            assert len(L) == 9, len(L)
            lines.add(tuple(sorted(L)))
    lines = sorted(lines)
    assert len(lines) == 73, len(lines)
    deg = [0] * 73
    for L in lines:
        for p in L:
            deg[p] += 1
    assert set(deg) == {9}
    # every pair on exactly one line
    pair = {}
    for L in lines:
        for i in range(9):
            for j in range(i + 1, 9):
                key = (L[i], L[j])
                pair[key] = pair.get(key, 0) + 1
    assert len(pair) == 73 * 72 // 2 and set(pair.values()) == {1}
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "board_pg2q8.txt").open("w", encoding="utf-8") as fh:
        fh.write(f"73 {len(lines)}\n")
        for L in lines:
            fh.write("9 " + " ".join(map(str, L)) + "\n")
    (OUT / "board_meta.json").write_text(json.dumps({
        "board": "PG(2,8)", "n": 73, "lines": len(lines), "k": 9,
        "pair_lambda": 1, "points": [list(p) for p in pts],
    }, indent=1), encoding="utf-8")
    print("PG(2,8): 73 points, 73 lines of 9; pair lambda 1; point degree 9")


if __name__ == "__main__":
    main()
