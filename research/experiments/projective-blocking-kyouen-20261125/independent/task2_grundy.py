"""Task 2: independent complete Grundy values and misere outcome for q = 2, 3.

Both boards are small enough for a literal full enumeration of all 2**n
subsets (128 and 8192).  We do that *and* a DFS over safe sets; the two counts
must agree.  Grundy values are computed by decreasing size (mex over children);
the misere outcome is computed by the usual win/lose recursion with terminal
positions winning for the player to move (no move => win under misere).

The report's claimed values are hard-coded below and also read from the
experiment's own ``output/grundy_pg2q*.txt`` files (read only, never modified).
"""

from __future__ import annotations

import json
import os

from common import Board, grundy_and_misere, read_board, size_histogram

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
BASE = os.path.dirname(HERE)

CLAIMED = {
    2: {
        "safe": 128,
        "grundy": {0: 64, 1: 64},
        "root_grundy": 1,
        "root_misere": 0,
        "maximal": {7: 1},
    },
    3: {
        "safe": 4330,
        "grundy": {0: 2184, 1: 2146},
        "root_grundy": 1,
        "root_misere": 0,
        "maximal": {7: 234, 9: 13},
    },
}


def parse_grundy_txt(path):
    """Parse the experiment's own engine output (data being verified)."""
    out = {"size": {}, "grundy": {}}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if not parts:
                continue
            key = parts[0]
            if key == "POINTS":
                out["points"] = int(parts[1])
            elif key == "CIRCLES":
                out["circles"] = int(parts[1])
            elif key == "SAFE":
                out["safe"] = int(parts[1])
            elif key == "ROOT":
                out["root"] = (int(parts[1]), int(parts[2]))
            elif key == "SIZE":
                out["size"][int(parts[1])] = {
                    "total": int(parts[2]),
                    "maximal": int(parts[3]),
                    "grundy0": int(parts[4]),
                }
            elif key == "GRUNDY":
                out["grundy"][int(parts[1])] = int(parts[2])
    return out


def analyse(q, keep_grundy=True):
    path = os.path.join(BASE, "output", f"board_pg2q{q}.txt")
    n, blocks = read_board(path)
    board = Board(n, blocks, cap=3)

    # plain 2**n enumeration
    sizes_bf, safe_masks_bf = board.brute_force()
    # DFS over safe sets (independent traversal), collecting masks by size
    sizes_dfs, by_size, maximal = board.enumerate_safe(collect=True)
    assert sizes_bf == sizes_dfs, (q, sizes_bf, sizes_dfs)
    assert len(safe_masks_bf) == sum(sizes_bf)

    grundy, win = grundy_and_misere(board, by_size)

    safe = len(safe_masks_bf)
    dist = {}
    for mask in safe_masks_bf:
        g = grundy[mask]
        dist[g] = dist.get(g, 0) + 1
    dist = dict(sorted(dist.items()))
    root = grundy[0]
    # report convention: ROOT <normal grundy> <misere>, 0 = first player loses
    root_misere = 0 if not win[0] else 1
    maximal_hist = size_histogram(maximal)
    per_size_grundy0 = {}
    for mask in safe_masks_bf:
        k = mask.bit_count()
        per_size_grundy0[k] = per_size_grundy0.get(k, 0) + (1 if grundy[mask] == 0 else 0)

    result = {
        "q": q,
        "n": n,
        "blocks": len(board.block_masks),
        "safe": safe,
        "safe_by_size": {int(k): int(v) for k, v in enumerate(sizes_bf) if v},
        "grundy_distribution": {int(k): int(v) for k, v in dist.items()},
        "root_grundy": root,
        "root_misere": root_misere,
        "root_misere_first_player_wins": bool(win[0]),
        "maximal_by_size": maximal_hist,
        "maximal_total": len(maximal),
        "max_grundy": max(dist),
        "per_size_grundy0": dict(sorted(per_size_grundy0.items())),
        "first_moves_losing_for_opponent": sum(
            1 for p in range(n)
            if board.safe(1 << p) and grundy[1 << p] == 0
        ) if q == 3 else None,
    }

    # claimed values
    claim = CLAIMED[q]
    checks = {}
    checks["safe"] = safe == claim["safe"]
    checks["grundy_distribution"] = dist == claim["grundy"]
    checks["root_grundy"] = root == claim["root_grundy"]
    checks["root_misere"] = root_misere == claim["root_misere"]
    checks["maximal_by_size"] = maximal_hist == claim["maximal"]
    checks["all_grundy_in_0_1"] = set(dist) <= {0, 1}

    # values from the experiment's own output file
    engine = parse_grundy_txt(os.path.join(BASE, "output", f"grundy_pg2q{q}.txt"))
    engine_checks = {}
    engine_checks["points"] = engine.get("points") == n
    engine_checks["circles"] = engine.get("circles") == len(board.block_masks)
    engine_checks["safe"] = engine.get("safe") == safe
    engine_checks["root"] = engine.get("root") == (root, root_misere)
    engine_checks["grundy_distribution"] = engine.get("grundy") == dist
    size_match = {}
    for k in range(n + 1):
        # the engine only prints a SIZE line for sizes where safe sets exist
        got = engine["size"].get(
            k, {"total": 0, "maximal": 0, "grundy0": 0})
        want = {
            "total": sizes_bf[k],
            "maximal": maximal_hist.get(k, 0),
            "grundy0": per_size_grundy0.get(k, 0),
        }
        size_match[k] = (got == want)
    engine_checks["size_lines"] = size_match
    engine_checks["all_size_lines_match"] = all(size_match.values())
    result["checks"] = checks
    result["engine_checks"] = engine_checks
    result["ok"] = all(checks.values()) and all(
        v for k, v in engine_checks.items() if k != "size_lines")

    if keep_grundy:
        result["grundy_values"] = {int(k): int(v) for k, v in sorted(grundy.items())}
    return result


def main():
    os.makedirs(OUT, exist_ok=True)
    out = {"tasks": []}
    for q in (2, 3):
        res = analyse(q)
        out["tasks"].append(res)
        print(f"--- q={q} (n={res['n']}) ---")
        print(f"  safe sets: {res['safe']}   by size: {res['safe_by_size']}")
        print(f"  Grundy distribution: {res['grundy_distribution']}  "
              f"max={res['max_grundy']}")
        print(f"  root Grundy (normal): {res['root_grundy']}   "
              f"root misere (0=first player loses): {res['root_misere']}")
        print(f"  maximal safe sets: {res['maximal_by_size']} "
              f"(total {res['maximal_total']})")
        for name, ok in res["checks"].items():
            print(f"  claim {name}: {'OK' if ok else 'MISMATCH'}")
        bad = [k for k, v in res["engine_checks"]["size_lines"].items() if not v]
        print(f"  engine SIZE lines: "
              f"{'all match' if not bad else 'mismatch at sizes ' + str(bad)}")
        print(f"  overall: {'PASS' if res['ok'] else 'FAIL'}")
    out["all_ok"] = all(t["ok"] for t in out["tasks"])
    with open(os.path.join(OUT, "task2_grundy.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("TASK 2:", "PASS" if out["all_ok"] else "FAIL")


if __name__ == "__main__":
    main()
