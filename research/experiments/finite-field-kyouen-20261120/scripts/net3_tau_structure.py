"""THE 3-NET TRANSVERSAL NUMBER tau_3(q): structure and bounds.

The three partitions of F_{q^2} \\ F_q (q^2-q points) into q classes of
size q-1 are

    P_0   : classes = F_q-lines through 0, minus F_q
    P_1   : classes = F_q-lines through 1, minus F_q
    P_inf : classes = phi^{-1}(F_q-lines through 0), phi(z) = z/(1-z)

A partial transversal picks at most one point per class in each partition.
Since each partition has q classes, tau_3 <= q trivially.

THE GROUP STRUCTURE.  F_{q^2}^* is cyclic of order q^2-1, and F_q^* is the
subgroup of order q-1.  The quotient F_{q^2}^*/F_q^* has order q+1.  So the
q^2-q = (q-1)(q+1) points of F_{q^2} \\ F_q split as

    (q-1) cosets of F_q^*  x  (q+1) elements of the quotient.

P_0 is exactly the coset decomposition: its q classes are NOT the cosets
(there are q+1 of those) but the F_q-lines through 0, which are the cosets
of F_q^* acting by multiplication -- and there are q+1 of them, not q.

Let me just compute the structure numerically: the intersection matrix of
the three partitions, and the exact tau_3 for as many q as possible.

Run:  python net3_tau_structure.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

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


def tau3(verts, cid, cap=50_000_000):
    """Exact maximum partial transversal of the 3-net."""
    n = len(verts)
    nparts = len(cid)
    sizes = [max(a for a in arr if a is not None) + 1 for arr in cid]
    used = [[False] * s for s in sizes]
    cur: list[int] = []
    best: list[list[int]] = [[]]
    state = {"nodes": 0}

    def rec(start: int) -> None:
        state["nodes"] += 1
        if state["nodes"] > cap:
            raise RuntimeError("node cap exceeded")
        if len(cur) > len(best[0]):
            best[0] = cur.copy()
        if len(cur) + (n - start) <= len(best[0]):
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
    return best[0], state["nodes"]


def intersection_matrix(cid, p, r):
    """How many points lie in class i of partition p and class j of partition r."""
    sizes_p = max(a for a in cid[p] if a is not None) + 1
    sizes_r = max(a for a in cid[r] if a is not None) + 1
    M = [[0] * sizes_r for _ in range(sizes_p)]
    for v in range(len(cid[0])):
        a, b = cid[p][v], cid[r][v]
        if a is None or b is None:
            continue
        M[a][b] += 1
    return M


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7, 8, 9])
    ap.add_argument("--cap", type=int, default=50_000_000)
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'|V|':>5} {'tau_3':>6} {'q':>4} {'tau/q':>6} "
          f"{'nodes':>10} {'sec':>7}")
    for q in args.q:
        t0 = time.time()
        F, sub, verts, parts = build_partitions(q)
        cid = class_ids(verts, parts)
        try:
            tv, nodes = tau3(verts, cid, cap=args.cap)
            tau, err = len(tv), None
        except RuntimeError as exc:
            tau, tv, nodes, err = None, None, -1, str(exc)
        dt = time.time() - t0

        # intersection matrices between the three partitions
        mats = {}
        for (p, r, name) in ((0, 1, "P0-P1"), (0, 2, "P0-Pinf"),
                             (1, 2, "P1-Pinf")):
            M = intersection_matrix(cid, p, r)
            flat = sorted({x for row in M for x in row})
            mats[name] = {"distinct_entries": flat,
                          "is_constant": len(flat) == 1}
        row = {"q": q, "vertices": len(verts), "tau_3": tau,
               "q_bound": q, "ratio": round(tau / q, 4) if tau else None,
               "nodes": nodes, "seconds": round(dt, 2),
               "intersections": mats, "error": err}
        rows.append(row)
        print(f"{q:>3} {len(verts):>5} {tau!s:>6} {q:>4} "
              f"{(tau/q if tau else 0):>6.3f} {nodes:>10} {dt:>7.1f}"
              + (f"  ERROR {err}" if err else ""), flush=True)
        for name, m in mats.items():
            print(f"      {name}: entries {m['distinct_entries']} "
                  f"constant={m['is_constant']}", flush=True)

    print()
    print("tau_3 <= q always (q classes per partition).")
    print("If the intersection matrices are constant, the 3-net is")
    print("'uniform' and tau_3 is governed by the transversal design.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
