"""Full DP on AG(2,7) s=2 (n=49, dict-based layer DP)."""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kyouen_lib as K

ROOT = HERE.parent.parent
OUT = HERE / "out"

board = ROOT / "s-parameter-kyouen-20261125/output/board_ag2q7.txt"
n, blocks = K.load_board(board)
print("board", K.validate_board(n, blocks), flush=True)
t0 = time.time()
res = K.solve_positions(n, blocks, 2, use_array=False)
res["key"] = "AG2q7_s2"
res["board_file"] = str(board).replace("\\", "/")
res["seconds"] = round(time.time() - t0, 2)
print("positions", res["positions"], "maximal", res["maximal_by_size"],
      "grundy", res["grundy_dist"], res["seconds"], "s", flush=True)
(OUT / "full_dense_AG2q7_s2.json").write_text(json.dumps(res, indent=1),
                                             encoding="utf-8")
