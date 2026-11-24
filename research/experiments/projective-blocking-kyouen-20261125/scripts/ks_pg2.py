"""Exact K_3 for PG(2,q): max |S| with |S ∩ line| <= 3, via binary ILP.

Usage:
    python ks_pg2.py --q 2 3 4 5 7
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def read_board(q: int):
    lines = (OUT / f"board_pg2q{q}.txt").read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    blocks = []
    for line in lines[1:]:
        parts = list(map(int, line.split()))
        if parts:
            blocks.append(parts[1:])
    return n, blocks


def ks(q: int, n: int, blocks, s: int = 3) -> int:
    A = np.zeros((len(blocks), n))
    for i, B in enumerate(blocks):
        for p in B:
            A[i, p] = 1
    res = milp(c=-np.ones(n), constraints=LinearConstraint(A, -np.inf, s),
               integrality=np.ones(n), bounds=Bounds(np.zeros(n), np.ones(n)))
    assert res.status == 0, res.message
    return int(round(-res.fun))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--out", type=Path, default=OUT / "ks_pg2.json")
    args = ap.parse_args()
    data = (json.loads(args.out.read_text(encoding="utf-8"))
            if args.out.exists() else {"rows": []})
    done = {r["q"] for r in data["rows"]}
    for q in args.q:
        if q in done:
            continue
        n, blocks = read_board(q)
        k3 = ks(q, n, blocks, 3)
        k4 = ks(q, n, blocks, 4)
        row = {"q": q, "v": n, "lines": len(blocks), "k": q + 1, "K3": k3, "K4": k4}
        data["rows"].append(row)
        print(row, flush=True)
        args.out.write_text(json.dumps(data, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
