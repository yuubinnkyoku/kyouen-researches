"""Independent exhaustive solver for K_s(q) on small boards (no SAT dependency).

Depth-first search over the points in a degree-descending order with two
prunings:
  * trivial: len(S) + (remaining points) <= best;
  * addability: a point that cannot be added to S now can never be added later,
    because circle counts only grow, so len(S) + #(individually addable
    remaining points) is an upper bound.
This is exact.  Used to cross-check the SAT results for q <= 5.

Usage:
    python brute_force.py --q 3 --s 3 4
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def solve(q: int, s: int) -> dict:
    board = json.loads((OUT / f"board_q{q}.json").read_text(encoding="utf-8"))
    v, blocks = board["v"], board["blocks"]
    if s >= q + 1:
        return {"q": q, "s": s, "exact": v, "nodes": 0, "seconds": 0.0}
    if s <= 2:
        return {"q": q, "s": s, "exact": s, "nodes": 0, "seconds": 0.0}
    pc = [[] for _ in range(v)]
    for c, b in enumerate(blocks):
        for p in b:
            pc[p].append(c)
    order = sorted(range(v), key=lambda p: -len(pc[p]))
    counts = [0] * len(blocks)
    best = [0]
    best_set: list[list[int]] = []
    nodes = [0]
    t0 = time.time()

    def addable(p: int) -> bool:
        return all(counts[c] < s for c in pc[p])

    def dfs(i: int, chosen: list[int]) -> None:
        nodes[0] += 1
        if len(chosen) > best[0]:
            best[0] = len(chosen)
            best_set.clear()
            best_set.append(list(chosen))
        if i == v:
            return
        ub = len(chosen) + sum(1 for j in range(i, v) if addable(order[j]))
        if ub <= best[0]:
            return
        p = order[i]
        if addable(p):
            for c in pc[p]:
                counts[c] += 1
            chosen.append(p)
            dfs(i + 1, chosen)
            chosen.pop()
            for c in pc[p]:
                counts[c] -= 1
        dfs(i + 1, chosen)

    dfs(0, [])
    return {"q": q, "s": s, "exact": best[0], "witness": best_set[0],
            "nodes": nodes[0], "seconds": round(time.time() - t0, 2)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--s", type=int, nargs="+", required=True)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    rows = [solve(args.q, s) for s in args.s]
    print(json.dumps(rows, indent=1))
    if args.out:
        args.out.write_text(json.dumps(rows, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
