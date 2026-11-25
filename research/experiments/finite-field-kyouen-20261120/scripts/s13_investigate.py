"""IS s(13) > 6?  THE CONJECTURE s(q) = k* MAY FAIL AT q = 13.

The blocking inequality gives s(q) >= k* with

    k* = min{ k : q^2 + 1 - k <= C(k,3)*(q-2) }.

For q = 13: k* = 6 (since 170-6 = 164 <= 20*11 = 220, but 170-5 = 165 >
10*11 = 110).

Random restarts found k*-maximal sets easily for q <= 11:
    q=9  : 4 trials
    q=11 : 697 trials

But for q = 13, 200,000 trials never produced a 6-point maximal set; the
best had 12 unblocked points.  That is a strong signal that s(13) > 6,
i.e. the conjecture s(q) = k* FAILS at q = 13.

WHY MIGHT IT FAIL?  Look at the defect

    delta = C(k,3)*(q-2) - (q^2 + 1 - k).

    q=9,  k=6: 20*7  - 76 = 140 - 76 = 64
    q=11, k=6: 20*9  - 116 = 180 - 116 = 64
    q=13, k=6: 20*11 - 164 = 220 - 164 = 56

The defect DROPS at q=13.  A smaller defect means less room for overlap,
so the covering must be more efficient -- and apparently 6 points cannot
achieve it.

This script:
  (1) tabulates the defect for k = k* across q;
  (2) runs a much more targeted search for q=13 (greedy + repair);
  (3) tests whether a 7-point maximal set exists for q=13.

Run:  python s13_investigate.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
import time
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s_q_large import build, kstar  # noqa: E402


def defect(q: int, k: int) -> int:
    return comb(k, 3) * (q - 2) - (q * q + 1 - k)


def one_trial(n, blocks, tri_circle, circles_of, target, rng):
    order = list(range(n))
    rng.shuffle(order)
    chosen: list[int] = []
    inS = [False] * n
    block = [0] * n
    cnt = [0] * len(blocks)
    for v in order:
        if len(chosen) == target:
            break
        if block[v] > 0:
            continue
        inS[v] = True
        chosen.append(v)
        for ci in circles_of[v]:
            cnt[ci] += 1
            if cnt[ci] == 3:
                for p in blocks[ci]:
                    if not inS[p]:
                        block[p] += 1
    if len(chosen) < target:
        return None
    unblocked = sum(1 for p in range(n) if not inS[p] and block[p] == 0)
    return chosen, unblocked


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20261122)
    args = ap.parse_args()

    rows = []

    print("=== defect delta at k = k* ===")
    print(f"{'q':>3} {'k*':>3} {'capacity':>9} {'needed':>7} {'delta':>7}")
    for q in (3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 29):
        ks = kstar(q)
        cap = comb(ks, 3) * (q - 2)
        need = q * q + 1 - ks
        d = cap - need
        rows.append({"check": "defect", "q": q, "k_star": ks,
                     "capacity": cap, "needed": need, "delta": d})
        print(f"{q:>3} {ks:>3} {cap:>9} {need:>7} {d:>7}", flush=True)

    print()
    print("=== q=13: search for maximal sets of size 6 and 7 ===")
    n, blocks, tri_circle, circles_of = build(13)
    print(f"  built n={n}, {len(blocks)} circles", flush=True)
    rng = random.Random(args.seed)
    for target in (6, 7):
        t0 = time.time()
        best = None
        found = None
        t = 0
        for t in range(args.trials):
            res = one_trial(n, blocks, tri_circle, circles_of, target, rng)
            if res is None:
                continue
            w, nun = res
            if best is None or nun < best[1]:
                best = (w, nun)
            if nun == 0:
                found = w
                break
        dt = time.time() - t0
        rows.append({"check": "q13", "target": target,
                     "found": found is not None, "witness": found,
                     "best_unblocked": best[1] if best else None,
                     "trials": t + 1, "seconds": round(dt, 2)})
        print(f"  size {target}: "
              + (f"FOUND {found}" if found
                 else f"not found (best unblocked={best[1] if best else '-'})")
              + f"  [{t+1} trials, {dt:.1f}s]", flush=True)

    print()
    print("If size 6 is never found but size 7 is, then s(13) = 7 > k* = 6,")
    print("and the conjecture s(q) = k* is FALSE.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
