"""Heuristic search for small blocking sets (tau_1) of the inversive plane.

tau_1(q) = min |X| such that every circle meets X.  By the complement duality
K_q(q) = q^2+1 - tau_1(q); exact values are known here for q=4 (8) and q=5 (10).

This script only produces upper bounds (explicit blocking sets), used to test
the conjecture tau_1(q) = 2q for q >= 4.  Every reported set is verified.

Usage:
    python blocking_search.py --q 3 4 5 7 8 9 --restarts 3000
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import spectrum_common as C  # noqa: E402


def verify(q: int, X: list[int]) -> bool:
    board = C.load_board(q)
    S = set(X)
    return all(S.intersection(cir) for cir in board["blocks"])


def greedy_blocking(q: int, rng: random.Random) -> list[int]:
    board = C.load_board(q)
    v, blocks = board["v"], board["blocks"]
    pc = C.point_circles(blocks, v)
    uncovered = set(range(len(blocks)))
    X: list[int] = []
    while uncovered:
        gains = []
        for p in range(v):
            gain = sum(1 for c in pc[p] if c in uncovered)
            gains.append((gain, p))
        top = max(g for g, _ in gains)
        # randomised greedy: pick among near-best candidates
        cands = [p for g, p in gains if g >= top - rng.choice([0, 1, 1, 2])]
        best_p = rng.choice(cands)
        X.append(best_p)
        uncovered.difference_update(c for c in pc[best_p] if c in uncovered)
    return X


def shrink(q: int, X: list[int], rng: random.Random) -> list[int]:
    """Repeatedly try to drop points while staying blocking (cheap 1-out test)."""
    board = C.load_board(q)
    blocks = board["blocks"]
    X = set(X)
    improved = True
    while improved:
        improved = False
        for p in sorted(X):
            Y = X - {p}
            if all(any(qq in Y for qq in cir) for cir in blocks):
                X = Y
                improved = True
                break
    return sorted(X)


def search(q: int, restarts: int, seed: int) -> dict:
    rng = random.Random(seed)
    best: list[int] | None = None
    for _ in range(restarts):
        X = greedy_blocking(q, rng)
        X = shrink(q, X, rng)
        if best is None or len(X) < len(best):
            best = X
    assert best is not None and verify(q, best)
    return {"q": q, "tau1_upper": len(best), "witness": best,
            "conjecture_2q": 2 * q}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--restarts", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261124)
    ap.add_argument("--out", type=Path, default=C.OUT / "blocking_upper.json")
    args = ap.parse_args()
    rows = [search(q, args.restarts, args.seed) for q in args.q]
    args.out.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    for r in rows:
        print(f"q={r['q']}: tau_1 <= {r['tau1_upper']} (2q = {r['conjecture_2q']})",
              flush=True)


if __name__ == "__main__":
    main()
