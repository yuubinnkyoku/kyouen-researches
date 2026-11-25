"""Structure of maximal safe sets on PG(2,q) (complements = minimal multiple
blocking sets).

DFS enumerates safe sets (<=3 points on every line); whenever no point can be
added, the set is maximal.  For each maximal size class the first representative
is reported together with the line-intersection profile of its complement and
the d-fold blocking check (d = q-2).

Usage:
    python structure_pg2.py --q 3 4
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
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
        blocks.append(tuple(parts[1:]))
    line_masks = [sum(1 << p for p in L) for L in blocks]
    point_lines = [[] for _ in range(n)]
    for i, L in enumerate(blocks):
        for p in L:
            point_lines[p].append(i)
    return n, blocks, line_masks, point_lines


def popcount(x: int) -> int:
    return bin(x).count("1")


def enumerate_maximal(q: int, limit_per_size: int = 1):
    n, blocks, line_masks, point_lines = read_board(q)
    counts = [0] * len(blocks)
    reps: dict[int, list[int]] = {}
    size_counts: Counter = Counter()
    maximal: Counter = Counter()

    def addable_points(mask: int) -> list[int]:
        out = []
        for p in range(n):
            if (mask >> p) & 1:
                continue
            if all(counts[c] < 3 for c in point_lines[p]):
                out.append(p)
        return out

    def dfs(mask: int, size: int, start: int):
        ext = addable_points(mask)
        if not ext:
            maximal[size] += 1
            if len(reps.setdefault(size, [])) < limit_per_size:
                reps[size].append(mask)
            return
        for p in ext:
            if p < start:
                continue
            for c in point_lines[p]:
                counts[c] += 1
            dfs(mask | (1 << p), size + 1, p + 1)
            for c in point_lines[p]:
                counts[c] -= 1

    # DFS from the empty set; this enumerates each maximal set once if we only
    # recurse forward in point order.
    dfs(0, 0, 0)
    return n, blocks, line_masks, point_lines, maximal, reps


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--out", type=Path, default=OUT / "structure.json")
    args = ap.parse_args()
    data = (json.loads(args.out.read_text(encoding="utf-8"))
            if args.out.exists() else {})
    for q in args.q:
        if str(q) in data:
            continue
        n, blocks, line_masks, point_lines, maximal, reps = enumerate_maximal(q)
        d = q - 2
        rows = {}
        for size, masks in sorted(reps.items()):
            mask = masks[0]
            comp = ((1 << n) - 1) ^ mask
            prof = Counter(popcount(comp & B) for B in line_masks)
            rows[str(size)] = {
                "count": maximal[size],
                "complement_size": n - size,
                "complement_profile": dict(sorted(prof.items())),
                "d_fold_min": min(prof),
                "d": d,
                "d_fold_ok": min(prof) >= d,
                "representative_safe": [p for p in range(n) if (mask >> p) & 1],
            }
        data[str(q)] = {"v": n, "maximal_counts": dict(sorted(maximal.items())),
                        "size_classes": rows}
        print(f"q={q}: maximal {dict(sorted(maximal.items()))}", flush=True)
        for k, row in rows.items():
            print(f"  safe size {k}: complement {row['complement_size']} "
                  f"profile {row['complement_profile']}", flush=True)
        args.out.write_text(json.dumps(data, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
