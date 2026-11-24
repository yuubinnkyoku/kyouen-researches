"""Build PG(2,9) from GF(9) = GF(3)[x]/(x^2+1).

Points: canonical nonzero vectors of GF(9)^3 (first nonzero coordinate 1).
Lines: 2D GF(9)-subspaces (91 lines of 10 points).

Usage:
    python build_pg2q9.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def add(a, b):
    return ((a[0] + b[0]) % 3, (a[1] + b[1]) % 3)


def mul(a, b):
    # (a0 + a1 i)(b0 + b1 i) = a0 b0 - a1 b1 + (a0 b1 + a1 b0) i, i^2 = -1 = 2
    return ((a[0] * b[0] - a[1] * b[1]) % 3, (a[0] * b[1] + a[1] * b[0]) % 3)


E = [(a, b) for a in range(3) for b in range(3)]


def inv(a):
    for y in E:
        if mul(a, y) == (1, 0):
            return y
    raise ValueError(a)


def canon(v):
    for x in v:
        if x != (0, 0):
            ix = inv(x)
            return tuple(mul(ix, z) for z in v)
    return None


def main() -> None:
    pts = sorted({canon(v) for v in ((a, b, c) for a in E for b in E for c in E)
                  if v != ((0, 0), (0, 0), (0, 0))})
    idx = {p: i for i, p in enumerate(pts)}
    assert len(pts) == 91
    lines = set()
    for i, p in enumerate(pts):
        for q in pts[i + 1:]:
            L = {idx[canon(tuple(add(mul(a, p[k]), mul(b, q[k])) for k in range(3)))]
                 for a in E for b in E if (a, b) != ((0, 0), (0, 0))}
            assert len(L) == 10
            lines.add(tuple(sorted(L)))
    lines = sorted(lines)
    assert len(lines) == 91
    deg = [0] * 91
    for L in lines:
        for p in L:
            deg[p] += 1
    assert set(deg) == {10}
    pair = {}
    for L in lines:
        for i in range(10):
            for j in range(i + 1, 10):
                key = (L[i], L[j])
                pair[key] = pair.get(key, 0) + 1
    assert len(pair) == 91 * 90 // 2 and set(pair.values()) == {1}
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "board_pg2q9.txt").open("w", encoding="utf-8") as fh:
        fh.write(f"91 {len(lines)}\n")
        for L in lines:
            fh.write("10 " + " ".join(map(str, L)) + "\n")
    (OUT / "board_meta.json").write_text(json.dumps({
        "board": "PG(2,9)", "n": 91, "lines": len(lines), "k": 10,
        "pair_lambda": 1,
    }, indent=1), encoding="utf-8")
    print("PG(2,9): 91 points, 91 lines of 10; pair lambda 1; point degree 10")


if __name__ == "__main__":
    main()
