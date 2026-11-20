"""Systematic sweep of Steiner 3-designs: how close is K to the lambda_2 bound?

For a t-(v,s,1) design with t = 3 the general bound is

    K <= lambda_2 + 2,     lambda_2 = (v-2)/(s-2).

Witt S(3,6,22) attains it (K = 7 = 5 + 2).  This script builds every
admissible small Steiner 3-design by exact cover and computes K exactly,
so we can see the DEFICIT  lambda_2 + 2 - K.

Admissible (v,s) for t = 3 (integrality of lambda_2 and of b):

    s = 4 :  v = 2, 4 (mod 6)
    s = 5 :  v = 2 (mod 3)
    s = 6 :  v = 2 (mod 4)
    s = 7 :  v = 2 (mod 5)
    s = 8 :  v = 2 (mod 6)

Run:  python steiner3_sweep.py
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from steiner3_kyouen import check_design, max_safe, steiner_design  # noqa: E402


def admissible(s: int, vmax: int):
    """All v <= vmax with lambda_2 and b integral."""
    out = []
    for v in range(s + 1, vmax + 1):
        if (v - 2) % (s - 2) != 0:
            continue
        lam2 = (v - 2) // (s - 2)
        if lam2 < 1:
            continue
        num = comb(v, 3)
        den = comb(s, 3)
        if num % den != 0:
            continue
        out.append((v, lam2, num // den))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--vmax", type=int, default=30)
    ap.add_argument("--node-cap", type=int, default=20_000_000)
    ap.add_argument("--safe-cap", type=int, default=20_000_000)
    args = ap.parse_args()

    rows = []
    for s in (4, 5, 6, 7, 8):
        cands = admissible(s, args.vmax)
        if not cands:
            continue
        print(f"--- s = {s} : candidates {[(v, l) for v, l, _ in cands]} ---",
              flush=True)
        for v, lam2, b in cands:
            t0 = time.time()
            try:
                blocks, nodes = steiner_design(v, s, 3, node_cap=args.node_cap)
            except RuntimeError as exc:
                print(f"  v={v:>3} s={s} lam2={lam2:>2}: design build failed "
                      f"({exc})", flush=True)
                rows.append({"v": v, "s": s, "lambda_2": lam2, "b": b,
                             "status": "design-build-failed"})
                continue
            if blocks is None:
                print(f"  v={v:>3} s={s} lam2={lam2:>2}: NO DESIGN "
                      f"({nodes} nodes)", flush=True)
                rows.append({"v": v, "s": s, "lambda_2": lam2, "b": b,
                             "status": "no-design", "nodes": nodes})
                continue
            design = check_design(v, blocks, 3)
            try:
                best, snodes = max_safe(v, blocks, node_cap=args.safe_cap)
                K = len(best)
                err = None
            except RuntimeError as exc:
                K, best, snodes, err = None, None, -1, str(exc)
            dt = time.time() - t0
            bound = lam2 + 2
            deficit = (bound - K) if K is not None else None
            rows.append({
                "v": v, "s": s, "lambda_2": lam2, "b": b,
                "K": K, "bound": bound, "deficit": deficit,
                "witness": best, "design_ok": design["is_design"],
                "nodes": nodes, "search_nodes": snodes,
                "seconds": round(dt, 2), "error": err,
                "status": "ok" if K is not None else "search-failed",
            })
            print(f"  v={v:>3} s={s} lam2={lam2:>2} b={b:>4}  K={K}  "
                  f"bound={bound}  deficit={deficit}  {dt:.1f}s"
                  + (f"  ERROR {err}" if err else ""), flush=True)

    ok = [r for r in rows if r.get("status") == "ok"]
    print()
    print(f"{len(ok)} designs solved.")
    if ok:
        tight = [r for r in ok if r["deficit"] == 0]
        print(f"bound attained (deficit 0): {[(r['v'], r['s']) for r in tight]}")
        print(f"deficits: {sorted({r['deficit'] for r in ok})}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
