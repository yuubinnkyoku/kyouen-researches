"""Shared, SAT-free helpers for the K_s(q) experiment (board loading, greedy)."""

from __future__ import annotations

import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def load_board(q: int) -> dict:
    return json.loads((OUT / f"board_q{q}.json").read_text(encoding="utf-8"))


def point_circles(blocks: list[list[int]], v: int) -> list[list[int]]:
    pc: list[list[int]] = [[] for _ in range(v)]
    for c, b in enumerate(blocks):
        for p in b:
            pc[p].append(c)
    return pc


def greedy(q: int, s: int, board: dict, restarts: int, seed: int) -> list[int]:
    v, blocks = board["v"], board["blocks"]
    pc = point_circles(blocks, v)
    rng = random.Random(seed)
    best: list[int] = []
    order = list(range(v))
    for _ in range(restarts):
        rng.shuffle(order)
        counts = [0] * len(blocks)
        S = []
        for p in order:
            if all(counts[c] < s for c in pc[p]):
                S.append(p)
                for c in pc[p]:
                    counts[c] += 1
        if len(S) > len(best):
            best = S
    return best
