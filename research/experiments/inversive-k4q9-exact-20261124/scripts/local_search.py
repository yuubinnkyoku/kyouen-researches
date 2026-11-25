"""Iterated greedy / forced-insertion search for large s-arcs in M(q).

Independent of SAT: only the board JSON (points, circles) is used.

An s-arc is a point set S with |S ∩ C| <= s for every circle C.

Main loop (standard iterated-greedy for maximum independent sets, adapted):

  * start from a maximal s-arc reached by greedy completion;
  * kick: pick a random point r outside S, delete the points that block r
    (one point per over-full circle through r), insert r, then finish with a
    randomised greedy completion;
  * keep the result only if it is not smaller than the current set
    (sideways moves allowed with a small probability) and record the best.

Restarts from scratch are interleaved so that the search cannot be trapped in
one basin.

Usage:
    python local_search.py --q 9 --s 4 --k 17 --seconds 120 --seed 1
"""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
REPO = EXP.parents[2]
BOARDS = EXP / "output"


def load_board(q: int) -> dict:
    return json.loads((BOARDS / f"board_q{q}.json").read_text(encoding="utf-8"))


def point_circles(blocks: list[list[int]], v: int) -> list[list[int]]:
    pc: list[list[int]] = [[] for _ in range(v)]
    for c, b in enumerate(blocks):
        for p in b:
            pc[p].append(c)
    return pc


def counts_of(S: set[int], pc: list[list[int]], m: int) -> list[int]:
    counts = [0] * m
    for p in S:
        for c in pc[p]:
            counts[c] += 1
    return counts


def complete(S: set[int], counts: list[int], pc: list[list[int]], s: int,
             order: list[int]) -> None:
    """Greedy completion in the given point order (mutates S and counts)."""
    for p in order:
        if p in S:
            continue
        ok = True
        for c in pc[p]:
            if counts[c] >= s:
                ok = False
                break
        if ok:
            S.add(p)
            for c in pc[p]:
                counts[c] += 1


def force_insert(S: set[int], counts: list[int], pc: list[list[int]], s: int,
                 r: int, rng: random.Random) -> None:
    """Delete a minimal blocking set for r, insert r."""
    victims: set[int] = set()
    for c in pc[r]:
        excess = counts[c] + 1 - s
        if excess > 0:
            cand = [p for p in S if c in pc[p]]
            victims.update(rng.sample(cand, min(excess, len(cand))))
    for p in victims:
        if p not in S:
            continue
        S.discard(p)
        for c in pc[p]:
            counts[c] -= 1
    S.add(r)
    for c in pc[r]:
        counts[c] += 1


def search(q: int, s: int, k: int, seconds: float, seed: int) -> dict:
    board = load_board(q)
    v, blocks = board["v"], board["blocks"]
    pc = point_circles(blocks, v)
    m = len(blocks)
    rng = random.Random(seed)
    t_end = time.time() + seconds

    best: set[int] = set()
    iters = 0
    restarts = 0
    while time.time() < t_end:
        # restart from scratch, or continue from the best set found so far
        if iters == 0 or rng.random() < 0.05:
            S: set[int] = set()
            counts = [0] * m
            order = list(range(v))
            rng.shuffle(order)
            complete(S, counts, pc, s, order)
            restarts += 1
        else:
            S = set(best) if rng.random() < 0.8 else set(S)
            counts = counts_of(S, pc, m)
        # one kick
        outside = [p for p in range(v) if p not in S]
        if outside:
            r = rng.choice(outside)
            force_insert(S, counts, pc, s, r, rng)
        order = list(range(v))
        rng.shuffle(order)
        complete(S, counts, pc, s, order)
        iters += 1
        if len(S) > len(best):
            best = set(S)
            if len(best) >= k:
                return {"q": q, "s": s, "k": k, "found": len(best),
                        "points": sorted(best), "iters": iters,
                        "restarts": restarts, "seconds": seconds, "seed": seed}
    return {"q": q, "s": s, "k": k, "found": len(best),
            "points": sorted(best), "iters": iters, "restarts": restarts,
            "seconds": seconds, "seed": seed}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--s", type=int, required=True)
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    res = search(args.q, args.s, args.k, args.seconds, args.seed)
    print(json.dumps(res))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
