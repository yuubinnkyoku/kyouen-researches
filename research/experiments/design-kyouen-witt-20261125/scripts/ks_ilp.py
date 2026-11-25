"""Exact K_s for a design board via binary ILP (scipy HiGHS).

K_s = max |S| subject to |S ∩ B| <= s for every block B.
This is an independent route to K_3 (cross-checks the Grundy engine's maximum
safe size) and gives K_4, K_5.

Usage:
    python ks_ilp.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def read_blocks(path: Path) -> tuple[int, list[frozenset[int]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    blocks = []
    for line in lines[1:]:
        parts = list(map(int, line.split()))
        if parts:
            blocks.append(frozenset(parts[1:]))
    assert len(blocks) == b
    return n, blocks


def ks(n: int, blocks: list[frozenset[int]], s: int) -> int:
    A = np.zeros((len(blocks), n))
    for i, B in enumerate(blocks):
        for p in B:
            A[i, p] = 1
    res = milp(c=-np.ones(n), constraints=LinearConstraint(A, -np.inf, s),
               integrality=np.ones(n), bounds=Bounds(np.zeros(n), np.ones(n)))
    assert res.status == 0, res.message
    return int(round(-res.fun))


def main() -> None:
    meta = json.loads((OUT / "designs_meta.json").read_text(encoding="utf-8"))
    tags = {"AG(3,2)": "ag32", "AG(4,2)": "ag42", "W_11": "w11", "W_12": "w12",
            "W_22": "w22", "W_23": "w23", "W_24": "w24"}
    rows = []
    for d in meta["designs"]:
        tag = tags[d["name"]]
        n, blocks = read_blocks(OUT / f"board_{tag}.txt")
        row = {"name": d["name"], "v": n, "b": len(blocks),
               "lambda2": d["lambda_2"][0], "lambda3": d["lambda_3"][0]}
        for s in (3, 4, 5):
            row[f"K{s}"] = ks(n, blocks, s)
            row[f"bound{s}"] = int((s - 2) * row["lambda2"] // row["lambda3"] + 2)
        rows.append(row)
        print(row)
    (OUT / "ks_ilp.json").write_text(json.dumps({"designs": rows}, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
