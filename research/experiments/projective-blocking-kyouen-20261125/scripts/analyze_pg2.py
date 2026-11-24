"""Analyse the blocking-set Kyouen game on PG(2,3) and PG(2,4).

- enumerate all safe sets and maximal safe sets (v <= 21, bitmasks);
- classify maximal safe sets by size and by PGL(3,q)-orbit;
- identify minimal blocking sets (complements of maximal safe sets);
- print line-intersection profiles and small structural invariants.

Usage:
    python analyze_pg2.py --q 3 [--q 4]
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def read_board(q: int):
    lines = (OUT / f"board_pg2q{q}.txt").read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    blocks = []
    for line in lines[1:]:
        parts = list(map(int, line.split()))
        blocks.append(sum(1 << x for x in parts[1:]))
    return n, blocks


def popcount(x: int) -> int:
    return bin(x).count("1")


def safe_masks(q: int):
    n, blocks = read_board(q)
    safe = []
    maximal = []
    by_size = {}
    for mask in range(1 << n):
        k = popcount(mask)
        if all(popcount(mask & B) <= 3 for B in blocks):
            safe.append(mask)
            by_size.setdefault(k, []).append(mask)
    for k, lst in by_size.items():
        for mask in lst:
            if all(not all(popcount((mask | (1 << p)) & B) <= 3 for B in blocks)
                   for p in range(n) if not (mask >> p) & 1):
                maximal.append(mask)
    return n, blocks, safe, maximal, by_size


def pgl3_orbits(q: int, masks: list[int], n: int) -> list[list[int]]:
    """Orbits of masks under PGL(3,q) (permutation action on the points)."""
    # points as canonical vectors
    from itertools import product as prod
    F_el = list(range(q))
    # build point list identical to build_pg2.py
    def canon(v):
        for c in v:
            if c % q:
                ci = pow(c, -1, q)
                return tuple((x * ci) % q for x in v)
        raise ValueError
    pts = sorted({canon(v) for v in prod(F_el, repeat=3) if any(v)})
    pos = {p: i for i, p in enumerate(pts)}
    perms = set()
    for a, b, c, d, e, f, g, h, i in product(F_el, repeat=9):
        det = (a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)) % q
        if det == 0:
            continue
        M = ((a, b, c), (d, e, f), (g, h, i))
        img = []
        ok = True
        for p in pts:
            v = ((a * p[0] + b * p[1] + c * p[2]) % q,
                 (d * p[0] + e * p[1] + f * p[2]) % q,
                 (g * p[0] + h * p[1] + i * p[2]) % q)
            if not any(v):
                ok = False
                break
            img.append(pos[canon(v)])
        if ok:
            perms.add(tuple(img))
    unseen = set(masks)
    orbits = []
    while unseen:
        m = next(iter(unseen))
        orbit = set()
        stack = [m]
        while stack:
            cur = stack.pop()
            if cur in orbit:
                continue
            orbit.add(cur)
            bits = [p for p in range(n) if (cur >> p) & 1]
            for perm in perms:
                new = 0
                for p in bits:
                    new |= 1 << perm[p]
                if new not in orbit:
                    stack.append(new)
        unseen -= orbit
        orbits.append(sorted(orbit))
    return orbits


def profile(mask: int, blocks: list[int], n: int) -> dict:
    from collections import Counter
    c = Counter(popcount(mask & B) for B in blocks)
    return dict(sorted(c.items()))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    args = ap.parse_args()
    out = {}
    for q in args.q:
        n, blocks, safe, maximal, by_size = safe_masks(q)
        sizes = {k: len(v) for k, v in sorted(by_size.items())}
        max_size = max(sizes)
        max_masks = by_size[max_size]
        max_sizes = [k for k, v in by_size.items() if any(
            m in maximal for m in v)]
        # maximal sets by size
        max_by_size = {}
        for mask in maximal:
            k = popcount(mask)
            max_by_size.setdefault(k, []).append(mask)
        row = {
            "q": q, "v": n, "safe": len(safe), "K": max_size,
            "size_counts": sizes,
            "maximal_by_size": {k: len(v) for k, v in sorted(max_by_size.items())},
            "minimal_blocking_sizes": sorted(n - k for k in max_by_size),
        }
        # orbit decomposition of maximal sets per size
        orbits = {}
        for k, lst in sorted(max_by_size.items()):
            if q <= 3:  # PGL(3,4) is far too large to enumerate this way
                orb = pgl3_orbits(q, lst, n)
                orbits[str(k)] = {"num_orbits": len(orb),
                                  "orbit_sizes": sorted(len(o) for o in orb),
                                  "representatives": [[p for p in range(n)
                                                       if (m >> p) & 1]
                                                      for m in (o[0] for o in orb)]}
            else:
                orbits[str(k)] = {"num_orbits": None,
                                  "profiles": [profile(m, blocks, n) for m in lst[:5]]}
        row["orbits"] = orbits
        out[f"q{q}"] = row
        print(json.dumps(row, indent=1)[:4000], flush=True)
    (OUT / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
