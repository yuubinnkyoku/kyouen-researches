"""Decide AG(2,13) size 14 with a much stronger propagation.

Key insight from the lambda_2 bound: for any pair {p,q} in S, the k-2 other
points must occupy distinct blocks through p,q.  With lambda_2 = q+1 = 14 and
k = 14, we need 12 of the 14 blocks through each pair to be used.

This is extremely tight!  Let me exploit it.

For k=14, each pair {p,q} in S needs 12 distinct blocks through it, each
containing a third point of S.  The pencil has 14 blocks, so only 2 are unused.

Let me use this as a strong prune: for each pair in S, count the blocks through
it that already contain a third point of S.  If (number of remaining points to
add) > (number of blocks through the pair that can still accept a third point),
prune.

That is the "pair budget" prune I already have.  Let me strengthen it further:
also require that the blocks through p,q that are NOT yet used can actually
receive a point of S.  A block B through p,q can receive a third point r only
if r is not blocked by other constraints.

Let me add a "look-ahead" prune: for each candidate point r, check whether
adding it would leave every pair in S∪{r} with enough budget.

Actually, let me try a different approach: use the CROSS constraint more
aggressively.  For q=13 (1 mod 4), there are 169 crosses of size 25.  The cross
constraint a_c + b_r - x_cr <= 3 is very strong.

For k=14: sum over c of a_c = 14, and each a_c <= 2 (proved).  So at least
7 columns have 2 points (if all have <= 2 and sum is 14, with 13 columns,
we need at least 1 column with 2... wait, 13 columns, sum 14, each <= 2:
at most 2 columns can have 2 (since 2*2 + 11*1 = 15 >= 14, so we need
at least 1 column with 2).  Actually: if x columns have 2 and 13-x have 1,
then 2x + (13-x) = 13+x = 14, so x = 1.  So exactly 1 column has 2 points,
12 columns have 1 point, and 0 columns have 0 points.

Wait, that assumes all columns have >= 1.  Let me redo: let x2 = #columns with 2,
x1 = #columns with 1, x0 = #columns with 0.  x2+x1+x0 = 13, 2x2+x1 = 14.
So x1 = 14-2x2, x0 = 13-x2-x1 = 13-x2-14+2x2 = x2-1.
For x0 >= 0: x2 >= 1.  For x1 >= 0: x2 <= 7.
So x2 in [1,7], x1 = 14-2x2, x0 = x2-1.

Similarly for rows.

Now the cross constraint: for c in C2 (a_c=2) and r in R2 (b_r=2), x_cr = 1.
We proved |C2| <= 2 and |R2| <= 2.

With k=14 and 13 columns: x2 = |C2| in [1,7], but |C2| <= 2.  So x2 in {1,2}.
  - x2=1: x1=12, x0=0.  One column has 2, twelve have 1, none has 0.
  - x2=2: x1=10, x0=1.  Two columns have 2, ten have 1, one has 0.

Similarly for rows.

Case x2=1 for columns: exactly one column has 2 points, all others 1.
Then |C2|=1.  For rows, |R2| in {1,2}.
  If |R2|=1: the single column c* with 2 points and the single row r* with 2
  points must have x_{c*r*} = 1 (cross constraint).
  If |R2|=2: c* must intersect both rows in S.

This is a very tight structure!  Let me use it as a strong prune.

Let me implement: track column counts and row counts, and enforce:
  - each column/row has <= 2 points,
  - at most 2 columns and 2 rows have 2 points,
  - if a_c = 2 and b_r = 2 then x_cr = 1.

This should prune massively.
"""

from __future__ import annotations

import argparse
import json
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402
from inversive_prime_power import FiniteField, find_irreducible  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=13)
    ap.add_argument("--target", type=int, nargs="+", default=[14])
    ap.add_argument("--node-cap", type=int, default=100_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    q = args.q
    pts, blocks, through, nc, nl = build_ag(q)
    n = len(pts)
    n_blocks = len(blocks)
    bpts = [tuple(b) for b in blocks]
    print(f"AG(2,{q}): {n} points, {n_blocks} blocks", flush=True)

    # Identify the split coordinates (s,t) for q = 1 mod 4.
    # We need to map each point (x,y) to (s,t) = (x+iy, x-iy).
    F = FiniteField(q, 1, find_irreducible(q, 1))
    # find i with i^2 = -1
    i_val = None
    for cand in range(q):
        if (cand * cand + 1) % q == 0:
            i_val = cand
            break
    if i_val is None:
        raise SystemExit("q is not 1 mod 4")
    print(f"  i = {i_val} (i^2 = -1)", flush=True)

    # map point index -> (s, t)
    st = {}
    for idx, p in enumerate(pts):
        x = p[0][0]
        y = p[1][0]
        s = (x + i_val * y) % q
        t = (x - i_val * y) % q
        st[idx] = (s, t)

    # column/row of each point
    col = {idx: st[idx][0] for idx in range(n)}
    row = {idx: st[idx][1] for idx in range(n)}

    pair_blocks: dict[tuple[int, int], list[int]] = {}
    for bi, b in enumerate(blocks):
        for i in range(len(b)):
            for j in range(i + 1, len(b)):
                pair_blocks.setdefault((b[i], b[j]), []).append(bi)

    rows_out = []
    for target in args.target:
        nodes = 0
        found = None
        fixed = [0, 1]

        def rec(start: int, chosen: list, pmask: int, cnt: list,
                colcnt: list, rowcnt: list):
            nonlocal nodes, found
            nodes += 1
            if nodes > args.node_cap:
                raise TimeoutError(f"node cap {args.node_cap} exceeded")
            if found is not None:
                return
            s = len(chosen)
            if s == target:
                found = list(chosen)
                return
            need = target - s
            if n - start < need:
                return
            # column/row constraints
            n2col = sum(1 for c in colcnt if c == 2)
            n2row = sum(1 for r in rowcnt if r == 2)
            if n2col > 2 or n2row > 2:
                return
            # pair budget
            for a in range(len(chosen)):
                for b in range(a + 1, len(chosen)):
                    bl = pair_blocks.get((chosen[a], chosen[b]), [])
                    free = sum(1 for bi in bl if cnt[bi] < 3)
                    if free < need:
                        return
            # block budget
            need_triples = comb(target, 3) - comb(s, 3)
            available = 0
            for bi in range(n_blocks):
                c = cnt[bi]
                if c >= 3:
                    continue
                free = 0
                for j in bpts[bi]:
                    if not (pmask >> j & 1):
                        free += 1
                if c + free >= 3:
                    available += 1
            if need_triples > available:
                return
            cands = []
            for p in range(start, n):
                if pmask >> p & 1:
                    continue
                if colcnt[col[p]] >= 2 or rowcnt[row[p]] >= 2:
                    continue
                ok = True
                cost = 0
                for bi in through[p]:
                    if cnt[bi] >= 3:
                        ok = False
                        break
                    if cnt[bi] == 2:
                        cost += 1
                if ok:
                    cands.append((cost, p))
            cands.sort()
            for cost, p in cands:
                for bi in through[p]:
                    cnt[bi] += 1
                colcnt[col[p]] += 1
                rowcnt[row[p]] += 1
                chosen.append(p)
                rec(p + 1, chosen, pmask | (1 << p), cnt, colcnt, rowcnt)
                chosen.pop()
                colcnt[col[p]] -= 1
                rowcnt[row[p]] -= 1
                for bi in through[p]:
                    cnt[bi] -= 1
                if found is not None:
                    return

        cnt = [0] * n_blocks
        colcnt = [0] * q
        rowcnt = [0] * q
        pmask = 0
        for p in fixed:
            for bi in through[p]:
                cnt[bi] += 1
            colcnt[col[p]] += 1
            rowcnt[row[p]] += 1
            pmask |= 1 << p
        try:
            rec(2, list(fixed), pmask, cnt, colcnt, rowcnt)
        except TimeoutError as e:
            print(f"  target={target}: TIMEOUT ({e}) nodes={nodes}", flush=True)
            rows_out.append({"target": target, "status": "timeout", "nodes": nodes})
            continue

        if found is None:
            print(f"  target={target}: NO (exhausted, nodes={nodes})", flush=True)
            rows_out.append({"target": target, "exists": False, "nodes": nodes})
        else:
            print(f"  target={target}: FOUND (nodes={nodes})", flush=True)
            rows_out.append({"target": target, "exists": True, "nodes": nodes,
                             "witness": found})

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows_out, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
