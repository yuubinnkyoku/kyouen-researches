"""Quantify: does block size alone predict the constraint strength?

For a board with ONLY blocks of one size s, the maximum safe set size should
depend on s.  Let me measure K for single-family boards.

For AG(2,q), the families are:
  * lines (size q)
  * circles (size q+1 or q-1 or 2q-1 or 2q depending on q mod 4)

Let me compute K for each single family, and see how it depends on the size.

Prediction: larger blocks -> smaller K (stronger constraint).

But careful: the NUMBER of blocks also matters.  A family with few large blocks
may constrain less than a family with many small blocks.

Let me measure both and look for the right invariant.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def max_safe(pts, blocks, n_fixed: int, node_cap: int = 10_000_000):
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
    for p in range(n_fixed):
        for bi in through[p]:
            cnt[bi] += 1
        pmask |= 1 << p
    try:
        rec(n_fixed, list(range(n_fixed)), pmask, cnt)
        return best[0], nodes, "complete"
    except TimeoutError:
        return best[0], nodes, "capped"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        sizes = Counter(len(b) for b in blocks)
        print(f"q={q}: sizes {dict(sorted(sizes.items()))}", flush=True)
        for sz in sorted(sizes):
            fam = [b for b in blocks if len(b) == sz]
            k, nodes, status = max_safe(pts, fam, 2)
            rows.append({"q": q, "size": sz, "count": len(fam), "K": k,
                         "status": status, "nodes": nodes})
            print(f"  size {sz} only ({len(fam)} blocks): K={k} "
                  f"({status}, nodes={nodes})", flush=True)

    print()
    print("summary: K vs block size and count")
    for r in rows:
        print(f"  q={r['q']}, size={r['size']}, count={r['count']}, K={r['K']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
