"""Independent witness checker for the K_s(q) experiment (no SAT dependency).

A witness file is ``{"q": int, "s": int, "n": int, "points": [int, ...]}``.
This script rebuilds nothing: it reads the board JSON written by build_board.py
and checks |S| = n and |S ∩ C| <= s for every circle C.

Usage:
    python verify_witness.py output/witness_q7_s4.json [...]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def verify(path: Path) -> dict:
    w = json.loads(path.read_text(encoding="utf-8"))
    board = json.loads((OUT / f"board_q{w['q']}.json").read_text(encoding="utf-8"))
    S = set(w["points"])
    assert len(S) == w["n"], (len(S), w["n"])
    assert S <= set(range(board["v"])), "point out of range"
    worst = 0
    for block in board["blocks"]:
        k = len(S.intersection(block))
        worst = max(worst, k)
        assert k <= w["s"], f"circle {block} meets S in {k} > {w['s']}"
    return {"q": w["q"], "s": w["s"], "n": w["n"], "max_circle_intersection": worst}


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: verify_witness.py <witness.json> [...]")
    for arg in sys.argv[1:]:
        print(json.dumps(verify(Path(arg))), flush=True)


if __name__ == "__main__":
    main()
