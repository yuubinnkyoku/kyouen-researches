#!/usr/bin/env python3
"""Stage 1: verify the board is PG(2,4) and enumerate all s=3-safe sets by DFS.

Python standard library only.  Run from anywhere; paths are anchored at the
repository root inferred from this file's location.
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BOARD_PATH = ROOT / "research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q4.txt"
OUT = HERE / "stage1.json"

N = 21


def parse_board(path: Path):
    raw = path.read_text(encoding="utf-8").splitlines()
    first = raw[0].split()
    assert len(first) == 2, f"bad header: {raw[0]!r}"
    n, nlines = int(first[0]), int(first[1])
    assert n == N and nlines == N, f"header says {n} {nlines}, expected {N} {N}"
    lines = []
    for i, ln in enumerate(raw[1:], start=1):
        parts = [int(x) for x in ln.split()]
        assert parts[0] == 5, f"line {i}: bad length prefix {parts[0]}"
        pts = parts[1:]
        assert len(pts) == 5, f"line {i}: {len(pts)} points"
        assert len(set(pts)) == 5, f"line {i}: repeated point"
        assert all(0 <= p < N for p in pts), f"line {i}: point out of range"
        lines.append(tuple(pts))
    assert len(lines) == N, f"{len(lines)} lines, expected {N}"
    return lines


def verify_projective_plane(lines):
    checks = {}
    checks["n_lines"] = len(lines)
    checks["all_lines_size_5"] = all(len(set(L)) == 5 for L in lines)
    checks["lines_distinct"] = len(set(frozenset(L) for L in lines)) == len(lines)
    # point degrees
    deg = [0] * N
    pair_count = {}
    for L in lines:
        for p in L:
            deg[p] += 1
        for a, b in itertools.combinations(sorted(L), 2):
            pair_count[(a, b)] = pair_count.get((a, b), 0) + 1
    checks["point_degrees"] = sorted(set(deg))
    checks["all_point_degree_5"] = all(d == 5 for d in deg)
    expected_pairs = N * (N - 1) // 2
    checks["n_pairs"] = len(pair_count)
    checks["expected_pairs"] = expected_pairs
    checks["every_pair_on_exactly_one_line"] = (
        len(pair_count) == expected_pairs and all(v == 1 for v in pair_count.values())
    )
    # dual: every two lines meet in exactly one point
    inter = {}
    for i, j in itertools.combinations(range(len(lines)), 2):
        k = len(set(lines[i]) & set(lines[j]))
        inter[(i, j)] = k
    checks["distinct_line_intersections"] = sorted(set(inter.values()))
    checks["every_two_lines_meet_once"] = all(v == 1 for v in inter.values())
    # v = q^2+q+1 with q=4 -> 21, k=q+1=5
    checks["is_projective_plane_order_4"] = (
        checks["n_lines"] == 21
        and checks["all_lines_size_5"]
        and checks["all_point_degree_5"]
        and checks["every_pair_on_exactly_one_line"]
        and checks["every_two_lines_meet_once"]
    )
    return checks


def main():
    t0 = time.time()
    lines = parse_board(BOARD_PATH)
    checks = verify_projective_plane(lines)
    print("BOARD CHECKS")
    for k, v in checks.items():
        print(f"  {k}: {v}")
    assert checks["is_projective_plane_order_4"], "board is not PG(2,4)"

    line_masks = []
    for L in lines:
        m = 0
        for p in L:
            m |= 1 << p
        line_masks.append(m)
    through = [[] for _ in range(N)]
    for li, L in enumerate(lines):
        for p in L:
            through[p].append(li)

    # Exhaustive DFS over safe sets (canonical increasing point order).
    counts = [0] * (N + 1)
    masks_by_size = [[] for _ in range(N + 1)]
    line_cnt = [0] * len(lines)

    def add_point(p):
        for li in through[p]:
            line_cnt[li] += 1

    def remove_point(p):
        for li in through[p]:
            line_cnt[li] -= 1

    def can_add(p):
        return all(line_cnt[li] <= 2 for li in through[p])

    counts[0] = 1
    masks_by_size[0].append(0)

    def dfs(start, mask, size):
        for p in range(start, N):
            if can_add(p):
                add_point(p)
                nm = mask | (1 << p)
                ns = size + 1
                counts[ns] += 1
                masks_by_size[ns].append(nm)
                dfs(p + 1, nm, ns)
                remove_point(p)

    sys.setrecursionlimit(10000)
    dfs(0, 0, 0)

    elapsed = time.time() - t0
    print("\nDFS SAFE-SET COUNTS")
    total = 0
    for m in range(N + 1):
        if counts[m]:
            print(f"  k={m}: {counts[m]}")
        total += counts[m]
    print(f"  total: {total}")
    print(f"  max size: {max(m for m in range(N + 1) if counts[m])}")
    print(f"  elapsed: {elapsed:.2f}s")

    claim = {
        0: 1,
        1: 21,
        2: 210,
        3: 1330,
        4: 5880,
        5: 18648,
        6: 41328,
        7: 58320,
        8: 42840,
        9: 11480,
    }
    claim_total = 180058
    ok = all(counts[m] == claim.get(m, 0) for m in range(N + 1)) and total == claim_total
    print(f"  matches claim counts: {ok}")
    if not ok:
        for m in range(N + 1):
            if counts[m] != claim.get(m, 0):
                print(f"    MISMATCH k={m}: got {counts[m]}, claim {claim.get(m,0)}")
        print(f"    total got {total}, claim {claim_total}")

    # cross-check: every set found is distinct (it is by construction) and
    # masks sorted list has no duplicates
    for m in range(N + 1):
        assert len(set(masks_by_size[m])) == len(masks_by_size[m])

    payload = {
        "board_checks": checks,
        "lines": [list(L) for L in lines],
        "line_masks": line_masks,
        "through": through,
        "counts": counts,
        "masks_by_size": masks_by_size,
        "total": total,
        "matches_claim": ok,
        "elapsed_s": elapsed,
    }
    import pickle

    with open(HERE / "stage1.pkl", "wb") as f:
        pickle.dump(payload, f)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(
            {
                "board_checks": checks,
                "counts": {str(m): counts[m] for m in range(N + 1) if counts[m]},
                "total": total,
                "max_size": max(m for m in range(N + 1) if counts[m]),
                "matches_claim": ok,
                "elapsed_s": elapsed,
            },
            f,
            indent=2,
        )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    sys.exit(main())
