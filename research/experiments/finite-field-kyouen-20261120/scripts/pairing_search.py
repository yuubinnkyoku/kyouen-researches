"""Search for a pairing strategy for the second player at a given q.

Necessary condition (level 1).  If the second player answers p with pi(p) then
for every pair {a, pi(a)} already on the board and every legal move p the set
{a, pi(a), p, pi(p)} must be safe, in particular never concyclic.  So the
perfect matching pi must satisfy: no two of its pairs have a concyclic union.

That is a matching problem: pairs are "compatible" when their union is not
concyclic, and we need a perfect matching whose pairs are pairwise compatible.
This script searches for one with a 2-opt local search over perfect matchings
(swap the partners of two conflicting pairs), which is cheap because a conflict
between two pairs can be tested with a precomputed dictionary of the 4-subsets
that lie on a circle.

A matching found here still has to pass the full strategy test in
pairing_check.c (which also covers positions with three pairs on the board).

Run:  python pairing_search.py --q 7 --restarts 40 --steps 20000
"""

from __future__ import annotations

import argparse
import itertools
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def load_circles(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        n, b = (int(x) for x in fh.readline().split())
        circles = []
        for _ in range(b):
            parts = fh.readline().split()
            k = int(parts[0])
            circles.append(tuple(int(x) for x in parts[1:1 + k]))
    return n, circles


def concyclic_quads(circles) -> set:
    quads = set()
    for c in circles:
        for quad in itertools.combinations(sorted(c), 4):
            quads.add(quad)
    return quads


def conflicts(partner, quads, n) -> int:
    """Number of conflicting pairs of matched pairs."""
    cnt = 0
    seen = set()
    for a in range(n):
        b = partner[a]
        if a > b:
            continue
        seen.add((a, b))
    plist = sorted(seen)
    for i in range(len(plist)):
        a, b = plist[i]
        for j in range(i + 1, len(plist)):
            c, d = plist[j]
            quad = tuple(sorted((a, b, c, d)))
            if quad in quads:
                cnt += 1
    return cnt


def random_matching(n, rng):
    order = list(range(n))
    rng.shuffle(order)
    partner = [0] * n
    for i in range(0, n, 2):
        partner[order[i]] = order[i + 1]
        partner[order[i + 1]] = order[i]
    return partner


def solve(q: int, restarts: int, steps: int, seed: int) -> int | None:
    out = Path(__file__).resolve().parent.parent / "output"
    n, circles = load_circles(out / f"circles_q{q}_fast.txt")
    quads = concyclic_quads(circles)
    rng = random.Random(seed)
    best = None
    for r in range(restarts):
        partner = random_matching(n, rng)
        cur = conflicts(partner, quads, n)
        for _ in range(steps):
            if cur == 0:
                break
            # pick a random pair of points and try re-matching the two pairs
            a = rng.randrange(n)
            b = partner[a]
            c = rng.randrange(n)
            if c == a or c == b:
                continue
            d = partner[c]
            if d == a or d == b:
                continue
            # two ways to re-match {a,b} and {c,d}
            options = [((a, c), (b, d)), ((a, d), (b, c))]
            best_opt = None
            best_delta = 1 << 30
            for (x, y), (u, v) in options:
                old = partner[:]
                partner2 = partner[:]
                partner2[x] = y; partner2[y] = x
                partner2[u] = v; partner2[v] = u
                new = conflicts(partner2, quads, n)
                delta = new - cur
                if delta < best_delta:
                    best_delta = delta
                    best_opt = partner2
                    if delta == 0:
                        break
            if best_opt is not None and best_delta <= 0:
                partner = best_opt
                cur += best_delta
        if best is None or cur < best:
            best = cur
        print(f"  restart {r}: conflicts={cur}", flush=True)
        if cur == 0:
            return partner
    print(f"  best conflicts over {restarts} restarts: {best}")
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--restarts", type=int, default=40)
    ap.add_argument("--steps", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    partner = solve(args.q, args.restarts, args.steps, args.seed)
    if partner is None:
        raise SystemExit("no conflict-free perfect matching found")
    n = len(partner)
    print(f"q={args.q}: conflict-free perfect matching found")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8") as fh:
            fh.write(f"{n}\n")
            for i in range(n):
                fh.write(f"{partner[i]}\n")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
