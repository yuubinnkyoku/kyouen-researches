"""Task 4: exact K_3(PG(2,q)) = maximum size of a set meeting every line in <= 3
points, for q = 2, 3, 4, using only our own searches.

  * q=2: all 2^7 subsets (K_3 = 7).
  * q=3: all 2^13 subsets (K_3 = 9); also all C(13,10) 10-subsets are unsafe,
    which independently proves no safe set of size >= 10 (safety is hereditary).
  * q=4: all C(21,10) = 352,716 10-subsets are unsafe (so no safe set of size
    >= 10), a safe 9-set is exhibited, and a branch-and-bound search confirms
    the maximum is 9.
"""

from __future__ import annotations

import itertools
import json
import os
import time

from common import Board, read_board

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
BASE = os.path.dirname(HERE)

CLAIMED_K3 = {2: 7, 3: 9, 4: 9}


def max_safe_bruteforce(board):
    best = 0
    best_mask = 0
    for mask in range(1 << board.n):
        if board.safe(mask):
            k = mask.bit_count()
            if k > best:
                best, best_mask = k, mask
    return best, best_mask


def count_safe_k_subsets(board, k):
    """Number of safe k-subsets, enumerating all C(n,k) of them."""
    count = 0
    examples = []
    for comb in itertools.combinations(range(board.n), k):
        mask = 0
        for p in comb:
            mask |= 1 << p
        if board.safe(mask):
            count += 1
            if len(examples) < 3:
                examples.append(list(comb))
    return count, examples


def max_safe_branch_and_bound(board):
    """Exact maximum safe set by include/exclude branch and bound."""
    n = board.n
    point_blocks = board.point_blocks
    cap = board.cap
    counts = [0] * len(board.block_masks)
    # order points by decreasing block degree (find large sets early)
    order = sorted(range(n), key=lambda p: -len(point_blocks[p]))
    best = [0, 0]

    def rec(i, mask, size):
        if size + (n - i) <= best[0]:
            return
        if i == n:
            if size > best[0]:
                best[0], best[1] = size, mask
            return
        p = order[i]
        ok = True
        for bi in point_blocks[p]:
            if counts[bi] >= cap:
                ok = False
                break
        if ok:
            for bi in point_blocks[p]:
                counts[bi] += 1
            rec(i + 1, mask | (1 << p), size + 1)
            for bi in point_blocks[p]:
                counts[bi] -= 1
        rec(i + 1, mask, size)

    rec(0, 0, 0)
    return best[0], best[1]


def analyse(q):
    path = os.path.join(BASE, "output", f"board_pg2q{q}.txt")
    n, blocks = read_board(path)
    board = Board(n, blocks, cap=3)

    t0 = time.time()
    bf_max, bf_mask = max_safe_bruteforce(board)
    bf_seconds = time.time() - t0

    t0 = time.time()
    k10, k10_examples = count_safe_k_subsets(board, 10)
    higher = {}
    for k in range(11, n + 1):
        higher[k], _ = count_safe_k_subsets(board, k)
    enumeration_seconds = time.time() - t0

    t0 = time.time()
    bb_max, bb_mask = max_safe_branch_and_bound(board)
    bb_seconds = time.time() - t0

    sizes, _by_size, maximal = board.enumerate_safe(collect=False)
    maximal_max = max(mask.bit_count() for mask in maximal)

    checks = {
        "brute_force_max_equals_claim": bf_max == CLAIMED_K3[q],
        "branch_and_bound_equals_brute_force": bb_max == bf_max,
        "no_safe_10_subsets": k10 == 0,
        "no_safe_subsets_above_10": all(v == 0 for v in higher.values()),
        "maximal_max_equals_brute_force": maximal_max == bf_max,
    }
    return {
        "q": q,
        "n": n,
        "K3": bf_max,
        "claimed": CLAIMED_K3[q],
        "witness": [p for p in range(n) if (bf_mask >> p) & 1],
        "safe_10_subsets": k10,
        "safe_11plus_subsets": higher,
        "branch_and_bound_max": bb_max,
        "maximal_max": maximal_max,
        "brute_force_seconds": round(bf_seconds, 2),
        "higher_enumeration_seconds": round(enumeration_seconds, 2),
        "branch_and_bound_seconds": round(bb_seconds, 2),
        "checks": checks,
        "ok": all(checks.values()),
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    out = {"tasks": []}
    for q in (2, 3, 4):
        res = analyse(q)
        out["tasks"].append(res)
        print(f"--- q={q} (n={res['n']}) ---")
        print(f"  K_3 = {res['K3']} (claimed {res['claimed']}); "
              f"witness {res['witness']}")
        print(f"  safe 10-subsets: {res['safe_10_subsets']}; "
              f"safe k>10 subsets: {res['safe_11plus_subsets']}")
        print(f"  branch-and-bound max: {res['branch_and_bound_max']}; "
              f"max maximal safe set: {res['maximal_max']}")
        print(f"  times: brute={res['brute_force_seconds']}s "
              f"higher={res['higher_enumeration_seconds']}s "
              f"bb={res['branch_and_bound_seconds']}s")
        for name, ok in res["checks"].items():
            print(f"  check {name}: {'OK' if ok else 'FAIL'}")
        print(f"  overall: {'PASS' if res['ok'] else 'FAIL'}")
    out["all_ok"] = all(t["ok"] for t in out["tasks"])
    with open(os.path.join(OUT, "task4_k3.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("TASK 4:", "PASS" if out["all_ok"] else "FAIL")


if __name__ == "__main__":
    main()
