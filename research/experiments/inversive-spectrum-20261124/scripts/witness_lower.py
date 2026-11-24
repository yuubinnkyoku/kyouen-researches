"""Write a verified lower-bound witness for K_s(q) from the greedy construction.

Used for (q, s) where the exact value was not settled, so that the recorded
lower bound has an explicit, independently checkable witness.

Usage:
    python witness_lower.py --q 8 --s 4 --restarts 20000
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import spectrum_common as C  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--s", type=int, required=True)
    ap.add_argument("--restarts", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20261124)
    args = ap.parse_args()
    board = C.load_board(args.q)
    best = C.greedy(args.q, args.s, board, args.restarts, args.seed)
    points = sorted(best)
    out = C.OUT / f"witness_q{args.q}_s{args.s}_n{len(points)}.json"
    out.write_text(json.dumps({"q": args.q, "s": args.s, "n": len(points),
                               "points": points}), encoding="utf-8")
    print(json.dumps({"q": args.q, "s": args.s, "n": len(points), "path": str(out)}))


if __name__ == "__main__":
    main()
