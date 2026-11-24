"""Complete Grundy values for the general s-parameter Kyouen game.

Board: board file (n, blocks).  Safe set: |S ∩ B| <= s for every block.
Normal play (no move loses) and misere (no move wins), complete Grundy.

Method: DFS enumeration of all safe sets grouped by size, then a descending DP
over sizes.  For n <= 25 a bytearray indexed by the bitmask stores the Grundy
values (255 = not a safe set).

Usage:
    python grundy_general.py --board output/board_ag2q4.txt --s 2 --name AG2(4)_s2
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def load(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    blocks = [tuple(map(int, l.split()[1:])) for l in lines[1:]]
    assert len(blocks) == b
    return n, blocks


def popcount(x: int) -> int:
    return x.bit_count()


def enumerate_safe(n: int, blocks, s: int):
    b = len(blocks)
    pc = [[] for _ in range(n)]
    for c, B in enumerate(blocks):
        for p in B:
            pc[p].append(c)
    counts = [0] * b
    by_size: dict[int, list[int]] = {}

    def rec(mask: int, size: int, start: int):
        by_size.setdefault(size, []).append(mask)
        for p in range(start, n):
            if (mask >> p) & 1:
                continue
            if all(counts[c] < s for c in pc[p]):
                for c in pc[p]:
                    counts[c] += 1
                rec(mask | (1 << p), size + 1, p + 1)
                for c in pc[p]:
                    counts[c] -= 1

    rec(0, 0, 0)
    return by_size, pc


def solve(n: int, blocks, s: int):
    t0 = time.time()
    by_size, pc = enumerate_safe(n, blocks, s)
    safe_total = sum(len(v) for v in by_size.values())
    t_enum = time.time() - t0
    line_masks = [sum(1 << p for p in B) for B in blocks]
    g = bytearray([255]) * (1 << n)
    mis = bytearray(1 << n)  # 0 = losing for player to move, 1 = winning
    maximal: dict[int, int] = {}
    max_size = max(by_size)
    full = (1 << n) - 1
    for size in range(max_size, -1, -1):
        for mask in by_size[size]:
            saturated = 0
            for L, LM in zip(line_masks, line_masks):
                if (mask & LM).bit_count() == s:
                    saturated |= LM
            addable = full & ~mask & ~saturated
            if not addable:
                maximal[size] = maximal.get(size, 0) + 1
            mex = set()
            # misere: a player with no move WINS
            mis_win = 1 if not addable else 0
            a = addable
            while a:
                low = a & -a
                ch = mask | low
                mex.add(g[ch])
                if mis[ch] == 0:
                    mis_win = 1
                a ^= low
            m = 0
            while m in mex:
                m += 1
            g[mask] = m
            mis[mask] = mis_win
    elapsed = time.time() - t0
    sizes = {k: len(v) for k, v in sorted(by_size.items())}
    grundy_dist: Counter = Counter()
    for v in g:
        if v != 255:
            grundy_dist[v] += 1

    return {
        "n": n, "blocks": len(blocks), "s": s,
        "safe": safe_total, "size_counts": sizes,
        "max_size": max_size,
        "maximal_by_size": dict(sorted(maximal.items())),
        "root_grundy": g[0], "root_misere_win": mis[0],
        "grundy_dist": dict(sorted(grundy_dist.items())),
        "enum_seconds": round(t_enum, 3), "total_seconds": round(elapsed, 3),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", type=Path, required=True)
    ap.add_argument("--s", type=int, required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--out", type=Path, default=OUT / "grundy_general.json")
    args = ap.parse_args()
    n, blocks = load(args.board)
    rec = solve(n, blocks, args.s)
    rec["name"] = args.name
    rec["board"] = str(args.board).replace("\\", "/")
    data = (json.loads(args.out.read_text(encoding="utf-8"))
            if args.out.exists() else {"games": []})
    data["games"] = [x for x in data["games"] if x.get("name") != args.name]
    data["games"].append(rec)
    data["games"].sort(key=lambda x: x["name"])
    args.out.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
