"""Build affine plane boards AG(2,q) for the s-parameter Kyouen games.

AG(2,q) is derived from the verified PG(2,q) board: fix a line L_inf, take the
q^2 points outside it, and for every other line remove its point on L_inf.
This works for any prime power and reuses the committed PG boards.

Usage:
    python build_ag2.py --q 2 3 4 5
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
REPO = EXP.parents[2]
PG_OUT = REPO / "research/experiments/projective-blocking-kyouen-20261125/output"
OUT = EXP / "output"


def read_pg(q: int):
    lines = (PG_OUT / f"board_pg2q{q}.txt").read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    blocks = [tuple(map(int, l.split()[1:])) for l in lines[1:]]
    return n, blocks


def build_ag(q: int, inf_line_index: int = 0):
    n, blocks = read_pg(q)
    L_inf = set(blocks[inf_line_index])
    pts = [p for p in range(n) if p not in L_inf]
    idx = {p: i for i, p in enumerate(pts)}
    ag_lines = []
    for i, B in enumerate(blocks):
        if i == inf_line_index:
            continue
        # every other line meets L_inf in exactly one point
        pts_on = [p for p in B if p not in L_inf]
        assert len(pts_on) == q, (i, len(pts_on))
        ag_lines.append(tuple(sorted(idx[p] for p in pts_on)))
    ag_lines = sorted(set(ag_lines))
    assert len(ag_lines) == q * (q + 1), (len(ag_lines), q * (q + 1))
    pair = {}
    for L in ag_lines:
        for a, b in combinations(L, 2):
            pair[(a, b)] = pair.get((a, b), 0) + 1
    assert len(pair) == q * q * (q * q - 1) // 2, (len(pair), q)
    assert set(pair.values()) == {1}
    return len(pts), ag_lines, {"v": q * q, "b": len(ag_lines), "k": q,
                                "pair_lambda": 1, "lines_ok": True}


def write_board(path: Path, n: int, blocks) -> None:
    with path.open("w", encoding="utf-8") as fh:
        fh.write(f"{n} {len(blocks)}\n")
        for B in blocks:
            fh.write(f"{len(B)} " + " ".join(map(str, B)) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {"experiment": "s-parameter-kyouen-20261125", "boards": []}
    for q in args.q:
        n, blocks, info = build_ag(q)
        write_board(OUT / f"board_ag2q{q}.txt", n, blocks)
        meta["boards"].append({"q": q, "name": f"AG(2,{q})", **info,
                               "board": f"output/board_ag2q{q}.txt"})
        print(f"AG(2,{q}): v={n} lines={len(blocks)} k={q}", flush=True)
    (OUT / "ag_boards_meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
