"""Re-verify the parity law predictions with the CORRECTED K values.

The parity law (proved): if all maximal safe sets have the same parity eps,
then g(empty) = eps, i.e. the winner is determined by the parity of maximal sets.

For uniform boards (all maximal sets have size K), g(empty) = K mod 2.

The corrected K values are:
  inversive: q=3:5, 4:5, 5:6, 7:6, 8:7, 9:9, 11:9, 13:8, 17:9, 19:9
  AG:        q=3:5, 4:5, 5:6, 7:6, 8:8, 9:9, 11:9, 13:13, 16:16

Let me check: for each board, is it uniform?  And does g(empty) = K mod 2?

For the small boards I can enumerate.  For the larger ones I use the
uniformity_check approach (search for a maximal set smaller than K).

Let me run the uniformity check on the corrected boards.
"""

from __future__ import annotations

import argparse
import json
import sys
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

    by_size: dict[int, list[int]] = {}
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        by_size.setdefault(pmask.bit_count(), []).append(pmask)
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
    K = max(sizes)

    return {
        "points": n,
        "safe_sets": sum(len(v) for v in by_size.values()),
        "maximal_sizes": dict(sorted(maximal_sizes.items())),
        "K": K,
        "same_parity": same_parity,
        "eps": eps,
        "g_empty": g[0],
        "max_grundy": max(g.values()),
        "predicted": eps if same_parity else None,
        "prediction_ok": (eps == g[0]) if same_parity else None,
    }


from collections import Counter


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    # small boards only (full enumeration feasible)
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

    print(f"{'board':>18} {'maximal':>20} {'K':>3} {'eps':>4} {'g0':>3} "
          f"{'pred':>5} {'ok':>5}")
    for r in rows:
        print(f"{r['board']:>18} {str(r['maximal_sizes']):>20} {r['K']:>3} "
              f"{str(r['eps']):>4} {r['g_empty']:>3} "
              f"{str(r['predicted']):>5} {str(r['prediction_ok']):>5}")

    print()
    uniform = [r for r in rows if r["same_parity"]]
    print(f"same-parity boards: {len(uniform)}/{len(rows)}")
    print(f"  all predictions correct: "
          f"{all(r['prediction_ok'] for r in uniform)}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
