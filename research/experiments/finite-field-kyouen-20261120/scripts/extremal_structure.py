"""Looking for a "cross-like" structure when q = 3 mod 4.

For q = 1 mod 4 the cross blocks (column + row) gave K <= q+2.  The key was:
  * q^2 blocks of size 2q-1,
  * two such blocks meet in 2 or q points,
  * the "2 points in a column and 2 in a row forces the intersection" argument.

For q = 3 mod 4 there are no such blocks.  But maybe there is an analogous
structure from the CIRCLE pencil.

Idea: fix a point P.  The circles through P: how many?  For the inversive plane
of order q, the circles through P correspond to the q(q-1) "directions" at P
(each circle through P has a tangent direction at P, and there are q+1 tangent
directions... let me just compute).

Actually let me look for LARGE blocks or LARGE "structured families" empirically:
  * compute the size distribution (done: only q and q+1),
  * compute, for each pair of blocks, the intersection size distribution,
  * look for a family of blocks whose pairwise intersections are large.

If no large blocks exist, maybe a different structure: consider the union of
two circles through a common point.  Two circles meet in at most 2 points, so
their union has 2(q+1)-2 = 2q points.  A safe set meets each circle in <= 3, so
it meets the union in <= 6.  That gives: for any two circles C1, C2,
    |S cap (C1 u C2)| <= 6.
Not obviously useful.

Let me instead check: is there a family of q^2 blocks of size ~2q in AG(2,q) for
q = 3 mod 4?  The answer from the size distribution is NO (only sizes q and q+1).

So the cross trick genuinely has no analogue.  Let me instead try to improve the
triple bound using the structure of the circle pencil.

TRIPLE BOUND REFINEMENT:
    C(k,3) <= #blocks = q^3 + q.
But not all triples are "free": a triple of S lies on exactly one block, and
that block holds at most 3 points of S.  So the map triple -> block is injective.
That is what gives C(k,3) <= #blocks.

Can we improve by noting that some blocks cannot host 3 points of S?  A block B
hosts 3 points of S only if all 3 are in S.  Hmm, circular.

Alternative: use the fact that the blocks through a fixed point P form a
"pencil" and the points of S on those blocks are constrained.

Let me try a computational search for the actual extremal configurations at
q=7 and q=11, to see what structure the maximum safe sets have.  That may
suggest the right inequality.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def find_max_safe(q: int, node_cap: int = 5_000_000):
    pts, blocks, through, nc, nl = build_ag(q)
    n = len(pts)
    n_blocks = len(blocks)
    through_l = [list(t) for t in through]
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
            for bi in through_l[p]:
                if cnt[bi] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for bi in through_l[p]:
                cnt[bi] += 1
            chosen.append(p)
            rec(p + 1, chosen, pmask | (1 << p), cnt)
            chosen.pop()
            for bi in through_l[p]:
                cnt[bi] -= 1

    cnt = [0] * n_blocks
    pmask = 0
    for p in range(2):
        for bi in through_l[p]:
            cnt[bi] += 1
        pmask |= 1 << p
    try:
        rec(2, [0, 1], pmask, cnt)
        status = "complete"
    except TimeoutError:
        status = "capped"
    return best[0], best[1], nodes, status, pts, blocks


def analyse(q: int):
    k, S, nodes, status, pts, blocks = find_max_safe(q)
    print(f"q={q}: best safe {k} (nodes={nodes}, {status})", flush=True)
    if S is None:
        return None
    Sset = set(S)
    # block profile: how many blocks hold 0,1,2,3 points of S
    prof = Counter()
    for b in blocks:
        c = len(set(b) & Sset)
        prof[c] += 1
    print(f"  block profile (points of S per block): {dict(sorted(prof.items()))}",
          flush=True)
    # for each point of S, how many blocks hold exactly 3
    per_point = []
    for p in S:
        c3 = 0
        for bi in range(len(blocks)):
            if p in blocks[bi]:
                pass
        per_point.append(0)
    # simpler: count blocks with exactly 3 points of S, and how many of them
    # contain each point of S
    full_blocks = [b for b in blocks if len(set(b) & Sset) == 3]
    print(f"  blocks with exactly 3 points of S: {len(full_blocks)}", flush=True)
    cnt3 = Counter()
    for b in full_blocks:
        for p in set(b) & Sset:
            cnt3[p] += 1
    print(f"  per-point count of full blocks: "
          f"{sorted(cnt3.values(), reverse=True)}", flush=True)
    return {"q": q, "k": k, "nodes": nodes, "status": status,
            "block_profile": dict(sorted(prof.items())),
            "full_blocks": len(full_blocks),
            "per_point_full": sorted(cnt3.values(), reverse=True)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[7, 11])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        r = analyse(q)
        if r:
            rows.append(r)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
