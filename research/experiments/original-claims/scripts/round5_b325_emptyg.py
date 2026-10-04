import sys as _ssot_sys
from pathlib import Path as _SSOTPath
_ssot_sys.path.insert(0, str(next(p for p in _SSOTPath(__file__).resolve().parents if (p / "pyproject.toml").is_file()) / "scripts/research"))
import sys
sys.path.insert(0, r"D:\ghq\github.com\yuubinnkyoku\kyouen-researches\research\experiments\original-claims\scripts")
from kyouen_core import board_square

for n in range(2, 6):
    B = board_square(n)
    g = B.solve_grundy()
    empty_g = g.get(0, "missing")
    print(f"n={n} empty_grundy={empty_g} n_states={len(g)} K={B.max_safe_size()}", flush=True)
