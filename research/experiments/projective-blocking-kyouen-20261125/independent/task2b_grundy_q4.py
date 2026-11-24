"""Extra (beyond the minimum asked in task 2): complete Grundy and misere values
for q = 4, computed independently.

Two independent enumerations are used:
  * a literal scan of all 2**21 = 2,097,152 subsets (no DFS) to count the safe
    sets and their sizes,
  * the DFS over safe sets, whose safe-set masks must coincide.

Then Grundy values are computed by decreasing size (mex over safe children) and
the misere win/lose values by the terminal-is-a-win recursion.  This lets us
check the report's q=4 claims: SAFE 180058, Grundy {0:89799, 1:90259},
ROOT 1 0, and the SIZE lines of output/grundy_pg2q4.txt.  It also checks the
parity-graded lemma prediction Grundy(S) = (9 - |S|) mod 2 for every safe S.
"""

from __future__ import annotations

import json
import os
import time

from common import Board, grundy_and_misere, read_board

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
BASE = os.path.dirname(HERE)

CLAIMED = {
    "safe": 180058,
    "grundy": {0: 89799, 1: 90259},
    "root": (1, 0),
    "maximal": {7: 360, 9: 11480},
}
CLAIMED_SIZES = {
    0: (1, 0, 0), 1: (21, 0, 21), 2: (210, 0, 0), 3: (1330, 0, 1330),
    4: (5880, 0, 0), 5: (18648, 0, 18648), 6: (41328, 0, 0),
    7: (58320, 360, 58320), 8: (42840, 0, 0), 9: (11480, 11480, 11480),
}


def parse_grundy_txt(path):
    out = {"size": {}, "grundy": {}}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "SAFE":
                out["safe"] = int(parts[1])
            elif parts[0] == "ROOT":
                out["root"] = (int(parts[1]), int(parts[2]))
            elif parts[0] == "SIZE":
                out["size"][int(parts[1])] = (
                    int(parts[2]), int(parts[3]), int(parts[4]))
            elif parts[0] == "GRUNDY":
                out["grundy"][int(parts[1])] = int(parts[2])
            elif parts[0] == "POINTS":
                out["points"] = int(parts[1])
            elif parts[0] == "CIRCLES":
                out["circles"] = int(parts[1])
    return out


def scan_all_subsets(board):
    """Literal 2**n scan; returns (sizes, by_size) for safe masks."""
    n = board.n
    masks = board.block_masks
    sizes = [0] * (n + 1)
    by_size = [[] for _ in range(n + 1)]
    t0 = time.time()
    for mask in range(1 << n):
        ok = True
        for bm in masks:
            if (mask & bm).bit_count() > board.cap:
                ok = False
                break
        if ok:
            k = mask.bit_count()
            sizes[k] += 1
            by_size[k].append(mask)
    return sizes, by_size, time.time() - t0


def main():
    os.makedirs(OUT, exist_ok=True)
    n, blocks = read_board(os.path.join(BASE, "output", "board_pg2q4.txt"))
    board = Board(n, blocks, cap=3)

    sizes_scan, by_size_scan, scan_seconds = scan_all_subsets(board)
    sizes_dfs, by_size_dfs, maximal = board.enumerate_safe(collect=True)
    dfs_match = all(
        sorted(by_size_scan[k]) == sorted(by_size_dfs[k])
        for k in range(n + 1)
    ) and sizes_scan == sizes_dfs

    t0 = time.time()
    grundy, win = grundy_and_misere(board, by_size_scan)
    dp_seconds = time.time() - t0

    dist = {}
    per_size_grundy0 = [0] * (n + 1)
    for k in range(n + 1):
        for mask in by_size_scan[k]:
            g = grundy[mask]
            dist[g] = dist.get(g, 0) + 1
            if g == 0:
                per_size_grundy0[k] += 1
    dist = dict(sorted(dist.items()))
    root = grundy[0]
    root_misere = 0 if not win[0] else 1

    maximal_hist = {}
    for s in maximal:
        k = s.bit_count()
        maximal_hist[k] = maximal_hist.get(k, 0) + 1

    parity_formula_ok = all(
        grundy[mask] == (9 - mask.bit_count()) % 2
        for k in range(n + 1) for mask in by_size_scan[k]
    )

    engine = parse_grundy_txt(os.path.join(BASE, "output", "grundy_pg2q4.txt"))
    engine_size_ok = {}
    for k in range(n + 1):
        want = (sizes_scan[k], maximal_hist.get(k, 0), per_size_grundy0[k])
        got = engine["size"].get(k, (0, 0, 0))
        engine_size_ok[k] = got == want

    checks = {
        "safe_total": sum(sizes_scan) == CLAIMED["safe"],
        "dfs_matches_literal_scan": dfs_match,
        "grundy_distribution": dist == CLAIMED["grundy"],
        "root": (root, root_misere) == CLAIMED["root"],
        "maximal_by_size": maximal_hist == CLAIMED["maximal"],
        "grundy_in_0_1": set(dist) <= {0, 1},
        "parity_formula_for_all_safe_sets": parity_formula_ok,
        "engine_size_lines": all(engine_size_ok.values()),
        "engine_grundy_lines": engine.get("grundy") == dist,
        "engine_root": engine.get("root") == (root, root_misere),
        "engine_safe": engine.get("safe") == sum(sizes_scan),
    }
    result = {
        "q": 4,
        "n": n,
        "safe_by_size": {int(k): int(v) for k, v in enumerate(sizes_scan) if v},
        "safe_total": sum(sizes_scan),
        "grundy_distribution": {int(k): int(v) for k, v in dist.items()},
        "root_grundy": root,
        "root_misere": root_misere,
        "maximal_by_size": maximal_hist,
        "max_grundy": max(dist),
        "parity_formula": "grundy(S) == (9 - |S|) mod 2 for all safe S",
        "parity_formula_ok": parity_formula_ok,
        "scan_seconds": round(scan_seconds, 1),
        "dp_seconds": round(dp_seconds, 1),
        "checks": checks,
    }
    result["ok"] = all(checks.values())

    print(f"literal scan of all 2^{n} = {1 << n} subsets: {result['scan_seconds']} s")
    print(f"safe sets: {result['safe_total']}  by size: {result['safe_by_size']}")
    print(f"DFS safe-set masks identical to literal scan: {dfs_match}")
    print(f"Grundy DP over {result['safe_total']} safe sets: {result['dp_seconds']} s")
    print(f"Grundy distribution: {result['grundy_distribution']}  max={result['max_grundy']}")
    print(f"root Grundy: {root}   root misere (0=first player loses): {root_misere}")
    print(f"maximal safe sets: {maximal_hist}")
    print(f"parity formula (9-|S|) mod 2 holds for every safe set: {parity_formula_ok}")
    for name, ok in checks.items():
        print(f"  {name}: {'OK' if ok else 'MISMATCH'}")
    print("TASK 2b (q=4 extra):", "PASS" if result["ok"] else "FAIL")
    with open(os.path.join(OUT, "task2b_grundy_q4.json"), "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)


if __name__ == "__main__":
    main()
