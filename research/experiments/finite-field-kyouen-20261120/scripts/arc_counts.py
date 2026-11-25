"""THE FULL ARC-COUNT SERIES: K is the largest size with a nonzero count.

The arc formulation makes K directly readable: K is the largest k for which
the elliptic quadric of PG(3,q) contains a k-arc (no 4 coplanar).

This script enumerates arcs by size for q = 3,4,5,7,8 and reports the
counts, so the series can be compared with the literature and with the
earlier K values.

Run:  python arc_counts.py --q 3 4 5 7 8
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

from arc_on_quadric import build  # noqa: E402


def count_arcs(F, ovoid, circles, kmax):
    n = len(ovoid)
    circ_of_quad = {}
    for ci, B in enumerate(circles):
        for quad in itertools.combinations(B, 4):
            circ_of_quad[quad] = ci

    hist = Counter()
    chosen: list[int] = []
    state = {"nodes": 0}

    def ok_add(v):
        for tri in itertools.combinations(chosen, 3):
            if tuple(sorted((tri[0], tri[1], tri[2], v))) in circ_of_quad:
                return False
        return True

    def rec(start):
        state["nodes"] += 1
        hist[len(chosen)] += 1
        if len(chosen) >= kmax:
            return
        for v in range(start, n):
            if ok_add(v):
                chosen.append(v)
                rec(v + 1)
                chosen.pop()

    rec(0)
    return hist, state["nodes"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7, 8])
    ap.add_argument("--kmax", type=int, default=None)
    args = ap.parse_args()

    KNOWN_K = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8}

    rows = []
    for q in args.q:
        t0 = time.time()
        F, ovoid, circles = build(q)
        n = len(ovoid)
        kmax = args.kmax if args.kmax is not None else KNOWN_K.get(q, q + 2) + 1
        hist, nodes = count_arcs(F, ovoid, circles, kmax)
        dt = time.time() - t0
        K = max(hist)
        known = KNOWN_K.get(q)
        row = {"q": q, "points": n, "circles": len(circles),
               "arc_counts": {str(k): v for k, v in sorted(hist.items())},
               "K_from_arcs": K, "known_K": known,
               "match": (K == known) if known else None,
               "nodes": nodes, "seconds": round(dt, 2)}
        rows.append(row)
        print(f"q={q:>3} n={n:>4}: K={K} (known {known}) "
              f"{'OK' if row['match'] else '?'}", flush=True)
        print(f"        counts {dict(sorted(hist.items()))}", flush=True)
        print(f"        {nodes} nodes, {dt:.1f}s", flush=True)

    print()
    print("K is the largest k with a nonzero arc count.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
