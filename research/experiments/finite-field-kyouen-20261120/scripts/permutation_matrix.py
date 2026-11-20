"""Why would K = q for q = 1 mod 4?

The cross bound gives K <= q+2.  The conjecture says K = q exactly.

Let me look for a structural reason.

For q = 1 mod 4, the split coordinates (s,t) give q^2 cross blocks, each of size
2q-1.  A safe set S meets each cross in at most 3 points.

The cross constraint: a_c + b_r - x_cr <= 3 where a_c = |S cap col c|,
b_r = |S cap row r|, x_cr = 1 if (c,r) in S.

We proved: at most 2 columns and 2 rows have 2 points; all others have <= 1.
So k <= 2*2 + (q-2)*1 = q+2.

For k = q+2, we need exactly 2 columns and 2 rows with 2 points, and the
remaining q-2 columns with 1 point each.  Total = 4 + (q-2) = q+2.

For k = q+1: either 2 columns with 2 points and q-3 with 1 (4+q-3 = q+1),
or 1 column with 2 and q-1 with 1 (2+q-1 = q+1).

For k = q: either 2 columns with 2 and q-4 with 1 (4+q-4 = q), or 1 column with
2 and q-2 with 1 (2+q-2 = q), or 0 columns with 2 and q with 1 (q).

So k = q is achievable by the cross constraint alone (e.g., one point in each
column and each row, i.e., a permutation matrix).

Now, is a permutation matrix safe?  A permutation matrix has one point in each
column and each row.  Does it contain 4 points on a circle?

For q=5: a permutation matrix has 5 points.  Is it safe?  K=5, so some
permutation matrix should be safe.

For q=9: K=9, so some permutation matrix should be safe.

For q=13: if K=13, some permutation matrix should be safe.

CONJECTURE REFINEMENT: for q = 1 mod 4, there is a safe set of size q which is
a "permutation matrix" (one point per column and row).

And no safe set of size q+1 exists.

Let me test: for q=5, 9, is there a safe permutation matrix?  And for q=13?

This is a much smaller search: q! permutation matrices (for q=5: 120, q=9:
362880, q=13: too many).  But we can search with pruning.

Actually, let me just check whether the maximum safe set found earlier is a
permutation matrix.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def find_max_safe(q: int, node_cap: int = 5_000_000):
    pts, blocks, through, nc, nl = build_ag(q)
    n = len(pts)
    n_blocks = len(blocks)
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
    for p in range(2):
        for bi in through[p]:
            cnt[bi] += 1
        pmask |= 1 << p
    try:
        rec(2, [0, 1], pmask, cnt)
        status = "complete"
    except TimeoutError:
        status = "capped"
    return best[0], best[1], nodes, status, pts, blocks


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[5, 9])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        k, S, nodes, status, pts, blocks = find_max_safe(q)
        if S is None:
            continue
        # check if S is a permutation matrix in split coordinates
        # we need the split coordinates; for q = 1 mod 4 they exist
        # but build_ag uses (x,y) coordinates.  Let me just report the size.
        rows.append({"q": q, "K": k, "nodes": nodes, "status": status})
        print(f"q={q}: K={k} ({status}, nodes={nodes})", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
