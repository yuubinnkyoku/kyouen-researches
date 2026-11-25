"""Hill-climb inside the "graph" ansatz:  S = { (a, f(a)) : a in F_q }.

The random arc searches of K1251 plateau near 0.65q, but K1253/K1251 never
tested structured subsets.  A probe showed that maximum arcs really can be
graphs: size q-1 at q=7 and size q at q=9, both equal to the known K.  So the
graph ansatz, which has only q degrees of freedom instead of choosing subsets of
q^2+1 points, is worth searching properly.

Objective: the number of circles carrying four or more graph points,
    penalty(f) = sum over circles c of max(0, |graph(f) cap c| - 3),
zero exactly when the graph is an arc.  A move changes f at one argument; the
delta only involves the circles through the two affected points, so a neighbour
costs O(q^2) and a full sweep of all q(q-1) neighbours O(q^4).

Run:  python graph_hillclimb.py --q 7 9 11 13 16 17 --restarts 6 --steps 400
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from inversive_fast import build_circles  # noqa: E402
from arc_lift_verify import Lift  # noqa: E402


def build(q: int):
    """Return (m, table, through, circ_masks, blocks) with table[i][j] point ids."""
    lift = Lift(q)
    F, sub = build_field(q)
    points, blocks = build_circles(q, check_orbit_size=True)
    coord_index = {}
    for i, z in enumerate(points):
        if z is None:
            continue
        v = lift.coords(z)
        coord_index[(v[1], v[2])] = i
    sub_list = list(sub)
    table = [[coord_index[(a, b)] for b in sub_list] for a in sub_list]
    n_circles = len(blocks)
    return sub_list, table, blocks


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--restarts", type=int, default=5)
    ap.add_argument("--steps", type=int, default=300)
    args = ap.parse_args()

    for q in args.q:
        sub_list, table, blocks = build(q)
        m = len(sub_list)
        npoints = q * q + 1
        through = [[] for _ in range(npoints)]
        cmask = []
        for ci, B in enumerate(blocks):
            mask = 0
            for p in B:
                mask |= 1 << p
                through[p].append(ci)
            cmask.append(mask)
        rng = random.Random(99 + q)
        best_pen = None
        for restart in range(args.restarts):
            f = [rng.randrange(m) for _ in range(m)]
            S = [table[i][f[i]] for i in range(m)]
            if len(set(S)) != m:
                continue
            cnt = [0] * len(blocks)
            for p in S:
                for ci in through[p]:
                    cnt[ci] += 1
            pen = sum(max(0, c - 3) for c in cnt)
            for step in range(args.steps):
                if pen == 0:
                    break
                best_move = None
                best_delta = 0
                order = list(range(m))
                rng.shuffle(order)
                for i in order:
                    old = f[i]
                    for j in range(m):
                        if j == old:
                            continue
                        p_old = table[i][old]
                        p_new = table[i][j]
                        delta = 0
                        changed = set(through[p_old]) | set(through[p_new])
                        for ci in changed:
                            before = cnt[ci]
                            after = before
                            if ci in through[p_old]:
                                after -= 1
                            if ci in through[p_new]:
                                after += 1
                            delta += max(0, after - 3) - max(0, before - 3)
                        if delta < best_delta:
                            best_delta = delta
                            best_move = (i, old, j, p_old, p_new)
                            if delta <= -2:
                                break
                    if best_move and best_delta <= -2:
                        break
                if best_move is None:
                    break
                i, old, j, p_old, p_new = best_move
                f[i] = j
                for ci in through[p_old]:
                    cnt[ci] -= 1
                for ci in through[p_new]:
                    cnt[ci] += 1
                pen += best_delta
            if best_pen is None or pen < best_pen:
                best_pen = pen
            status = "ARC" if pen == 0 else f"penalty {pen}"
            print(f"q={q} restart {restart}: {status}", flush=True)
            if pen == 0:
                break
        print(f"q={q}: best penalty {best_pen} "
              f"({'graph arc of size ' + str(q) if best_pen == 0 else 'no full graph arc found'})",
              flush=True)


if __name__ == "__main__":
    main()
