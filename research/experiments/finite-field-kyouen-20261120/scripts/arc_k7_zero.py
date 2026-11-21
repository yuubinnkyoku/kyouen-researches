"""k=7 AT q=5: ZERO ARCS, and why.

MEASURED: for q=5, ALL C(26,7) = 657800 seven-subsets are bad.  So there is
no 7-arc, consistent with K(5) = 6.

The profiles are:

    (4,4,4,4)      312000
    (4,4,4)         96200
    (5,4,4)         85800
    (4,4,4,4,4)     78000
    (5,4)           62400
    (4,4)           15600
    (4,4,4,4,4,4)    5200
    (6,)             2600
    ----------------------
    total          657800

WHY NO 7-ARC AT q=5?  A 7-set S is an arc iff no circle carries 4 of its
points.  At q=5 a circle has 6 points, and there are 130 circles.

The blocking bound: a maximal safe set of size k needs
    q^2+1-k <= C(k,3)*(q-2)
For q=5, k=7: 20 <= 35*3 = 105.  Satisfied, so the bound does not forbid it.

But the ARC count is zero.  So the obstruction is geometric, not counting.

Let me check: is there a 7-arc for larger q?  K(7) = 6, so no.  K(8) = 7,
so yes at q=8.  K(9) = 9, K(11) = 9.

So the first q with a 7-arc is q=8.

This script confirms the q=5 zero and checks q=7 (K=6, so also zero) and
q=8 (K=7, so at least one).

Run:  python arc_k7_zero.py --q 5 7 8
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_on_quadric import build  # noqa: E402


def count_arcs_of_size(q: int, k: int, cap=50_000_000):
    F, ovoid, circles = build(q)
    n = len(ovoid)
    circ_of_quad = {}
    for ci, B in enumerate(circles):
        for quad in itertools.combinations(B, 4):
            circ_of_quad[quad] = ci

    cnt = 0
    nodes = 0
    chosen: list[int] = []

    def ok_add(v):
        for tri in itertools.combinations(chosen, 3):
            if tuple(sorted((tri[0], tri[1], tri[2], v))) in circ_of_quad:
                return False
        return True

    def rec(start):
        nonlocal cnt, nodes
        nodes += 1
        if nodes > cap:
            raise RuntimeError("cap")
        if len(chosen) == k:
            cnt += 1
            return
        if len(chosen) + (n - start) < k:
            return
        for v in range(start, n):
            if ok_add(v):
                chosen.append(v)
                rec(v + 1)
                chosen.pop()

    try:
        rec(0)
        return cnt, nodes, False
    except RuntimeError:
        return cnt, nodes, True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7, 8])
    ap.add_argument("--k", type=int, default=7)
    args = ap.parse_args()

    KNOWN_K = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8}

    rows = []
    for q in args.q:
        cnt, nodes, capped = count_arcs_of_size(q, args.k)
        K = KNOWN_K.get(q)
        row = {"q": q, "k": args.k, "arcs": cnt, "nodes": nodes,
               "capped": capped, "known_K": K,
               "consistent": (cnt > 0) == (K >= args.k) if K else None}
        rows.append(row)
        print(f"q={q}: {args.k}-arcs = {cnt}"
              + (" (CAPPED)" if capped else "")
              + f"  [K={K}, consistent={row['consistent']}]", flush=True)

    print()
    print("A k-arc exists iff K >= k.  This checks the arc counts against")
    print("the known K values.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
