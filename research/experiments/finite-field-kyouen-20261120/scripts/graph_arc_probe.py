"""Test structured "graph" families as candidates for large arcs.

The randomised searches plateau at about 0.65q points while the proven upper
bound is q+1 (K1252), so a structured family reaching q would have been missed.
The cheapest structured family to test is the graph of a function in the affine
model of the inversive plane (K1250):  z = a + b*u  with  b = f(a),  for every
a in F_q.

This script indexes the q^2 affine points by (a, b) in F_q and tests random
functions and random low-degree polynomials:  S = { point(a, f(a)) : a in F_q }.
It also greedily shrinks a graph to an arc when it is not one.

Run:  python graph_arc_probe.py --q 5 7 9 11 13 --trials 200
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


def build_index(q: int):
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
    # table[i][j] = point index with a = sub_list[i], b = sub_list[j]
    table = [[coord_index[(a, b)] for b in sub_list] for a in sub_list]
    return sub_list, table, blocks


def is_arc(blocks, chosen) -> bool:
    aset = set(chosen)
    for c in blocks:
        if len(aset.intersection(c)) >= 4:
            return False
    return True


def shrink(blocks, chosen) -> list:
    """Keep points in order while they preserve the arc condition."""
    keep = []
    for p in chosen:
        if is_arc(blocks, keep + [p]):
            keep.append(p)
    return keep


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--trials", type=int, default=200)
    args = ap.parse_args()

    for q in args.q:
        sub_list, table, blocks = build_index(q)
        m = len(sub_list)
        rng = random.Random(20261123 + q)
        best = 0
        best_kind = None
        full_graphs = 0
        for t in range(args.trials):
            kind = "random function" if t % 2 == 0 else "random quadratic"
            if kind == "random function":
                f = [rng.randrange(m) for _ in range(m)]
            else:
                # f(i) = c2*i^2 + c1*i + c0 over F_q using integer indices
                c2, c1, c0 = (rng.randrange(m) for _ in range(3))
                f = [(c2 * i * i + c1 * i + c0) % m for i in range(m)]
            chosen = [table[i][f[i]] for i in range(m)]
            if len(set(chosen)) != m:
                continue
            if is_arc(blocks, chosen):
                full_graphs += 1
                if best < m:
                    best = m
                    best_kind = kind
                continue
            kept = shrink(blocks, chosen)
            if len(kept) > best:
                best = len(kept)
                best_kind = f"greedy subset of a {kind}"
        print(f"q={q}: best {best}  ({best_kind}); full graphs that are arcs: {full_graphs}",
              flush=True)


if __name__ == "__main__":
    main()
