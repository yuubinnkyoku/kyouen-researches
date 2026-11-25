"""Task 1: is the board PG(2,8), and does its point ordering equal the
sorted-canonical-vector model?

Run from anywhere:  python task1_board.py
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pg8

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(HERE, os.pardir, "output", "board_pg2q8.txt")


def main():
    print("=" * 78)
    print("TASK 1 - board is PG(2,8) and ordering is the sorted-canonical model")
    print("=" * 78)
    print("board file:", os.path.normpath(BOARD))

    print("\n-- GF(8) = GF(2)[x]/(x^3+x+1) -------------------------------")
    for k, v in pg8.field_axiom_report().items():
        print(f"  {k:26s} : {v}")

    board = pg8.Board(BOARD)
    res = pg8.verify_board(board)

    print("\n-- structural checks ----------------------------------------")
    keys = [
        "header",
        "n_points_declared_73",
        "n_lines",
        "all_lines_size_9",
        "all_points_in_range",
        "all_lines_distinct",
        "lines_have_distinct_points",
        "n_pairs_covered",
        "all_pairs_once",
        "point_degrees",
        "all_degrees_9",
        "model_n_lines",
        "model_equals_board_as_sets",
        "model_equals_board_in_order",
        "point_ordering_matches",
    ]
    for k in keys:
        print(f"  {k:28s} : {res[k]}")

    print("\n-- model spot checks (index -> canonical vector) ------------")
    for i, v in res["model_points_sample"]:
        print(f"  point {i:2d} = {v}")

    ok = (
        res["n_points_declared_73"]
        and res["n_lines"] == 73
        and res["all_lines_size_9"]
        and res["all_points_in_range"]
        and res["all_lines_distinct"]
        and res["lines_have_distinct_points"]
        and res["all_pairs_once"]
        and res["all_degrees_9"]
        and res["model_n_lines"] == 73
        and res["model_equals_board_as_sets"]
        and res["model_equals_board_in_order"]
        and res["point_ordering_matches"]
    )
    print("\nTASK 1:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
