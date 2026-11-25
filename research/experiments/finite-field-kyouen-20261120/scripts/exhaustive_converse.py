"""Attempt to PROVE the converse: non-uniform maximal sets => max Grundy >= 2.

Setup.  A finite impartial game where positions are safe sets, moves add one
point, and terminal positions are the maximal safe sets.

THEOREM (proved).  If all maximal sets have size T, then g(S) = (T-|S|) mod 2.

CONVERSE (to prove).  If two maximal sets have different sizes, then some
position has Grundy value >= 2.

PROOF ATTEMPT.

Let A, B be maximal with |A| = a < b = |B|.

Step 1: Consider the position A.  It is maximal, so g(A) = 0.

Step 2: Consider a position S on a path from the empty set to B.  Hmm.

Better approach: use the "height" of a position.

For a position S, let H(S) = { |M| - |S| : M maximal, M ⊇ S } be the set of
possible remaining play lengths.  Note H(S) is nonempty (every position extends
to a maximal one).

CLAIM 1: g(S) = 0 iff every child S' has g(S') != 0.
CLAIM 2: if H(S) = {d} (singleton), then g(S) = d mod 2.  (This is the theorem,
generalised to positions.)

PROOF of CLAIM 2: induct on d.  If d = 0, S is maximal, g = 0.  If d > 0, every
child S' has H(S') = {d-1} (since extending S' to a maximal set gives a maximal
set containing S, and all such have size |S|+d).  By induction g(S') = (d-1) mod 2
for all children, so g(S) = mex{(d-1) mod 2} = d mod 2.  QED.

So: if H(S) is a singleton, g(S) is determined.

Now, the converse.  Suppose A, B maximal with |A| < |B|.  Take S = A ∩ B.
Then H(S) contains both |A| - |S| and |B| - |S|, which differ.  So H(S) is not
a singleton.

Does that force g(S) >= 2?  Not directly.  But consider:

Let d1 = |A| - |S| < d2 = |B| - |S|.

Consider the position S.  Its children S ∪ {p} for p in A\S have H containing
d1 - 1; those for p in B\S have H containing d2 - 1.

Hmm, this is getting complicated.  Let me try a cleaner approach.

CLEANER APPROACH: consider the "parity" function.

Define p(S) = |S| mod 2.  The theorem says: if uniform, g(S) = (T - |S|) mod 2,
i.e., g(S) = (T mod 2) XOR (|S| mod 2).  So g is an affine function of |S| mod 2.

If the game is NOT uniform, then g is not such an affine function.  Since g takes
values in {0,1,2,...}, and g(S) = 0 for maximal S, we need to show some g >= 2.

Suppose for contradiction that g(S) in {0,1} for all S.

Then g is a {0,1}-valued function with g(maximal) = 0 and
g(S) = mex{g(children)}.

Since g in {0,1}: g(S) = 0 iff 0 is not among the children's values, i.e., all
children have g = 1.  And g(S) = 1 iff some child has g = 0.

So: g(S) = 0 iff all children have g = 1; g(S) = 1 iff some child has g = 0.

Now, consider a maximal set A (g=0) and a maximal set B (g=0) with |A| < |B|.

Take a path from ∅ to B: ∅ = S_0 ⊂ S_1 ⊂ ... ⊂ S_b = B, with |S_i| = i.
Since g(B) = g(S_b) = 0, and B is maximal, that is consistent.

Along the path, g alternates?  Not necessarily.

Hmm.  Let me think about the position S = A ∩ B again.

Actually, let me try: consider the position A.  g(A) = 0.  A is maximal.

Now consider B.  g(B) = 0.  B is maximal.

Consider the position C = A ∩ B.  From C, we can reach A (by adding A\C) and B
(by adding B\C).  The play lengths differ.

Let me consider the simplest case: |A| = a, |B| = b = a+1, and |A ∩ B| = a-1
(so A and B differ by one element each: A = C ∪ {x}, B = C ∪ {y} with x ≠ y).

Then C has children including A (g=0) and B (g=0).  So g(C) = mex{0, ...} >= 1.
If all other children of C have g = 1, then g(C) = mex{0,1} = 2.  If some child
has g = 2, then g(C) >= 3.

Hmm, so g(C) >= 1.  To get g(C) >= 2 we need a child with g = 1.

Is there a child of C with g = 1?  A child is C ∪ {z} for z ∉ C.  If z ∈ A\C = {x},
the child is A (g=0).  If z ∈ B\C = {y}, the child is B (g=0).  Other z give
positions C ∪ {z} which are not maximal (they extend to some maximal set).

Hmm, so we need to know whether some C ∪ {z} has g = 1.

Let me think about the general structure.  This is getting deep.  Let me instead
do a computational search for a counterexample with a SMARTER generator: search
over all small hypergraphs exhaustively (not randomly) to see if the converse
ever fails.

n=5, all 4-uniform hypergraphs: 2^5 = 32 possible edges, so 2^32 subsets is too
many.  But we can restrict to small numbers of edges.

Let me do: n=5, all subsets of the 5 four-edges (2^5 = 32 hypergraphs).
n=6, all subsets of the 15 four-edges: 2^15 = 32768, feasible.

Let me run the exhaustive check.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def analyse(n: int, edges: list[tuple[int, ...]]):
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, e in enumerate(edges):
        for i in e:
            through[i].append(bi)

    def can_add(i: int, pmask: int) -> bool:
        for bi in through[i]:
            cnt = 0
            for j in edges[bi]:
                if pmask >> j & 1:
                    cnt += 1
                    if cnt >= 3:
                        return False
        return True

    by_size: dict[int, list[int]] = defaultdict(list)
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        by_size[pmask.bit_count()].append(pmask)
        for i in range(start, n):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask):
                stack.append((i + 1, pmask | (1 << i)))

    g: dict[int, int] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            reach = set()
            for i in range(n):
                if pmask >> i & 1:
                    continue
                if can_add(i, pmask):
                    reach.add(g[pmask | (1 << i)])
            m = 0
            while m in reach:
                m += 1
            g[pmask] = m

    maximal_sizes = Counter()
    for size in by_size:
        for pmask in by_size[size]:
            if all(pmask >> i & 1 or not can_add(i, pmask) for i in range(n)):
                maximal_sizes[size] += 1

    return {
        "n": n,
        "edges": len(edges),
        "maximal_sizes": dict(sorted(maximal_sizes.items())),
        "uniform": len(maximal_sizes) == 1,
        "max_grundy": max(g.values()),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[5, 6])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    counterexamples = []
    for n in args.n:
        all_edges = list(itertools.combinations(range(n), 4))
        total = 1 << len(all_edges)
        print(f"n={n}: {len(all_edges)} possible 4-edges, {total} hypergraphs",
              flush=True)
        if total > 40000:
            print(f"  too many, skipping", flush=True)
            continue
        for mask in range(total):
            edges = [all_edges[i] for i in range(len(all_edges)) if mask >> i & 1]
            if not edges:
                continue
            r = analyse(n, edges)
            r["mask"] = mask
            rows.append(r)
            if not r["uniform"] and r["max_grundy"] <= 1:
                counterexamples.append(r)
        print(f"  checked {total} hypergraphs, counterexamples so far: "
              f"{len(counterexamples)}", flush=True)

    print()
    uniform = [r for r in rows if r["uniform"]]
    nonuniform = [r for r in rows if not r["uniform"]]
    print(f"total: {len(rows)}")
    print(f"  uniform: {len(uniform)}, max Grundy dist "
          f"{dict(sorted(Counter(r['max_grundy'] for r in uniform).items()))}")
    print(f"  non-uniform: {len(nonuniform)}, max Grundy dist "
          f"{dict(sorted(Counter(r['max_grundy'] for r in nonuniform).items()))}")
    print()
    print(f"COUNTEREXAMPLES: {len(counterexamples)}")
    for c in counterexamples[:10]:
        print(f"  n={c['n']} edges={c['edges']} maximal={c['maximal_sizes']} "
              f"maxg={c['max_grundy']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "total": len(rows),
            "uniform": len(uniform),
            "nonuniform": len(nonuniform),
            "counterexamples": counterexamples,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
