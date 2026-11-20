"""TWO-PHASE SEARCH: use the 3-net as a filter, then check families C and D.

The normalised reformulation is

    K(inversive q) = 3 + max{ |T| : {0,1,inf} u T safe },   T in F_{q^2}\\F_q.

Family B (pairs) is exactly "T is a partial transversal of the 3-net
(P_0, P_1, P_inf)".  Families C and D are higher-order and cannot be
expressed through the net.

So search in two phases:

  PHASE 1  enumerate partial transversals of the 3-net, largest first.
           This is a much smaller space than all subsets.
  PHASE 2  for each candidate, check families C and D by cross-ratio.

Because family B is NECESSARY, phase 1 loses nothing.  The win is that the
net constraint prunes enormously: a partial transversal of size m in a
3-net with q classes of size q-1 has at most one point per class, so
m <= q automatically.

This makes q = 11, 13 reachable.

Run:  python net3_two_phase.py --q 3 4 5 7 8 9 11
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


def phase1_transversals(verts, cid, min_size, cap=20_000_000):
    """All partial transversals of the 3-net with size >= min_size."""
    n = len(verts)
    nparts = len(cid)
    used = [[False] * (max(a for a in arr if a is not None) + 1) for arr in cid]
    cur: list[int] = []
    found: list[list[int]] = []
    state = {"nodes": 0}

    def rec(start: int) -> None:
        state["nodes"] += 1
        if state["nodes"] > cap:
            raise RuntimeError("node cap exceeded")
        if len(cur) >= min_size:
            found.append(cur.copy())
        if len(cur) == n:
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
            for pi in range(nparts):
                used[pi][cid[pi][v]] = True
            cur.append(v)
            rec(v + 1)
            cur.pop()
            for pi in range(nparts):
                used[pi][cid[pi][v]] = False

    rec(0)
    return found, state["nodes"]


def phase2_ok(F, sub, verts, T):
    """Check families C and D on the candidate T (indices into verts)."""
    zero, one, inf = F.zero, F.one, None
    pts = [verts[i] for i in T]
    m = len(pts)
    # family C: no 3 points of T on a circle through an anchor
    for a in (zero, one, inf):
        for tri in itertools.combinations(range(m), 3):
            if concyclic(F, sub, (a, pts[tri[0]], pts[tri[1]], pts[tri[2]])):
                return False
    # family D: no 4 points of T concyclic
    for quad in itertools.combinations(range(m), 4):
        if concyclic(F, sub, tuple(pts[i] for i in quad)):
            return False
    return True


def solve(q: int, cap: int = 20_000_000):
    F, sub, verts, parts = build_field_and_parts(q)
    cid = class_ids(verts, parts)
    n = len(verts)

    # find tau_3 first (largest transversal), then descend
    for target in range(q, 0, -1):
        try:
            cands, nodes = phase1_transversals(verts, cid, target, cap=cap)
        except RuntimeError as exc:
            return {"q": q, "error": str(exc), "tau_lower": target + 1}
        if not cands:
            continue
        for T in cands:
            if phase2_ok(F, sub, verts, T):
                return {"q": q, "K": 3 + len(T),
                        "witness": [repr(verts[i]) for i in T],
                        "candidates_at_size": len(cands),
                        "phase1_nodes": nodes}
    return {"q": q, "K": 3, "witness": [], "note": "no T of size >= 1"}


def build_field_and_parts(q):
    F, sub, verts, parts = build_partitions(q)
    return F, sub, verts, parts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7, 8, 9])
    ap.add_argument("--cap", type=int, default=20_000_000)
    args = ap.parse_args()

    INV_K = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8}

    rows = []
    print(f"{'q':>3} {'|V|':>5} {'K':>4} {'known':>6} {'match':>6} {'cands':>8} "
          f"{'nodes':>10} {'sec':>7}")
    for q in args.q:
        t0 = time.time()
        try:
            r = solve(q, cap=args.cap)
        except Exception as exc:  # noqa: BLE001
            r = {"q": q, "error": repr(exc)}
        dt = time.time() - t0
        K = r.get("K")
        known = INV_K.get(q)
        match = (K == known) if (K is not None and known is not None) else None
        rows.append({**r, "known": known, "match": match,
                     "seconds": round(dt, 2)})
        print(f"{q:>3} {q*q-q:>5} {K!s:>4} {known!s:>6} {match!s:>6} "
              f"{r.get('candidates_at_size', '-'):>8} "
              f"{r.get('phase1_nodes', '-'):>10} {dt:>7.1f}"
              + (f"  ERROR {r['error']}" if "error" in r else ""), flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
