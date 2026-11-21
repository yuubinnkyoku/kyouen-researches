"""UNIFIED ARC-COUNT TABLE: all k at once, with the closed forms checked.

This is the consolidated harness for the arc-count programme.  It

  (1) enumerates arcs by size for each q (exhaustive, with a node cap);
  (2) checks the closed forms for k <= 5;
  (3) checks the k=6 pure formula;
  (4) reports K as the largest k with a nonzero count.

Run:  python arc_table.py --q 3 4 5 7 8
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from collections import Counter
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_on_quadric import build  # noqa: E402
from arc_k6_pure import arcs6  # noqa: E402


def enumerate_arcs(q: int, kmax: int, cap: int = 100_000_000):
    F, ovoid, circles = build(q)
    n = len(ovoid)
    circ_of_quad = {}
    for ci, B in enumerate(circles):
        for quad in itertools.combinations(B, 4):
            circ_of_quad[quad] = ci

    hist = Counter()
    chosen: list[int] = []
    state = {"nodes": 0, "capped": False}

    def ok_add(v):
        for tri in itertools.combinations(chosen, 3):
            if tuple(sorted((tri[0], tri[1], tri[2], v))) in circ_of_quad:
                return False
        return True

    def rec(start):
        state["nodes"] += 1
        if state["nodes"] > cap:
            state["capped"] = True
            return
        hist[len(chosen)] += 1
        if len(chosen) >= kmax:
            return
        for v in range(start, n):
            if ok_add(v):
                chosen.append(v)
                rec(v + 1)
                chosen.pop()
                if state["capped"]:
                    return

    rec(0)
    return hist, state["nodes"], state["capped"]


def closed_form(q: int, k: int):
    """Closed form for #k-arcs where known, else None."""
    n = q * q + 1
    b = q * (q * q + 1)
    s = q + 1
    if k <= 3:
        return comb(n, k)
    if k == 4:
        return comb(n, 4) - b * comb(s, 4)
    if k == 5:
        return (comb(n, 5) - b * comb(s, 5)
                - b * comb(s, 4) * (n - s))
    if k == 6:
        val, _ = arcs6(q)
        return val
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    ap.add_argument("--kmax", type=int, default=None)
    ap.add_argument("--cap", type=int, default=100_000_000)
    args = ap.parse_args()

    KNOWN_K = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8}

    rows = []
    for q in args.q:
        kmax = args.kmax if args.kmax is not None else KNOWN_K.get(q, q + 2) + 1
        t0 = time.time()
        hist, nodes, capped = enumerate_arcs(q, kmax, cap=args.cap)
        dt = time.time() - t0
        K = max(hist)
        known = KNOWN_K.get(q)
        print(f"q={q}: n={q*q+1}, K={K} (known {known}) "
              f"{'OK' if K == known else '?'}  [{nodes} nodes, {dt:.1f}s"
              + (", CAPPED" if capped else "") + "]", flush=True)
        checks = []
        for k in sorted(hist):
            cf = closed_form(q, k)
            if cf is None:
                continue
            ok = abs(hist[k] - cf) < 1e-6
            checks.append({"k": k, "exhaustive": hist[k], "closed": cf,
                           "ok": ok})
            print(f"   k={k}: exhaustive {hist[k]}, closed {cf}, "
                  f"{'OK' if ok else 'MISMATCH'}", flush=True)
        rows.append({"q": q, "n": q * q + 1, "K": K, "known_K": known,
                     "histogram": {str(k): v for k, v in sorted(hist.items())},
                     "closed_form_checks": checks,
                     "nodes": nodes, "capped": capped,
                     "seconds": round(dt, 2)})

    print()
    print("=== summary ===")
    print(f"{'q':>3} {'K':>3} {'closed forms verified':>22}")
    for r in rows:
        ok = sum(1 for c in r["closed_form_checks"] if c["ok"])
        tot = len(r["closed_form_checks"])
        print(f"{r['q']:>3} {r['K']:>3} {f'{ok}/{tot}':>22}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
