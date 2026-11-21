"""s(q) FOR q = 16, 17: how far above k* does the minimum go?

The defect delta = C(k,3)(q-2) - (q^2+1-k) drops sharply:

    q=13, k=6: delta = 56
    q=16, k=6: delta = 29
    q=17, k=6: delta = 16

Random 6-sets leave 69 (q=16) and 54 (q=17) unblocked, far worse than the
14 seen at q=13.  So s(16), s(17) are well above 6.

This script searches upward in k until a maximal set is found, giving
s(q) for q = 16, 17.

Run:  python s_q_1617.py
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s_q_large import build, kstar, one_trial  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[16, 17])
    ap.add_argument("--trials", type=int, default=3000)
    ap.add_argument("--kmax", type=int, default=14)
    ap.add_argument("--seed", type=int, default=20261122)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        t0 = time.time()
        n, blocks, tri_circle, circles_of = build(q)
        tb = time.time() - t0
        ks = kstar(q)
        print(f"q={q}: n={n}, {len(blocks)} circles, k*={ks}, "
              f"build {tb:.1f}s", flush=True)
        rng = random.Random(args.seed + q)
        s_found = None
        for target in range(ks, args.kmax + 1):
            found = None
            best = None
            t = 0
            for t in range(args.trials):
                r = one_trial(n, blocks, tri_circle, circles_of, target, rng)
                if r is None:
                    continue
                w, nun = r
                if best is None or nun < best[1]:
                    best = (w, nun)
                if nun == 0:
                    found = w
                    break
            status = (f"FOUND {found}" if found
                      else f"best unblocked={best[1] if best else '-'}")
            print(f"  size {target}: {status}  [{t+1} trials]", flush=True)
            rows.append({"q": q, "n": n, "k_star": ks, "target": target,
                         "found": found is not None, "witness": found,
                         "best_unblocked": best[1] if best else None,
                         "trials": t + 1})
            if found:
                s_found = target
                break
        print(f"  => s({q}) = {s_found}", flush=True)
        rows.append({"q": q, "s": s_found, "k_star": ks,
                     "gap": (s_found - ks) if s_found else None,
                     "build_seconds": round(tb, 2)})

    print()
    print("s(q) - k* measures how far the blocking bound is from tight.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
