"""Systematic ablation: which block family drives K?

For each q, decompose the blocks into families by size and measure K with each
family removed.  This isolates the contribution of each family.

Families (by size):
  * size q   : lines
  * size q+1 : genuine circles
  * size q-1 : degenerate circles (q = 1 mod 4)
  * size 2q-1: crosses (q = 1 mod 4)
  * size 2q  : char-2 degenerate circles (q even)

For q=5: sizes {4: 100, 5: 30, 9: 25}
  - size 4 = q-1: degenerate circles
  - size 5 = q: lines
  - size 9 = 2q-1: crosses

For q=7: sizes {7: 56, 8: 294}
  - size 7 = q: lines
  - size 8 = q+1: circles

Let me measure K with each family removed.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def max_safe(pts, blocks, n_fixed: int, node_cap: int = 20_000_000):
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
        print(f"q={q}: {len(blocks)} blocks, sizes {dict(sorted(sizes.items()))}",
              flush=True)
        k_all, n0, s0 = max_safe(pts, blocks, 2)
        print(f"  all blocks: K={k_all} ({s0}, nodes={n0})", flush=True)
        rows.append({"q": q, "family": "all", "K": k_all, "status": s0,
                     "nodes": n0})
        for sz in sorted(sizes):
            kept = [b for b in blocks if len(b) != sz]
            k, n, s = max_safe(pts, kept, 2)
            print(f"  without size-{sz} ({sizes[sz]} blocks): K={k} "
                  f"({s}, nodes={n})", flush=True)
            rows.append({"q": q, "family": f"without_size_{sz}", "K": k,
                         "status": s, "nodes": n})

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
