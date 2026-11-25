"""Is "every triple on a block" a general property of extremal safe sets?

For q=7 the maximum safe set of size 6 has the property that ALL C(6,3)=20
triples lie on a common block (circle or line).  This is a very strong
structure.  Let us test it for other boards:

  * AG(2,q) for q = 3, 5, 7, 9, 11
  * the inversive plane for q = 3, 4, 5

For each board, find a maximum safe set and check whether all its triples lie
on a block.  Also report the "triple coverage" = (# triples on a block) / C(k,3).

If the property holds generally, it suggests a new route to upper bounds:
bound the size of a set all of whose triples lie on blocks.

Note: for a 3-(v,s,1) design (the inversive plane), EVERY triple lies on exactly
one block by definition!  So the property is automatic there.  The interesting
case is AG(2,q), where a triple can be non-collinear and non-concyclic.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def find_max_safe(pts, blocks, through, node_cap: int = 3_000_000):
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
    return best[0], best[1], nodes, status


def triple_coverage(S, blocks):
    """Fraction of triples of S that lie on some block."""
    Sset = set(S)
    # precompute block sets restricted to S
    bsets = [frozenset(b) & Sset for b in blocks]
    bsets = [b for b in bsets if len(b) >= 3]
    total = 0
    covered = 0
    for tri in itertools.combinations(S, 3):
        total += 1
        t = frozenset(tri)
        if any(t <= b for b in bsets):
            covered += 1
    return covered, total


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7, 9, 11])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        k, S, nodes, status = find_max_safe(pts, blocks, through)
        if S is None:
            continue
        cov, tot = triple_coverage(S, blocks)
        rows.append({"q": q, "k": k, "nodes": nodes, "status": status,
                     "triples": tot, "covered": cov,
                     "all_covered": cov == tot})
        print(f"q={q}: max safe {k} ({status}, nodes={nodes}), "
              f"triples on a block: {cov}/{tot} "
              f"({'ALL' if cov == tot else 'partial'})", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
