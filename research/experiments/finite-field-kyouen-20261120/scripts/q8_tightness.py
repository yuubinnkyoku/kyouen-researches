"""THE q=8 TIGHTNESS: a 5-point maximal set forces a perfect resolution.

For a maximal safe set S of size k in the inversive plane of order q, the
blocking count is

    (number of triples of S) x (outside points per circle)
        = C(k,3) * (q - 2)

and every one of the q^2 + 1 - k outside points must be covered at least
once.  So

    q^2 + 1 - k  <=  C(k,3) * (q - 2).                        (*)

For k = 5 this reads  q^2 - 4 <= 10(q-2), i.e. (q-2)(q-8) <= 0, i.e.
q <= 8.  At q = 8 the inequality is an EQUALITY:

    q^2 - 4 = 60 = 10 * (8 - 2).

Equality in (*) means every outside point is covered EXACTLY ONCE.  So at
q = 8 a 5-point maximal safe set forces the 10 circles through triples of
S to be pairwise disjoint outside S -- a perfect resolution of the 60
outside points into 10 blocks of 6.

This script verifies that structure on an actual q=8 witness.

Run:  python q8_tightness.py
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

from inversive_all_q import build_inversive_plane  # noqa: E402


def build(q: int):
    points, circles = build_inversive_plane(q)
    idx = {p: i for i, p in enumerate(points)}
    blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]
    n = len(points)
    tri_circle = {}
    for ci, B in enumerate(blocks):
        for tri in itertools.combinations(B, 3):
            tri_circle[tri] = ci
    circles_of = [[] for _ in range(n)]
    for ci, B in enumerate(blocks):
        for p in B:
            circles_of[p].append(ci)
    return n, blocks, tri_circle, circles_of


def find_maximal(n, blocks, tri_circle, circles_of, target, cap=5_000_000):
    chosen: list[int] = []
    inS = [False] * n
    block = [0] * n
    cnt = [0] * len(blocks)
    state = {"nodes": 0}
    out = []

    def add(v):
        inS[v] = True
        chosen.append(v)
        for ci in circles_of[v]:
            cnt[ci] += 1
            if cnt[ci] == 3:
                for p in blocks[ci]:
                    if not inS[p]:
                        block[p] += 1

    def rem(v):
        for ci in circles_of[v]:
            if cnt[ci] == 3:
                for p in blocks[ci]:
                    if not inS[p]:
                        block[p] -= 1
            cnt[ci] -= 1
        chosen.pop()
        inS[v] = False

    def rec(start):
        state["nodes"] += 1
        if state["nodes"] > cap:
            return True
        k = len(chosen)
        if k == target:
            if all(inS[p] or block[p] > 0 for p in range(n)):
                out.append(list(chosen))
                return True
            return False
        for v in range(start, n):
            if inS[v] or block[v] > 0:
                continue
            add(v)
            if rec(v + 1):
                return True
            rem(v)
        return False

    rec(0)
    return (out[0] if out else None), state["nodes"]


def analyse(q: int, S, n, blocks, tri_circle):
    Sset = set(S)
    circles_used = []
    for tri in itertools.combinations(sorted(S), 3):
        ci = tri_circle.get(tuple(sorted(tri)))
        if ci is not None:
            circles_used.append(ci)
    circles_used = sorted(set(circles_used))

    # multiplicity of each outside point
    mult = Counter()
    for ci in circles_used:
        for p in blocks[ci]:
            if p not in Sset:
                mult[p] += 1

    outside = [p for p in range(n) if p not in Sset]
    covered = [p for p in outside if mult[p] > 0]
    hist = Counter(mult[p] for p in outside)

    # are the circles pairwise disjoint outside S?
    disjoint = True
    for a, b in itertools.combinations(circles_used, 2):
        inter = (set(blocks[a]) & set(blocks[b])) - Sset
        if inter:
            disjoint = False
            break

    return {
        "q": q, "n": n, "k": len(S), "witness": S,
        "triples": comb(len(S), 3),
        "circles_used": len(circles_used),
        "outside_points": len(outside),
        "covered_outside": len(covered),
        "maximal": len(covered) == len(outside),
        "capacity": comb(len(S), 3) * (q - 2),
        "multiplicity_histogram": {str(k): v for k, v in sorted(hist.items())},
        "circles_disjoint_outside_S": disjoint,
        "tight": len(covered) == comb(len(S), 3) * (q - 2),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[8])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        t0 = time.time()
        n, blocks, tri_circle, circles_of = build(q)
        tb = time.time() - t0
        print(f"q={q}: built n={n}, {len(blocks)} circles in {tb:.1f}s",
              flush=True)
        w, nodes = find_maximal(n, blocks, tri_circle, circles_of, 5)
        if w is None:
            print(f"q={q}: no 5-point maximal set found", flush=True)
            continue
        r = analyse(q, w, n, blocks, tri_circle)
        r["build_seconds"] = round(tb, 2)
        r["search_nodes"] = nodes
        rows.append(r)
        print(f"  witness {w}", flush=True)
        print(f"  outside points      : {r['outside_points']}", flush=True)
        print(f"  covered outside     : {r['covered_outside']}", flush=True)
        print(f"  capacity C(k,3)(q-2): {r['capacity']}", flush=True)
        print(f"  multiplicity hist   : {r['multiplicity_histogram']}",
              flush=True)
        print(f"  circles disjoint outside S: "
              f"{r['circles_disjoint_outside_S']}", flush=True)
        print(f"  tight (covered == capacity): {r['tight']}", flush=True)

    print()
    print("At q=8 the blocking inequality is an equality, so a 5-point")
    print("maximal set forces every outside point to be covered exactly")
    print("once: the 10 triple-circles resolve the 60 outside points into")
    print("10 blocks of 6, pairwise disjoint outside S.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
