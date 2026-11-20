"""Structural analysis of maximum 3-arcs: what do they look like?

A 3-arc in the inversive plane of order q is a set meeting every circle in at
most 3 points.  Our K is the maximum size.

Let us examine the structure of maximum 3-arcs for small q:
  * the "circle profile": how many circles meet the arc in 0,1,2,3 points,
  * whether the arc is contained in a "nice" configuration,
  * the stabiliser size (symmetry).

This may reveal a pattern that suggests a construction or a bound.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_bfs import build_field, circles_bfs, projective_line  # noqa: E402


def find_max_arc(q: int, node_cap: int = 20_000_000):
    F, sub = build_field(q)
    pts = projective_line(F)
    circles = circles_bfs(F, sub, pts)
    idx = {p: i for i, p in enumerate(pts)}
    blocks = [sorted(idx[p] for p in c) for c in circles]
    n = len(pts)
    n_blocks = len(blocks)
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)

    nodes = 0
    best = [0, None]

    def rec(start: int, chosen: list, pmask: int, cnt: list):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError
        if len(chosen) > best[0]:
            best[0] = len(chosen)
            best[1] = list(chosen)
        for p in range(start, n):
            if pmask >> p & 1:
                continue
            ok = True
            for bi in through[p]:
                if cnt[bi] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for bi in through[p]:
                cnt[bi] += 1
            chosen.append(p)
            rec(p + 1, chosen, pmask | (1 << p), cnt)
            chosen.pop()
            for bi in through[p]:
                cnt[bi] -= 1

    cnt = [0] * n_blocks
    pmask = 0
    fixed = [0, 1, 2]
    for p in fixed:
        for bi in through[p]:
            cnt[bi] += 1
        pmask |= 1 << p
    try:
        rec(3, list(fixed), pmask, cnt)
        status = "complete"
    except TimeoutError:
        status = "capped"
    return best[0], best[1], nodes, status, pts, blocks


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        k, S, nodes, status, pts, blocks = find_max_arc(q)
        if S is None:
            continue
        Sset = set(S)
        prof = Counter()
        for b in blocks:
            prof[len(set(b) & Sset)] += 1
        # symmetry: count automorphisms of the arc within PGL(2,q^2)?
        # too expensive; instead report the profile
        rows.append({"q": q, "K": k, "nodes": nodes, "status": status,
                     "circle_profile": dict(sorted(prof.items())),
                     "num_circles": len(blocks)})
        print(f"q={q}: K={k} ({status}, nodes={nodes})", flush=True)
        print(f"   circle profile (points of arc per circle): "
              f"{dict(sorted(prof.items()))}", flush=True)
        # check: sum of profile * count should equal k * (circles through a point)
        total_inc = sum(c * n for c, n in prof.items())
        print(f"   total incidences: {total_inc}, k*(q+1) = {k*(q+1)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
