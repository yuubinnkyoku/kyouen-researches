"""IS THE INVERSIVE-PLANE KYOUEN GAME FIXED-LENGTH?  (incremental version)

The game ends when the safe set S is MAXIMAL.  Possible game lengths are
the sizes of maximal safe sets:

    K(q) = max size of a maximal safe set
    s(q) = min size of a maximal safe set

If s(q) = K(q), every play has the same length and the winner is decided by
parity alone -- exactly the hypothesis of the parity law.

ALGORITHM (incremental).  Maintain, for every point p outside S, the number
`block[p]` of triples of S whose circle contains p.  Then

    S is maximal  <=>  block[p] >= 1 for every p outside S.

When a point v is added to S, the new triples created are exactly
{pair, v} for pairs in S; each such triple's circle contributes +1 to
every point on it.  So the update is O(C(k,2) * (q+1)) per node, and the
maximality test is O(1) if we also maintain `nblocked` = #{p : block[p] > 0}.

Run:  python min_maximal2.py --q 3 4 5 7
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
    blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]
    n = len(points)
    tri_circle = {}
    for ci, B in enumerate(blocks):
        for tri in itertools.combinations(B, 3):
            tri_circle[tri] = ci
    return n, blocks, tri_circle


def enumerate_maximal(n, blocks, tri_circle, kmax, node_cap=200_000_000):
    hist = Counter()
    state = {"nodes": 0, "capped": False}
    chosen: list[int] = []
    inS = [False] * n
    block = [0] * n
    nblocked = [0]

    def add_point(v: int) -> list[tuple[int, int]]:
        """Add v to S; return the list of (point, delta) to undo."""
        undo = []
        # v leaves the "outside" pool, so it no longer counts as blocked
        if block[v] > 0:
            nblocked[0] -= 1
        inS[v] = True
        chosen.append(v)
        for pair in itertools.combinations(chosen[:-1], 2):
            tri = tuple(sorted((pair[0], pair[1], v)))
            ci = tri_circle.get(tri)
            if ci is None:
                continue
            for p in blocks[ci]:
                if inS[p]:
                    continue
                if block[p] == 0:
                    nblocked[0] += 1
                block[p] += 1
                undo.append((p, 1))
        return undo

    def remove_point(v: int, undo: list[tuple[int, int]]) -> None:
        for p, d in undo:
            block[p] -= d
            if block[p] == 0:
                nblocked[0] -= 1
        chosen.pop()
        inS[v] = False
        if block[v] > 0:
            nblocked[0] += 1

    def rec(start: int) -> None:
        state["nodes"] += 1
        if state["nodes"] > node_cap:
            state["capped"] = True
            return
        k = len(chosen)
        # maximal iff every point outside S is blocked
        if k >= 3 and nblocked[0] == n - k:
            hist[k] += 1
            return
        if k >= kmax:
            return
        for v in range(start, n):
            if inS[v]:
                continue
            # ILLEGAL iff v lies on a circle already carrying 3 points of S,
            # i.e. iff some triple of S has a circle through v.
            if block[v] > 0:
                continue
            undo = add_point(v)
            rec(v + 1)
            remove_point(v, undo)
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
          f"{'size histogram':>30} {'nodes':>10} {'sec':>7}")
    for q in args.q:
        n, blocks, tri_circle = build(q)
        kmax = args.kmax if args.kmax is not None else KNOWN_K.get(q, q + 2)
        t0 = time.time()
        hist, nodes, capped = enumerate_maximal(n, blocks, tri_circle, kmax,
                                                node_cap=args.cap)
        dt = time.time() - t0
        if not hist:
            print(f"{q:>3} {n:>4}  no maximal set found (kmax={kmax}, "
                  f"nodes={nodes}{' CAPPED' if capped else ''})", flush=True)
            continue
        s, K = min(hist), max(hist)
        known = KNOWN_K.get(q)
        row = {"q": q, "n": n, "s": s, "K": K, "fixed_length": s == K,
               "histogram": {str(k): v for k, v in sorted(hist.items())},
               "known_K": known, "K_matches": (K == known) if known else None,
               "nodes": nodes, "capped": capped, "seconds": round(dt, 2)}
        rows.append(row)
        print(f"{q:>3} {n:>4} {s:>5} {K:>5} {str(s == K):>7} "
              f"{str(dict(sorted(hist.items()))):>30} {nodes:>10} {dt:>7.1f}"
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
