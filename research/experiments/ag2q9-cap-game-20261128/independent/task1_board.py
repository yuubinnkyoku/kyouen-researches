"""Task 1: build AG(2,9) independently, verify the axioms, determine the parent's indexing.

Run:  python task1_board.py
Writes out/task1_board.json and prints a summary.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import (  # noqa: E402
    E, dec, enc, fadd, fmul, build_board, parse_board, verify_linear_space,
    line_masks, is_cap,
)

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
PARENT_BOARD = HERE.parent / "output" / "board_ag2q9.txt"


def main():
    result = {}

    # ---------------------------------------------------------------- my board
    my_pts, my_lines = build_board("y")          # index = 9*enc(y) + enc(x)
    my_check = verify_linear_space(81, my_lines)
    result["my_board"] = {
        "convention": "index = 9*enc(y) + enc(x), enc(a+bi) = 3a+b",
        "n_points": len(my_pts),
        "n_lines": len(my_lines),
        "axioms_ok": my_check["ok"],
        "errors": my_check["errors"],
        "parallel_classes": my_check.get("parallel_classes"),
    }
    if not my_check["ok"]:
        raise SystemExit("my board failed the AG(2,9) axioms: %r" % my_check["errors"])

    # ------------------------------------------------------------ parent board
    pn, pnb, p_lines = parse_board(PARENT_BOARD)
    p_check = verify_linear_space(pn, p_lines)
    result["parent_board"] = {
        "path": str(PARENT_BOARD.relative_to(HERE.parent.parent.parent.parent)),
        "n_points": pn,
        "n_lines": pnb,
        "axioms_ok": p_check["ok"],
        "errors": p_check["errors"],
        "parallel_classes": p_check.get("parallel_classes"),
    }
    if not p_check["ok"]:
        raise SystemExit("parent board failed the AG(2,9) axioms: %r" % p_check["errors"])

    # ------------------------------------------- infer the parent's indexing
    # (a) the first nine lines are consecutive 9-blocks and partition the points
    first_nine_are_blocks = all(p_lines[i] == list(range(9 * i, 9 * i + 9)) for i in range(9))
    block_union = set()
    for L in p_lines[:9]:
        block_union |= set(L)
    blocks_partition = len(block_union) == 81

    # (b) lines 9..17 are the transversals {9*t + j}
    transversals_ok = all(
        sorted(p_lines[9 + j]) == [9 * t + j for t in range(9)] for j in range(9)
    )

    # (c) exact reconstruction: point i <-> (x, y) = (dec(i // 9), dec(i % 9))
    #     parent index = 9*enc(x) + enc(y); lines: x=c, then y = m*x+b.
    reconstructed = []
    for c in E:
        reconstructed.append([9 * enc(c) + enc(y) for y in E])
    for m in E:
        for b in E:
            reconstructed.append([9 * enc(x) + enc(fadd(fmul(m, x), b)) for x in E])
    exact_reconstruction = reconstructed == p_lines

    # how many of the 90 lines match when order is ignored
    n_set_equal = sum(
        1 for a, b in zip(reconstructed, p_lines) if set(a) == set(b)
    )

    # cross-check that the *first* vertical line of the reconstruction is the
    # first parent line and the last line matches too
    endpoints_ok = reconstructed[0] == p_lines[0] and reconstructed[-1] == p_lines[-1]

    result["parent_indexing"] = {
        "point_index_formula": "idx(x,y) = 9*enc(x) + enc(y), enc(a+bi)=3a+b",
        "line_order": (
            "lines 0..8: vertical x=c (c in E order); "
            "lines 9..89: y=m*x+b with m in E order, then b in E order"
        ),
        "first_nine_are_consecutive_blocks": first_nine_are_blocks,
        "first_nine_partition_the_points": blocks_partition,
        "lines_9_to_17_are_transversals": transversals_ok,
        "exact_reconstruction_of_all_90_lines": exact_reconstruction,
        "lines_equal_as_sets": n_set_equal,
        "endpoints_match": endpoints_ok,
    }

    # --------------------------------------- isomorphism from my board to parent
    # my idx = 9*enc(y)+enc(x); parent idx = 9*enc(x)+enc(y): swap base-9 digits.
    pi = lambda i: 9 * (i % 9) + (i // 9)          # noqa: E731
    mapped = [[pi(p) for p in L] for L in my_lines]
    iso_ordered = mapped == p_lines
    iso_sets = [sorted(L) for L in mapped] == [sorted(L) for L in p_lines]
    pi_is_bijection = sorted(pi(i) for i in range(81)) == list(range(81))
    result["indexing_isomorphism"] = {
        "map": "my index i = 9*enc(y)+enc(x) -> parent index 9*(i mod 9) + i//9",
        "bijection": pi_is_bijection,
        "line_lists_equal_in_order": iso_ordered,
        "line_lists_equal_as_sets": iso_sets,
    }

    # ------------------------------------------------------------ the 3-cap F
    # F in the parent script is the bit set {0, 9, 1}.
    F_script = (1 << 0) | (1 << 9) | (1 << 1)
    # The README names F = {(0,0),(1,0),(0,1)} in field coordinates; under the
    # parent indexing that is {0, 27, 3}.
    F_coords = (1 << 0) | (1 << 27) | (1 << 3)
    p_masks = line_masks(81, p_lines)
    result["F"] = {
        "script_mask_points": sorted(i for i in range(81) if (F_script >> i) & 1),
        "script_points_coords": [
            [dec(i // 9), dec(i % 9)] for i in sorted(i for i in range(81) if (F_script >> i) & 1)
        ],
        "script_is_cap": is_cap(F_script, p_masks),
        "coords_mask_points": sorted(i for i in range(81) if (F_coords >> i) & 1),
        "coords_points_coords": [
            [dec(i // 9), dec(i % 9)] for i in sorted(i for i in range(81) if (F_coords >> i) & 1)
        ],
        "coords_is_cap": is_cap(F_coords, p_masks),
        "note": (
            "Both are non-collinear triples, hence in the same AGL(2,9) orbit; "
            "the cone statistics only depend on the orbit."
        ),
    }

    # ----------------------------------------- my board's F in my own indexing
    my_idx = {p: i for i, p in enumerate(my_pts)}
    my_F_script = 0
    for x, y in [((0, 0), (0, 0)), ((0, 1), (0, 0)), ((0, 0), (0, 1))]:
        my_F_script |= 1 << my_idx[(x, y)]
    # i.e. (0,0), (i,0), (0,i)
    result["F"]["my_board_mask"] = sorted(i for i in range(81) if (my_F_script >> i) & 1)
    result["F"]["my_mask_maps_to_script_mask"] = sorted(
        pi(i) for i in range(81) if (my_F_script >> i) & 1
    ) == result["F"]["script_mask_points"]

    result["all_task1_checks_ok"] = all(
        [
            my_check["ok"],
            p_check["ok"],
            first_nine_are_blocks,
            blocks_partition,
            transversals_ok,
            exact_reconstruction,
            n_set_equal == 90,
            endpoints_ok,
            pi_is_bijection,
            iso_ordered,
            iso_sets,
            result["F"]["script_is_cap"],
            result["F"]["coords_is_cap"],
            result["F"]["my_mask_maps_to_script_mask"],
        ]
    )

    (OUT / "task1_board.json").write_text(json.dumps(result, indent=1), encoding="utf-8")

    print("=" * 78)
    print("TASK 1  board + indexing")
    print("=" * 78)
    print("my board      :", len(my_pts), "points,", len(my_lines), "lines, axioms", my_check["ok"])
    print("parent board  :", pn, "points,", pnb, "lines, axioms", p_check["ok"])
    print("first 9 lines are consecutive blocks :", first_nine_are_blocks)
    print("lines 9..17 are transversals         :", transversals_ok)
    print("exact reconstruction of all 90 lines :", exact_reconstruction,
          "(%d/90 equal as sets)" % n_set_equal)
    print("isomorphism (digit swap) ordered     :", iso_ordered)
    print("parent point formula                 : idx(x,y) = 9*enc(x)+enc(y)")
    print("F (script bits 0,9,1) = coords      :",
          result["F"]["script_points_coords"], "cap:", result["F"]["script_is_cap"])
    print("F (README field coords)             :",
          result["F"]["coords_points_coords"], "cap:", result["F"]["coords_is_cap"])
    print("all task-1 checks                    :", result["all_task1_checks_ok"])
    print("wrote", OUT / "task1_board.json")
    return result


if __name__ == "__main__":
    r = main()
    raise SystemExit(0 if r["all_task1_checks_ok"] else 1)
