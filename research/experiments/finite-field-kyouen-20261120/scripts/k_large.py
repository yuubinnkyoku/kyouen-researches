"""K(q) FOR LARGER q, USING THE FAST OVOID CONSTRUCTION.

The ovoid model builds the inversive plane in O(q^3), so q = 13, 16, 17
are now reachable for the maximum-safe-set search.

The search is the standard DFS with the 3-net filter (family B) plus the
cross-ratio check for families C and D.  But the cross-ratio machinery was
built for the P^1(F_{q^2}) model; here we have the ovoid model, so we use
the plain "does adding v complete a 4-point circle" test, which is exact
and needs no cross-ratio.

SPEEDUP.  Maintain cnt[circle] = number of S-points on each circle.  Adding
v is legal iff no circle through v already has 3 points of S.

Run:  python k_large.py --q 13 16 17
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s_q_large import build  # noqa: E402


def max_safe(n, blocks, circles_of, node_cap=200_000_000):
    """Maximum safe set size, with the incremental circle counter."""
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
    print(f"{'q':>3} {'n':>4} {'circles':>8} {'K':>4} {'known':>6} "
          f"{'match':>6} {'nodes':>12} {'sec':>8}")
    for q in args.q:
        t0 = time.time()
        n, blocks, tri_circle, circles_of = build(q)
        tb = time.time() - t0
        try:
            best, nodes, capped = max_safe(n, blocks, circles_of,
                                           node_cap=args.cap)
            K, err = len(best), None
        except Exception as exc:  # noqa: BLE001
            K, best, nodes, capped, err = None, None, -1, False, repr(exc)
        dt = time.time() - t0
        known = KNOWN.get(q)
        match = (K == known) if (K is not None and known is not None) else None
        row = {"q": q, "n": n, "circles": len(blocks), "K": K,
               "known": known, "match": match, "witness": best,
               "nodes": nodes, "capped": capped,
               "build_seconds": round(tb, 2),
               "total_seconds": round(dt, 2), "error": err}
        rows.append(row)
        print(f"{q:>3} {n:>4} {len(blocks):>8} {K!s:>4} {known!s:>6} "
              f"{match!s:>6} {nodes:>12} {dt:>8.1f}"
              + ("  CAPPED" if capped else "")
              + (f"  ERROR {err}" if err else ""), flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
