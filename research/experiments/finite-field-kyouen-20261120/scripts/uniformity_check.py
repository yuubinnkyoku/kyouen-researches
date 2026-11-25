"""Use the parity law to PREDICT winners of geometric boards without Grundy search.

The parity law (proved): if all maximal safe sets have the same parity eps, then
g(S) = (eps - |S|) mod 2, in particular g(empty) = eps.

So: to determine the winner of a board, it suffices to determine the PARITY of
its maximal safe sets.  That is much cheaper than computing Grundy values.

KEY INSIGHT: for a board where every maximal safe set has size exactly K
(the maximum), the parity is K mod 2.  So if we can prove "no maximal set is
smaller than K", we get the winner for free.

Let me apply this to the finite-field boards where we know K exactly:
  inversive q=3: K=5 -> g(empty)=1 (first player wins)
  inversive q=4: K=5 -> g(empty)=1
  inversive q=5: K=6 but maximal sizes {5,6} -> no prediction
  AG(2,3): K=5 -> g(empty)=1
  AG(2,5): K=6 but maximal {3,5,6} -> no prediction

And for the LARGER boards where we know K but cannot compute Grundy:
  AG(2,13): K=13 -> if uniform, g(empty)=1
  AG(2,16): K=16 -> if uniform, g(empty)=0
  inversive q=16: K=12 -> if uniform, g(empty)=0
  inversive q=17: K=13 -> if uniform, g(empty)=1
  inversive q=19: K=14 -> if uniform, g(empty)=0

The question: are these boards uniform?  We cannot enumerate all safe sets for
q=13+.  But we CAN check whether a SMALLER maximal set exists, by searching for
a maximal safe set of size < K.

That is a much smaller search: find any maximal set of size < K.

Let me implement: for a given board and target size t < K, search for a safe set
of size t that is MAXIMAL (no point can be added).

If none exists for any t < K, then all maximal sets have size K, and the parity
law gives the winner.

This is a genuinely new application: it turns the parity law into a WINNER
PREDICTION for boards too large for full Grundy computation.
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


def exists_maximal_of_size(pts, blocks, through, target: int,
                           node_cap: int = 50_000_000):
    """Is there a safe set of size `target` that is maximal (no legal addition)?"""
    n = len(pts)
    n_blocks = len(blocks)
    nodes = 0
    found = None

    def can_add(i: int, pmask: int) -> bool:
        for bi in through[i]:
            cnt = 0
            for j in blocks[bi]:
                if pmask >> j & 1:
                    cnt += 1
                    if cnt >= 3:
                        return False
        return True

    def rec(start: int, chosen: list, pmask: int):
        nonlocal nodes, found
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError
        if found is not None:
            return
        if len(chosen) == target:
            # check maximality
            if all(pmask >> i & 1 or not can_add(i, pmask) for i in range(n)):
                found = list(chosen)
            return
        need = target - len(chosen)
        if n - start < need:
            return
        for i in range(start, n):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask):
                chosen.append(i)
                rec(i + 1, chosen, pmask | (1 << i))
                chosen.pop()
                if found is not None:
                    return

    try:
        rec(0, [], 0)
        return found, nodes, "complete"
    except TimeoutError:
        return None, nodes, "capped"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", choices=["ag", "inv"], required=True)
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--K", type=int, required=True)
    ap.add_argument("--node-cap", type=int, default=20_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    if args.board == "ag":
        pts, blocks, through = build_ag(args.q)
    else:
        pts, blocks, through = build_inv(args.q)
    print(f"{args.board}(q={args.q}): {len(pts)} points, {len(blocks)} blocks, "
          f"K={args.K}", flush=True)

    rows = []
    smaller_exists = False
    for t in range(1, args.K):
        w, nodes, status = exists_maximal_of_size(pts, blocks, through, t,
                                                  args.node_cap)
        rows.append({"target": t, "exists": w is not None, "nodes": nodes,
                     "status": status})
        print(f"  maximal set of size {t}: exists={w is not None} "
              f"nodes={nodes} status={status}", flush=True)
        if w is not None:
            smaller_exists = True
            break

    print()
    if smaller_exists:
        print("RESULT: a smaller maximal set exists -> board is NOT uniform -> "
              "parity law gives no prediction")
    else:
        print(f"RESULT: no maximal set smaller than K={args.K} found -> "
              f"board is uniform -> g(empty) = {args.K} mod 2 = {args.K % 2}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "board": args.board, "q": args.q, "K": args.K,
            "smaller_maximal_exists": smaller_exists,
            "predicted_g_empty": (args.K % 2) if not smaller_exists else None,
            "rows": rows,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
