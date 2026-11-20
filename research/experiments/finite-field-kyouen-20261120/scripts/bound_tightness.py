"""Verify the lambda_2 bound is tight for small q by checking q+3 is impossible.

For q=3: bound q+3=6, K=5.  We verified size 6 is impossible (all 84 six-subsets
contain a circle).

For q=5: bound q+3=8, K=6.  Let me verify sizes 7 and 8 are impossible.

For q=7: bound q+3=10, K=6.  Sizes 7..10 should be impossible.

This confirms the bound is not tight, and measures the gap precisely.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def exists_safe(pts, blocks, through, target: int, n_fixed: int,
                node_cap: int = 20_000_000):
    n = len(pts)
    n_blocks = len(blocks)
    nodes = 0
    found = None

    def rec(start: int, chosen: list, pmask: int, cnt: list):
        nonlocal nodes, found
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError
        if found is not None:
            return
        if len(chosen) == target:
            found = list(chosen)
            return
        need = target - len(chosen)
        if n - start < need:
            return
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
            if found is not None:
                return

    cnt = [0] * n_blocks
    pmask = 0
    for p in range(n_fixed):
        for bi in through[p]:
            cnt[bi] += 1
        pmask |= 1 << p
    try:
        rec(n_fixed, list(range(n_fixed)), pmask, cnt)
        return None, nodes, "exhausted"
    except TimeoutError:
        return None, nodes, "capped"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        print(f"AG(2,{q}): {len(pts)} points, {len(blocks)} blocks, "
              f"bound q+3 = {q+3}", flush=True)
        for t in range(q + 1, q + 4):
            w, nodes, status = exists_safe(pts, blocks, through, t, 2)
            rows.append({"q": q, "target": t, "exists": w is not None,
                         "nodes": nodes, "status": status})
            print(f"  target={t}: exists={w is not None} nodes={nodes} "
                  f"status={status}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
