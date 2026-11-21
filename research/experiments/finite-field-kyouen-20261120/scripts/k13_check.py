"""INDEPENDENT CHECK OF K(13) = 8 ON THE OVOID MODEL.

The value K(inversive q=13) = 8 came from the fixed-bitset C++ program
(agq_fixed.cpp / inv_fixed.cpp) after the 64-bit mask bug was found.  It is
worth an INDEPENDENT check on a completely different construction (the
elliptic quadric model in Python).

The ovoid model builds the inversive plane of order q in O(q^3), so q=13
is feasible (n=170, 2210 circles).

The search: maximum set with no 4 coplanar.  Use the incremental circle
counter (cnt[circle] = number of S-points on it); adding v is legal iff no
circle through v already has 3 points of S.

Run:  python k13_check.py
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s_q_large import build  # noqa: E402


def max_safe(n, blocks, circles_of, node_cap=200_000_000):
    cnt = [0] * len(blocks)
    chosen: list[int] = []
    best: list[list[int]] = [[]]
    state = {"nodes": 0, "capped": False}

    def rec(start: int) -> None:
        state["nodes"] += 1
        if state["nodes"] > node_cap:
            state["capped"] = True
            return
        if len(chosen) > len(best[0]):
            best[0] = chosen.copy()
        if len(chosen) + (n - start) <= len(best[0]):
            return
        for v in range(start, n):
            ok = True
            for ci in circles_of[v]:
                if cnt[ci] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for ci in circles_of[v]:
                cnt[ci] += 1
            chosen.append(v)
            rec(v + 1)
            chosen.pop()
            for ci in circles_of[v]:
                cnt[ci] -= 1
            if state["capped"]:
                return

    rec(0)
    return best[0], state["nodes"], state["capped"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[13])
    ap.add_argument("--cap", type=int, default=200_000_000)
    args = ap.parse_args()

    KNOWN = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8}

    rows = []
    for q in args.q:
        t0 = time.time()
        n, blocks, tri_circle, circles_of = build(q)
        tb = time.time() - t0
        print(f"q={q}: n={n}, {len(blocks)} circles, "
              f"circle size {len(blocks[0])}, build {tb:.1f}s", flush=True)
        best, nodes, capped = max_safe(n, blocks, circles_of,
                                       node_cap=args.cap)
        dt = time.time() - t0
        K = len(best)
        known = KNOWN.get(q)
        row = {"q": q, "n": n, "circles": len(blocks), "K": K,
               "known": known, "match": K == known, "witness": best,
               "nodes": nodes, "capped": capped,
               "build_seconds": round(tb, 2),
               "total_seconds": round(dt, 2)}
        rows.append(row)
        print(f"  K = {K} (known {known}) match={K == known}  "
              f"[{nodes} nodes, {dt:.1f}s"
              + (", CAPPED" if capped else "") + "]", flush=True)
        print(f"  witness: {best}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
