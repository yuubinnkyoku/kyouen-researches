"""IS THE INVERSIVE-PLANE KYOUEN GAME FIXED-LENGTH?

The game ends when no point can be added, i.e. when the safe set S is
MAXIMAL.  So the possible game lengths are exactly the sizes of maximal
safe sets.  Write

    K(q) = max size of a maximal safe set   (the usual K)
    s(q) = min size of a maximal safe set   (the saturation number)

If s(q) = K(q), every play has the same length, and the winner is decided
purely by parity: the first player wins iff K is odd.

This is exactly the hypothesis of the parity law (K1058 section 6):
"all maximal safe sets share parity  <=>  all Grundy values <= 1".

The summary records that for q = 3, 4 the minimum maximal size equals K.
This script tests q = 5, 7 and beyond.

ALGORITHM.  DFS over safe sets with the crucial pruning:

    as soon as S is MAXIMAL, record its size and DO NOT EXTEND IT
    (any superset would be unsafe, so maximal sets are leaves).

That makes the tree small: we enumerate maximal safe sets, not all safe
sets.  Iterative deepening on the size cap gives s(q) directly.

Run:  python min_maximal.py --q 3 4 5 7
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_inversive_plane  # noqa: E402


def build(q: int):
    points, circles = build_inversive_plane(q)
    idx = {p: i for i, p in enumerate(points)}
    blocks = [frozenset(idx[p] for p in c) for c in circles]
    n = len(points)
    # triple -> circle index
    tri_circle = {}
    for ci, B in enumerate(blocks):
        for tri in itertools.combinations(sorted(B), 3):
            tri_circle[tri] = ci
    # for each point, the triples it completes
    return n, blocks, tri_circle


def enumerate_maximal(n, blocks, tri_circle, kmax, node_cap=200_000_000):
    """All maximal safe sets of size <= kmax, as a size histogram."""
    hist = Counter()
    state = {"nodes": 0, "capped": False}
    chosen: list[int] = []

    def is_maximal() -> bool:
        """Is every point outside `chosen` blocked by a triple of chosen?"""
        S = set(chosen)
        blocked = set()
        for tri in itertools.combinations(chosen, 3):
            ci = tri_circle.get(tuple(sorted(tri)))
            if ci is None:
                continue
            for p in blocks[ci]:
                if p not in S:
                    blocked.add(p)
        return len(blocked) == n - len(S)

    def rec(start: int) -> None:
        state["nodes"] += 1
        if state["nodes"] > node_cap:
            state["capped"] = True
            return
        if len(chosen) >= 3 and is_maximal():
            hist[len(chosen)] += 1
            return                      # maximal sets are leaves
        if len(chosen) >= kmax:
            return
        for v in range(start, n):
            ok = True
            for pair in itertools.combinations(chosen, 2):
                if tuple(sorted((pair[0], pair[1], v))) in tri_circle:
                    ok = False
                    break
            if not ok:
                continue
            chosen.append(v)
            rec(v + 1)
            chosen.pop()
            if state["capped"]:
                return

    rec(0)
    return hist, state["nodes"], state["capped"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    ap.add_argument("--kmax", type=int, default=None)
    ap.add_argument("--cap", type=int, default=200_000_000)
    args = ap.parse_args()

    KNOWN_K = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8}

    rows = []
    print(f"{'q':>3} {'n':>4} {'s(q)':>5} {'K(q)':>5} {'fixed?':>7} "
          f"{'size histogram':>34} {'nodes':>10} {'sec':>7}")
    for q in args.q:
        n, blocks, tri_circle = build(q)
        kmax = args.kmax if args.kmax is not None else KNOWN_K.get(q, q + 2)
        t0 = time.time()
        hist, nodes, capped = enumerate_maximal(n, blocks, tri_circle, kmax,
                                                node_cap=args.cap)
        dt = time.time() - t0
        if not hist:
            print(f"{q:>3} {n:>4}  no maximal set found (kmax={kmax})",
                  flush=True)
            continue
        s = min(hist)
        K = max(hist)
        known = KNOWN_K.get(q)
        row = {"q": q, "n": n, "s": s, "K": K, "fixed_length": s == K,
               "histogram": {str(k): v for k, v in sorted(hist.items())},
               "known_K": known, "K_matches": (K == known) if known else None,
               "nodes": nodes, "capped": capped, "seconds": round(dt, 2)}
        rows.append(row)
        print(f"{q:>3} {n:>4} {s:>5} {K:>5} {str(s == K):>7} "
              f"{str(dict(sorted(hist.items()))):>34} {nodes:>10} {dt:>7.1f}"
              + ("  CAPPED" if capped else ""), flush=True)

    print()
    print("If s(q) = K(q) for all q, the inversive-plane game is FIXED-LENGTH")
    print("and the winner is decided by parity alone.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
