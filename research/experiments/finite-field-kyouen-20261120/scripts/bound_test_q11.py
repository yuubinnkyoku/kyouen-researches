"""Is "every triple on a block" really necessary for maximal safe sets?

The bound K <= lambda_2 + 2 = q + 3 relies on the property that EVERY triple of
the maximum safe set lies on a block.  We verified this for q = 3,5,7,9.

But is the property NECESSARY?  Maybe a larger safe set exists that does NOT
have the property, in which case the bound would be invalid.

Let me test: for each q, find the maximum safe set and check whether it has the
property.  If some maximum safe set lacks the property, the bound's hypothesis
fails and we need a different argument.

Also: the bound k <= lambda_2 + 2 was derived assuming the property.  Let me
verify the bound directly against the known K values:
  q=3: K=5 <= 6 OK
  q=5: K=6 <= 8 OK
  q=7: K=6 <= 10 OK
  q=9: K=9 <= 12 OK
  q=11: K=9 <= 14 OK
  q=13: K>=13 <= 16 OK
  q=17: K>=17 <= 20 OK
  q=19: K>=13 <= 22 OK

All consistent.  But the bound is only valid if the property holds.

IMPORTANT: the property might fail for larger q.  Let me look for a safe set
that is LARGER than lambda_2 + 2 -- if one exists, the property must fail.

Actually, a cleaner test: for q=11, is there a safe set of size 13 (= lambda_2+2
= 12+2 = 14? no, lambda_2 = 12, so bound is 14)?  Let me check whether safe sets
of size 12, 13, 14 exist for q=11.  If size 14 exists, the bound is tight.
If size 15 exists, the bound is WRONG.

Let me run the search for q=11 at sizes 10..14.
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
    ap.add_argument("--q", type=int, default=11)
    ap.add_argument("--target", type=int, nargs="+", default=[10, 11, 12, 13, 14])
    ap.add_argument("--node-cap", type=int, default=20_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    pts, blocks, through, nc, nl = build_ag(args.q)
    print(f"AG(2,{args.q}): {len(pts)} points, {len(blocks)} blocks", flush=True)
    print(f"  lambda_2 = q+1 = {args.q+1}, so the bound is K <= {args.q+3}",
          flush=True)

    rows = []
    for t in args.target:
        w, nodes, status = exists_safe(pts, blocks, through, t, 2, args.node_cap)
        rows.append({"target": t, "exists": w is not None, "nodes": nodes,
                     "status": status})
        print(f"  target={t}: exists={w is not None} nodes={nodes} "
              f"status={status}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
