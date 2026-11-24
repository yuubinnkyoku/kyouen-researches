"""Task 1: verify from the board files that each board is PG(2,q).

For q = 2, 3, 4 check
  * n = q^2 + q + 1 points and b = n blocks,
  * every block has exactly q+1 distinct points (all blocks distinct),
  * every pair of points lies on exactly one block,
  * every point lies on exactly q+1 blocks.

Extra (cheap) dual checks that any projective plane of order q satisfies:
  * every pair of distinct blocks meets in exactly one point,
  * the incidence count n*(q+1) = b*(q+1).

Note: for q = 2, 3, 4 the projective plane of order q is unique up to
isomorphism (the smallest non-Desarguesian plane has order 9), so the axioms
above certify that the board is PG(2,q).
"""

from __future__ import annotations

import itertools
import json
import os

from common import read_board

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
BASE = os.path.dirname(HERE)          # .../projective-blocking-kyouen-20261125


def check_board(path, q):
    n, blocks = read_board(path)
    n_expected = q * q + q + 1
    report = {
        "path": os.path.relpath(path, BASE).replace("\\", "/"),
        "q": q,
        "n": n,
        "b": len(blocks),
        "n_expected": n_expected,
        "checks": {},
        "ok": True,
    }
    checks = report["checks"]

    def require(name, condition, detail=None):
        checks[name] = {"ok": bool(condition)}
        if detail is not None:
            checks[name]["detail"] = detail
        if not condition:
            report["ok"] = False

    require("n_equals_q2_plus_q_plus_1", n == n_expected,
            f"n={n}, expected {n_expected}")
    require("b_equals_n", len(blocks) == n, f"b={len(blocks)}, n={n}")

    # block sizes / ranges / distinctness
    sizes = [len(b) for b in blocks]
    require("every_block_size_q_plus_1", all(s == q + 1 for s in sizes),
            f"block sizes seen: {sorted(set(sizes))}")
    require("every_block_has_distinct_points",
            all(len(set(b)) == len(b) for b in blocks))
    require("all_points_in_range",
            all(0 <= p < n for b in blocks for p in b))
    require("all_blocks_distinct",
            len({frozenset(b) for b in blocks}) == len(blocks))

    # incidence: point -> blocks
    point_blocks = [[] for _ in range(n)]
    for bi, blk in enumerate(blocks):
        for p in blk:
            point_blocks[p].append(bi)
    degrees = [len(v) for v in point_blocks]
    require("every_point_on_q_plus_1_blocks",
            all(d == q + 1 for d in degrees),
            f"degrees seen: {sorted(set(degrees))}")
    report["incidences"] = sum(sizes)
    report["incidences_expected"] = n * (q + 1)

    # every pair of points on exactly one block
    pair_count = {}
    for bi, blk in enumerate(blocks):
        for a, b in itertools.combinations(sorted(blk), 2):
            pair_count[(a, b)] = pair_count.get((a, b), 0) + 1
    total_pairs = n * (n - 1) // 2
    counts = list(pair_count.values())
    bad_pairs = {k: v for k, v in pair_count.items() if v != 1}
    require("every_pair_on_exactly_one_block",
            len(pair_count) == total_pairs and not bad_pairs,
            f"pairs seen {len(pair_count)}/{total_pairs}; "
            f"pairs with count != 1: {len(bad_pairs)}")
    report["pair_multiplicities"] = sorted(set(counts)) if counts else []

    # dual checks
    block_sets = [set(b) for b in blocks]
    pair_meet = []
    for i, j in itertools.combinations(range(len(blocks)), 2):
        pair_meet.append(len(block_sets[i] & block_sets[j]))
    require("every_pair_of_blocks_meets_in_one_point",
            all(c == 1 for c in pair_meet),
            f"intersection sizes seen: {sorted(set(pair_meet))}")

    # A count identity that must hold in any 2-(n, q+1, 1) design:
    #   b * C(q+1, 2) = C(n, 2)
    require("pair_count_identity",
            len(blocks) * (q + 1) * q // 2 == total_pairs,
            f"{len(blocks)}*C({q + 1},2) = {len(blocks) * (q + 1) * q // 2}, "
            f"C({n},2) = {total_pairs}")

    return report


def main():
    os.makedirs(OUT, exist_ok=True)
    out = {"boards": []}
    for q in (2, 3, 4):
        path = os.path.join(BASE, "output", f"board_pg2q{q}.txt")
        rep = check_board(path, q)
        out["boards"].append(rep)
        status = "PASS" if rep["ok"] else "FAIL"
        print(f"q={q}: {status}  n={rep['n']} b={rep['b']} "
              f"incidences={rep['incidences']} "
              f"pair-multiplicities={rep['pair_multiplicities']}")
        for name, item in rep["checks"].items():
            if not item["ok"]:
                print(f"    FAILED: {name} {item.get('detail', '')}")
    out["all_ok"] = all(rep["ok"] for rep in out["boards"])
    print("ALL BOARDS PASS" if out["all_ok"] else "BOARD CHECK FAILED")
    with open(os.path.join(OUT, "task1_boards.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
