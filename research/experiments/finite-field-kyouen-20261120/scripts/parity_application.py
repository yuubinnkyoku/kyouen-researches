"""Apply the parity law to real kyouen boards: predict Grundy values without search.

The parity law (proved): if all maximal safe sets have the same parity, then
g(S) = (eps - |S|) mod 2 for all S, and max g <= 1.

This gives a PREDICTION for any board where we can determine the parity of
maximal sets WITHOUT computing Grundy values.  Determining the parity is much
cheaper than computing Grundy values: we only need to know whether all maximal
sets have the same parity.

KEY APPLICATION: for a board where every maximal set has size exactly K (the
maximum), the parity is K mod 2, and we get g(S) = (K - |S|) mod 2 for free.

So: if we can prove "every maximal safe set has size K" (i.e., no smaller
maximal sets exist), then the whole Grundy table is determined by K and |S|.

Let me check which boards have this property, and use it to predict.

For the inversive plane q=3: maximal sizes {5}, K=5, so g(S) = (5-|S|) mod 2.
Verified: gdist {0:202, 1:226}, and 202 = number of odd-size positions,
226 = number of even-size positions.  Let me check.

For q=4: maximal {5}, K=5.
For q=5: maximal {5,6}, mixed -> no prediction.

Let me also check: for the AG(2,q) boards, what are the maximal sizes?

And importantly: can I PREDICT the root Grundy value (who wins) from K alone?
g(empty) = K mod 2.  So the empty board is a P-position iff K is even.

Check:
  inversive q=3: K=5 odd -> g(empty)=1 (N, first player wins).  Actual: 1. OK.
  inversive q=4: K=5 odd -> g(empty)=1.  Actual: 1. OK.
  AG(2,3): K=5 odd -> g(empty)=1.  Actual: 1. OK.
  3x3 integer: K=5 odd -> g(empty)=1.  Actual: 1. OK.

So for uniform boards, the winner is determined by K's parity!

This is a nice practical corollary: to determine the winner of a uniform board,
we only need K mod 2, not the full Grundy table.

Let me verify this on all boards and document it.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def build_ag(q: int):
    from ag2_prime_power import build_ag as _b
    pts, blocks, through, nc, nl = _b(q)
    return pts, blocks, through


def build_inv(q: int):
    from inversive_bfs import build_field, circles_bfs, projective_line
    F, sub = build_field(q)
    pts = projective_line(F)
    circles = circles_bfs(F, sub, pts)
    idx = {p: i for i, p in enumerate(pts)}
    blocks = [sorted(idx[p] for p in c) for c in circles]
    n = len(pts)
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)
    return pts, blocks, through


def analyse(pts, blocks, through):
    n = len(pts)
    n_blocks = len(blocks)

    def can_add(i: int, pmask: int) -> bool:
        for bi in through[i]:
            cnt = 0
            for j in blocks[bi]:
                if pmask >> j & 1:
                    cnt += 1
                    if cnt >= 3:
                        return False
        return True

    by_size: dict[int, list[int]] = defaultdict(list)
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        by_size[pmask.bit_count()].append(pmask)
        for i in range(start, n):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask):
                stack.append((i + 1, pmask | (1 << i)))

    g: dict[int, int] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            reach = set()
            for i in range(n):
                if pmask >> i & 1:
                    continue
                if can_add(i, pmask):
                    reach.add(g[pmask | (1 << i)])
            m = 0
            while m in reach:
                m += 1
            g[pmask] = m

    maximal_sizes = Counter()
    for size in by_size:
        for pmask in by_size[size]:
            if all(pmask >> i & 1 or not can_add(i, pmask) for i in range(n)):
                maximal_sizes[size] += 1

    sizes = sorted(maximal_sizes)
    same_parity = len({s % 2 for s in sizes}) == 1
    eps = sizes[0] % 2 if same_parity else None

    # prediction from parity law
    predicted_ok = True
    if same_parity:
        for pmask, val in g.items():
            if val != (eps - pmask.bit_count()) % 2:
                predicted_ok = False
                break

    # root prediction
    root_pred = eps if same_parity else None
    root_actual = g[0]

    return {
        "points": n,
        "safe_sets": sum(len(v) for v in by_size.values()),
        "maximal_sizes": dict(sorted(maximal_sizes.items())),
        "same_parity": same_parity,
        "eps": eps,
        "K": max(sizes),
        "max_grundy": max(g.values()),
        "prediction_ok": predicted_ok,
        "root_predicted": root_pred,
        "root_actual": root_actual,
        "root_prediction_ok": (root_pred == root_actual) if same_parity else None,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in (3, 4, 5):
        pts, blocks, through = build_inv(q)
        r = analyse(pts, blocks, through)
        r["board"] = f"inversive q={q}"
        rows.append(r)
    for q in (3, 5):
        pts, blocks, through = build_ag(q)
        r = analyse(pts, blocks, through)
        r["board"] = f"AG(2,{q})"
        rows.append(r)
    from ff_kyouen import int_forbidden_quads, int_grid
    for n in (3, 4, 5):
        pts = int_grid(n)
        quads = int_forbidden_quads(n, pts)
        through = [[] for _ in range(n * n)]
        blocks = [list(qd) for qd in quads]
        for bi, b in enumerate(blocks):
            for i in b:
                through[i].append(bi)
        r = analyse(pts, blocks, through)
        r["board"] = f"{n}x{n} integer"
        rows.append(r)

    print(f"{'board':>18} {'maximal':>18} {'K':>3} {'eps':>4} {'maxg':>5} "
          f"{'pred ok':>8} {'root pred/act':>14}")
    for r in rows:
        print(f"{r['board']:>18} {str(r['maximal_sizes']):>18} {r['K']:>3} "
              f"{str(r['eps']):>4} {r['max_grundy']:>5} "
              f"{str(r['prediction_ok']):>8} "
              f"{str(r['root_predicted'])}/{r['root_actual']}")

    print()
    print("COROLLARY: for a uniform board (all maximal sets size K),")
    print("  g(S) = (K - |S|) mod 2, so the empty board is a P-position iff K is even.")
    print()
    uniform = [r for r in rows if r["same_parity"]]
    print(f"boards with same-parity maximal sets: {len(uniform)}/{len(rows)}")
    print(f"  all predictions correct: "
          f"{all(r['prediction_ok'] for r in uniform)}")
    print(f"  all root predictions correct: "
          f"{all(r['root_prediction_ok'] for r in uniform)}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
