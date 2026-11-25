"""Compute the maximum "2-arc" size (at most 2 per circle) for comparison.

Our K is the maximum size of a set meeting every circle in at most 3 points
(a "3-arc" in the inversive plane).

The literature's "k-arc" meets every circle in at most 2 points (a "2-arc").

Let us compute the maximum 2-arc size for the inversive plane of order q, to
compare with the literature's (q+5)-arc claim.

If the maximum 2-arc size is much smaller than q+5, then Sonnino's Ad(q) must
be a different structure (as we suspect).

If it is around q+5, then our understanding of the definition is wrong.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_bfs import build_field, circles_bfs, projective_line  # noqa: E402


def max_arc(q: int, limit: int, node_cap: int = 20_000_000):
    """Maximum set meeting every circle in at most `limit` points."""
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
                if cnt[bi] >= limit:
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

    # PGL(2,q^2) is 3-transitive; for limit=2 we can fix 2 points
    cnt = [0] * n_blocks
    pmask = 0
    fixed = [0, 1]
    for p in fixed:
        for bi in through[p]:
            cnt[bi] += 1
        pmask |= 1 << p
    try:
        rec(2, list(fixed), pmask, cnt)
        status = "complete"
    except TimeoutError:
        status = "capped"
    return best[0], nodes, status


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'max 2-arc':>10} {'max 3-arc (K)':>14} {'q+5':>5} {'status':>9}")
    K3 = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 10}
    for q in args.q:
        k2, nodes, status = max_arc(q, 2)
        rows.append({"q": q, "max_2arc": k2, "max_3arc": K3.get(q),
                     "q_plus_5": q + 5, "nodes": nodes, "status": status})
        print(f"{q:>3} {k2:>10} {K3.get(q, '-'):>14} {q+5:>5} {status:>9}")

    print()
    print("if max 2-arc << q+5, then Sonnino's Ad(q) is a different structure.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
