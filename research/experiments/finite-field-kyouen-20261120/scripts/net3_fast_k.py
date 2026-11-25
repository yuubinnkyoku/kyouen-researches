"""FAST SEARCH FOR K USING THE CYCLIC STRUCTURE.

The normalised problem is

    K(inversive q) = 3 + max{ |T| : {0,1,inf} u T safe },   T in F_{q^2}\\F_q.

Family B says T is a partial transversal of the 3-net, which is the
addition table of Z_{q+1}.  But T lives in F_{q^2} \\ F_q, not in F_q, so
the alpha coordinates of F_q do not directly label T.

STILL, the 3-net gives a strong filter: T must meet each class of P_0,
P_1, P_inf at most once.  That is what net3_two_phase.py exploits.

THIS SCRIPT adds a much better filter: instead of enumerating ALL partial
transversals, enumerate them in DECREASING size and stop at the first that
passes families C and D.  Combined with a good branching order this should
reach q = 11, 13.

Run:  python net3_fast_k.py --q 3 4 5 7 8 9 11
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from crossratio_graph import concyclic  # noqa: E402
from inversive_all_q import build_field  # noqa: E402
from net3_transversal import build_partitions  # noqa: E402


def class_ids(verts, parts):
    pos = {repr(z): i for i, z in enumerate(verts)}
    out = []
    for P in parts:
        arr = [None] * len(verts)
        for k, key in enumerate(sorted(P)):
            for z in P[key]:
                arr[pos[repr(z)]] = k
        out.append(arr)
    return out


def solve(q: int, cap: int = 200_000_000):
    F, sub, verts, parts = build_partitions(q)
    cid = class_ids(verts, parts)
    n = len(verts)
    nparts = len(cid)
    sizes = [max(a for a in arr if a is not None) + 1 for arr in cid]

    zero, one, inf = F.zero, F.one, None
    state = {"nodes": 0, "best": []}

    used = [[False] * s for s in sizes]
    chosen: list[int] = []

    def ok_add(v):
        z = verts[v]
        for u in chosen:
            w = verts[u]
            if (concyclic(F, sub, (zero, one, z, w))
                    or concyclic(F, sub, (zero, inf, z, w))
                    or concyclic(F, sub, (one, inf, z, w))):
                return False
        for u, w2 in itertools.combinations(chosen, 2):
            a, b = verts[u], verts[w2]
            if (concyclic(F, sub, (zero, z, a, b))
                    or concyclic(F, sub, (one, z, a, b))
                    or concyclic(F, sub, (inf, z, a, b))):
                return False
        for u, w2, w3 in itertools.combinations(chosen, 3):
            if concyclic(F, sub, (z, verts[u], verts[w2], verts[w3])):
                return False
        return True

    def rec(start: int) -> None:
        state["nodes"] += 1
        if state["nodes"] > cap:
            raise RuntimeError("node cap exceeded")
        if len(chosen) > len(state["best"]):
            state["best"] = chosen.copy()
        if len(chosen) + (n - start) <= len(state["best"]):
            return
        for v in range(start, n):
            ok = True
            for pi in range(nparts):
                c = cid[pi][v]
                if c is None or used[pi][c]:
                    ok = False
                    break
            if not ok:
                continue
            if not ok_add(v):
                continue
            for pi in range(nparts):
                used[pi][cid[pi][v]] = True
            chosen.append(v)
            rec(v + 1)
            chosen.pop()
            for pi in range(nparts):
                used[pi][cid[pi][v]] = False

    rec(0)
    return 3 + len(state["best"]), state["nodes"], state["best"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7, 8, 9])
    ap.add_argument("--cap", type=int, default=200_000_000)
    args = ap.parse_args()

    INV_K = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8}

    rows = []
    print(f"{'q':>3} {'|V|':>5} {'K':>4} {'known':>6} {'match':>6} "
          f"{'nodes':>12} {'sec':>8}")
    for q in args.q:
        t0 = time.time()
        try:
            K, nodes, best = solve(q, cap=args.cap)
            err = None
        except RuntimeError as exc:
            K, nodes, best, err = None, -1, None, str(exc)
        dt = time.time() - t0
        known = INV_K.get(q)
        match = (K == known) if (K is not None and known is not None) else None
        rows.append({"q": q, "K": K, "known": known, "match": match,
                     "nodes": nodes, "seconds": round(dt, 2), "error": err})
        print(f"{q:>3} {q*q-q:>5} {K!s:>4} {known!s:>6} {match!s:>6} "
              f"{nodes:>12} {dt:>8.1f}"
              + (f"  ERROR {err}" if err else ""), flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
