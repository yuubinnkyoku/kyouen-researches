"""STRENGTHENING s(13) = 7: a targeted search for a 6-point maximal set.

Random restarts never found a 6-point maximal set at q = 13 (200,000
trials, best 12 unblocked).  That is strong evidence but not proof.

A 6-point maximal set needs its C(6,3) = 20 triple-circles to cover all
164 outside points.  The capacity is 20*11 = 220, so the defect is 56:
the 20 circles must cover 164 of their 220 available outside slots, i.e.
they may waste at most 56 slots on overlaps.

KEY STRUCTURE.  Two triple-circles of S share 0, 1 or 2 points of S.
  - sharing 2 points: the circles meet in exactly those 2 points, so they
    waste NOTHING outside S.
  - sharing 1 point: they meet in that point plus at most 1 more, so they
    waste at most 1 outside slot.
  - sharing 0 points: they meet in at most 2 points, so they waste at most
    2 outside slots.

So the waste is bounded by the "intersection profile" of S.  A 6-set with
many disjoint triples wastes a lot.

This script computes, for random 6-sets, the exact waste and the number of
unblocked points, to see how far from maximal the best 6-sets are, and
whether the waste bound alone rules out maximality.

Run:  python s13_waste.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
from collections import Counter
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s_q_large import build  # noqa: E402


def analyse(S, n, blocks, tri_circle):
    Sset = set(S)
    circles = []
    for tri in itertools.combinations(sorted(S), 3):
        ci = tri_circle.get(tuple(sorted(tri)))
        if ci is not None:
            circles.append(ci)
    circles = sorted(set(circles))
    mult = Counter()
    for ci in circles:
        for p in blocks[ci]:
            if p not in Sset:
                mult[p] += 1
    outside = [p for p in range(n) if p not in Sset]
    covered = sum(1 for p in outside if mult[p] > 0)
    total_slots = sum(mult.values())
    waste = total_slots - covered
    return {
        "k": len(S), "circles": len(circles),
        "outside": len(outside), "covered": covered,
        "unblocked": len(outside) - covered,
        "total_slots": total_slots, "waste": waste,
        "capacity": comb(len(S), 3) * (len(blocks[0]) - 3),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, default=13)
    ap.add_argument("--samples", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261122)
    args = ap.parse_args()

    q = args.q
    n, blocks, tri_circle, circles_of = build(q)
    print(f"q={q}: n={n}, {len(blocks)} circles, circle size {len(blocks[0])}",
          flush=True)

    rng = random.Random(args.seed)
    rows = []
    for k in (6, 7):
        best = None
        hist = Counter()
        for _ in range(args.samples):
            S = rng.sample(range(n), k)
            # only safe sets matter
            ok = True
            for tri in itertools.combinations(sorted(S), 3):
                ci = tri_circle.get(tuple(sorted(tri)))
                if ci is None:
                    ok = False
                    break
            if not ok:
                continue
            r = analyse(S, n, blocks, tri_circle)
            hist[r["unblocked"]] += 1
            if best is None or r["unblocked"] < best["unblocked"]:
                best = r
        if best is None:
            print(f"  k={k}: no safe set sampled", flush=True)
            continue
        rows.append({"q": q, "k": k, **best,
                     "unblocked_histogram": {str(a): b
                                             for a, b in sorted(hist.items())}})
        print(f"  k={k}: best unblocked={best['unblocked']}, "
              f"covered={best['covered']}/{best['outside']}, "
              f"waste={best['waste']}, capacity={best['capacity']}",
              flush=True)
        print(f"        unblocked histogram (first few): "
              f"{dict(sorted(hist.items())[:6])}", flush=True)

    print()
    print("A maximal set needs unblocked = 0.  If even the best sampled")
    print("6-sets are far from 0 while 7-sets reach 0, that supports")
    print("s(13) = 7 > k* = 6.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
