"""Can "every triple on a block" give an upper bound?

Setup.  S is a safe set with |S| = k, and every triple of S lies on a block
(circle or line).  Each block holds at most 3 points of S, so the map
    triple of S -> block containing it
is injective.  Hence C(k,3) <= b, the triple bound.  Not saturated.

But we can use MORE structure.  For each point p in S, consider the blocks
through p that contain 2 other points of S.  These are the "full blocks at p".
Let f(p) = number of such blocks.  Then
    sum over p in S of f(p) = 3 * (#full blocks) = 3 * C(k,3)
because each full block has 3 points and each triple is on exactly one block.

So f(p) = 3*C(k,3)/k = (k-1)(k-2)/2 for every p (if the configuration is
"uniform", which we observed).

Now, the blocks through p: how many are there?  For AG(2,q), p lies on
q^2+q blocks.  Among them, f(p) = (k-1)(k-2)/2 are full.

But here is the constraint: the full blocks at p are determined by PAIRS of
other points of S.  Two distinct pairs {a,b} and {c,d} of S\\{p} give the same
block through p only if {a,b} and {c,d} are on a common block with p, i.e. the
four points a,b,c,d plus p lie on a block -- impossible since a block holds at
most 3 points of S.  So distinct pairs give distinct blocks!

Therefore f(p) = C(k-1,2) exactly, and all these blocks are distinct.

Now, the blocks through p that contain 2 points of S: each such block is
determined by the pair.  So the number of blocks through p containing at least
2 points of S is C(k-1,2) (each pair gives one block, and they are distinct).

But a block through p containing 2 points of S is a block containing 3 points
of S (p plus the pair).  So the count is consistent.

Hmm, this gives no new bound.  Let me think differently.

KEY: consider a point p in S and the q^2+q blocks through p.  Each block
through p contains at most 2 other points of S.  The pairs of S\\{p} are
C(k-1,2) in number, and each pair determines exactly one block through p.
So the blocks through p that contain >= 2 points of S number exactly C(k-1,2).

Now, the blocks through p that contain exactly 1 other point of S: these are
blocks containing p and one other point q, but no third point of S.  For each
q in S\\{p}, the blocks through p and q form a pencil of size lambda_2 = q
(for AG(2,q): 1 line + (q-1) circles).  Of these q blocks, exactly ONE contains
a third point of S (the one determined by the pair {p,q} and that third point)?
No -- the block through p and q containing a third point r of S is determined
by the triple {p,q,r}, and different r give different blocks (since a block
holds at most 3 points of S).  So for fixed q, the number of blocks through
p,q containing a third point of S is (number of r in S\\{p,q} such that
{p,q,r} is on a block) = k-2 (since EVERY triple is on a block!).

So for each q, there are k-2 blocks through p and q that contain a third point
of S.  But the pencil through p and q has only lambda_2 = q blocks!

THEREFORE:  k - 2 <= q,  i.e.  k <= q + 2.

THAT IS THE BOUND!  And it works for ALL q (not just q = 1 mod 4)!

Let me double check.  For fixed p, q in S:
  - the blocks through p and q form a pencil of size lambda_2.
  - for each r in S\\{p,q}, the triple {p,q,r} lies on a block, which must be
    a block through p and q.
  - different r give different blocks (a block holds at most 3 points of S,
    so it cannot contain two different r's together with p,q).
  - hence we need at least k-2 distinct blocks through p and q.
  - so k-2 <= lambda_2.

For AG(2,q): lambda_2 = q (1 line + q-1 circles).  So k <= q+2.
For the inversive plane: lambda_2 = q-1 (circles through two points).  So k <= q+1.

THIS IS A CLEAN GENERAL BOUND!  Let me verify it against the data:
  AG: q=3 K=5 <= 5 OK (tight!)
      q=5 K=6 <= 7 OK
      q=7 K=6 <= 9 OK
      q=9 K=9 <= 11 OK
      q=11 K=9 <= 13 OK
      q=13 K>=13 <= 15 OK
      q=17 K>=17 <= 19 OK
      q=19 K>=13 <= 21 OK
  inversive: q=3 K=5 <= 4 ?? FAILS!

Hmm, inversive q=3: lambda_2 = q-1 = 2, so k <= 4, but K=5.  Contradiction!

Let me recheck.  For the inversive plane of order q, the number of circles
through two points is q-1.  For q=3: 2 circles through any two points.
But K=5.  So the argument must be wrong somewhere.

The error: "different r give different blocks".  A block holds at most 3 points
of S.  If the block contains p, q, r, it has 3 points of S.  Another r' would
need a different block.  So yes, different r give different blocks.

But wait: for q=3 inversive, the circles have 4 points.  A circle through p and
q containing r has 3 points of S.  That is allowed (<= 3).  So different r
should give different circles.  With k=5, we need 3 distinct circles through
p,q, but only 2 exist.  Contradiction.

So either K=5 is wrong for inversive q=3, or the "every triple on a block"
property fails there.

AH -- the inversive plane IS a 3-design, so every triple IS on a circle.  So
the argument applies.  Let me recheck lambda_2 for the inversive plane.

Inversive plane of order q: 3-(q^2+1, q+1, 1) design.  The number of blocks
through 2 points: by design theory, lambda_2 = (v-2)/(s-2) = (q^2-1)/(q-1) = q+1.

I had it wrong!  lambda_2 = q+1, not q-1.

So for the inversive plane: k <= q+3.
  q=3: k <= 6, K=5 OK.
  q=5: k <= 8, K=6 OK.
  q=9: k <= 12, K=9 OK.
  q=13: k <= 16, K=10 OK.

And for AG(2,q): lambda_2 = 1 (line) + (number of circles through 2 points).
The circles through 2 points of AG(2,q): the circle pencil.  For AG(2,q) the
circles are the traces of x^2+y^2+Dx+Ey+F=0.  Through 2 points, how many?
Let me compute it numerically.

This script verifies lambda_2 for both boards and derives the bound.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402
from inversive_bfs import build_field, circles_bfs, projective_line  # noqa: E402


def lambda2(blocks):
    cnt = Counter()
    for b in blocks:
        for pair in itertools.combinations(sorted(b), 2):
            cnt[pair] += 1
    vals = Counter(cnt.values())
    return vals


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7, 9])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        # AG
        pts, blocks, through, nc, nl = build_ag(q)
        vals = lambda2(blocks)
        lam = next(iter(vals)) if len(vals) == 1 else None
        print(f"AG(2,{q}): lambda_2 distribution {dict(sorted(vals.items()))}, "
              f"uniform={len(vals)==1}, lambda_2={lam}", flush=True)
        if lam:
            print(f"   bound k <= lambda_2 + 2 = {lam + 2}", flush=True)
        rows.append({"board": f"AG(2,{q})", "q": q,
                     "lambda2_dist": dict(sorted(vals.items())),
                     "lambda2": lam,
                     "bound": lam + 2 if lam else None})

        # inversive
        F, sub = build_field(q)
        ipts = projective_line(F)
        icirc = circles_bfs(F, sub, ipts)
        idx = {p: i for i, p in enumerate(ipts)}
        iblocks = [sorted(idx[p] for p in c) for c in icirc]
        ivals = lambda2(iblocks)
        ilam = next(iter(ivals)) if len(ivals) == 1 else None
        print(f"inv({q}): lambda_2 distribution {dict(sorted(ivals.items()))}, "
              f"uniform={len(ivals)==1}, lambda_2={ilam}", flush=True)
        if ilam:
            print(f"   bound k <= lambda_2 + 2 = {ilam + 2}", flush=True)
        rows.append({"board": f"inv({q})", "q": q,
                     "lambda2_dist": dict(sorted(ivals.items())),
                     "lambda2": ilam,
                     "bound": ilam + 2 if ilam else None})

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
