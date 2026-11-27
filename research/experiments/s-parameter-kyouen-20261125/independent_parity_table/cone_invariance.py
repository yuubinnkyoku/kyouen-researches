"""Robustness check: the cone distribution must not depend on the chosen
representative F of the t-subset orbit.  For each large board we compute two or
three cones from different F and compare T_m, T_m(g) and maximal counts.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kyouen_lib as K

ROOT = HERE.parent.parent
OUT = HERE / "out"

TASKS = [
    ("PG2q9_s2", ROOT / "pg2q9-cap-game-20261125/output/board_pg2q9.txt", 2,
     [(0, 1, 10), (0, 2, 20), (0, 3, 30)]),
    ("AG2q9_s2", ROOT / "ag2q9-cap-game-20261128/output/board_ag2q9.txt", 2,
     [(0, 9, 1), (0, 27, 3), (0, 30, 55)]),
    ("AG2q7_s2", ROOT / "s-parameter-kyouen-20261125/output/board_ag2q7.txt", 2,
     [(0, 1, 7), (2, 3, 9), (4, 5, 11)]),
    ("PG2q5_s3", ROOT / "projective-blocking-kyouen-20261125/output/board_pg2q5.txt", 3,
     [(0, 1, 6), (0, 2, 7)]),
    ("W22_s5", ROOT / "design-kyouen-witt-20261125/output/board_w22.txt", 5,
     [(0, 1, 2), (0, 5, 10), (3, 7, 15)]),
    ("W24_s5", ROOT / "design-kyouen-witt-20261125/output/board_w24.txt", 5,
     [(0, 1, 2, 3, 4), (0, 6, 12, 18, 23), (1, 5, 9, 14, 20)]),
    ("W24_s6", ROOT / "design-kyouen-witt-20261125/output/board_w24.txt", 6,
     [(0, 1, 2, 3, 4), (0, 6, 12, 18, 23), (1, 5, 9, 14, 20)]),
    ("W24_s7", ROOT / "design-kyouen-witt-20261125/output/board_w24.txt", 7,
     [(0, 1, 2, 3, 4), (0, 6, 12, 18, 23), (1, 5, 9, 14, 20)]),
]


def main():
    out = {}
    for key, path, s, Fs in TASKS:
        n, blocks = K.load_board(path)
        cones = []
        for F in Fs:
            c = K.cone_distribution(n, blocks, s, F)
            cones.append(c)
            print(key, "F", F, "cone", c["cone_size"],
                  "rootG", c["root_grundy"], flush=True)
        ref = cones[0]
        same_T = all(c["T"] == ref["T"] for c in cones)
        same_Tg = all(c["T_g"] == ref["T_g"] for c in cones)
        same_max = all(c["T_max"] == ref["T_max"] for c in cones)
        same_root = all(c["root_grundy"] == ref["root_grundy"] for c in cones)
        out[key] = {
            "s": s,
            "Fs": [list(F) for F in Fs],
            "cone_sizes": [c["cone_size"] for c in cones],
            "root_grundy": [c["root_grundy"] for c in cones],
            "T_equal": same_T,
            "T_g_equal": same_Tg,
            "T_max_equal": same_max,
            "root_grundy_equal": same_root,
        }
        print(key, "invariance:", out[key], flush=True)
    (OUT / "cone_invariance.json").write_text(json.dumps(out, indent=1),
                                             encoding="utf-8")


if __name__ == "__main__":
    main()
