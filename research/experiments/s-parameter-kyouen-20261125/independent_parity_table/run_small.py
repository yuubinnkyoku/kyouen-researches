"""Full (complete board) recomputation for boards with n <= 25 points.

Each result is written to out/<key>.json immediately.
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kyouen_lib as K

ROOT = HERE.parent.parent  # research/experiments
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

TASKS = [
    # key, board, s
    ("AG2q5_s2", ROOT / "s-parameter-kyouen-20261125/output/board_ag2q5.txt", 2),
    ("AG2q4_s3", ROOT / "s-parameter-kyouen-20261125/output/board_ag2q4.txt", 3),
    ("PG2q3_s3", ROOT / "projective-blocking-kyouen-20261125/output/board_pg2q3.txt", 3),
    ("PG2q4_s3", ROOT / "projective-blocking-kyouen-20261125/output/board_pg2q4.txt", 3),
    ("PG2q4_s4", ROOT / "projective-blocking-kyouen-20261125/output/board_pg2q4.txt", 4),
    ("AG2q5_s3", ROOT / "s-parameter-kyouen-20261125/output/board_ag2q5.txt", 3),
    ("W22_s5", ROOT / "design-kyouen-witt-20261125/output/board_w22.txt", 5),
    ("W24_s5", ROOT / "design-kyouen-witt-20261125/output/board_w24.txt", 5),
    ("W24_s6", ROOT / "design-kyouen-witt-20261125/output/board_w24.txt", 6),
]

only = set(sys.argv[1:])
for key, board_path, s in TASKS:
    if only and key not in only:
        continue
    print(f"=== {key}: {board_path.name} s={s}", flush=True)
    n, blocks = K.load_board(board_path)
    val = K.validate_board(n, blocks)
    print("  board:", n, "points,", len(blocks), "blocks, valid_2design=",
          val["valid_2design"], flush=True)
    t0 = time.time()
    res = K.solve_positions(n, blocks, s, use_array=True)
    res["key"] = key
    res["board_file"] = str(board_path).replace("\\", "/")
    res["validation"] = val
    res["seconds"] = round(time.time() - t0, 2)
    print("  positions", res["positions"], "maximal", res["maximal_by_size"],
          "grundy", res["grundy_dist"], f"{res['seconds']}s", flush=True)
    (OUT / f"full_{key}.json").write_text(json.dumps(res, indent=1),
                                          encoding="utf-8")
print("done")
