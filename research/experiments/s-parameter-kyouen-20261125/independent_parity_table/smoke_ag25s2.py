"""Quick smoke test: full DP on AG(2,5) s=2, compared with grundy_general.json."""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kyouen_lib as K

BOARD = HERE.parent / "output" / "board_ag2q5.txt"
PUB = HERE.parent / "output" / "grundy_general.json"

n, blocks = K.load_board(BOARD)
print("board", n, len(blocks))
print("validation", K.validate_board(n, blocks))

t0 = time.time()
res = K.solve_positions(n, blocks, 2, use_array=True)
print("elapsed", round(time.time() - t0, 2), "s")
print(json.dumps({k: res[k] for k in ("positions", "maximal_by_size",
                                      "grundy_dist", "root_grundy")}, indent=1))

pub = json.load(open(PUB, encoding="utf-8"))
game = next(g for g in pub["games"] if g["name"] == "AG2(5)_s2")
print("published maximal", game["maximal_by_size"])
print("published grundy ", game["grundy_dist"])
print("match maximal", {str(k): v for k, v in res["maximal_by_size"].items()}
      == game["maximal_by_size"])
print("match grundy ", {str(k): v for k, v in res["grundy_dist"].items()}
      == game["grundy_dist"])
print("match sizes", {str(k): v for k, v in res["size_counts"].items()}
      == game["size_counts"])
