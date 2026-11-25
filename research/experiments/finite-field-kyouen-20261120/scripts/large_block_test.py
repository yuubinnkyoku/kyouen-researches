"""Test the large-block hypothesis directly: remove large blocks and see if K drops.

Hypothesis: large blocks (size > q+1) RAISE K/q because they provide structure
(column+row, or degenerate line pairs) that allows permutation-matrix-like
configurations.

Test: for q=5 and q=9 (which have crosses of size 2q-1), compute the maximum
safe size with the crosses REMOVED.  If K drops significantly, the crosses are
helping (raising K).  If K stays the same or rises, the crosses are not the
reason.

Also for q=4, 8 (char 2, large blocks of size 2q): remove them and compare.
"""

from __future__ import annotations

import argparse
import json
import sys
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
    ap.add_argument("--q", type=int, nargs="+", default=[4, 5, 8, 9])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        big = [b for b in blocks if len(b) > q + 1]
        small = [b for b in blocks if len(b) <= q + 1]
        print(f"q={q}: {len(blocks)} blocks, {len(big)} large (> q+1={q+1}), "
              f"{len(small)} small", flush=True)
        k_all, n1, s1 = max_safe(pts, blocks, 2)
        k_small, n2, s2 = max_safe(pts, small, 2)
        rows.append({"q": q, "K_all": k_all, "K_small_only": k_small,
                     "large_blocks": len(big), "status_all": s1,
                     "status_small": s2})
        print(f"   with all blocks: K={k_all} ({s1}, nodes={n1})", flush=True)
        print(f"   without large blocks: K={k_small} ({s2}, nodes={n2})", flush=True)
        print(f"   difference: {k_all - k_small}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
